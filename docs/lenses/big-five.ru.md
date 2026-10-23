# Большая пятёрка: как перенести материал человека в OHC

**Рецепт · линза `urn:ohc:lens:big-five` 0.2.0 · OHC 0.1.0-draft.2 · информативный · 12 октября 2026**

Этот рецепт превращает материал человека по Большой пятёрке (результат опросника, который у него есть, его собственные слова о своих склонностях и прочтения недавних эпизодов) в записи OHC — шаг за шагом и запись за записью, не сохраняя ничего, что запрещают линза или методика.

Описание линзы — `spec/lenses/big-five.lens.json` (`descriptorStatus: draft`, `legalReviewNeeded: true`). Это полное описание, а не заготовка (stub), поэтому доступны все шаги ниже. Прочитайте его до начала: его `mentalModel`, `ip` и `defaults` — это факты и рекомендации, которые применяет рецепт.

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:big-five-basic`](../../spec/playbooks/big-five-basic.playbook.json) («Большая пятёрка: базовые способы работы», редакция OHC), для таких ситуаций: планирование предстоящей недели; выбор между вариантами; обратная связь другому человеку; разбор того, что произошло; подготовка к трудному разговору; под нагрузкой: усталость, давление или перегрузка. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** У записи BFI-2 в каталоге есть блок `import`, поэтому результат BFI-2 человек может принести через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md); разобранный пример — [Тове](../../examples/tove-bring-a-result/)). Шаги ниже записывают отчёт вручную, как для IPIP-NEO-120 и NEO-PI-3.

## 1. Что у вас может быть

| Что есть | Пример | Куда это идёт |
|---|---|---|
| Самоописание в разговоре | «Я собранный, но толпа меня выматывает.» | Утверждение (Claim) словами человека (шаг 4). Без AssessmentRecord: слова — не балл. |
| Отчёт методики, который есть у человека | Страница с баллами IPIP-NEO-120; баллы BFI-2 из исследования; отчёт NEO-PI-3 от квалифицированного специалиста | Файл отчёта — источник (Source, шаг 2); баллы — AssessmentRecord (шаг 3). |
| Заметки из коучинга, обучения или терапии, где использовалась Большая пятёрка | Заметки коуча о сессии, где упомянуты баллы человека | Путь принятия линзы `inherited-from-practice` (шаг 1); заметки — источник под охраной специалиста (шаг 2). Их текст никогда не копируется в записи. |
| Прочтение агента | Собеседника, который неделями разговаривает с человеком, спрашивают: «а ты бы как оценил?» | Только если человек сам просит и только по разрешению, которое даёт агенту и `suggest`, и `infer`: AssessmentRecord с `mode: agent-inference`, который видит только человек (шаг 3b), и прочтения эпизодов (шаг 5). |

В линзе перечислены три методики: `urn:ohc:instrument:ipip-neo-120` (вопросы в общественном достоянии, открытый подсчёт), `urn:ohc:instrument:bfi-2` (авторское право на вопросы — у Сото и Джона; бесплатно только для некоммерческих исследований) и `urn:ohc:instrument:neo-pi-3` (закрытая методика PAR, Inc.; квалификация уровня S). Тест, которого нет среди этих трёх, нельзя указать в `instrument` (AR-8); см. §6.

## 2. Прежде чем начать

**Путь принятия линзы.** Выберите тот, что соответствует тому, как человек пришёл к линзе. Он записывается в `LensAdoption.route`.

| Путь | Когда | Что он меняет |
|---|---|---|
| `self-chosen` | Человек сам выбрал линзу. Пример этого рецепта идёт этим путём. | Принятие действует сразу после записи. |
| `agent-suggested` | Линзу предложили вы — по разрешению, которое это позволяет (`suggest` с селектором, называющим линзу). `adoption.suggestionRequires` в описании говорит, когда это обычно уместно: после того как человек сам попросил способы описать свои склонности. | Добавьте `suggestedBy` с вашим идентификатором Party. Принятие остаётся `proposed`, пока человек не допустит его записью Review с `admit` (LA-1); см. фрагмент ниже. |
| `inherited-from-practice` | Линза пришла от коуча, преподавателя или терапевта человека (`adoption.inheritanceRoles`). | Добавьте блок `practice`: `role`, `practitioner` (идентификатор Party), `relationship`, `since` и `releaseRef` (источник с разрешением специалиста) — всякий раз, когда хранится источник, автор которого специалист или который у него на хранении, включая сам отчёт (LA-3). Задайте `confidentiality` и `onEnd`. Принятие линзы не даёт специалисту никакого доступа (LA-2); доступ даёт только разрешение (Grant). |
| `imported` | Принятие создала программа импорта из отчёта. | Принятие остаётся `proposed`, пока человек его не допустит; так же и каждый AssessmentRecord из того же прогона импорта (LA-5). |

**Путь `agent-suggested` в записях.** Принятие остаётся записью человека (`assertedBy: "subject"`); `suggestedBy` называет вас. Просьбу человека запишите в `note` его словами: в OHC 0.1 для неё нет поля (§6).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "route": "agent-suggested", "suggestedBy": "a-01",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "big-five.score-profile",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-10T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"],
 "note": "Kesi asked for ways to describe tendencies; the companion suggested the Big Five.", "synthetic": true}
```

Затем допуск человека кладётся в `reviews`. Допускает только сам человек: допуск от кого-то другого не проходит LA-1. Пока человек его не допустил, принятие не действует и ничего не запрещает и не разрешает.

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-08-10T18:05:00Z"}
```

**Согласие.** Спрашивайте перед каждым шагом и зачитывайте каждую запись перед сохранением. Человек может остановиться на любом шаге. Для ваших собственных прочтений и оценок нужно отдельное «да»: разрешение, которое даёт агенту и `suggest`, и `infer`, с `basis.legal: explicit-consent` (INF-1, R-G11). Разрешение с `infer`, но без `suggest` не проходит INF-1.

**Кто пишет.** Собственный держатель человека пишет записи человека с `assertedBy: "subject"`. Если вы агент, вы пишете только два вида записей:

- свои прочтения и оценки: `assertedBy` — ваш идентификатор Party, `origin: "inferred"`, а `underGrant` и `purpose` называют разрешение, которое даёт вам `suggest` и `infer` (INF-1). Они остаются `proposed`, пока человек не решит;
- собственные утверждения человека — только если человек дал вам разрешение с `write`: оставьте `assertedBy: "subject"`, добавьте `recordedBy` (ваш идентификатор Party), `underGrant` и `purpose` и сначала зачитайте запись. Такая запись действует сразу, поэтому никогда не пишите того, что человек не подтвердил слово в слово (§6).

**Умолчания этой линзы** (`defaults` в описании):

- `sensitivity: "special"`: любая запись этой линзы относится к особой категории. Разрешение дотягивается до неё, только если называет её идентификатор, её линзу или её категорию, при явно выраженном согласии (R-G3).
- `categories: ["mental-health"]`. Понятия `big-five/N`, `big-five/N/anxiety` и `big-five/N/depression` сами несут `mental-health`.
- `reviewAfter: "P3Y"`: через три года результаты пора пересмотреть.
- Ограничения обращения: описание запрещает помощнику комментировать аспекты «Тревожность» и «Депрессивность», если человек сам о них не заговорил. Храните эти два аспекта в отдельном AssessmentRecord с ограничениями `subject-initiated-only` и `no-quote-back` (шаг 3).

**Что не хранится никогда.**

- Текст вопросов любой методики. Для NEO-PI-3 и BFI-2 это условие лицензии (`ip.restrictions`); для IPIP он просто не нужен.
- Ответы на вопросы. Единственное исключение — собственные тестовые данные человека в `ext["ohc.test-data"]` с ограничением `person-only` и признаком валидности `test-data-personal-only` (AR-3).
- Ключи подсчёта и текст отчёта (например, толкования из отчёта NEO-PI-3). Копируйте числа, а не фразы.
- Ярлыки других систем, выведенные из этих баллов: никаких буквенных типов, никаких «типов» вообще (M-4).
- Балл как оценка человека: «низкая доброжелательность» — это диапазон по одному опроснику, а не «трудный характер».

## 3. Шаги

Каждый шаг говорит, что сделать, какую запись написать, даёт фрагмент JSON, который проходит проверку по `spec/schema/*.schema.json`, и говорит, кто видит запись по умолчанию. Фрагменты — это записи разобранного примера (§5) в форме одного документа: каждая кладётся в массив, названный в шаге. **По умолчанию никто, кроме самого человека, ничего не видит** (R-G1); это меняется только в шаге 7.

### Шаг 0. Файл и его папка

Один контекст — одна папка. Все записи лежат в одном файле, `context.json`. Исходные файлы (отчёты, заметки, разрешения специалистов) лежат рядом с ним в `vault/`. Программу проверки запускают на папку (шаг 8).

```text
<папка>/
  context.json
  vault/5a/5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c.json
```

Начните `context.json` с корня. Вот корневые поля разобранного примера:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:kesi:big-five", "version": "2026-09-12.1",
 "subject": {"id": "urn:ohc:example:kesi", "displayName": "Kesi (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-08-10T18:00:00Z",
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` и `subject` обязательны (`spec/schema/context.schema.json`).
- `id` и `subject.id`: для настоящего человека — `urn:uuid:`, который вы создаёте сами, никогда не имя и не почта. `urn:ohc:example:<имя>[:<контекст>]` — только для примеров.
- `version` — любой текст на ваш выбор; меняйте его при каждом изменении файла.
- `synthetic: true` — только в примерах: и в корне, и в каждой записи. Для настоящего человека это поле не пишется.
- В тот же объект добавьте `conformance`, `parties` и `lenses` (шаг 1), затем массивы, которые заполняет этот рецепт: `lensAdoptions` (шаг 1), `sources` (2), `assessments` (3, 3b), `claims` и `relations` (4), `episodes` и `interpretations` (5), `reviews` (3b, 5), `practices` и `outcomes` (6), `grants` (7). Массив, которым вы не пользуетесь, не пишите.
- **Коды для `contexts`** (в любой записи, где есть это поле): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`. Всё остальное должно быть локальным кодом `x-<пространство>:<код>`, объявленным в корневом `vocabulary`, например `"vocabulary": {"x-kesi:choir": {"definition": "Singing in a community choir"}}`. Любое другое значение не проходит S-3.

### Шаг 1. Закрепите линзу и запишите её принятие

Спросите, как человек пришёл к линзе и что он хочет с ней делать. Затем:

1. В манифесте объявите модули, которыми будете пользоваться, и закрепите линзу. `sha256` — это SHA-256 файла описания, который вы прочитали (`shasum -a 256 spec/lenses/big-five.lens.json`); по нему позже можно проверить, какая версия использовалась.
2. Перечислите все стороны (Party), которых будете называть: агентов, программу, которая выдала отчёт, специалиста, если он есть.
3. Запишите LensAdoption в `lensAdoptions`.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"},
  {"id": "s-01", "partyKind": "software", "label": "Public IPIP scoring page"}
],
"lenses": [{"id": "urn:ohc:lens:big-five", "version": "0.2.0", "sha256": "6af97400e92c87df43cdb7aa7d7406c0a6688c4f819d456182559bd4d41b0a4d"}]
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "big-five.score-profile",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-10T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `uses` записывает, на что человек согласился: `speak-in-lens`, `store-results`, `interpret`, `offer-practices`, `recall`. OHC 0.1 этого не проверяет: ни одно правило не связывает запись с `uses`. Поэтому держаться этого должны вы и держатель сами: храните результаты только при `store-results`, пишите прочтения только при `interpret`, предлагайте инструменты линзы только при `offer-practices` (§6).
- `agentInterpretation` — `off` (по умолчанию), `ask-first` или `allowed`. Пока принятие действует, `off` останавливает любое прочтение агента через линзу, что бы ни говорило разрешение. При `ask-first` спрашивайте перед каждым прочтением; в контексте с журналом событий (L2) каждое подтверждение записывается как событие (Event) `ask-first` (I5).
- `interpretationAuthors` — кто из людей, кроме самого человека (например, коуч), может писать прочтения через линзу. Агент читает через неё по своему разрешению: по разрешению с `infer`, чья область называет линзу (I5).
- `representationPreference` — единственный способ представления в описании, `big-five.score-profile` (сырой балл, диапазон и процентиль с названной нормативной группой).

**Кто видит:** только человек. Принятие линзы никому не даёт доступа.

### Шаг 2. Сохраните исходный отчёт как источник

Положите файл отчёта, который дал вам человек, в хранилище источников и опишите его. Три значения вычисляйте по самому файлу, никогда не набирайте их вручную:

- `sha256` — SHA-256 байтов файла строчными шестнадцатеричными символами (`shasum -a 256 <файл>` или `sha256sum <файл>`);
- `size` — длина файла в байтах (`wc -c < <файл>`);
- `vaultPath` — `vault/<первые два символа sha256>/<sha256>.<расширение>`, относительно папки, где лежит `context.json`.

Программа проверки только сверяет `sha256` с именем в `vaultPath` (SR-3). Файлы хранилища она не открывает (`vaultContentRead: false`), поэтому неверный хеш, неверный размер или отсутствующий файл проходят незамеченными (§6).

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/5a/5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c.json"},
             "sha256": "5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c",
             "mediaType": "application/json", "size": 644},
 "capturedAt": "2026-08-14T19:40:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Score page saved after taking the IPIP-NEO-120.", "authoredBy": "subject",
             "recordedAt": "2026-08-14T20:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-14T20:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author` — тот, кто выдал отчёт: программа подсчёта (Party вида `software`) или специалист, который его передал (Party вида `person`).
- `maxRelease: "index"`: получатель узнаёт самое большее, что отчёт существует. Держите `index` для любого отчёта: в отчёте NEO-PI-3 есть закрытый авторский текст, который никуда не должен уходить.
- **От специалиста** (отчёт NEO-PI-3, заметки коуча): добавьте `"custody": {"custodian": "<идентификатор Party специалиста>", "confidentiality": "coaching" | "therapy", "releaseRef": "<идентификатор источника с разрешением специалиста>"}`, оставьте `maxRelease: "index"`, а для заметок используйте `sourceKind: "practitioner-notes"`. Для преподавателя пишите `"confidentiality": "none"`: в 0.1 нет кода для обучения (§6), поэтому файл защищает `maxRelease: "index"`. Само разрешение специалиста сохраните отдельным источником (`sourceKind: "practitioner-release"`, автор — специалист).
- `summary.text` — собственное описание человека в одну строку. Никогда не вставляйте текст отчёта в `summary`, `title` или `note` (SR-4).

**Кто видит:** человек — всегда и полностью. Получатель — самое большее на уровне `index` и только если разрешение его называет.

### Шаг 3. Запишите результат как AssessmentRecord

Переносите из отчёта только числа. Спросите человека, хочет ли он вообще хранить аспекты «Тревожность» и «Депрессивность»; если да — запишите их во вторую запись с собственными ограничениями.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "lensVariant": "5-domain-30-facet",
 "instrument": {"id": "urn:ohc:instrument:ipip-neo-120", "form": "120"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-08-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/O", "label": "Openness", "raw": 4.2, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 81}},
   {"type": "dimension-score", "construct": "big-five/C", "label": "Conscientiousness", "raw": 3.9, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 66}},
   {"type": "dimension-score", "construct": "big-five/E", "label": "Extraversion", "raw": 2.6, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 22}},
   {"type": "dimension-score", "construct": "big-five/A", "label": "Agreeableness", "raw": 3.7, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 52}},
   {"type": "dimension-score", "construct": "big-five/N", "label": "Neuroticism", "raw": 3.1, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 55}}],
 "normGroup": {"id": "ipip-neo-120-internet-2014", "year": 2014, "note": "Internet sample published with the IPIP-NEO-120"},
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "public IPIP scoring page", "method": "means of keyed items on a 1-5 scale; percentiles against the published internet norms"},
 "assertedBy": "subject", "recordedAt": "2026-08-14T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "as-02", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "lensVariant": "5-domain-30-facet",
 "instrument": {"id": "urn:ohc:instrument:ipip-neo-120", "form": "120"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-08-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/N/anxiety", "label": "Anxiety (facet)", "raw": 3.5, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "big-five/N/depression", "label": "Depression (facet)", "raw": 2.5, "rawRange": [1, 5]}],
 "normGroup": {"id": "ipip-neo-120-internet-2014", "year": 2014, "note": "Internet sample published with the IPIP-NEO-120"},
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "public IPIP scoring page", "method": "means of keyed items on a 1-5 scale"},
 "assertedBy": "subject", "recordedAt": "2026-08-14T20:06:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only", "no-quote-back"],
 "synthetic": true}
```

Поля заполняются так:

| Поле | Значение |
|---|---|
| `lens` | `{"id": "urn:ohc:lens:big-five", "version": "0.2.0"}` |
| `lensVariant` | `5-domain-30-facet` для IPIP-NEO-120 и NEO-PI-3; `bfi-2-15-facet` для BFI-2. Программа проверки это значение не проверяет, поэтому копируйте его точно (§6). |
| `instrument` | `id` — один из трёх идентификаторов методик. `form` — идентификатор формы из описания методики (`spec/instruments/<имя>.instrument.json`, `forms[].id`): `"120"` для IPIP-NEO-120, `"60"` для BFI-2, `"self-report"` или `"informant-report"` для NEO-PI-3. `version` — издание издателя, **напечатанное в отчёте**, а не собственная `version` записи каталога (`0.1.0`; `0.2.0` у BFI-2). Если в отчёте издание не напечатано, `version` не пишите — как на странице баллов Кеси и обычно на листе BFI-2. |
| `mode` и `origin` (AR-1) | Баллы посчитали вы или открытая страница подсчёта: `self-report-instrument` с `origin: "derived"`, плюс `derivedFrom` (источник) и `generatedBy` с `method`. Отчёт поставщика переносится как есть (NEO-PI-3): `vendor-report-import` с `origin: "imported"` и `importedFrom` (`importedAt` равен `recordedAt`); см. фрагмент ниже. Человека оценивал другой человек по форме для наблюдателя: `observer-report` с `assessedBy` (его идентификатор Party) и `raterRelationship`. |
| `results` | По одному `dimension-score` на понятие. `construct` берётся из `constructs` описания: `big-five/O`, `big-five/C`, `big-five/E`, `big-five/A`, `big-five/N`, `big-five/N/anxiety`, `big-five/N/depression`. Других аспектов в описании нет, поэтому остальные аспекты отчёта не записывайте; никогда не придумывайте идентификатор (§6). `raw` и `rawRange` — как напечатано; `standardized` — только если отчёт его даёт (`percentile`, `T`, `z`, `stanine` или `sten`). Для BFI-2 сохраните формулировку отчёта в `label` (например, «Negative Emotionality»), а идентификатор понятия — `big-five/N`. |
| `normGroup` | Нормативная выборка, которую называет отчёт. Если отчёт её не называет, не пишите `normGroup` и при каждом показе баллов говорите «нормативной группы нет». |
| `validityFlags` | То, что говорит отчёт или ситуация: `incomplete`, `translated-form`, `norm-mismatch`, `vendor-algorithm-undisclosed` и т. д. У отчёта поставщика NEO-PI-3 всегда есть `vendor-algorithm-undisclosed` (его подсчёт закрыт). Пустой список значит, что ничего не применимо. |
| `trademarkNotice` | Только у подлинного результата NEO-PI-3: `notice` знака из `spec/instruments/neo-pi-3.instrument.json`, скопированный точно. OHC 0.1 требует уведомления только для знаков из описания линзы (у этой линзы их нет), и программа проверки этого уведомления не требует; всё равно добавьте его (§6). Никогда — у оценки агента (AR-2). |
| `reviewAfter` | `P3Y`, из `defaults` описания. |
| `sensitivity`, `categories` | `special`, `["mental-health"]`. |

**Отчёт NEO-PI-3 от специалиста.** Постройте запись как `as-01`, уберите `derivedFrom` и `generatedBy` и используйте такие поля (у Кеси такого отчёта нет, поэтому в примере его нет; запись, построенная так, проходит L1):

```json
"lensVariant": "5-domain-30-facet",
"instrument": {"id": "urn:ohc:instrument:neo-pi-3", "form": "self-report"},
"mode": "vendor-report-import",
"validityFlags": ["vendor-algorithm-undisclosed"],
"trademarkNotice": "NEO-PI-3™ is a mark of PAR, Inc.; used here only to name the instrument.",
"origin": "imported",
"importedFrom": {"system": "NEO-PI-3 report handed over by the psychologist", "importedAt": "2026-08-15T10:00:00Z"},
"recordedAt": "2026-08-15T10:00:00Z"
```

**Кто видит:** человек. Получатель — только если разрешение называет линзу, категорию или идентификатор при явно выраженном согласии. `as-02` к тому же несёт `subject-initiated-only` (используется только в разговоре, который начал сам человек) и `no-quote-back` (никогда не приводится человеку как доказательство).

### Шаг 3b. Только если человек просит: оценка агента

Можно ли вам делать оценку, решает разрешение человека: оно должно давать вам и `suggest`, и `infer` и называть линзу (`g-01` в шаге 7). Делайте оценку, когда человек о ней просит, например чтобы сравнить с опросником. Пишите её как свою запись; затем человек решает, оставить ли её.

```json
{"id": "as-03", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"},
 "mode": "agent-inference", "assessedBy": "a-01",
 "administeredAt": {"start": "2026-09-01", "end": "2026-09-10", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/E", "raw": 3.4, "rawRange": [1, 5]}],
 "validityFlags": ["agent-estimate-not-validated"], "validityCeiling": "agent-estimate-not-validated",
 "derivedFrom": ["ep-01", "ep-02", "ep-03"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-10T10:05:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["person-only"],
 "note": "Asked for by Kesi: a rough guess from three episodes, to compare with the questionnaire.",
 "synthetic": true}
```

```json
{"id": "rv-02", "target": "as-03", "action": "admit", "by": "subject", "recordedAt": "2026-09-12T08:02:00Z"}
```

- AR-2 требует всё сразу: ограничение `person-only`, признак и потолок `agent-estimate-not-validated`, никакого `trademarkNotice` и никаких фирменных обозначений.
- `derivedFrom` называет эпизоды, на которых держится догадка (шаг 5). `label` не пишите: это догадка, а не измеренный результат. Никогда не пишите туда название методики, например «NEO-PI-3».
- Допустить её может только сам человек (R-A1); запись Review кладётся в `reviews`. Если человек отказывается, напишите `"action": "decline"`; оценка остаётся в истории и не используется.

**Кто видит:** всегда только человек (`person-only`); даже вам она в проекции не возвращается.

### Шаг 4. Утверждения, которые человек принимает

Покажите человеку профиль баллов: сырой балл, диапазон и нормативную группу вместе. Спросите, какие склонности он узнаёт и в каких обстоятельствах. Пишите утверждение (Claim) только о том, на что он говорит «да».

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Openness: high range (raw 4.2 of 5; 81st percentile; IPIP-NEO-120, internet norms 2014; August 2026).",
 "horizon": "foundation", "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "holder app", "method": "one result line of as-01 restated with its norm group"},
 "assertedBy": "subject", "recordedAt": "2026-09-06T20:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "I get absorbed in new ideas and need a quiet hour to think them through.",
 "horizon": "foundation", "evidence": [{"ref": "as-01", "kind": "instrument"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- **Строка результата, которую человек принимает** (`c-01`): грань `disposition`, предикат `assessed-trait`, `origin: "derived"`, `derivedFrom` — AssessmentRecord, `generatedBy.method` объясняет, как строка пересказана (CL-3). Оставьте в тексте методику, нормативную группу и дату.
- **Та же склонность своими словами человека** (`c-02`): предикат `self-described-tendency`, `origin: "declared"` и `evidence` со ссылкой на результат, вид основания `instrument`.
- На строку, которую человек не узнаёт, утверждение не пишется. Для неё — проверка соответствия (шаг 5).

Линза также поддерживает «выбор предпочтений в общении, которые человек затем сам формулирует». Такое предпочтение пишется как обычное утверждение, **без** ссылки на результат: ссылка подняла бы его до особой категории (C3) и закрыла бы от рабочего ассистента. Если человек хочет сохранить связь, добавьте связь (Relation): она не поднимает уровень записей, которые соединяет.

```json
{"id": "c-03", "facet": "preference", "predicate": "format",
 "text": "Send the agenda the day before; I prepare better in writing than on the spot.",
 "horizon": "focus", "contexts": ["work"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:10:00Z", "synthetic": true}
```

```json
{"id": "rl-01", "rel": "supports", "from": "as-01", "to": "c-03",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:11:00Z",
 "note": "Kesi chose this preference after reading the score profile.", "synthetic": true}
```

**Кто видит:** `c-01` и `c-02` — особая категория (они ссылаются на результат) и уходят только по разрешению, которое называет их идентификаторы или категорию `mental-health`; селектор `lenses` до них не дотягивается (§6). `c-03` — предпочтение личного уровня: до него дотягивается разрешение с селектором по грани `preference`. `rl-01` — особая категория, как и результат, на который она ссылается.

### Шаг 5. Прочтите недавние эпизоды через линзу

Инструмент описания `big-five.fit-check` сравнивает одну шкалу с тремя недавними эпизодами и отмечает, подходит она или нет. Его результат — интерпретация (Interpretation).

1. Запишите в `episodes` эпизоды, о которых рассказывает человек, если их там ещё нет. Держите то, что произошло, отдельно от того, как это понималось. В `contexts` — коды из шага 0.

```json
{"id": "ep-01", "title": "Team workshop", "occurred": {"start": "2026-08-27", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-08-27T19:00:00Z", "addedAt": "2026-08-27T19:00:00Z",
               "accountKind": "in-the-moment", "happened": "Led a two-hour team workshop and did most of the talking.",
               "didOrTried": "Prepared written notes the evening before."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-27T19:00:00Z", "synthetic": true}
```

У `ep-02` (ужин со старыми друзьями, `"contexts": ["friends"]`) и `ep-03` (звонок клиенту, `"contexts": ["work"]`) те же поля.

2. Собственная проверка соответствия у человека — его интерпретация с `stance: "lens-reading"` и линзой:

```json
{"id": "in-01", "about": ["as-01", "ep-01", "ep-02", "ep-03"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"},
 "text": "Fit check, Extraversion: the low score fits the dinner, not the two work episodes.",
 "facets": ["disposition"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T19:30:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

3. Вашему прочтению как агента нужно разрешение, которое даёт вам `suggest` и `infer` и называет линзу (I5, INF-1), и, если у человека есть действующее принятие линзы, его `agentInterpretation` не `off`; при `ask-first` человек сказал «да» на этот раз. Нужны основания, то, что не сходится, не меньше двух альтернатив, из которых хотя бы одна не психологическая, и пределы (I4):

```json
{"id": "in-02", "about": ["ep-01", "ep-03"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "adoption": "la-01",
 "text": "At work you may speak up because the role asks for it; the low Extraversion score may describe what you choose when no role is set.",
 "causal": "hypothesized",
 "grounds": [{"ref": "ep-01", "kind": "evidence"}, {"ref": "ep-03", "kind": "evidence"}, {"ref": "as-01", "kind": "instrument"}],
 "counterEvidence": [{"ref": "ep-02", "kind": "evidence", "note": "Left early where no role was set."}],
 "alternatives": [
   {"text": "Both work episodes were prepared in writing the day before.", "kind": "informational"},
   {"text": "Both work topics were ones Kesi knows well.", "kind": "situational"},
   {"text": "The dinner came at the end of a long week.", "kind": "physiological"}],
 "limits": "Three episodes and one questionnaire; a reflection aid, not a description of who Kesi is.",
 "facets": ["disposition"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-10T10:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

4. Человек отвечает на ваше прочтение записью Review. Здесь он принимает его часть — своими словами:

```json
{"id": "rv-01", "target": "in-02", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-09-12T08:00:00Z",
 "endorsedPart": "At work I speak up because the role asks for it."}
```

Пишите самое большее `causal: "hypothesized"`; агент никогда не утверждает причину (I2). Говорите о склонностях и диапазонах; никогда не используйте балл, чтобы отмести сказанное человеком.

**Кто видит:** эпизоды — чувствительный уровень, они уходят только по разрешению, которое называет вид записи или идентификатор. Прочтения — особая категория: разрешение должно называть линзу, а его правило `interpretations` должно их допускать (R-G8). Ваше прочтение остаётся `proposed` — его видят человек и вы как автор предложения, — пока человек не решит.

### Шаг 6. Практика из инструментов линзы и её исход

Если человек хочет повторять проверку соответствия, запишите её как практику (Practice) с инструментом линзы в качестве образца, а то, как она прошла, — как исход (Outcome).

```json
{"id": "pr-01", "name": "Yearly fit check",
 "description": "Take one domain and three recent episodes; note where the score fits and where it does not.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:big-five", "templateId": "big-five.fit-check"},
 "steps": ["Pick one domain", "Pick three recent episodes from different settings", "Write fit or no fit for each, in one line"],
 "duration": "PT20M", "limits": "Not a re-test; it never changes the scores.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T19:00:00Z", "synthetic": true}
```

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T21:00:00Z", "synthetic": true}
```

- У `big-five.fit-check` стоит `agentMayOffer: true`, так что вы можете её предложить — если в `uses` принятия есть `offer-practices`. Если практику записываете вы сами, используйте `source.route: "from-agent"` и свой идентификатор Party в `assertedBy`; тогда это предложение (PC-1).
- Никогда не храните утверждений о том, насколько практика действенна (PC-3). Исход — собственная оценка человека; исход от агента помечается как «оценка агента» (O-1).

**Кто видит:** практика — личного уровня, поэтому до неё дотягивается любое разрешение, чья область её покрывает, в том числе разрешение с селектором `lenses` для этой линзы (практика `from-lens` считается записью линзы). Баллов в ней нет. Исход имеет уровень своей практики.

### Шаг 7. Кто что может видеть

Без разрешения из контекста ничего не уходит. Пишите по одному разрешению на получателя и цель. В примере собеседник для рефлексии может читать записи линзы, две склонности и эпизоды и может предлагать прочтения и оценки; рабочий ассистент видит только сформулированные рабочие предпочтения.

```json
{"id": "g-01", "recordedAt": "2026-09-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:big-five"]}, {"ids": ["c-01", "c-02"]}, {"kinds": ["Episode"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "all",
 "constraints": {"expiresAt": "2027-02-26T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D",
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-01T09:00:00Z", "channel": "holder-ui"},
 "note": "Reflection only. Scores and readings never leave this companion."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-06T20:15:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["communication-adaptation"],
 "scope": {"include": [{"facets": ["preference"], "contexts": ["work"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T20:15:00Z", "channel": "holder-ui"},
 "note": "The work assistant sees stated work preferences only, never scores."}
```

- Любое разрешение, которое дотягивается до записей этой линзы или включает `infer`, использует `basis.legal: "explicit-consent"` и истекает не позже чем через 180 дней (R-G10, GR-1, GR-4). Остальные разрешения истекают не позже чем через год.
- `actions`: `read` позволяет агенту видеть; `suggest` и `infer` вместе позволяют ему писать собственные прочтения и оценки как предложения (INF-1). Получателю, который должен только читать, не давайте ни того, ни другого.
- Селектор `lenses` отдаёт каждую запись, которая несёт линзу: LensAdoption, AssessmentRecord, прочтения и любую практику `from-lens`, а не только баллы (§6). То, чего у этого получателя быть не должно, исключите по идентификатору.
- В `purposes` никогда нет запрещённых целей (§8.10). Для этой линзы это значит: никакого найма, распределения задач, оценки работы, повышения, сравнения с другими людьми и подстройки убеждения.
- `expressedBy` — то, как человек сказал «да». Ваши слова «человек согласился» согласием не являются.
- Разрешения кладутся в `grants`. Если человек хочет что-то скрыть от одного получателя, добавьте селектор `exclude` или отдельное разрешение с `"effect": "deny"`.

### Шаг 8. Проверка

Из репозитория спецификации запустите программу проверки на папку из шага 0:

```sh
python3 -B tools/check.py <папка> --level L1 --json
```

Исправьте каждую ошибку. Программа проверки никогда не печатает ваши значения. Она проверяет форму и правила, а не истинность и не согласие: значение имеет подтверждение человека на каждом шаге. Файлы хранилища она тоже не открывает, поэтому сверьте `sha256` и `size` с файлами сами командами из шага 2.

## 4. Никогда

- **Никогда для этих целей,** ни по какому разрешению: отбор персонала, распределение задач, оценка работы, решения о повышении, сравнение с другими людьми, подстройка убеждения и другие запрещённые цели (§8.10). Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required` в разрешении, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Никогда** не намекайте, что человек подходит или не подходит для работы или роли.
- **Никогда** не комментируйте аспекты «Тревожность» и «Депрессивность», если человек сам о них не заговорил.
- **Никогда** не предсказывайте по черте, что человек сделает в конкретный момент, и никогда не используйте балл, чтобы отмести сказанное человеком.
- **Никогда** не подавайте высокий или низкий балл как недостаток; никогда не подавайте результаты как клиническое состояние.
- **Никогда** не делайте оценку агента без разрешения, которое даёт вам и `suggest`, и `infer` для этой линзы, или без `person-only`. Никогда не используйте такую оценку как вход для других выводов (C-7).
- **Никогда** не переводите баллы в ярлыки другой системы: никаких буквенных типов из баллов Большой пятёрки (M-4) и никаких баллов HEXACO из баллов Большой пятёрки (M-1). Сопоставления на уровне популяции никогда не применяются, чтобы пересчитать результат одного человека. Каждая строка сопоставления между линзами в каталоге 0.1 запрещает такое использование (AR-7 его отклоняет).
- **Никогда** не храните текст вопросов, ответы (вне `ext["ohc.test-data"]`), ключи подсчёта и текст отчёта. Никогда не проводите сами NEO-PI-3 (квалификация уровня S) и BFI-2 (только некоммерческие исследования). Если человек хочет пройти опросник вместе с вами, используйте IPIP-NEO-120: его вопросы в общественном достоянии.
- **Товарные знаки:** «NEO-PI-3» — знак PAR, Inc. (в каталоге статус не проверен; `use: nominative-only`). Используйте его только как название этой методики, никогда как общий ярлык и никогда в `label` оценки. Подлинный результат NEO-PI-3 несёт уведомление из описания методики в `trademarkNotice` (шаг 3).

## 5. Разобранный пример

[examples/big-five/context.json](examples/big-five/context.json) — контекст в форме одного документа для Кеси (Kesi), вымышленного человека. Каждая запись несёт `"synthetic": true`. В нём ровно записи из §3: `la-01`, `src-01` (с файлом в хранилище), `as-01`, `as-02`, `as-03` и `rv-02`, `c-01`, `c-02`, `c-03`, `rl-01`, с `ep-01` по `ep-03`, `in-01`, `in-02` и `rv-01`, `pr-01` и `oc-01`, `g-01` и `g-02`. Фрагмент пути из §2 (`agent-suggested` с `rv-00`) и фрагмент NEO-PI-3 из шага 3 — варианты, а не часть примера; каждый проверен отдельно и проходит L1.

```sh
python3 -B tools/check.py docs/lenses/examples/big-five --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений. Ожидаемый вывод хранится в [examples/big-five/expected-check.json](examples/big-five/expected-check.json).

## 6. Что пока не укладывается

Каждый пункт записан для следующей редакции стандарта.

1. **Ограничения обращения для отдельных понятий.** Правило «не комментировать тревожность и депрессивность, пока человек сам о них не заговорил» можно соблюсти, только вынеся эти аспекты в отдельную запись (`as-02`). Ни `defaults.perConstruct`, ни отдельный результат не могут нести `handling`.
2. **Какой инструмент линзы породил запись.** `in-01` получена инструментом `big-five.fit-check`, но в интерпретации (как и в AssessmentRecord и ModelView) нет поля, чтобы это сказать; `templateId` есть только у практики.
3. **Утверждения, выведенные из результата, теряют линзу.** Селектор `lenses` дотягивается только до записей с полем `lens`. `c-01` и `c-02` приходится называть по идентификатору в каждом разрешении.
4. **Связь, которая не является свидетельством.** Предпочтение, подсказанное результатом, не может сослаться на него, не став особой категорией (C3), поэтому `rl-01` использует `supports`, а это читается как свидетельство. Кода связи «подсказано этим» нет.
5. **У оценки агента нет оснований, альтернатив и пределов.** Интерпретация агента обязана их нести (I4); AssessmentRecord с `mode: agent-inference` — не может. В `as-03` вместо этого — `derivedFrom` и `note`.
6. **Методики вне каталога.** Тест по Большой пятёрке, которого нет среди трёх перечисленных, нельзя назвать в `instrument` (AR-8), а локальных идентификаторов методик, как у локальных линз (`x-`), нет.
7. **Нормативные группы — свободный текст.** `normGroup.id` не привязан к описанию методики, поэтому две записи с одними нормами не узнать как таковые.
8. **Программа импорта пишет недопустимые записи.** *Исправлено в 0.1.0-draft.2:* `tools/import_assessment.py` пишет `standardized: {"type": "percentile", "value": …}` и только коды способов из каталога.
9. **Записи, которые агент пишет от имени человека, действуют сразу.** При `assertedBy: "subject"` и `recordedBy`, указывающем на агента, нигде не записано, что человек подтвердил текст.
10. **`cross-lens-estimate` недостижим.** У каждого сопоставления между линзами в каталоге 0.1 есть `forbiddenUse` или закрытый `rowStatus`, а обязательный текст `scope` гласит «never for converting one person's result». Способ существует, но ни одна запись не может им воспользоваться.
11. **У большинства аспектов нет идентификатора понятия.** В описании есть пять шкал и два аспекта. Остальные 28 аспектов IPIP-NEO-120 и NEO-PI-3 и 15 аспектов BFI-2 нельзя записать с идентификаторами, которые «берутся из понятий линзы».
12. **Идентификаторы понятий не проверяются.** Программа проверки принимает в результате любую строку `construct`, даже из другой линзы (`hexaco/H` в записи Большой пятёрки проходит), хотя LENSES.md §5 требует идентификаторов из линзы, а M-1 запрещает отождествлять понятия разных линз.
13. **У `uses` нет силы.** Ни одно правило не связывает запись с действующим принятием её линзы или с `uses` этого принятия. AssessmentRecord, прочтения самого человека и оценки агента проходят L1 при `uses: ["store-results"]` и даже вовсе без LensAdoption; на принятие смотрит только I5 и только для прочтений, автор которых — не сам человек.
14. **Знаки в описаниях методик не учитываются.** Знак NEO-PI-3 и его уведомление лежат в описании методики, а не в `ip.marks` линзы (там пусто). Подлинный импорт NEO-PI-3 без `trademarkNotice` проходит, как и оценка агента с меткой «NEO-PI-3 Extraversion»: проверка меток в AR-2 читает только знаки линзы.
15. **`form` и `lensVariant` не проверяются.** `form: "999"` и `lensVariant: "no-such-variant"` проходят L1. AR-8 проверяет только идентификатор методики, но не `forms` её описания и не `variants` линзы.
16. **У `instrument.version` нет определённого смысла, а описания методик нельзя закрепить.** Не сказано, что хранит поле — издание издателя («2014») или версию записи каталога («0.1.0»); а манифест закрепляет по `sha256` линзы, но не методики, так что потом нельзя узнать, какое описание (с его `neverStore`, знаками и условиями) действовало.
17. **Просьбу человека о предложении нельзя записать.** `adoption.suggestionRequires` говорит, когда предложение обычно уместно (после того как человек попросил способы описать склонности); в LensAdoption нет поля для этой просьбы, поэтому она живёт в `note`. Можно ли вам предлагать, решает разрешение человека (`suggest`); LA-1 проверяет только, что допускает сам человек.
18. **Файлы хранилища никогда не сверяются со своим описанием.** Программа проверки не читает файлы хранилища (`vaultContentRead: false`). SR-3 проверяет только совпадение `sha256` с именем в `vaultPath`, поэтому `size` 999 для файла в 379 байт, `sha256`, который не является хешем файла (и так же записан в `vaultPath`), или файл, которого вообще нет, проходят L1.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
