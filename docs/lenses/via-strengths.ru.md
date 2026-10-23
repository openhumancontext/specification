# Рецепт линзы: Сильные стороны характера VIA (по ссылке)

**Рецепт · линза `urn:ohc:lens:via-strengths` 0.2.0 · OHC 0.1.0-draft.2 · справочный документ (informative) · 12 октября 2026**

Этот рецепт по шагам показывает, как сильные стороны характера человека (из отчёта опросника, который принадлежит ему, от его коуча, преподавателя или терапевта, или из его собственных рассказов об эпизодах) превращаются в записи OHC под его контролем.

Описание линзы — [spec/lenses/via-strengths.lens.json](../../spec/lenses/via-strengths.lens.json): `descriptorStatus: draft`, вид `strengths-ranked`, уровень измерения `T2` (проверено с оговорками), онтологический статус `measured-construct`. Линза помогает размышлять о сильных сторонах в действии и выбирать практики, которые на них опираются. Она не говорит, каков человек по сравнению с другими, не измеряет навыки и компетентность и не говорит о пригодности к работе или должности. Ранжирование описывает одного человека и никогда не сравнивается ни с кем другим (M-5).

Классификация сильных сторон защищена авторским правом, поэтому на неё **ссылаются, а не воспроизводят**: в описании линзы нет списка конструктов, есть только `constructsByReference` с шаблоном id `via-strengths/<n>`, где `<n>` — опубликованное название сильной стороны строчными буквами, слова которого соединены дефисами.

Форма записей описана в [SPECIFICATION.md](../../spec/SPECIFICATION.md): §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §17 (Practice, Outcome) и §12 (Grant); схемы лежат в [spec/schema/](../../spec/schema/). Правила линз — в [LENSES.md](../../spec/LENSES.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:via-strengths-basic`](../../spec/playbooks/via-strengths-basic.playbook.json) («Сильные стороны характера VIA: базовые способы работы», редакция OHC), для таких ситуаций: планирование предстоящей недели; разбор того, что произошло; после неудачи; обратная связь другому человеку. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Использовать? | Куда идёт |
|---|---|---|
| Рассказ человека о своих сильных сторонах в разговоре («меня держит любопытство») | Да | Claim его словами (шаг 4) |
| Отчёт опросника, который человек прошёл и который принадлежит ему: VIA-IS-R или GACS — два инструмента каталога 0.1. Опросник бесплатен для частных лиц **[F2]** | Да | Source (шаг 2) и AssessmentRecord с `mode: vendor-report-import` (шаг 3) |
| Собственный выбор человеком своих самых сильных сторон, без опросника | Да | Claim его словами (шаг 4) или AssessmentRecord с `mode: self-identified` (шаг 3, вариант) |
| Заметки коуча, преподавателя или терапевта, который работает с сильными сторонами | Да, с письменным разрешением специалиста | Путь `inherited-from-practice` с `practice.releaseRef` (шаг 1), Source с разрешением и Source с заметками (шаг 2, вариант) |
| Рассказы человека об эпизодах и его собственное прочтение того, какие сильные стороны он проявил | Да | Episode и Interpretation (шаг 5) |
| Прочтение агента («у вас явно есть лидерство») | **Только по разрешению человека** | Интерпретации агента нужны `suggest` и `infer`, называющие линзу, и действующее принятие линзы не в `off` (I5). Позиция агента в описании: не выводить сильные стороны из поведения. В примере человек не разрешает ничего из этого. |

**[F2]** — отметка о степени проверенности: факт взят из вторичного источника и должен быть перепроверен, прежде чем на него опираться в нормативном тексте ([LENSES.md](../../spec/LENSES.md) §7.3; там же указан источник).

## 2. Прежде чем начать

### 2.1 Путь принятия линзы

Выберите путь вместе с человеком. От него зависит, кто пишет LensAdoption и когда запись начинает действовать. В шаге 1 есть полная запись для каждого пути, который используют разобранные примеры.

| Путь | Когда | Что меняется |
|---|---|---|
| `self-chosen` | Человек сам выбирает линзу. | Запись пишет сам человек: `assertedBy: "subject"`, `origin: "declared"`, без блока `practice`. Она действует сразу. |
| `agent-suggested` | Человек попросил агента о способах взглянуть на то, что ему хорошо удаётся (условие `adoption.suggestionRequires` в описании линзы), и принял предложенную линзу. | Сначала человек даёт агенту разрешение с действием `suggest`, область которого называет линзу. Затем агент пишет запись по этому разрешению: `suggestedBy` и `assertedBy` — его Party id, `origin: "observed"` (`declared` отвергается правилом ENV-2), `underGrant` — id разрешения, `purpose` — одна из целей (`purposes`) этого разрешения. Запись остаётся `proposed`, пока человек сам не напишет Review `admit` (LA-1). Записи: шаг 1, вариант «предложил агент». |
| `inherited-from-practice` | Линза пришла от коуча, преподавателя или терапевта человека (`adoption.inheritanceRoles` в описании линзы). Этот путь — в разобранном примере. | Специалист — участник (Party) с `role: "practitioner"`; в записи есть блок `practice`. Если хранятся материалы встреч, сначала сохраняется разрешение специалиста — Source вида `practitioner-release`, и **тот же id** ставится в `practice.releaseRef` принятия линзы (LA-3) и в `custody.releaseRef` Source с заметками (SR-7). Поставьте `confidentiality`: `practitioner-scope` для коуча или преподавателя; для терапевта человек может выбрать `therapy-confidential`, и тогда сама запись принятия становится `special` и `person-only` (LA-4). LA-4 действует только на записи, которые ссылаются на принятие по id, а собственные результаты, прочтения и практики человека в этой линзе на него не ссылаются; поэтому при `therapy-confidential` добавьте `"person-only"` в `handling` каждой записи, которая называет линзу (раздел 6). Оставьте `onEnd` равным `ask`: когда отношения со специалистом заканчиваются, замещающая запись принятия с `"relationship": "ended"` считается `paused`, пока человек не решит. Принятие линзы не даёт специалисту доступа (LA-2); доступ даёт только Grant (шаг 7). |
| `imported` | Программа импорта создаёт запись из отчёта опросника. | `origin: "derived"`, `derivedFrom` указывает на Source с отчётом, `generatedBy` называет программу, `importedFrom` содержит идентификатор прогона `run`; у каждой записи `importedFrom.importedAt` равно её собственному `recordedAt` (ENV-3). Сама запись и все AssessmentRecord с тем же `importedFrom.run` остаются `proposed`, пока человек их не примет (LA-5). Полностью этот путь показан в [рецепте schwartz-values](schwartz-values.ru.md). |

В примере `agentInterpretation` на любом пути равно `"off"` — это значение по умолчанию, которое человек оставляет: прочтения через эту линзу пишет только он сам (I5). Человек может это изменить.

### 2.2 Согласие

- Агент говорит языком линзы, когда человек её принял, и словами самого человека; он никогда не выводит сильные стороны из поведения (`agentPosture`).
- Без разрешения (Grant) ничего не покидает контекст (R-G1). Любой результат в этой линзе считается данными особой категории: разрешение требует `basis.legal: "explicit-consent"`, должно называть записи по id, по линзе или по категории `mental-health` (R-G3) и действует не дольше 180 дней (GR-1).
- Заметки специалиста попадают в контекст только с его разрешением, которое хранится отдельным Source.

### 2.3 Значения по умолчанию для этой линзы

| Поле | Значение | Почему |
|---|---|---|
| `sensitivity` | `"special"` на каждой записи, которая называет линзу (LensAdoption, AssessmentRecord, Interpretation с `lens`, Practice с `source.lens`), на каждом Source с отчётом, разрешением или заметками и на каждом Claim, который ссылается на результат | `defaults.sensitivity` в описании линзы; AR-5; I9; правило распространения C3 |
| `categories` | `["mental-health"]`; добавьте `"belief"` в каждую запись, которая называет сильную сторону `via-strengths/spirituality` | `defaults.categories` и `defaults.perConstruct` в описании линзы |
| `handling` на результатах | `["no-infer"]`; добавьте `"subject-initiated-only"`, когда запись называет `via-strengths/spirituality` | `no-infer`: человек не допускает ранжирование ни к каким выводам и сопоставлениям (M-7; у линзы к тому же `crossLensMapping: not-allowed`). `subject-initiated-only`: описание линзы запрещает говорить об этой сильной стороне, если человек сам её не поднял. |
| `reviewAfter` | `"P3Y"` | `defaults.reviewAfter` в описании линзы |
| `maxRelease` у Source | `"index"` | Отчёт — текст издателя, защищённый авторским правом; получатель никогда не получает ни файл, ни название, ни текст |

### 2.4 Что никогда не хранится

- Тексты вопросов опросника, ответы на них, ключ подсчёта и текст отчёта, включая описания каждой сильной стороны из отчёта (AR-3; `neverStore` в записях инструментов). Файл отчёта может лежать в собственном хранилище человека; ни одна запись его не цитирует.
- Сама классификация: перечень сильных сторон с их группами как справочные данные. Сильные стороны называют только собственные результаты человека, по id.
- Изменённая классификация: свои группировки, объединённые или переименованные сильные стороны (`ip.restrictions`).
- Любое сравнение с другими людьми: процентили относительно других, «выше среднего», групповые рейтинги (M-5).
- Сильная сторона с низким местом в ранжировании как слабость или недостаток, и любое ранжирование как суждение о человеке.

## 3. Шаги

Фрагменты кода ниже — записи из разобранных примеров (раздел 5); они проходят проверку по названным схемам. В них стоит `"synthetic": true`, потому что это примеры. Используйте непрозрачные id (`as-1`, а не `as-curiosity`; W-ID1). Время — в формате RFC 3339 со смещением.

**Один раз подготовьте контекст.** Создайте каталог для контекста (дальше — *каталог контекста*) и сохраните в нём эту заготовку под именем `context.json`. Каждый шаг ниже называет массив, в который идёт его запись; порядок записей внутри массива не важен.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:bento:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:bento", "displayName": "Bento (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-20T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"},
   {"id": "s-01", "partyKind": "software", "label": "Survey report"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:via-strengths", "version": "0.2.0",
             "sha256": "69a5583d8ef60955575b99cf4d706affc7d24c6d987a23d3ba628820e59ca500"}],
 "lensAdoptions": [], "sources": [], "assessments": [], "claims": [], "reviews": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- Поля `format`, `specVersion`, `id`, `version` и `subject` обязательны (`context.schema.json`). `holder`, `lang`, `created` и `policy` необязательны; оставьте их как в заготовке. Неиспользуемые массивы можно не писать.
- `"synthetic": true` помечает пример. В примере это поле ОБЯЗАНО стоять и в корне контекста, и на каждой содержательной записи, иначе проверка выдаёт ошибку CX-8. **Для реального человека** дайте `id` и `subject.id` вид `urn:uuid:<новый UUID>` и не ставьте `synthetic` ни в корне, ни на записях.
- `lenses[].sha256` — SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/via-strengths.lens.json`.
- Модуль `governance` нужен для разрешений Grant (шаги 1 и 7), `practices` — для Practice и Outcome (шаг 6).
- Каждого участника, на которого вы ссылаетесь, перечислите в `parties` (CX-3). Основному пути нужны коуч `p-01` и программа опросника `s-01`. Варианту «предложил агент» нужен `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`.
- Проверка проходит только тогда, когда в контексте есть Claim или Episode с рассказом (LV-0); до шага 4 она сообщает об ошибке LV-0.

### Шаг 1. Человек принимает линзу: LensAdoption

Коуч человека работает с сильными сторонами, и человек хочет пользоваться этой линзой. Запишите одну LensAdoption (схема `lens-adoption.schema.json`, массив `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-06-01"},
 "confidentiality": "practitioner-scope",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "via-strengths.ranked-list", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `releaseRef` здесь нет, потому что материалы встреч не хранятся.
- `practice.role` — `coach`, `teacher` или `therapist` (`adoption.inheritanceRoles` в описании линзы).
- `uses` выберите вместе с человеком: `speak-in-lens`, `store-results`, `interpret` (собственные прочтения человека), `offer-practices` (агент может предложить `via-strengths.strengths-in-episode` — единственный элемент инструментария с `agentMayOffer: true`), `recall`.

**Вариант «заметки коуча»: материалы встреч хранятся.** Сначала запишите Source с разрешением (шаг 2, вариант), затем принятие линзы с id этого разрешения в `practice.releaseRef`, затем Source с заметками. Всё это есть в [examples/via-strengths/variants/coach-notes/context.json](examples/via-strengths/variants/coach-notes/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-06-01", "releaseRef": "src-2"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "via-strengths.ranked-list",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Без `practice.releaseRef` правило LA-3 не проходит, как только заметки сохранены.

**Вариант «предложил агент» (`agent-suggested`).** Добавьте `a-01` в `parties` и запишите три записи в таком порядке. Все три есть в [examples/via-strengths/variants/with-agent/context.json](examples/via-strengths/variants/with-agent/context.json).

(1) Человек даёт агенту разрешение предлагать (массив `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-19T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:via-strengths"]}], "exclude": [{"ids": ["as-2"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-17T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-19T10:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest this lens and the episode exercise; it never sees my ranking."}
```

(2) Агент пишет принятие линзы по этому разрешению (массив `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "via-strengths.ranked-list", "origin": "observed", "assertedBy": "a-01",
 "underGrant": "g-0", "purpose": "self-reflection", "recordedAt": "2026-09-19T10:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

(3) Человек принимает её (массив `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-19T10:10:00Z"}
```

- `purpose` в принятии линзы ОБЯЗАН быть одной из целей (`purposes`) разрешения; иначе не проходит INF-1.
- Область разрешения ОБЯЗАНА называть линзу: `{"lenses": [...]}`. Подстановка вроде `{"all": true}` или селектор, который не называет линзу, не считаются, и INF-1 не проходит.
- Разрешению достаточно одного действия `suggest`. В его `exclude` перечислены id результатов человека (здесь `as-2`, шаг 3), чтобы агент, который предлагает, никогда их не видел; id можно указать ещё до того, как запись появилась.
- `origin` — `"observed"`: агент фиксирует, что человек согласился. `"declared"` не проходит ENV-2 (раздел 6).
- Пока человек не написал `admit`, принятие линзы остаётся `proposed`, и его не получает ни один получатель. `admit` пишет только сам человек (LA-1).

**Кто видит по умолчанию:** только сам человек. Коуч не видит запись без разрешения.

### Шаг 2. Сохраните оригинал: Source

Если у человека есть файл отчёта или заметки специалиста:

1. вычислите SHA-256 файла: `shasum -a 256 <файл>`;
2. скопируйте файл в каталог контекста как `vault/<первые два шестнадцатеричных знака хеша>/<хеш>.<расширение>`;
3. запишите Source (схема `source.schema.json`, массив `sources`), у которого `content.locator.vaultPath` — этот же путь, относительно каталога контекста и начиная с `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/82/82b74edd1ea2a5c1273c407ff5f91ffee9333e401b0e943c4ea4d7b510b0ce2a.pdf"}, "sha256": "82b74edd1ea2a5c1273c407ff5f91ffee9333e401b0e943c4ea4d7b510b0ce2a", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-18T19:00:00Z", "authorship": {"author": "s-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:02:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author` — программный участник для отчёта опросника.
- Не ставьте `title` и не пишите `summary`, который повторяет текст отчёта.
- Если файл на месте, проверка читает его и сравнивает хеш с `sha256`; при расхождении не проходит SR-2. `"vaultContentRead": false` в отчёте проверки значит, что содержимое не разбиралось; хеш при этом проверяется. Если файла нет, как в разобранных примерах, проверяется только запись.

**Вариант «заметки коуча»: сначала разрешение, потом заметки.** Разрешение — это письменное согласие специалиста на то, чтобы заметки хранились у человека. Сохраните его первым:

```json
{"id": "src-2", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/48/4806966871b1f06873d59a4ffbde1dfa7e4e3050f75278d715d3de4df1596e26.pdf"}, "sha256": "4806966871b1f06873d59a4ffbde1dfa7e4e3050f75278d715d3de4df1596e26", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:50:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

Затем заметки со ссылкой на то же разрешение:

```json
{"id": "src-3", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/27/2711ac21d0cf3dc92b0945151fdaf5ba811a16a8445142915e1a7420fbdfce02.pdf"}, "sha256": "2711ac21d0cf3dc92b0945151fdaf5ba811a16a8445142915e1a7420fbdfce02", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-2"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:01:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Id разрешения `src-2` стоит дважды: здесь в `custody.releaseRef` (SR-7) и в `practice.releaseRef` принятия линзы (шаг 1; LA-3).
- Для терапевта поставьте в `custody` значение `"confidentiality": "therapy"`.
- Claim, который опирается на заметки, ссылается на них так: `{"ref": "src-3", "kind": "practitioner"}` (Claim `c-2` в файле coach-notes).

**Кто видит по умолчанию:** только сам человек, на любом уровне выдачи (V-0). Получатель может получить самое большее уровень `index`.

### Шаг 3. Запишите результат: AssessmentRecord

Запишите одну AssessmentRecord для отчёта опросника (схема `assessment-record.schema.json`, массив `assessments`):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:via-is-r", "form": "adult"}, "mode": "vendor-report-import",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-18", "precision": "day"},
 "results": [
   {"type": "ranking", "constructs": ["via-strengths/curiosity", "via-strengths/kindness", "via-strengths/honesty", "via-strengths/perseverance", "via-strengths/humor"], "signatureTopN": 5}],
 "validityFlags": ["vendor-algorithm-undisclosed"], "source": "src-1",
 "trademarkNotice": "VIA is used only to name the VIA Institute's instruments; OHC is not authored or endorsed by the VIA Institute.",
 "origin": "imported",
 "importedFrom": {"system": "survey report (PDF), top five copied by the person", "importedAt": "2026-09-20T18:05:00Z"},
 "formulatedAt": "2026-09-18T19:00:00Z", "reviewAfter": "P3Y", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:05:00Z", "sensitivity": "special", "categories": ["mental-health"],
 "handling": ["no-infer"],
 "note": "Only the five signature strengths are stored; the rest of the order stays in the report.",
 "synthetic": true}
```

- `instrument.id` — `urn:ohc:instrument:via-is-r` или `urn:ohc:instrument:gacs`, смотря какой инструмент назван в отчёте (AR-8). `instrument.version` добавляйте, только если отчёт его указывает.
- `mode: "vendor-report-import"` требует `origin: "imported"` и `importedFrom` (AR-1). `formulatedAt` — когда отчёт был составлен; `recordedAt` — когда он вошёл в контекст (R-T5b).
- `importedFrom.importedAt` равно `recordedAt` (ENV-3). Не ставьте туда момент, когда файл копировали.
- **Id конструктов.** Для каждой сильной стороны возьмите её название так, как оно напечатано в отчёте, запишите строчными буквами, соедините слова дефисами и поставьте впереди `via-strengths/`. Знак, который не является буквой, опустите, а слова оставьте: на условных названиях `Alpha Beta` становится `via-strengths/alpha-beta`, и `Alpha & Beta` тоже становится `via-strengths/alpha-beta`. Больше об опущенном знаке ничего не записывается; пробел указан в разделе 6.
- **Порядок.** `constructs` перечисляет сильные стороны в порядке отчёта, от самой сильной. `signatureTopN` — сколько «ключевых» сильных сторон отмечено в отчёте. Храните весь порядок или только ключевые сильные стороны — как предпочитает человек; если храните часть, скажите об этом в `note` (раздел 6). В разобранном примере хранятся только первые пять, чтобы открытый файл не воспроизводил перечень классификации.
- Не храните баллы, процентили и нормативные группы: результат — ранжирование внутри одного человека (M-5).
- `trademarkNotice` копируется слово в слово из `notice` знака `VIA` в записи инструмента ([via-is-r](../../spec/instruments/via-is-r.instrument.json), [gacs](../../spec/instruments/gacs.instrument.json)).
- **Если в сохранённом порядке есть `via-strengths/spirituality`**, поставьте в этой записи `"categories": ["mental-health", "belief"]` и `"handling": ["no-infer", "subject-initiated-only"]` (`perConstruct` в описании линзы). Тогда это относится ко всей записи целиком (раздел 6).

**Вариант «самоопределение»: собственный выбор человека, без опросника.** Из файла with-agent:

```json
{"id": "as-2", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-19", "precision": "day"},
 "results": [{"type": "ranking", "constructs": ["via-strengths/curiosity", "via-strengths/kindness", "via-strengths/humor"]}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "reviewAfter": "P3Y", "assertedBy": "subject", "recordedAt": "2026-09-19T10:20:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer"], "synthetic": true}
```

- В отличие от `as-1`: `mode: "self-identified"`, `origin: "declared"`, `validityFlags: ["self-identified-only"]`; нет `instrument`, `trademarkNotice`, `importedFrom` и `formulatedAt`.
- `assessedBy: "subject"`, `sensitivity`, `categories`, `handling` и `reviewAfter` оставьте как в `as-1`, включая правило для Spirituality.
- `constructs` — сильные стороны, которые называет человек, в его порядке. `signatureTopN`, `note` и `source` не ставьте, если только человек не отмечает ключевые сильные стороны (`signatureTopN`) или не приносит записанный список (тогда это Source, на который ссылается `source`).

**Кто видит по умолчанию:** только сам человек. Уровень `special`, аудитория `named`.

### Шаг 4. С чем человек согласен: Claim

Спросите человека, какие сильные стороны он в себе узнаёт, и запишите только то, что он сказал, его словами, как Claim (схема `claim.schema.json`, массив `claims`). Сошлитесь на результат в `evidence`. Вид основания (`kind`) следует за записью, на которую вы ссылаетесь: `instrument` для результата опросника (`as-1`), `subject-statement` для самоопределения (`as-2`), `practitioner` для заметок специалиста (`src-3`).

```json
{"id": "c-1", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "Curiosity and kindness are what I lean on most, especially at the repair cafe.",
 "evidence": [{"ref": "as-1", "kind": "instrument"}], "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:10:00Z", "horizon": "foundation", "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- В варианте «самоопределение» тот же Claim ссылается так: `{"ref": "as-2", "kind": "subject-statement"}` (файл with-agent).
- Грань `disposition`, а не `capability`: линза не говорит о навыках и компетентности. `disposition` требует `origin: "declared"` от самого человека или `derived` из AssessmentRecord (CL-3). Предпочтите слова человека.
- Никогда не переносите в `text` описание сильной стороны из отчёта и никогда не пишите Claim о сильных сторонах с низким местом в ранжировании.
- Если человек не узнаёт себя в результате, он пишет Review (схема `review.schema.json`, массив `reviews`) `{"id": "rv-3", "target": "as-1", "action": "reject", "by": "subject", "recordedAt": "<сейчас>", "reasonCode": "not-true"}` или `"partially-endorse"` с `endorsedPart` своими словами. Запись остаётся; отвергнутая запись больше никому не выдаётся.

**Кто видит по умолчанию:** только сам человек.

### Шаг 5. Сильные стороны в эпизоде: Episode и Interpretation

Это элемент инструментария `via-strengths.strengths-in-episode`: человек выбирает недавний эпизод и отмечает, какие сильные стороны проявил и как. Эпизод — Episode (схема `episode.schema.json`, массив `episodes`); прочтение — Interpretation (схема `interpretation.schema.json`, массив `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-26", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-26T19:00:00Z", "addedAt": "2026-09-26T19:05:00Z", "accountKind": "in-the-moment", "happened": "At the repair cafe a neighbour brought a radio that would not turn on.", "didOrTried": "Asked what she had already tried, then showed her how to test the fuse; we fixed it together.", "experienced": "Light and awake."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-26T19:05:00Z", "contexts": ["community"], "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"},
 "text": "I used curiosity and kindness: I asked what she had tried before showing anything, and kept it light.",
 "alternatives": [{"text": "It was a quiet afternoon, so there was time to explain.", "kind": "situational"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-27T09:00:00Z",
 "heldDuring": {"from": "2026-09-27"}, "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Прочтение здесь пишет только сам человек (`assertedBy: "subject"`). Агент может предложить упражнение и задать вопросы из описания линзы («Какие сильные стороны вы проявили в этом эпизоде?», «Какой сильной стороной вы хотели бы пользоваться чаще?»), но прочтение агента через эту линзу не проходит правило I5, пока у принятия линзы `agentInterpretation` равно `off`.
- Называйте только сильные стороны в действии и словами человека. Они названы в `text`; структурного поля для них пока нет (раздел 6).
- Попросите хотя бы одно непсихологическое объяснение (`situational`, `physiological`, `informational` или `external`), чтобы удачный день не приписывался одному характеру.

**Кто видит по умолчанию:** только сам человек. Interpretation имеет уровень `special`, потому что называет линзу (I9).

### Шаг 6. Практики и их исходы: Practice и Outcome

Способ по-новому применить сильную сторону — здесь его предложил коуч — это Practice (схема `practice.schema.json`, массив `practices`); как он сработал — Outcome (схема `outcome.schema.json`, массив `outcomes`):

```json
{"id": "pr-1", "name": "One question before every repair",
 "description": "Use curiosity in a new place: ask about the person's own attempt before I touch the tool.",
 "practiceKind": "conversation",
 "source": {"route": "from-practitioner", "lens": "urn:ohc:lens:via-strengths", "by": "p-01"},
 "steps": ["Ask what they have already tried", "Ask what they want to learn", "Only then pick up the tool"],
 "limits": "Not when someone only wants the thing fixed quickly.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T18:00:00Z", "contexts": ["community"],
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "helped", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-08T20:00:00Z", "contexts": ["community"], "synthetic": true}
```

- Человек сам записывает предложение коуча (`assertedBy: "subject"`, `source.by` — коуч). Запись действует сразу.
- Регулярная практика «сильные стороны в эпизоде», которую человек заводит сам, записывается с `"source": {"route": "from-lens", "lens": "urn:ohc:lens:via-strengths", "templateId": "via-strengths.strengths-in-episode"}`.
- Outcome, записанный кем-то кроме самого человека, — это только «оценка агента» (O-1).

**Вариант «предложил агент»: агент предлагает упражнение с эпизодом.** Агент может предложить только `via-strengths.strengths-in-episode` (`agentMayOffer: true`). Для этого нужно разрешение с `suggest`, область которого называет линзу: разрешение `g-0` из шага 1 (если линза принята другим путём, запишите его сейчас, как показано там). Агент пишет Practice; человек её принимает. Обе записи есть в файле with-agent.

```json
{"id": "pr-2", "name": "Strengths in one episode a week",
 "description": "Once a week, pick an episode and note which strengths I used and how.",
 "practiceKind": "reflection",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:via-strengths", "templateId": "via-strengths.strengths-in-episode", "by": "a-01"},
 "steps": ["Pick one episode from the week", "Note which strengths I used", "Note one I would like to use more"],
 "limits": "Skip any week it feels like homework.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-09-27T09:00:00Z", "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-09-27T09:30:00Z"}
```

- `underGrant` — `g-0`; `purpose` ОБЯЗАН быть одной из целей (`purposes`) `g-0` (INF-1). Область ОБЯЗАНА называть линзу; подстановка не считается.
- `initialStatus` — `"candidate"`: человек ещё не пробовал. `origin` — `"observed"`, а `assertedBy` и `source.by` — агент (`"declared"` не проходит ENV-2).
- Пока человек не написал `admit`, Practice и её Outcome не выдаются ни одному получателю (PC-1; проверено инструментом проекций). После этого получатели видят Practice с пометкой `observed` (раздел 6).
- Агент никогда не предлагает `via-strengths.record-result` (PC-2).

**Кто видит по умолчанию:** только сам человек.

### Шаг 7. Кто что может видеть: Grant

Человек разрешает коучу читать записи о сильных сторонах для их работы (схема `grant.schema.json`, массив `grants`):

```json
{"id": "g-1", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "p-01",
 "purposes": ["coaching"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:via-strengths"]}, {"ids": ["c-1", "oc-1"]}]}, "actions": ["read"],
 "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-25T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"},
 "note": "For our coaching sessions: my strengths and how the practices went."}
```

- Селектор `{"lenses": [...]}` охватывает все записи, которые называют линзу: принятие, результат, прочтение и Practice. Claim и Outcome линзу не называют; добавьте их по `ids`. Эпизод не передаётся.
- `basis.legal` ОБЯЗАН быть `explicit-consent`; `expiresAt` — не позже чем через 180 дней после `recordedAt` (GR-1). В `purposes` никогда нет запрещённых целей (раздел 4).
- `mode: "summary"` убирает `note`, `evidence` и подробности импорта; само ранжирование выдаётся.
- Ограничения обращения едут вместе с каждой записью: получатель получает `no-infer` (и `subject-initiated-only`, где названа Spirituality) в `obligations.handling` и обязан их соблюдать (C-4, C-6).
- Запись, которая называет `via-strengths/spirituality`, всё равно попадает под селектор линзы. Чтобы не выдавать её, исключите её по id: `"exclude": [{"ids": ["as-1"]}]`. Тогда не выдаётся всё ранжирование целиком (раздел 6).

**Что получает этот получатель.** Запустите проекцию, которую получил бы получатель:

```sh
python3 -B tools/ohc_query.py <каталог вашего контекста> project --grant g-1 --purpose coaching --now latest
```

`--purpose` — одна из целей (`purposes`) разрешения; `--now latest` считает на самый поздний момент в контексте. **Для контекста реального человека** (без `synthetic`) добавьте `--holder-key-file <файл>` — файл с секретным ключом держателя (K_holder, §12.3, шаг 11); без него инструмент останавливается с сообщением «--holder-key-file is required: this context is not marked synthetic». Для разобранного примера он выдаёт `la-1`, `as-1`, `c-1` и `pr-1` в `statements`, `in-1` в `interpretations` и `oc-1` в `recall`; не выдаёт `ep-1` и `src-1`.

### Шаг 8. Проверка

```sh
python3 -B tools/check.py <каталог вашего контекста> --level L1 --json
```

Ожидайте `"valid": true` и `"levelMet": "L1"`, затем запустите команду проекции из шага 7 для каждого разрешения. Проверка не охватывает всё, чего требует этот рецепт. Проверьте вручную:

- каждый id конструкта следует шаблону `via-strengths/<n>` с опубликованным названием, записанным как в шаге 3;
- запись, которая называет `via-strengths/spirituality`, имеет категорию `belief` и ограничение `subject-initiated-only`;
- вид каждого основания (`kind`) соответствует записи, на которую оно ссылается (шаг 4);
- ни одна запись не содержит текстов вопросов, текста отчёта, описаний сильных сторон, баллов относительно других людей или перечня классификации;
- ни одна запись не написана агентом через эту линзу сверх того, что разрешают разрешение и принятие линзы человека.

## 4. Никогда

- **Запрещённые цели.** Никогда не используйте записи этой линзы для `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и других запрещённых целей (§8.10), ни по какому разрешению. Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14). Рекомендации самого издателя тоже исключают отбор и расстановку людей.
- **Никаких сравнений между людьми.** Ранжирование — внутри одного человека. Никогда не сравнивайте его с ранжированием другого человека или группы и никогда не сопоставляйте с другой линзой (`crossLensMapping: not-allowed`).
- **Агент не делает выводов, если человек не разрешил.** Сам по себе агент никогда не выводит сильные стороны человека из поведения или текста (`agentPosture`). Оценка (`mode: agent-inference`) или прочтение через линзу бывает только по разрешению человека (`suggest` и `infer`, называющие линзу; для прочтений — I5), как видимое только человеку предложение (AR-2).
- **Никаких слабостей.** Никогда не описывайте сильную сторону с низким местом в ранжировании как недостаток, дефицит или то, что надо исправить.
- **О Spirituality — только если человек сам заговорил.** Не говорите об этой сильной стороне, пока человек сам её не поднял: она может раскрывать религиозные или философские убеждения.
- **Никакого воспроизведения классификации.** Никогда не храните, не перечисляйте, не перегруппировывайте и не переименовывайте классификацию и никогда не цитируйте описания сильных сторон издателя.
- **Название VIA — только чтобы назвать инструменты издателя.** Используйте его в номинативном смысле, с уведомлением и никогда так, чтобы казалось, будто издатель написал или одобрил OHC или записи человека.

## 5. Разобранный пример

[examples/via-strengths/context.json](examples/via-strengths/context.json) — контекст в виде одного документа о Бенту; он вымышлен. В нём ровно записи основного пути из раздела 3: `la-1`, `src-1`, `as-1`, `c-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` и `g-1`, два участника и закреплённое описание линзы. Коуч Бенту работает с сильными сторонами; Бенту прошёл опросник, хранит пять своих ключевых сильных сторон, читает через них вечер в мастерской по ремонту вещей, пробует практику, которую предложил коуч, и разрешает коучу читать эти записи для их работы.

```sh
python3 -B tools/check.py docs/lenses/examples/via-strengths --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений. Вывод совпадает с [examples/via-strengths/expected-check.json](examples/via-strengths/expected-check.json).

Варианты из раздела 3 лежат ещё в двух контекстах о том же вымышленном Бенту. Каждый проходит так же (`"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений):

| Вариант | Файл | Записи |
|---|---|---|
| заметки коуча | [variants/coach-notes/context.json](examples/via-strengths/variants/coach-notes/context.json) | `src-2`, `la-1`, `src-3`, `c-2` |
| предложил агент, самоопределение, практика от агента | [variants/with-agent/context.json](examples/via-strengths/variants/with-agent/context.json) | `g-0`, `la-1`, `rv-1`, `as-2`, `c-1`, `pr-2`, `rv-2` |

```sh
python3 -B tools/check.py docs/lenses/examples/via-strengths/variants/coach-notes --level L1 --json
python3 -B tools/check.py docs/lenses/examples/via-strengths/variants/with-agent --level L1 --json
```

Файлы отчёта, разрешения и заметок в примеры не входят; когда файла нет, проверка проверяет только запись Source (шаг 2).

## 6. Что пока не помещается

Это пробелы OHC 0.1 для этой линзы. Они собраны для следующего прохода по стандарту.

1. **Частичное ранжирование выглядит как полное.** Результат `ranking` не может сказать, что в нём только первые N сильных сторон более длинного порядка; пример вынужден говорить об этом в `note`. Предложение: необязательное поле `complete` (логическое, по умолчанию `true`) у результатов `ranking`.
2. **Шаблон id неточен, а id конструктов не проверяются.** «Слова, соединённые дефисами» не говорит, что делать со знаками вроде `&`; этот рецепт их опускает, но проверка принимает и `via-strengths/alpha-beta`, и `via-strengths/alpha-&-beta` (условные названия), и любой другой id, в том числе с пробелами и заглавными буквами (проверено), так что ошибочный выбор никогда не замечается. Предложение: определить нормализацию в описании линзы (строчные буквы; знаки, которые не являются буквами или цифрами, опускаются; пробелы становятся дефисами; повторные дефисы сливаются) и добавить в проверку правило, которое сверяет id конструктов с `constructs` или `constructsByReference.idPattern`.
3. **Правило для Spirituality действует на всю запись.** `perConstruct` поднимает одну сильную сторону до `belief`, но категории и ограничения стоят на AssessmentRecord, поэтому всё ранжирование становится `belief` и `subject-initiated-only`, а скрыть от получателя одну эту сильную сторону можно, только скрыв всё ранжирование. Проверка не проверяет `perConstruct` (проверено). Предложение: категории для отдельных элементов результата, шаг выдачи, который убирает конструкты, чьи категории не названы селектором разрешения, и правило проверки для `perConstruct`.
4. **Прочтение не может назвать сильные стороны, о которых оно.** У Interpretation и Practice через линзу есть только свободный текст, поэтому «какие сильные стороны проявились в моих эпизодах» нельзя посчитать без разбора текста. Предложение: необязательный список `constructs` (id конструктов указанной линзы) у Interpretation и Practice.
5. **Прочтение специалиста через линзу нельзя сохранить.** *Исправлено в 0.1.0-draft.2:* LA-7 снято, а I5 применяет `agentInterpretation` только к авторам-агентам и программам; прочтению коуча нужно, чтобы коуч был в `interpretationAuthors` действующего принятия.
6. **Доступ специалиста описан непоследовательно.** CONTEXT-08 говорит, что доступу «нужно собственное разрешение, которого 0.1 для специалистов не предусматривает», но Grant участнику-человеку с ролью `practitioner` проходит проверку и остаётся единственным способом поделиться с коучем (как в примере). Предложение: указать в CONTEXT-08, что участник-специалист может быть получателем с целью `coaching` или `therapy-support`, а само принятие линзы доступа никогда не даёт.
7. **`therapy-confidential` не доходит до результатов.** LA-4 распространяет `special` и `person-only` только на записи, которые ссылаются на принятие; собственные AssessmentRecord, Claim, Interpretation и Practice человека в этой линзе на него не ссылаются (у AssessmentRecord для этого даже нет поля), поэтому селектор линзы их по-прежнему выдаёт (проверено инструментом проекций). Предложение: применять LA-4 ко всем записям, у которых `lens` или `source.lens` — принятая линза, пока принятие имеет `therapy-confidential`.
8. **Не указано, какой `origin` у записей, которые агент пишет за человека.** У Practice с `source.route: from-agent` и у записи принятия на пути `agent-suggested`, написанной агентом, нет поля `text`, поэтому `origin: declared` не проходит ENV-2; `observed` проходит, но нигде не описан (проверено). Предложение: указать `origin: observed` для таких записей в §10.5, §17.1 и CONTEXT-08.
9. **Авторское право на сохранённый отчёт никак не отмечено.** Отчёт издателя может лежать в хранилище человека, но в Source нигде не записано, что его текст принадлежит издателю; от получателей его защищает только `maxRelease`, а человек может его ослабить. Предложение: необязательная пометка `rights` у Source (`holder`, `use: "personal-copy"`) и предупреждение держателя перед любой выдачей выше `index`.
10. **LensAdoption ничего не ограничивает.** Контекст с результатами линзы, прочтениями через неё и практиками из неё, но без LensAdoption, проходит L1; результаты проходят, когда в `uses` принятия нет `store-results` и когда они записаны раньше принятия; пока принятие на пути `agent-suggested` или `imported` ещё `proposed`, селектор по линзе уже выдаёт результаты, прочтения и практики человека в этой линзе (проверено). `uses` не имеет нормативной силы; §10.5 не даёт `uses` никакого правила. Предложение: правило LA-8 — запись с `lens` или `source.lens` от автора, который не является самим человеком, требует принятия этой линзы, действующего на её `recordedAt`, с подходящим значением в `uses` (`store-results`, `interpret`, `offer-practices`); предупреждение для собственных записей человека в линзе без действующего принятия; проекция, которая не выдаёт записи линзы, пока принятие `proposed` или `paused`.
11. **Практика, предложенная агентом, доходит до получателей с пометкой «observed».** После `admit` человека Practice с `source.route: from-agent` и принятое `agent-suggested` принятие линзы выдаются с вычисленными `label: observed` и `endorsement: not-asked` (проверено инструментом проекций). Получатель видит предложение агента как наблюдение о человеке и не видит, что человек его принял. Предложение: вычислять для таких записей `label: suggested`, а `endorsement: admitted` — когда есть Review `admit` от человека; или добавить origin `suggested` вместо `observed`.
12. **Вид основания (`kind`) не связан с записью, на которую оно ссылается.** Claim может сослаться на ранжирование самоопределения с `kind: instrument`; проверка принимает любой вид для любой цели, а прежняя версия этого рецепта давала `instrument` во всех случаях. Получатель тогда читает собственный выбор человека как данные опросника. Предложение: когда `ref` основания — AssessmentRecord, `kind` соответствует её `mode` (`self-identified` → `subject-statement`; режимы специалиста → `practitioner`; режимы инструментов → `instrument`), или проекция выводит вид из режима.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
