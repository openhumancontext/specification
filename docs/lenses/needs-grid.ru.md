# Рецепт линзы: сетка потребностей

**Рецепт · линза `urn:ohc:lens:needs-grid` 0.2.0 · OHC 0.1.0-draft.2 · информативно · 12 октября 2026**

Этот рецепт раскладывает собственные Claim человека в сетку потребностей (шесть строк «хочу», «нужно» и «есть» на трёх горизонтах) и сохраняет её как представление, которое ведёт сам человек, не добавляя ни одного утверждения, которого человек не делал.

Описание линзы — [spec/lenses/needs-grid.lens.json](../../spec/lenses/needs-grid.lens.json); Claim описан в [SPECIFICATION.md §9.4](../../spec/SPECIFICATION.md#94-claim), LensAdoption — в [§10.5](../../spec/SPECIFICATION.md#105-lensadoption), Practice и Outcome — в [§17](../../spec/SPECIFICATION.md#17-practices-and-outcomes), схемы — в [spec/schema/](../../spec/schema/). Общая процедура принятия линзы — [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:needs-grid-basic`](../../spec/playbooks/needs-grid-basic.playbook.json) («Сетка потребностей: базовые способы работы», редакция OHC), для таких ситуаций: планирование предстоящей недели; после неудачи; выбор между вариантами. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

| Что есть | Что это | Куда это идёт |
|---|---|---|
| Самоописание в разговоре | «Хочу закончить лодку», «ещё один курс мне не нужен» | Claim — по одному на каждое высказывание, разложенные по клеткам (шаг 3). Это главный вход. |
| Claim, которые уже есть в контексте | Цели, границы, потребности, ресурсы и умения, записанные раньше | Ничего нового: сетка показывает их там, где им место (шаг 3). |
| Собственный список или лист человека | Заметка, набранный список, скан страницы | Source в хранилище (шаг 2); Claim могут на него ссылаться. |
| Лист с сеткой от коуча или с семинара | То же, но предложенное кем-то другим | Source и путь `self-chosen`: пути `inherited-from-practice` в описании нет (§6). |
| Предложение агента | Помощник предлагает посмотреть на цели, потребности и ресурсы в виде сетки | Путь `agent-suggested` (шаг 4), только после того как человек сам попросил такой обзор. Агент может также предложить пересмотр сетки (шаг 6). Он никогда не заполняет клетки. |
| Отчёты инструментов | — | Нет. Сетка — не оценка, и инструмента у неё нет. |

## 2. Прежде чем начать

**Что это за линза в OHC.** Представление, а не теория: `kind: representation`, `ontologicalStatus: representation`, `measurementTier: not-applicable`. Она ничего не утверждает о доказательствах и **не даёт собственных результатов**: для неё нет AssessmentRecord, ModelView или Interpretation. Сетка вычисляется в момент показа из Claim человека.

**Конструкты.** Строки: `needs-grid/row/want` («хочу»), `…/dont-want` («не хочу»), `…/need` («нужно»), `…/dont-need` («не нужно»), `…/have-can` («есть / могу»), `…/lack-cant` («нет / не могу»). Столбцы: `needs-grid/column/foundation` (годы), `…/focus` (месяцы), `…/state` (часы или дни).

**Правило раскладки в этом рецепте.** OHC 0.1 не определяет, как Claim попадает в строку (§6). Этот рецепт берёт строку из facet записи Claim, для двух строк, которые не выражаются ни одним facet, — из локального predicate, а столбец — из `horizon` записи. `predicate` каждого facet должен быть из собственного списка этого facet ([spec/catalogs/claim-facets.json](../../spec/catalogs/claim-facets.json)) или кодом `x-`; любой другой predicate не проходит CL-8. Одна схема этих списков по facet не показывает (список predicate в ней общий), поэтому пользуйтесь таблицей:

| Строка | `facet` записи Claim | Допустимый `predicate` |
|---|---|---|
| Хочу | `goal` | `outcome`, `habit`, `career`, `learning`, `relationship` |
| Хочу | `interest` | `topic`, `activity` |
| Не хочу | `boundary` | `never`, `only-if`, `ask-first`, `time-window` |
| Нужно | `need` | `rest`, `support`, `autonomy`, `structure`, `connection` |
| Не нужно | `need` | `x-needs-grid:dont-need` |
| Есть / могу | `resource` | `time`, `attention`, `energy`, `money`, `tools`, `network` |
| Есть / могу | `capability` | `skill`, `language-skill`, `tool-skill` |
| Нет / не могу | `resource` или `capability` | `x-needs-grid:lack` |

Predicate необязателен; Claim без него попадает в «положительную» строку своего facet. Столбец = `horizon` (`foundation`, `focus` или `state`). У Claim без `horizon` столбца нет: спросите человека, никогда не угадывайте. Claim с любым другим facet в сетке не показывается.

**Состояния клеток** берутся из производных меток Claim (§6.6 спецификации): **пустая** — нет действующего Claim; **оставлена пустой намеренно** — Claim-отсутствие с `code: "not-chosen"` и `intentional: true`; **устаревшая** — метка ○ устарело (свежесть `review-due`, `expired` или `unknown`); **оспоренная** — метка ⊘ оспорено или Tension между Claim в одной клетке.

**Пути принятия.**

| Путь | Можно | Что он меняет |
|---|---|---|
| `self-chosen` | да | Человек сам пишет принятие (`assertedBy: "subject"`, без `recordedBy`); оно действует сразу, и ни разрешение, ни Review не нужны (шаг 5 пропускается). |
| `agent-suggested` | да | По разрешению, которое позволяет агенту предлагать линзу; рекомендация описания (`suggestionRequires`): «человек попросил обзор своих целей, потребностей и ресурсов». Принятие несёт `suggestedBy` и остаётся `proposed`, пока человек не подтвердит его записью Review `admit` (LA-1). Агенту, который его записывает, нужен Grant с `suggest` или `write`, охват которого включает `LensAdoption` (INF-1). Разобранный пример идёт этим путём. |
| `inherited-from-practice`, `imported` | **нет** | Этих путей нет в описании линзы. |

**Согласие.** Собственные записи человека разрешения не требуют. Помощнику, который предлагает сетку, читает Claim или предлагает пересмотр, сначала нужен Grant (шаг 1). По умолчанию ничто в этой линзе не имеет уровня `special`, поэтому хватает `basis.legal: "consent"` и срока до одного года — если только какой-то Claim в сетке сам не `special` (тогда до него дотягиваются лишь по его id или его особой категории, при явном согласии).

**Что задано по умолчанию для этой линзы.** `defaults.sensitivity: "personal"` и никаких категорий (единственный вид линз, на который не распространяется LN-4). Показываемые Claim сохраняют свои уровни: Claim с `need` по умолчанию `sensitive`, остальные `personal`; любая особая категория поднимает Claim до `special`. Ограничений обращения линза не задаёт.

**Что не хранится никогда.**

- Claim, которого человек не делал, — ни в одной клетке: никаких выведенных потребностей, никаких «вам наверняка ещё нужно…».
- Балл, процент заполненных клеток, индекс баланса или любое другое число о сетке.
- Пометка, что пустая клетка — это проблема. Пустая клетка — законное состояние (`riskNotes` в описании).
- Сама сетка как оценка. Это представление, его каждый раз вычисляют заново.
- Потребности, желания или ресурсы других людей (TP-1). Claim может назвать Party только как вторую сторону цели или границы.

## 3. Шаги

Каждый фрагмент — запись из [разобранного примера](examples/needs-grid/context.json), и он проходит проверку по схеме.

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
  "created": "2026-05-02T18:00:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "vocabulary": {},
  "grants": [], "sources": [], "claims": [], "lensAdoptions": [], "reviews": [], "practices": [], "outcomes": []
}
```

- Схема требует `format`, `specVersion`, `id`, `version` и `subject.id`. `holder`, `lang` и `policy` выше — это выписанные значения по умолчанию. Меняйте `version` с каждым набором изменений.
- **Только для вымышленного человека:** добавьте `"synthetic": true` в корень **и** в каждую содержательную запись. Контекст о реальном человеке этого флага не несёт никогда. Проверка требует оба флага только для папки внутри каталога `examples/` или для `id`, начинающегося с `urn:ohc:example:` (разобранный пример использует `urn:ohc:example:femi:needs-grid`). `tools/ohc_query.py` (шаг 8) строит проекцию без ключа держателя только при флаге в корне.

Затем заполните `conformance`, `parties`, `lenses` и `vocabulary`. Объявите модули, внесите помощника как Party (только если в работе участвует агент), закрепите описание (`sha256` — это SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/needs-grid.lens.json`) и определите два локальных predicate из правила раскладки.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "a-01", "partyKind": "agent", "label": "Planning assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:needs-grid", "version": "0.2.0", "sha256": "75d7db57639e2b6639c2bf0b740613d994111c26a14f528bd7f11cef47c83426"}
],
"vocabulary": {
  "x-needs-grid:dont-need": {"definition": "Needs-grid row 'don't need': something the person states they do not need."},
  "x-needs-grid:lack": {"definition": "Needs-grid row 'lack / can't': something the person states they do not have or cannot do."}
}
```

Проверка не сверяет записи `vocabulary` (она проходит, даже если `vocabulary` убрать, §6). Всё равно определите оба кода: читатели считают неопределённый код `x-` непрозрачным.

### Шаг 1. Разрешить помощнику читать и предлагать: Grant

Нужно, только если агент будет предлагать сетку, читать её или предлагать пересмотр. На пути `self-chosen` без агента этот шаг пропустите, оставьте `parties` пустым и не пишите `delivery` в шаге 6в. Охват — facet, которые показывает сетка, плюс виды записей, которые добавляет линза. Действия — `read` и `suggest`; никогда `infer`.

```json
{"id": "g-01", "recordedAt": "2026-09-30T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["assist-personal"],
 "scope": {"include": [{"kinds": ["LensAdoption", "Practice", "Outcome"]},
                       {"facets": ["goal", "need", "boundary", "resource", "capability"]}]},
 "actions": ["read", "suggest"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-30T09:00:00Z", "channel": "holder-ui"},
 "note": "Help me plan; you may suggest, but you never fill my grid for me."}
```

Селекторы называют виды записей и facet, поэтому достают и Claim с `need` уровня `sensitive` (R-G3(a)). До Claim уровня `special` они не дотягиваются никогда. Если человек называет и интересы, добавьте в facet `"interest"`.

### Шаг 2. Сохранить собственный список человека: Source

Если человек написал список или заполнил лист, положите его в хранилище. Вычислите значения сами, не копируйте их из примера:

1. `sha256` — вывод `shasum -a 256 <файл>` (или `sha256sum <файл>`);
2. `size` — число байтов, `wc -c < <файл>`;
3. переместите файл в `<папка>/vault/<первые два шестнадцатеричных символа sha256>/<sha256>.<расширение>` и запишите этот путь, относительно папки, в `vaultPath`.

Проверка L1 не читает хранилище (`"vaultContentRead": false`): неверный хеш или размер всё равно проходит, поэтому вычисляйте их.

```json
{"id": "src-01", "sourceKind": "note",
 "content": {"locator": {"vaultPath": "vault/20/20541f1223c5cf30469bd239d69b192eb79d8353c7f901ad84e18fc03caf6e4a.md"},
             "sha256": "20541f1223c5cf30469bd239d69b192eb79d8353c7f901ad84e18fc03caf6e4a",
             "mediaType": "text/markdown", "size": 181},
 "capturedAt": "2026-10-04T19:30:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "My list of wants, needs and resources for this season.", "authoredBy": "subject",
             "recordedAt": "2026-10-04T20:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:00:00Z", "synthetic": true}
```

Кто видит: только человек. `maxRelease: "index"`, а у Grant g-01 нет действий с источниками, так что помощник его не получает никогда. Лист от коуча записывается так же, с `authorship.author` — Party коуча и `inbound: true`.

### Шаг 3. Заполнить клетки высказываниями человека: Claim

Один Claim на одно высказывание, словами человека, с facet, predicate и горизонтом по правилу раскладки (§2). Если человек не назвал горизонт — спросите. В разобранном примере такие Claim; `c-08` записан несколькими месяцами раньше и теперь появляется в сетке.

```json
{"id": "c-08", "facet": "need", "predicate": "support",
 "text": "A friend's help with the boat engine this summer.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-05-02T18:05:00Z", "horizon": "focus",
 "synthetic": true}
```

```json
{"id": "c-01", "facet": "goal", "predicate": "outcome",
 "text": "Finish restoring the boat before next summer.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:10:00Z", "horizon": "focus",
 "valid": {"until": "2027-07-01"},
 "evidence": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "subject-statement"}],
 "synthetic": true}
```

```json
{"id": "c-02", "facet": "boundary", "predicate": "never",
 "text": "No school messages on Sundays.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:12:00Z", "horizon": "foundation",
 "synthetic": true}
```

```json
{"id": "c-03", "facet": "need", "predicate": "rest",
 "text": "Two quiet evenings at home this week.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:14:00Z", "horizon": "state",
 "valid": {"from": "2026-10-05", "until": "2026-10-12"}, "synthetic": true}
```

```json
{"id": "c-04", "facet": "need", "predicate": "x-needs-grid:dont-need",
 "text": "I do not need another course this year; I need to use what I already learned.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:16:00Z", "horizon": "focus",
 "evidence": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "subject-statement"}],
 "synthetic": true}
```

```json
{"id": "c-05", "facet": "resource", "predicate": "time",
 "text": "Friday afternoons are free until March.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:18:00Z", "horizon": "focus",
 "valid": {"until": "2027-03-01"}, "synthetic": true}
```

```json
{"id": "c-06", "facet": "resource", "predicate": "x-needs-grid:lack",
 "text": "No budget to rent workshop space this year.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:20:00Z", "horizon": "focus",
 "synthetic": true}
```

Клетка, которую человек намеренно оставляет пустой, — это отсутствие, а не пропущенная запись:

```json
{"id": "c-07", "facet": "goal",
 "absence": {"code": "not-chosen", "intentional": true, "note": "Not naming a life direction right now."},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:22:00Z", "horizon": "foundation",
 "synthetic": true}
```

- Claim с горизонтом `state` получает `valid.until` (иначе его пора пересматривать уже через день, W-CL5).
- `evidence` для собственных Claim человека не обязателен; ссылайтесь на список, если человек хочет к нему возвращаться.

Сетка, которая получается из этих Claim (метки на 10 октября 2026):

| | Основа (годы) | Фокус (месяцы) | Состояние (часы или дни) |
|---|---|---|---|
| **Хочу** | намеренно пусто (`c-07`) | `c-01` | пусто |
| **Не хочу** | `c-02` | пусто | пусто |
| **Нужно** | пусто | `c-08` ○ устарело | `c-03` |
| **Не нужно** | пусто | `c-04` | пусто |
| **Есть / могу** | пусто | `c-05` | пусто |
| **Нет / не могу** | пусто | `c-06` | пусто |

Кто видит: только человек, пока Grant не назовёт их facet. Claim с `need` имеют уровень `sensitive`, остальные — `personal`. Метка у каждого — ✓ заявлено, кроме `c-08` (○ устарело).

### Шаг 4. Записать отношение к линзе: LensAdoption

В примере помощник предложил сетку после того, как человек попросил обзор, и человек согласился. Помощник записывает это «да» **как высказывание самого человека** (`assertedBy: "subject"`, `recordedBy: "a-01"`) в рамках своего Grant. Запись остаётся `proposed`, пока человек её не подтвердит (шаг 5).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:needs-grid", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "needs-grid.grid",
 "origin": "declared", "assertedBy": "subject", "recordedBy": "a-01", "recordedAt": "2026-10-05T09:00:00Z",
 "underGrant": "g-01", "purpose": "assist-personal", "synthetic": true}
```

- `uses`: `speak-in-lens` (говорить строками и клетками) и `offer-practices` (предлагать пересмотр сетки). Не `store-results`: результатов у линзы нет. Не `interpret`: сетка — не теория.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет: сетка — представление, и читать через неё нечего (I5).
- Grant `g-01` должен существовать раньше `la-01`, называть `assist-personal` среди своих целей, давать `suggest` или `write` и включать `LensAdoption` в охват. Ошибка `INF-1` на `la-01/underGrant` обычно значит, что у `g-01` нет `suggest` или `write` или что в его охвате нет `LensAdoption`. Она не значит, что `underGrant` отсутствует.
- Proposal для неё не пишите: PR-1 требует, чтобы предлагающий был автором записи, а агент не может сам быть автором этой записи (§6).
- **Для `self-chosen`** уберите `suggestedBy`, `recordedBy`, `underGrant` и `purpose` и поставьте `"route": "self-chosen"`. Шаг 5 пропустите: принятие действует сразу. Шаг 1 делайте, только если сетку будет читать агент.

Кто видит: пока запись — предложение, только человек; после того как человек её подтвердил, — получатели, чей охват называет `LensAdoption` (уровень `sensitive`).

### Шаг 5. Человек подтверждает принятие: Review

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-10-05T09:10:00Z"}
```

Принятие, предложенное агентом, включает только сам человек (LA-1). Молчание — не согласие.

### Шаг 6. Пересмотреть сетку вместе: Practice, Review и Outcome

Позиция набора `needs-grid.review` (`agentMayOffer: true`, собственной записи не создаёт) — короткая встреча: посмотреть на сетку, отметить пустые, устаревшие и оспоренные клетки и дать человеку решить по каждой: заполнить, обновить или оставить пустой. Записывается это так.

**6а. Пересмотр как практика, которую человек сохраняет у себя**, — пишет сам человек, с `source.route: "from-lens"` и id позиции набора:

```json
{"id": "pr-01", "name": "Monthly grid review",
 "description": "Once a month, look at the grid and decide which cells to fill, update or leave empty.",
 "practiceKind": "planning",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:needs-grid", "templateId": "needs-grid.review"},
 "steps": ["Open the grid", "Mark cells that are empty, stale or contested", "Decide for each: fill, update or leave empty"],
 "duration": "PT20M", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-05T09:20:00Z", "synthetic": true}
```

**6б. Решения человека по клеткам** — записи Review: `confirm-current` для клетки, которая по-прежнему верна, `mark-not-current` для той, что больше не верна. Новые высказывания — новые Claim (шаг 3); изменённое высказывание — новый Claim с `supersedes`; пустая клетка, которую человек хочет оставить пустой, становится Claim-отсутствием, как `c-07`.

```json
{"id": "rv-02", "target": "c-05", "action": "confirm-current", "by": "subject", "recordedAt": "2026-10-05T09:30:00Z"}
```

```json
{"id": "rv-03", "target": "c-08", "action": "mark-not-current", "by": "subject", "recordedAt": "2026-10-05T09:31:00Z",
 "note": "Summer is over; this cell is done."}
```

**6в. Как прошло** — Outcome самого человека. Предложение помощника записывается в `delivery` (если пересмотр не предлагал агент, `delivery` не пишите):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "delivery": {"at": "2026-10-05T09:12:00Z", "by": "a-01", "response": "accepted"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-05T09:40:00Z", "synthetic": true}
```

Кто видит: человек, а также получатели, чей охват называет `Practice` и `Outcome` (обе записи уровня `personal`). Review — записи управления, их видит человек.

### Шаг 7. Прочтения через линзу

Нет. Сетка — представление, а не теория: ни Interpretation, ни ModelView, ни Pattern не называют эту линзу, а рекомендация описания — никогда не выводить потребности из других клеток.

### Шаг 8. Кто что видит

По Grant g-01 (посчитано справочными инструментами на разобранном примере) помощник получает в режиме `summary`: с `c-01` по `c-08`, `la-01`, `pr-01` и `oc-01`, а также свою собственную Party `a-01`, на которую указывают `la-01` и `oc-01`. `c-08` приходит с меткой ○ устарело, и считать её актуальной нельзя (C-5). Помощник никогда не получает `src-01`, записи с ограничением `person-only`, Claim уровня `special` и никакие прочтения. До шага 5 `la-01` не отдаётся никому, кроме самого человека. Селектор `lenses` с этой линзой достал бы только `la-01` и `pr-01`, но не Claim (§6): называйте facet.

Чтобы посчитать это для своего контекста, запустите:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose assist-personal --now 2026-10-10T12:00:00Z
```

Отданные записи появляются в `statements`, `experience`, `interpretations` и `recall`; Party, на которые они указывают, — в `parties`. Контексту без `"synthetic": true` в корне нужен `--holder-key-file`.

### Шаг 9. Проверить

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Ожидается `"valid": true` и `"levelMet": "L1"`. Папку внутри каталога `examples/` проверка сравнивает с её `expected-check.json` (X-3); ваш собственный контекст — нет. Успешная проверка не покрывает того, что, как сказано в шагах, она не ловит: записи `vocabulary` и хеши хранилища.

## 4. Никогда

- Никогда не заполняйте клетку за человека и никогда не вписывайте Claim в сетку без него (`helperMustNot`). Собственная догадка агента о потребности — не клетка; в лучшем случае это отдельное предложение по CONTEXT-02, и не о потребностях, выведенных из других клеток (`agentPosture.dont`).
- Никогда не подавайте сетку как оценку, балл или диагноз и никогда не считайте пустую клетку проблемой, которую надо решить. Никогда не делайте выводов из того, какие клетки пусты (C-8).
- Никогда не предлагайте сетку, если человек не просил обзор своих целей, потребностей и ресурсов (`suggestionRequires`); никогда не включайте принятие сами.
- Никогда не выводите потребности из других клеток и не заполняйте клетки за человека (`agentPosture`, `helperMustNot`); никогда не читайте через сетку сверх разрешения и принятия линзы человека (I5) и не сопоставляйте её с другой линзой (`crossLensMapping: not-allowed`).
- Никогда не используйте сетку или любой Claim в ней для запрещённых целей (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и остальных из §8.10), ни по какому разрешению. Работодатель никогда не видит сетку, чтобы распределять работу.
- Никогда не сравнивайте сетку одного человека с сеткой другого.
- Никогда не кладите в клетку потребности, желания или ресурсы другого человека (TP-1).

## 5. Разобранный пример

[examples/needs-grid/context.json](examples/needs-grid/context.json): Феми, вымышленный учитель музыки, который восстанавливает лодку. Пример содержит ровно записи раздела 3: `g-01`, `src-01`, с `c-01` по `c-08`, `la-01`, `rv-01`, `pr-01`, `rv-02`, `rv-03`, `oc-01`, а также заглушку в хранилище для `src-01`. Корень контекста и каждая содержательная запись несут `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/needs-grid --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений ([expected-check.json](examples/needs-grid/expected-check.json)).

## 6. Что пока не помещается

1. **Нет правила, которое кладёт Claim в строку.** Четыре строки совпадают с facet, но для «не нужно» и «нет / не могу» нет ни facet, ни predicate. Этот рецепт использует локальные predicate, которые занимают место обычного predicate (`c-06` теряет `money`). Предложение: правило раскладки в описании линзы (`representations[].placement`: facet, predicate, полярность → конструкт) и поле `polarity` в Claim (`positive` | `negative`) или predicate `not-needed` и `lacking` в закрытых списках.
2. **Столбцы зависят от необязательного поля.** У Claim без `horizon` нет столбца. Предложение: правило раскладки задаёт столбец по умолчанию для каждого facet, или сетка показывает полосу «не разложено».
3. **Пересмотр сетки не оставляет записи о себе.** Позиция набора ничего не создаёт; то, что смотрели и отмечали, рассыпано по Review, и нет способа сохранить «сетку такой, какой мы видели её 5 октября». Предложение: позволить ModelView (или лёгкой записи-представлению) обслуживать линзы-представления: `scope.claims`, `representation`, без обязательных гипотез.
4. **Агент не может сам записать принятие, которое он предложил.** ENV-2 запрещает `origin: "declared"` для записи агента без `text`, а `inferred` потребовал бы разрешения `infer` ради простого предложения; поэтому агент записывает «да» человека от имени человека и не может подать Proposal (PR-1). Предложение: разрешить `declared` для LensAdoption агента с `route: "agent-suggested"` (и для Practice с `route: "from-agent"`) или добавить код происхождения вроде `suggested`.
5. **Агент, предлагающий пересмотр, не может записать это как своё предложение.** Practice с `source.route: "from-agent"` и `templateId: "needs-grid.review"`, записанная агентом, не проходит ENV-2, если она не `inferred`. Предложение — как в пункте 4.
6. **Селектор линзы не достаёт до сетки.** У Claim нет линзы, поэтому «всё, что показывает моя сетка потребностей» нельзя разрешить, назвав линзу; селектор `lenses` достаёт только `la-01` и `pr-01`, и разрешение должно перечислять facet. Предложение: селектор `lenses` для линзы-представления совпадает с записями, которые показывает её правило раскладки.
7. **Сетку, предложенную коучем, нельзя унаследовать.** Пути — только `self-chosen` и `agent-suggested`. Предложение: разрешить `inherited-from-practice` (с `confidentiality: none`) для линз-представлений.
8. **«Оспоренная клетка» не определена.** Это может быть оспоренный Claim или Tension между двумя Claim в одной клетке. Предложение: определить это в описании линзы.
9. **Локальные коды `x-` не сверяются с `Context.vocabulary`.** Разобранный пример проходит L1 и без `vocabulary`, хотя его predicate — коды `x-needs-grid`. Предложение: правило (предупреждение на L1, ошибка на L2): каждый код `x-`, использованный в записи, определён в `Context.vocabulary`.
10. **Диагностика INF-1 не различает свои причины.** Когда `g-01` даёт только `read`, ошибка говорит, что запись «MUST carry `underGrant` … and `purpose`», хотя оба поля есть; настоящая причина — действия или охват Grant. Предложение: отдельный код (например, INF-2: Grant из `underGrant` не включает `write` или `suggest` либо не покрывает вид или уровень записи) со своим сообщением.
11. **Списки predicate по facet есть только в каталоге.** `claim.schema.json` перечисляет все predicate одним общим списком; какой predicate к какому facet относится, сказано в `claim-facets.json` и проверяется правилом CL-8 (`interest` + `outcome`, `need` + `time` и `goal` + `tools` не проходят). Агент, у которого есть только схемы, этих списков не знает. Предложение: ограничения `if`/`then` по facet в `claim.schema.json` или ссылка на каталог в описании поля `predicate` в схеме.
12. **Флаг `synthetic` в корне не связан с флагами записей.** Вне режима примеров все содержательные записи могут быть синтетическими, а корень — нет; проверка это принимает, а `ohc_query.py` тогда требует ключ держателя. Предложение: предупреждение на L1 при расхождении или выводить флаг корня из записей.
13. **На L1 хранилище не сверяется с Source.** Неверные `sha256` или `size` проходят (`"vaultContentRead": false`). Предложение: проверка по флагу (или на L1, когда хранилище локальное), которая хеширует файлы хранилища и сверяет `sha256` и `size`: ошибка при расхождении, предупреждение, когда файла нет.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
