# Рецепт линзы: Дизайн человека

**Рецепт · линза `urn:ohc:lens:human-design` 0.2.0 · OHC 0.1.0-draft.2 · информативно · 12 октября 2026**

Этот рецепт переносит карту Дизайна человека — обычно выгруженную из приложения — в OHC в виде записей, которые относятся только к рамке, которые человек сам подтверждает и читает своими словами и по которым никто не может делать о нём выводы или решать за него.

Описание линзы — [spec/lenses/human-design.lens.json](../../spec/lenses/human-design.lens.json); устройство записей — в [SPECIFICATION.md §10.5–§10.6](../../spec/SPECIFICATION.md#105-lensadoption), схемы — в [spec/schema/](../../spec/schema/). Общая процедура принятия линзы — [CONTEXT-08](../agents/procedures/CONTEXT-08.md). Используйте только общее название «Дизайн человека» (Human Design) (§4).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию. Результаты этой рамки и всё, что из них прочитано, остаются `frame-relative` и никогда не выдаются за эмпирический факт или предсказание (AR-4, C-7).

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:human-design-basic`](../../spec/playbooks/human-design-basic.playbook.json) («Дизайн человека как рамка самоописания: базовые способы работы», редакция OHC), для таких ситуаций: разбор того, что произошло; выбор между вариантами; подготовка к трудному разговору. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Что это | Куда это идёт |
|---|---|---|
| Карта, выгруженная из приложения | Файл с типом, авторитетом, профилем и центрами, рассчитанными по данным о рождении | Путь `imported`: запуск импорта (шаг 1), Source (шаг 2), Claim с данными о рождении (шаг 3), LensAdoption (шаг 4) и AssessmentRecord (шаг 5); всё это человек затем просматривает и решает (шаг 6). Разобранный пример идёт этим путём. |
| Самоописание в разговоре | «Я Проектор», «мой авторитет — селезёночный» | Путь `self-chosen` (§2). Если карты нет — результат, названный самим человеком (шаг 5, вариант). Собственные Claim человека (шаг 7). |
| Данные о рождении | Дата, время и место рождения | Один Claim с `facet: "fact"` и категорией `birth-data` (шаг 3). |
| Заметки с разбора у аналитика | Прочтение карты практиком | Source, автор — Party аналитика (`role: "practitioner"`, шаг 2). Своё прочтение человек пишет сам (шаг 8). С 0.1.0-draft.2 прочтение аналитика можно записать и как прочтение через линзу — при принятии `inherited-from-practice`, где аналитик указан в `interpretationAuthors` (I5); в примере этого нет. |
| Прочтение агента | — | **Только по разрешению человека.** Агент предлагает рамку или читает через неё, только если это позволяет договорённость человека (`suggest`, `infer`, называющие линзу) и действующее принятие линзы не в `off` (I5). Всё прочитанное остаётся `frame-relative` и говорится языком рамки, а не как факт или предсказание (AR-4, C-7). |

## 2. Прежде чем начать

**Что это за линза в OHC.** Символическая рамка: `kind: self-description-frame`, `measurementTier: T5`, `ontologicalStatus: symbolic-frame`. Любой результат и всё прочитанное из него — `frame-relative` и никогда не выдаётся за эмпирический факт (AR-4, C-7); связи с эмпирическими конструктами нет (сопоставление `urn:ohc:mapping:human-design--any`, `not-permitted`). Описание линзы не ссылается ни на одно эмпирическое исследование; его ссылки касаются только интеллектуальной собственности (суд Флоренции, 2020 **[F2]**; две записи USPTO, прочитаны).

**Пути принятия.**

| Путь | Можно | Что он меняет |
|---|---|---|
| `imported` | да | Импортёр за один запуск создаёт записи по выгрузке. Все они несут `importedFrom` с одним и тем же `run` (id записи Event). LensAdoption и AssessmentRecord остаются `proposed`, пока человек не подтвердит их записями Review (LA-5). Разобранный пример идёт этим путём. |
| `self-chosen` | да | Записи пишет сам человек; принятие действует сразу. Измените разобранный пример так: **нет** `events` и **нет** `reviews` (шаги 1 и 6 пропускаются). `la-01`: `"route": "self-chosen"`, `"origin": "declared"`, без `generatedBy`, `derivedFrom` и `importedFrom`. `as-01`: без `importedFrom` и `formulatedAt`; запись остаётся `origin: "derived"` (AR-1), а её `generatedBy` называет программу, которая рассчитала карту (например, `{"software": "example-chart-app", "version": "5.1", "method": "computed by the chart app from the birth data; type, authority, profile and defined centres copied from its export"}`). `c-01` и `src-01`: `"origin": "declared"`, без `importedFrom` и `formulatedAt`. |
| `agent-suggested` | только по разрешению человека | Указан, обычно когда человек сам заговорил о рамке; пути описывают обычную практику и ничего не ограничивают. Агент предлагает рамку только по разрешению с `suggest`, называющему линзу, и принятие остаётся предложением, пока человек его не допустит (LA-1). |
| `inherited-from-practice` | да | Указан (роль `other`). Разбор у аналитика можно унаследовать с блоком `practice`; прочтениям аналитика нужно, чтобы он был в `interpretationAuthors` (I5). |

**Согласие.** Для записи разрешение не нужно; без Grant никому ничего не раскрывается. Записи, ссылающиеся на линзу, имеют уровень `special`: чтобы ими поделиться, нужен Grant с `basis.legal: "explicit-consent"` и сроком не дольше 180 дней (R-G3, R-G10). `la-01`, `as-01` и `in-01` — записи `frame-relative`: до них дотягивается только селектор, называющий линзу; одни id не дотягиваются никогда (§12.3, шаг 8). Селектор `ids` работает только для Episode и простых Claim.

**Что задано по умолчанию для этой линзы.**

- Записи, ссылающиеся на линзу: `sensitivity: "special"`, `categories: ["birth-data"]`.
- Claim с данными о рождении: категория `birth-data`; рекомендуется `handling: ["person-only"]`.
- AssessmentRecord: `epistemic: "frame-relative"`; рекомендуется `handling: ["no-infer", "no-quote-back"]`, если человек хочет держать карту в стороне от любых выводов.
- Каждый Claim, выведенный из карты: `epistemic: "frame-relative"`, вручную (шаг 7а). Проверка не замечает, если его нет.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет; `interpretationAuthors` остаётся `["subject"]`. Человек может изменить и то и другое (I5).
- У линзы `reviewAfter` равно `on-change`; в AssessmentRecord `reviewAfter` не указывайте.

**Что не хранится никогда.**

- Описания типов, авторитетов, профилей и центров из приложения или книги (текст отчётов). Выгрузка остаётся в хранилище; в записях — только значения атрибутов и слова самого человека.
- Зарегистрированный составной товарный знак и заброшенный знак из `ip.marks` описания — нигде: ни в ярлыках, ни в названиях, ни в заметках, ни в полях `engine`.
- Ворота, каналы и положения планет с градусами, если человек сам о них не попросил: по ним можно восстановить время рождения.
- Карта другого человека или карта, объединяющая нескольких людей (пару, семью, команду). Ни одна запись не описывает третье лицо (TP-1).
- Ярлыки, перенесённые между линзами в любую сторону (тип Дизайна человека «по вашей Большой пятёрке», черта Большой пятёрки «по вашему типу»).
- Указания, что человеку следует решить. «Стратегия» и «авторитет» остаются атрибутами рамки и никогда не становятся правилами, которые применяют другие.

## 3. Шаги

Импорт запускает сам человек (или агент делает это за него, записывая от его имени, `assertedBy: "subject"`). Каждый фрагмент — запись из [разобранного примера](examples/human-design/context.json), и он проходит проверку по схеме, если он не помечен как вариант (варианты проверены отдельно и тоже проходят L1).

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
  "created": "2026-09-09T20:30:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "events": [], "sources": [], "claims": [], "lensAdoptions": [], "assessments": [], "reviews": [],
  "episodes": [], "interpretations": [], "grants": []
}
```

- Схема требует `format`, `specVersion`, `id`, `version` и `subject.id`. `holder`, `lang` и `policy` выше — это выписанные значения по умолчанию. Меняйте `version` с каждым набором изменений.
- **Только для вымышленного человека:** добавьте `"synthetic": true` в корень **и** в каждую содержательную запись. Контекст о реальном человеке этого флага не несёт никогда. Проверка требует оба флага только для папки внутри каталога `examples/` или для `id`, начинающегося с `urn:ohc:example:` (разобранный пример использует `urn:ohc:example:wren:human-design`). `tools/ohc_query.py` (шаг 10) строит проекцию без ключа держателя только при флаге в корне.
- Для пути `self-chosen` не пишите `events` и `reviews`. Если делаете шаг 9, добавьте `"practices": []`.

Затем заполните `conformance`, `parties` и `lenses`. Объявите модули (Event и Review относятся к `governance`), перечислите каждую Party, на которую будете ссылаться (приложение как `software` с общей подписью и агентов, с которыми человек будет делиться), и закрепите описание (`sha256` — это SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/human-design.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "s-01", "partyKind": "software", "label": "Chart app"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Personal assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:human-design", "version": "0.2.0", "sha256": "8348d08e660ee9a92c8d31d6400f92a80f5b1fe491d299b9101c2cd9fb819d6e"}
]
```

### Шаг 1. Записать запуск импорта: Event

Одна запись Event с типом `import-run` перечисляет все записи, созданные запуском. Её `id` — это `run` в `importedFrom` каждой записи. В одном файле с единственной Event `seq` равно 1, а `prev` — `sha256:` и 64 нуля; `salt` — не меньше 16 случайных байтов в base64url. Проверка не сверяет `records` с записями, которые несут этот `run` (§6): перечислите ровно те записи, у которых `importedFrom.run` равен `e-01`, — не больше и не меньше.

```json
{"id": "e-01", "seq": 1, "at": "2026-09-12T19:00:00Z", "eventType": "import-run", "actor": "subject",
 "records": ["src-01", "c-01", "la-01", "as-01"], "salt": "kGllOqi3Niw8joCgjhcr3A",
 "prev": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
```

Кто видит: Event хранит только id и коды. Это журнал самого человека.

### Шаг 2. Сохранить выгрузку: Source

Файл выгрузки кладётся в хранилище. Вычислите значения сами, не копируйте их из примера:

1. `sha256` — вывод `shasum -a 256 <файл>` (или `sha256sum <файл>`);
2. `size` — число байтов, `wc -c < <файл>`;
3. переместите файл в `<папка>/vault/<первые два шестнадцатеричных символа sha256>/<sha256>.<расширение>` и запишите этот путь, относительно папки, в `vaultPath`.

Проверка L1 не читает хранилище (`"vaultContentRead": false`): неверный хеш или размер всё равно проходит, поэтому вычисляйте их. Исходное время создания идёт в `formulatedAt`, время импорта — в `recordedAt` (R-T5b).

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/80/802b521730c95985f71e8a4a9a8f5611ceaf3e5e34df5c4dff595e255d9c5d68.json"},
             "sha256": "802b521730c95985f71e8a4a9a8f5611ceaf3e5e34df5c4dff595e255d9c5d68",
             "mediaType": "application/json", "size": 152},
 "capturedAt": "2026-03-02T21:10:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "imported", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "formulatedAt": "2026-03-02T21:10:00Z",
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Кто видит: только человек. `maxRelease: "index"`: ни один получатель не получит больше, чем вид источника, тип файла и примерную дату. **Заметки аналитика** (вариант): добавьте аналитика в `parties` как `{"id": "p-01", "partyKind": "person", "label": "Chart analyst", "role": "practitioner"}` (общая роль, никогда не имя) и храните заметки как Source с `sourceKind: "practitioner-notes"`, `authorship.author: "p-01"`, `inbound: true`, `maxRelease: "index"` и без `summary`.

### Шаг 3. Записать данные о рождении: Claim

Данные о рождении есть в выгрузке; импортёр записывает их один раз. Попросите человека их проверить.

```json
{"id": "c-01", "facet": "fact", "predicate": "birth-data",
 "text": "Born 2 November 1988 at 23:15 local time in Utrecht.",
 "origin": "imported", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "formulatedAt": "2026-03-02T21:10:00Z",
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "horizon": "foundation", "sensitivity": "sensitive", "categories": ["birth-data"], "handling": ["person-only"],
 "synthetic": true}
```

Кто видит: только человек, всегда (`person-only`). Никогда не вписывайте данные о рождении в id, заголовок или заметку.

### Шаг 4. Записать отношение к линзе: LensAdoption

`route: "imported"`, запись создаёт импорт (`origin: "derived"`, поэтому нужны `generatedBy.method` и `derivedFrom`). Она остаётся `proposed`, пока человек не подтвердит её на шаге 6.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"}, "route": "imported",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "human-design.chart",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-import", "version": "0.1.0", "method": "adopt the lens of the imported chart"},
 "derivedFrom": ["src-01"],
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Кто видит: только человек; метка … ожидает решения, пока запись не подтверждена, затем ◇ рамка. После этого Grant дотягивается до неё только через селектор, называющий линзу; один её id не дотягивается никогда.

### Шаг 5. Записать карту: AssessmentRecord

Одна AssessmentRecord с одним результатом `frame-attributes`. `mode: "computed-from-birth-data"` требует `origin: "derived"` (AR-1) вместе с `generatedBy.method` и `derivedFrom`. Ключи `attributes` — id конструктов из описания: `human-design/type`, `human-design/authority`, `human-design/profile`, `human-design/centres`. Значения — короткие коды строчными буквами, никогда не описания. Поля `instrument` нет (линза не перечисляет инструментов), `trademarkNotice` нет (знаки не используются). Раз запись принадлежит тому же запуску, что и импортированное принятие, она `proposed` (LA-5). Проверка не проверяет ключи и значения атрибутов (§6), поэтому следите за этими правилами сами.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "mode": "computed-from-birth-data", "administeredAt": {"start": "2026-03-02", "precision": "day"},
 "results": [
   {"type": "frame-attributes",
    "attributes": {
      "human-design/type": "projector",
      "human-design/authority": "splenic",
      "human-design/profile": "2/4",
      "human-design/centres": {"defined": ["spleen", "throat", "ajna"]}},
    "computedFrom": "c-01",
    "engine": {"name": "example-chart-app", "version": "5.1"}}],
 "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-import", "version": "0.1.0", "method": "copy type, authority, profile and defined centres from the app export"},
 "derivedFrom": ["c-01", "src-01"],
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "formulatedAt": "2026-03-02T21:10:00Z",
 "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**Вариант без карты** (в разобранном примере его нет). Если человек называет только свой тип, запишите запись целиком так:

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "mode": "self-identified", "administeredAt": {"start": "2026-09-12", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "human-design/type", "label": "Projector", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- Нет `source`, `generatedBy`, `derivedFrom`, `computedFrom`, `engine`, `importedFrom` и `formulatedAt`: ничего не рассчитывалось и не импортировалось. Проверка принимает `generatedBy` и `derivedFrom` в заявленной записи (§6); всё равно их не пишите.
- Без карты нет и импорта: идите путём `self-chosen` (§2) и не пишите ни Event, ни Source (шаги 1 и 2 пропускаются). Шаг 3 делайте, только если человек хочет записать данные о рождении, — тогда с `"origin": "declared"` и без `importedFrom` и `formulatedAt`. Если другие записи контекста всё же пришли из запуска импорта, не включайте `as-01` в `records` этой Event.

Кто видит: только человек; позже запись отдаётся только по Grant, селектор которого называет линзу.

### Шаг 6. Человек решает: Review

Ничто из импорта не считается, пока человек этого не скажет. Покажите ему, что импортировано. Он подтверждает принятие линзы (`admit`) и соглашается с картой полностью (`endorse`), частично (`partially-endorse` с `endorsedPart` своими словами — это заодно и подтверждает запись) или не соглашается вовсе (`reject`). `endorsedPart` никогда не цитирует запись: называйте конструкты, а не значения.

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

```json
{"id": "rv-02", "target": "as-01", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-09-13T08:05:00Z",
 "endorsedPart": "The authority and the profile speak to me; I leave the type aside."}
```

**Если человек отклоняет принятие линзы** (вариант), напишите обе записи Review: `decline` на принятие **и** `reject` на карту. Отклонённое принятие само по себе карту не отзывает: в OHC 0.1 карта, оставшаяся с `partially-endorse`, продолжает действовать и отдаётся по селектору линзы (§6). Затем не пишите прочтений через линзу (шаги 7а и 8 пропускаются).

```json
{"id": "rv-01", "target": "la-01", "action": "decline", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

```json
{"id": "rv-02", "target": "as-01", "action": "reject", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

Эти решения принимает только сам человек: записи имеют уровень `special` (R-A1). Молчание — не согласие: импорт, который человек так и не просмотрел, остаётся `proposed`.

### Шаг 7. Оставить только то, что человек принимает: Claim

**7а. Самоописание в терминах системы.** `facet: "identity"`, `predicate: "self-description"`, `epistemic: "frame-relative"`, `derivedFrom` — карта. Никогда не `facet: "disposition"` (CL-3; линза не устанавливает черт).

**Вы ОБЯЗАНЫ поставить `epistemic: "frame-relative"` в каждый Claim, выведенный из `as-01`.** Проверка не замечает, если его нет. Без него Claim считается `as-reported`, получает метку ✓ заявлено, и Grant, называющий его id, отдаёт его как простой заявленный факт.

```json
{"id": "c-02", "facet": "identity", "predicate": "self-description",
 "text": "In this system's terms I decide by a quiet first yes or no in the moment; I trust that more than long lists.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T20:00:00Z", "horizon": "foundation",
 "derivedFrom": ["as-01"], "epistemic": "frame-relative", "handling": ["no-quote-back", "no-infer"],
 "synthetic": true}
```

Кто видит: только человек. В OHC 0.1 эту запись не отдаёт ни один Grant (§6).

**7б. То же понимание простыми словами — чтобы агенты могли с ним считаться.** Спросите человека простыми словами, как с ним лучше работать. Запишите это без слов рамки и **без** `derivedFrom`, чтобы запись держалась на слове человека. Так «авторитет» превращается в то, что помощник может уважать, никогда не решая за человека.

```json
{"id": "c-03", "facet": "preference", "predicate": "decision-brief",
 "text": "For a big request, give me the main point in one line and let me answer the same day; skip the long pros-and-cons list.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T20:05:00Z", "horizon": "foundation",
 "synthetic": true}
```

Кто видит: только человек, пока Grant её не назовёт; уровень `personal`, метка ✓ заявлено.

### Шаг 8. Прочитать эпизод через линзу словами человека: Episode и Interpretation

В примере прочтение через эту линзу пишет сам человек, после того как принятие подтверждено (§6, пункт 10). Добавьте хотя бы одну альтернативу непсихологического вида.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-01", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-09T21:00:00Z", "addedAt": "2026-09-09T21:00:00Z",
    "accountKind": "first-narrative",
    "happened": "At the first meeting I said yes to leading the neighbourhood garden project; a week later I stepped back.",
    "didOrTried": "Wrote to the group and offered to help with watering instead.",
    "understandingThen": "I thought I had simply taken on too much."}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-09T21:00:00Z",
 "sensitivity": "sensitive", "contexts": ["community"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "text": "In this system's terms I answered from the pressure of the room, not from my own first sense in the moment.",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The meeting ran late and everyone was waiting for a volunteer.", "kind": "situational"},
   {"text": "The project budget was cut the following week.", "kind": "external"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-16T09:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-quote-back"], "contexts": ["community"], "synthetic": true}
```

Кто видит: только человек. Episode имеет уровень `sensitive`; прочтение — `special` и `frame-relative`.

### Шаг 9. Практики из набора инструментов

Агенту выполнять нечего. В наборе одна позиция, `human-design.chart` (сама карта); агент может её предложить (`agentMayOffer: true`), когда договорённость человека позволяет ему предлагать рамку.

Практика, которая у человека уже есть, записывается как Practice с `source.route: "self-discovered"` и без `templateId` (вариант, в разобранном примере его нет). Сначала добавьте `"practices"` в `conformance.modules` и `"practices": []` в файл; без модуля проверка падает на CX-5. `practiceKind` — одно из `breathing`, `movement`, `reflection`, `writing`, `conversation`, `rest`, `planning`, `environment`, `social-contact`, `creative`, `contemplative`, `other`.

```json
{"id": "pr-01", "name": "Pause before saying yes", "description": "Wait until the next morning before taking on a new role.",
 "practiceKind": "reflection", "source": {"route": "self-discovered"}, "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-16T09:30:00Z", "synthetic": true}
```

### Шаг 10. Решить, кто что видит: Grant

```json
{"id": "g-01", "recordedAt": "2026-09-15T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:human-design"]}, {"ids": ["ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-15T10:00:00Z", "channel": "holder-ui"},
 "note": "The system's language for my own reflection only; never advice about what I should decide."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-15T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["assist-personal"],
 "scope": {"include": [{"facets": ["preference"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-15T10:05:00Z", "channel": "holder-ui"}}
```

Что получает каждый получатель по §12.3 (посчитано справочными инструментами на разобранном примере, после решений Review):

| Получатель | Отдаётся | Не отдаётся никогда |
|---|---|---|
| `a-01` Спутник для размышлений | `la-01`, `as-01` (подтверждение `partial`, метка ◇ рамка), `in-01`, `ep-01` | `c-01` (`person-only`), `c-02` (Claim `frame-relative`, §6), `c-03` (вне охвата), `src-01` (`maxSourceTier: none`) |
| `a-02` Личный помощник | `c-03` | всё, что ссылается на линзу |

До шага 6 записи `la-01` и `as-01` — предложения и не отдаются никому, кроме самого человека. При `decline` и `reject` (вариант шага 6) и без прочтений `a-01` получает только `ep-01`. Grant только с `{"ids": ["la-01", "as-01"]}` не отдаёт ни одной из них, даже при явном согласии: называйте линзу. Grant g-01 не даёт ни `suggest`, ни `write`, ни `infer`: спутник говорит с человеком его словами и ничего не пишет через линзу.

Чтобы посчитать эту таблицу для своего контекста, запустите для каждого Grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose assist-personal --now 2026-10-10T12:00:00Z
```

Отданные записи появляются в `statements`, `experience`, `interpretations` и `recall`; Party, на которые они указывают, — в `parties`. Контексту без `"synthetic": true` в корне нужен `--holder-key-file`.

### Шаг 11. Проверить

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Ожидается `"valid": true` и `"levelMet": "L1"`. Папку внутри каталога `examples/` проверка сравнивает с её `expected-check.json` (X-3); ваш собственный контекст — нет. Успешная проверка не покрывает того, что, как сказано в §2 и шагах, она не ловит: `epistemic` у выведенных Claim, ключи атрибутов, `e-01.records` и хеши хранилища.

## 4. Никогда

- Никогда не заводите речь о Дизайне человека и не предлагайте рассчитать карту, если договорённость человека этого не позволяет (`suggest`, называющее линзу), а тогда — только как один из вариантов. Никогда не читайте через линзу от имени агента сверх разрешения и принятия линзы человека (I5); оценка видна только человеку (AR-2), а всё прочитанное в рамке — `frame-relative` (AR-4).
- Никогда не используйте ни зарегистрированный составной знак из описания (`use: avoid`), ни заброшенный — ни в одном поле. Говорите «Дизайн человека» (Human Design) и пользуйтесь id конструктов.
- Никогда не говорите человеку, что ему решить, исходя из типа, стратегии или авторитета, и никогда не используйте карту, чтобы направлять, давить или убеждать (`persuasion-targeting` запрещено; ограничение `no-leverage`, если человек его добавит). При `decisionUse: approval-required` вы можете назвать принятый человеком атрибут карты, когда что-то предлагаете, — как язык рамки, а не как факт (R-G14, C-7). Помощники следуют простому предпочтению самого человека (шаг 7б).
- Никогда не выдавайте атрибут карты или прочитанное из него за эмпирическую черту или предсказание (C-7); никогда не сопоставляйте атрибуты карты с чертой, типом или баллом (LN-3, сопоставление `no-relation`).
- Никогда не используйте ничего из этой линзы для запрещённых целей (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting`), в том числе для подбора команды или подбора пар людей по картам.
- Никогда не приводите карту как довод («ваш дизайн говорит…»): `no-quote-back`. Говорите языком рамки словами человека.
- Никогда не рассчитывайте, не храните и не обсуждайте карту другого человека или объединённую карту (TP-1).
- Никогда не отдавайте Claim с данными о рождении; никогда не вписывайте данные о рождении в id, заголовки или заметки (R-I1).

## 5. Разобранный пример

[examples/human-design/context.json](examples/human-design/context.json): Рен, вымышленный волонтёр соседского проекта. Пример содержит ровно записи раздела 3 (без вариантов): `e-01`, `src-01`, `c-01`, `la-01`, `as-01`, `rv-01`, `rv-02`, `c-02`, `c-03`, `ep-01`, `in-01`, `g-01`, `g-02`, а также заглушку в хранилище для `src-01`. Корень контекста и каждая содержательная запись несут `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/human-design --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений ([expected-check.json](examples/human-design/expected-check.json)).

## 6. Что пока не помещается

1. **Claim с `frame-relative` нельзя никому показать.** У Claim нет поля `lens`, а §12.3, шаг 8 отдаёт запись `frame-relative` только по селектору, называющему её линзу; Claim из шага 7а не отдаётся даже по id. Предложение: разрешить `lens` в Claim с `frame-relative` или позволить шагу 8 принимать селектор `ids`.
2. **Нет связи «пришло в голову при взгляде на карту», которая не была бы свидетельством.** Ссылка на карту в простом Claim (шаг 7б) сделала бы рамку основанием и подняла бы Claim до `special`. Предложение: код связи Relation вроде `prompted-by`, без переноса уровня и никогда не путь для выводов.
3. **Импортированную карту приходится помечать как `derived`.** AR-1 допускает для `computed-from-birth-data` только `derived` (и отвергает `imported`), хотя значения скопированы из приложения, расчёт которого человек не запускал. Предложение: разрешить для этого режима `imported` (с `importedFrom`).
4. **Импортированные данные о рождении действуют, хотя человек на них не смотрел.** LA-5 делает предложениями только AssessmentRecord из импортированного запуска; Claim с данными о рождении и Source из того же запуска действуют сразу, а Claim даже получает метку ✓ подтверждено. Предложение: распространить LA-5 на все содержательные записи запуска.
5. **Точное происхождение может столкнуться с товарными знаками.** Если в названии самого приложения есть знак, который описание велит избегать (`avoid`), его нельзя записать ни в `engine.name`, ни в `importedFrom.system`. Предложение: разрешить номинативное употребление только в полях происхождения, с уведомлением о знаке, или ссылку `engine.ref`.
6. **Прочтению аналитика негде жить.** *Исправлено в 0.1.0-draft.2:* пути ничего не ограничивают (LN-3 теперь запрещает только сопоставление с другими линзами), а I5 применяет `agentInterpretation` только к авторам-агентам и программам, поэтому аналитик из `interpretationAuthors` унаследованного принятия может быть автором прочтения.
7. **`frame-attributes.attributes` — без структуры.** У центров (определённых и неопределённых), ворот и каналов нет формы, ничто не связывает ключи с конструктами и не ограничивает точность. Предложение: `attributes: [{"construct", "value"}]` и список атрибутов в описании, которые никогда не хранятся.
8. **`decisionUse: never` читается так, будто запрещено и собственное использование человеком.** *Исправлено в 0.1.0-draft.2:* у записей нет `decisionUse`. Собственные выборы человека — его дело; что агент может учитывать в своих предложениях, решает разрешение человека (R-G14), а решения других о человеке закрыты запрещёнными целями (§8.10).
9. **Умолчания линзы не задают ограничения обращения.** Предложение: `defaults.handling` в описании. (То, что путь принятия не сверяется с путями из описания, с 0.1.0-draft.2 задумано: пути описывают и никогда не ограничивают.)
10. **Записи линзы продолжают отдаваться, когда человек отклонил принятие, а прочтение отдаётся, пока принятие ещё `proposed`.** После Review `decline` на `la-01` запись `as-01` из того же запуска импорта (оставшаяся с `partially-endorse`) и `in-01` по-прежнему отдаются по селектору линзы. Совсем без Review `in-01` отдаётся, пока `la-01` — предложение. Предложение (§12.3): селектор линзы отдаёт записи линзы только пока принятие этой линзы человеком действует; и LA-5: отклонение импортированного принятия отклоняет все записи его запуска.
11. **`importedFrom.run` не разрешается, а `Event.records` не сверяется.** `c-01` и `src-01` с `importedFrom.run: "e-01"` проходят, когда Event нет вовсе (путь `self-chosen`, выполненный буквально, оставляет ровно это). Event, в `records` которой нет `la-01`, хотя `la-01` несёт этот запуск, тоже проходит. Предложение: добавить `importedFrom.run` в каталог допустимых ссылок с целью Event с `eventType: "import-run"` и правило: каждая запись с запуском `e` перечислена в `e.records`, и наоборот.
12. **Статус `frame-relative` не передаётся по `derivedFrom`.** Claim, выведенный из карты (шаг 7а) и записанный без `epistemic`, считается `as-reported`, получает метку ✓ заявлено и отдаётся по Grant, называющему его id; ни правило, ни предупреждение не срабатывают. Предложение: передавать `frame-relative` по `derivedFrom` и `grounds`, как передаётся уровень, или ошибка на L1, когда запись, выведенная из записи `frame-relative`, сама не `frame-relative`.
13. **Заявленная запись может нести `generatedBy` и `derivedFrom`.** AssessmentRecord, названная самим человеком (`origin: "declared"`), с этими полями проходит, и её происхождение утверждает расчёт, которого не было. Предложение: `generatedBy` только при `origin` `derived` или `inferred`.
14. **Флаг `synthetic` в корне не связан с флагами записей.** Вне режима примеров все содержательные записи могут быть синтетическими, а корень — нет; проверка это принимает, а `ohc_query.py` тогда требует ключ держателя. Предложение: предупреждение на L1 при расхождении или выводить флаг корня из записей.
15. **На L1 хранилище не сверяется с Source.** Неверные `sha256` или `size` проходят (`"vaultContentRead": false`). Предложение: проверка по флагу (или на L1, когда хранилище локальное), которая хеширует файлы хранилища и сверяет `sha256` и `size`: ошибка при расхождении, предупреждение, когда файла нет.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
