# Рецепт линзы: `ifs` (линза частей)

**Рецепт · линза `urn:ohc:lens:ifs` 0.2.0 · OHC 0.1.0-draft.2 · справочный документ · 12 октября 2026**

Этот рецепт по шагам показывает, как собственный язык частей человека попадает в контекст OHC через линзу `ifs`: какие записи при этом создаются, кто их видит и чего агент никогда не делает.

> **Уведомление.** Возможности OHC не являются IFS-терапией и не сертифицированы IFS. Название Internal Family Systems — предмет заявки на товарный знак в США SN 98151674 от The Center for Self Leadership, Inc. (IFS Institute); заявка оспаривается. Название используется здесь только для того, чтобы указать метод, на который ссылается описание линзы.

**Линза коротко** (по [`spec/lenses/ifs.lens.json`](../../spec/lenses/ifs.lens.json); см. также [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person)):

| | |
|---|---|
| Вид и статус | `parts-model`, описание в статусе `draft` |
| Понятия линзы | `ifs/self`, `ifs/manager`, `ifs/firefighter`, `ifs/exile` (близко к травме), `ifs/burden` (близко к травме) |
| Опросники | нет: измерять нечего |
| Инструменты | `ifs.noticing-a-part` (человек сам; агент никогда не предлагает; даёт запись Part); `ifs.exile-work` (только со специалистом; в OHC ничего не даёт) |
| Представление | `ifs.parts-map`: карта, которая собирается из записей Part и связей между частями при показе и никогда не хранится (P-4) |
| Предложение агентом | по разрешению человека (`suggest`, называющее линзу); рекомендация описания: только после того, как человек попросил о способах посмотреть на внутренний конфликт |
| Толкование агентом | по разрешению человека (`infer`, называющее линзу) и его принятию линзы (I5); в примере `off`, как по умолчанию; никогда не называя и не толкуя части (`helperMustNot`) |
| Сопоставление с другими линзами | `not-allowed` |
| Значения по умолчанию | уровень `special`; категории `mental-health`, `trauma-adjacent`; `reviewAfter` `P6M` |

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:ifs-basic`](../../spec/playbooks/ifs-basic.playbook.json) («Внутренние семейные системы: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; подготовка к трудному разговору; после неудачи. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

- **Рассказ человека в разговоре.** Человек своими словами говорит о внутренних позициях: «часть меня хочет ещё раз проверить цифры, другая часть хочет всё отменить».
- **Собственные записи человека.** Запись в дневнике, сделанная после того, как он заметил часть.
- **Записи из терапии или коучинга**, где используется язык частей: записи специалиста, итог сессии или собственные заметки человека с сессии. Это материал специалиста, у него есть хранитель.

Для этой линзы не подходит:

- **Отчёт опросника.** У линзы нет опросника, поэтому нет ни баллов, ни профиля, ни типа для переноса.
- **Толкование агента** без разрешения человека (`infer` с именем линзы) и его принятия линзы (I5). И с ними агент никогда не называет, не придумывает и не предлагает части (`helperMustNot`); в примере у разрешения только `read`.

## 2. Прежде чем начать

**Путь принятия линзы.** Выберите тот, который соответствует тому, как человек пришёл к линзе.

| Путь | Когда | Что меняется |
|---|---|---|
| `self-chosen` | Человек выбрал линзу сам. | Человек записывает принятие; оно действует сразу. |
| `agent-suggested` | Человек попросил вас о способах посмотреть на внутренний конфликт, вы назвали эту линзу как один из вариантов, и человек её выбрал. | Только по разрешению с `suggest`, называющему линзу; вы называете линзу только после такой просьбы (`suggestionRequires`) и не используете её язык, пока линза не принята. В принятии есть `suggestedBy` (id вашей стороны), и оно остаётся `proposed`, пока человек не примет его записью Review, даже если запись сделал сам человек. Проверка не напомнит вам об этой записи Review (шаг 1). |
| `inherited-from-practice` | Человек пользуется линзой в терапии или коучинге. | Добавьте блок `practice` (роль, сторона-специалист, состояние отношений). С терапевтом поставьте `confidentiality: "therapy-confidential"`: принятие и все записи, которые ссылаются на него в поле `adoption` (части, толкования через линзу), становятся `person-only` (LA-4). Практика (Practice) не может сослаться на принятие, поэтому `person-only` на неё вы ставите сами (шаг 6). С коучем — `practitioner-scope`. Если вы храните материалы сессий, `practice.releaseRef` должен указывать на разрешение специалиста (LA-3). `onEnd` говорит, что будет, когда работа со специалистом закончится. |
| `imported` | Для этой линзы не указан: импортировать не из чего. | Пути описывают обычную практику и ничего не запрещают. |

**Согласие.** Линзу принимает человек, а не вы. Принятие — это утверждение человека, а не разрешение: оно никому не даёт доступа, даже специалисту (LA-2, R-G13). Для доступа нужна запись Grant (шаг 7). Каждую запись Part пишет сам человек (P-2). Вы можете записывать то, что человек диктует, прочитать ему и дать исправить до сохранения ([CONTEXT-01](../agents/procedures/CONTEXT-01.md)). Поле `recordedBy` не заполняйте: если поставить туда id вашей стороны, правило INF-1 потребует `underGrant` и `purpose` по разрешению с действием `write`.

**Значения по умолчанию для этой линзы.**

- `sensitivity: "special"` на каждой записи линзы: на принятии, частях, толкованиях через линзу, практиках из её инструментов и источниках из сессий. В документации это называется «относится к особой категории».
- `categories: ["mental-health", "trauma-adjacent"]` — категории линзы по умолчанию. Записи могут их повышать, но не понижать; понизить уровень может только сам человек записью Review `relax`.
- У записей Part по умолчанию `handling: ["person-only"]` (P-3). Рекомендуется добавить `no-quote-back` и `no-forward`.
- `agentInterpretation: "off"` — всегда.
- `reviewAfter`: `P6M`.

**Что никогда не хранится.**

- Любые баллы и оценки: опросника нет, а «насколько сильна каждая часть» — не измерение.
- Учебные материалы метода и опубликованные тексты упражнений (ограничение из описания линзы).
- Имена, роли или описания частей, которые придумал или подсказал агент.
- Всё об «изгнанниках» и «бременах», что написал или о чём спросил агент.
- Ярлыки из других линз, привязанные к частям, например тип личности у части (`crossLensMapping: not-allowed`).
- Диагнозы и клинические термины.
- Текст записей специалиста внутри любой записи. Записью является только описание источника (Source), сами байты лежат в хранилище.

## 3. Шаги

Для каждого шага сказано, что сделать, какая запись появляется, в какой массив файла контекста она идёт, как выглядит минимальная запись, которая проходит проверку по схеме, и кто её видит по умолчанию. Фрагменты взяты из [разобранного примера](#5-разобранный-пример) или проверены вместе с ним; в них стоит `"synthetic": true`, потому что человек вымышлен — для настоящего человека это поле не пишут. Пока нет разрешения, никто, кроме самого человека, ничего не видит. Выполняйте шаги по порядку и ставьте каждой записи `recordedAt` позже, чем у записей, на которые она опирается.

### Шаг 0. Завести файл контекста

Создайте папку для контекста человека, а в ней файл `context.json` (форма «один документ», [§3.3](../../spec/SPECIFICATION.md#33-two-serializations-of-one-data-model); [схема](../../spec/schema/context.schema.json)). Начните его с такой оболочки:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:ysolde:context",
  "version": "2026-10-01.1",
  "subject": {"id": "urn:ohc:example:ysolde", "displayName": "Ysolde (fictional)"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-20T19:00:00Z",
  "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices", "inner-system"], "subjectIsAdult": true},
  "parties": [],
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "lenses": [{"id": "urn:ohc:lens:ifs", "version": "0.2.0"}],
  "synthetic": true,
  "lensAdoptions": [], "sources": [], "episodes": [], "parts": [], "relations": [], "claims": [],
  "interpretations": [], "practices": [], "outcomes": [], "grants": [], "reviews": []
}
```

- **Модули.** Объявите каждый модуль, чьи записи вы пишете, иначе проверка выдаст ошибки: `core` (Party, Source, Episode, Claim, Relation, Interpretation, Review), `governance` (Grant), `lenses` (LensAdoption), `practices` (Practice, Outcome), `inner-system` (Part и связи между частями).
- **Массивы.** Каждая запись идёт в массив своего вида: LensAdoption → `lensAdoptions`, Source → `sources`, Episode → `episodes`, Part → `parts`, Relation → `relations`, Claim → `claims`, Interpretation → `interpretations`, Practice → `practices`, Outcome → `outcomes`, Grant → `grants`, Review → `reviews`, Party → `parties`. В каждом шаге ниже массив назван ещё раз.
- **`synthetic`.** В примере `"synthetic": true` стоит у самого контекста и у каждой записи с содержанием; у сторон (Party) и у записей Grant и Review его не бывает никогда (схема его там не принимает).
- **Для настоящего человека.** Возьмите идентификаторы вида `urn:uuid:` для `id` и `subject.id`, например из `python3 -c "import uuid; print('urn:uuid:' + str(uuid.uuid4()))"`; уберите `synthetic` отовсюду; `displayName` необязателен. Не кладите папку внутрь папки с именем `examples`. Контекст, чей `id` начинается с `urn:ohc:example:` или который лежит внутри папки `examples`, проверяется как пример, и тогда `"synthetic": true` нужен на каждой записи с содержанием (X-1, CX-8).
- **`version`** вы выбираете сами; меняйте её при каждом наборе изменений.
- **Пустой файл проверку ещё не проходит.** В контексте должно быть хотя бы одно утверждение (Claim) или один эпизод (Episode) с рассказом (LV-0); его добавляет шаг 3. Проверяйте после шага 3 и ещё раз в конце (шаг 8).

### Шаг 1. Записать принятие линзы (LensAdoption → `lensAdoptions`)

Спросите человека, как он пришёл к линзе и для чего её можно использовать. Запишите одну запись LensAdoption ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption), [схема](../../spec/schema/lens-adoption.schema.json)).

- `uses`: `speak-in-lens` (вы можете называть части собственными словами человека, когда он сам о них говорит), `store-results` (человек хранит записи Part), `interpret` (собственные толкования человека). Не указывайте `offer-practices`: единственный инструмент для самостоятельной работы агент никогда не предлагает.
- `interpretationAuthors`: `["subject"]`. Терапевт, которого человек сюда добавит, может быть автором толкований через линзу (I5; §6, пункт 4).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "route": "self-chosen",
 "confidentiality": "none", "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "ifs.parts-map",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"], "synthetic": true}
```

**Вариант: `inherited-from-practice` с терапевтом.** Добавьте специалиста в `parties`: `{"id": "p-01", "partyKind": "person", "label": "Therapist", "role": "practitioner"}`. Затем измените принятие так:

```json
{"route": "inherited-from-practice",
 "practice": {"role": "therapist", "practitioner": "p-01", "relationship": "active", "since": "2026-05-01", "releaseRef": "src-03"},
 "confidentiality": "therapy-confidential", "onEnd": "ask"}
```

`handling` в само принятие не добавляйте: LA-4 уже делает `person-only` и его, и каждую запись, которая ссылается на него в поле `adoption`. `releaseRef` указывает на источник-разрешение из шага 2; если материалы сессий вы не храните, уберите это поле.

**Вариант: `agent-suggested`.** Добавьте себя в `parties`: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`. Добавьте в принятие `"suggestedBy": "a-01"` и сразу после него запишите в `reviews` запись Review от человека:

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-20T19:01:00Z"}
```

Без неё принятие остаётся `proposed`. **Проверка вам об этом не напомнит:** контекст без этой записи всё равно проходит, а части и практика линзы всё равно выдаются (§6, пункт 9). Пишите запись Review `admit` раньше любой записи Part, Interpretation или Practice этой линзы, с `recordedAt` раньше, чем у них.

**Кто видит:** только человек.

### Шаг 2. Сохранить оригинал в хранилище (Source → `sources`)

Если есть заметка, сохраните её как запись Source ([§10.1](../../spec/SPECIFICATION.md#101-source), [схема](../../spec/schema/source.schema.json)). В записи только описание, а сами байты кладутся в хранилище:

1. Посчитайте хеш: `shasum -a 256 <файл>` (или `sha256sum <файл>`). 64 шестнадцатеричных знака — это `sha256`.
2. Посчитайте размер в байтах: `wc -c < <файл>`. Это число — `size`.
3. Скопируйте файл в `vault/<первые два знака хеша>/<хеш>.<расширение>`. Путь `vaultPath` отсчитывается от папки, где лежит `context.json`.
4. Проверка уровня L1 хранилище не открывает (в её отчёте `"vaultContentRead": false`): она не заметит ни отсутствующего файла, ни неверного хеша, ни неверного размера. Выполните обе команды ещё раз для сохранённого файла и сравните.

Поставьте `maxRelease: "index"`, чтобы получатель мог узнать самое большее то, что заметка существует.

```json
{"id": "src-01", "sourceKind": "journal-entry", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-24T21:10:00Z",
 "content": {"locator": {"vaultPath": "vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md"},
             "sha256": "4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68",
             "mediaType": "text/markdown", "size": 313},
 "capturedAt": "2026-09-24T21:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Evening note after the club meeting.", "authoredBy": "subject",
             "recordedAt": "2026-09-24T21:10:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["community"], "synthetic": true}
```

Разобранный пример содержит эти байты: [examples/ifs/vault/4f/…](examples/ifs/vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md).

Записи, сделанные терапевтом, — это другой источник: `sourceKind: "practitioner-notes"`, в `authorship.author` — сторона-специалист, `inbound: true` и блок `custody`. Само разрешение специалиста — второй источник вида `practitioner-release`. Без разрешения любой получатель может узнать самое большее `index`; с разрешением материалы терапии всё равно не выходят дальше `summary` (§15.3). Хеши и размеры ниже относятся к файлам, которых в примере нет: посчитайте свои по своим файлам.

```json
{"id": "src-02", "sourceKind": "practitioner-notes", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/b8/b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67.md"},
             "sha256": "b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67", "mediaType": "text/markdown", "size": 57},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "custody": {"custodian": "p-01", "confidentiality": "therapy", "releaseRef": "src-03"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"], "synthetic": true}
```

```json
{"id": "src-03", "sourceKind": "practitioner-release", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/d1/d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd.md"},
             "sha256": "d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd", "mediaType": "text/markdown", "size": 71},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "synthetic": true}
```

**Кто видит:** человеку доступно всё (V-0). Получатель узнаёт самое большее `index` (без названия, без краткого содержания, без хеша), и только по разрешению, которое прямо называет этот источник.

### Шаг 3. Опыт и части (Episode → `episodes`, Part → `parts`, Relation → `relations`)

Результаты этой линзы записываются как части (Part), а не как AssessmentRecord.

**3а. Опыт.** Сначала простыми словами запишите, что произошло, — как запись Episode с рассказом самого человека ([§10.2](../../spec/SPECIFICATION.md#102-episode), [схема](../../spec/schema/episode.schema.json)). Части появляются потом, в своих записях.

```json
{"id": "ep-01", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T21:15:00Z",
 "title": "Budget evening at the club", "occurred": {"start": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T21:00:00Z", "addedAt": "2026-09-24T21:15:00Z",
    "accountKind": "in-the-moment",
    "happened": "Before the club meeting I opened the budget file four times and drafted a message cancelling my slot.",
    "experienced": "Tight in the chest; a pull to check again and a pull to run.",
    "didOrTried": "Did not send the message. Wrote down what each side wanted, then went.",
    "understandingThen": "I thought I was just badly prepared.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "salience": "medium",
 "contexts": ["community"], "synthetic": true}
```

**3б. Части.** Одна запись Part на каждую внутреннюю позицию, которую называет человек ([§20](../../spec/SPECIFICATION.md#20-inner-system-parts-experimental), [схема](../../spec/schema/part.schema.json)).

- `name` — собственные слова человека. Никогда не подсказывайте имя.
- `role` необязательна. Ставьте её, только если человек сам выбрал для этой части одно из понятий линзы (`ifs/manager` или `ifs/firefighter`). Никогда не используйте `ifs/self`: в этой линзе Я (Self) — не часть. Никогда не предлагайте `ifs/exile` или `ifs/burden`. Если человек приносит такую часть из терапии, он записывает её сам, она остаётся `person-only`, и вы о ней не спрашиваете.
- `authoredWith`: `alone`, `with-practitioner` или `with-agent`, если вы записывали под диктовку.
- `adoption: "la-01"` связывает часть с принятием; при терапевте именно эта ссылка делает её `person-only` по LA-4.

```json
{"id": "part-01", "name": "The double-checker", "description": "Goes over every figure again before anyone sees it.",
 "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "adoption": "la-01", "role": "ifs/manager",
 "intention": "Make sure nobody finds a mistake in my numbers.", "concern": "Being shown up in front of the club.",
 "typicalTriggers": ["presenting figures to a group"], "firstNoticed": {"start": "2026-09-01", "precision": "month"},
 "authoredWith": "alone", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T21:20:00Z",
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "handling": ["person-only", "no-quote-back", "no-forward"], "synthetic": true}
```

У второй части в примере, `part-02` («The one who wants to cancel», «Та, что хочет отменить»), нет `role`: человек её не выбрал.

**3в. Как части связаны.** Связь между частями — запись Relation `protects`, `polarized-with` или `allied-with`, которую пишет человек ([§9.5](../../spec/SPECIFICATION.md#95-relation)).

```json
{"id": "r-01", "rel": "polarized-with", "from": "part-01", "to": "part-02", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-24T21:22:00Z", "synthetic": true}
```

Карта частей (`ifs.parts-map`) собирается из этих записей при показе и никогда не хранится.

**Кто видит:** только человек (части — `person-only`, связи между частями — `special`).

### Шаг 4. Утверждения, которые человек принимает (Claim → `claims`, Relation `held-by` → `relations`)

У линзы нет результатов, поэтому утверждение (Claim) из неё никогда не выводится. Утверждение также никогда не опирается на часть, потому что часть — это толкование (слой `interpretation`). Если, заметив часть, человек пришёл к потребности, границе или предпочтению и хочет это сказать, запишите обычное утверждение его словами ([§9.4](../../spec/SPECIFICATION.md#94-claim)) и свяжите его с частью записью Relation `held-by` («это утверждение говорит эта часть»).

```json
{"id": "c-01", "facet": "need", "predicate": "structure",
 "text": "I need the figures closed a day before I present them.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-26T08:00:00Z", "horizon": "focus", "contexts": ["community"], "synthetic": true}
```

```json
{"id": "r-02", "rel": "held-by", "from": "c-01", "to": "part-01", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-26T08:01:00Z", "synthetic": true}
```

**Кто видит:** утверждение сохраняет свой уровень (`sensitive` для вида `need`), потому что уровни передаются по ссылкам и никогда — по связям Relation. Поэтому разрешение, которое называет вид утверждения, может показать потребность, не раскрывая, какая часть за ней стоит. Связь `held-by` имеет уровень `special` и показывается только тому, чьё разрешение называет её прямо.

### Шаг 5. Толкование эпизода через линзу — самим человеком (Interpretation → `interpretations`)

В примере через эту линзу толкует только человек (у разрешения только `read`). После принятия линзы и только когда человек сам заговорил о внутреннем конфликте, вы можете задать вопросы из описания линзы: «Какие внутренние позиции и потребности сейчас активны?» и «Чего, может быть, боится эта часть, если она отступит?» Ответ записывает человек.

Запишите толкование как запись Interpretation об эпизоде, с линзой и принятием ([§10.3](../../spec/SPECIFICATION.md#103-interpretation), [схема](../../spec/schema/interpretation.schema.json)). От человека другие объяснения не требуются, но предложите место для них: хотя бы одно непсихологическое объяснение (сон, нагрузка, недостающие сведения) делает толкование честнее. В поле `about` толкование не может указывать на часть (§6, пункт 1). Если толкование называет часть, которая всё ещё `person-only`, пометьте `person-only` и само толкование: иначе имя части уйдёт вместе с текстом толкования (§6, пункт 2).

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading", "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"},
 "adoption": "la-01",
 "text": "Two of my parts pulled in opposite directions: the double-checker wanted one more pass, the one who wants to cancel wanted out. Once each had been heard, I could go.",
 "alternatives": [
   {"text": "I had slept five hours the night before.", "kind": "physiological"},
   {"text": "The final bank figures only arrived that afternoon.", "kind": "informational"}],
 "heldDuring": {"from": "2026-09-27"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-27T20:00:00Z", "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "handling": ["person-only", "no-quote-back"], "contexts": ["community"], "synthetic": true}
```

**Кто видит:** только человек (`person-only`).

### Шаг 6. Практика из инструментов линзы и её итог (Practice → `practices`, Outcome → `outcomes`)

Единственный инструмент для самостоятельной работы — `ifs.noticing-a-part`: заметить, назвать своими словами, спросить, что эта часть хочет сообщить, ничего не меняя. В описании стоит `agentMayOffer: false`, поэтому вы его никогда не предлагаете (PC-2). Если человек уже так делает и хочет это сохранить, он записывает практику своими словами как Practice ([§17.1](../../spec/SPECIFICATION.md#171-practice), [схема](../../spec/schema/practice.schema.json)) с `source.route: "from-lens"` и `templateId: "ifs.noticing-a-part"`. `ifs.exile-work` — только со специалистом и здесь никогда не становится практикой.

```json
{"id": "pr-01", "name": "Pause and ask the part",
 "description": "When I notice the pull, I name it in my own words and ask what it wants me to know, without trying to change it.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:ifs", "templateId": "ifs.noticing-a-part"},
 "steps": ["Stop for a minute", "Name the pull in my own words", "Ask what it wants me to know", "Write one line, change nothing"],
 "duration": "PT5M",
 "limits": "Stop if it gets too much. Anything that feels like old hurt goes to a practitioner, not here.",
 "initialStatus": "in-use", "nonClinical": true, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T19:30:00Z", "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "synthetic": true}
```

**Если принятие `therapy-confidential`,** сами добавьте в практику `"handling": ["person-only"]`. У практики нет поля `adoption`, поэтому LA-4 до неё не доходит, и без этой пометки разрешение на линзу её выдаёт (проверено; §6, пункт 8).

Как всё прошло, человек записывает как Outcome ([§17.2](../../spec/SPECIFICATION.md#172-outcome), [схема](../../spec/schema/outcome.schema.json)):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-01", "result": "helped", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-24T21:25:00Z", "synthetic": true}
```

**Кто видит:** пока разрешения нет — только человек. По разрешению, которое называет линзу, практика выдаётся, потому что несёт линзу в `source.lens`. Итог (Outcome) — нет, потому что линзы у него нет; он получает уровень практики.

### Шаг 7. Кто что может видеть (Party → `parties`, Grant → `grants`, Review `relax` → `reviews`)

По умолчанию никто ничего не видит. Если человек хочет, чтобы спутник для размышлений мог использовать его имена частей, сначала добавьте спутника в `parties` (пропустите, если уже сделали это в шаге 1):

```json
{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
```

Приставка id называет вид стороны и проверяется: `a-` — агент, `p-` — человек, `s-` — программа, `o-` — организация. Затем человек даёт узкое разрешение ([§12.1](../../spec/SPECIFICATION.md#121-grant), [схема](../../spec/schema/grant.schema.json)):

- Только `actions: ["read"]` в этом примере: все записи линзы пишет человек. Добавить `suggest` или `infer` с именем линзы — выбор человека (I5); агент и тогда никогда не называет, не придумывает и не толкует части.
- Условие, которое называет линзу (`lenses`), `basis.legal: "explicit-consent"` и срок не больше 180 дней: для записей уровня `special` нужны все три условия (R-G3, R-G10).
- `mode: "summary"`, `interpretations: "subject-endorsed"`, `maxSourceTier: "none"`.

```json
{"id": "g-01", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:ifs"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-28T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"},
 "note": "Use my own part names when I bring them up. Never name, interpret or look for parts yourself."}
```

Само разрешение не открывает ни одной части, потому что части — `person-only`. Человек сам, часть за частью, решает, какую из них спутник может знать, и снимает `person-only` записью Review `relax` ([§11.1](../../spec/SPECIFICATION.md#111-review)):

```json
{"id": "rv-01", "target": "part-01", "action": "relax", "by": "subject", "recordedAt": "2026-10-01T09:05:00Z",
 "disclosure": {"removeHandling": ["person-only"]},
 "note": "The companion may know this part and use its name."}
```

**Что после этого получает спутник.** Из корня репозитория выполните:

```sh
python3 -B tools/ohc_query.py <папка вашего контекста> project --grant g-01 --purpose self-reflection --now latest
```

Для разобранного примера папка — `docs/lenses/examples/ifs`. `--purpose` обязателен и должен быть одной из целей разрешения. `--now latest` считает разрешение на момент самой новой записи в файле, поэтому результат не зависит ни от сегодняшней даты, ни от того, истёк ли с тех пор срок разрешения. Команда печатает две строки (какое время она взяла и какой ключ) и затем выдачу в формате JSON. Выданные записи перечислены в `statements` (здесь `statements.lensAdoptions`: `la-01`; `statements.practices`: `pr-01`), в `experience` (здесь пусто) и в `interpretations` (здесь `interpretations.parts`: `part-01`). В `derived` — вычисленные отметки каждой выданной записи, в `obligations.handling` — ограничения, которые спутник обязан соблюдать (`part-01`: `no-forward`, `no-quote-back`). Спутник не получает `part-02`, толкование `in-01`, эпизод, источник, утверждение, итог и ни одной связи.

### Шаг 8. Проверка

Из корня репозитория:

```sh
python3 -B tools/check.py <папка вашего контекста> --level L1 --json
```

Исправляйте ошибки, пока проверка не сообщит `"valid": true` и `"levelMet": "L1"`. Проверка ещё сравнивает свой вывод с файлом `expected-check.json` рядом (правило X-3), но только когда папка лежит внутри папки с именем `examples`; для папки вашего собственного контекста он не нужен. Проверка не читает хранилище (шаг 2) и не сообщает об отсутствующей записи Review `admit` (шаг 1): проверьте и то и другое сами.

## 4. Никогда

- **Запрещённые цели:** `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` и все остальные цели из [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed), ни по какому разрешению. Толкование служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- **Никаких выводов агента, если человек не разрешил.** Записи с `origin: "inferred"` через эту линзу пишите только по разрешению человека (`infer`, называющее линзу) и при его принятии линзы (I5); в примере `agentInterpretation` равно `off`. И тогда никогда не называйте, не придумывайте и не толкуйте части (`helperMustNot`) и никогда не переводите части или толкования в другую линзу (`crossLensMapping: not-allowed`).
- **Никакой работы с частями со стороны агента.** Никогда не представляйтесь как проводящий IFS-терапию. Никогда не называйте, не придумывайте и не толкуйте части. Никогда не идите к «изгнанникам» и «бременам» и не предлагайте «разгрузку». Никогда не пишите запись Part сами (P-2).
- **Часть — не действующее лицо.** Часть никогда не даёт согласия, не выдаёт разрешений и ничего не разрешает (P-1, C-10). «Эта часть согласна» — не согласие.
- **Никаких предложений без просьбы.** Не называйте линзу, если человек не просил о способах посмотреть на внутренний конфликт (`suggestionRequires`) и разрешение человека не позволяет её предлагать. Никогда не предлагайте `ifs.noticing-a-part` (`agentMayOffer: false`) и `ifs.exile-work` (только со специалистом).
- **Никаких напоминаний против человека.** Никогда не используйте часть против человека, вроде «опять ваш перепроверяльщик» (`no-quote-back`, `no-leverage`).
- **Товарный знак.** Используйте «Internal Family Systems» и «IFS» только чтобы назвать метод, на который ссылается линза, никогда — как ярлык для того, что делает агент, и приводите уведомление выше, когда называете метод.

## 5. Разобранный пример

[examples/ifs/context.json](examples/ifs/context.json) — один файл уровня L1 об Изольде (Ysolde), вымышленном человеке. `"synthetic": true` стоит у самого контекста и у каждой записи с содержанием. В файле ровно записи раздела 3:

| Шаг | Записи |
|---|---|
| 0 | оболочка с модулями `core`, `governance`, `lenses`, `practices`, `inner-system` |
| 1 | `la-01` |
| 2 | `src-01` и его байты в [vault/4f/](examples/ifs/vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md) |
| 3 | `ep-01`, `part-01`, `part-02`, `r-01` |
| 4 | `c-01`, `r-02` |
| 5 | `in-01` |
| 6 | `pr-01`, `oc-01` |
| 7 | сторона `a-01`, `g-01`, `rv-01` |

Варианты из шагов 1, 2 и 6 (терапевт, разрешение специалиста, предложение агента, практика с `person-only`) в файл не входят.

```sh
python3 -B tools/check.py docs/lenses/examples/ifs --level L1 --json
```

Проверка сообщает `"valid": true` и `"levelMet": "L1"`, без ошибок и предупреждений. [expected-check.json](examples/ifs/expected-check.json) — точный вывод. Выдача из шага 7:

```sh
python3 -B tools/ohc_query.py docs/lenses/examples/ifs project --grant g-01 --purpose self-reflection --now latest
```

## 6. Что пока не помещается

Это пробелы OHC 0.1 для этой линзы, найденные при написании рецепта и когда новичок прошёл по нему. К каждому — предложение на следующий проход.

1. **Толкование не может быть о части.** `Interpretation.about` принимает только эпизоды, утверждения, закономерности и записи AssessmentRecord (RF-1); проверка отклоняет там часть. При этом §8.3 и I9 говорят о толковании, чей `about` включает часть. *Предложение:* разрешить `about` → Part, когда объявлен модуль `inner-system`, и согласовать I9 с RF-1.
2. **Имена частей утекают через текст.** Толкование через линзу, где названа часть с `person-only`, уходит по разрешению на линзу, если автор не пометил его отдельно: ограничения части не переходят на текст. *Предложение:* поле `mentions: [id частей]` у толкований и рассказов в эпизодах, которое переносит уровень и ограничения частей (C3); или `person-only` по умолчанию для любого толкования через линзу вида `parts-model`.
3. **Нельзя поделиться только именем.** `uses: speak-in-lens` требует, чтобы агент знал имена частей, но единственный способ — снять `person-only` со всей части записью Review `relax`, и тогда уходят и её описание, намерение, опасение и поводы. *Предложение:* код ограничения или режим разрешения, который отдаёт у части только `name` и `role`.
4. **Толкование специалиста не может нести линзу.** *Исправлено в 0.1.0-draft.2:* LA-7 снято, а I5 применяет `agentInterpretation` только к авторам-агентам и программам; терапевт из `interpretationAuthors` действующего принятия может толковать через линзу.
5. **Каждая запись — «близко к травме».** Категории линзы по умолчанию ставят `trauma-adjacent` на каждую запись, так что и часть, которая перепроверяет цифры, считается близкой к травме; разрешение не может исключить материал «изгнанников» по категории, а каждую подсказку-напоминание должен писать сам человек (RC-2). *Предложение:* категории линзы по умолчанию `["mental-health"]`; `trauma-adjacent` — через `defaults.perConstruct` для `ifs/exile` и `ifs/burden`; проверка выводит категории части из её `role`.
6. **`Part.role` не проверяется.** Проходит любая строка, в том числе `ifs/self`, хотя в этой линзе Я — не часть. *Предложение:* правило, что `role` — понятие линзы этой части, и отметка у понятия (например `notAPartRole`) для `ifs/self`.
7. **Условие предложения не оставляет следа.** Для «человек попросил о способах посмотреть на внутренний конфликт» (`suggestionRequires`) нет места в записях, и принятие `agent-suggested` проходит проверку без этого. *Предложение:* принятие `agent-suggested` ссылается на эпизод, источник или сообщение, где человек попросил (например в `derivedFrom`); проверка предупреждает, если ссылки нет.
8. **Тайна терапии не доходит до практики.** LA-4 (`therapy-confidential` значит `person-only`) передаётся только через поле `adoption`. У Practice и AssessmentRecord такого поля нет, поэтому практика, принесённая из терапии, выдаётся по разрешению на линзу (проверено: `pr-01` выдаётся, хотя `la-01` скрыто). *Предложение:* необязательное поле `adoption` у Practice (путь `from-lens`) и у AssessmentRecord, и LA-4 для них; или применять LA-4 к каждой записи с пометкой линзы (`lens` или `source.lens`), пока действующее принятие этой линзы — `therapy-confidential`, и предупреждать, если такая запись не `person-only`.
9. **Записи на предложенном принятии выдаются.** Если принятие `agent-suggested` и записи Review `admit` нет, само принятие скрыто, но `part-01` и `pr-01` остаются действующими и выдаются по разрешению на линзу, а проверка не предупреждает (проверено). Порог принятия можно обойти, просто написав записи линзы. *Предложение:* записи линзы, чьё `adoption` не действует, наследуют вычисленное состояние принятия (`proposed`); проверка предупреждает (например W-LA-ADM), если запись с пометкой линзы ссылается на недействующее принятие.
10. **Хранилище никогда не проверяется.** Проверка уровня L1 не открывает хранилище: источник, чей файл отсутствует или у которого неверны `size` или `sha256`, проходит (проверено: `size` 999 и отсутствующий файл всё равно дают L1 без ошибок). Неверный хеш потом молча ломает удаление и проверки при повышении уровня доступа. *Предложение:* режим проверки (например `--vault`), который находит `vaultPath` относительно папки контекста и сверяет наличие файла, размер и хеш, сообщая об отсутствующем файле как о предупреждении; и прогонять его по опубликованным примерам, которые теперь содержат свои байты.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
