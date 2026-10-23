"""Catalogs, schemas and the type catalog; enum generation (§5.10, S-4).

``Spec`` loads everything the tools need from a specification checkout:

- ``spec/schema/index.json`` and every schema it lists (one registry by ``$id``);
- ``spec/schema/type-catalog.json`` (layer, module, collection and default tier per kind);
- ``spec/catalogs/*.json`` (controlled vocabularies with their extra data);
- ``spec/lenses``, ``spec/instruments``, ``spec/mappings`` and ``spec/playbooks`` (registry documents).

Vocabulary ``$defs`` in ``common.schema.json`` are generated from the catalogs:
a catalog without ``lists`` gives one ``$def`` named after the file; a catalog with
``lists`` gives one ``$def`` per list, named ``<catalog>.<list>``. A closed list is
``{"enum": [...]}``; an open list also accepts a local ``x-`` code.
"""

import glob
import os

from . import jsonio

TIERS = ("ordinary", "personal", "sensitive", "special")
RELEASE_TIERS = ("none", "index", "summary", "excerpt", "verbatim")
COMMON_ID = "urn:ohc:schema:common:0.1.0-draft"


def default_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def tier_rank(tier):
    return TIERS.index(tier) if tier in TIERS else 0


def max_tier(*tiers):
    best = None
    for tier in tiers:
        if tier is None:
            continue
        if best is None or tier_rank(tier) > tier_rank(best):
            best = tier
    return best


def release_rank(tier):
    return RELEASE_TIERS.index(tier) if tier in RELEASE_TIERS else 0


def min_release(*tiers):
    best = None
    for tier in tiers:
        if tier is None:
            continue
        if best is None or release_rank(tier) < release_rank(best):
            best = tier
    return best


def generated_enum_defs(catalogs):
    """Return ``{def_name: schema}`` for every catalog that generates an enum."""
    defs = {}
    for name in sorted(catalogs):
        catalog = catalogs[name]
        if catalog.get("generatesEnum", True) is False:
            continue
        if "lists" in catalog:
            for item in catalog["lists"]:
                codes = [c["code"] for c in catalog["codes"] if c.get("list") == item["name"]]
                defs[name + "." + item["name"]] = _enum(codes, item["closed"])
        else:
            defs[name] = _enum([c["code"] for c in catalog["codes"]], catalog["closed"])
    return defs


def _enum(codes, closed):
    if closed:
        return {"enum": list(codes)}
    return {"anyOf": [{"enum": list(codes)}, {"$ref": "#/$defs/LocalCode"}]}


def is_vocab_def(name):
    return name[:1].islower()


def merge_enum_defs(common_schema, enum_defs):
    """Return a copy of common.schema.json whose vocabulary ``$defs`` equal ``enum_defs``.

    Structural ``$defs`` (capitalised names) keep their order; vocabulary ``$defs``
    follow, sorted by name.
    """
    result = {}
    for key, value in common_schema.items():
        if key != "$defs":
            result[key] = value
    defs = {}
    for key, value in common_schema.get("$defs", {}).items():
        if not is_vocab_def(key):
            defs[key] = value
    for key in sorted(enum_defs):
        defs[key] = enum_defs[key]
    result["$defs"] = defs
    return result


class Spec(object):
    """Everything loaded from a specification checkout."""

    def __init__(self, root=None, registries=None):
        self.root = os.path.abspath(root or default_root())
        # Extra registry directories (``lenses/``, ``instruments/``, ``playbooks/``, ``mappings/``): local drafts
        # that resolve like catalog entries for a context check. The published catalog never includes them.
        self.registries = [os.path.abspath(r) for r in registries or []]
        self.schema_dir = os.path.join(self.root, "spec", "schema")
        self.catalog_dir = os.path.join(self.root, "spec", "catalogs")
        self._load_schemas()
        self._load_catalogs()
        self._load_types()
        self._load_registry()
        self._validators = {}

    # ---------------------------------------------------------------- schemas
    def _load_schemas(self):
        self.index = jsonio.load_json(os.path.join(self.schema_dir, "index.json"))
        self.schemas = {}
        self.schema_paths = {}
        self.by_format = {}
        self.by_kind = {}
        self.by_name = {}
        for entry in self.index["schemas"]:
            path = os.path.join(self.schema_dir, entry["path"])
            schema = jsonio.load_json(path)
            self.schemas[entry["id"]] = schema
            self.schema_paths[entry["id"]] = path
            self.by_name[entry["name"]] = entry["id"]
            if entry.get("format"):
                self.by_format[entry["format"]] = entry["id"]
            if entry.get("kind"):
                self.by_kind[entry["kind"]] = entry["id"]
        self.common = self.schemas[COMMON_ID]

    def registry(self):
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012

        resources = []
        for schema_id, schema in self.schemas.items():
            resources.append((schema_id, Resource.from_contents(schema, default_specification=DRAFT202012)))
        return Registry().with_resources(resources)

    def validator(self, schema_id):
        if schema_id not in self._validators:
            from jsonschema import Draft202012Validator

            if not hasattr(self, "_registry"):
                self._registry = self.registry()
            self._validators[schema_id] = Draft202012Validator(self.schemas[schema_id], registry=self._registry)
        return self._validators[schema_id]

    def validate(self, schema_id, value):
        """Return a list of error paths (JSON pointers) for ``value``; values are never echoed."""
        errors = []
        for error in self.validator(schema_id).iter_errors(value):
            errors.append("/" + "/".join(str(p) for p in error.absolute_path))
        return sorted(set(errors))

    def validate_detail(self, schema_id, value):
        """Like ``validate``, with a short explanation per error: ``[(pointer, detail)]``.

        The detail names the failing JSON Schema keyword and schema-defined names only (a missing property, the
        expected type, a vocabulary's codes). A key the writer typed is named only when it is a near miss of a
        schema property ("did you mean ..."); values are never echoed.
        """
        out = []
        for error in self.validator(schema_id).iter_errors(value):
            out.append(_explain_error(error))
        out.sort(key=lambda pair: pair[0])
        unique, seen = [], set()
        for pointer, detail in out:
            if (pointer, detail) not in seen:
                seen.add((pointer, detail))
                unique.append((pointer, detail))
        return unique

    def validator_for_subschema(self, schema_id, pointer):
        """A validator for a ``$defs`` subschema of a registered schema."""
        key = schema_id + "#" + pointer
        if key not in self._validators:
            from jsonschema import Draft202012Validator

            if not hasattr(self, "_registry"):
                self._registry = self.registry()
            self._validators[key] = Draft202012Validator({"$ref": key}, registry=self._registry)
        return self._validators[key]

    # --------------------------------------------------------------- catalogs
    def _load_catalogs(self):
        self.catalogs = {}
        for path in sorted(glob.glob(os.path.join(self.catalog_dir, "*.json"))):
            name = os.path.basename(path)[:-5]
            self.catalogs[name] = jsonio.load_json(path)
        cat = self.catalogs
        self.categories_min = {c["code"]: c.get("minimumTier", "personal") for c in cat["categories"]["codes"]}
        self.review_actions = {c["code"]: c for c in cat["review-actions"]["codes"]}
        self.labels = {c["code"]: c for c in cat["labels"]["codes"]}
        self.label_order = [c["code"] for c in sorted(cat["labels"]["codes"], key=lambda c: c.get("precedence", 0))]
        self.default_intervals = dict(cat["freshness"].get("defaultIntervals", {}))
        self.kind_defaults = {c["code"]: c for c in cat["kind-defaults"]["codes"]}
        self.relation_codes = {c["code"]: c for c in cat["relation-codes"]["codes"]}
        self.biometric_kinds = set(c["code"] for c in cat["source-kinds"]["codes"] if c.get("biometricOrBehavioural"))
        self.source_kind_tier = dict((c["code"], c.get("defaultTier")) for c in cat["source-kinds"]["codes"])
        self.reference_targets = {}
        for code in (cat.get("reference-targets") or {}).get("codes") or []:
            targets = set()
            for endpoint in code.get("endpoints") or []:
                targets.update(endpoint.get("to") or [])
            self.reference_targets[code["code"]] = targets
        self.handling_codes = set(c["code"] for c in cat["handling"]["codes"])
        self.custody = {c["code"]: c for c in cat["custody"]["codes"]}
        grant = cat["grant"]["codes"]
        self.grant_actions = {c["code"]: c for c in grant if c.get("list") == "actions"}
        self.assessment_modes = {c["code"]: c for c in cat["assessment"]["codes"] if c.get("list") == "modes"}
        self.modules = {c["code"]: c for c in cat["modules"]["codes"]}
        self.kind_module = {}
        for module in self.modules.values():
            for kind in module.get("kinds", []):
                self.kind_module[kind] = module["code"]
        facets = cat["claim-facets"]["codes"]
        self.facet_predicates = {}
        for code in facets:
            if code.get("list") == "facets":
                if code.get("predicatesCatalog") == "urn:ohc:catalog:relationship-kinds":
                    self.facet_predicates[code["code"]] = set(
                        c["code"] for c in cat["relationship-kinds"]["codes"])
                else:
                    self.facet_predicates[code["code"]] = set(code.get("predicates", []))
        self.facet_family = dict((c["code"], c.get("facetFamily")) for c in facets if c.get("list") == "facets")
        self.prohibited_purposes = set(c["code"] for c in cat["prohibited-purposes"]["codes"])
        self.purposes = set(c["code"] for c in cat["purposes"]["codes"])
        self.content_kinds = [c["code"] for c in cat["content-kinds"]["codes"]]
        self.id_prefixes = {c["code"]: c["kinds"] for c in cat["id-prefixes"]["codes"]}

    def codes(self, catalog, list_name=None):
        items = self.catalogs[catalog]["codes"]
        if list_name is not None:
            items = [c for c in items if c.get("list") == list_name]
        return [c["code"] for c in items]

    def enum_defs(self):
        return generated_enum_defs(self.catalogs)

    def regenerate_common(self):
        return merge_enum_defs(self.common, self.enum_defs())

    # ---------------------------------------------------------- type catalog
    def _load_types(self):
        path = os.path.join(self.schema_dir, "type-catalog.json")
        self.type_catalog = jsonio.load_json(path)
        self.types = {t["kind"]: t for t in self.type_catalog["types"]}
        self.collection_kind = {}
        self.kind_collection = {}
        self.kind_file = {}
        for kind, item in self.types.items():
            if item.get("collection"):
                self.collection_kind[item["collection"]] = kind
                self.kind_collection[kind] = item["collection"]
                self.kind_file[kind] = item.get("file")
        self.layers = {kind: item["layer"] for kind, item in self.types.items()}

    def layer(self, kind):
        return self.layers.get(kind)

    def module_of(self, kind):
        return self.types.get(kind, {}).get("module") or self.kind_module.get(kind)

    def maturity(self, kind):
        return self.types.get(kind, {}).get("maturity")

    def default_tier(self, kind):
        return self.types.get(kind, {}).get("defaultTier")

    # -------------------------------------------------------------- registry
    def _load_registry(self):
        self.lenses = {}
        self.lens_paths = {}
        self.instruments = {}
        self.mappings = {}
        self.playbooks = {}
        self.playbook_paths = {}
        roots = [os.path.join(self.root, "spec")] + self.registries
        for base in roots:
            for path in sorted(glob.glob(os.path.join(base, "lenses", "*.lens.json"))):
                doc = jsonio.load_json(path)
                self.lenses[doc["id"]] = doc
                self.lens_paths[doc["id"]] = path
            for path in sorted(glob.glob(os.path.join(base, "instruments", "*.instrument.json"))):
                doc = jsonio.load_json(path)
                self.instruments[doc["id"]] = doc
            for path in sorted(glob.glob(os.path.join(base, "mappings", "*", "*.mapping.json"))):
                doc = jsonio.load_json(path)
                self.mappings[doc["id"]] = doc
            for path in sorted(glob.glob(os.path.join(base, "playbooks", "*.playbook.json"))):
                doc = jsonio.load_json(path)
                self.playbooks[doc["id"]] = doc
                self.playbook_paths[doc["id"]] = path

    def lens(self, lens_id):
        return self.lenses.get(lens_id)

    def playbook(self, playbook_id):
        return self.playbooks.get(playbook_id)


def _pointer(path):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in path) if path else "/"


def _leaf(error):
    """The most specific error under an anyOf/oneOf, preferring errors about the deepest instance location."""
    from jsonschema.exceptions import best_match

    seen = 0
    while error.context and seen < 8:
        candidate = best_match(error.context)
        if candidate is None:
            break
        error = candidate
        seen += 1
    return error


def _explain_error(error):
    import difflib

    error = _leaf(error)
    keyword = error.validator
    pointer = _pointer(list(error.absolute_path))
    schema = error.schema if isinstance(error.schema, dict) else {}
    instance = error.instance
    if keyword == "required" and isinstance(instance, dict):
        missing = [name for name in error.validator_value if name not in instance]
        return pointer.rstrip("/") + "/" + (missing[0] if missing else ""), "required: %s" % (
            missing[0] if missing else "a property")
    if keyword == "additionalProperties" and isinstance(instance, dict):
        known = list((schema.get("properties") or {}).keys())
        extra = [k for k in instance if k not in known]
        hint = ""
        for key in extra:
            close = difflib.get_close_matches(key, known, n=1, cutoff=0.75)
            if close:
                hint = "; did you mean %s?" % close[0]
                break
        return pointer, "additionalProperties: unknown property" + hint
    if keyword == "type":
        expected = error.validator_value
        expected = " or ".join(expected) if isinstance(expected, list) else expected
        return pointer, "type: expects %s" % expected
    if keyword == "enum":
        values = [v for v in error.validator_value if isinstance(v, str)]
        if 0 < len(values) <= 24:
            return pointer, "enum: expected one of %s" % ", ".join(values)
        return pointer, "enum: not a code of this vocabulary (see spec/catalogs/)"
    if keyword == "const":
        value = error.validator_value
        if isinstance(value, (str, bool, int)) and not isinstance(value, float):
            return pointer, "const: expects %s" % json_text(value)
        return pointer, "const"
    if keyword == "pattern":
        return pointer, "pattern: does not match the expected form"
    if keyword in ("minItems", "maxItems", "minLength", "maxLength", "minimum", "maximum", "minProperties"):
        return pointer, "%s: %s" % (keyword, error.validator_value)
    if keyword == "not":
        return pointer, "not: a combination of members that is not allowed"
    return pointer, keyword


def json_text(value):
    import json

    return json.dumps(value)

