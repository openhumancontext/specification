# Процессуальный подход: рецепт

**Рецепт · линза `urn:ohc:lens:process-work` 0.2.0 · OHC 0.1.0-draft.2 · информативный · 12 октября 2026**

Рецепт показывает, как человек переносит в свой контекст OHC то, что у него есть из процессуальной работы (свои заметки, резюме практика, свои прочтения и практики), и что агенту можно и нельзя с этим делать.

> **Эта линза — заготовка.** У её описания ([spec/lenses/process-work.lens.json](../../spec/lenses/process-work.lens.json)) `descriptorStatus: stub`: подход назван, но в описании нет ни конструктов, ни набора инструментов, ни представлений, ни опросников. Поэтому в рецепте остались только безопасные шаги: принятие линзы, слова самого человека, исходные материалы, его собственные прочтения и практики, доступ для других. **Ни AssessmentRecord, ни ModelView** здесь не пишутся, и в примере **ни один агент не толкует через эту линзу**: человек оставляет `agentInterpretation: off` (I5).

**Факты, а не разрешения (0.1.0-draft.2).** Описание линзы несёт факты и рекомендации, но не разрешения. Предлагает ли агент эту линзу, читает ли через неё, предлагает ли её инструменты и учитывает ли её результаты в том, что предлагает человеку, решает договорённость человека с ним: разрешение, чья область называет линзу (`suggest`, `infer`; `decisionUse`, R-G14), суженное принятием линзы (`agentInterpretation`) и кодами обращения ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). Запрещённые цели ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) защищают человека от решений других и связывают любого получателя; ни одна запись не несёт их копию.

**Способы работы.** Описание называет один плейбук, [`urn:ohc:playbook:process-work-basic`](../../spec/playbooks/process-work-basic.playbook.json) («Процессуальный подход: базовые способы работы», редакция OHC), для таких ситуаций: под нагрузкой: усталость, давление или перегрузка; после неудачи; разбор того, что произошло. Агент получает его в начале сессии вместе с записями человека в этой линзе, выполняет шаг только в пределах разрешения и никогда не ставит шаг выше того, что человек говорит сейчас (PB-4, PB-5). Человек может выбрать другие плейбуки или ни одного в поле `playbooks` принятия линзы (PB-3); собственный способ работы коуча или терапевта с линзой приходит как местный плейбук (`urn:ohc:playbook:x-<namespace>:<name>`) и хранится в контексте человека.

## 1. Что у вас может быть

| Что есть | Подходит? | Куда это идёт |
|---|---|---|
| Рассказ человека о себе в разговоре: что он замечает (сигнал тела, движение, сон, «что-то, что хочет проявиться») | да | Claims (шаг 3) и Episodes (шаг 4), словами человека |
| Собственные заметки человека после сессии | да | Source вида `note` или `journal-entry` (шаг 2), на него ссылается Episode |
| Заметки или резюме его практика (терапевта, коуча, ведущего) | да, с разрешением практика | Source вида `practitioner-notes` под защитой конфиденциальности и Source вида `practitioner-release` (шаг 2) |
| Прочтение практика в пересказе человека | да, как прочтение самого человека | Interpretation от человека с основанием вида `practitioner` (шаг 5; почему не от имени практика — в разделе 6) |
| Практика, которой человек научился в этой работе или нашёл сам | да | Practice и её Outcomes (шаг 6) |
| Отчёт опросника | **нет** | у линзы нет опросников |
| Прочтение агента через линзу | **только по разрешению человека** | `infer`, называющее линзу, и действующее принятие линзы не в `off` (I5); прочтения в заготовке остаются `frame-relative`. Рекомендация описания: не проводить по ней упражнений. В примере человек не разрешает ничего из этого. |

## 2. Перед началом

**Путь принятия линзы.** Описание разрешает три пути (`adoption.routes`).

| Путь | Кто пишет LensAdoption | Что это меняет |
|---|---|---|
| `self-chosen` | сам человек (`assertedBy: "subject"`) | Действует сразу. |
| `inherited-from-practice` | сам человек | Нужен блок `practice`: роль практика, практик как Party, `relationship` (`active` или `ended`), `since` и `releaseRef`, если хранятся материалы сессий (LA-3). Выберите `confidentiality`: `practitioner-scope` или `therapy-confidential`. При `therapy-confidential` хранитель сам ставит уровень `special` и ограничение `person-only` на принятие и на каждую Interpretation, AssessmentRecord или ModelView, у которой `adoption` — это принятие (LA-4). На Claims, Episodes, Sources, Practices и Outcomes это **не** распространяется: если выбрали этот вариант, добавьте `"handling": ["person-only"]` вручную в `c-01`, `ep-01`, `src-02`, `src-03`, `pr-01` и `oc-01`. Тогда разрешение из шага 7 выдаст только `c-02`. `onEnd` оставьте `ask`: когда отношения с практиком закончатся, принятие встанет на паузу, пока человек не решит. |
| `agent-suggested` | агент, как предложение | Только по разрешению с `suggest`, называющему линзу; рекомендация описания (`suggestionRequires`): агент может назвать подход, только если человек сам попросил другие способы взглянуть на свой опыт, и только как один вариант из нескольких. Он пишет принятие по разрешению с действием `suggest`, и оно остаётся предложением, пока человек его не примет (LA-1). Этот путь шаг за шагом показан в [рецепте когнитивной оценки](cognitive-appraisal.ru.md). |
| `imported` | — | Недоступен: импортировать не из чего, опросников нет. |

**Согласие.** Человек решает, принимать ли линзу, что хранить и кому показывать. Без Grant ничего не уходит из контекста (R-G1). Разрешающий Grant, который достаёт до записей этой линзы, даётся с `basis.legal: "explicit-consent"` и истекает не позже чем через 180 дней от своего `recordedAt` (R-G10, R-G11, GR-1). У отказа (`effect: deny`) предела срока нет.

**Умолчания линзы** (`defaults`): уровень чувствительности `special`, категория `mental-health`, `reviewAfter: on-change`.

- LensAdoption и каждая Interpretation, где указана линза, получают `special` сами (умолчание линзы; I9).
- Claims и Sources остаются на том уровне, который вы записали. Source не бывает ниже `sensitive`, а Source под `custody` сам становится `special`. На каждый Claim и Source, где есть материал этой работы, поставьте `"sensitivity": "special"` и `"categories": ["mental-health"]` вручную. Разрешение практика `src-01` не содержит материала сессий и остаётся `sensitive`.
- Practice тоже не поднимается сама: её `source.lens` позволяет селектору `lenses` в разрешении найти её, но умолчания линзы к ней не применяет. Уровень и категорию поставьте вручную.
- Outcome о практике уровня `special` и Episode, основанием которого служит Source уровня `special`, наследуют `special` по C3 (§8.4). На Episode его всё равно можно написать для ясности; у `oc-01` в шаге 6 его нет, и он всё равно `special`.
- `agentInterpretation` равно `"off"` — значение по умолчанию, которое человек здесь оставляет (I5). `interpretationAuthors` равно `["subject"]`.
- `uses`: `speak-in-lens` и `interpret` (прочтения самого человека). Не `offer-practices` (набора инструментов нет) и не `store-results` (нет формы результата).

**Что не хранится никогда.** Учебные материалы, сценарии упражнений и тексты метода; заметки практика сверх того, что позволяет его разрешение (`practitioner-release`); ярлыки из другой линзы или опросника, пересказанные языком этой линзы; любой балл, тип или вердикт о человеке; прочтение агента через линзу.

**Пометка «вымышлено».** В примерах (контекст, чей `id` начинается с `urn:ohc:example:`, или любая папка `examples` в пути) поставьте `"synthetic": true` на сам Context и на каждый Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice и Outcome (X-1, CX-8). Никогда не ставьте его на Grant, Proposal, Review или Event и на Party: их схемы это запрещают (S-3). Для реального человека не ставьте его нигде.

## 3. Шаги

**0. Создайте файл контекста.** Заведите папку для контекста и создайте в ней `context.json` (контекст одним документом). Начните с такой заготовки:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-05T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:process-work", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` и `subject` обязательны. Меняйте `version` при каждом изменении файла.
- `conformance.subjectIsAdult: true` — заявление хранителя, что человек взрослый и решает за себя сам. Без него проверка отклоняет любое заявление о соответствии (R-C4), и `levelMet` равно `null`. Без `conformance.level` проверка проверяет только L0.
- `modules`: всегда `core` и `lenses`, `governance` — для разрешения (шаг 7), `practices` — для практики (шаг 6).
- `lenses` закрепляет описание линзы, которым пользуется контекст.
- Каждая запись ниже ложится в массив верхнего уровня, названный по её коллекции: `lensAdoptions`, `sources`, `claims`, `episodes`, `interpretations`, `practices`, `outcomes`, `grants`. Каждая Party ложится в `parties`.
- В примере берите id вида `urn:ohc:example:<имя>:process-work` (контекст) и `urn:ohc:example:<имя>` (человек) и добавьте `"synthetic": true` на сам Context (см. раздел 2).

**1. Примите линзу.** Человек говорит, что работает в этом подходе. Добавьте практика в `parties` с ролью вместо имени: `{"id": "p-01", "partyKind": "person", "label": "Practitioner", "role": "practitioner"}`. Затем запишите **LensAdoption** (коллекция `lensAdoptions`):

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:process-work", "version": "0.2.0"},
 "route": "inherited-from-practice",
 "practice": {"role": "therapist", "practitioner": "p-01", "relationship": "active", "since": "2025-11-01",
              "releaseRef": "src-01"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"]}
```

Кто видит по умолчанию: только сам человек. Принятие линзы не даёт практику никакого доступа (LA-2).

**2. Положите исходники в хранилище.** Папка `vault/` лежит рядом с `context.json`, и каждый `vaultPath` отсчитывается от папки, где лежит `context.json`. Для каждого файла (разрешение практика, заметка самого человека, резюме практика):

1. посчитайте sha256 его байтов командой `shasum -a 256 <файл>` (или `sha256sum <файл>`) и размер в байтах командой `wc -c < <файл>`;
2. сохраните файл как `vault/<первые два шестнадцатеричных знака>/<sha256>.<расширение>`;
3. запишите **Source** (коллекция `sources`) с этим путём, хешем и размером.

Проверка не открывает хранилище (в её отчёте `"vaultContentRead": false`). Пропавший файл, неверный хеш или размер всё равно пройдут шаг 8, поэтому сверьте путь, `sha256` и `size` сами до шага 8.

Разрешение:

```json
{"id": "src-01", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/f8/f80a523bdc2eebff12a5884e805cc272be41e389d56f07d5ec2ff520dca2252e.md"},
             "sha256": "f80a523bdc2eebff12a5884e805cc272be41e389d56f07d5ec2ff520dca2252e",
             "mediaType": "text/markdown", "size": 174},
 "authorship": {"author": "p-01"}, "inbound": true, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:00:00Z",
 "sensitivity": "sensitive"}
```

Резюме практика хранится под его конфиденциальностью (`custody`). `custody.confidentiality` выбирайте по роли практика в принятии линзы (`practice.role`):

| `practice.role` | `custody.confidentiality` | Предел для получателей без разрешения / с разрешением (§15.3) |
|---|---|---|
| `therapist` | `therapy` | `index` / `summary` |
| `coach` | `coaching` | `index` / `excerpt` |
| `facilitator`, `teacher` или `other` | `therapy`, если сессии терапевтические, иначе `coaching` | как выше |

В любом случае оставьте `maxRelease` равным `index`.

```json
{"id": "src-03", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/f0/f019f7f2face1e47c00a3739818e5eaf79fe0a06d7d4dec3df3457391bce52cc.md"},
             "sha256": "f019f7f2face1e47c00a3739818e5eaf79fe0a06d7d4dec3df3457391bce52cc",
             "mediaType": "text/markdown", "size": 214},
 "capturedAt": "2026-09-13T10:00:00Z", "authorship": {"author": "p-01"}, "inbound": true, "maxRelease": "index",
 "custody": {"custodian": "p-01", "confidentiality": "therapy", "releaseRef": "src-01"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-13T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Собственная заметка человека после сессии:

```json
{"id": "src-02", "sourceKind": "note",
 "content": {"locator": {"vaultPath": "vault/2e/2ec43e0965b6a0221313c116fabf00043b1c17679d145430e6e39faa7d935802.md"},
             "sha256": "2ec43e0965b6a0221313c116fabf00043b1c17679d145430e6e39faa7d935802",
             "mediaType": "text/markdown", "size": 229},
 "capturedAt": "2026-09-12T20:00:00Z", "authorship": {"author": "subject"}, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Кто видит Sources по умолчанию: только сам человек, ему всегда доступно всё (V-0). Никто из получателей не получит больше, чем `maxRelease`, а конфиденциальность практика ограничивает ещё сильнее: для `therapy` без разрешения — `index`, с разрешением — `summary` (§15.3).

**3. Запишите, что человек говорит о себе.** Каждое утверждение — это **Claim** (коллекция `claims`) словами самого человека. Описание себя:

```json
{"id": "c-01", "facet": "identity", "predicate": "self-description",
 "text": "I work with a process-oriented therapist. I pay attention to body signals and dreams that do not fit how I usually see myself.",
 "horizon": "focus", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Как агентам обращаться с этим материалом — это граница. В ней нет внутреннего материала, поэтому она может остаться на уровне по умолчанию и дойти до любого агента, которого выберет человек:

```json
{"id": "c-02", "facet": "boundary", "predicate": "never",
 "text": "Do not explain my body signals or dreams to me. Ask what I notice.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:12:00Z"}
```

Кто видит по умолчанию: только сам человек.

**4. Запишите, что произошло.** Одно событие — это **Episode** (коллекция `episodes`) с рассказом человека, разделённым на «что произошло», «что переживалось», «что сделано» и «как понималось тогда». Позднее прочтение сюда не пишется (EP-4).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-12", "precision": "day"}, "participants": ["p-01"],
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-12T20:00:00Z", "addedAt": "2026-09-12T20:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "While I talked about moving flats, my left hand kept pushing against my knee.",
    "experienced": "Pressure in the hand; more curious than worried.",
    "didOrTried": "Let the hand push against a cushion for about a minute.",
    "understandingThen": "Just restlessness.",
    "evidence": [{"source": "src-02", "selector": {"type": "whole"}}]}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Кто видит по умолчанию: только сам человек.

**5. Собственное прочтение человека через линзу.** Человек читает эпизод в понятиях линзы: это **Interpretation** (коллекция `interpretations`) со `stance: lens-reading`. Если прочтение пришло от практика, человек пишет его своими словами и добавляет основание вида `practitioner` со ссылкой на заметки практика. Альтернативы для самого человека необязательны, но их стоит добавить.

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:process-work", "version": "0.2.0"}, "adoption": "la-01",
 "text": "The pushing hand looks like a less familiar side of me that wants to push back about the move.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"},
             {"span": {"source": "src-03", "selector": {"type": "whole"}}, "kind": "practitioner"}],
 "alternatives": [{"text": "Two short nights before the session; the hand may just have been tired.", "kind": "physiological"}],
 "heldDuring": {"from": "2026-09-14"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T08:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Кто видит по умолчанию: только сам человек. В примере агент такую запись не пишет: при `agentInterpretation: off` и только самом человеке в `interpretationAuthors` проверка отклоняет любое прочтение не от самого человека, где указана эта линза (I5).

**6. Практика, которой человек уже пользуется.** Это **Practice** (коллекция `practices`) словами человека, с указанием, откуда она. Добавьте `handling: ["subject-initiated-only"]`, чтобы агент пользовался ею, только когда человек сам о ней заговорит.

```json
{"id": "pr-01", "name": "Hand against the cushion",
 "description": "When my hand starts pushing in a hard conversation, I let it push against something for a minute and notice what it would say.",
 "practiceKind": "movement",
 "source": {"route": "from-practitioner", "lens": "urn:ohc:lens:process-work", "by": "p-01"},
 "steps": ["Notice the hand", "Let it push against a cushion or a wall for about a minute", "Write one line: what would it say?"],
 "limits": "Not in meetings. If it gets too strong, stop and bring it to the next session.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T08:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only"]}
```

Попробовав практику, человек оценивает её в **Outcome** (коллекция `outcomes`):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "partly",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T19:00:00Z"}
```

Кто видит по умолчанию: только сам человек.

**7. Кто что может видеть.** **Grant** (коллекция `grants`) для собеседника-помощника в размышлениях: только чтение, для самоосмысления, только собственные прочтения человека. Селектор `lenses` достаёт до LensAdoption, Interpretations и Practice (через `source.lens`). У Claims и Episodes линзы нет, поэтому они названы по `ids`.

```json
{"id": "g-01", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:process-work"]}, {"ids": ["c-01", "c-02", "ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-29T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"}}
```

Получатель — это Party (`{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`). С таким разрешением агент может говорить словами человека, соблюдать границу `c-02` и пользоваться практикой, только когда человек начнёт сам. Ни `suggest`, ни `infer` он не получает: через эту линзу ему нечего предлагать. Outcome не выдаётся: разрешение его не называет.

**8. Проверьте.** Сначала сверьте хранилище вручную (шаг 2). Затем запустите `python3 -B tools/check.py <папка вашего контекста> --level L1 --json`. Ожидается `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений. Что значат ошибки:

- `R-C4`: нет `conformance.subjectIsAdult` (шаг 0).
- `X-1` или `CX-8`: включён режим примера (id контекста начинается с `urn:ohc:example:` или в пути есть папка `examples`), а у записи с содержанием или у самого Context нет `"synthetic": true` (раздел 2).
- `S-3` на Grant: в нём стоит `synthetic`, а его схема это запрещает.
- `I5`: прочтение не от самого человека указывает эту линзу без разрешения или принятия, которые это позволяют.

## 4. Никогда

- Агент толкует через эту линзу только по разрешению человека (`infer`, называющее линзу) и при его принятии линзы (I5); его прочтения остаются `frame-relative`, и упражнений по заготовке он не проводит. В примере человек не разрешает ничего из этого.
- Агент упоминает подход только по разрешению, которое позволяет предлагать линзу, только если человек попросил другие способы взглянуть, и только как один вариант из нескольких (`suggestionRequires`); языком подхода он говорит словами самого человека, когда тот принял линзу (`agentPosture`).
- Агент не проводит упражнений из подхода, не выдаёт себя за практика этого подхода и не превращает сохранённую Practice в предложение, которого человек сам не начинал. Работа с переживанием может поднять сильный материал; глубокая работа — дело практика (`riskNotes`).
- Ничто из этой линзы не используется для отбора персонала, распределения задач, оценки работы, решений о повышении, сравнения людей между собой, подбора убеждения под психологию человека и других запрещённых целей (§8.10), ни по какому разрешению. Прочтение служит основанием для выбора, который вы предлагаете человеку, только при `decisionUse: approval-required`, только если человек его принял, и с указанием, что вы учли (R-G14).
- Ничто из линзы не переводится в другую линзу (`crossLensMapping: not-allowed`), и прочтение в ней никогда не выдаётся за эмпирический факт (C-7).
- Нельзя описывать внутренние состояния практика или других участников, например в групповой работе (TP-1).
- В описании нет товарных знаков. Пишите просто «процессуальный подход»; не копируйте в записи учебные тексты и сценарии упражнений подхода.

## 5. Разобранный пример

[examples/process-work/context.json](examples/process-work/context.json) — контекст одним документом уровня L1 об Орсолье, она вымышлена. В нём ровно записи из раздела 3: LensAdoption `la-01`; Sources `src-01` (разрешение), `src-02` (её заметка) и `src-03` (резюме практика); Claims `c-01` и `c-02`; Episode `ep-01`; её прочтение `in-01`; Practice `pr-01` и её Outcome `oc-01`; Grant `g-01`. В папке также три синтетических файла хранилища и `expected-check.json`: проверка сравнивает с ним свой вывод для любой папки примера.

```sh
python3 -B tools/check.py docs/lenses/examples/process-work --level L1 --json
```

Результат: `"valid": true`, `"levelMet": "L1"`, ни ошибок, ни предупреждений.

## 6. Что пока не помещается

1. **Прочтение практика нельзя записать с линзой от имени практика.** *Исправлено в 0.1.0-draft.2:* LN-10 снято, а I5 применяет `agentInterpretation` только к авторам-агентам и программам, поэтому практик из `interpretationAuthors` действующего принятия может быть автором прочтения. Пример сохраняет обход из шага 5: прочтение самого человека с основанием вида `practitioner`.
2. **Записи без поля линзы.** Claims, Episodes, Sources и Outcomes не могут сказать, что относятся к этой линзе. Селектор `lenses` до них не достаёт, поэтому в каждом разрешении их приходится перечислять по id, а уровень и категорию линзы ставить вручную.
3. **Внутренние события.** Сны, сигналы тела и жесты — главный материал этого подхода. У Episode нет способа сказать, что событие внутреннее: `happened` определено как наблюдаемые события, а в `experienced` теряется само событие.
4. **У заготовки нет формы результата и набора инструментов.** [LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses) говорит, что человек может хранить результаты в заготовке, но ни конструкты, ни представления не говорят, что такое результат. Практики из этой работы можно записать только как обычные Practice, а то, что агент не будет их предлагать, держится на том, что человек не забыл поставить `subject-initiated-only`.
5. **`therapy-confidential` защищает только слой прочтений.** LA-4 достаёт только до записей с полем `adoption`. Claims, Episodes, Sources, Practices (связанные с линзой только через `source.lens`) и Outcomes с тем же материалом терапии остаются доступными для разрешений, пока человек не поставит `person-only` на каждую из них (раздел 2). Человек, выбравший `therapy-confidential`, вправе ждать, что весь этот материал будет виден только ему.
6. **`subjectIsAdult` обязателен, но схема об этом молчит.** В `context.schema.json` поле `conformance.subjectIsAdult` необязательное, а проверка без него отклоняет любое заявление о соответствии (R-C4). Агент, у которого есть только схемы, об этом не узнает.
7. **Хранилище не проверяется.** Проверка не открывает `vaultPath`, поэтому пропавший файл, неверный `sha256` или неверный `size` всё равно проходят L1. Шаг 2 просит человека сверить это вручную.
8. **Роли практика и виды конфиденциальности не совпадают.** `practice.role` допускает `facilitator`, `teacher` и `other`, а у `custody.confidentiality` есть только `therapy`, `coaching`, `legal` и `medical`. Таблица в шаге 2 — догадка этого рецепта, а от выбора зависит предел выдачи.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
