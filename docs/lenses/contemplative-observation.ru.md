# Рецепт линзы: созерцательное наблюдение

**Рецепт · линза `urn:ohc:lens:contemplative-observation` 0.2.0 · OHC 0.1.0-draft.2 · информативно · 12 октября 2026**

Этот рецепт записывает, что человек созерцательно наблюдает свой опыт, не закрепляя его за устойчивым образом себя, и делает это только безопасными для линзы-заготовки шагами: принятие линзы, собственные слова человека, его практика и источники — и ничего, что агент вычитывает в них сам.

Описание линзы — [spec/lenses/contemplative-observation.lens.json](../../spec/lenses/contemplative-observation.lens.json); LensAdoption описана в [SPECIFICATION.md §10.5](../../spec/SPECIFICATION.md#105-lensadoption), Practice и Outcome — в [§17](../../spec/SPECIFICATION.md#17-practices-and-outcomes), схемы — в [spec/schema/](../../spec/schema/). Общая процедура принятия линзы — [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:contemplative-observation-basic`](../../spec/playbooks/contemplative-observation-basic.playbook.json) («Созерцательное наблюдение: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; после неудачи; разбор того, что произошло. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

| Что есть | Что это | Куда это идёт |
|---|---|---|
| Самоописание в разговоре | «Я сижу каждое утро», «я стараюсь смотреть на мысль, не принимая её за себя» | LensAdoption (шаг 1), простые Claim о том, как работать с человеком (шаг 3), и собственная Practice человека (шаг 4). |
| Дневник практики | Заметки после сидения или после трудного момента | Source в хранилище (шаг 2), на него ссылаются Episode и прочтение человека (шаг 5). |
| Учитель, группа или ретрит | Человек практикует с кем-то | Путь `inherited-from-practice` с блоком `practice` (шаг 1). Собственные заметки учителя хранятся только вместе с его письменным разрешением (шаг 2). |
| Данные приложения для медитации или носимого устройства | Журналы сессий, пульс, баллы «спокойствия» | Самое большее — Source вида `log` со временем сессий. Никакое состояние, настроение или «глубина» из этого не выводится (R-X4). |
| Прочтение агента | — | **Только по разрешению человека.** Агент читает через перспективу только при `infer`, называющем линзу, и действующем принятии линзы не в `off` (I5); прочтения в заготовке остаются `frame-relative`, и упражнений по перспективе агент не проводит (`agentPosture`). В примере человек не разрешает ничего из этого. |
| Отчёт инструмента | — | Нет. У линзы нет инструментов и нет AssessmentRecord. |

## 2. Прежде чем начать

**Эта линза — заготовка.** `descriptorStatus: stub`: перспектива названа, но не описана. У неё нет конструктов, набора инструментов, способов представления, инструментов и разбора доказательств (`measurementTier: not-assessed`). Она не называет ни одной традиции. Поэтому в рецепте оставлены только безопасные шаги: принятие линзы, собственные утверждения человека, практика, эпизоды и прочтения, источники и разрешения. Для этой линзы **нет AssessmentRecord, нет ModelView, нет Interpretation агента, нет Practice от агента, нет Pattern и нет Part**. Каждую содержательную запись ниже пишет сам человек (`assertedBy: "subject"`).

**Пути принятия.**

| Путь | Можно | Что он меняет |
|---|---|---|
| `inherited-from-practice` | да | Человек приносит перспективу из практики с учителем, группой или на ретрите. Нужен блок `practice` (`role: "teacher"`, учитель как Party, `relationship`, `since`). Если хранятся собственные заметки учителя, нужен ещё Source с разрешением учителя, указанный в `practice.releaseRef` (LA-3). Принятие не даёт учителю никакого доступа (LA-2). Разобранный пример идёт этим путём. |
| `self-chosen` | да | Учителя нет. Уберите из принятия блок `practice`, `confidentiality` и `onEnd`, уберите Party учителя и его Source, а источник Practice запишите как `{"route": "self-discovered", "lens": "urn:ohc:lens:contemplative-observation"}` без `by`. Действует сразу. Полный фрагмент — в шаге 1. |
| `agent-suggested` | только как упоминание | Только по разрешению с `suggest`, называющему линзу; рекомендация описания (`suggestionRequires`): агент может упомянуть перспективу только тогда, когда человек просит разные способы взглянуть на свой опыт, как один вариант из нескольких. Если человек её берёт, принятие несёт `suggestedBy`, не имеет блока `practice` и остаётся `proposed`, пока человек не подтвердит его записью Review `admit` (LA-1). Полные фрагменты — в шаге 1. |
| `imported` | необычно | Этого пути нет в описании линзы; пути описывают обычную практику и ничего не ограничивают. Никакая методика не даёт результатов в этой перспективе. |

**Называть традицию.** Описание не называет ни одной, а живую традицию никогда не называют в реестре без согласия её держателей (LN-11). Человек может пользоваться своими словами в своих записях (например, в названии Practice). Если он хочет линзу для рамки своей традиции, напишите локальное описание `urn:ohc:lens:x-<пространство-имён>:<имя>` ([LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses)); это заготовка, она остаётся внутри контекста человека и никогда не публикуется без согласия держателей традиции. Агент никогда не называет, не угадывает и не приписывает традицию.

**Согласие.** Собственные записи человека разрешения не требуют; без Grant никому ничего не раскрывается. Записи, ссылающиеся на эту линзу, имеют уровень `special`: чтобы ими поделиться, нужен Grant с `basis.legal: "explicit-consent"`, селектором, который до них дотягивается, и сроком не дольше 180 дней (R-G3, R-G10). До принятия линзы (`la-01`) и Practice (`pr-01`) дотягивается селектор, называющий линзу или их id. Прочтение человека (`in-01`) — `frame-relative`, и до него дотягивается **только** селектор, называющий линзу; одни id до него не дотягиваются никогда (§12.3, шаг 8).

**Что задано по умолчанию для этой линзы.**

- `sensitivity: "special"`, `categories: ["mental-health"]` у записей, ссылающихся на линзу. Если практика для человека духовная, добавьте `"belief"` (тоже особая категория). Об этом умолчании — в §6.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет; `interpretationAuthors` остаётся `["subject"]`. Человек может изменить и то и другое; учитель из `interpretationAuthors` тогда может быть автором прочтений (I5).
- Прочтениям человека через линзу ставьте `epistemic: "frame-relative"` сами (инструменты для этой линзы его не вычисляют, §6). **Проверка не замечает, если у прочтения нет `epistemic`.** Проверьте это до шага 7: без него прочтение считается `as-reported`, и Grant, называющий его id, его отдаёт.
- Practice, называющая линзу в `source.lens`, не получает умолчаний линзы автоматически: задайте ей `sensitivity` и `categories` вручную.
- С учителем рекомендуется `confidentiality: "practitioner-scope"` и `onEnd: "ask"`. Без учителя оба поля не пишите.

**Что не хранится никогда.**

- Наставления, беседы или тексты учителя, скопированные в записи. Если их вообще хранят, они остаются в хранилище как Source, с разрешением учителя.
- Уровни, ступени, «достижения», оценки глубины или прогресса, любые баллы практики человека.
- Состояния, настроения или «спокойствие» из приложений, носимых устройств или датчиков (R-X4).
- Название традиции, имя учителя или группы, если человек их не называл; настоящие имена кого бы то ни было (подписи Party — общие роли).
- Переживания других участников группы или ретрита (TP-1).

## 3. Шаги

Каждый фрагмент — запись из [разобранного примера](examples/contemplative-observation/context.json), и он проходит проверку по схеме, если он не помечен как вариант (варианты проверены отдельно и тоже проходят L1).

### Шаг 0. Подготовить файл контекста

Заведите папку для контекста. Сохраните файл как `<папка>/context.json`, файлы хранилища кладите в `<папка>/vault/`, а в `check.py` передавайте `<папка>` (не файл). Начните с этой заготовки; шаги ниже заполняют её массивы.

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:uuid:<new random UUID>",
  "version": "1",
  "subject": {"id": "urn:uuid:<another new random UUID>", "displayName": "<what the person wants to be called>"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-20T18:00:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "lensAdoptions": [], "sources": [], "claims": [], "practices": [], "episodes": [],
  "interpretations": [], "outcomes": [], "grants": []
}
```

- Схема требует `format`, `specVersion`, `id`, `version` и `subject.id`. `holder`, `lang` и `policy` выше — это выписанные значения по умолчанию. Меняйте `version` с каждым набором изменений.
- **Только для вымышленного человека:** добавьте `"synthetic": true` в корень **и** в каждую содержательную запись. Контекст о реальном человеке этого флага не несёт никогда. Проверка требует оба флага только для папки внутри каталога `examples/` или для `id`, начинающегося с `urn:ohc:example:` (разобранный пример использует `urn:ohc:example:ondine:contemplative-observation`). `tools/ohc_query.py` (шаг 7) строит проекцию без ключа держателя только при флаге в корне.
- Для пути `agent-suggested` добавьте `"reviews": []`.

Затем заполните `conformance`, `parties` и `lenses`: объявите модули, перечислите Party по общим ролям и закрепите описание (`sha256` — это SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/contemplative-observation.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "p-01", "partyKind": "person", "label": "Practice teacher", "role": "teacher"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0", "sha256": "2dcef40d8a3565c56997241355551d4ec4d4052bd817a74cfd74a874c44e635c"}
]
```

Подпись учителя — общая роль, никогда не имя и не название группы: каждый получатель, которому отдаются принятие линзы или Practice, получает и эту Party (шаг 7).

### Шаг 1. Записать отношение к перспективе: LensAdoption

`uses`: `speak-in-lens` (агент может пользоваться собственными словами человека об этом способе смотреть) и `interpret` (человек может так читать свои эпизоды). Никогда не `offer-practices` и не `store-results`: у заготовки нет ни практик, ни результатов.

Если человек хранит и заметки учителя, сначала сделайте шаг 2: `practice.releaseRef` называет разрешение учителя (`src-03`). Если материалов учителя нет, `releaseRef` не пишите.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "inherited-from-practice",
 "practice": {"role": "teacher", "practitioner": "p-01", "relationship": "active", "since": "2025-02-01", "releaseRef": "src-03"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

Кто видит: только человек. Уровень `special`. Grant дотягивается до записи через селектор, называющий линзу или её id, при явном согласии. Учитель через неё ничего не видит. Когда отношения практики заканчиваются, напишите заменяющую LensAdoption с `practice.relationship: "ended"`; при `onEnd: "ask"` принятие приостанавливается, пока человек не решит.

**Вариант: `self-chosen`** (учителя нет). У принятия нет `practice`, `confidentiality` и `onEnd`; уберите `p-01` из `parties`, пропустите Source учителя в шаге 2 и возьмите источник Practice из шага 4.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "self-chosen", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

**Вариант: `agent-suggested`.** Человек пишет принятие (или диктует его) с `suggestedBy`, называющим агента, без полей учителя, а затем подтверждает его записью Review. Добавьте в заготовку `"reviews": []`; уберите `p-01`, как для `self-chosen`.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "agent-suggested", "suggestedBy": "a-01", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-20T18:05:00Z"}
```

- Пока `rv-01` нет, `la-01` остаётся `proposed` и не отдаётся никому, кроме человека. Запись `admit` может сделать только сам человек (LA-1). Молчание — не согласие.
- Если «да» человека записывает сам агент, добавьте в `la-01` `"recordedBy": "a-01", "underGrant": "g-00", "purpose": "self-reflection"`. Grant `g-00` должен существовать раньше `la-01`, давать `suggest` (или `write`) и иметь охват, который называет и вид записи, и линзу, потому что принятие — особая запись:

```json
{"id": "g-00", "recordedAt": "2026-09-20T17:50:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"kinds": ["LensAdoption"], "lenses": ["urn:ohc:lens:contemplative-observation"]}]},
 "actions": ["read", "suggest"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-20T17:50:00Z", "channel": "holder-ui"}}
```

Ошибка `INF-1` на `la-01/underGrant` здесь обычно значит, что у Grant нет `suggest` или `write` или что его охват не называет линзу. Она не значит, что `underGrant` отсутствует. Ошибка `GR-4` на Grant («`infer` requires…») здесь значит, что Grant дотягивается до особой записи без `explicit-consent`.

### Шаг 2. Сохранить заметки: Source

Запись дневника человека кладётся в хранилище. Для каждого файла хранилища вычислите значения сами, не копируйте их из примера:

1. `sha256` — вывод `shasum -a 256 <файл>` (или `sha256sum <файл>`);
2. `size` — число байтов, `wc -c < <файл>`;
3. переместите файл в `<папка>/vault/<первые два шестнадцатеричных символа sha256>/<sha256>.<расширение>` и запишите этот путь, относительно папки, в `vaultPath`.

Проверка L1 не читает хранилище (`"vaultContentRead": false`): неверный хеш или размер всё равно проходит, поэтому вычисляйте их. Автор дневника — сам человек, поэтому разрешение не нужно.

```json
{"id": "src-01", "sourceKind": "journal-entry",
 "content": {"locator": {"vaultPath": "vault/79/7951165ce25dba1062995826e6716283545f901a54d88483b1abdd5e6cfeea75.md"},
             "sha256": "7951165ce25dba1062995826e6716283545f901a54d88483b1abdd5e6cfeea75",
             "mediaType": "text/markdown", "size": 210},
 "capturedAt": "2026-09-22T21:30:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Practice-journal note after the planning meeting.", "authoredBy": "subject",
             "recordedAt": "2026-09-22T21:35:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-22T21:35:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Заметки учителя — только с его разрешением.** Если человек хочет сохранить заметку, которую ему дал учитель, храните два Source: саму заметку (`practitioner-notes`) и письменное разрешение учителя (`practitioner-release`); у обоих автор — Party учителя, и оба помечены `inbound`. Затем поставьте в `la-01.practice.releaseRef` id разрешения (шаг 1). Заметки учителя без `releaseRef` не проходят LA-3.

```json
{"id": "src-02", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/2f/2f461934c3398118ecb0abf30190545b0719bf98d15ca85a74c8f72e24811914.md"},
             "sha256": "2f461934c3398118ecb0abf30190545b0719bf98d15ca85a74c8f72e24811914",
             "mediaType": "text/markdown", "size": 219},
 "capturedAt": "2026-09-18T20:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:40:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "src-03", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/37/37bf2083edef0444dd571621a9e0690328a8bd6979360b57eb38e7bc096cf8ec.md"},
             "sha256": "37bf2083edef0444dd571621a9e0690328a8bd6979360b57eb38e7bc096cf8ec",
             "mediaType": "text/markdown", "size": 234},
 "capturedAt": "2026-09-19T09:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:45:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- У Source учителя нет `summary`: краткое изложение было бы выборкой из слов учителя.
- Нет `custody`: в OHC 0.1 нет кода конфиденциальности для обучения практике (§6).

Кто видит: только человек. У всех трёх `maxRelease: "index"`: ни один получатель никогда не получит больше вида, типа содержимого и грубой даты.

### Шаг 3. Сказать простыми словами, как работать с человеком: Claim

Сама перспектива остаётся при человеке. Агентам нужно простое: чего не делать и как слушать. У этих Claim нет линзы и нет слов рамки, поэтому их может уважать любой агент, которого выберет человек.

```json
{"id": "c-01", "facet": "boundary", "predicate": "never",
 "text": "Do not offer me breathing, attention or meditation exercises.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:10:00Z", "horizon": "foundation",
 "synthetic": true}
```

```json
{"id": "c-02", "facet": "preference", "predicate": "tone",
 "text": "When I describe a hard moment, ask what I noticed before asking what it means.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:12:00Z", "horizon": "foundation",
 "synthetic": true}
```

Кто видит: только человек, пока Grant их не назовёт. Уровень `personal`, метка ✓ заявлено.

### Шаг 4. Записать собственную практику человека: Practice

С учителем практика идёт от учителя (`source.route: "from-practitioner"`, `source.by: "p-01"`). Она помечена линзой, чтобы ею можно было поделиться одним селектором линзы. `templateId` нет: у заготовки нет набора инструментов. Уровень и категории задайте вручную (§2).

```json
{"id": "pr-01", "name": "Morning sitting",
 "description": "Twenty minutes of sitting and noting before opening email.",
 "practiceKind": "contemplative",
 "source": {"route": "from-practitioner", "by": "p-01", "lens": "urn:ohc:lens:contemplative-observation"},
 "steps": ["Sit before opening email", "Note what arises without following it", "Stop after twenty minutes"],
 "duration": "PT20M",
 "limits": "Not as a fix for a hard day; questions about the practice go to my teacher.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:20:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Вариант: `self-chosen` или `agent-suggested`** (учителя нет). Пишите `"source": {"route": "self-discovered", "lens": "urn:ohc:lens:contemplative-observation"}` без `by`, а в `limits` не упоминайте учителя (например, `"Not as a fix for a hard day."`). Никогда не `from-agent`: ни один агент не предлагает практику из этой линзы.

Шаги — короткие слова самого человека, никогда не текст учителя. Кто видит: только человек; уровень `special`.

### Шаг 5. Эпизод и собственное прочтение его человеком: Episode и Interpretation

Человек рассказывает, что произошло. Если хочет, он читает это так, как учит этот способ смотреть (Interpretation с `lens`, `stance: "lens-reading"`, `epistemic: "frame-relative"`). Это прочтение пишет только сам человек. Добавьте хотя бы одну альтернативу непсихологического вида. На пути `agent-suggested` не пишите прочтений, пока нет `rv-01` (§6, пункт 10).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-22", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-22T21:30:00Z", "addedAt": "2026-09-22T21:35:00Z",
    "accountKind": "in-the-moment",
    "happened": "In the planning meeting my proposal was cut from the budget.",
    "experienced": "A tight jaw, then quieter after a minute.",
    "didOrTried": "Waited before answering; asked when the next budget round opens.",
    "understandingThen": "I thought they did not value my work.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-22T21:35:00Z",
 "sensitivity": "sensitive", "contexts": ["work"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "text": "Watched as it arose, the irritation came and went; it was an event in me, not a verdict on who I am.",
 "grounds": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "evidence"}],
 "alternatives": [
   {"text": "The cut came from the overall budget, not from the quality of my proposal.", "kind": "situational"},
   {"text": "I had skipped lunch and the meeting ran into the afternoon.", "kind": "physiological"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-23T08:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["mental-health"],
 "handling": ["no-quote-back"], "contexts": ["work"], "synthetic": true}
```

Прежде чем идти дальше, проверьте, что у `in-01` есть `"epistemic": "frame-relative"`. Проверка не сообщает, если его нет (§2).

Кто видит: только человек. Episode становится `special`, потому что ссылается на особую запись дневника (C3); прочтение — `special` и `frame-relative`, поэтому до него дотягивается только селектор линзы.

### Шаг 6. Что дала практика: Outcome

Собственная оценка человека, привязанная к эпизоду, где это случилось.

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-01", "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-23T08:05:00Z", "synthetic": true}
```

Кто видит: только человек; уровень записи следует за Practice (`special`).

### Шаг 7. Решить, кто что видит: Grant

Спутник для размышлений может читать то, чем человек делится по этой линзе, чтобы слушать рядом с практикой; у него нет `suggest`, `write` и `infer`. Рабочий помощник видит только простые границу и предпочтение, в режиме `rule-only`.

```json
{"id": "g-01", "recordedAt": "2026-09-24T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:contemplative-observation"]}, {"ids": ["ep-01", "oc-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-24T10:00:00Z", "channel": "holder-ui"},
 "note": "To listen alongside my practice; never to teach it or interpret through it."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-24T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["work-collaboration"],
 "scope": {"include": [{"facets": ["boundary", "preference"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-24T10:05:00Z", "channel": "holder-ui"}}
```

Что получает каждый получатель по §12.3 (посчитано справочными инструментами на разобранном примере):

| Получатель | Отдаётся | Не отдаётся никогда |
|---|---|---|
| `a-01` Спутник для размышлений | `la-01` (вместе с блоком `practice`, где есть голый id `src-03`), `pr-01`, `in-01`, `ep-01`, `oc-01` и Party `p-01` (подпись «Practice teacher», роль `teacher`), потому что на неё указывают `la-01` и `pr-01` | `src-01`, `src-02`, `src-03` (`maxSourceTier: none`); `c-01` и `c-02` (вне охвата) |
| `a-02` Рабочий помощник | `c-01`, `c-02` (только id, facet, predicate и текст) | всё, что ссылается на линзу, эпизод и источники |

Учитель не видит ничего. Спутник же узнаёт, что человек практикует с учителем, под подписью этой Party. Поэтому подпись остаётся общей ролью (§6, пункт 8). Outcome назван по id, потому что линзы у него нет; он отдаётся только вместе со своей Practice.

Чтобы посчитать эту таблицу для своего контекста, запустите для каждого Grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose work-collaboration --now 2026-10-10T12:00:00Z
```

Отданные записи появляются в `statements`, `experience`, `interpretations` и `recall`; Party, на которые они указывают, — в `parties`. Контексту без `"synthetic": true` в корне нужен `--holder-key-file`.

### Шаг 8. Проверить

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Ожидается `"valid": true` и `"levelMet": "L1"`. Папку внутри каталога `examples/` проверка сравнивает с её `expected-check.json` (X-3); ваш собственный контекст — нет. Успешная проверка не покрывает того, что, как сказано в §2, она не ловит: путь принятия, отсутствие `epistemic` у `in-01` и хеши хранилища.

## 4. Никогда

- Никогда не толкуйте через эту линзу от имени агента сверх разрешения человека (`infer`, называющее линзу) и его принятия линзы (I5). Ваши прочтения остаются `frame-relative`. В примере человек оставляет `agentInterpretation: off`, поэтому никаких Interpretation, ModelView, Pattern или AssessmentRecord агента с этой линзой.
- Никогда не проводите по ней упражнений и не давайте наставлений по практике и никогда не выдавайте себя за практикующего или учащего этому подходу (`helperMustNot`). Созерцательная практика принадлежит собственным учителям и традициям человека (`riskNotes`).
- Никогда не заводите речь об этой перспективе сами. Упоминайте её только тогда, когда человек просит разные способы посмотреть, как один вариант из нескольких (`suggestionRequires`), и только по разрешению, которое позволяет её предлагать.
- Никогда не называйте, не угадывайте и не приписывайте традицию и никогда не говорите от её имени (LN-11).
- Никогда не оценивайте практику: никаких уровней, ступеней, глубины, прогресса или сравнения с другими практикующими (`cross-person-ranking`).
- Никогда не выводите состояние, настроение или «спокойствие» из устройств, голоса или поведения (R-X4).
- Никогда не сопоставляйте ничего из этой линзы с другой линзой (`crossLensMapping: not-allowed`), никогда не выдавайте это за эмпирический факт (C-7) и никогда не используйте для запрещённых целей (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и остальных из §8.10), ни по какому разрешению. Прочтение служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял (R-G14). Помощник работодателя никогда не видит записей, ссылающихся на эту линзу.
- Никогда не приводите прочтение человека ему же как довод («вы же сами сказали, что это не приговор…»): `no-quote-back`.
- Никогда не считайте принятие линзы доступом для учителя (LA-2) и никогда не подписывайте Party учителя личным именем.

## 5. Разобранный пример

[examples/contemplative-observation/context.json](examples/contemplative-observation/context.json): Ондина, вымышленный руководитель проектов, которая практикует с учителем. Пример содержит ровно записи раздела 3 (без вариантов): `la-01`, `src-01`, `src-02`, `src-03`, `c-01`, `c-02`, `pr-01`, `ep-01`, `in-01`, `oc-01`, `g-01`, `g-02`, а также три заглушки в хранилище. Корень контекста и каждая содержательная запись несут `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/contemplative-observation --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений ([expected-check.json](examples/contemplative-observation/expected-check.json)).

## 6. Что пока не помещается

1. **Категория по умолчанию называет созерцательную практику «психическим здоровьем».** В описании `defaults.categories` — `["mental-health"]`, тогда как §8.2 относит духовную практику к `belief`. Человек может не хотеть, чтобы его практику помечали как психологическую. Предложение: `defaults.categories: ["belief"]` или выбор между ними в принятии.
2. **Прочтения через доступную заготовку не считаются `frame-relative`, и ничто не предупреждает.** §6.3 называет созерцательные линзы среди рамок, прочтения которых `frame-relative`, и линза без описания так и трактуется (LA-6). Но справочные инструменты вычисляют это только для рамок T5 и символических, так что прочтение через эту заготовку остаётся `as-reported`, если не поставить статус вручную. Прочтение без `epistemic` проходит L1 без предупреждения. Предложение: результаты и прочтения любой заготовки — `frame-relative`; хотя бы предупреждение, когда у прочтения через заготовку нет `epistemic`.
3. **Practice, помеченная линзой, не получает уровень линзы по умолчанию.** C3 перечисляет «умолчание его линзы», но справочные инструменты не применяют его через `Practice.source.lens`: Practice этой линзы без собственного уровня остаётся `personal`. Предложение: применять умолчание линзы через `source.lens` или прямо сказать, что оно не применяется.
4. **У учителя нет кода хранения.** У конфиденциальности хранения есть `therapy`, `coaching`, `legal` и `medical`, но ничего для обучения практике. *Исправлено в 0.1.0-draft.2:* учитель может читать через линзу — LN-10 снято, а I5 применяет `agentInterpretation` только к авторам-агентам и программам; учитель из `interpretationAuthors` действующего принятия может быть автором прочтения. Предложение: код хранения вроде `teaching`.
5. **Нечем пометить, что линзу можно упомянуть, но нельзя применять.** Предлагает ли агент линзу, решает разрешение человека; от упражнений агента защищает лишь текст в `agentPosture` и `helperMustNot`. На практике это несёт граница самого человека (шаг 3, `c-01`). Предложение: машиночитаемое `toolkitUse: "none"` (или `agentMayOffer` на уровне линзы) для заготовок.
6. **Путь принятия не сверяется с путями из описания.** Принятие этой линзы с `imported` проходит проверку; проверяется только `agent-suggested` (LA-1). Предложение: правило, что `route` входит в `adoption.routes` описания.
7. **Поля учителя не привязаны к учителю.** Принятие `self-chosen` с `confidentiality: "practitioner-scope"` и `onEnd: "ask"` без блока `practice` проходит проверку. Проходит и Practice с `source.route: "from-practitioner"` и `by: "p-01"`, когда ни одно принятие не называет `p-01` практиком. У человека без учителя может оказаться практика «от учителя». Предложение: `confidentiality` не `none` и `onEnd` требуют блока `practice`; `Practice.source.by` при пути `from-practitioner` должен быть практиком действующего принятия или Party с ролью `practitioner` или `teacher`.
8. **Получатель всегда получает то, на что указывают отданные записи.** Проекция для `a-01` несёт Party `p-01` (подпись и роль) и весь блок `practice` принятия, включая `releaseRef: "src-03"` — id записи, которую получатель получить не может. Человек не может поделиться перспективой, не показав, что практикует с учителем. Предложение: дать Grant управлять упомянутыми Party (например, `constraints.parties: "include" | "role-only" | "omit"`), по умолчанию скрывать ссылки на практика у линз уровня special и убирать ссылки на записи вне проекции.
9. **Две диагностики указывают не на ту причину.** Для принятия, записанного агентом, когда охват Grant — `{"kinds": ["LensAdoption"]}` без линзы или в действиях нет `suggest`, проверка сообщает INF-1 «MUST carry `underGrant` … and `purpose`», хотя оба поля есть. При `basis.legal: "consent"` GR-4 сообщает «`infer` requires … `explicit-consent`» для Grant без `infer`; настоящая причина — Grant дотягивается до особой записи. Предложение: отдельный код для «названный Grant не покрывает это действие, вид или уровень» (например, INF-2) и сообщение GR-4, которое называет охват особого уровня.
10. **Записи линзы отдаются, пока принятие ещё `proposed`.** На пути `agent-suggested` без `admit` запись `la-01` не отдаётся, но `in-01` и `pr-01` по-прежнему отдаются `a-01` по селектору линзы. Предложение (§12.3): селектор линзы отдаёт записи линзы только пока принятие этой линзы человеком действует.
11. **Флаг `synthetic` в корне не связан с флагами записей.** Вне режима примеров (папка не внутри `examples/`, id не начинается с `urn:ohc:example:`) все содержательные записи могут быть синтетическими, а корень — нет; проверка это принимает, а `ohc_query.py` тогда требует ключ держателя. Предложение: предупреждение на L1, когда все записи синтетические, а корень нет, и наоборот; или выводить флаг корня из записей.
12. **На L1 хранилище не сверяется с Source.** Неверные `sha256` или `size` проходят (`"vaultContentRead": false`), поэтому тот, кто по рецепту скопирует хеш из примера, получит корректный контекст, указывающий не на те байты. Предложение: проверка по флагу (или на L1, когда хранилище локальное), которая хеширует файлы хранилища и сверяет `sha256` и `size`: ошибка при расхождении, предупреждение, когда файла нет.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
