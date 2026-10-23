# Рецепт линзы: Эннеаграмма (девять мотивационных паттернов)

**Рецепт · линза `urn:ohc:lens:enneagram` 0.2.0 · OHC 0.1.0-draft.2 · справочный документ (informative) · 12 октября 2026**

Этот рецепт по шагам показывает, как то, что человек знает о своём паттерне Эннеаграммы (собственное узнавание, отчёт теста, который принадлежит ему, или типирующее интервью), превращается в записи OHC под его контролем.

Описание линзы — [spec/lenses/enneagram.lens.json](../../spec/lenses/enneagram.lens.json): `descriptorStatus: draft`, вид `type-categorical`, уровень измерения `T4` (спорный), онтологический статус `theoretical-model`. Линза помогает размышлять о повторяющихся мотивах и даёт общий словарь, который человек выбрал сам. Она не доказывает, что девять отдельных типов существуют, не ставит диагнозов и не говорит о пригодности к работе. Прочитайте `mentalModel` в описании линзы до начала работы: собственное узнавание человека важнее любого балла.

Форма записей описана в [SPECIFICATION.md](../../spec/SPECIFICATION.md): §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §17 (Practice, Outcome) и §12 (Grant); схемы лежат в [spec/schema/](../../spec/schema/). Правила линз — в [LENSES.md](../../spec/LENSES.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:enneagram-basic`](../../spec/playbooks/enneagram-basic.playbook.json) («Эннеаграмма: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; разбор того, что произошло; подготовка к трудному разговору; выбор между вариантами. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Использовать? | Куда идёт |
|---|---|---|
| Собственное узнавание человека, сказанное в разговоре («Я узнаю себя в паттерне 4, особенно когда на меня давят») | Да | AssessmentRecord с `mode: self-identified` (шаг 3а), Claim его словами (шаг 4) |
| Отчёт инструмента, который человек прошёл и который принадлежит ему. RHETI® v2.5 — единственный инструмент Эннеаграммы в каталоге 0.1 | Да | Source (шаг 2) и AssessmentRecord с `mode: vendor-report-import` (шаг 3б) |
| Результат любого другого теста по Эннеаграмме (бесплатные тесты в интернете, опросники других школ) | Только как собственное определение человека | Source (шаг 2, вариант «тест вне каталога») и AssessmentRecord с `mode: self-identified` (шаг 3а, вариант); никогда как результат инструмента: проверка отвергает инструмент, которого нет в списке линзы (AR-8) |
| Заметки или результат типирующего интервью с коучем, преподавателем или ведущим | Да, с письменным разрешением специалиста | Путь `inherited-from-practice` (шаг 1, вариант), Source с разрешением и Source с заметками (шаг 2, вариант) и AssessmentRecord с `mode: practitioner-facilitated` (шаг 3в) |
| Рассказы человека об эпизодах и его собственные прочтения их через линзу | Да | Episode и Interpretation (шаг 5) |
| Прочтение агента («судя по тому, как вы пишете, вы, похоже, восьмёрка») | **Только по разрешению человека** | Интерпретации агента нужны `suggest` и `infer`, называющие линзу, и действующее принятие линзы не в `off` (I5). Рекомендация описания: никогда не типировать человека и не выдавать описания типов за факты о нём. В примере человек не разрешает ничего из этого. |

## 2. Прежде чем начать

### 2.1 Путь принятия линзы

Выберите путь вместе с человеком. От него зависит, кто пишет LensAdoption и когда запись начинает действовать. В шаге 1 есть полная запись для каждого пути, который используют разобранные примеры.

| Путь | Когда | Что меняется |
|---|---|---|
| `self-chosen` | Человек сам выбирает линзу. | Запись пишет сам человек: `assertedBy: "subject"`, `origin: "declared"`. Она действует сразу. Этот путь — в разобранном примере. |
| `agent-suggested` | Человек попросил агента о способах взглянуть на повторяющиеся мотивы (условие `suggestionRequires` в описании линзы) и принял предложенную линзу. | Сначала человек даёт агенту разрешение с действием `suggest`, область которого называет линзу. Затем агент пишет запись по этому разрешению: `suggestedBy` и `assertedBy` — его Party id, `origin: "observed"` (агент фиксирует, что человек согласился; `declared` отвергается правилом ENV-2), `underGrant` — id разрешения, `purpose` — одна из целей (`purposes`) этого разрешения. Запись остаётся `proposed`, пока человек сам не напишет Review `admit`. Агент никогда не принимает её сам (LA-1). Записи: шаг 1, вариант «предложил агент». |
| `inherited-from-practice` | Линза пришла от коуча, преподавателя или ведущего человека (`inheritanceRoles` в описании линзы). Используйте этот путь всегда, когда в работе есть типирующее интервью. | Коуч — участник (Party) с `role: "practitioner"`. В записи есть блок `practice`. Если хранятся материалы встреч, например заметки типирующего интервью, сначала сохраняется разрешение специалиста — Source вида `practitioner-release`, и его id ставится и в `practice.releaseRef` принятия линзы (LA-3), и в `custody.releaseRef` Source с заметками (SR-7). `confidentiality: "practitioner-scope"`, `onEnd: "ask"`. Принятие линзы не даёт специалисту доступа (LA-2); доступ даёт только Grant (шаг 7). Записи: шаг 1, вариант «с коучем». |
| `imported` | Программа импорта создаёт запись из отчёта инструмента. | `origin: "derived"`, `derivedFrom` указывает на Source с отчётом, `generatedBy` называет программу, `importedFrom` содержит идентификатор прогона `run`; у каждой записи `importedFrom.importedAt` равно её собственному `recordedAt` (ENV-3). Сама запись и все AssessmentRecord с тем же `importedFrom.run` остаются `proposed`, пока человек их не примет (LA-5). Полностью этот путь показан в [рецепте schwartz-values](schwartz-values.ru.md). |

В примере `agentInterpretation` на любом пути равно `"off"` — это значение по умолчанию, которое человек оставляет: прочтения через эту линзу пишет только он сам (I5). Человек может это изменить.

### 2.2 Согласие

- Агент говорит языком линзы, когда человек её принял, и словами самого человека; он никогда не типирует человека (`agentPosture`).
- Без разрешения (Grant) ничего не покидает контекст (R-G1). Любой результат в этой линзе считается данными особой категории, поэтому разрешение, которое им делится, требует `basis.legal: "explicit-consent"`, должно называть записи по id, по линзе или по категории `mental-health` (R-G3) и действует не дольше 180 дней (GR-1).
- Заметки специалиста попадают в контекст только с его разрешением, которое хранится отдельным Source.

### 2.3 Значения по умолчанию для этой линзы

| Поле | Значение | Почему |
|---|---|---|
| `sensitivity` | `"special"` на каждой записи, которая называет линзу (LensAdoption, AssessmentRecord, Interpretation с `lens`, Practice с `source.lens`), на каждом Source с отчётом, снимком экрана, разрешением или заметками и на каждом Claim или Tension, которые ссылаются на результат | `defaults.sensitivity` в описании линзы; AR-5; I9; правило распространения C3 |
| `categories` | `["mental-health"]` на тех же записях | `defaults.categories` в описании линзы |
| `handling` на результатах | `["no-infer", "no-quote-back"]` | `no-infer`: человек не допускает результат ни к каким выводам и сопоставлениям (M-7). `no-quote-back`: никто не предъявляет человеку тип как факт о нём («как четвёрка, вы…»). |
| `reviewAfter` | не указывать | В описании линзы стоит `on-change`, а поле AssessmentRecord не может его хранить (раздел 6) |
| `maxRelease` у Source | `"index"` | Получатель никогда не получает ни сам файл отчёта, ни его название, ни текст |

### 2.4 Что никогда не хранится

- Тексты вопросов RHETI®, ответы на них, ключи подсчёта и текст отчёта (AR-3; `neverStore` в записи инструмента). Файл отчёта может лежать в собственном хранилище человека; ни одна запись его не цитирует.
- Описательные названия типов, которые даёт школа или издатель. Подписи конструктов — только `Type 1` … `Type 9` (`ip.restrictions` в описании линзы).
- Название теста вне каталога — ни в каком поле.
- Метка типа, полученная из результата другой линзы, например из баллов Большой пятёрки (M-4).
- Описания «базовых страхов» или того, что «нужно» типу, записанные как факты о человеке.
- Балл или тип как суждение о человеке («она девятка»). Результат — датированное описание внутри одного человека с указанием способа, которым он получен.

## 3. Шаги

Фрагменты кода ниже — записи из разобранных примеров (раздел 5); они проходят проверку по названным схемам. В них стоит `"synthetic": true`, потому что это примеры. Используйте непрозрачные id (`as-1`, а не `as-type4`; W-ID1). Время — в формате RFC 3339 со смещением.

**Один раз подготовьте контекст.** Создайте каталог для контекста (дальше — *каталог контекста*) и сохраните в нём эту заготовку под именем `context.json`. Каждый шаг ниже называет массив, в который идёт его запись; порядок записей внутри массива не важен.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:linnea:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:linnea", "displayName": "Linnea (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-24T22:05:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "s-01", "partyKind": "software", "label": "Online test report"},
   {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:enneagram", "version": "0.2.0",
             "sha256": "1c22298a0fb2bc26f272a35d5382eefb026585597aa3020279ea1078e2c99a3b"}],
 "lensAdoptions": [], "sources": [], "assessments": [], "tensions": [], "claims": [], "reviews": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- Поля `format`, `specVersion`, `id`, `version` и `subject` обязательны (`context.schema.json`). `holder`, `lang`, `created` и `policy` необязательны; оставьте их как в заготовке. Неиспользуемые массивы можно не писать.
- `"synthetic": true` помечает пример. В примере это поле ОБЯЗАНО стоять и в корне контекста, и на каждой содержательной записи, иначе проверка выдаёт ошибку CX-8. **Для реального человека** дайте `id` и `subject.id` вид `urn:uuid:<новый UUID>` и не ставьте `synthetic` ни в корне, ни на записях.
- `lenses[].sha256` — SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/enneagram.lens.json`.
- Модуль `governance` нужен для разрешений Grant (шаги 1 и 7), `practices` — для Practice и Outcome (шаг 6).
- Каждого участника, на которого вы ссылаетесь, перечислите в `parties` (CX-3). Основному пути нужны `s-01` и `a-01`. Вариант «тест вне каталога» добавляет `{"id": "s-02", "partyKind": "software", "label": "Online test site"}`; варианту «с коучем» нужен `{"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"}`.
- Проверка проходит только тогда, когда в контексте есть Claim или Episode с рассказом (LV-0); до шага 4 она сообщает об ошибке LV-0.

### Шаг 1. Человек принимает линзу: LensAdoption

Человек говорит, что хочет смотреть на себя через Эннеаграмму. Запишите одну LensAdoption (схема `lens-adoption.schema.json`, массив `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "enneagram.type-label", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-10-01T19:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `uses` выберите вместе с человеком: `speak-in-lens` (агент может пользоваться словами паттернов), `store-results`, `interpret` (собственные прочтения человека), `offer-practices` (агент может предложить `enneagram.recognition` — единственный элемент инструментария с `agentMayOffer: true`), `recall`.
- Если в работе есть типирующее интервью со специалистом, сразу выберите путь `inherited-from-practice` (вариант «с коучем» ниже). Так рекомендуется; проверка этого не требует (раздел 6).

**Вариант «предложил агент» (`agent-suggested`).** Запишите три записи в таком порядке. Все три есть в [examples/enneagram/variants/with-agent/context.json](examples/enneagram/variants/with-agent/context.json).

(1) Человек даёт агенту разрешение предлагать (массив `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-29T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:enneagram"]}], "exclude": [{"ids": ["as-4"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-27T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-29T10:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest this lens and its recognition exercise; it never sees my results."}
```

(2) Агент пишет принятие линзы по этому разрешению (массив `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "enneagram.type-label", "origin": "observed", "assertedBy": "a-01",
 "underGrant": "g-0", "purpose": "self-reflection", "recordedAt": "2026-09-29T10:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

(3) Человек принимает её (массив `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-29T10:10:00Z"}
```

- `purpose` в принятии линзы ОБЯЗАН быть одной из целей (`purposes`) разрешения; иначе не проходит INF-1.
- Область разрешения ОБЯЗАНА называть линзу: `{"lenses": [...]}`. Подстановка вроде `{"all": true}` не считается, и INF-1 не проходит.
- Разрешению достаточно одного действия `suggest`. В его `exclude` перечислены id результатов человека (здесь `as-4`, шаг 3а), чтобы агент, который предлагает, никогда их не видел; id можно указать ещё до того, как запись появилась.
- `origin` — `"observed"`: агент фиксирует, что человек согласился. `"declared"` не проходит ENV-2 (раздел 6).
- Пока человек не написал `admit`, принятие линзы остаётся `proposed`, и его не получает ни один получатель. `admit` пишет только сам человек (LA-1).
- То же разрешение покрывает и предложение агентом практики (шаг 6, вариант).

**Вариант «с коучем»: линза пришла от специалиста.** Добавьте участника-коуча `p-01` в `parties`, запишите Source с разрешением (шаг 2, вариант), затем это принятие линзы, затем Source с заметками. Всё это есть в [examples/enneagram/variants/with-coach/context.json](examples/enneagram/variants/with-coach/context.json).

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-08-01", "releaseRef": "src-2"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "enneagram.type-label",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `practice.releaseRef` — id Source с разрешением. Тот же id поставьте в `custody.releaseRef` Source с заметками (шаг 2). Без `practice.releaseRef` правило LA-3 не проходит, как только заметки сохранены.
- `practice.role` — `coach`, `teacher` или `facilitator` (`adoption.inheritanceRoles` в описании линзы).
- `confidentiality: "practitioner-scope"` и `onEnd: "ask"`: когда отношения со специалистом заканчиваются, человек сам решает, что будет с принятием линзы.

**Кто видит по умолчанию:** только сам человек. Принятие линзы на пути `agent-suggested` никому не выдаётся, пока человек его не принял.

### Шаг 2. Сохраните оригинал: Source

Если у человека есть файл отчёта, снимок экрана или заметки специалиста:

1. вычислите SHA-256 файла: `shasum -a 256 <файл>`;
2. скопируйте файл в каталог контекста как `vault/<первые два шестнадцатеричных знака хеша>/<хеш>.<расширение>`;
3. запишите Source (схема `source.schema.json`, массив `sources`), у которого `content.locator.vaultPath` — этот же путь, относительно каталога контекста и начиная с `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/64/64d90261deb72a4b6bf2c0220a75433793731f33d7555598b864f5d6013c1ec9.pdf"}, "sha256": "64d90261deb72a4b6bf2c0220a75433793731f33d7555598b864f5d6013c1ec9", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-28T20:00:00Z", "authorship": {"author": "s-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:02:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author` — программный участник для отчёта издателя.
- Не ставьте `title` и не пишите `summary`, который повторяет текст отчёта.
- Если файл на месте, проверка читает его и сравнивает хеш с `sha256`; при расхождении не проходит SR-2. `"vaultContentRead": false` в отчёте проверки значит, что содержимое не разбиралось; хеш при этом проверяется. Если файла нет, как в разобранных примерах, проверяется только запись.

**Вариант «тест вне каталога»: бесплатный тест в интернете.** `sourceKind` — `instrument-report` для скачанного отчёта или `image` для снимка экрана. `authorship.author` — программный участник, например `s-02` («Online test site»). Никогда не называйте тест — ни в `title`, ни где-либо ещё.

```json
{"id": "src-4", "sourceKind": "image",
 "content": {"locator": {"vaultPath": "vault/fc/fc16c529b1a721d09ee4596d5d6d92dd0d2fb22ed664fdcb6fef01d0082203d9.png"}, "sha256": "fc16c529b1a721d09ee4596d5d6d92dd0d2fb22ed664fdcb6fef01d0082203d9", "mediaType": "image/png"},
 "capturedAt": "2026-09-30T20:00:00Z", "authorship": {"author": "s-02"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T20:05:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

**Вариант «с коучем»: сначала разрешение, потом заметки.** Разрешение — это письменное согласие специалиста на то, чтобы заметки хранились у человека. Сохраните его первым:

```json
{"id": "src-2", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/22/22f766eb7183cf2ec7f3e20f0bc59eb224e2f66fdc07a867805208b880b83f74.pdf"}, "sha256": "22f766eb7183cf2ec7f3e20f0bc59eb224e2f66fdc07a867805208b880b83f74", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T18:50:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

Затем заметки типирующего интервью со ссылкой на то же разрешение:

```json
{"id": "src-3", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/b9/b9212fcb20d7a5360968d7106f6030f5f296ce526a63f4eb1afd4450b15d4776.pdf"}, "sha256": "b9212fcb20d7a5360968d7106f6030f5f296ce526a63f4eb1afd4450b15d4776", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-2"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-01T19:02:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Id разрешения `src-2` стоит дважды: здесь в `custody.releaseRef` (SR-7) и в `practice.releaseRef` принятия линзы (шаг 1; LA-3).

**Кто видит по умолчанию:** только сам человек, на любом уровне выдачи (V-0). Получатель может получить самое большее уровень `index`: вид, тип файла и день, но никогда сам файл или название.

### Шаг 3. Запишите результаты: AssessmentRecord

Пишите по одной AssessmentRecord на каждый способ, которым получен результат (схема `assessment-record.schema.json`, массив `assessments`). Id конструктов берутся из `constructs` описания линзы: `enneagram/type-1` … `enneagram/type-9`, `enneagram/wing`, `enneagram/instinctual-variant`.

**3а. Собственное узнавание человека** (элемент инструментария `enneagram.recognition`: человек читает нейтральные описания девяти паттернов и говорит, какие узнаёт и когда):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-10-01", "precision": "day"},
 "results": [
   {"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "self-identified", "alternatives": ["enneagram/type-9"]},
   {"type": "type-assignment", "construct": "enneagram/wing", "label": "Wing: type 5", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:05:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- Для `self-identified` `origin` — `declared` (AR-1). Поля `instrument` нет.
- В `alternatives` — другие паттерны, которые человек тоже в себе узнаёт.
- «Крыло» записывается вторым результатом `type-assignment` с `construct: "enneagram/wing"`; соседний тип можно назвать только в `label` (раздел 6). Инстинктивные варианты не записывайте или назовите их только в Claim словами человека (раздел 6).

**Вариант «тест вне каталога».** Результат бесплатного теста в интернете записывается точно как 3а, с `"source"`, указывающим на его Source (шаг 2, вариант), и без `instrument`:

```json
{"id": "as-4", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-30", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"], "source": "src-4",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T20:10:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**3б. Отчёт RHETI® v2.5, который принадлежит человеку:**

```json
{"id": "as-2", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:rheti-2.5", "version": "2.5", "form": "2.5"},
 "mode": "vendor-report-import", "assessedBy": "subject",
 "administeredAt": {"start": "2026-09-28", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "enneagram/type-1", "label": "Type 1", "raw": 14},
   {"type": "dimension-score", "construct": "enneagram/type-2", "label": "Type 2", "raw": 12},
   {"type": "dimension-score", "construct": "enneagram/type-3", "label": "Type 3", "raw": 9},
   {"type": "dimension-score", "construct": "enneagram/type-4", "label": "Type 4", "raw": 19},
   {"type": "dimension-score", "construct": "enneagram/type-5", "label": "Type 5", "raw": 17},
   {"type": "dimension-score", "construct": "enneagram/type-6", "label": "Type 6", "raw": 13},
   {"type": "dimension-score", "construct": "enneagram/type-7", "label": "Type 7", "raw": 8},
   {"type": "dimension-score", "construct": "enneagram/type-8", "label": "Type 8", "raw": 6},
   {"type": "dimension-score", "construct": "enneagram/type-9", "label": "Type 9", "raw": 21},
   {"type": "type-assignment", "construct": "enneagram/type-9", "label": "Type 9", "method": "instrument"}],
 "validityFlags": ["vendor-algorithm-undisclosed"], "source": "src-1",
 "trademarkNotice": "RHETI® (US Reg. No. 5584848) is a registered mark of Enneagram Personality Types, Inc. (dba The Enneagram Institute). Enneathought and Enneagram Institute are names it uses; their status is not verified here. All are used only to name its products.",
 "origin": "imported",
 "importedFrom": {"system": "vendor report (PDF), scores copied by the person", "importedAt": "2026-10-01T19:10:00Z"},
 "generatedBy": {"software": "vendor scoring (not disclosed)", "method": "main type as stated in the vendor report; the vendor's rule is not disclosed"},
 "formulatedAt": "2026-09-28T20:00:00Z", "assertedBy": "subject", "recordedAt": "2026-10-01T19:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"],
 "synthetic": true}
```

- `instrument.id` ОБЯЗАН быть `urn:ohc:instrument:rheti-2.5` (AR-8).
- `mode: "vendor-report-import"` требует `origin: "imported"` и `importedFrom` (AR-1). `formulatedAt` — когда отчёт был составлен; `recordedAt` — когда он вошёл в контекст (R-T5b).
- `importedFrom.importedAt` равно `recordedAt` (ENV-3). Не ставьте туда момент, когда файл копировали.
- Перенесите девять баллов по типам в `raw` так, как они напечатаны в отчёте. `rawRange` добавляйте, только если отчёт указывает диапазон. `normGroup` не ставьте: баллы описывают одного человека и не сравнивают его с нормой.
- Если отчёт называет основной тип, добавьте один `type-assignment` с `method: "instrument"`. Тогда ОБЯЗАТЕЛЬНО `generatedBy.method` (AR-6).
- `trademarkNotice` копируется слово в слово из `notice` знака `RHETI` в [spec/instruments/rheti-2.5.instrument.json](../../spec/instruments/rheti-2.5.instrument.json).
- Если человек запустил программу импорта, а не переписал баллы вручную, оставьте `assertedBy: "subject"`; если программа заодно записала принятие линзы с путём `imported`, обе записи остаются `proposed`, пока человек их не примет (LA-5).

**3в. Вариант «с коучем»: типирующее интервью** (элемент инструментария `enneagram.typing-interview`, для него нужен специалист; агент никогда его не предлагает). Используйте путь `inherited-from-practice` (шаг 1, вариант) и Source с заметками `src-3` (шаг 2, вариант). Полная запись:

```json
{"id": "as-3", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "practitioner-facilitated",
 "assessedBy": "p-01", "administeredAt": {"start": "2026-09-30", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "interview"}],
 "source": "src-3",
 "origin": "declared", "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-10-01T19:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- `validityFlags` нет. `assessedBy` и `assertedBy` — специалист; `recordedBy: "subject"`, потому что запись в свой контекст вносит сам человек (тогда INF-1 не применяется).
- Поскольку утверждает не сам человек, запись остаётся `proposed` и не выдаётся ни одному получателю, пока человек сам не напишет Review `endorse`, `partially-endorse` или `admit` (R-A1) в массив `reviews`:

```json
{"id": "rv-3", "target": "as-3", "action": "endorse", "by": "subject", "recordedAt": "2026-10-01T19:20:00Z"}
```

**Кто видит результаты по умолчанию:** только сам человек. Уровень `special`, аудитория `named`.

### Шаг 4. С чем человек согласен: Claim, и Tension, если результаты расходятся

Спросите человека, что ему подходит, и запишите только то, что он сказал, его словами, как Claim (схема `claim.schema.json`, массив `claims`). Никогда не переносите в `text` описание типа. Сошлитесь на результат в `evidence`. Вид основания (`kind`) следует за результатом, на который вы ссылаетесь: `subject-statement` для результата 3а, `instrument` для результата 3б, `practitioner` для результата 3в.

```json
{"id": "c-1", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "Under pressure I go quiet and wait to be noticed instead of asking for what I want.",
 "evidence": [{"ref": "as-1", "kind": "subject-statement"}], "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-02T08:00:00Z", "horizon": "foundation", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-quote-back"], "synthetic": true}
```

- В варианте «с коучем» Claim `c-2` ссылается так: `{"ref": "as-3", "kind": "practitioner"}`; см. файл with-coach.
- Грань `disposition` требует `origin: "declared"` от самого человека или `derived` из AssessmentRecord (CL-3). Предпочтите слова человека (`declared`). Механическая копия результата (`origin: "derived"`) требует `derivedFrom` и `generatedBy.method` и не добавляет ничего, чего нет в AssessmentRecord.
- Если узнавание человека и инструмент расходятся, сохраните обе записи и свяжите их напряжением (схема `tension.schema.json`, массив `tensions`); расхождение — тоже данные (M-8):

```json
{"id": "t-1", "between": ["as-1", "as-2"], "tensionKind": "source-divergence", "whoDecides": "subject",
 "text": "I recognise pattern 4; the test put pattern 9 first. I keep both.", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-10-01T19:15:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Если человек совсем не узнаёт себя в результате, он пишет Review (схема `review.schema.json`, массив `reviews`) `{"id": "rv-4", "target": "as-2", "action": "reject", "by": "subject", "recordedAt": "<сейчас>", "reasonCode": "not-true"}`. Запись и её основания остаются; получатели перестают её получать. `contest` вместо этого оставляет вопрос открытым для обсуждения.

**Кто видит по умолчанию:** только сам человек.

### Шаг 5. Прочтения эпизодов через линзу: Episode и Interpretation

Человек рассказывает, что произошло (Episode, схема `episode.schema.json`, массив `episodes`), и отдельно — как он это читает через линзу (Interpretation, схема `interpretation.schema.json`, массив `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T22:00:00Z", "addedAt": "2026-09-24T22:05:00Z", "accountKind": "in-the-moment", "happened": "At choir rehearsal the solo I had prepared went to another singer.", "experienced": "Hot face, then flat.", "didOrTried": "Said nothing and left before the last song.", "understandingThen": "My voice was not good enough this week."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-24T22:05:00Z", "contexts": ["community"], "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"},
 "text": "This is the pattern I recognise as my 4: I pulled back and waited to be seen instead of asking for the solo.",
 "alternatives": [
   {"text": "I had a cold that week and my voice was weak.", "kind": "physiological"},
   {"text": "The solo list may have been set before the rehearsal.", "kind": "situational"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T08:10:00Z",
 "heldDuring": {"from": "2026-10-02"}, "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Прочтения через линзу здесь пишет только сам человек. `assertedBy` — `"subject"`; прочтение агента через эту линзу не проходит правило I5, пока у принятия линзы `agentInterpretation` равно `off`.
- Прочтения никогда не записываются в Episode (EP-4). Если человек передумал, это новое Interpretation с `stance: "revision"` и `supersedes`.
- Попросите человека назвать хотя бы одно непсихологическое объяснение (`situational`, `physiological`, `informational` или `external`). Обязательно оно только для авторов, которые не являются самим человеком (I4), но оно не даёт паттерну стать единственным объяснением.
- После принятия линзы агент может задавать вопросы из описания линзы («Какой паттерн вы узнаёте в себе в напряжении?», «Что помогает, когда этот паттерн силён?»). Ответ — запись самого человека, а не агента.

**Кто видит по умолчанию:** только сам человек. Interpretation имеет уровень `special`, потому что называет линзу (I9).

### Шаг 6. Практики и их исходы: Practice и Outcome

Способ действовать, который человек берёт из линзы, — это Practice (схема `practice.schema.json`, массив `practices`); как он сработал — Outcome (схема `outcome.schema.json`, массив `outcomes`):

```json
{"id": "pr-1", "name": "Say one sentence before I go quiet",
 "description": "When I notice the pull to withdraw, I name the pattern to myself and say one sentence about what I want.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:enneagram", "templateId": "enneagram.recognition"},
 "steps": ["Notice the pull to go quiet", "Name it to myself as the pattern", "Say one sentence about what I want"],
 "limits": "Not a rule for every silence; sometimes quiet is what I want.", "initialStatus": "in-use",
 "nonClinical": true, "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T08:20:00Z",
 "contexts": ["community"], "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "partly", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-09T21:00:00Z", "note": "Said it once at rehearsal; the second time I still went quiet.",
 "contexts": ["community"], "synthetic": true}
```

- `templateId` — id элемента инструментария из описания линзы.
- Outcome, записанный кем-то кроме самого человека, — это только «оценка агента» (O-1).

**Вариант «предложил агент»: агент предлагает упражнение на узнавание.** Агент может предложить только `enneagram.recognition` (`agentMayOffer: true`). Для этого нужно разрешение с `suggest`, область которого называет линзу: разрешение `g-0` из шага 1 (если линза принята другим путём, запишите его сейчас, как показано там). Агент пишет Practice; человек её принимает. Обе записи есть в файле with-agent.

```json
{"id": "pr-2", "name": "Notice the pattern once a day",
 "description": "Once a day, notice whether the pull to go quiet showed up, without judging it.",
 "practiceKind": "reflection",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:enneagram", "templateId": "enneagram.recognition", "by": "a-01"},
 "steps": ["At the end of the day, recall one moment", "Note whether the pull to go quiet was there"],
 "limits": "Only while it feels useful; skip any day.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-10-02T09:00:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-10-02T09:30:00Z"}
```

- `underGrant` — `g-0`; `purpose` ОБЯЗАН быть одной из целей (`purposes`) `g-0` (INF-1). Область ОБЯЗАНА называть линзу; подстановка не считается.
- `initialStatus` — `"candidate"`: человек ещё не пробовал. `origin` — `"observed"`, а `assertedBy` и `source.by` — агент (`"declared"` не проходит ENV-2).
- Пока человек не написал `admit`, Practice и её Outcome не выдаются ни одному получателю (PC-1; проверено инструментом проекций). После этого получатели видят Practice с пометкой `observed` (раздел 6).
- Агент никогда не предлагает `enneagram.typing-interview` и `enneagram.record-instrument-result` (PC-2).

**Кто видит по умолчанию:** только сам человек. Practice здесь имеет уровень `special`, потому что называет линзу; Outcome получает уровень своей Practice.

### Шаг 7. Кто что может видеть: Grant

Человек решает, кто что получает. Запишите разрешение (схема `grant.schema.json`, массив `grants`); без него ничего не покидает контекст:

```json
{"id": "g-1", "recordedAt": "2026-10-03T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [
    {"lenses": ["urn:ohc:lens:enneagram"]},
    {"ids": ["c-1", "oc-1"]}], "exclude": [{"ids": ["as-2"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-31T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-03T09:00:00Z", "channel": "holder-ui"},
 "note": "Pattern language for reflection; the test scores stay with me."}
```

- Селектор `{"lenses": [...]}` охватывает все записи, которые называют линзу: принятие, результаты, прочтения и Practice, у которых её называет `source.lens`. Claim и Outcome линзу не называют; добавьте их по `ids`.
- `exclude` оставляет баллы инструмента у человека. Тогда и напряжение `t-1` не выдаётся — без какой-либо пометки, потому что один из его членов не выдаётся (T3).
- `basis.legal` ОБЯЗАН быть `explicit-consent` (записи особой категории); `expiresAt` — не позже чем через 180 дней после `recordedAt` (GR-1). В `purposes` никогда нет запрещённых целей (раздел 4).
- Ограничения обращения едут вместе с каждой записью: получатель получает `no-infer` и `no-quote-back` в `obligations.handling` и обязан их соблюдать (C-4, C-6). Своего поля для ограничений у Grant нет.
- `expressedBy.actor` — `"subject"`. Слова агента «человек согласился» никогда не считаются согласием.

**Что получает этот получатель.** Запустите проекцию, которую получил бы получатель:

```sh
python3 -B tools/ohc_query.py <каталог вашего контекста> project --grant g-1 --purpose self-reflection --now latest
```

`--purpose` — одна из целей (`purposes`) разрешения; `--now latest` считает на самый поздний момент в контексте. **Для контекста реального человека** (без `synthetic`) добавьте `--holder-key-file <файл>` — файл с секретным ключом держателя (K_holder, §12.3, шаг 11); без него инструмент останавливается с сообщением «--holder-key-file is required: this context is not marked synthetic». Для разобранного примера он выдаёт `la-1`, `as-1`, `c-1` и `pr-1` в `statements`, `in-1` в `interpretations` и `oc-1` в `recall`; не выдаёт `as-2`, `t-1`, `ep-1` и `src-1`.

### Шаг 8. Проверка

```sh
python3 -B tools/check.py <каталог вашего контекста> --level L1 --json
```

Ожидайте `"valid": true` и `"levelMet": "L1"`, затем запустите команду проекции из шага 7 для каждого разрешения. Проверка не охватывает всё, чего требует этот рецепт. Проверьте вручную:

- каждый id конструкта есть среди `constructs` описания линзы;
- `trademarkNotice` есть у результата RHETI® и отсутствует у остальных;
- вид каждого основания (`kind`) соответствует результату, на который оно ссылается (шаг 4);
- результат `practitioner-facilitated` стоит под принятием линзы с путём `inherited-from-practice`;
- ни одна запись не содержит текстов вопросов, текста отчёта, названий типов какой-либо школы или названия теста вне каталога;
- ни одна запись не написана агентом через эту линзу сверх того, что разрешают разрешение и принятие линзы человека.

## 4. Никогда

- **Запрещённые цели.** Никогда не используйте записи этой линзы для `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и других запрещённых целей (§8.10), ни по какому разрешению. Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Агент не типирует.** Агент никогда не присваивает человеку тип и не выводит его из баллов другой линзы (M-4). Оценка или прочтение агента через линзу бывает только по разрешению человека (`suggest` и `infer`, называющие линзу; для прочтений — I5), как видимое только человеку предложение (AR-2), а не тип. Сопоставление с Большой пятёркой — статистика по популяции со статусом `unresolved`; оно никогда не переводит результат одного человека.
- **Никаких названий школ как подписей.** Названия типов конкретной школы — только метки издателя, никогда не подписи конструктов и не обычные слова.
- **RHETI® — только для результатов RHETI®.** Знак используется только чтобы назвать подлинный инструмент, в номинативном смысле и с его уведомлением. Никогда не называйте RHETI® другой тест.
- **Никакого клинического языка.** Не говорите о базовых страхах, если человек сам их не поднял; не выдавайте описание типа за факт о человеке; не выдавайте паттерн за диагноз.
- **Никаких ролей и команд.** Никогда не используйте тип, чтобы предлагать роли, задачи или состав команды.
- **Агент не проводит типирующее интервью.** Типирующее интервью — дело специалиста; более глубокая работа, касающаяся личной истории, — тоже.

## 5. Разобранный пример

[examples/enneagram/context.json](examples/enneagram/context.json) — контекст в виде одного документа о Линнее; она вымышлена. В нём ровно записи основного пути из раздела 3: `la-1`, `src-1`, `as-1`, `as-2`, `t-1`, `c-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` и `g-1`, два участника и закреплённое описание линзы. Линнея узнаёт в себе паттерн 4 с крылом 5; её отчёт RHETI® ставит на первое место тип 9; она сохраняет оба результата, записывает напряжение и делится с собеседником для рефлексии словарём паттернов, но не баллами.

```sh
python3 -B tools/check.py docs/lenses/examples/enneagram --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений. Вывод совпадает с [examples/enneagram/expected-check.json](examples/enneagram/expected-check.json).

Варианты из раздела 3 лежат ещё в двух контекстах о той же вымышленной Линнее. Каждый проходит так же (`"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений):

| Вариант | Файл | Записи |
|---|---|---|
| предложил агент, тест вне каталога, практика от агента | [variants/with-agent/context.json](examples/enneagram/variants/with-agent/context.json) | `g-0`, `la-1`, `rv-1`, `src-4`, `as-4`, `c-1`, `pr-2`, `rv-2` |
| с коучем | [variants/with-coach/context.json](examples/enneagram/variants/with-coach/context.json) | `la-1`, `src-2`, `src-3`, `as-3`, `rv-3`, `c-2` |

```sh
python3 -B tools/check.py docs/lenses/examples/enneagram/variants/with-agent --level L1 --json
python3 -B tools/check.py docs/lenses/examples/enneagram/variants/with-coach --level L1 --json
```

Файлы отчёта, снимка экрана и заметок в примеры не входят; когда файла нет, проверка проверяет только запись Source (шаг 2).

## 6. Что пока не помещается

Это пробелы OHC 0.1 для этой линзы. Они собраны для следующего прохода по стандарту.

1. **Для крыльев и инстинктивных вариантов нет структурной формы.** `enneagram/wing` — один конструкт без значения, поэтому соседний тип остаётся только в свободном `label`; у инстинктивных вариантов нет кодов вовсе. Предложение: поле `role` (`main`, `wing`, `instinctual-variant`) у результатов `type-assignment` и конструкты своими словами OHC — `enneagram/instinct/self-preservation`, `enneagram/instinct/social` и `enneagram/instinct/one-to-one` — под `enneagram/instinctual-variant`.
2. **Нельзя записать «в напряжении» и «в спокойствии».** Описание линзы обращает внимание на паттерны в напряжении и в спокойствии, но у результата нет условия. Предложение: необязательное `condition` у результатов `type-assignment` (`under-stress`, `at-ease` или свободный текст).
3. **`reviewAfter: on-change` нельзя сохранить.** Поле `reviewAfter` у AssessmentRecord принимает только длительность, а §7.2 не определяет `on-change`. Предложение: разрешить `on-change` и определить его как «актуально, пока не замещено или не отмечено неактуальным».
4. **Прочтение специалиста через линзу нельзя сохранить.** *Исправлено в 0.1.0-draft.2:* LA-7 снято, а I5 применяет `agentInterpretation` только к авторам-агентам и программам; прочтению коуча нужно, чтобы коуч был в `interpretationAuthors` действующего принятия.
5. **У результатов тестов вне каталога нет честного режима.** Чаще всего люди приносят бесплатный тест из интернета, а AR-8 отвергает его как инструмент; `self-identified` скрывает, что тест был. Предложение: разрешить локальный id инструмента `urn:ohc:instrument:x-<namespace>:<name>` с флагом `unlisted-instrument`, никогда — с `trademarkNotice`.
6. **Правило об уведомлении о товарном знаке неоднозначно.** `trademarkNotice` обязательно, когда знаки линзы требуют уведомления и результат подлинный; для результата `self-identified` без инструмента это читается как «обязательно». Проверка этого не проверяет. Предложение: требовать уведомление ровно тогда, когда есть `instrument` и у знаков этого инструмента есть уведомление; в остальных случаях запрещать; добавить правило в проверку.
7. **AR-6 требует правило, которое издатель не раскрывает.** Основной тип, назначенный издателем, заставляет писать в `generatedBy.method` заглушку. Предложение: считать AR-6 выполненным для `mode: vendor-report-import` с `validityFlags`, содержащим `vendor-algorithm-undisclosed`.
8. **В записи инструмента нет шкалы результата.** Без неё программа импорта не может заполнить `rawRange`. Предложение: `forms[].resultScale` (`min`, `max`, `unit`) в записях инструментов — только из открытых источников.
9. **Не указано, какой `origin` у записей, которые агент пишет за человека.** У LensAdoption на пути `agent-suggested`, написанной агентом, и у Practice с `source.route: from-agent` нет поля `text`, поэтому `origin: declared` не проходит ENV-2; `observed` проходит, но нигде не описан, а `inferred` требует оснований, которых у таких записей нет (проверено). Предложение: указать в §10.5, §17.1 и CONTEXT-08, что такие записи используют `origin: observed` («агент фиксирует, что человек согласился»).
10. **Практика, предложенная агентом, доходит до получателей с пометкой «observed».** После `admit` человека Practice с `source.route: from-agent`, `origin: observed` и агентом в роли утверждающего выдаётся с вычисленными `label: observed` и `endorsement: not-asked`; то же с принятым `agent-suggested` принятием линзы (проверено инструментом проекций). Получатель видит предложение агента как наблюдение о человеке и не видит, что человек его принял. Предложение: вычислять `label: suggested` для Practice с `source.route: from-agent` и для принятий линзы `agent-suggested`, а `endorsement: admitted` — когда есть Review `admit` от человека; или добавить origin `suggested` вместо `observed`.
11. **LensAdoption ничего не ограничивает.** Контекст с результатами линзы, прочтениями через неё и практиками из неё, но без LensAdoption, проходит L1; результаты проходят, когда в `uses` принятия нет `store-results` и когда они записаны раньше принятия; пока принятие на пути `agent-suggested` или `imported` ещё `proposed`, селектор по линзе уже выдаёт результаты, прочтения и практики человека в этой линзе (проверено). `uses` не имеет нормативной силы; §10.5 не даёт `uses` никакого правила. Предложение: правило LA-8 — запись с `lens` или `source.lens` от автора, который не является самим человеком, требует принятия этой линзы, действующего на её `recordedAt`, с подходящим значением в `uses` (`store-results`, `interpret`, `offer-practices`); предупреждение для собственных записей человека в линзе без действующего принятия; проекция, которая не выдаёт записи линзы, пока принятие `proposed` или `paused`.
12. **Путь не обязан соответствовать способу получения результата.** Принятие `self-chosen` с результатом `practitioner-facilitated` проходит проверку (проверено), так что типирующее интервью может войти без записи об отношениях со специалистом и без его разрешения. Предложение: предупреждение, когда есть AssessmentRecord `practitioner-facilitated`, а действующего принятия её линзы с путём `inherited-from-practice` и `practice.practitioner`, равным её `assessedBy`, нет.
13. **Вид основания (`kind`) не связан с записью, на которую оно ссылается.** Claim может сослаться на результат самоопределения или специалиста с `kind: instrument`; проверка принимает любой вид для любой цели, и прежняя версия этого рецепта так и делала. Получатель тогда читает собственное узнавание как данные инструмента. Предложение: когда `ref` основания — AssessmentRecord, `kind` соответствует её `mode` (`self-identified` → `subject-statement`; `practitioner-facilitated` и режимы интервью → `practitioner`; режимы инструментов → `instrument`), или проекция выводит вид из режима.
14. **Source не может назвать линзу, к которой относится.** У снимка экрана бесплатного теста, сохранённого без записи самоопределения, нет поля `lens`, поэтому селекторы по линзе, значения линзы по умолчанию (`special`, `mental-health`) и разрешения по линзе до него не доходят, и человек не может привязать его к линзе. Предложение: необязательное поле `lens` (LensRef) у Source; тогда селекторы по линзе доходят до него на уровне его `maxRelease`, а категории линзы по умолчанию применяются к нему.
15. **Отчёт проверки читается так, будто хранилище не проверялось.** `"vaultContentRead": false` стоит, даже когда проверка прочитала файл в хранилище и сравнила хеш (на подменённом файле срабатывает SR-2; проверено). Предложение: выводить `vaultHashesChecked` (число) рядом с `vaultContentRead` и определить `vaultContentRead` как «содержимое не разбиралось».

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
