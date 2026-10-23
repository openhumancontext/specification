# Рецепт линзы: `cbt` (когнитивно-поведенческая линза, неклиническое использование)

**Рецепт · линза `urn:ohc:lens:cbt` 0.2.0 · OHC 0.1.0-draft.2 · справочный документ · 12 октября 2026**

Этот рецепт по шагам показывает, как записи мыслей человека и его работа с когнитивно-поведенческой линзой попадают в контекст OHC: какие записи при этом создаются, кто их видит и как агент может предложить толкование, не навешивая ярлыков на чужие мысли.

**Линза коротко** (по [`spec/lenses/cbt.lens.json`](../../spec/lenses/cbt.lens.json); см. также [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person)):

| | |
|---|---|
| Вид и статус | `practice-method`, описание в статусе `draft`, только неклиническое использование |
| Понятия линзы | `cbt/situation`, `cbt/automatic-thought`, `cbt/emotion`, `cbt/behavior`, `cbt/alternative-thought` |
| Опросники | нет |
| Инструменты | `cbt.thought-record`: лист, который заполняет человек; агент может его предложить; даёт запись AssessmentRecord |
| Представление | `cbt.thought-record`: пять столбцов словами человека (тип результата `thought-record`) |
| Предложение агентом | по разрешению человека (`suggest`, называющее линзу); рекомендация описания: когда человек попросил о способе посмотреть на повторяющуюся реакцию |
| Толкование агентом | по разрешению человека (`infer`, называющее линзу) и его принятию линзы (I5) |
| Сопоставление с другими линзами | `not-allowed` |
| Значения по умолчанию | уровень `special`; категория `mental-health`; `reviewAfter` `P3M` |
| Доказательная база | OHC не утверждает, что метод помогает. Единственная ссылка в описании помечена **[verify]**: Hofmann et al. 2012, обзор метаанализов о клинической эффективности, для такого использования не проверялся. |

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:cbt-basic`](../../spec/playbooks/cbt-basic.playbook.json) («Когнитивно-поведенческая линза: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; после неудачи; подготовка к трудному разговору; выбор между вариантами. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

- **Рассказ человека в разговоре.** Человек описывает ситуацию, что пронеслось в голове, что он чувствовал и что сделал.
- **Запись мыслей, которую человек сделал сам**: напечатанную, в приложении или на бумаге и сфотографированную.
- **Записи из терапии или коучинга**, где использовались записи мыслей, в том числе листы, заполненные на сессии.
- **Толкование агента.** По разрешению человека с `infer`, которое называет линзу, и при его принятии линзы, и всегда как предложение, о котором решает человек.

Для этой линзы не подходит отчёт опросника: у линзы нет ни опросника, ни баллов.

## 2. Прежде чем начать

**Путь принятия линзы.**

| Путь | Когда | Что меняется |
|---|---|---|
| `self-chosen` | Человек выбрал линзу сам. | Человек записывает принятие; оно действует сразу. |
| `agent-suggested` | Человек попросил о способе посмотреть на повторяющуюся реакцию, и вы предложили запись мыслей. | В принятии есть `suggestedBy` (id вашей стороны), и оно остаётся `proposed`, пока человек не примет его записью Review, даже если запись сделал сам человек. Проверка не напомнит вам об этой записи Review (шаг 1). |
| `inherited-from-practice` | Человек делает записи мыслей с терапевтом или коучем. | Добавьте блок `practice`. С терапевтом поставьте `confidentiality: "therapy-confidential"`: принятие и все записи, которые ссылаются на него в поле `adoption` (здесь толкование агента), становятся `person-only` (LA-4). AssessmentRecord и Practice не могут сослаться на принятие, поэтому сами добавьте `"handling": ["person-only"]` в каждую запись мыслей и каждую практику линзы (шаги 4 и 7), а также в эпизоды из сессий. Запись мыслей, сделанная на сессии, получает `mode: "practitioner-facilitated"`. Если вы храните материалы сессий, `practice.releaseRef` должен указывать на разрешение специалиста (LA-3). |
| `imported` | Для этой линзы не указан: импортировать не из чего. | Пути описывают обычную практику и ничего не запрещают. |

**Согласие.** Линзу принимает человек, а не вы. Принятие никому не даёт доступа (LA-2). Чтобы вы могли читать записи мыслей или предлагать толкование, человек сначала должен дать вам разрешение с `infer` и явным согласием. **Это разрешение даётся в шаге 2, и оно должно существовать раньше любой записи, которую вы пишете или подаёте** (правила INF-1 и PR-2 проверяют, что разрешение уже было дано на момент `recordedAt` каждой вашей записи). То, что человек вам диктует, записывается как его собственное (`assertedBy: "subject"`), читается ему и подтверждается ([CONTEXT-01](../agents/procedures/CONTEXT-01.md)). Поле `recordedBy` не заполняйте: если поставить туда id вашей стороны, правило INF-1 потребует `underGrant` и `purpose` по разрешению с действием `write`.

**Значения по умолчанию для этой линзы.**

- `sensitivity: "special"` и `categories: ["mental-health"]` на каждой записи линзы: на принятии, записях мыслей, толкованиях через линзу, практиках из её инструментов и источниках с записями мыслей. В документации это называется «относится к особой категории».
- Утверждение, которое ссылается на запись мыслей в `derivedFrom`, получает `special` и `mental-health` (C3; см. шаг 5).
- `reviewAfter`: `P3M` для записей мыслей.
- `agentInterpretation`: по умолчанию `off`. Человек может поставить `ask-first` или `allowed`; при `off` в действующем принятии ни один агент не читает через линзу (I5).

**Что никогда не хранится.**

- Опубликованные тексты листов, инструкции или примеры из пособий и приложений (ограничение из описания линзы). Храните только собственные записи человека.
- Ярлыки для мыслей (названия «искажений», «иррационально», «катастрофизация» и подобное), диагнозы и клинические баллы.
- Значение эмоции, настроения или стресса, которое вы вывели сами — из поведения или как-то иначе (R-X4). Столбец эмоции — всегда собственное слово человека.
- Запись мыслей, заполненная агентом, и альтернативная мысль, которую человек не принял как свою.
- Любой балл, использованный как суждение о человеке.

## 3. Шаги

Для каждого шага сказано, что сделать, какая запись появляется, в какой массив файла контекста она идёт, как выглядит минимальная запись, которая проходит проверку по схеме, и кто её видит по умолчанию. Фрагменты взяты из [разобранного примера](#5-разобранный-пример) или проверены вместе с ним; в них стоит `"synthetic": true`, потому что человек вымышлен — для настоящего человека это поле не пишут. Пока нет разрешения, никто, кроме самого человека, ничего не видит. Выполняйте шаги по порядку и ставьте каждой записи `recordedAt` позже, чем у записей, на которые она опирается: проверка отклоняет запись агента, сделанную раньше его разрешения, но другие записи в неправильном порядке не замечает (§6, пункт 12).

### Шаг 0. Завести файл контекста

Создайте папку для контекста человека, а в ней файл `context.json` (форма «один документ», [§3.3](../../spec/SPECIFICATION.md#33-two-serializations-of-one-data-model); [схема](../../spec/schema/context.schema.json)). Начните его с такой оболочки:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:jovana:context",
  "version": "2026-09-16.1",
  "subject": {"id": "urn:ohc:example:jovana", "displayName": "Jovana (fictional)"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-03T19:00:00Z",
  "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
  "parties": [],
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "lenses": [{"id": "urn:ohc:lens:cbt", "version": "0.2.0"}],
  "synthetic": true,
  "lensAdoptions": [], "grants": [], "sources": [], "episodes": [], "assessments": [], "claims": [],
  "interpretations": [], "proposals": [], "practices": [], "outcomes": [], "reviews": []
}
```

- **Модули.** Объявите каждый модуль, чьи записи вы пишете, иначе проверка выдаст ошибки: `core` (Party, Source, Episode, Claim, Interpretation, Proposal, Review), `governance` (Grant), `lenses` (LensAdoption, AssessmentRecord), `practices` (Practice, Outcome).
- **Массивы.** Каждая запись идёт в массив своего вида: LensAdoption → `lensAdoptions`, Grant → `grants`, Source → `sources`, Episode → `episodes`, AssessmentRecord → `assessments`, Claim → `claims`, Interpretation → `interpretations`, Proposal → `proposals`, Practice → `practices`, Outcome → `outcomes`, Review → `reviews`, Party → `parties`. В каждом шаге ниже массив назван ещё раз.
- **`synthetic`.** В примере `"synthetic": true` стоит у самого контекста и у каждой записи с содержанием; у сторон (Party) и у записей Grant, Proposal и Review его не бывает никогда (схема его там не принимает).
- **Для настоящего человека.** Возьмите идентификаторы вида `urn:uuid:` для `id` и `subject.id`, например из `python3 -c "import uuid; print('urn:uuid:' + str(uuid.uuid4()))"`; уберите `synthetic` отовсюду; `displayName` необязателен. Не кладите папку внутрь папки с именем `examples`. Контекст, чей `id` начинается с `urn:ohc:example:` или который лежит внутри папки `examples`, проверяется как пример, и тогда `"synthetic": true` нужен на каждой записи с содержанием (X-1, CX-8).
- **`version`** вы выбираете сами; меняйте её при каждом наборе изменений.
- **Пустой файл проверку ещё не проходит.** В контексте должно быть хотя бы одно утверждение (Claim) или один эпизод (Episode) с рассказом (LV-0); его добавляет шаг 4. Проверяйте после шага 4 и ещё раз в конце (шаг 8).

### Шаг 1. Записать принятие линзы (Party → `parties`, LensAdoption → `lensAdoptions`, Review → `reviews`)

Спросите, как человек пришёл к линзе и для чего её можно использовать ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption), [схема](../../spec/schema/lens-adoption.schema.json)).

- `uses`: `speak-in-lens`, `offer-practices` (вы можете предложить запись мыслей), `store-results` (человек хранит записи мыслей), `interpret` (толкования через линзу).
- `interpretationAuthors`: `["subject"]` и любые люди (например, терапевт), чьи толкования человек хочет хранить. Указать здесь id вашей стороны, как в примере, не вредно; ваши собственные толкования идут по вашему разрешению (I5). `agentInterpretation: "ask-first"` значит, что перед каждым толкованием вы спрашиваете.

В примере вы предложили запись мыслей в разговоре, и человек согласился. Сначала добавьте себя в `parties`; приставка id `a-` обязательна для агента (`p-` — человек, `s-` — программа, `o-` — организация):

```json
{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
```

Затем человек сам записывает принятие и принимает его:

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "confidentiality": "none",
 "uses": ["speak-in-lens", "offer-practices", "store-results", "interpret"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "cbt.thought-record",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-03T19:01:00Z"}
```

Без записи Review `admit` принятие остаётся `proposed`, а принятие-предложение ничего не разрешает и не запрещает: ваше толкование в шаге 6 прошло бы I5 по одному разрешению, а выбор человека `ask-first` не подействовал бы. Собственные записи мыслей и практики человека по этой линзе всё равно выдаются. Пишите запись `admit` раньше любой другой записи линзы.

Для пути `self-chosen` уберите `suggestedBy` и запись Review. Для пути `inherited-from-practice` см. §2.

**Вариант: принятие записываете вы сами**, вне разговора, в котором человек его подтверждает. Тогда это ваше предложение: агент не может записать его как `declared` (ENV-2), поэтому оно `inferred`, ссылается на то место, где человек попросил, и требует разрешения из шага 2 с `suggest` и `infer`. Действуйте в таком порядке:

1. Сначала запишите разрешение из шага 2, с `recordedAt` и `expressedBy.at` раньше всего, что ниже (например `2026-09-03T18:40:00Z`).
2. Запишите эпизод (или источник), в котором человек попросил, с `recordedAt` раньше принятия:

   ```json
   {"id": "ep-00", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:50:00Z",
    "title": "Asked for a way to look at it", "occurred": {"start": "2026-09-03", "precision": "day"},
    "accounts": [{"narrator": "subject", "narratedAt": "2026-09-03T18:45:00Z", "addedAt": "2026-09-03T18:50:00Z",
      "accountKind": "in-the-moment",
      "happened": "I asked the companion for a way to look at why I keep holding drafts back."}],
    "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "contexts": ["work"], "synthetic": true}
   ```

3. Замените в принятии эти поля:

   ```json
   {"assertedBy": "a-01", "origin": "inferred", "underGrant": "g-01", "purpose": "self-reflection",
    "derivedFrom": ["ep-00"]}
   ```

4. Подайте его в `proposals`. `expiresAt` необязателен; без него предложение истекает через 30 дней после `recordedAt`:

   ```json
   {"id": "prop-00", "proposer": "a-01", "recordedAt": "2026-09-03T19:00:00Z", "underGrant": "g-01",
    "purpose": "self-reflection", "items": ["la-01"],
    "rationale": "The thought record is one way to look at holding drafts back. Take it only if it suits you.",
    "expiresAt": "2026-10-03T19:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-03T18:59:00Z"}}
   ```

5. Дождитесь записи Review `admit` от человека (`rv-01` выше). До неё принятие — `proposed`.

Проверка не сверяет, что `ep-00` старше принятия (§6, пункт 12): соблюдайте этот порядок сами. Этот вариант проверен и проходит на уровне L1; в файл примера он не входит.

**Кто видит:** человек, а по разрешению из шага 2 — и вы.

### Шаг 2. Кто что может видеть — до любого толкования (Grant → `grants`)

По умолчанию никто ничего не видит. Для спутника, который может читать записи мыслей и предлагать толкования, человек даёт такое разрешение сейчас ([§12.1](../../spec/SPECIFICATION.md#121-grant), [схема](../../spec/schema/grant.schema.json)). Его `recordedAt` и `expressedBy.at` должны быть раньше каждой записи, которую вы пишете или подаёте по нему (шаги 6 и 7); иначе проверка не пройдёт из-за INF-1 и PR-2.

- `actions: ["read", "suggest", "infer"]`: `infer` никогда не подразумевается другими действиями (R-G11).
- Условие, которое называет линзу, `basis.legal: "explicit-consent"` и срок не больше 180 дней (R-G3, R-G10).
- Эпизоды имеют уровень `sensitive`: назовите их по виду записи, здесь только рабочие.
- `maxSourceTier: "none"`: оригиналы недоступны.

```json
{"id": "g-01", "recordedAt": "2026-09-03T19:05:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:cbt"]}, {"kinds": ["Episode"], "contexts": ["work"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "all", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T19:05:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D", "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-03T19:05:00Z", "channel": "holder-ui"},
 "note": "Thought records and readings of work situations only. No labels for my thoughts."}
```

Рабочий помощник никогда не получает эту линзу: записи мыслей никогда не служат входом для работы (запрещённые цели в §4). Что в итоге получает спутник, показано в конце шага 7.

### Шаг 3. Сохранить оригинал в хранилище (Source → `sources`)

Если человек где-то записал мысли, сохраните оригинал как запись Source ([§10.1](../../spec/SPECIFICATION.md#101-source), [схема](../../spec/schema/source.schema.json)): `sourceKind: "note"` для напечатанного текста, `"image"` для фотографии бумажного листа, `"document"` для выгрузки в PDF. В записи только описание, а сами байты кладутся в хранилище:

1. Посчитайте хеш: `shasum -a 256 <файл>` (или `sha256sum <файл>`). 64 шестнадцатеричных знака — это `sha256`.
2. Посчитайте размер в байтах: `wc -c < <файл>`. Это число — `size`.
3. Скопируйте файл в `vault/<первые два знака хеша>/<хеш>.<расширение>`. Путь `vaultPath` отсчитывается от папки, где лежит `context.json`.
4. Проверка уровня L1 хранилище не открывает (в её отчёте `"vaultContentRead": false`): она не заметит ни отсутствующего файла, ни неверного хеша, ни неверного размера. Выполните обе команды ещё раз для сохранённого файла и сравните.

Поставьте `maxRelease: "index"`.

```json
{"id": "src-01", "sourceKind": "note", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-08T21:00:00Z",
 "content": {"locator": {"vaultPath": "vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md"},
             "sha256": "60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef",
             "mediaType": "text/markdown", "size": 324},
 "capturedAt": "2026-09-08T20:40:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "My thought record for Tuesday.", "authoredBy": "subject",
             "recordedAt": "2026-09-08T21:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["work"], "synthetic": true}
```

Разобранный пример содержит эти байты: [examples/cbt/vault/60/…](examples/cbt/vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md).

Фотография относится к поведенческим видам источников (R-X4). Запись мыслей, которая указывает её в `source`, допустима только как собственные записи человека (`origin: "declared"`); версия, распознанная программой (`origin: "derived"`), не проходит проверку (AR-1), и ничего о чувствах из фотографии выводить нельзя.

**Кто видит:** человеку доступно всё. Получатель узнаёт самое большее `index`, и только по разрешению, которое прямо называет этот источник.

### Шаг 4. Ситуация и запись мыслей (Episode → `episodes`, AssessmentRecord → `assessments`)

**4а. Ситуация.** Запишите, что произошло, как запись Episode с рассказом самого человека ([§10.2](../../spec/SPECIFICATION.md#102-episode), [схема](../../spec/schema/episode.schema.json)).

```json
{"id": "ep-01", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T20:30:00Z",
 "title": "Floor-plan draft kept back", "occurred": {"start": "2026-09-08", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-08T20:30:00Z", "addedAt": "2026-09-08T20:30:00Z",
    "accountKind": "in-the-moment",
    "happened": "The floor-plan draft was due to my team lead on Tuesday. I kept it for a third day.",
    "experienced": "A knot in my stomach every time I opened the send window.",
    "didOrTried": "Changed the stair detail again. Did not send.",
    "understandingThen": "The draft was not ready."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "contexts": ["work"], "synthetic": true}
```

**4б. Запись мыслей.** Одна запись AssessmentRecord на каждый заполненный лист ([§10.6](../../spec/SPECIFICATION.md#106-assessmentrecord), [схема](../../spec/schema/assessment-record.schema.json)), с одним результатом типа `thought-record`.

- Пять столбцов — собственные слова человека. Вы можете задавать вопросы («Что пронеслось в голове прямо перед этим?», «Что ещё может быть правдой?»), но никогда не заполняете столбец сами.
- `mode: "self-identified"` с `origin: "declared"` и отметкой `self-identified-only` — самое близкое в 0.1 для записей, которые человек сделал сам (§6, пункт 1). Если запись делалась со специалистом на сессии — `practitioner-facilitated`.
- `instrument` не указывается: у линзы его нет.
- `derivedFrom: ["ep-01"]` связывает запись с её ситуацией (§6, пункт 2). `source` указывает на оригинал.
- Оценки, если человек их даёт, остаются в тексте столбца (§6, пункт 3).
- С терапевтом (`therapy-confidential`) добавьте в запись `"handling": ["person-only"]`: LA-4 до неё не доходит (§6, пункт 11).

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-08", "precision": "day"},
 "results": [
   {"type": "thought-record",
    "situation": "Draft ready to send to my team lead on Tuesday afternoon.",
    "thought": "If she sees the stair detail she will think I cannot do this job.",
    "emotion": "Dread, about 70 out of 100.",
    "behavior": "Kept the draft and reworked the stair detail.",
    "alternative": "She asked for a draft, not a finished plan. Early comments are cheaper for both of us."}],
 "validityFlags": ["self-identified-only"], "source": "src-01", "derivedFrom": ["ep-01"],
 "reviewAfter": "P3M", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T21:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"], "synthetic": true}
```

**Кто видит:** человек; по разрешению, которое называет линзу, — вся запись целиком, включая столбец эмоции (§6, пункт 4). Эпизод выдаётся по условию разрешения на эпизоды.

### Шаг 5. Утверждения, которые человек принимает (Claim → `claims`)

Если запись мыслей показала человеку что-то, что он хочет сказать о себе, запишите это как утверждение его словами и только после того, как он сам это скажет ([§9.4](../../spec/SPECIFICATION.md#94-claim)). Склонность, которую человек узнаёт в себе, — это вид `disposition` с уточнением `self-described-tendency` (CL-3 допускает `declared` от самого человека). `derivedFrom` указывает на запись мыслей.

```json
{"id": "c-01", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When I expect a draft to be criticised, I hold it back and keep reworking details.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T21:10:00Z", "horizon": "focus",
 "derivedFrom": ["as-01"], "contexts": ["work"], "synthetic": true}
```

**Кто видит:** через `derivedFrom` утверждение получает `special` и `mental-health` (C3), поэтому до него доходит только разрешение, которое называет его по id или по категории; разрешение из шага 2 не доходит. Если человек хочет шире поделиться простым утверждением — например, целью «Отправлять первый черновик к полудню среды» для рабочего помощника, — запишите это утверждение без `derivedFrom`: со ссылкой рабочий помощник его никогда не получит (проверено; §6, пункт 6).

### Шаг 6. Толкование эпизода агентом, с другими объяснениями (Interpretation → `interpretations`, Proposal → `proposals`, Review → `reviews`)

Только по разрешению из шага 2 (`infer`, называющее линзу), данному раньше этой записи, и пока принятие линзы человека не говорит `off` (I5). При `ask-first` спрашивайте человека перед каждым толкованием («Можно предложить один взгляд на вторник?»); на уровне L2 этот вопрос записывается как событие Event `ask-first`.

Запишите толкование как ваше предложение ([§10.3](../../spec/SPECIFICATION.md#103-interpretation), [схема](../../spec/schema/interpretation.schema.json)):

- `origin: "inferred"`, `epistemic: "hypothesis"`, `causal` не сильнее `hypothesized`, а также `underGrant` с `purpose`.
- Хотя бы одно основание, хотя бы два других объяснения, из которых хотя бы одно непсихологическое, и `limits` (I4).
- Вопрос или «возможно», никогда не поправка. Никаких ярлыков для мыслей (I3). Никаких слов о чувствах от себя: чувства человека остаются в его записи мыслей.

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"},
 "adoption": "la-01",
 "text": "An expectation that the team lead would judge her ability by one detail may have come before the draft was held back.",
 "causal": "hypothesized", "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-09T08:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "grounds": [{"ref": "as-01", "kind": "instrument"}, {"ref": "ep-01", "kind": "evidence"}],
 "alternatives": [
   {"text": "The stair detail really was open: the structural figures arrived late.", "kind": "informational"},
   {"text": "It was the third late evening that week.", "kind": "physiological"}],
 "limits": "One episode, one lens and one thought record; a self-reflection aid, not a clinical reading.",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"], "synthetic": true}
```

Подайте его записью Proposal ([§11.2](../../spec/SPECIFICATION.md#112-proposal)); `expiresAt` необязателен и по умолчанию равен 30 дням после `recordedAt`. Пояснение пишется для человека и не цитирует ни одной записи.

```json
{"id": "prop-01", "proposer": "a-01", "recordedAt": "2026-09-09T08:00:00Z", "underGrant": "g-01",
 "purpose": "self-reflection", "items": ["in-01"],
 "rationale": "One reading of Tuesday's draft, with two other explanations to weigh.",
 "expiresAt": "2026-10-09T08:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-09T07:58:00Z"}}
```

Человек решает записью Review: `endorse`, `partially-endorse` (своими словами), `reject` или `contest`. Молчание — не согласие: предложение без ответа истекает как отклонённое.

```json
{"id": "rv-02", "target": "in-01", "action": "partially-endorse", "by": "subject",
 "recordedAt": "2026-09-16T19:00:00Z",
 "endorsedPart": "I expected her to judge me by the stair detail."}
```

**Кто видит:** пока предложение открыто — человек и вы (в режиме просмотра своих предложений, [§12.5](../../spec/SPECIFICATION.md#125-proposer-view)). После решения человека толкование выдаётся по разрешению со своей отметкой, здесь `partly-confirmed` («частично подтверждено»). С терапевтом толкование ссылается на принятие и становится `person-only` (LA-4).

### Шаг 7. Практика из инструментов линзы и её итог (Practice → `practices`, Episode → `episodes`, Outcome → `outcomes`)

Вы можете предложить запись мыслей как практику (`agentMayOffer: true`). Если человек её оставляет, он записывает её своими словами как Practice ([§17.1](../../spec/SPECIFICATION.md#171-practice), [схема](../../spec/schema/practice.schema.json)): `source.route: "from-lens"`, `templateId: "cbt.thought-record"` и `source.by` — вы, если предложили вы. Если практику записываете вы сами, у неё `route: "from-agent"`, она остаётся предложенной, пока человек её не примет (PC-1), и требует вашего разрешения (INF-1). С терапевтом добавьте `"handling": ["person-only"]` (§6, пункт 11).

```json
{"id": "pr-01", "name": "Thought record before I hold a draft back",
 "description": "Ten minutes of writing before I decide to keep a draft another day.",
 "practiceKind": "writing",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:cbt", "templateId": "cbt.thought-record", "by": "a-01"},
 "steps": ["One line: the situation", "What went through my mind", "The feeling and how strong, 0 to 100", "What I did", "What else could be true"],
 "duration": "PT10M", "limits": "Not to talk myself out of a real problem in the drawing.",
 "initialStatus": "in-use", "nonClinical": true, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-10T19:00:00Z", "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["work"], "synthetic": true}
```

Как всё прошло, человек записывает как Outcome со ссылкой на эпизод, где он использовал практику ([§17.2](../../spec/SPECIFICATION.md#172-outcome)). В примере это эпизод `ep-02`, «Section draft sent», записанный как в шаге 4а.

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-02", "result": "helped", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-12T13:05:00Z", "contexts": ["work"], "synthetic": true}
```

**Кто видит:** человек; по разрешению из шага 2 вы получаете практику (она несёт линзу в `source.lens`) и `ep-02` (по условию на эпизоды), но не итог, потому что линзы у итога нет.

**Что в итоге получает спутник.** Из корня репозитория выполните:

```sh
python3 -B tools/ohc_query.py <папка вашего контекста> project --grant g-01 --purpose self-reflection --now latest
```

Для разобранного примера папка — `docs/lenses/examples/cbt`. `--purpose` обязателен и должен быть одной из целей разрешения. `--now latest` считает разрешение на момент самой новой записи в файле, поэтому результат не зависит от сегодняшней даты. Команда печатает две строки (какое время она взяла и какой ключ) и затем выдачу в формате JSON. Выданные записи перечислены в `statements` (`lensAdoptions`: `la-01`; `assessments`: `as-01`; `practices`: `pr-01`), в `experience` (`episodes`: `ep-01`, `ep-02`) и в `interpretations` (`interpretations`: `in-01`). В `derived` — вычисленные отметки; у `in-01` это `"label": "partly-confirmed"`. Спутник не получает источник `src-01`, утверждение `c-01` и итог `oc-01`.

### Шаг 8. Проверка

Из корня репозитория:

```sh
python3 -B tools/check.py <папка вашего контекста> --level L1 --json
```

Исправляйте ошибки, пока проверка не сообщит `"valid": true` и `"levelMet": "L1"`. Если вы видите INF-1 на своём толковании или PR-2 на своём предложении, хотя в обоих есть `underGrant` и `purpose`, значит, разрешение дано позже них: передвиньте `recordedAt` и `expressedBy.at` разрешения раньше (§6, пункт 13). Проверка ещё сравнивает свой вывод с файлом `expected-check.json` рядом (правило X-3), но только когда папка лежит внутри папки с именем `examples`; для папки вашего собственного контекста он не нужен. Проверка не читает хранилище (шаг 3): проверьте его сами.

## 4. Никогда

- **Запрещённые цели.** Никогда не используйте записи этой линзы для `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и других целей из [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed), ни по какому разрешению; записи мыслей часто касаются работы, помните об этом. Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Выводы агента — только как предложения.** Пишите толкования только по разрешению с `infer`, как гипотезы `inferred` с основаниями, другими объяснениями и границами. Никогда не заполняйте запись мыслей за человека (`mode: "agent-inference"` не для этой линзы, даже если проверка это пропускает; §6, пункт 5). Никогда не переносите результаты в другую линзу (`crossLensMapping: not-allowed`).
- **Никаких ярлыков.** Никогда не применяйте названия «искажений», диагнозы или клинические ярлыки (I3). Никогда не называйте мысль иррациональной или неправильной и никогда не переубеждайте человека.
- **Никакой терапии.** Никогда не представляйтесь как когнитивно-поведенческая терапия. Клиническая работа — дело клиницистов; медицинские записи — только указатели (HealthRef).
- **Никаких выведенных чувств.** Никогда не выводите значение эмоции, настроения или стресса из поведения, голоса, лица или набора текста (R-X4) и никогда не вставляйте такое в свои толкования.
- **Никаких цитат против человека и давления.** Никогда не используйте запись мыслей или принятое толкование, чтобы давить на человека («вы же сами говорили, что…»); соблюдайте `no-quote-back` и `no-leverage`, где человек их ставит.
- **Товарный знак.** В описании линзы товарных знаков нет. Не называйте коммерческую программу или приложение так, будто OHC её предоставляет.

## 5. Разобранный пример

[examples/cbt/context.json](examples/cbt/context.json) — один файл уровня L1 о Йоване (Jovana), вымышленном человеке. `"synthetic": true` стоит у самого контекста и у каждой записи с содержанием. В файле ровно записи раздела 3, и время записей идёт в порядке шагов:

| Шаг | Записи |
|---|---|
| 0 | оболочка с модулями `core`, `governance`, `lenses`, `practices` |
| 1 | сторона `a-01`, `la-01`, `rv-01` |
| 2 | `g-01` |
| 3 | `src-01` и его байты в [vault/60/](examples/cbt/vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md) |
| 4 | `ep-01`, `as-01` |
| 5 | `c-01` |
| 6 | `in-01`, `prop-01`, `rv-02` |
| 7 | `pr-01`, `ep-02`, `oc-01` |

Варианты (принятие, записанное агентом; терапевт) в файл не входят.

```sh
python3 -B tools/check.py docs/lenses/examples/cbt --level L1 --json
```

Проверка сообщает `"valid": true` и `"levelMet": "L1"`, без ошибок и предупреждений. [expected-check.json](examples/cbt/expected-check.json) — точный вывод. Выдача из шага 7:

```sh
python3 -B tools/ohc_query.py docs/lenses/examples/cbt project --grant g-01 --purpose self-reflection --now latest
```

## 6. Что пока не помещается

Это пробелы OHC 0.1 для этой линзы, найденные при написании рецепта и когда новичок прошёл по нему. К каждому — предложение на следующий проход.

1. **Нет способа для собственного листа человека.** В закрытом списке способов получения результата нет способа для записей, которые человек делает в листе; ближе всего `self-identified` («человек выбрал тип или результат») с отметкой `self-identified-only`. *Предложение:* добавить способ `self-recorded` (`origin` `declared`) для листов, журналов и дневников внутри линзы.
2. **Запись мыслей не может сказать, о какой она ситуации.** У AssessmentRecord нет `about`; `derivedFrom: [Episode]` у записи `declared` — натяжка, а столбец `situation` повторяет эпизод. *Предложение:* необязательное поле `about: [Episode]` у AssessmentRecord (или `situationRef` в результате), и тогда `situation` можно не заполнять.
3. **Только пять строк.** В результате нет места для силы чувства, для того, насколько человек верит мысли до и после, и для нескольких мыслей и чувств в одной записи, поэтому собственные числа человека оказываются внутри текста. *Предложение:* необязательные числовые поля (`emotionIntensity`, `beliefBefore`, `beliefAfter`, от 0 до 100) и списки для нескольких мыслей и чувств — всё от самого человека.
4. **Нельзя делиться по столбцам и показать, кто что написал.** По разрешению на линзу столбец эмоции уходит вместе с остальными; человек не может поделиться ситуацией и альтернативой, оставив чувство при себе. Запись также не может показать, что альтернативу сначала предложил агент, а потом её принял человек. *Предложение:* ограничения по столбцам (или ссылка на закрытое утверждение `state`/`emotion` вместо текста) и необязательное `suggestedBy` у столбца.
5. **Запись мыслей, написанная агентом, проходит проверку.** `mode: "agent-inference"` с отметками AR-2 принимается для типа результата `thought-record`, хотя описание линзы говорит, что запись содержит только собственные записи человека. *Предложение:* правило: результат `thought-record` требует способа `self-identified` (или предлагаемого `self-recorded`) либо `practitioner-facilitated` и автора — самого человека.
6. **Происхождение мешает делиться.** Утверждение с `derivedFrom` на запись мыслей получает `special` и `mental-health`; простая цель, записанная так, никогда не доходит до рабочего помощника, а та же цель без `derivedFrom` доходит (проверено). Человеку приходится выбирать между происхождением и возможностью поделиться. *Предложение:* ссылка на происхождение, которая не переносит уровень, когда утверждение пишет сам человек (например `inspiredBy`), или `relax`, который может явно снять унаследованные категории.
7. **Ограничения записи не сверяются с линзой, а ограничения этой линзы узкие.** *Исправлено в 0.1.0-draft.2:* ни записи, ни линзы не несут запрещённых целей; все тринадцать из §8.10 связывают любого получателя, какой бы ни была линза.
8. **У предложения линзы агентом нет честного происхождения.** Если принятие записывает агент, оно не может быть `declared` (ENV-2 требует `text`, которого у LensAdoption нет), поэтому оно должно быть `inferred` с основаниями и разрешением `infer`, хотя предложить линзу — не вывод о человеке. Отдельно: принятие `agent-suggested` остаётся предложенным до `admit`, даже если его записал сам человек, а таблица в §10.5 этого не говорит. *Предложение:* разрешить `declared` с коротким `rationale` для предложения линзы агентом и записать правило о принятии в §10.5.
9. **Писцу нужно разрешение.** §15.9 позволяет агенту записывать то, что человек диктует, от имени человека, с `recordedBy` — агентом, но тогда INF-1 требует разрешения с `write`. *Предложение:* освободить от INF-1 записи `declared` с `assertedBy: "subject"` и агентом в `recordedBy`, когда человек их подтверждает, или ввести отдельную роль писца.
10. **У маленькой проверки ожидания нет шаблона.** Описание линзы говорит, что изменения идут через «маленькие другие действия», но среди инструментов есть только запись мыслей, а у Outcome нет места для того, что ожидалось и что вышло. *Предложение:* инструмент `cbt.small-test` (упражнение, самостоятельно, агент может предложить) и необязательные тексты `expected`/`observed` у Outcome, которые пишет человек.
11. **Тайна терапии не доходит до записей мыслей и практик.** LA-4 (`therapy-confidential` значит `person-only`) передаётся только через поле `adoption`. У AssessmentRecord и Practice такого поля нет, поэтому результаты линзы из терапии выдаются по разрешению на линзу (проверено с принятием через терапевта: `as-01`, `pr-01` и оба эпизода выдаются; скрыты только принятие и толкование агента). Конфиденциальность, которую обещает путь `inherited-from-practice`, не доходит до самых важных записей. *Предложение:* необязательное поле `adoption` у AssessmentRecord и у Practice (путь `from-lens`), и LA-4 для них; или применять LA-4 к каждой записи с пометкой линзы (`lens` или `source.lens`), пока действующее принятие этой линзы — `therapy-confidential`, и предупреждать, если такая запись не `person-only`.
12. **Происхождение может указывать в будущее.** Запись может ссылаться в `derivedFrom`, `grounds` или `evidence` на запись, чей `recordedAt` позже (проверено: принятие, записанное агентом 2026-10-01, с `derivedFrom` на эпизод, записанный 2026-10-04, проходит). След `agent-suggested` держится на ссылке туда, где человек попросил, а ссылка в будущее лишает этот след смысла. *Предложение:* правило (предупреждение на L1, ошибка на L2): у каждой цели `derivedFrom`, `grounds.ref` и `evidence.source` `recordedAt` не позже, чем у ссылающейся записи, кроме случая, когда ссылающаяся запись заменяет прежнюю версию.
13. **INF-1 не говорит, что дело во времени.** Если разрешение есть, но дано позже записи, INF-1 всё равно пишет, что запись «MUST carry `underGrant` … and `purpose`», хотя оба поля в ней есть (проверено). По сообщению нельзя понять, что нарушен порядок. *Предложение:* разделить INF-1 на «нет `underGrant`/`purpose`» и «разрешение не действовало на момент `recordedAt` (дано позже, истекло или отозвано)», с временем выдачи разрешения в сообщении, как уже делает PR-2.
14. **Хранилище никогда не проверяется.** Проверка уровня L1 не открывает хранилище: источник, чей файл отсутствует или у которого неверны `size` или `sha256`, проходит. *Предложение:* режим проверки (например `--vault`), который находит `vaultPath` относительно папки контекста и сверяет наличие файла, размер и хеш, сообщая об отсутствующем файле как о предупреждении; и прогонять его по опубликованным примерам, которые теперь содержат свои байты.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
