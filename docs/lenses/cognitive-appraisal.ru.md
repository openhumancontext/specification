# Когнитивная оценка: рецепт

**Рецепт · линза `urn:ohc:lens:cognitive-appraisal` 0.2.0 · OHC 0.1.0-draft.2 · информативный · 12 октября 2026**

Рецепт показывает, как человек, который спрашивает себя «может, это неопределённость, нагрузка или вызревание, а не мой изъян?», записывает такой взгляд в свой контекст OHC: линзу предложил агент и принял человек, трудный эпизод, собственная переоценка человека, привычка, которая помогает, и простое утверждение о нагрузке, которое может видеть рабочий помощник.

> **Эта линза — заготовка.** У её описания ([spec/lenses/cognitive-appraisal.lens.json](../../spec/lenses/cognitive-appraisal.lens.json)) `descriptorStatus: stub`: подход назван, но в описании нет ни конструктов, ни набора инструментов, ни представлений, ни опросников. Поэтому в рецепте остались только безопасные шаги: принятие линзы, слова самого человека, исходные материалы, его собственные прочтения и практики, доступ для других. **Ни AssessmentRecord, ни ModelView** здесь не пишутся, и в примере **ни один агент не толкует через эту линзу**: человек оставляет `agentInterpretation: off` (I5).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:cognitive-appraisal-basic`](../../spec/playbooks/cognitive-appraisal-basic.playbook.json) («Когнитивная оценка: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; после неудачи; разбор того, что произошло. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

| Что есть | Подходит? | Куда это идёт |
|---|---|---|
| Слова человека в разговоре: что он говорит себе, когда дело встало («я ленивый»), и что тогда происходило | да | Claims (шаг 3) и Episodes (шаг 4) |
| Дневник или заметки человека за те дни | да | Source (шаг 2), на него ссылаются Episode и прочтение |
| Заметки из коучинга или терапии, где человек учился искать другие объяснения | да, с разрешением практика | путь `inherited-from-practice` и Source вида `practitioner-notes` под защитой конфиденциальности, как в [рецепте процессуального подхода](process-work.ru.md), шаги 1–2 |
| Привычка, которой человек пользуется, когда застрял | да | Practice и её Outcomes (шаг 6) |
| Отчёт опросника | **нет** | у линзы нет опросников |
| Прочтение агента через линзу | **только по разрешению человека** | `infer`, называющее линзу, и действующее принятие линзы не в `off` (I5); прочтения в заготовке остаются `frame-relative`. Рекомендация описания: не проводить по ней упражнений. В примере человек не разрешает ничего из этого. |

Любое прочтение, которое пишет не сам человек, с линзой или без неё, обязано иметь хотя бы одно основание, хотя бы две альтернативы (одну из них непсихологического вида) и `limits` (I4). Это общее правило OHC для всех прочтений. Это не прочтение через эту линзу, и оно никогда её не называет.

## 2. Перед началом

**Путь принятия линзы.** Описание разрешает три пути (`adoption.routes`).

| Путь | Кто пишет LensAdoption | Что это меняет |
|---|---|---|
| `self-chosen` | сам человек (`assertedBy: "subject"`) | Действует сразу. |
| `agent-suggested` | агент, как предложение | Только по разрешению с `suggest`, называющему линзу; рекомендация описания (`suggestionRequires`): агент может назвать подход, только после того как человек попросил другие способы взглянуть на свой опыт (`suggestionRequires`), только как один вариант из нескольких и с его ограничениями (это заготовка, доказательства не оценивались). Нужно разрешение с действием `suggest`. Принятие остаётся предложением, пока человек сам, лично, его не примет (LA-1, R-A1). До этого агент не говорит языком линзы. Рецепт идёт этим путём. |
| `inherited-from-practice` | сам человек | Блок `practice` с практиком как Party, `confidentiality` и `releaseRef`, если хранятся заметки сессий (LA-3, LA-4). |
| `imported` | — | Недоступен: опросников нет. |

**Согласие.** Человек решает, принимать ли линзу, что хранить и кому показывать. Без Grant ничего не уходит из контекста (R-G1). Разрешающий Grant, который достаёт до записей этой линзы, даётся с `basis.legal: "explicit-consent"` и истекает не позже чем через 180 дней от своего `recordedAt` (R-G10, R-G11, GR-1). У отказа (`effect: deny`) предела срока нет.

**Умолчания линзы** (`defaults`): уровень чувствительности `special`, категория `mental-health`, `reviewAfter: on-change`.

- LensAdoption и каждая Interpretation, где указана линза, получают `special` сами (умолчание линзы; I9).
- У Claims, Episodes, Sources и Practices нет поля `lens`, поэтому умолчания линзы до них не доходят (`source.lens` у Practice только помогает селектору `lenses` в разрешении её найти). Если в них самокритика или внутренний материал этой работы, поставьте `"sensitivity": "special"` и `"categories": ["mental-health"]` вручную. Episode, основанием которого служит Source уровня `special`, и Outcome о практике уровня `special` наследуют `special` по C3 (§8.4).
- Простой факт о ситуации (например, нагрузка недели) может остаться на своём уровне по умолчанию, чтобы человек мог делиться им шире (шаг 5).
- Самокритичные утверждения получают `handling: ["no-quote-back"]`: их никогда не показывают человеку как довод против него.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет (I5). `interpretationAuthors` равно `["subject"]`. `uses`: `speak-in-lens` и `interpret`.

**Что не хранится никогда.** Ярлыки «искажений», диагнозы; вердикт о характере человека; любой балл; прочтение агента через линзу; тексты метода, скопированные из книг или курсов.

**Пометка «вымышлено».** В примерах (контекст, чей `id` начинается с `urn:ohc:example:`, или любая папка `examples` в пути) поставьте `"synthetic": true` на сам Context и на каждый Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice и Outcome (X-1, CX-8). Никогда не ставьте его на Grant, Proposal, Review или Event и на Party: их схемы это запрещают (S-3). Для реального человека не ставьте его нигде.

## 3. Шаги

**0. Создайте файл контекста.** Заведите папку для контекста и создайте в ней `context.json` (контекст одним документом). Начните с такой заготовки:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-20T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` и `subject` обязательны. Меняйте `version` при каждом изменении файла.
- `conformance.subjectIsAdult: true` — заявление хранителя, что человек взрослый и решает за себя сам. Без него проверка отклоняет любое заявление о соответствии (R-C4), и `levelMet` равно `null`. Без `conformance.level` проверка проверяет только L0.
- `modules`: всегда `core` и `lenses`, `governance` — для разрешений, предложений и решений человека (шаги 1 и 7), `practices` — для практики (шаг 6).
- `lenses` закрепляет описание линзы, которым пользуется контекст.
- Каждая запись ниже ложится в массив верхнего уровня, названный по её коллекции: `grants`, `lensAdoptions`, `proposals`, `reviews`, `sources`, `claims`, `episodes`, `interpretations`, `practices`, `outcomes`. Каждая Party ложится в `parties`.
- В примере берите id вида `urn:ohc:example:<имя>:cognitive-appraisal` (контекст) и `urn:ohc:example:<имя>` (человек) и добавьте `"synthetic": true` на сам Context (см. раздел 2).

**1. Примите линзу (здесь: её предложил агент).** Человек попросил своего собеседника-помощника в размышлениях о другом взгляде на застрявшую задачу. Дальше четыре записи, в таком порядке.

**Порядок.** Разрешение в 1a называет `c-01` и `ep-01`: слова самого человека и эпизод, которые обычно есть ещё до того, как кто-то предложит линзу. Сначала запишите Source `src-01` (шаг 2), Claim `c-01` (шаг 3) и Episode `ep-01` (шаг 4), потом вернитесь сюда. Если их ещё нет, когда человек даёт разрешение, не пишите их id в `g-01`. Разрешение нельзя исправить: чтобы добавить их позже, человек даёт новое разрешение с `"renews": "g-01"`.

1a. **Grant** человека (коллекция `grants`) разрешает собеседнику читать записи линзы и предлагать, но не делать выводов. Собеседник — это Party: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`.

```json
{"id": "g-01", "recordedAt": "2026-09-25T18:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:cognitive-appraisal"]}, {"ids": ["c-01", "ep-01"]},
                       {"facets": ["preference"]}]},
 "actions": ["read", "suggest"], "mode": "full", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-20T18:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-25T18:00:00Z", "channel": "holder-ui"}}
```

1b. Собеседник называет подход как один из вариантов. Человек соглашается. Собеседник пишет **LensAdoption** (коллекция `lensAdoptions`) как свою запись по этому разрешению. Её `origin` равно `observed`: он фиксирует согласие человека, а не своё утверждение своими словами (запись агента с `declared` обязана иметь `text`, ENV-2). `underGrant` и `purpose` называют разрешение из 1a и одну из его целей (INF-1).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"},
 "route": "agent-suggested", "suggestedBy": "a-01",
 "uses": ["speak-in-lens", "interpret"], "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "observed", "assertedBy": "a-01", "recordedAt": "2026-09-25T19:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection",
 "sensitivity": "special", "categories": ["mental-health"]}
```

1c. Собеседник подаёт **Proposal** (коллекция `proposals`), в котором лежит это принятие. Пояснение пишется для человека и не цитирует ни одну запись. `presentation.askedAt` — момент, когда собеседник предложил это человеку в разговоре; ни схема, ни SPECIFICATION §11.2 пока это поле не определяют (см. раздел 6). На Proposal никогда не ставится `synthetic`, даже в примере.

```json
{"id": "prop-01", "proposer": "a-01", "recordedAt": "2026-09-25T19:00:00Z", "underGrant": "g-01",
 "purpose": "self-reflection", "items": ["la-01"],
 "rationale": "You asked for other ways of looking at a stalled task. This perspective is one option; it is not a reading of you.",
 "expiresAt": "2026-10-09T19:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-25T18:58:00Z"}}
```

1d. Человек принимает его записью **Review** (коллекция `reviews`). Сделать это может только сам человек (R-A1). Молчание — не согласие (C-9). На Review никогда не ставится `synthetic`, даже в примере. Если человек не принял предложение, принятие остаётся предложением: не пишите прочтений, которые на него ссылаются (шаг 5).

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-25T19:10:00Z"}
```

Кто видит принятие: сам человек и собеседник по `g-01`.

**2. Положите исходники в хранилище.** Папка `vault/` лежит рядом с `context.json`, и каждый `vaultPath` отсчитывается от папки, где лежит `context.json`. Для записи в дневнике:

1. посчитайте sha256 её байтов командой `shasum -a 256 <файл>` (или `sha256sum <файл>`) и размер в байтах командой `wc -c < <файл>`;
2. сохраните файл как `vault/<первые два шестнадцатеричных знака>/<sha256>.<расширение>`;
3. запишите **Source** (коллекция `sources`) с этим путём, хешем и размером.

Проверка не открывает хранилище (в её отчёте `"vaultContentRead": false`). Пропавший файл, неверный хеш или размер всё равно пройдут шаг 8, поэтому сверьте путь, `sha256` и `size` сами до шага 8.

Дневник за дни самокритичного эпизода — это сырой материал этой работы, поэтому он `special` с `mental-health`. Если в записи есть самокритика человека его же словами, добавьте ещё `"handling": ["no-quote-back"]`. На своём уровне по умолчанию, `sensitive`, может остаться только материал, где нет ничего, кроме внешних фактов (выгрузка календаря, письмо фонда).

```json
{"id": "src-01", "sourceKind": "journal-entry",
 "content": {"locator": {"vaultPath": "vault/bd/bd2ef427fdd98e16536b45a3bfcf4a6415820201c1f7277e2eb34d7dc86bfbcb.md"},
             "sha256": "bd2ef427fdd98e16536b45a3bfcf4a6415820201c1f7277e2eb34d7dc86bfbcb",
             "mediaType": "text/markdown", "size": 231},
 "capturedAt": "2026-09-24T22:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T22:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"]}
```

Кто видит по умолчанию: только сам человек. `maxSourceTier: none` в `g-01` не пускает к нему собеседника.

**3. Запишите, что человек говорит о себе.** Привычное объяснение себе — это **Claim** (коллекция `claims`) словами человека, с пометкой, чтобы его никогда не цитировали в ответ:

```json
{"id": "c-01", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When a piece of work stalls, my first explanation is that I am lazy.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-quote-back"]}
```

Как человек хочет, чтобы агент реагировал, — это предпочтение:

```json
{"id": "c-02", "facet": "preference", "predicate": "pushback",
 "text": "If I call myself lazy, ask what else was going on that week before suggesting anything.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:05:00Z"}
```

Кто видит по умолчанию: только сам человек. По `g-01` собеседник видит `c-01` (названо по id) и `c-02` (грань `preference`).

**4. Запишите, что произошло.** Трудность — это **Episode** (коллекция `episodes`). В `understandingThen` остаётся, как человек понимал это тогда, даже если это была самокритика. Переоценка придёт позже, как Interpretation.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-22", "end": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T22:00:00Z", "addedAt": "2026-09-24T22:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "Three evenings in a row I opened the grant draft and closed it after about ten minutes.",
    "experienced": "Heavy. A familiar voice saying I am just lazy.",
    "didOrTried": "Tidied the desk and answered emails instead.",
    "understandingThen": "I am lazy and undisciplined.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T22:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

**5. Переоценка человека через линзу.** Прочтения, которые ссылаются на `la-01`, пишите только после того, как есть `rv-01`, и с `recordedAt` позже, чем у этого Review. Если человек не принял линзу, пишите прочтение без `lens` и `adoption`, как обычную Interpretation со `stance: "retrospective"`. Проверка не ловит прочтение, которое ссылается на ещё не принятое предложение, а хранитель выдал бы его собеседнику (см. раздел 6).

Сначала вопрос человека, сохранённый как прочтение (**Interpretation** с `question`, коллекция `interpretations`):

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}, "adoption": "la-01",
 "question": "Was I stuck because I did not know which version of the guidelines counted, rather than because I am lazy?",
 "heldDuring": {"from": "2026-09-26"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-26T08:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Потом ответ человека и объяснения, которые он оставляет открытыми, в `alternatives`. Неопределённость — вид `informational`, нагрузка или усталость — `physiological`, внешнее препятствие — `situational` или `external`. Для вызревания вида нет, используйте `other` (см. раздел 6).

```json
{"id": "in-02", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}, "adoption": "la-01",
 "text": "The stall had ordinary causes: I did not know which version of the guidelines counted, and it was a week of late shifts.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"},
             {"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "evidence"}],
 "alternatives": [{"text": "The structure was still forming; it came together on Saturday without effort.", "kind": "other"},
                  {"text": "Part of me doubts the project itself.", "kind": "psychological"}],
 "heldDuring": {"from": "2026-09-28"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Если вывод человека — простой факт о ситуации, он может записать его ещё и как обычный **Claim** без линзы. Такой Claim остаётся на уровне по умолчанию, и им можно поделиться там, где это помогает (шаг 7):

```json
{"id": "c-03", "facet": "state", "predicate": "load",
 "text": "Late shifts until Friday 3 October; slow on writing tasks.",
 "horizon": "state", "valid": {"from": "2026-09-28", "until": "2026-10-04"}, "contexts": ["work"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:10:00Z"}
```

Кто видит прочтения: сам человек и собеседник по `g-01` (собственные прочтения человека, через селектор `lenses`). Сам собеседник прочтений не пишет: в его разрешении нет `infer`, а принятие линзы оставляет `agentInterpretation: off` (I5).

**6. Привычка, которая помогает.** **Practice** (коллекция `practices`) словами человека; запускает её только сам человек (`subject-initiated-only`):

```json
{"id": "pr-01", "name": "Three ordinary causes",
 "description": "When a task stalls, write three causes that are about the situation, not about my character.",
 "practiceKind": "writing",
 "source": {"route": "self-discovered", "lens": "urn:ohc:lens:cognitive-appraisal"},
 "steps": ["Write the stalled task in one line", "Write three causes about the situation: unclear, too much, not ready yet", "Pick one small step for the cause I can change"],
 "duration": "PT10M", "limits": "Not to argue myself out of a real doubt; a real doubt gets its own note.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:15:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only"]}
```

Попробовав её, человек оценивает результат в **Outcome** (коллекция `outcomes`):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T21:00:00Z"}
```

Кто видит по умолчанию: только сам человек. По `g-01` собеседник видит и Practice (селектор `lenses` достаёт до неё через `source.lens`), но сам её не предлагает.

**7. Кто что может видеть.** У собеседника уже есть `g-01`. Рабочий помощник получает только простое утверждение о нагрузке, в режиме `rule-only`, без материала линзы и без прочтений. Помощник — это Party: `{"id": "a-02", "partyKind": "agent", "label": "Work assistant"}`.

```json
{"id": "g-02", "recordedAt": "2026-09-28T10:20:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["scheduling"],
 "scope": {"include": [{"facets": ["state"], "predicates": ["load"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-06-30T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-28T10:20:00Z", "channel": "holder-ui"}}
```

**8. Проверьте.** Сначала сверьте хранилище вручную (шаг 2). Затем запустите `python3 -B tools/check.py <папка вашего контекста> --level L1 --json`. Ожидается `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений. Что значат ошибки:

- `R-C4`: нет `conformance.subjectIsAdult` (шаг 0).
- `X-1` или `CX-8`: включён режим примера (id контекста начинается с `urn:ohc:example:` или в пути есть папка `examples`), а у записи с содержанием или у самого Context нет `"synthetic": true` (раздел 2).
- `S-3` на Grant, Proposal или Review: в нём стоит `synthetic`, а его схема это запрещает.
- `INF-1` на `la-01` вместе с `PR-2` на `prop-01`: в разрешении нет `suggest`, или в момент `recordedAt` оно ещё не было дано (или уже закончилось).
- `INF-1` на `la-01` без `PR-2`: охват разрешения не достаёт до `la-01` (нет ни селектора `lenses` с этой линзой, ни id `la-01`), или `purpose` у `la-01` не входит в `purposes` разрешения.
- `ENV-2`: агент записал принятие как `declared`.

## 4. Никогда

- Агент толкует через эту линзу только по разрешению человека (`infer`, называющее линзу) и при его принятии линзы (I5); его прочтения остаются `frame-relative`, и упражнений по заготовке он не проводит. В примере человек не разрешает ничего из этого.
- Агент предлагает линзу только по разрешению с `suggest`, называющему её, только если человек просил других способов взглянуть, и никогда как единственный вариант (`suggestionRequires`). Её языком он говорит словами самого человека, когда тот принял линзу (`agentPosture`), и никогда не включает принятие сам (LA-1).
- Другие объяснения предлагаются вопросами, а не поправками (`languageGuidance`). Что подходит, решает человек; навязанное объяснение может звучать как отмахивание (`riskNotes`).
- Агент не проводит упражнений из линзы и не выдаёт себя за практика этого подхода.
- Никогда не цитировать человеку его самокритику как доказательство («вы же сами сказали, что ленивый»); `no-quote-back` (§8.5).
- Никаких ярлыков «искажений», диагнозов и клинических терминов (I3).
- Ничто из этой линзы не используется для отбора персонала, распределения задач, оценки работы, решений о повышении, сравнения людей между собой, подбора убеждения под психологию человека и других запрещённых целей (§8.10), ни по какому разрешению. Прочтение служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14). Рабочий помощник получает простой Claim с гранью `state`, но никогда — записи линзы.
- Ничто из линзы не переводится в другую линзу (`crossLensMapping: not-allowed`), и прочтение в ней никогда не выдаётся за эмпирический факт (C-7).

## 5. Разобранный пример

[examples/cognitive-appraisal/context.json](examples/cognitive-appraisal/context.json) — контекст одним документом уровня L1 о Тамсин, она вымышлена. В нём ровно записи из раздела 3: Grants `g-01` и `g-02`; LensAdoption `la-01`, её Proposal `prop-01` и принимающий Review `rv-01`; Source `src-01`; Claims `c-01`, `c-02` и `c-03`; Episode `ep-01`; её прочтения `in-01` и `in-02`; Practice `pr-01` и её Outcome `oc-01`. В папке также синтетический файл хранилища и `expected-check.json`: проверка сравнивает с ним свой вывод для любой папки примера.

```sh
python3 -B tools/check.py docs/lenses/examples/cognitive-appraisal --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений.

## 6. Что пока не помещается

1. **У трёх объяснений самой линзы нет видов альтернатив.** Неопределённость ложится на `informational`, нагрузка — на `physiological`, а для вызревания вида нет, оно попадает в `other`. Список видов альтернатив закрыт.
2. **У принятия, записанного агентом, нет правильного происхождения.** У LensAdoption нет `text`, поэтому агент не может записать его как `declared` (ENV-2). [CONTEXT-08](../agents/procedures/CONTEXT-08.md) не говорит, какое происхождение ставить; здесь стоит `observed`. Тестовый пример записывает тот же путь с `assertedBy: "subject"`, и тогда принятие действует сразу.
3. **Просьба человека «покажи другие способы взглянуть» не оставляет следа.** `suggestionRequires` в описании держится на этой просьбе, но её не записать ни в поле, ни в Event, а пояснение в Proposal не может цитировать разговор. `Proposal.presentation.askedAt` не определено ни в схеме, ни в SPECIFICATION §11.2: это может быть и просьба человека, и момент, когда агент предложил это человеку. Рецепт понимает его во втором смысле.
4. **Умолчания линзы не умеют задавать ограничения.** Самокритичным утверждениям каждый раз нужно `no-quote-back`, а в `defaults` есть только уровни, категории и `reviewAfter`.
5. **Граница между этой линзой и I4 не проведена.** Любое прочтение агента уже обязано предложить непсихологическую альтернативу (I4) — это и есть ход этой линзы, а ModelView по CBT в примере Ноа называет эту линзу альтернативой. И при этом агенту нельзя читать через неё.
6. **Уровень по умолчанию тяжелее содержания.** LN-4 делает каждую линзу `special`, поэтому «это была нагрузка» внутри линзы остаётся особой категорией. Чтобы поделиться этим с рабочим помощником, человеку приходится переписать это простым Claim с гранью `state` (шаг 5).
7. **Прочтение под ещё не принятой линзой проходит проверку.** Interpretation, у которой `adoption` всё ещё предложение (принимающего Review нет), допустима на L1, и хранитель выдаёт её получателям, хотя само принятие придерживает. Так текст в понятиях линзы может дойти до агента раньше, чем человек принял линзу, вопреки рекомендации описания (`agentPosture`). Шаг 5 просит дождаться `rv-01`.
8. **На Proposal и Review нельзя поставить `synthetic`.** X-1 говорит о «каждой записи с содержанием» и не перечисляет виды, а схемы записей управления запрещают `synthetic` (S-3), хотя в `rationale` у Proposal и в `note` у Review есть свободный текст. Опубликованный пример не может пометить их как вымышленные.
9. **Общие пробелы, которые встречаются и здесь:** проверка требует `conformance.subjectIsAdult`, а схема считает его необязательным, и проверка никогда не открывает хранилище (см. [рецепт процессуального подхода](process-work.ru.md), раздел 6, пункты 6–7).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
