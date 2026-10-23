# HEXACO: как перенести материал человека в OHC

**Рецепт · линза `urn:ohc:lens:hexaco` 0.2.0 · OHC 0.1.0-draft.2 · информативный · 12 октября 2026**

Этот рецепт по шагам превращает материал человека по HEXACO (чаще всего лист с баллами HEXACO-PI-R от коуча, собственные слова человека и замечание коуча) в записи OHC, оставляя шкалу «Честность-скромность» у самого человека и не сохраняя ничего, что запрещают линза или методика.

Описание линзы — `spec/lenses/hexaco.lens.json` (`descriptorStatus: draft`, `legalReviewNeeded: true`). Это полное описание, а не заготовка (stub), поэтому доступны все шаги ниже. Прочитайте его до начала: его `mentalModel`, `ip` и `defaults` — это факты и рекомендации, которые применяет рецепт. HEXACO — не Большая пятёрка с добавленным шестым фактором: несколько шкал определены иначе, и записи HEXACO никогда не заимствуют идентификаторы или баллы Большой пятёрки.

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:hexaco-basic`](../../spec/playbooks/hexaco-basic.playbook.json) («HEXACO: базовые способы работы», редакция OHC), для таких ситуаций: планирование предстоящей недели; выбор между вариантами; обратная связь другому человеку; разбор того, что произошло. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Пример | Куда это идёт |
|---|---|---|
| Самоописание в разговоре | «Я держу слово, даже когда мне это дорого обходится.» | Утверждение (Claim) словами человека (шаг 4). Без AssessmentRecord: слова — не балл. |
| Отчёт методики, который есть у человека | Лист с баллами HEXACO-PI-R (форма на 60, 100 или 200 вопросов) от коуча, с курса или из исследования | Лист — источник (Source, шаг 2); баллы — записи AssessmentRecord (шаг 3). |
| Заметки или замечания из коучинга, обучения или терапии, где использовался HEXACO | Замечание коуча на сессии, которое человек записал | Путь принятия линзы `inherited-from-practice` (шаг 1); материал коуча — источник под охраной коуча (шаг 2); замечание, которое человек хочет сохранить, — интерпретация (Interpretation) с авторством коуча (шаг 5). |
| Прочтение агента | Собеседника просят угадать баллы человека | Когда человек сам просит, по разрешению, которое даёт агенту и `suggest`, и `infer` и называет линзу. См. шаг 3b. |

В линзе одна методика: `urn:ohc:instrument:hexaco-pi-r` (формы `60`, `100`, `200`; авторское право на вопросы — у Кибома Ли и Майкла Эштона; скачивание бесплатно только для некоммерческих академических исследований; проведение онлайн — только на страницах под паролем или закрытых от поиска; для неакадемического использования нужно связаться с авторами). Подсчёт открыт.

## 2. Прежде чем начать

**Путь принятия линзы.** Выберите тот, что соответствует тому, как человек пришёл к линзе. Он записывается в `LensAdoption.route`.

| Путь | Когда | Что он меняет |
|---|---|---|
| `self-chosen` | Человек сам выбрал линзу. | Принятие действует сразу после записи. |
| `agent-suggested` | Линзу предложили вы — по разрешению, которое это позволяет (`suggest` с селектором, называющим линзу). `adoption.suggestionRequires` в описании говорит, когда это обычно уместно: после того как человек сам попросил способы описать свои склонности. | Добавьте `suggestedBy` с вашим идентификатором Party. Принятие остаётся `proposed`, пока человек не допустит его записью Review с `admit` (LA-1); см. фрагмент ниже. |
| `inherited-from-practice` | Линза пришла от коуча, преподавателя или терапевта человека (`adoption.inheritanceRoles`). Пример этого рецепта идёт этим путём. | Добавьте блок `practice`: `role`, `practitioner` (идентификатор Party), `relationship`, `since` и `releaseRef` (источник с разрешением специалиста) — всякий раз, когда хранится источник, автор которого специалист или который у него на хранении, включая сам лист с баллами (LA-3). Задайте `confidentiality` и `onEnd`. Принятие линзы не даёт специалисту никакого доступа (LA-2); доступ даёт только разрешение (шаг 7). |
| `imported` | Принятие создала программа импорта из отчёта. | Принятие остаётся `proposed`, пока человек его не допустит; так же и каждый AssessmentRecord из того же прогона импорта (LA-5). |

**Путь `agent-suggested` в записях.** Принятие остаётся записью человека (`assertedBy: "subject"`); добавьте `"suggestedBy": "<ваш идентификатор Party>"` и запишите просьбу человека в `note` его словами (в OHC 0.1 для неё нет поля; §6). Затем допуск человека кладётся в `reviews`, и его `recordedAt` должен быть раньше любого прочтения через линзу; допускает только сам человек (LA-1):

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-06-05T18:01:00Z"}
```

**Когда работа со специалистом заканчивается.** Человек пишет новое LensAdoption, которое заменяет (`supersedes`) прежнее, с `practice.relationship: "ended"` и выбранным `onEnd` (`keep-read-only`, `archive-person-only` или `erase`). Пока `onEnd` равно `ask`, принятие приостановлено до решения человека. Разрешение коуча само не заканчивается: если человек этого хочет, отзовите его записью Review `{"id": "<новый идентификатор>", "target": "<идентификатор разрешения>", "action": "withdraw-grant", "by": "subject", "recordedAt": "<сейчас>"}`.

**Согласие.** Спрашивайте перед каждым шагом и зачитывайте каждую запись перед сохранением. Человек может остановиться на любом шаге. Для ваших собственных прочтений и оценок нужно отдельное «да»: разрешение, которое даёт агенту и `suggest`, и `infer`, с `basis.legal: explicit-consent` (INF-1, R-G11). Разрешение с `infer`, но без `suggest` не проходит INF-1.

**Кто пишет.** Собственный держатель человека пишет записи человека с `assertedBy: "subject"`. Запись о том, что коуч посчитал или сказал, приписывается коучу (`assertedBy: "p-01"`), а записывает её человек (`recordedBy: "subject"`); она остаётся `proposed`, пока человек её не допустит. Если вы агент, вы пишете только свои прочтения и оценки (`assertedBy` — ваш идентификатор Party, `origin: "inferred"`, `underGrant` и `purpose` называют разрешение с `suggest` и `infer`) или — по разрешению с `write` — подтверждённые утверждения самого человека, с `recordedBy`, равным вашему идентификатору Party.

**Умолчания этой линзы** (`defaults` в описании):

- `sensitivity: "special"`: любая запись этой линзы относится к особой категории. Разрешение дотягивается до неё, только если называет её идентификатор, её линзу или её категорию, при явно выраженном согласии (R-G3).
- `categories: ["mental-health"]`. Понятия `hexaco/E`, `hexaco/E/fearfulness` и `hexaco/E/anxiety` сами несут `mental-health`.
- `reviewAfter: "P3Y"`.
- Ограничения обращения. Описание запрещает помощнику обсуждать «Честность-скромность» с кем-либо, кроме самого человека, и комментировать аспекты «Тревожность» и «Боязливость», если человек сам о них не заговорил. Храните «Честность-скромность» в отдельном AssessmentRecord с ограничением `no-forward` (шаг 3). Селектор `lenses` дотягивается и до этой записи, поэтому в каждом разрешении: исключите её по идентификатору (`"exclude": [{"ids": ["as-02", "in-01"]}]`), если только человек не просит, чтобы этот получатель её имел; тогда ещё и назовите её по идентификатору в `include`, чтобы по разрешению было видно, что это выбор человека (шаг 7). Если человек сохраняет аспекты эмоциональности, дайте «Тревожности» и «Боязливости» отдельную запись с ограничением `subject-initiated-only`.

**Что не хранится никогда.**

- Текст вопросов HEXACO-PI-R (`ip.restrictions`) и ответы на них. Единственное исключение для ответов — собственные тестовые данные человека в `ext["ohc.test-data"]` с ограничением `person-only` и признаком валидности `test-data-personal-only` (AR-3).
- Текст отчёта: копируйте числа, а не фразы.
- Идентификаторы и баллы Большой пятёрки и ярлыки типов, выведенные из баллов HEXACO (M-1, M-4).
- Балл как оценка человека. Низкий балл по «Честности-скромности» никогда не приговор характеру и никогда не мера надёжности.

## 3. Шаги

Каждый шаг говорит, что сделать, какую запись написать, даёт фрагмент JSON, который проходит проверку по `spec/schema/*.schema.json`, и говорит, кто видит запись по умолчанию. Фрагменты — это записи разобранного примера (§5) в форме одного документа: каждая кладётся в массив, названный в шаге. **По умолчанию никто, кроме самого человека, ничего не видит** (R-G1); это меняется только в шаге 7.

### Шаг 0. Файл и его папка

Один контекст — одна папка. Все записи лежат в одном файле, `context.json`. Исходные файлы (листы с баллами, заметки, разрешения специалистов) лежат рядом с ним в `vault/`. Программу проверки запускают на папку (шаг 8).

```text
<папка>/
  context.json
  vault/81/8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b.md
  vault/cf/cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8.json
```

Начните `context.json` с корня. Вот корневые поля разобранного примера:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:sefa:hexaco", "version": "2026-06-12.1",
 "subject": {"id": "urn:ohc:example:sefa", "displayName": "Sefa (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-06-05T18:00:00Z",
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` и `subject` обязательны (`spec/schema/context.schema.json`).
- `id` и `subject.id`: для настоящего человека — `urn:uuid:`, который вы создаёте сами, никогда не имя и не почта. `urn:ohc:example:<имя>[:<контекст>]` — только для примеров.
- `version` — любой текст на ваш выбор; меняйте его при каждом изменении файла.
- `synthetic: true` — только в примерах: и в корне, и в каждой записи. Для настоящего человека это поле не пишется.
- В тот же объект добавьте `conformance`, `parties` и `lenses` (шаг 1), затем массивы, которые заполняет этот рецепт: `lensAdoptions` (шаг 1), `sources` (2), `assessments` (3, 3b), `claims` (4), `episodes` и `interpretations` (5), `reviews` (3, 3b, 5), `practices` и `outcomes` (6, если нужны), `grants` (7). Массив, которым вы не пользуетесь, не пишите.
- **Коды для `contexts`** (в любой записи, где есть это поле): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`. Всё остальное должно быть локальным кодом `x-<пространство>:<код>`, объявленным в корневом `vocabulary`, например `"vocabulary": {"x-sefa:course": {"definition": "Evening course on personality"}}`. Любое другое значение не проходит S-3.

### Шаг 1. Закрепите линзу и запишите её принятие

Спросите, как человек пришёл к линзе, кто его коуч и что он хочет сохранить. Затем объявите модули, перечислите стороны (Party), закрепите линзу (`sha256` прочитанного файла описания: `shasum -a 256 spec/lenses/hexaco.lens.json`) и запишите LensAdoption в `lensAdoptions`.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
],
"lenses": [{"id": "urn:ohc:lens:hexaco", "version": "0.2.0", "sha256": "37e5ebddae7e8c9b6dc571d5b78cb9f056312db9d8bb2753bb5e640ecfa92a0a"}]
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-05-01", "releaseRef": "src-02"},
 "confidentiality": "practitioner-scope",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject", "p-01"], "agentInterpretation": "allowed",
 "representationPreference": "hexaco.score-profile", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

- `practice.role`: `coach`, `teacher` или `therapist` (`inheritanceRoles` линзы).
- `confidentiality: "practitioner-scope"`: материал коучинга остаётся в пределах этих отношений. Для терапевта используйте `therapy-confidential`; это закрепляет особую категорию и ограничение `person-only` за каждой записью, которая ссылается на принятие (LA-4).
- `uses` записывает, на что человек согласился: `speak-in-lens`, `store-results`, `interpret`, `offer-practices`, `recall`. OHC 0.1 этого не проверяет: ни одно правило не связывает запись с `uses`. Поэтому держаться этого должны вы и держатель сами (§6). Сефа не соглашалась на `offer-practices`, поэтому никто не предлагает ей инструменты линзы.
- `interpretationAuthors` — кто из людей, кроме самого человека, может писать прочтения через линзу: здесь коуч. Агентов этот список не касается: агент читает через линзу по разрешению с `infer`, которое её называет (I5).
- `agentInterpretation: "allowed"` позволяет агенту с таким разрешением читать через линзу; здесь это собеседник по `g-02`. С 0.1.0-draft.2 это поле касается только авторов-агентов и программ, поэтому `off` не пустил бы агентов, но замечание коуча в шаге 5 по-прежнему проходило бы (I5).
- `onEnd: "ask"`: см. «Когда работа со специалистом заканчивается» в §2.
- `handling: ["no-forward"]` на самом принятии: оно называет коуча и отношения с ним. Разрешение с селектором `lenses` для этой линзы отдаёт и само принятие (и любую практику `from-lens`), а не только баллы. Получатель не должен передавать его дальше; если получатель вообще не должен его видеть, исключите `la-01` по идентификатору в его разрешении.

**Кто видит:** только человек. Принятие линзы не даёт коучу доступа.

### Шаг 2. Сохраните разрешение коуча и лист с баллами как источники

Положите оба файла в хранилище источников. Три значения вычисляйте по самому файлу, никогда не набирайте их вручную:

- `sha256` — SHA-256 байтов файла строчными шестнадцатеричными символами (`shasum -a 256 <файл>` или `sha256sum <файл>`);
- `size` — длина файла в байтах (`wc -c < <файл>`);
- `vaultPath` — `vault/<первые два символа sha256>/<sha256>.<расширение>`, относительно папки, где лежит `context.json`.

Программа проверки только сверяет `sha256` с именем в `vaultPath` (SR-3). Файлы хранилища она не открывает (`vaultContentRead: false`), поэтому неверный хеш, неверный размер или отсутствующий файл проходят незамеченными (§6).

Сначала разрешение коуча — на него ссылаются принятие линзы и лист с баллами; затем сам лист, под охраной коуча.

```json
{"id": "src-02", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/81/8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b.md"},
             "sha256": "8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b",
             "mediaType": "text/markdown", "size": 169},
 "capturedAt": "2026-06-03T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"], "maxRelease": "index",
 "retention": {"eraseOnRequest": true}, "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T17:50:00Z",
 "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/cf/cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8.json"},
             "sha256": "cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8",
             "mediaType": "application/json", "size": 511},
 "capturedAt": "2026-06-03T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"],
 "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-02"},
 "maxRelease": "index",
 "retention": {"eraseOnRequest": true}, "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T17:55:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `custody` называет коуча хранителем, а разрешение — `releaseRef`. `custody.confidentiality` зависит от специалиста:

  | Специалист | `custody.confidentiality` | `contexts` |
  |---|---|---|
  | коуч | `coaching`: получатель получает самое большее `excerpt` при разрешении специалиста и `index` без него (§15.3) | `["coaching"]` |
  | терапевт | `therapy`: самое большее `summary` при разрешении и `index` без него | `["therapy"]` |
  | преподаватель | `none`: в OHC 0.1 нет кода для обучения (§6). Не берите `coaching` взаймы; файл защищает `maxRelease: "index"`. | `["learning"]` |

  В любом случае оставьте `maxRelease: "index"`.
- Если человек проходил опросник сам (в исследовании), не пишите `custody`, а в `authorship.author` укажите сторону (Party), выдавшую лист.
- Никогда не вставляйте текст листа или заметок в `summary`, `title` или `note` (SR-4).

**Кто видит:** человек — полностью. Получатель — самое большее на уровне `index` и только если разрешение называет этот источник.

### Шаг 3. Запишите баллы как AssessmentRecord

Переносите только числа и только то, что напечатано на листе. «Честность-скромность» с её аспектами вынесите в отдельную запись.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:hexaco-pi-r", "form": "100"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-06-03", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/E", "label": "Emotionality", "raw": 3.0, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/X", "label": "eXtraversion", "raw": 3.4, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/A", "label": "Agreeableness (versus Anger)", "raw": 3.2, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/C", "label": "Conscientiousness", "raw": 4.1, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/O", "label": "Openness to Experience", "raw": 3.6, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/altruism", "label": "Altruism (interstitial scale)", "raw": 3.8, "rawRange": [1, 5]}],
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "coach's score sheet", "method": "means of keyed items on a 1-5 scale, with the authors' published scoring"},
 "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-05T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["coaching"],
 "note": "The score sheet names no norm group; raw means only.", "synthetic": true}
```

```json
{"id": "as-02", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:hexaco-pi-r", "form": "100"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-06-03", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/H", "label": "Honesty-Humility", "raw": 3.9, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/sincerity", "label": "Sincerity (facet)", "raw": 4.0, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/fairness", "label": "Fairness (facet)", "raw": 4.5, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/greed-avoidance", "label": "Greed Avoidance (facet)", "raw": 3.2, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/modesty", "label": "Modesty (facet)", "raw": 3.9, "rawRange": [1, 5]}],
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "coach's score sheet", "method": "means of keyed items on a 1-5 scale, with the authors' published scoring"},
 "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-05T18:06:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "contexts": ["coaching"],
 "note": "Honesty-Humility kept apart: it is never shown to anyone but Sefa unless she names it in a grant.",
 "synthetic": true}
```

Лист считал коуч, поэтому обе записи — утверждение коуча (`assertedBy: "p-01"`), записанное человеком. Они остаются `proposed`, пока человек сам их не допустит (R-A1):

```json
{"id": "rv-01", "target": ["as-01", "as-02"], "action": "admit", "by": "subject", "recordedAt": "2026-06-05T18:10:00Z"}
```

Поля заполняются так:

| Поле | Значение |
|---|---|
| `lens` | `{"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}` |
| `instrument` | `{"id": "urn:ohc:instrument:hexaco-pi-r", "form": "60" \| "100" \| "200"}` — форма, напечатанная на листе. Форма на 60 вопросов — часть формы на 100. `version` пишите, только если на листе напечатано издание (не `0.1.0` записи каталога); на этом листе его нет. Программа проверки не проверяет `form`, поэтому копируйте её точно (§6). |
| `mode` и `origin` (AR-1) | Человек сам отвечал на опросник: `self-report-instrument` с `origin: "derived"`, `derivedFrom` (источник) и `generatedBy` с `method`. Человека оценивал другой человек: `observer-report` с `assessedBy` (идентификатор Party оценивавшего) и `raterRelationship`. |
| `results` | По одному `dimension-score` на каждое понятие, напечатанное на листе, с идентификаторами из описания. Шесть шкал: `hexaco/H`, `hexaco/E`, `hexaco/X`, `hexaco/A`, `hexaco/C`, `hexaco/O`. Их 24 аспекта: `hexaco/H/sincerity`, `hexaco/H/fairness`, `hexaco/H/greed-avoidance`, `hexaco/H/modesty`; `hexaco/E/fearfulness`, `hexaco/E/anxiety`, `hexaco/E/dependence`, `hexaco/E/sentimentality`; `hexaco/X/social-self-esteem`, `hexaco/X/social-boldness`, `hexaco/X/sociability`, `hexaco/X/liveliness`; `hexaco/A/forgivingness`, `hexaco/A/gentleness`, `hexaco/A/flexibility`, `hexaco/A/patience`; `hexaco/C/organization`, `hexaco/C/diligence`, `hexaco/C/perfectionism`, `hexaco/C/prudence`; `hexaco/O/aesthetic-appreciation`, `hexaco/O/inquisitiveness`, `hexaco/O/creativity`, `hexaco/O/unconventionality`. Промежуточная шкала: `hexaco/altruism`. Записывайте только то, что напечатано: лист формы на 60 вопросов обычно даёт только шесть шкал, без аспектов и без альтруизма. Никогда не идентификатор `big-five/…`. `raw` и `rawRange` — как напечатано; `standardized` — только если лист его даёт. |
| `normGroup` | Нормативная выборка, которую называет лист. Этот лист её не называет, поэтому `normGroup` не пишется, а `note` говорит об этом; при каждом показе баллов говорите «нормативной группы нет». |
| `reviewAfter`, `sensitivity`, `categories` | `P3Y`, `special`, `["mental-health"]`. |
| `handling` | `no-forward` на записи «Честности-скромности». `subject-initiated-only` на записи с аспектами «Тревожность» или «Боязливость», если человек их хранит (Сефа — нет). |

**Кто видит:** человек. Получатель — только если разрешение называет линзу, категорию или идентификатор при явно выраженном согласии. `as-02` к тому же несёт `no-forward`: получатель, которому она досталась, никому её не передаёт.

### Шаг 3b. Только если человек просит: оценка агента

Можно ли вам делать оценку, решает разрешение человека: оно должно давать вам и `suggest`, и `infer` и называть линзу (`g-02` в шаге 7). В примере Сефа просит собеседника примерно угадать её экстраверсию, чтобы сравнить с листом коуча. Оценка держится на эпизодах, о которых рассказал человек (`ep-02`, шаг 5).

```json
{"id": "as-03", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "mode": "agent-inference", "assessedBy": "a-01",
 "administeredAt": {"start": "2026-06-20", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/X", "raw": 2.8, "rawRange": [1, 5]}],
 "validityFlags": ["agent-estimate-not-validated"], "validityCeiling": "agent-estimate-not-validated",
 "derivedFrom": ["ep-02"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-06-20T10:00:00Z",
 "underGrant": "g-02", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["person-only"],
 "note": "Asked for by Sefa: a rough guess from one episode, to compare with the coach's sheet.",
 "synthetic": true}
```

Сефа её отклоняет; оценка остаётся в истории и не используется. Чтобы сохранить оценку, человек пишет `"action": "admit"`. Любая из этих записей Review кладётся в `reviews`, и пишет её только сам человек (R-A1).

```json
{"id": "rv-03", "target": "as-03", "action": "decline", "by": "subject", "recordedAt": "2026-06-21T08:00:00Z",
 "note": "One evening says little; I keep the coach's sheet."}
```

- AR-2 требует всё сразу: ограничение `person-only`, признак и потолок `agent-estimate-not-validated`, никакого `trademarkNotice` и никаких фирменных обозначений.
- `derivedFrom` называет эпизоды, на которых держится догадка. `label` не пишите: это догадка, а не измеренный результат. `instrument` тоже нет.
- INF-1 требует, чтобы разрешение из `underGrant` было выдано вам, содержало `suggest` **и** `infer`, называло `purpose`, дотягивалось до записи (здесь — через селектор `lenses`) и действовало в момент `recordedAt`.
- Никогда не оценивайте «Честность-скромность» (`hexaco/H` или её аспекты) ни для кого, кроме самого человека, который об этом попросил. OHC 0.1 не умеет запретить оценку одного понятия; программа проверки такую оценку примет (§6).

**Кто видит:** всегда только человек (`person-only`); даже вам она в проекции не возвращается.

### Шаг 4. Утверждения, которые человек принимает

Покажите профиль баллов: сырой балл и диапазон, а также нормативную группу или слова «нормативной группы нет». Спросите, какие склонности человек узнаёт и где. Пишите утверждение (Claim) только о том, на что он говорит «да».

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Conscientiousness: raw 4.1 on a 1-5 scale (HEXACO-PI-R, 100-item self-report, scored by my coach, June 2026; no norm group).",
 "horizon": "foundation", "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "holder app", "method": "one result line of as-01 restated with instrument, form and date"},
 "assertedBy": "subject", "recordedAt": "2026-06-08T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "I plan ahead and finish what I promise, sometimes to the point of checking things twice.",
 "horizon": "foundation", "evidence": [{"ref": "as-01", "kind": "instrument"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-08T19:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Строка результата, которую человек принимает (`c-01`): грань `disposition`, предикат `assessed-trait`, `origin: "derived"`, `derivedFrom` — AssessmentRecord, `generatedBy.method` (CL-3).
- Та же склонность словами человека (`c-02`): предикат `self-described-tendency`, `origin: "declared"`, `evidence` с видом основания `instrument`.
- Прежде чем писать любое утверждение о «Честности-скромности», спросите отдельно и дайте такому утверждению ограничение `no-forward`. Сефа такого не писала.
- Предпочтение, которое человек выбирает, посмотрев профиль (например, как он хочет получать обратную связь), — обычное утверждение `preference` **без** ссылки на результат, чтобы оно не стало особой категорией (C3).

**Кто видит:** оба утверждения — особая категория (они ссылаются на результат) и уходят только по разрешению, которое называет их идентификаторы или категорию `mental-health`; селектор `lenses` до них не дотягивается (§6).

### Шаг 5. Прочтения через линзу: проверка соответствия у человека и замечание коуча

Инструмент описания `hexaco.fit-check` сравнивает одну шкалу с тремя недавними эпизодами и отмечает, подходит она или нет; его результат — интерпретация. Задайте вопросы из описания: «Где вы узнаёте честность и скромность в том, как поступаете?» и «Где балл не совпадает с вашим опытом?»

1. Запишите эпизоды, о которых рассказывает человек. В `contexts` — коды из шага 0.

```json
{"id": "ep-01", "title": "Quote for a new client", "occurred": {"start": "2026-06-09", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-06-09T18:00:00Z", "addedAt": "2026-06-09T18:00:00Z",
               "accountKind": "in-the-moment", "happened": "Sent a new client a quote at my usual rate, although a colleague suggested doubling it.",
               "understandingThen": "The usual rate is what the work is worth."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-09T18:00:00Z", "synthetic": true}
```

```json
{"id": "ep-02", "title": "Client evening", "occurred": {"start": "2026-06-16", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-06-16T22:00:00Z", "addedAt": "2026-06-16T22:00:00Z",
               "accountKind": "in-the-moment", "happened": "Went to a client evening, talked with two people I already knew and left after an hour."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-16T22:00:00Z", "synthetic": true}
```

2. Проверка соответствия у человека. Она о «Честности-скромности», поэтому несёт `no-forward`, как и запись, которую она читает; OHC не копирует ограничения за вас (§6).

```json
{"id": "in-01", "about": ["as-02", "ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "text": "Fit check, Honesty-Humility: the Fairness facet fits this quote; Greed Avoidance I am less sure of.",
 "facets": ["disposition"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-09T18:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

3. Замечание коуча, которое человек хочет сохранить, — интерпретация коуча, записанная человеком. Её автор — не сам человек, поэтому нужны `adoption`, `epistemic: "hypothesis"`, основания, не меньше двух альтернатив (одна не психологическая) и пределы (I1, I4, I5). Если альтернатив не дал коуч, скажите в `limits`, кто их добавил.

```json
{"id": "in-02", "about": ["as-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}, "adoption": "la-01",
 "text": "High Conscientiousness with middling Agreeableness may be why you take over colleagues' unfinished tasks instead of asking them.",
 "causal": "hypothesized",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The team is one person short this quarter.", "kind": "situational"},
   {"text": "Nobody else has access to the client files.", "kind": "informational"}],
 "limits": "A coach's remark in one session, written down by Sefa the same evening; the two alternatives are Sefa's.",
 "facets": ["disposition"], "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-10T20:00:00Z",
 "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

4. Человек решает, что делать с замечанием коуча:

```json
{"id": "rv-02", "target": "in-02", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-06-11T08:00:00Z",
 "endorsedPart": "I do take over unfinished tasks at work."}
```

Никогда не пишите прочтений, где «Честность-скромность» — моральный приговор или мера надёжности. Агент пишет прочтения через эту линзу только по разрешению с `suggest` и `infer`, которое называет линзу, и только пока действующее принятие линзы у человека не говорит `off` (I5).

**Кто видит:** эпизоды — чувствительный уровень, они уходят только по разрешению, которое называет вид записи или идентификатор. Прочтения — особая категория: разрешение должно называть линзу (или идентификатор) и допускать интерпретации (R-G8). `in-01` к тому же несёт `no-forward`.

### Шаг 6. Практики

У линзы один инструмент — проверка соответствия, и её результат — интерпретация из шага 5. Сефа не ведёт практики, поэтому в примере нет записи Practice. Чтобы сделать проверку соответствия регулярной практикой, напишите Practice с `id`, собственным названием человека в `name`, `practiceKind: "reflection"`, `"source": {"route": "from-lens", "lens": "urn:ohc:lens:hexaco", "templateId": "hexaco.fit-check"}`, `nonClinical: true`, `origin: "declared"`, `assertedBy: "subject"` и `recordedAt`. Каждое применение записывайте как Outcome с `id`, `"about": {"practice": "<идентификатор практики>"}`, `result` (`helped`, `partly`, `no-effect`, `worse`, `unclear` или `not-tried`), `origin: "declared"`, `assertedBy: "subject"` и `recordedAt`. Добавьте `"practices"` в `conformance.modules`. Агент предлагает проверку соответствия (`agentMayOffer: true`), только если в `uses` принятия есть `offer-practices`. Практика `from-lens` считается записью линзы: её получает каждое разрешение с селектором `lenses` для HEXACO.

### Шаг 7. Кто что может видеть

Без разрешения из контекста ничего не уходит. Коуч получает результаты для сессий, без «Честности-скромности». Собеседник может читать записи линзы — включая «Честность-скромность», потому что Сефа её называет, — две склонности и эпизоды; он может сделать оценку, когда Сефа просит, но не толкует.

```json
{"id": "g-01", "recordedAt": "2026-06-12T09:00:00Z", "grantor": "subject", "grantee": "p-01",
 "purposes": ["coaching"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:hexaco"]}],
           "exclude": [{"ids": ["as-02", "in-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2026-12-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-06-12T09:00:00Z", "channel": "holder-ui"},
 "note": "For our coaching sessions; Honesty-Humility stays with me."}
```

```json
{"id": "g-02", "recordedAt": "2026-06-12T09:05:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:hexaco"]}, {"ids": ["as-02", "in-01", "c-01", "c-02"]}, {"kinds": ["Episode"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2026-12-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D",
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-06-12T09:05:00Z", "channel": "holder-ui"},
 "note": "The companion may talk with me in HEXACO terms, including Honesty-Humility, and make a rough estimate when I ask for one; it does not interpret through the lens."}
```

- Любое разрешение, которое дотягивается до записей этой линзы или содержит `infer`, использует `basis.legal: "explicit-consent"` и истекает не позже чем через 180 дней (R-G10, GR-1, GR-4).
- «Честность-скромность» (`as-02`, `in-01`) исключена из разрешения коуча по идентификатору. Сефа попросила, чтобы она была у собеседника, поэтому `g-02` называет оба идентификатора в `include`; уходит она с `no-forward`.
- Селектор `lenses` отдаёт каждую запись, которая несёт линзу: LensAdoption (с именем коуча и отношениями с ним), AssessmentRecord, прочтения и любую практику `from-lens`, а не только баллы (§6). То, чего у получателя быть не должно, исключите по идентификатору.
- `actions`: `suggest` и `infer` вместе позволяют собеседнику писать собственные оценки как предложения (шаг 3b). Получателю, который должен только читать, как коучу, не давайте ни того, ни другого.
- Никогда не выдавайте записи этой линзы никому в рабочей обстановке: описание предупреждает, что раскрытие «Честности-скромности» на работе грозит ущербом репутации, а все рабочие цели, которые оценивали бы человека, запрещены.
- `expressedBy` — то, как человек сказал «да»; ваши слова «человек согласился» согласием не являются.

### Шаг 8. Проверка

Из репозитория спецификации запустите программу проверки на папку из шага 0:

```sh
python3 -B tools/check.py <папка> --level L1 --json
```

Исправьте каждую ошибку. Программа проверки никогда не печатает ваши значения. Она проверяет форму и правила, а не истинность и не согласие. Файлы хранилища она тоже не открывает, поэтому сверьте `sha256` и `size` с файлами сами командами из шага 2.

## 4. Никогда

- **Никогда для этих целей,** ни по какому разрешению: отбор персонала, распределение задач, оценка работы, решения о повышении, сравнение с другими людьми, подстройка убеждения и другие запрещённые цели (§8.10). Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required` в разрешении, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Никогда** не считайте «Честность-скромность» мерой надёжности или морального облика и никогда не обсуждайте её ни с кем, кроме самого человека.
- **Никогда** не комментируйте аспекты «Тревожность» и «Боязливость», если человек сам о них не заговорил.
- **Никогда** не намекайте, что человек подходит или не подходит для работы или роли; никогда не подавайте результаты как клиническое состояние; никогда не предсказывайте по черте отдельный момент.
- **Никогда** не переводите баллы HEXACO в баллы Большой пятёрки и никогда не объявляйте идентификатор HEXACO равным идентификатору Большой пятёрки (M-1). Строка каталога `hexaco--big-five--ashton-lee-2007` — это `corresponds` с `rowStatus: not-identity`; она никогда не даст оценки через другую линзу (AR-7).
- **Никогда** не храните текст вопросов HEXACO-PI-R и текст отчёта. Никогда не проводите HEXACO-PI-R сами в продукте или сервисе: онлайн это разрешено только на страницах под паролем или закрытых от поиска, а для неакадемического использования нужно связаться с авторами.
- **Никогда** не делайте оценку агента, если человек о ней не просил, без разрешения, которое даёт вам и `suggest`, и `infer`, или без `person-only`. Никогда не оценивайте «Честность-скромность» ни для кого, кроме самого человека, который об этом попросил.
- **Товарные знаки:** для этой линзы и её методики в каталоге знаков нет.

## 5. Разобранный пример

[examples/hexaco/context.json](examples/hexaco/context.json) — контекст в форме одного документа для Сефы (Sefa), вымышленного человека, чей коуч использовал HEXACO-PI-R. Каждая запись несёт `"synthetic": true`. В нём ровно записи из §3: `la-01`, `src-02` и `src-01` (с их файлами в хранилище), `as-01`, `as-02` и `rv-01`, `as-03` и `rv-03`, `c-01` и `c-02`, `ep-01` и `ep-02`, `in-01`, `in-02` и `rv-02`, `g-01` и `g-02`. Фрагмент `agent-suggested` из §2 (`rv-00`) и строка про преподавателя из шага 2 — варианты, а не часть примера; каждый проверен отдельно и проходит L1.

```sh
python3 -B tools/check.py docs/lenses/examples/hexaco --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений. Ожидаемый вывод хранится в [examples/hexaco/expected-check.json](examples/hexaco/expected-check.json).

## 6. Что пока не укладывается

Каждый пункт записан для следующей редакции стандарта.

1. **Прочтение специалиста зависит от `agentInterpretation`.** *Исправлено в 0.1.0-draft.2:* I5 применяет `agentInterpretation` только к авторам-агентам и программам; прочтению коуча нужно, чтобы коуч был в `interpretationAuthors` действующего принятия.
2. **Альтернативы без автора.** I4 требует двух альтернатив для любого прочтения не от самого человека — и для замечания коуча, которое человек записал. Человеку приходится добавлять альтернативы, которых коуч не давал, и нигде, кроме текста `limits`, не сказано, кто их добавил.
3. **Ограничения обращения не идут по ссылкам.** C3 переносит по ссылкам уровень и категории, но не ограничения. `in-01` читает запись `as-02` с `no-forward`, и `no-forward` пришлось скопировать вручную.
4. **В описании нет ограничений обращения для отдельных понятий.** «Не обсуждать „Честность-скромность“ ни с кем, кроме человека» и «не комментировать тревожность и боязливость, пока человек сам не заговорил» соблюдаются только разделением записей; в `defaults.perConstruct` нет `handling`, а в этом описании нет и самого `perConstruct`.
5. **Условия методики — свободный текст.** «Онлайн — только на страницах под паролем или закрытых от поиска» и «для неакадемического использования свяжитесь с авторами» не имеют машиночитаемой формы, которую агент мог бы проверить, прежде чем предлагать опросник. В списке `forms` также не сказано, для самоотчёта форма или для наблюдателя.
6. **Окончание работы со специалистом не трогает его разрешение.** `onEnd` приостанавливает или завершает принятие линзы; разрешение коуча нужно отзывать отдельно, и ничто об этом не напоминает.
7. **«Нормативной группы нет» сказать нельзя.** Описание требует показывать нормативную группу с каждым баллом; если лист её не называет, запись может только не писать `normGroup` и объяснить это в `note`.
8. **Утверждения, выведенные из результата, теряют линзу.** Селектор `lenses` не дотягивается до `c-01` и `c-02`; каждое разрешение должно называть их по идентификатору.
9. **Идентификаторы понятий не проверяются.** Программа проверки приняла бы `big-five/E` в записи HEXACO — то самое отождествление, которое запрещает M-1.
10. **Программа импорта пишет недопустимые записи.** `tools/import_assessment.py` кладёт `percentile` прямо в результат `dimension-score`, а схема это отклоняет (S-3); поэтому путь `imported` требует ручной правки.
11. **У `uses` и `agentInterpretation` нет силы над результатами и оценками.** Ни одно правило не связывает запись с действующим принятием её линзы или с его `uses`. Оценка агента проходит L1 при принятии с `uses: ["store-results"]` и `agentInterpretation: off`; AssessmentRecord и прочтения самого человека проходят вовсе без LensAdoption. На принятие смотрит только I5 и только для прочтений, автор которых — не сам человек.
12. **В охране источника нет кода для обучения.** `Source.custody.confidentiality` — это `none`, `therapy`, `coaching`, `legal` или `medical`, хотя линза называет `teacher` среди ролей наследования. Материалу преподавателя приходится либо брать взаймы `coaching`, либо обходиться без потолка охраны.
13. **Нельзя ограничить оценки агента для одного понятия.** «Никогда не оценивать „Честность-скромность“ ни для кого, кроме самого человека» не записать: разрешение называет линзу, идентификатор или категорию, но не понятие, поэтому оценка агента по `hexaco/H` проходит L1 при любом разрешении с `infer` для линзы.
14. **Селектор `lenses` отдаёт больше, чем результаты.** Он совпадает с каждой записью, у которой есть поле `lens`, и с каждой практикой с `source.lens`: проекция через разрешение коуча отдаёт LensAdoption (блок практики, отношения, `onEnd`) и любую практику `from-lens`, а не только баллы. Человек, выдающий «мои результаты HEXACO», по разрешению этого не видит.
15. **Просьбу человека о предложении нельзя записать.** `adoption.suggestionRequires` говорит, когда предложение обычно уместно (после того как человек попросил способы описать склонности); в LensAdoption нет поля для этой просьбы, поэтому она живёт в `note`.
16. **`form` не проверяется, а у `instrument.version` нет определённого смысла.** `form: "999"` проходит L1 (AR-8 проверяет только идентификатор методики). Не сказано, что такое `version` — издание издателя или версия записи каталога, а описания методик нельзя закрепить по `sha256`, как линзы.
17. **Файлы хранилища никогда не сверяются со своим описанием.** Программа проверки не читает файлы хранилища (`vaultContentRead: false`); SR-3 проверяет только совпадение `sha256` с именем в `vaultPath`. Неверный `size`, неверный хеш, так же записанный в `vaultPath`, или отсутствующий файл проходят L1.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
