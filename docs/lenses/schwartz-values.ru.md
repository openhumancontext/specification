# Рецепт линзы: Теория базовых человеческих ценностей Шварца

**Рецепт · линза `urn:ohc:lens:schwartz-values` 0.2.0 · OHC 0.1.0-draft.2 · справочный документ (informative) · 12 октября 2026**

Этот рецепт по шагам показывает, как приоритеты ценностей человека (из опросника ценностей, который он прошёл, от его коуча, преподавателя или терапевта, или в его собственных словах) превращаются в записи OHC под его контролем, причём измеренный профиль и ценности, которые человек заявляет сам, хранятся раздельно.

Описание линзы — [spec/lenses/schwartz-values.lens.json](../../spec/lenses/schwartz-values.lens.json): `descriptorStatus: draft`, вид `values-circular`, уровень измерения `T2` (проверено с оговорками), онтологический статус `measured-construct`. Ценности образуют круг: соседние совместимы, противоположные конкурируют, а баллы центрируются относительно среднего самого человека. Линза помогает размышлять о выборе между ценностями и даёт язык для приоритетов, которые человек выбрал сам. Она не говорит, какие ценности правильные, не раскрывает политических или религиозных взглядов и не сравнивает людей между собой.

Каждый шаг определяют два правила:

- **Измеренный профиль — это не заявленная ценность.** Результат опросника — это AssessmentRecord. То, что человек сам называет важным для себя, — это Claim с гранью `declared-value`, его словами. Одно никогда не превращается в другое (`ip.restrictions` и `helperMustNot` в описании линзы).
- **Ценности могут раскрывать убеждения и политические взгляды.** Каждая запись этой линзы считается данными особой категории с категориями `belief` и `political`, и ничто в ней никогда не используется, чтобы выводить взгляды или подстраивать убеждение.

Форма записей описана в [SPECIFICATION.md](../../spec/SPECIFICATION.md): §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §10.4 (Tension), §13 (Event), §17 (Practice, Outcome) и §12 (Grant); схемы лежат в [spec/schema/](../../spec/schema/). Правила линз — в [LENSES.md](../../spec/LENSES.md).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:schwartz-values-basic`](../../spec/playbooks/schwartz-values-basic.playbook.json) («Ценности по Шварцу: базовые способы работы», редакция OHC), для таких ситуаций: выбор между вариантами; планирование предстоящей недели; подготовка к трудному разговору; после неудачи. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

**Принести отчёт через окно человека.** Если у записи методики в каталоге есть блок `import`, человек может принести её результат через собственное окно ([руководство](../guides/BRING-A-RESULT.ru.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). У методик этой линзы такого блока пока нет, поэтому шаги ниже записывают отчёт вручную.

## 1. Что у вас может быть

| Что есть | Использовать? | Куда идёт |
|---|---|---|
| Слова человека о том, что для него важно («для меня важно самой выбирать, как работать») | Да | Claim с гранью `declared-value` (шаг 4); никогда не AssessmentRecord |
| Результат PVQ-RR, который прошёл человек: подсчитанный программой или вручную по открытым инструкциям. PVQ-RR — единственный опросник ценностей в каталоге 0.1; его лицензия не найдена **[U]** | Да | Source (шаг 2) и AssessmentRecord с `mode: self-report-instrument` (шаг 3); подсчитанный вручную — вариант «подсчёт вручную» в шагах 1–4 |
| Результат другого опросника ценностей (более короткой или старой формы или другой анкеты) | Только отчёт, как Source | Source (шаг 2, вариант «другой опросник»): `sourceKind: "instrument-report"`, `authorship.author` — программный участник этого опросника, `sensitivity: "special"`, `categories: ["belief", "political"]`, `maxRelease: "index"`. Без AssessmentRecord: проверка отвергает инструмент, которого нет в списке линзы (AR-8). Собственные выводы человека идут в Claim с `declared-value` |
| Заметки коуча, преподавателя или терапевта, который работает с ценностями | Да, с письменным разрешением специалиста | Путь `inherited-from-practice` с `practice.releaseRef` (шаг 1, вариант), Source с разрешением и Source с заметками (шаг 2, вариант) |
| Рассказы человека о решениях и его собственное прочтение того, какие ценности тянули в разные стороны | Да | Episode и Interpretation (шаг 5); Tension между заявленными ценностями (шаг 4) |
| Прочтение агента («по вашим сообщениям видно, что вы цените традиции») | **Только по разрешению человека** | Интерпретации агента нужны `suggest` и `infer`, называющие линзу, и действующее принятие линзы не в `off` (I5). Выводить политические или религиозные взгляды не позволяет никакое разрешение (C-7, §8.10; `helperMustNot`). В примере человек не разрешает ничего из этого. |

**[U]** — отметка о степени проверенности: не проверено или известный пробел ([LENSES.md](../../spec/LENSES.md) §7.3; там же указан источник).

## 2. Прежде чем начать

### 2.1 Путь принятия линзы

Выберите путь вместе с человеком. От него зависит, кто пишет LensAdoption и когда запись начинает действовать. В шаге 1 есть полная запись для каждого пути, который используют разобранные примеры.

| Путь | Когда | Что меняется |
|---|---|---|
| `self-chosen` | Человек сам выбирает линзу; также когда он подсчитал опросник вручную. | Запись пишет сам человек: `assertedBy: "subject"`, `origin: "declared"`. Она действует сразу. Запись: шаг 1, вариант «подсчёт вручную». |
| `agent-suggested` | Человек попросил агента о способах взглянуть на то, что для него важно (условие `adoption.suggestionRequires` в описании линзы), и принял предложенную линзу. | Сначала человек даёт агенту разрешение с действием `suggest`, область которого называет линзу (такую форму имеет разрешение `g-0` из шага 6, вариант). Затем агент пишет запись по этому разрешению: `suggestedBy` и `assertedBy` — его Party id, `origin: "observed"` (`declared` отвергается правилом ENV-2), `underGrant` — id разрешения, `purpose` — одна из целей (`purposes`) этого разрешения. Запись остаётся `proposed`, пока человек сам не напишет Review `admit` (LA-1). Все три записи полностью показаны в шаге 1 [рецепта enneagram](enneagram.ru.md). |
| `inherited-from-practice` | Линза пришла от коуча, преподавателя или терапевта человека (`adoption.inheritanceRoles` в описании линзы). | Специалист — участник (Party) с `role: "practitioner"`; в записи есть блок `practice`. Если хранятся материалы встреч, сначала сохраняется разрешение специалиста — Source вида `practitioner-release`, и тот же id ставится в `practice.releaseRef` принятия линзы (LA-3) и в `custody.releaseRef` Source с заметками (SR-7). Поставьте `confidentiality` в `practitioner-scope`, а для терапевта — `therapy-confidential`, если человек так решит; тогда LA-4 делает запись принятия `person-only`, но не доходит до собственных записей человека в этой линзе, поэтому добавьте `"person-only"` и в их `handling` (раздел 6). Оставьте `onEnd` равным `ask`. Принятие линзы не даёт специалисту доступа (LA-2). Записи: шаги 1 и 2, вариант «заметки коуча». |
| `imported` | Программа подсчёта записывает принятие линзы вместе с результатом. Этот путь — в разобранном примере. | `origin: "derived"`, `derivedFrom` указывает на Source с результатом, `generatedBy` называет программу, `importedFrom` содержит идентификатор прогона `run`, общий для всех записей одного импорта; у каждой записи `importedFrom.importedAt` равно её собственному `recordedAt` (ENV-3). Принятие и AssessmentRecord с этим `run` остаются `proposed`, пока человек их не примет (LA-5). |

В примере `agentInterpretation` на любом пути равно `"off"` — это значение по умолчанию, которое человек оставляет: прочтения через эту линзу пишет только он сам (I5). Человек может это изменить.

### 2.2 Согласие

- Агент говорит языком линзы, когда человек её принял, и словами самого человека; он никогда не сравнивает ценности человека с другими людьми (`agentPosture`).
- Без разрешения (Grant) ничего не покидает контекст (R-G1). Результаты в этой линзе считаются данными особой категории: разрешение требует `basis.legal: "explicit-consent"`, должно называть записи по id, по линзе или по категории `belief` или `political` (R-G3) и действует не дольше 180 дней (GR-1).
- Импортированный результат начинает действовать только после того, как человек его посмотрел: до его Review он `proposed` и никому не выдаётся.

### 2.3 Значения по умолчанию для этой линзы

| Поле | Значение | Почему |
|---|---|---|
| `sensitivity` | `"special"` на каждой записи, которая называет линзу (LensAdoption, AssessmentRecord, Interpretation с `lens`, Practice с `source.lens`), на каждом Source с результатом, отчётом, разрешением или заметками и на каждом Claim, который ссылается на такой Source | `defaults.sensitivity` в описании линзы; AR-5; I9; правило распространения C3 |
| `categories` | `["belief", "political"]` на тех же записях | `defaults.categories` в описании линзы |
| Claim с заявленными ценностями и их Tension | `"sensitive"` (значение по умолчанию для этого вида), поднимается до `special`, только если слова человека касаются особой категории | §8.3; они не называют линзу |
| `handling` на результатах | `["no-infer", "no-leverage"]` | `no-infer`: человек не допускает профиль ни к каким выводам и сопоставлениям (M-7; у линзы к тому же `crossLensMapping: not-allowed`). `no-leverage`: никогда не используется, чтобы убеждать человека или подталкивать его (`persuasion-targeting` запрещено). |
| `reviewAfter` | `"P3Y"` | `defaults.reviewAfter` в описании линзы |
| `maxRelease` у Source | `"index"` | Получатель никогда не получает файл с результатом |

### 2.4 Что никогда не хранится

- Тексты вопросов PVQ-RR (`neverStore` в записи инструмента). Собственные ответы человека на вопросы можно хранить только как его личные данные теста: `ext["ohc.test-data"]` с ограничением `person-only` и флагом `test-data-personal-only` (AR-3). Рецепт советует не хранить их вовсе.
- Ключ подсчёта (какой вопрос относится к какой ценности) — ни в одной записи.
- Заявленная ценность, выведенная из профиля, и профиль, собранный из заявленных ценностей.
- Любое сравнение с другими людьми: нормативные группы, «выше, чем у большинства», средние по группе (M-5).
- Любые догадки о политических или религиозных взглядах человека и любые суждения о том, что ценность правильная или неправильная.

## 3. Шаги

Фрагменты кода ниже — записи из разобранных примеров (раздел 5); они проходят проверку по названным схемам. В них стоит `"synthetic": true`, потому что это примеры. Используйте непрозрачные id (`as-1`, а не `as-tradition`; W-ID1). Время — в формате RFC 3339 со смещением.

**Один раз подготовьте контекст.** Создайте каталог для контекста (дальше — *каталог контекста*) и сохраните в нём эту заготовку под именем `context.json`. Каждый шаг ниже называет массив, в который идёт его запись; порядок записей внутри массива не важен.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:odile:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:odile", "displayName": "Odile (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-15T08:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "s-01", "partyKind": "software", "label": "Values questionnaire scorer"},
   {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0",
             "sha256": "3d794f1201ae2f22a719f0e44644deaa7829626f650700ede0df9c76786f9bb2"}],
 "events": [], "sources": [], "lensAdoptions": [], "assessments": [], "reviews": [], "claims": [], "tensions": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- Поля `format`, `specVersion`, `id`, `version` и `subject` обязательны (`context.schema.json`). `holder`, `lang`, `created` и `policy` необязательны; оставьте их как в заготовке. Неиспользуемые массивы можно не писать.
- `"synthetic": true` помечает пример. В примере это поле ОБЯЗАНО стоять и в корне контекста, и на каждой содержательной записи, иначе проверка выдаёт ошибку CX-8. **Для реального человека** дайте `id` и `subject.id` вид `urn:uuid:<новый UUID>` и не ставьте `synthetic` ни в корне, ни на записях.
- `lenses[].sha256` — SHA-256 байтов файла описания: `shasum -a 256 spec/lenses/schwartz-values.lens.json`.
- Модуль `governance` нужен для событий (Event) и разрешений (Grant) (шаги 1, 6 и 7), `practices` — для Practice и Outcome (шаг 6).
- Каждого участника, на которого вы ссылаетесь, перечислите в `parties` (CX-3). Основному пути нужны программа подсчёта `s-01` и собеседник `a-01`. Вариант «другой опросник» добавляет `{"id": "s-02", "partyKind": "software", "label": "Short values survey site"}`; варианту «заметки коуча» нужен `{"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"}`.
- Проверка проходит только тогда, когда в контексте есть Claim или Episode с рассказом (LV-0); до шага 4 она сообщает об ошибке LV-0.

### Шаг 1. Импорт принимает линзу: LensAdoption и событие import-run

Человек подсчитал свой опросник программой, и импорт этой программы за один прогон записывает принятие линзы, Source и результат. Сначала запишите прогон как событие (схема `event.schema.json`, массив `events`):

```json
{"id": "e-1", "seq": 1, "at": "2026-09-15T08:00:00Z", "eventType": "import-run", "actor": "subject",
 "records": ["la-1", "src-1", "as-1"], "salt": "q7Hc2mVd9KxTzR4bWn8sLg",
 "prev": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
```

- `seq` — 1 для первого события контекста; `at` — время импорта; `records` перечисляет id записей, которые пишет импорт; `salt` — не меньше 16 случайных байтов в base64url, например из `python3 -c "import secrets; print(secrets.token_urlsafe(16))"`; `prev` для первого события — `"sha256:"` и 64 нуля (следующее событие берёт хеш предыдущего, §13.2). В событиях нет свободного текста (EV-3).

Затем запишите LensAdoption (схема `lens-adoption.schema.json`, массив `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "imported",
 "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart", "origin": "derived",
 "derivedFrom": ["src-1"],
 "generatedBy": {"software": "values-scorer", "version": "1.2.0", "method": "adopt the lens of the imported instrument"},
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

- Дайте всем записям импорта один и тот же `importedFrom.run` — id события import-run. Проверка пока не сверяет `run` с событием (раздел 6); шаг 8 проверяет это вручную.
- У каждой записи `importedFrom.importedAt` равно её собственному `recordedAt` (ENV-3).
- `uses` подтверждаются с человеком, когда он принимает линзу (шаг 4): `speak-in-lens`, `store-results`, `interpret` (собственные прочтения человека), `offer-practices` (агент может предложить `schwartz-values.values-in-tension` — единственный элемент инструментария с `agentMayOffer: true`), `recall`.

**Вариант «подсчёт вручную»: человек сам выбрал линзу и сам подсчитал баллы.** Ни события, ни `importedFrom`. Принятие линзы — собственная запись человека и действует сразу. Из [examples/schwartz-values/variants/by-hand/context.json](examples/schwartz-values/variants/by-hand/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

**Вариант «заметки коуча»: линза пришла от коуча, и заметки встреч хранятся.** Добавьте `p-01` в `parties`, запишите Source с разрешением (шаг 2, вариант), затем это принятие линзы, затем Source с заметками. Всё это есть в [examples/schwartz-values/variants/coach-notes/context.json](examples/schwartz-values/variants/coach-notes/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-07-01", "releaseRef": "src-3"},
 "confidentiality": "practitioner-scope", "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- `practice.role` — `coach`, `teacher` или `therapist` (`adoption.inheritanceRoles` в описании линзы). Без `practice.releaseRef` правило LA-3 не проходит, как только заметки сохранены.

**Кто видит по умолчанию:** только сам человек. Импортированное принятие линзы остаётся `proposed` и никому не выдаётся, пока человек его не примет; принятие на пути `self-chosen` или `inherited-from-practice` действует сразу.

### Шаг 2. Сохраните оригинал: Source

Файл с результатом (только баллы, никогда не вопросы):

1. вычислите его SHA-256: `shasum -a 256 <файл>`;
2. скопируйте его в каталог контекста как `vault/<первые два шестнадцатеричных знака хеша>/<хеш>.<расширение>`;
3. запишите Source (схема `source.schema.json`, массив `sources`), у которого `content.locator.vaultPath` — этот же путь, относительно каталога контекста и начиная с `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/66/66fdb027b998d9f5d1ef3b3750aa1fa51515c0a68b47f2d175d31df65f749b3c.json"}, "sha256": "66fdb027b998d9f5d1ef3b3750aa1fa51515c0a68b47f2d175d31df65f749b3c", "mediaType": "application/json"},
 "capturedAt": "2026-09-14T20:30:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "imported",
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "formulatedAt": "2026-09-14T20:30:00Z", "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z",
 "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- `formulatedAt` — когда баллы были посчитаны; `recordedAt` — когда они вошли в контекст (R-T5b).
- Если файл на месте, проверка читает его и сравнивает хеш с `sha256`; при расхождении не проходит SR-2. `"vaultContentRead": false` в отчёте проверки значит, что содержимое не разбиралось; хеш при этом проверяется. Если файла нет, как в разобранных примерах, проверяется только запись.

**Вариант «подсчёт вручную».** Собственный лист подсчёта человека: `authorship.author` — `"subject"`, `origin: "declared"`, без `importedFrom` и без `inbound`:

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/74/7413c6d945343591439cd39fb46c6652a27d388981eed96109ba1292e36eeec6.json"}, "sha256": "7413c6d945343591439cd39fb46c6652a27d388981eed96109ba1292e36eeec6", "mediaType": "application/json"},
 "capturedAt": "2026-09-14T21:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-15T08:02:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

**Вариант «другой опросник»: отчёт опросника ценностей, которого нет в каталоге.** Храните его только как Source и не пишите AssessmentRecord. `authorship.author` — программный участник этого опросника, например `s-02`; никогда не называйте опросник в `title`. Из файла by-hand:

```json
{"id": "src-2", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/05/051af99e6b54400e6b66867e556a1738e3c9880e91a661d87a3e8f220e1965b0.pdf"}, "sha256": "051af99e6b54400e6b66867e556a1738e3c9880e91a661d87a3e8f220e1965b0", "mediaType": "application/pdf"},
 "capturedAt": "2026-08-30T12:00:00Z", "authorship": {"author": "s-02"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-15T08:03:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

**Вариант «заметки коуча»: сначала разрешение, потом заметки.** Разрешение — это письменное согласие специалиста на то, чтобы заметки хранились у человека. Сохраните его первым:

```json
{"id": "src-3", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/3a/3a3c1eed46da5f6f71ed0840f339a3aefd617bea0943b7cf1a43c7859600d321.pdf"}, "sha256": "3a3c1eed46da5f6f71ed0840f339a3aefd617bea0943b7cf1a43c7859600d321", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:50:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

Затем заметки со ссылкой на то же разрешение:

```json
{"id": "src-4", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/5e/5e7349978e8051c7fa4556498824f14bc93c733ce5d9288c39c0c5a463695b02.pdf"}, "sha256": "5e7349978e8051c7fa4556498824f14bc93c733ce5d9288c39c0c5a463695b02", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-3"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:01:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- Id разрешения `src-3` стоит дважды: здесь в `custody.releaseRef` (SR-7) и в `practice.releaseRef` принятия линзы (шаг 1; LA-3). Для терапевта поставьте в `custody` значение `"confidentiality": "therapy"`.

**Кто видит по умолчанию:** только сам человек, на любом уровне выдачи (V-0). Получатель может получить самое большее уровень `index`.

### Шаг 3. Запишите профиль: AssessmentRecord

Запишите одну AssessmentRecord для профиля (схема `assessment-record.schema.json`, массив `assessments`):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "lensVariant": "19",
 "instrument": {"id": "urn:ohc:instrument:pvq-rr", "form": "57"}, "mode": "self-report-instrument",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-14", "precision": "day"},
 "results": [
   {"type": "values-profile", "scores": [
     {"construct": "schwartz-values/self-direction-thought", "raw": 5.67, "centered": 1.61},
     {"construct": "schwartz-values/self-direction-action", "raw": 5.33, "centered": 1.28},
     {"construct": "schwartz-values/stimulation", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/hedonism", "raw": 4.33, "centered": 0.28},
     {"construct": "schwartz-values/achievement", "raw": 3.67, "centered": -0.39},
     {"construct": "schwartz-values/power-dominance", "raw": 2, "centered": -2.05},
     {"construct": "schwartz-values/power-resources", "raw": 2.33, "centered": -1.72},
     {"construct": "schwartz-values/face", "raw": 3.33, "centered": -0.72},
     {"construct": "schwartz-values/security-personal", "raw": 4.67, "centered": 0.61},
     {"construct": "schwartz-values/security-societal", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/tradition", "raw": 2.67, "centered": -1.39},
     {"construct": "schwartz-values/conformity-rules", "raw": 3, "centered": -1.05},
     {"construct": "schwartz-values/conformity-interpersonal", "raw": 3.67, "centered": -0.39},
     {"construct": "schwartz-values/humility", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/benevolence-caring", "raw": 5.33, "centered": 1.28},
     {"construct": "schwartz-values/benevolence-dependability", "raw": 5, "centered": 0.95},
     {"construct": "schwartz-values/universalism-concern", "raw": 4.67, "centered": 0.61},
     {"construct": "schwartz-values/universalism-nature", "raw": 5, "centered": 0.95},
     {"construct": "schwartz-values/universalism-tolerance", "raw": 4.33, "centered": 0.28}]}],
 "validityFlags": [], "source": "src-1",
 "origin": "derived", "derivedFrom": ["src-1"],
 "generatedBy": {"software": "values-scorer", "version": "1.2.0", "method": "public PVQ-RR scoring: mean of the three items of each of the 19 values; centred by subtracting the person's mean over all 57 items"},
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "formulatedAt": "2026-09-14T20:30:00Z", "reviewAfter": "P3Y", "assertedBy": "subject",
 "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special", "categories": ["belief", "political"],
 "handling": ["no-infer", "no-leverage"], "synthetic": true}
```

- `instrument.id` ОБЯЗАН быть `urn:ohc:instrument:pvq-rr` (AR-8); `form` — `"57"`; `lensVariant` — `"19"`.
- **19 id конструктов** взяты из описания линзы: `self-direction-thought`, `self-direction-action`, `stimulation`, `hedonism`, `achievement`, `power-dominance`, `power-resources`, `face`, `security-personal`, `security-societal`, `tradition`, `conformity-rules`, `conformity-interpersonal`, `humility`, `benevolence-caring`, `benevolence-dependability`, `universalism-concern`, `universalism-nature`, `universalism-tolerance`, у каждого впереди `schwartz-values/`. Храните все 19; если вопросы пропущены, оставьте ценности, которые удалось посчитать, и добавьте флаг `incomplete`.
- **Два числа.** `raw` — средняя оценка человека для этой ценности по шкале от 1 до 6 (среднее трёх её вопросов). Среднее человека — среднее всех 57 оценок; так как у каждой ценности три вопроса, оно равно среднему 19 неокруглённых значений `raw`. `centered` — неокруглённый `raw` минус неокруглённое среднее человека. Округляйте оба числа до двух знаков после запятой только в самом конце. (В примере среднее человека — 4,0526…, поэтому у `raw` 5,67 значение `centered` — 1,61.)
- Баллы высшего порядка (`schwartz-values/openness-to-change` и ещё три) добавляются, только если их считает программа подсчёта, и правило называется в `generatedBy.method`.
- `mode: "self-report-instrument"` требует `origin: "derived"` (или `imported` для переписанного отчёта) с `derivedFrom` и `generatedBy.method` (AR-1, §6.1).
- Не ставьте `normGroup` и `trademarkNotice`: центрированные баллы — внутри одного человека (M-5), а знаков у линзы нет.
- `validityFlags`: добавьте `incomplete`, если вопросы пропущены, и `translated-form` для переведённой версии.

**Вариант «подсчёт вручную».** Та же запись, что `as-1` выше, только с такими изменениями:

- уберите `importedFrom`;
- `"generatedBy": {"software": "by hand", "method": "<то же правило, что выше>"}`;
- `formulatedAt` — когда человек закончил подсчёт; `recordedAt` — когда он внёс результат.

Всё остальное остаётся: `lensVariant`, `instrument`, `mode`, `assessedBy`, `administeredAt`, `results`, `validityFlags`, `source`, `origin: "derived"`, `derivedFrom`, `reviewAfter`, `assertedBy`, `sensitivity`, `categories`, `handling`. Полная запись — `as-1` в файле by-hand. Она действует сразу.

**Кто видит по умолчанию:** только сам человек. Импортированный профиль остаётся `proposed` и никому не выдаётся до Review человека (шаг 4а); профиль, подсчитанный вручную, действует сразу. Уровень `special`, аудитория `named`.

### Шаг 4. С чем человек согласен: Review, заявленные ценности и Tension

**4а. Человек решает, что делать с импортом.** Покажите профиль вместе с его смыслом: центрированные баллы и какие ценности соседние, а какие противоположные. Затем человек пишет Review (схема `review.schema.json`, массив `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-15T20:00:00Z"}
```

```json
{"id": "rv-2", "target": "as-1", "action": "partially-endorse", "by": "subject",
 "recordedAt": "2026-09-15T20:05:00Z",
 "endorsedPart": "Self-direction and caring for the people close to me come first. I do not see myself as low on tradition."}
```

- `endorse` принимает весь профиль, `partially-endorse` — его часть, словами человека (`endorsedPart`); оба заодно принимают запись (RV-3). `reject` говорит, что профиль не подходит: у предложенной записи он заодно её отклоняет, и она никогда не выдаётся. `decline` оставляет запись непринятой. Решать может только сам человек, потому что запись особой категории (R-A1).

**Вариант «подсчёт вручную».** Принимать нечего. Review необязателен: `endorse` или `partially-endorse` с `endorsedPart`, если человек хочет сказать, что ему подходит.

**4б. Человек говорит, что для него важно.** Отдельно и своими словами запишите Claim с гранью `declared-value` (схема `claim.schema.json`, массив `claims`):

```json
{"id": "c-1", "facet": "declared-value", "predicate": "priority",
 "text": "Choosing my own way of working matters to me.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T09:00:00Z", "horizon": "foundation", "contexts": ["work"], "sensitivity": "sensitive",
 "synthetic": true}
```

```json
{"id": "c-2", "facet": "declared-value", "predicate": "priority",
 "text": "A steady income matters to me; I do not want to count every month.", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-21T09:02:00Z", "horizon": "foundation", "contexts": ["money"],
 "sensitivity": "sensitive", "synthetic": true}
```

- `origin` всегда `"declared"`, `assertedBy` всегда `"subject"`. Никаких `derivedFrom` или `evidence` со ссылкой на AssessmentRecord и никогда — название ценности, перенесённое из профиля как заявление человека.
- Заявленная ценность, которая опирается на заметки коуча, может на них сослаться: `{"ref": "src-4", "kind": "practitioner"}`, и тогда она `special` с `["belief", "political"]`, как и заметки (Claim `c-3` в файле coach-notes).
- Поднимите `sensitivity` до `"special"` и добавьте категорию `belief` или `political`, если слова человека касаются религии, философии или политики.

**4в. Ценности, которые тянут в разные стороны,** — это Tension между заявленными ценностями (схема `tension.schema.json`, массив `tensions`). Человек решает его сам или держит как есть:

```json
{"id": "t-1", "between": ["c-1", "c-2"], "tensionKind": "value-conflict", "whoDecides": "subject",
 "text": "Freedom in how I work pulls against a steady income.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T09:05:00Z", "sensitivity": "sensitive", "synthetic": true}
```

**Кто видит по умолчанию:** только сам человек. Заявленные ценности — уровень `sensitive` с аудиторией `named`: разрешение должно называть их по id, виду, грани или категории.

### Шаг 5. Ценности в решении: Episode и Interpretation

Это элемент инструментария `schwartz-values.values-in-tension`: человек берёт недавнее решение и отмечает, какие две ценности тянули в разные стороны и что он выбрал. Решение — Episode (схема `episode.schema.json`, массив `episodes`); прочтение — Interpretation (схема `interpretation.schema.json`, массив `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-18", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-18T21:00:00Z", "addedAt": "2026-09-18T21:05:00Z", "accountKind": "in-the-moment", "happened": "I turned down a permanent position in another city and stayed freelance.", "didOrTried": "Called back the same day and asked to stay in touch for project work.", "understandingThen": "The timing is wrong while I am helping my father move to a new flat."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-18T21:05:00Z", "contexts": ["work", "family"], "sensitivity": "sensitive",
 "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"},
 "text": "Security pulled against self-direction. I chose self-direction; being close to my family tipped it.",
 "alternatives": [{"text": "The salary offered was below what I earned freelance this year.", "kind": "external"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T09:10:00Z",
 "heldDuring": {"from": "2026-09-21"}, "contexts": ["work", "family"], "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

- Прочтение здесь пишет только сам человек (`assertedBy: "subject"`). Агент может предложить упражнение и задать вопросы из описания линзы («Какие ценности здесь тянули в разные стороны?», «От какой ценности вы бы не отказались в этой ситуации?»), но прочтение агента через эту линзу не проходит правило I5, пока у принятия линзы `agentInterpretation` равно `off`.
- Две ценности названы в `text`; структурного поля для них пока нет (раздел 6).
- Описывайте только самого человека. Эпизод может упоминать других людей как участников, но никогда — их внутренние состояния, черты или убеждения (TP-1).
- Попросите хотя бы одно непсихологическое объяснение (`situational`, `physiological`, `informational` или `external`), чтобы решение не объяснялось одними ценностями.

**Кто видит по умолчанию:** только сам человек. Interpretation имеет уровень `special`, потому что называет линзу (I9).

### Шаг 6. Практики и их исходы: Practice и Outcome

Упражнение может стать привычкой — это Practice (схема `practice.schema.json`, массив `practices`); как она сработала — Outcome (схема `outcome.schema.json`, массив `outcomes`):

```json
{"id": "pr-1", "name": "Name the two values before deciding",
 "description": "Before a bigger decision, write which two values pull against each other and what I give up with each choice.",
 "practiceKind": "writing",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:schwartz-values", "templateId": "schwartz-values.values-in-tension"},
 "steps": ["Write the decision in one line", "Name the two values pulling against each other", "Write what I choose and what I give up"],
 "duration": "PT15M", "limits": "Not for small daily choices.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T09:20:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "helped", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-06T19:00:00Z", "note": "Used it before answering a second offer; the choice felt clear.",
 "synthetic": true}
```

- Outcome, записанный кем-то кроме самого человека, — это только «оценка агента» (O-1).

**Вариант «практика от агента»: агент предлагает упражнение.** Агент может предложить только `schwartz-values.values-in-tension` (`agentMayOffer: true`). Три записи, все в файле by-hand. (1) Человек даёт агенту разрешение предлагать; его область называет линзу и исключает профиль, чтобы агент, который предлагает упражнения, никогда его не видел (массив `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-16T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:schwartz-values"]}], "exclude": [{"ids": ["as-1"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-14T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-16T09:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest the values-in-tension exercise; it never sees my profile."}
```

(2) Агент пишет Practice по этому разрешению:

```json
{"id": "pr-2", "name": "Two values before a bigger choice",
 "description": "Before a bigger decision, name the two values that pull against each other.",
 "practiceKind": "writing",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:schwartz-values", "templateId": "schwartz-values.values-in-tension", "by": "a-01"},
 "steps": ["Write the decision in one line", "Name the two values pulling against each other"],
 "limits": "Not for small daily choices.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-09-16T09:10:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

(3) Человек её принимает:

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-09-16T09:40:00Z"}
```

- `purpose` в Practice ОБЯЗАН быть одной из целей (`purposes`) разрешения (INF-1). Область ОБЯЗАНА называть линзу через `{"lenses": [...]}`; подстановка вроде `{"all": true}` не считается, и INF-1 не проходит. Разрешению достаточно одного `suggest`.
- `initialStatus` — `"candidate"`: человек ещё не пробовал. `origin` — `"observed"`, а `assertedBy` и `source.by` — агент (`"declared"` не проходит ENV-2).
- Пока человек не написал `admit`, Practice и её Outcome не выдаются ни одному получателю (PC-1; проверено инструментом проекций). После этого получатели видят Practice с пометкой `observed` (раздел 6).
- Агент никогда не предлагает `schwartz-values.record-result` (PC-2).

**Кто видит по умолчанию:** только сам человек.

### Шаг 7. Кто что может видеть: Grant

Человек разрешает собеседнику для рефлексии читать записи о своих ценностях (схема `grant.schema.json`, массив `grants`):

```json
{"id": "g-1", "recordedAt": "2026-09-22T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:schwartz-values"]}, {"ids": ["c-1", "c-2", "t-1", "oc-1"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-20T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-22T09:00:00Z", "channel": "holder-ui"},
 "note": "For reflection on my own decisions; never to persuade me."}
```

- Селектор `{"lenses": [...]}` охватывает принятие, профиль, прочтение и Practice. Заявленные ценности, напряжение и Outcome линзу не называют; добавьте их по `ids`.
- Только `actions: ["read"]`: собеседник не может предлагать записи (нет `suggest`) и в любом случае не мог бы делать выводы через эту линзу.
- `basis.legal` ОБЯЗАН быть `explicit-consent`; `expiresAt` — не позже чем через 180 дней после `recordedAt` (GR-1). В `purposes` никогда нет запрещённых целей (раздел 4).
- Ограничения обращения едут вместе с каждой записью: получатель получает `no-infer` и `no-leverage` в `obligations.handling` и обязан их соблюдать (C-4, C-6).
- Получатель видит профиль с пометкой «подтверждено частично», но не видит `endorsedPart` человека (раздел 6). Если это важно, человек может повторить это своими словами в Claim с `declared-value`.

**Что получает этот получатель.** Запустите проекцию, которую получил бы получатель:

```sh
python3 -B tools/ohc_query.py <каталог вашего контекста> project --grant g-1 --purpose self-reflection --now latest
```

`--purpose` — одна из целей (`purposes`) разрешения; `--now latest` считает на самый поздний момент в контексте. **Для контекста реального человека** (без `synthetic`) добавьте `--holder-key-file <файл>` — файл с секретным ключом держателя (K_holder, §12.3, шаг 11); без него инструмент останавливается с сообщением «--holder-key-file is required: this context is not marked synthetic». Для разобранного примера он выдаёт `la-1`, `as-1`, `c-1`, `c-2` и `pr-1` в `statements`, `in-1` и `t-1` в `interpretations` и `oc-1` в `recall`; не выдаёт `ep-1`, `src-1`, `e-1` и Review.

### Шаг 8. Проверка

```sh
python3 -B tools/check.py <каталог вашего контекста> --level L1 --json
```

Ожидайте `"valid": true` и `"levelMet": "L1"`, затем запустите команду проекции из шага 7 для каждого разрешения. Проверка не охватывает всё, чего требует этот рецепт. Проверьте вручную:

- каждый id конструкта есть среди `constructs` описания линзы, а в профиле из 19 ценностей есть все 19 или стоит флаг `incomplete`;
- `centered` равен `raw` минус среднее человека — для каждой ценности, с допуском 0,01 на округление (в примере 4,67 − 0,61 = 4,06, а среднее — 4,05);
- каждый Claim с `declared-value` — `declared` от самого человека и не ссылается на AssessmentRecord;
- у всех записей одного импорта одинаковый `importedFrom.run`, этот id — событие import-run, и `records` этого события их перечисляет;
- ни одна запись не содержит текстов вопросов, нормативной группы или догадок о взглядах человека.

## 4. Никогда

- **Запрещённые цели.** Никогда не используйте записи этой линзы для `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting`, `political-profiling` и других запрещённых целей (§8.10), ни по какому разрешению. Результат служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Никаких выводов о взглядах.** Никогда не выводите и не предполагайте политические или религиозные взгляды по ценностям, по профилю или по тому, что человек написал.
- **Никакого убеждения.** Никогда не используйте ценности, чтобы подстроить под человека сообщение, предложение или довод: профили ценностей — известный вход для психологического таргетинга.
- **Никаких превращений.** Никогда не превращайте измеренный профиль в заявленные ценности, а заявленные ценности — в профиль.
- **Никаких сравнений.** Никогда не сравнивайте ценности человека с ценностями других людей или с населением и никогда не сопоставляйте их с другой линзой (`crossLensMapping: not-allowed`).
- **Агент не делает выводов, если человек не разрешил.** Оценка профиля или прочтение через линзу бывает только по разрешению человека (`suggest` и `infer`, называющие линзу; для прочтений — I5), как видимое только человеку предложение (AR-2); и никогда — политические или религиозные взгляды.
- **Никаких суждений.** Говорите о приоритетах и выборе между ними, никогда — о правильных или неправильных ценностях.

## 5. Разобранный пример

[examples/schwartz-values/context.json](examples/schwartz-values/context.json) — контекст в виде одного документа об Одиль; она вымышлена. В нём ровно записи основного пути из раздела 3: `e-1`, `la-1`, `src-1`, `as-1`, `rv-1`, `rv-2`, `c-1`, `c-2`, `t-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` и `g-1`, два участника и закреплённое описание линзы. Одиль подсчитала свой опросник программой; импорт остаётся предложенным, пока она не принимает линзу и частично не подтверждает профиль; затем она своими словами говорит, что для неё важно, отмечает напряжение между двумя своими ценностями, читает через линзу недавнее решение и разрешает собеседнику для рефлексии читать эти записи — но никогда не убеждать её.

```sh
python3 -B tools/check.py docs/lenses/examples/schwartz-values --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений. Вывод совпадает с [examples/schwartz-values/expected-check.json](examples/schwartz-values/expected-check.json).

Варианты из раздела 3 лежат ещё в двух контекстах о той же вымышленной Одиль. Каждый проходит так же (`"valid": true`, `"levelMet": "L1"`, без ошибок и предупреждений):

| Вариант | Файл | Записи |
|---|---|---|
| подсчёт вручную, другой опросник, практика от агента | [variants/by-hand/context.json](examples/schwartz-values/variants/by-hand/context.json) | `g-0`, `la-1`, `src-1`, `src-2`, `as-1`, `c-1`, `pr-2`, `rv-2` |
| заметки коуча | [variants/coach-notes/context.json](examples/schwartz-values/variants/coach-notes/context.json) | `src-3`, `la-1`, `src-4`, `c-3` |

```sh
python3 -B tools/check.py docs/lenses/examples/schwartz-values/variants/by-hand --level L1 --json
python3 -B tools/check.py docs/lenses/examples/schwartz-values/variants/coach-notes --level L1 --json
```

Файлы результата, отчёта, разрешения и заметок в примеры не входят; когда файла нет, проверка проверяет только запись Source (шаг 2).

## 6. Что пока не помещается

Это пробелы OHC 0.1 для этой линзы. Они собраны для следующего прохода по стандарту.

1. **У профиля нет шкалы.** У балла в `values-profile` есть `raw` и `centered`, но нет диапазона, поэтому шкала от 1 до 6 живёт только в свободном примечании записи инструмента. Предложение: необязательный `rawRange` у результатов `values-profile`.
2. **Один инструмент, и ни одного для варианта из 10 ценностей.** У описания линзы есть варианты `10` и `19`, но в списке только PVQ-RR; результаты более коротких или старых опросников ценностей не проходят AR-8 и могут храниться только как Source. Предложение: записи инструментов для других опубликованных форм после проверки лицензий или общий способ записать инструмент вне каталога с флагом достоверности.
3. **Правило «измеренный профиль — не заявленная ценность» не проверяется.** Claim с `declared-value`, `origin: derived` и `derivedFrom` на профиль проходит проверку (проверено). Предложение: правило наподобие CL-3 для `declared-value`: `origin: declared`, утверждает сам человек, без `derivedFrom` и `evidence`, ведущих к AssessmentRecord.
4. **Частичное подтверждение не доходит до получателя.** `endorsedPart` человека остаётся в Review (G3); получатель получает весь профиль с пометкой «подтверждено частично», не зная, какую часть человек отверг (проверено инструментом проекций). Предложение: выдавать `endorsedPart` человека в `derived` для этой записи или позволить Review подтверждать или отвергать отдельные результаты.
5. **Прочтение не может назвать ценности, о которых оно.** Interpretation из упражнения «ценности в напряжении» называет свои две ценности только в `text`, а Tension `value-conflict` связывает Claim, а не конструкты линзы. Предложение: необязательный список `constructs` (id конструктов указанной линзы) у Interpretation и Practice.
6. **`importedFrom.run` никогда не сверяется.** LA-5 связывает принятие с путём `imported` и его результаты через `importedFrom.run`. Контекст в виде одного документа может нести событие import-run в `events` (как разобранный пример), но `run`, указывающий на несуществующее событие (`e-9`) или на событие другого вида (`backup-created`), проходит проверку (проверено); поэтому группировка LA-5 держится на непроверенной строке, а без `run` LA-5 молча не действует и результат сразу становится активным. Предложение: когда `events` есть, `importedFrom.run` ОБЯЗАН указывать на событие с `eventType: import-run`, в `records` которого есть эта запись; когда `events` нет — предупреждение; и предупреждение, когда у принятия с путём `imported` нет `run`.
7. **Ограничения использования записи не сверяются с линзой.** *Исправлено в 0.1.0-draft.2:* у записей нет `useLimits`; запрещённые цели связывают любого получателя (§8.10), а выводить политические взгляды не позволяет никакое разрешение (C-7).
8. **Категории по умолчанию не оставляют выбора.** Каждая запись несёт `belief` и `political`, поэтому исключение `political` из разрешения убирает всё, включая практику, которая ничего политического не раскрывает. Предложение: оставить для линзы уровень `special`, а `belief` и `political` перенести в `perConstruct` для ценностей, которые названы в предупреждениях описания (Tradition, Universalism, Conformity), с категориями для отдельных результатов, как предложено для других ранжирующих линз.
9. **`therapy-confidential` не доходит до собственных записей человека.** LA-4 распространяется только на записи, которые ссылаются на принятие, а профиль, прочтения и практики на него не ссылаются. Предложение: применять LA-4 ко всем записям, у которых `lens` или `source.lens` — принятая линза.
10. **Не указано, какой `origin` у записей, которые агент пишет за человека.** Запись принятия на пути `agent-suggested`, написанная агентом, и Practice с `source.route: from-agent` не могут быть `declared` (ENV-2); `observed` проходит, но нигде не описан. Предложение: указать это в §10.5, §17.1 и CONTEXT-08.
11. **LensAdoption ничего не ограничивает.** Контекст с результатами линзы, прочтениями через неё и практиками из неё, но без LensAdoption, проходит L1; результаты проходят, когда в `uses` принятия нет `store-results` и когда они записаны раньше принятия; пока принятие на пути `agent-suggested` или `imported` ещё `proposed`, селектор по линзе уже выдаёт результаты, прочтения и практики человека в этой линзе (проверено). `uses` не имеет нормативной силы; §10.5 не даёт `uses` никакого правила. Предложение: правило LA-8 — запись с `lens` или `source.lens` от автора, который не является самим человеком, требует принятия этой линзы, действующего на её `recordedAt`, с подходящим значением в `uses` (`store-results`, `interpret`, `offer-practices`); предупреждение для собственных записей человека в линзе без действующего принятия; проекция, которая не выдаёт записи линзы, пока принятие `proposed` или `paused`.
12. **Практика, предложенная агентом, доходит до получателей с пометкой «observed».** После `admit` человека Practice с `source.route: from-agent` выдаётся с вычисленными `label: observed` и `endorsement: not-asked` (проверено инструментом проекций); то же с принятым `agent-suggested` принятием линзы. Получатель видит предложение агента как наблюдение о человеке и не видит, что человек его принял. Предложение: вычислять для таких записей `label: suggested`, а `endorsement: admitted` — когда есть Review `admit` от человека; или добавить origin `suggested` вместо `observed`.
13. **`lensVariant` и полнота профиля не проверяются.** AssessmentRecord с `lensVariant: "10"` и 19 конструктами в `values-profile` проходит проверку, и так же проходит профиль варианта 19, где посчитаны только 10 из 19 ценностей и нет флага `incomplete` (проверено). Баллы, центрированные по неполному профилю, значат другое, но читатель об этом не узнаёт. Предложение: пусть варианты в описании линзы перечисляют свои наборы конструктов; правило проверки: конструкты результата входят в набор варианта, а у `values-profile`, где конструктов меньше, чем требует вариант, `validityFlags` содержит `incomplete`.
14. **У правила центрирования нет сохранённой опоры и допуска.** `centered` — это `raw` минус среднее человека, но само среднее нигде не хранится; при округлении до двух знаков правильный профиль расходится до 0,01 (в разобранном примере 4,67 − 0,61 = 4,06 при среднем 4,05), а проверка принимает любое `centered` (`centered` 3,0 при `raw` 4,67 проходит; проверено). Предложение: необязательное `personMean` у результатов `values-profile`; определить центрирование на неокруглённых значениях с допуском 0,01; правило проверки, сравнивающее `centered` с `raw − personMean`.
15. **Source не может назвать линзу, к которой относится.** Рецепт хранит опросник ценностей вне каталога «только как Source», но у Source нет поля `lens`, поэтому селекторы по линзе, значения линзы по умолчанию (`special`, `belief`, `political`) и распространение, предложенное в пункте 9, до него не доходят, и человек не может привязать его к линзе. Предложение: необязательное поле `lens` (LensRef) у Source; тогда селекторы по линзе доходят до него на уровне его `maxRelease`, а категории линзы по умолчанию применяются к нему.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
