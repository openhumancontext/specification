# Рецепт линзы: астрология

**Рецепт · линза `urn:ohc:lens:astrology` 0.2.0 · OHC 0.1.0-draft.2 · информативно · 12 октября 2026**

Этот рецепт превращает астрологию человека (его данные о рождении, рассчитанную карту и то, как он пользуется её языком) в записи OHC, которые сохраняют рамку как выбранный человеком язык и не дают ей стать фактом о нём, предсказанием или входом для чьих-либо выводов.

Описание линзы — [spec/lenses/astrology.lens.json](../../spec/lenses/astrology.lens.json); устройство записей — в [SPECIFICATION.md §10.5–§10.6](../../spec/SPECIFICATION.md#105-lensadoption), схемы — в [spec/schema/](../../spec/schema/). Общая процедура принятия линзы — [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию. Результаты этой рамки и всё, что из них прочитано, остаются `frame-relative` и никогда не выдаются за эмпирический факт или предсказание (AR-4, C-7).

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:astrology-basic`](../../spec/playbooks/astrology-basic.playbook.json) («Астрология как рамка самоописания: базовые способы работы», редакция OHC), для таких ситуаций: разбор того, что произошло; выбор между вариантами; подготовка к трудному разговору. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Что это | Куда это идёт |
|---|---|---|
| Самоописание в разговоре | «Моё Солнце в Рыбах», «моя Луна в Тельце» | LensAdoption (шаг 1) и собственные Claim человека (шаг 5). Если карты нет — результат, названный самим человеком (шаг 4, вариант). |
| Данные о рождении | Дата, время и место рождения | Один Claim с `facet: "fact"` и категорией `birth-data` (шаг 2). |
| Карта, которую человек рассчитал в программе | Выгрузка или распечатка положений и аспектов | Source в хранилище (шаг 3) и одна AssessmentRecord с результатом `frame-attributes` (шаг 4). |
| Выгрузка карты, загруженная импортёром | То же, но прочитанное программой | Путь `imported` (§2): принятие линзы и результат остаются предложениями, пока человек не подтвердит их записями Review. |
| Заметки с консультации у астролога | Прочтение карты астрологом | Source, автор — Party астролога (`role: "practitioner"`, шаг 3). Своё прочтение человек пишет своими словами (шаг 6). С 0.1.0-draft.2 прочтение астролога можно записать и как прочтение через линзу — при принятии `inherited-from-practice`, где астролог указан в `interpretationAuthors` (I5); в примере этого нет. |
| Прочтение агента | — | **Только по разрешению человека.** Агент предлагает рамку или читает через неё, только если это позволяет договорённость человека (`suggest`, `infer`, называющие линзу) и действующее принятие линзы не в `off` (I5). Всё прочитанное остаётся `frame-relative` и говорится языком рамки, а не как факт или предсказание (AR-4, C-7). |

## 2. Прежде чем начать


**Пути принятия.**

| Путь | Можно | Что он меняет |
|---|---|---|
| `self-chosen` | да | Человек сам пишет принятие с `assertedBy: "subject"`; оно действует сразу. Разобранный пример идёт этим путём. |
| `imported` | да | Импортёр создаёт принятие и результат по выгрузке, оба с одинаковым `importedFrom.run`. Оба остаются `proposed`, пока человек не подтвердит их записью Review (LA-5). Полностью этот путь показан в рецепте «Дизайн человека». |
| `agent-suggested` | только по разрешению человека | Указан, обычно когда человек сам заговорил о рамке; пути описывают обычную практику и ничего не ограничивают. Агент предлагает рамку только по разрешению с `suggest`, называющему линзу, и принятие остаётся предложением, пока человек его не допустит (LA-1). |
| `inherited-from-practice` | да | Указан (роль `other`). Консультацию у астролога можно унаследовать с блоком `practice`; прочтениям специалиста нужно, чтобы он был в `interpretationAuthors` (I5). Кода хранения для консультации нет (§6). |

**Согласие.** Для записи разрешение не нужно: человек пишет в свой контекст, а без Grant никому ничего не раскрывается (L0). Чтобы поделиться, человек пишет Grant (шаг 8). Записи, ссылающиеся на эту линзу, имеют уровень `special`, поэтому Grant требует `basis.legal: "explicit-consent"` и срок не дольше 180 дней (R-G3, R-G10). `la-01`, `as-01` и `in-01` — записи `frame-relative`: до них дотягивается только селектор, называющий линзу; одни id не дотягиваются никогда (§12.3, шаг 8). Селектор `ids` работает только для Episode и простых Claim.

**Что задано по умолчанию для этой линзы.**

- Записи, ссылающиеся на линзу (LensAdoption, AssessmentRecord, Interpretation): `sensitivity: "special"`, `categories: ["birth-data"]`.
- Claim с данными о рождении: категория `birth-data` (уровень не ниже `sensitive`). Рекомендуется `handling: ["person-only"]`.
- AssessmentRecord: `epistemic: "frame-relative"`. Рекомендуется `handling: ["no-infer", "no-quote-back"]`, если человек хочет держать карту в стороне от любых выводов.
- Каждый Claim, выведенный из карты: `epistemic: "frame-relative"`, вручную (шаг 5а). Проверка не замечает, если его нет.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет; `interpretationAuthors` остаётся `["subject"]`. Человек может изменить и то и другое (I5).
- У линзы `reviewAfter` равно `on-change`. Натальная карта не меняется, поэтому `reviewAfter` в AssessmentRecord не указывайте.

**Что не хранится никогда.**

- Текст отчётов: толкования из программы, с сайта, из книги или от астролога. Он остаётся в хранилище (шаг 3) или не хранится вовсе. В записях — только положения, аспекты и слова самого человека.
- Градусы, минуты, углы и куспиды, если человек сам о них не попросил. Вместе с местом они позволяют восстановить дату и время рождения. Храните знаки (а номера домов — только если человек сам этого хочет).
- Карта или данные о рождении другого человека: совместимость, синастрия, карта партнёра или ребёнка. Ни одна запись не описывает третье лицо (TP-1).
- Прогнозы (транзиты или прогрессии, прочитанные как предсказание) в виде Claim или результатов.
- Ярлыки, перенесённые между линзами в любую сторону: тип или черта «по вашей карте», знак «по вашему тесту».
- Баллы, ранжирование или оценки человека. Атрибуты рамки — никогда не черты.

## 3. Шаги

Все записи ниже пишет сам человек или агент под его диктовку от имени человека (`assertedBy: "subject"`). Каждый фрагмент — запись из [разобранного примера](examples/astrology/context.json), и он проходит проверку по схеме, если он не помечен как вариант (варианты проверены отдельно и тоже проходят L1).

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
  "created": "2026-09-03T18:30:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "lensAdoptions": [], "claims": [], "sources": [], "assessments": [], "episodes": [],
  "interpretations": [], "grants": []
}
```

- Схема требует `format`, `specVersion`, `id`, `version` и `subject.id`. `holder`, `lang` и `policy` выше — это выписанные значения по умолчанию. Меняйте `version` с каждым набором изменений.
- **Только для вымышленного человека:** добавьте `"synthetic": true` в корень **и** в каждую содержательную запись. Контекст о реальном человеке этого флага не несёт никогда. Проверка требует оба флага только для папки внутри каталога `examples/` или для `id`, начинающегося с `urn:ohc:example:` (разобранный пример использует `urn:ohc:example:imre:astrology`). `tools/ohc_query.py` (шаг 8) строит проекцию без ключа держателя только при флаге в корне.
- Для пути `imported` добавьте `"reviews": []`, а если делаете шаг 7 — `"practices": []`.

Затем заполните `conformance`, `parties` и `lenses`. Объявите модули, перечислите каждую Party, на которую будете ссылаться (программу для карт и агентов, с которыми человек потом поделится; подписи — общие роли, никогда не имена), и закрепите описание (`sha256` — это SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/astrology.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "s-01", "partyKind": "software", "label": "Chart software"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:astrology", "version": "0.2.0", "sha256": "5ebefc64c34aa0c6a977e271b4c80d7bb8ade6a5c1d1e53a90cdb89e43e09e74"}
]
```

### Шаг 1. Записать отношение человека к линзе: LensAdoption

Человек говорит, что описывает свой опыт языком астрологии. Напишите одну LensAdoption. Значения `uses` выберите вместе с человеком: `speak-in-lens` (после принятия агент может говорить словами рамки), `store-results` (карту можно хранить), `interpret` (человек может читать через неё эпизоды).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "astrology.chart",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:45:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Кто видит по умолчанию: только сам человек. Уровень `special`, метка ◇ рамка. Запись — `frame-relative`: Grant дотягивается до неё только через селектор, называющий линзу, при явном согласии; селектор с одним её id не дотягивается никогда.

### Шаг 2. Записать данные о рождении: Claim

Карта рассчитывается по ним, поэтому они записываются один раз, словами человека и с той точностью, которую он выбрал (достаточно города; никогда не адрес).

```json
{"id": "c-01", "facet": "fact", "predicate": "birth-data",
 "text": "Born 14 March 1991 at about 06:40 local time in Porto.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:50:00Z", "horizon": "foundation",
 "sensitivity": "sensitive", "categories": ["birth-data"], "handling": ["person-only"], "synthetic": true}
```

Кто видит: только человек, всегда. Запись с `person-only` не отдаётся никакому получателю, что бы ни говорил Grant. Никогда не вписывайте данные о рождении в id, заголовок или заметку.

### Шаг 3. Сохранить исходную карту: Source

Выгрузка карты (или скан распечатки) кладётся в хранилище. Вычислите значения сами, не копируйте их из примера:

1. `sha256` — вывод `shasum -a 256 <файл>` (или `sha256sum <файл>`);
2. `size` — число байтов, `wc -c < <файл>`;
3. переместите файл в `<папка>/vault/<первые два шестнадцатеричных символа sha256>/<sha256>.<расширение>` и запишите этот путь, относительно папки, в `vaultPath`.

Проверка L1 не читает хранилище (`"vaultContentRead": false`): неверный хеш или размер всё равно проходит, поэтому вычисляйте их. Запись Source хранит только сведения о файле.

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/03/03b169fc93949c19bd13ceb6b0c931d850b13a17cc4f91b57a6cf66d74074162.json"},
             "sha256": "03b169fc93949c19bd13ceb6b0c931d850b13a17cc4f91b57a6cf66d74074162",
             "mediaType": "application/json", "size": 172},
 "capturedAt": "2026-09-03T18:55:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Chart export saved from my chart software.", "authoredBy": "subject",
             "recordedAt": "2026-09-03T19:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:00:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

- `custody` не указан: файл принадлежит человеку.
- `summary.text` — собственная строка человека о файле, никогда не скопированный текст отчёта.
- **Письменные заметки астролога** (вариант): добавьте астролога в `parties` как `{"id": "p-01", "partyKind": "person", "label": "Consulting astrologer", "role": "practitioner"}` (роль — `practitioner`, подпись — общая роль, никогда не имя). Храните заметки как Source с `sourceKind: "practitioner-notes"` (по умолчанию `special`), `authorship.author: "p-01"`, `inbound: true` и `maxRelease: "index"`, без `summary`.

Кто видит: только человек (ему всегда доступны все уровни). `maxRelease: "index"` значит, что ни один получатель не получит больше, чем вид источника, тип файла и примерную дату.

### Шаг 4. Записать карту: AssessmentRecord

Одна AssessmentRecord с одним результатом `frame-attributes`. Правила: `mode: "computed-from-birth-data"` требует `origin: "derived"` (AR-1), а он требует `generatedBy.method` и `derivedFrom`. `computedFrom` называет Claim с данными о рождении; `engine` — программу и её версию. Ключи `attributes` — id конструктов линзы (`astrology/placement`, `astrology/aspect`); значения — только знаки, без градусов. `lensVariant` — `western-tropical` или `vedic-sidereal`. Поля `instrument` нет (линза не перечисляет инструментов), `trademarkNotice` тоже нет (у линзы нет товарных знаков). Проверка не проверяет ни ключи и значения атрибутов, ни `computedFrom` (§6), поэтому следите за этими правилами сами.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "lensVariant": "western-tropical",
 "mode": "computed-from-birth-data", "administeredAt": {"start": "2026-09-03", "precision": "day"},
 "results": [
   {"type": "frame-attributes",
    "attributes": {
      "astrology/placement": [
        {"point": "sun", "sign": "pisces"},
        {"point": "moon", "sign": "taurus"},
        {"point": "ascendant", "sign": "pisces"}],
      "astrology/aspect": [
        {"points": ["sun", "saturn"], "aspect": "sextile"}]},
    "computedFrom": "c-01",
    "engine": {"name": "example-chart-engine", "version": "3.2"}}],
 "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-engine", "version": "3.2", "method": "western tropical zodiac; signs only, no degrees and no houses"},
 "derivedFrom": ["c-01"], "assertedBy": "subject", "recordedAt": "2026-09-03T19:10:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**Вариант без карты** (в разобранном примере его нет). Если человек знает только одно положение («моё Солнце в Рыбах»), запишите запись целиком так:

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "lensVariant": "western-tropical",
 "mode": "self-identified", "administeredAt": {"start": "2026-09-03", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "astrology/placement", "label": "Sun in Pisces", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:10:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- `lensVariant` оставляйте, только если человек его знает.
- Нет `generatedBy`, `derivedFrom`, `computedFrom` и `engine`: ничего не рассчитывалось. Проверка принимает `generatedBy` и `derivedFrom` в заявленной записи (§6), но они утверждали бы расчёт, которого не было.
- Нет `source`, если только Source не существует (например, фото записки, написанной человеком от руки).
- Шаг 3 пропустите. Шаг 2 нужен, только если человек хочет записать данные о рождении.

Кто видит: только человек. Уровень `special`, метка ◇ рамка. Запись отдаётся только по Grant, селектор которого называет линзу (§12.3, шаг 8 требует этого для любой записи `frame-relative`).

### Шаг 5. Оставить только то, что человек принимает: Claim

Покажите человеку результат. Пишите Claim только о том, что человек узнаёт в себе, и его словами. Бывает два вида.

**5а. Самоописание языком рамки.** `facet: "identity"`, `predicate: "self-description"`, `epistemic: "frame-relative"`, `derivedFrom` — карта. Никогда не `facet: "disposition"`: эта линза не устанавливает никаких черт (CL-3 и `doesNotEstablish` в описании).

**Вы ОБЯЗАНЫ поставить `epistemic: "frame-relative"` в каждый Claim, выведенный из `as-01`.** Проверка не замечает, если его нет. Без него Claim считается `as-reported`, получает метку ✓ заявлено, и Grant, называющий его id, отдаёт его как простой заявленный факт. Проверьте это до шага 8.

```json
{"id": "c-02", "facet": "identity", "predicate": "self-description",
 "text": "In my chart's language I am a Pisces Sun with a Taurus Moon: I do my best thinking alone, before the day starts.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T20:00:00Z", "horizon": "foundation",
 "derivedFrom": ["as-01"], "epistemic": "frame-relative", "handling": ["no-quote-back", "no-infer"],
 "synthetic": true}
```

Кто видит: только человек. Её уровень — `special`, он передаётся от карты. В OHC 0.1 эту запись не отдаёт ни один Grant, даже называющий её id, потому что Claim не может назвать линзу (§6).

**5б. То же понимание простыми словами, если человек хочет, чтобы агенты с ним считались.** Спросите: «Есть ли здесь что-то, что другим стоит учитывать, — скажите это простыми словами?» Запишите обычный Claim без слов рамки и **без** `derivedFrom`: он держится на слове человека, а не на карте.

```json
{"id": "c-03", "facet": "preference", "predicate": "timing",
 "text": "Keep my mornings for focused work; put meetings after 11:00.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T20:05:00Z", "horizon": "foundation",
 "contexts": ["work"], "synthetic": true}
```

Кто видит: только человек, пока Grant её не назовёт. Уровень `personal`, метка ✓ заявлено. До неё дотягивается любой Grant, селектор которого совпадает с `facet: "preference"`.

### Шаг 6. Прочитать эпизод через линзу словами человека: Episode и Interpretation

Человек рассказывает, что произошло (Episode). Если хочет, он читает это через свою карту (Interpretation с `lens` и `stance: "lens-reading"`). Это прочтение пишет только сам человек. Добавьте хотя бы одну альтернативу непсихологического вида, чтобы рамка никогда не оставалась единственным объяснением.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-08", "end": "2026-09-19", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-20T21:00:00Z", "addedAt": "2026-09-20T21:00:00Z",
    "accountKind": "first-narrative",
    "happened": "For two weeks the translation stalled; I rewrote the opening of the same chapter five times.",
    "didOrTried": "Moved my desk to the window and started working at night.",
    "understandingThen": "I thought the text was simply hard."}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T21:00:00Z",
 "sensitivity": "sensitive", "contexts": ["work"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"},
 "text": "Read through my chart, those weeks were my Pisces Sun asking for more solitude than the shared office gave me.",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The publisher changed the style guide in the middle of the job.", "kind": "external"},
   {"text": "I was sleeping badly after the move.", "kind": "physiological"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-27T09:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-quote-back"], "contexts": ["work"], "synthetic": true}
```

Кто видит: только человек. Episode имеет уровень `sensitive` (Grant должен назвать её id, вид записи или facet); прочтение — `special` и `frame-relative` (Grant должен назвать линзу).

### Шаг 7. Практики из набора инструментов

Агенту выполнять нечего. В наборе одна позиция, `astrology.chart` (расчёт карты): это шаг 4; агент может её предложить (`agentMayOffer: true`), когда договорённость человека позволяет ему предлагать рамку.

Если у человека есть своя практика, запишите её как Practice с `source.route: "self-discovered"` и без `templateId` (вариант, в разобранном примере его нет). Сначала добавьте `"practices"` в `conformance.modules` и `"practices": []` в файл; без модуля проверка падает на CX-5. `practiceKind` — одно из `breathing`, `movement`, `reflection`, `writing`, `conversation`, `rest`, `planning`, `environment`, `social-contact`, `creative`, `contemplative`, `other`.

```json
{"id": "pr-01", "name": "Evening notes", "description": "A few lines before sleep about what the day asked of me.",
 "practiceKind": "writing", "source": {"route": "self-discovered"}, "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T21:00:00Z", "synthetic": true}
```

### Шаг 8. Решить, кто что видит: Grant

Два типичных разрешения. Спутник для размышлений может читать записи рамки и эпизод, чтобы говорить с человеком на выбранном им языке. У него нет `suggest` и `infer`: через эту линзу он ничего не пишет. Рабочий помощник видит только простые предпочтения.

```json
{"id": "g-01", "recordedAt": "2026-09-06T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:astrology"]}, {"ids": ["ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T10:00:00Z", "channel": "holder-ui"},
 "note": "Chart language for my own reflection only; no advice, no predictions."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-06T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["scheduling"],
 "scope": {"include": [{"facets": ["preference"], "contexts": ["work"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T10:05:00Z", "channel": "holder-ui"}}
```

Что получает каждый получатель по §12.3 (посчитано справочными инструментами на разобранном примере):

| Получатель | Отдаётся | Не отдаётся никогда |
|---|---|---|
| `a-01` Спутник для размышлений | `la-01`, `as-01`, `in-01`, `ep-01` | `c-01` (`person-only`), `c-02` (Claim `frame-relative`, §6), `c-03` (вне охвата), `src-01` (`maxSourceTier: none`) |
| `a-02` Рабочий помощник | `c-03` | всё, что ссылается на линзу |

Чтобы посчитать эту таблицу для своего контекста, запустите для каждого Grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose scheduling --now 2026-10-10T12:00:00Z
```

Отданные записи появляются в `statements`, `experience`, `interpretations` и `recall`; Party, на которые они указывают, — в `parties`. Контексту без `"synthetic": true` в корне нужен `--holder-key-file`.

`expiresAt` — не позже чем через 180 дней после `recordedAt` для g-01 (оно достаёт записи уровня `special`) и не позже чем через год для g-02. Grant только с `{"ids": ["la-01", "as-01", "in-01"]}` не отдаёт ни одной из них, даже при явном согласии: называйте линзу. Никогда не добавляйте для этой линзы `infer`, `write` или селектор «всё».

### Шаг 9. Проверить

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Ожидается `"valid": true` и `"levelMet": "L1"`. Папку внутри каталога `examples/` проверка сравнивает с её `expected-check.json` (X-3); ваш собственный контекст — нет. Успешная проверка не покрывает того, что, как сказано в §2 и шаге 5а, она не ловит: `epistemic` у выведенных Claim, ключи и точность атрибутов, `computedFrom` и хеши хранилища.

## 4. Никогда

- Никогда не заводите речь о рамке и не рассчитывайте карту, если договорённость человека этого не позволяет (`suggest`, называющее линзу), а тогда — только как один из вариантов.
- Никогда не читайте через линзу от имени агента сверх разрешения и принятия линзы человека (I5). Оценка видна только человеку (AR-2), а прочтение или оценка в символической рамке — `frame-relative` (AR-4).
- Никогда не выдавайте атрибут карты или прочитанное из него за эмпирическую черту или предсказание (C-7); никогда не сопоставляйте атрибуты карты с чертой, типом или баллом (LN-3, сопоставление `no-relation`).
- Никогда не используйте ничего из этой линзы для запрещённых целей (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и остальных из §8.10), ни по какому разрешению. Сюда входят подбор команды, «соответствие» при найме и совместимость с коллегами или партнёрами. Атрибут карты служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и называется как язык рамки, а не как факт (R-G14, C-7).
- Говорите языком рамки словами самого человека. Никогда не приводите карту как довод («по вашей карте вы…»): `no-quote-back`.
- Никогда не предсказывайте и никогда не подавайте атрибут рамки как факт о человеке.
- Никогда не рассчитывайте, не храните и не обсуждайте карту другого человека (TP-1).
- Никогда не отдавайте Claim с данными о рождении; никогда не вписывайте данные о рождении в id, заголовки или заметки (R-I1).
- Товарных знаков в описании линзы нет. Программу для карт называйте только как источник происхождения (`engine`, `generatedBy`), никогда как ярлык результата.

## 5. Разобранный пример

[examples/astrology/context.json](examples/astrology/context.json): Имре, вымышленный переводчик. Пример содержит ровно записи раздела 3 (без вариантов): `la-01`, `c-01`, `src-01`, `as-01`, `c-02`, `c-03`, `ep-01`, `in-01`, `g-01`, `g-02`, а также заглушку в хранилище для `src-01`. Корень контекста и каждая содержательная запись несут `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/astrology --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений ([expected-check.json](examples/astrology/expected-check.json)).

## 6. Что пока не помещается

1. **Claim с `frame-relative` нельзя никому показать.** У Claim нет поля `lens`, а §12.3, шаг 8 отдаёт запись `frame-relative` только по селектору, называющему её линзу. Claim из шага 5а не отдаётся, даже если Grant называет его id. Предложение: разрешить `lens` в Claim с эпистемическим статусом `frame-relative` или позволить шагу 8 принимать селектор `ids`.
2. **Нет связи «это пришло мне в голову, когда я смотрел на карту», которая не делала бы карту свидетельством.** `derivedFrom` и `evidence` делают рамку основанием и переносят уровень `special` на простой Claim (шаг 5б). Предложение: код связи Relation вроде `prompted-by`: не свидетельство, без переноса уровня, никогда не путь для выводов.
3. **Прочтению астролога негде жить.** *Исправлено в 0.1.0-draft.2,* кроме хранения: пути ничего не ограничивают (LN-3 теперь запрещает только сопоставление с другими линзами), а I5 применяет `agentInterpretation` только к авторам-агентам и программам, поэтому астролог из `interpretationAuthors` унаследованного принятия может быть автором прочтения. Кода конфиденциальности хранения для консультации по-прежнему нет. Предложение: добавить код хранения вроде `consultation`.
4. **`frame-attributes.attributes` — объект без структуры.** Ничто не связывает его ключи с id конструктов и не ограничивает точность (градусы выдают время рождения): значения в градусах и ключи не из конструктов проходят L1. Предложение: `attributes: [{"construct", "value"}]` с конструктами из описания линзы и поле описания со списком атрибутов, которые никогда не хранятся.
5. **Нет формы для атрибута рамки, названного самим человеком.** `frame-attributes` требует `computedFrom` и `engine`; человек, который знает только одно положение, вынужден брать `type-assignment`. Предложение: сделать оба поля необязательными при `mode: "self-identified"`.
6. **`computedFrom` не проверяется.** Его нет в каталоге допустимых ссылок, и ничто не проверяет, что он указывает на Claim с данными о рождении; висячий `computedFrom` проходит. Предложение: добавить его в каталог и правило: он указывает на Claim с `facet: "fact"` и `predicate: "birth-data"`.
7. **Умолчания линзы не задают ограничения обращения.** `no-infer` и `no-quote-back` подходят ко всем записям этой линзы, но их приходится добавлять вручную. Предложение: поле `defaults.handling` в описании линзы.
8. **`on-change` нельзя записать в запись.** `reviewAfter` в AssessmentRecord принимает только длительность, а §7.2 не говорит, как `on-change` влияет на свежесть. Предложение: разрешить `on-change` и определить его (актуально, пока запись не заменена и не отмечена неактуальной).
9. **Путь принятия не сверяется с описанием линзы.** *Закрыто в 0.1.0-draft.2 как задумано:* `adoption.routes` описывает обычную практику и никогда не ограничивает LensAdoption.
10. **Статус `frame-relative` не передаётся по `derivedFrom`.** Claim, выведенный из AssessmentRecord с `frame-relative` и записанный без `epistemic`, считается `as-reported` и получает метку ✓ заявлено; Grant, называющий его id (проверено на помощнике по расписанию при явном согласии), его отдаёт. Язык карты уходит наружу как простой заявленный факт, и ни правило, ни предупреждение не срабатывают. Предложение: передавать `frame-relative` по `derivedFrom` и `grounds`, как передаётся уровень, или правило (ошибка на L1): запись, у которой в `derivedFrom` или `grounds` есть запись `frame-relative`, ОБЯЗАНА быть `frame-relative`.
11. **Заявленная запись может нести `generatedBy` и `derivedFrom`.** AssessmentRecord, названная самим человеком (`origin: "declared"`), с `generatedBy` и `derivedFrom: ["c-01"]` проходит проверку. Её происхождение тогда утверждает расчёт программой, а сама запись говорит, что это сказал человек. Предложение: правило конверта — `generatedBy` допустим только при `origin` `derived` или `inferred`; связь заявленной записи с тем, что её навело, идёт через `evidence` или предложенную связь Relation `prompted-by` (пункт 2), а не через `derivedFrom`.
12. **Флаг `synthetic` в корне не связан с флагами записей.** Вне режима примеров (папка не внутри `examples/`, id не начинается с `urn:ohc:example:`) все содержательные записи могут быть синтетическими, а корень — нет; проверка это принимает, а `ohc_query.py` тогда требует ключ держателя. Предложение: предупреждение на L1, когда все записи синтетические, а корень нет, и наоборот; или выводить флаг корня из записей.
13. **На L1 хранилище не сверяется с Source.** Неверные `sha256` или `size` проходят (`"vaultContentRead": false`). Предложение: проверка по флагу (или на L1, когда хранилище локальное), которая хеширует файлы хранилища и сверяет `sha256` и `size`: ошибка при расхождении, предупреждение, когда файла нет.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
