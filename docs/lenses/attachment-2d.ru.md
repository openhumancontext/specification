# Привязанность у взрослых (два измерения): рецепт

**Рецепт · линза `urn:ohc:lens:attachment-2d` 0.2.0 · OHC 0.1.0-draft.2 · информативный · 12 октября 2026**

Рецепт показывает, как человек переносит в свой контекст OHC свой результат опросника о привязанности у взрослых (два балла: тревожность и избегание в привязанности) и то, что он в нём узнаёт, так, чтобы это оставалось про него самого, никогда не про его партнёра и никогда не попадало в рабочий контекст.

Описание линзы — [spec/lenses/attachment-2d.lens.json](../../spec/lenses/attachment-2d.lens.json) (`descriptorStatus: draft`, уровень измерения T2). Её единственный опросник — [ECR-R](../../spec/instruments/ecr-r.instrument.json): 36 пунктов, результат — два средних по шкалам от 1 до 7.

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:attachment-2d-basic`](../../spec/playbooks/attachment-2d-basic.playbook.json) («Привязанность у взрослых: базовые способы работы», редакция OHC), для таких ситуаций: подготовка к трудному разговору в близких отношениях; после неудачи в близких отношениях; разбор того, что произошло в близких отношениях. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Подходит? | Куда это идёт |
|---|---|---|
| Результат опросника, который принадлежит человеку: страница или лист с двумя средними ECR-R | да | Source (шаг 2) и AssessmentRecord (шаг 3) |
| Слова самого человека: за чем он следит в близости, что узнаёт в баллах | да | Claims (шаг 4) |
| Случай в близких отношениях в рассказе человека | да | Episode и собственное прочтение человека (шаг 5) |
| Заметки из терапии или коучинга, где обсуждались баллы | да, с разрешением практика | путь `inherited-from-practice` (роли `therapist` или `coach`) и Source вида `practitioner-notes` под защитой конфиденциальности, как в [рецепте процессуального подхода](process-work.ru.md), шаги 1–2 |
| Результат другого опросника, теста или приложения (например, «стиль» из четырёх категорий) | не как результат | у линзы есть только ECR-R (AR-8). Сохраните слова человека как Claim или опишите ту систему как локальную линзу ([LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses)) |
| Оценка баллов агентом или прочтение агента через линзу | **только по разрешению человека** | `suggest` и `infer`, называющие линзу, действующее принятие линзы не в `off` (I5) и для оценки — признаки «только для человека» (AR-2). Рекомендация описания: никогда не поднимать тему первым. В примере человек не разрешает ничего из этого. |

## 2. Перед началом

**Путь принятия линзы.** Описание разрешает все четыре пути (`adoption.routes`).

| Путь | Кто пишет LensAdoption | Что это меняет |
|---|---|---|
| `self-chosen` | сам человек (`assertedBy: "subject"`) | Действует сразу. Рецепт идёт этим путём. |
| `agent-suggested` | агент, как предложение | Только по разрешению, которое позволяет агенту предлагать линзу (`suggest` с селектором, называющим её); `suggestionRequires` в описании говорит когда: после того как человек попросил другие способы взглянуть на близкие отношения, и только как один вариант. Сам агент эту тему не поднимает (`agentPosture`). Принятие остаётся предложением, пока человек его не примет (LA-1). Шаги показаны в [рецепте когнитивной оценки](cognitive-appraisal.ru.md). |
| `inherited-from-practice` | сам человек | Блок `practice` с ролью `therapist` или `coach`, практик как Party, `confidentiality` и `releaseRef`, если хранятся заметки сессий (LA-3, LA-4). |
| `imported` | программа импорта | Программа импорта создаёт принятие и AssessmentRecord из файла с результатами. Оба остаются предложениями, пока человек их не примет (LA-5). Для пакета это делает `tools/import_assessment.py` с `--adopt`. |

**Согласие.** Человек решает, принимать ли линзу, что хранить и кому показывать. Без Grant ничего не уходит из контекста (R-G1). Разрешающий Grant, который достаёт до записей этой линзы, даётся с `basis.legal: "explicit-consent"` и истекает не позже чем через 180 дней от своего `recordedAt` (R-G10, R-G11, GR-1). У отказа (`effect: deny`) предела срока нет, поэтому отказ `g-02` в шаге 7 может действовать пять лет.

**Умолчания линзы** (`defaults`): уровень чувствительности `special`, категория `intimate`, `reviewAfter: P2Y`.

- LensAdoption, AssessmentRecord и каждая Interpretation, где указана линза, — уровня `special` (AR-5, I9). Ставьте им `"categories": ["intimate"]`.
- У Claims, Episodes и Sources нет поля `lens`, поэтому умолчания линзы до них не доходят. Claim, выведенный из AssessmentRecord или ссылающийся на него как на основание, наследует `special` и `intimate` по C3 (§8.4); Episode — нет. Всё равно поставьте `"sensitivity": "special"` и `"categories": ["intimate"]` вручную на все такие записи, чтобы это было видно в самой записи. Episode, где участвует партнёр, получает ещё `third-party`.
- Ограничения, которые подходят этой линзе: `subject-initiated-only` (агент сам не поднимает тему), `no-quote-back` (никогда «по вашим баллам вы тревожный»), `no-leverage`.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет; `interpretationAuthors` равно `["subject"]`. Человек может изменить и то и другое (I5).
- `uses`: `store-results`, `speak-in-lens`, `interpret` (собственные прочтения человека).

**Что не хранится никогда.** Тексты пунктов ECR-R, формулировки пунктов на сохранённой странице, ключ подсчёта (какие пункты обратные), сырые ответы на пункты вне личных тестовых данных человека, текст отчёта. Категория или «стиль» как будто это измеренный результат. Ярлык из другого опросника или приложения, переименованный в понятия этой линзы. Что-либо о привязанности партнёра или другого человека (TP-1). Балл как оценка человека.

**Пометка «вымышлено».** В примерах (контекст, чей `id` начинается с `urn:ohc:example:`, или любая папка `examples` в пути) поставьте `"synthetic": true` на сам Context и на каждый Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice и Outcome (X-1, CX-8). Никогда не ставьте его на Grant, Proposal, Review или Event и на Party: их схемы это запрещают (S-3). Для реального человека не ставьте его нигде.

## 3. Шаги

**0. Создайте файл контекста.** Заведите папку для контекста и создайте в ней `context.json` (контекст одним документом). Начните с такой заготовки:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-14T21:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "lenses", "governance"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` и `subject` обязательны. Меняйте `version` при каждом изменении файла.
- `conformance.subjectIsAdult: true` — заявление хранителя, что человек взрослый и решает за себя сам. Без него проверка отклоняет любое заявление о соответствии (R-C4), и `levelMet` равно `null`. Без `conformance.level` проверка проверяет только L0.
- `modules`: всегда `core` и `lenses`, `governance` — для разрешений (шаг 7).
- `lenses` закрепляет описание линзы, которым пользуется контекст.
- Каждая запись ниже ложится в массив верхнего уровня, названный по её коллекции: `lensAdoptions`, `sources`, `assessments`, `claims`, `episodes`, `interpretations`, `grants`. Каждая Party ложится в `parties`.
- В примере берите id вида `urn:ohc:example:<имя>:attachment-2d` (контекст) и `urn:ohc:example:<имя>` (человек) и добавьте `"synthetic": true` на сам Context (см. раздел 2).

**1. Примите линзу.** Запишите **LensAdoption** (коллекция `lensAdoptions`):

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["store-results", "speak-in-lens", "interpret"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "attachment-2d.two-dimension-plot",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T21:05:00Z",
 "sensitivity": "special", "categories": ["intimate"], "handling": ["subject-initiated-only"]}
```

Кто видит по умолчанию: только сам человек.

**2. Положите страницу с баллами в хранилище.** Сохраните только два средних по шкалам. Проще всего — и так сделано в разобранном примере — вписать их в свой короткий файл JSON такого вида (одной строкой; в примере добавьте `"synthetic": true`). Если вместо этого храните саму страницу, сначала уберите с неё формулировки пунктов.

```json
{"instrument": "ECR-R", "form": "36", "takenOn": "2026-09-14", "scaleMeans": {"anxiety": 4.2, "avoidance": 2.3}, "range": [1, 7]}
```

Папка `vault/` лежит рядом с `context.json`, и каждый `vaultPath` отсчитывается от папки, где лежит `context.json`. Затем:

1. посчитайте sha256 байтов файла командой `shasum -a 256 <файл>` (или `sha256sum <файл>`) и размер в байтах командой `wc -c < <файл>`;
2. сохраните файл как `vault/<первые два шестнадцатеричных знака>/<sha256>.<расширение>`;
3. запишите **Source** (коллекция `sources`) с этим путём, хешем и размером.

Проверка не открывает хранилище (в её отчёте `"vaultContentRead": false`). Пропавший или пустой файл, неверный хеш или размер всё равно пройдут шаг 8, поэтому сверьте путь, `sha256` и `size` сами до шага 8.

Страница, которая посчитала баллы, — это Party: `{"id": "s-01", "partyKind": "software", "label": "Questionnaire scoring page"}`.

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/90/9009fc94cbbec1b99c895cb69ba4fcee3fdfd7091ec12bbe9f4ac45e01e67503.json"},
             "sha256": "9009fc94cbbec1b99c895cb69ba4fcee3fdfd7091ec12bbe9f4ac45e01e67503",
             "mediaType": "application/json", "size": 149},
 "capturedAt": "2026-09-14T21:10:00Z", "authorship": {"author": "s-01"}, "inbound": true, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T21:15:00Z",
 "sensitivity": "special", "categories": ["intimate"]}
```

Кто видит по умолчанию: только сам человек. `maxRelease: index` не пускает к самой странице никого из получателей.

**3. Запишите результат.** Это **AssessmentRecord** (коллекция `assessments`). Заполняйте так:

- `instrument.id` должен быть в списке `instruments` линзы (AR-8): `urn:ohc:instrument:ecr-r`, `form: "36"`.
- `instrument.version` — издание так, как его называет издатель (у ECR-R: `"2000"`), а не версия описания опросника в OHC (`0.1.0`). Если на странице с баллами издание не указано, не пишите это поле.
- `mode: self-report-instrument`, с `origin: derived`, `generatedBy.method` (опубликованное правило подсчёта) и `derivedFrom` (этот Source) (AR-1). Копия отчёта поставщика, сделанная программой импорта, — это `vendor-report-import` с `origin: imported` и `importedFrom`.
- `results`: по одному `dimension-score` на измерение, с id конструктов `attachment-2d/anxiety` и `attachment-2d/avoidance`, `raw` и `rawRange: [1, 7]`. `standardized` и `normGroup` добавляйте, только если они есть в отчёте; процентиль никогда не придумывайте.
- `validityFlags`: `incomplete`, если пункты пропущены, `translated-form` для перевода, иначе `[]`.
- Для того, о ком отношения (романтические партнёры вообще или одни отношения), поля пока нет: поставьте сферу жизни в `contexts` и скажите это в `note` (см. раздел 6).
- Категорию не храните. У линзы нет конструктов-категорий (см. раздел 6). Проверка не ловит ни сохранённую категорию, ни id конструкта, которого нет в линзе, поэтому до шага 8 убедитесь, что в `results` ровно две записи, обе `dimension-score`, с конструктами `attachment-2d/anxiety` и `attachment-2d/avoidance`.
- `trademarkNotice` не нужен: у линзы нет товарных знаков.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:ecr-r", "version": "2000", "form": "36"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-09-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "attachment-2d/anxiety", "label": "Attachment-related anxiety",
    "raw": 4.2, "rawRange": [1, 7]},
   {"type": "dimension-score", "construct": "attachment-2d/avoidance", "label": "Attachment-related avoidance",
    "raw": 2.3, "rawRange": [1, 7]}],
 "validityFlags": [],
 "reviewAfter": "P2Y", "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "questionnaire scoring page",
                 "method": "mean of the 18 items of each scale after recoding reverse-keyed items"},
 "derivedFrom": ["src-01"], "formulatedAt": "2026-09-14T21:10:00Z",
 "assertedBy": "subject", "recordedAt": "2026-09-14T21:20:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"],
 "handling": ["no-quote-back", "no-leverage", "subject-initiated-only"],
 "note": "Relationship target: romantic partners in general, as the questionnaire asks. Not about one person."}
```

Кто видит по умолчанию: только сам человек.

**4. Запишите только то, что человек принимает.** Покажите человеку два балла и спросите, что он узнаёт. Для измерения, которое, по словам человека, подходит, запишите производный **Claim** (коллекция `claims`), который переносит число:

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Attachment-related anxiety: 4.2 on the 1 to 7 scale (questionnaire, 14 September 2026).",
 "value": 4.2, "unit": "scale mean, 1-7", "horizon": "foundation", "reviewAfter": "P2Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "manual entry", "method": "copy of one scale mean from as-01, at the person's request"},
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"],
 "handling": ["no-quote-back", "subject-initiated-only"]}
```

То, что человек узнаёт, его собственными словами, — это заявленный Claim, который ссылается на результат как на основание:

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When someone close to me goes quiet, I start checking whether something is wrong.",
 "evidence": [{"ref": "as-01", "kind": "instrument"}], "horizon": "foundation",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-15T08:05:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"], "handling": ["no-quote-back"]}
```

Измерение, которое человек не узнаёт, Claim не получает; его балл остаётся только в AssessmentRecord. Кто видит Claims по умолчанию: только сам человек. Проверка выдаёт предупреждение `W-CL4` на каждый производный Claim `assessed-trait`, в тексте которого названа «attachment-related anxiety» (здесь `c-01`): слово «anxiety» в названии конструкта она читает как чувство. Claim про избегание или заявленный Claim вроде `c-02` предупреждения не получают. Название — не чувство, и предупреждение можно оставить (см. раздел 6).

**5. Прочтите случай через линзу (только сам человек).** Случай — это **Episode** (коллекция `episodes`). Пишите только, что другой человек сделал, и никогда — что он чувствовал или имел в виду (TP-1).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-20", "precision": "day"}, "participants": ["p-01"],
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-20T23:00:00Z", "addedAt": "2026-09-20T23:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "My partner was travelling and did not reply to messages from noon until late evening.",
    "experienced": "Restless; kept checking the phone.",
    "didOrTried": "Went for a run; sent one message instead of five.",
    "understandingThen": "Something must be wrong between us."}],
 "contexts": ["partner"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T23:05:00Z",
 "sensitivity": "special", "categories": ["intimate", "third-party"]}
```

Партнёр — это Party с ролью вместо имени: `{"id": "p-01", "partyKind": "person", "label": "Partner", "role": "partner"}`. Собственное прочтение человека — это **Interpretation** (коллекция `interpretations`) о случае и о результате, с обычными объяснениями, которые человек оставляет открытыми:

```json
{"id": "in-01", "about": ["ep-01", "as-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}, "adoption": "la-01",
 "text": "This was the anxiety side in action: I was watching for distance. It says how I relate, not anything about my partner.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"}, {"ref": "as-01", "kind": "instrument"}],
 "alternatives": [{"text": "I had slept badly and was on edge anyway.", "kind": "physiological"},
                  {"text": "We had planned a call that evening and the time was unclear.", "kind": "informational"}],
 "heldDuring": {"from": "2026-09-21"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T08:00:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"]}
```

Кто видит по умолчанию: только сам человек. Агент пишет такое прочтение только по разрешению и принятию линзы человека (I5); в примере он его не пишет.

**6. Практики.** Их нет. Единственный пункт набора инструментов линзы, «Записать результат опросника», — это и есть этот рецепт; это `instrument-use`, и агент его никогда не предлагает (`agentMayOffer: false`).

**7. Кто что может видеть.** Собеседник-помощник в размышлениях может читать результат и принятые Claims, для самоосмысления, когда человек сам заводит разговор (на записях стоит `subject-initiated-only`). Episode не назван, поэтому не выдаётся.

```json
{"id": "g-01", "recordedAt": "2026-09-21T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:attachment-2d"]}, {"ids": ["c-01", "c-02"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-15T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-21T09:00:00Z", "channel": "holder-ui"}}
```

Рабочему помощнику закрыто всё в этой линзе и всё с категорией `intimate`, что бы ни говорило другое разрешение (запрет сильнее, R-G2):

```json
{"id": "g-02", "recordedAt": "2026-09-21T09:05:00Z", "grantor": "subject", "grantee": "a-02", "effect": "deny",
 "purposes": ["work-collaboration", "task-execution", "communication-adaptation"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:attachment-2d"]}, {"categories": ["intimate"]}]},
 "constraints": {"expiresAt": "2031-09-21T09:05:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent", "note": "An explicit refusal by the person."},
 "expressedBy": {"actor": "subject", "at": "2026-09-21T09:05:00Z", "channel": "holder-ui"}}
```

Схема требует `purposes` и у отказа, но отказ они не сужают: хранитель никогда не выдаёт эти записи `a-02`, какой бы ни была цель запроса (§12.3, шаг 6). Отказу не нужны ни `actions`, ни `mode`, ни `interpretations`.

Получатели — это Party: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}` и `{"id": "a-02", "partyKind": "agent", "label": "Work assistant"}`.

**8. Проверьте.** Сначала сверьте вручную хранилище (шаг 2) и `results` в `as-01` (шаг 3). Затем запустите `python3 -B tools/check.py <папка вашего контекста> --level L1 --json`. Ожидается `"valid": true` и `"levelMet": "L1"`, ошибок нет, и по одному предупреждению `W-CL4` на каждый производный Claim `assessed-trait`, в тексте которого названа «attachment-related anxiety», а иначе предупреждений нет (шаг 4). Что значат ошибки:

- `R-C4`: нет `conformance.subjectIsAdult` (шаг 0).
- `X-1` или `CX-8`: включён режим примера (id контекста начинается с `urn:ohc:example:` или в пути есть папка `examples`), а у записи с содержанием или у самого Context нет `"synthetic": true` (раздел 2).
- `S-3` на Grant: в нём стоит `synthetic`, а его схема это запрещает.
- `AR-8`: опросник не ECR-R.
- `AR-2`: у оценки агента нет `person-only` или признака и потолка `agent-estimate-not-validated`.

## 4. Никогда

- Агент никогда не проводит опросник и не предлагает его (`agentMayOffer: false`). Оценивает баллы или читает через линзу он только по разрешению и принятию линзы человека (I5), а оценка видна только человеку (AR-2).
- Никогда не присваивать категорию или «стиль» — ни по баллам, ни по разговору — и никогда не выдавать категорию за диагноз. Говорить о склонностях в отношениях, а не о расстройствах привязанности (`languageGuidance`).
- Никогда не описывать привязанность партнёра или любого другого человека и не предсказывать, как сложатся отношения (TP-1, `doesNotEstablish`).
- Никогда не поднимать тему первым и всегда держать явным, о каких отношениях речь (`agentPosture`).
- Никогда не использовать результаты в рабочем контексте (`helperMustNot`). Никогда не использовать их для отбора персонала, распределения задач, оценки работы, решений о повышении, сравнения людей между собой, подбора убеждения под психологию человека и других запрещённых целей (§8.10), ни по какому разрешению. Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- Результаты не переводятся в другую линзу (`crossLensMapping: not-allowed`), а оценка не идёт на вход другим выводам (C-7).
- Никогда не хранить и не повторять пункты ECR-R и его ключ подсчёта. Пункты свободны для некоммерческих исследований; для коммерческого применения нужно разрешение авторов (`itemsLicence`).

## 5. Разобранный пример

[examples/attachment-2d/context.json](examples/attachment-2d/context.json) — контекст одним документом уровня L1 об Эскиле, он вымышлен. В нём ровно записи из раздела 3: LensAdoption `la-01`; Source `src-01`; AssessmentRecord `as-01`; Claims `c-01` и `c-02`; Episode `ep-01`; его прочтение `in-01`; Grants `g-01` и `g-02`. В папке также синтетический файл хранилища (сводка баллов без формулировок пунктов) и `expected-check.json`: проверка сравнивает с ним свой вывод для любой папки примера.

```sh
python3 -B tools/check.py docs/lenses/examples/attachment-2d --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ошибок нет, одно предупреждение: `W-CL4` на `c-01` (см. раздел 6).

## 6. Что пока не помещается

1. **Нет поля для того, о ком отношения.** Описание линзы его требует (`ip.restrictions` называет `relationshipTarget`; ментальная модель говорит, что результат от этого зависит), но у AssessmentRecord такого поля нет. Рецепт обходится `contexts: ["partner"]` и `note`.
2. **Категориям некуда лечь.** Описание разрешает категорию только «как производную, с правилом» (AR-6), но конструктов-категорий в нём нет, и у результата `type-assignment` нет id конструкта. Проверка не сверяет, что конструкты результата взяты из линзы.
3. **Предупреждение об аффекте путает название конструкта с чувством.** `W-CL4` срабатывает на любой производный Claim, где названа «attachment-related anxiety». Карантин (R-X3) сделал бы его видимым только самому человеку, а человек этого не просил.
4. **Ограничения на всю линзу оставлены человеку.** «Никогда в рабочем контексте» и «никогда без запроса» нельзя записать в описании линзы так, чтобы хранитель это соблюдал. Человеку приходится писать запрещающее разрешение и ставить `subject-initiated-only` на каждую запись вручную.
5. **Условия опросника не отделяют проведение от записи.** ECR-R свободен для некоммерческих исследований, а для коммерческого применения нужно разрешение. Может ли коммерческий агент записать балл, который у человека уже есть, выразить нельзя.
6. **Отказ нельзя ограничить частью целей.** Запрещающее разрешение обязано перечислить `purposes`, но хранитель применяет его для любой цели (§12.3, шаг 6). Человек не может сказать «откажи для работы, но разреши для личного расписания», а перечисленные цели создают впечатление более узкого отказа, чем действует на деле (шаг 7).
7. **У `instrument.version` нет определённого смысла.** В примерах там стоит год публикации (`"2000"`), издание или ничего, а описания опросников в OHC имеют версию `0.1.0`. Результаты разных изданий и переводов нельзя надёжно сравнить, и ничто не закрепляет, какой версией описания опросника пользовались. Рецепт пишет издание по издателю.
8. **Общие пробелы, которые встречаются и здесь:** проверка требует `conformance.subjectIsAdult`, а схема считает его необязательным, и проверка никогда не открывает хранилище, так что пустой файл с баллами проходит (см. [рецепт процессуального подхода](process-work.ru.md), раздел 6, пункты 6–7).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
