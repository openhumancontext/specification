"""OHC binding checks, separate from ODE's package and runtime validation."""


def is_binding(doc):
    if not isinstance(doc, dict):
        return False
    extensions = doc.get("extensions")
    return (isinstance(extensions, dict) and "ohc.binding" in extensions) or (
        "subjectAlias" in doc and "grantRef" in doc and "checkAtUse" in doc)


def check_binding(doc, path, spec, findings):
    full = doc.get("format") == "digital-employee-package"
    wrapped = "extensions" in doc
    selected = doc
    if full:
        selected = {
            "manifest": {k: doc[k] for k in ("requiredExtensions", "standards") if k in doc},
            "externalDependencies": doc.get("externalDependencies"),
            "extensions": {"ohc.binding": doc["extensions"]["ohc.binding"]},
        }
        if doc.get("specVersion") != "0.4.0-draft":
            findings.add("OB-4", None, path + "#/specVersion")
    errors = spec.validate_detail("urn:ohc:schema:ode-binding:0.1.0-draft", selected)
    if errors:
        findings.add("S-2", None, path + "#" + errors[0][0], detail=errors[0][1])
        return
    if not wrapped:
        findings.add("W-OB1", None, path)
        return
    binding = selected["extensions"]["ohc.binding"]
    context = binding["grantRef"].get("context")
    if not context or "#" in context:
        findings.add("OB-1", None, path + "#/extensions/ohc.binding/grantRef/context")
        return
    target = context + "#" + binding["grantRef"]["id"]
    matches = [dep for dep in selected["externalDependencies"] if dep["objectId"] == target]
    if len(matches) != 1 or matches[0]["version"] != binding["grantVersion"]:
        findings.add("OB-2", None, path + "#/externalDependencies")
    standards = [row for row in selected["manifest"].get("standards", []) if row["id"] == "ohc"]
    if len(standards) != 1 or standards[0]["revision"] != "0.1.0-draft" or \
            standards[0]["url"] != "urn:ohc:specification":
        findings.add("OB-3", None, path + ("#/standards" if full else "#/manifest/standards"))
