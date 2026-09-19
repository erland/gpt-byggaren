# Projektkontrakt – `gpt-project.yaml`

## Syfte

`gpt-project.yaml` är det maskinläsbara kontraktet för ett GPT-projekt.

Filen används av:

- GPT Byggaren själv,
- buildscript,
- linter,
- validering,
- GitHub Actions,
- distributionspaketering,
- projektåterupptagning.

## Designprincip

Regler som behöver användas av flera delar av toolchainen ska deklareras här i stället för att dupliceras i Python-script, GitHub Actions och dokumentation.

När löptext och maskinläsbart kontrakt skiljer sig ska `gpt-project.yaml` behandlas som auktoritativ för projektets tekniska konfiguration.

## Huvudsektioner

### `project`

Projektets identitet och språk.

### `development`

Var utvecklingsplan, status och centrala projektdokument finns.

### `structure`

Deklarerar canonical och villkorade kataloger.

### `runtime`

Beskriver distributionsmålen och deras roller, plattformsbegränsningar och runtimekonfiguration.

GPT Byggaren har normalt ingen förvald primär runtime. Chat ZIP och Custom GPT kan deklareras som jämbördiga distributionsmål från samma canonical kontrakt.

### `capabilities`

Beskriver projektets **plattformsneutrala capability-kontrakt**. Kontraktet anger vilka förmågor assistenten behöver, inte vilket produktnamn en viss runtime använder för att realisera dem.

Exempel:

```yaml
capabilities:
  contract_version: 1
  schema: schemas/capability-contract.schema.json
  recommendation_mode: inferred_from_use_case
  requirements:
    web:
      level: recommended
    filesystem:
      read: required
      write: required
    shell:
      level: optional
    code_execution:
      level: required
    structured_data:
      level: required
    persistent_state:
      level: recommended
    external_tools:
      level: optional
      preferred_protocols:
        - mcp
```

Tillåtna nivåer är `required`, `recommended`, `optional`, `not_required` och `to_be_recommended`.

Äldre projekt med fält som `data_analysis`, `file_handling`, `structured_knowledge` och motsvarande ska kunna normaliseras till detta kontrakt utan att källprojektet måste skrivas om direkt. Runtime-adaptrar ansvarar därefter för översättningen till plattformens egna capabilitybegrepp.

### `project_hygiene`

Deklarerar projektets städregler.

### `build`

Deklarerar krav på deterministiskt bygge, manifest, checksummor och direktbyggda artefakter.

### `release`

Beskriver GitHub-baserad releaseautomation och lokal/direct build. För GPT Byggaren är GitHub-stöd standard, medan samma distributionsartefakter också ska kunna byggas utan GitHub. När GitHub Release används är release-taggen versionskälla.

### `artifacts`

Beskriver ett **plattformsneutralt artifact/output-kontrakt**: vad assistenten eller buildkedjan ska producera, oberoende av hur en viss runtime gör resultatet tillgängligt.

Exempel:

```yaml
artifacts:
  contract_version: 1
  schema: schemas/artifact-contract.schema.json
  outputs:
    development_plan:
      kind: document
      format: markdown
      requirement: required
      persistence: persistent
    project_package:
      kind: package
      format: zip
      requirement: required
      persistence: persistent
    runtime_package:
      kind: distribution
      format: zip
      requirement: required
      persistence: persistent
      multiplicity: many
```

Kontraktet skiljer därmed på canonical leveranser och konkreta distributionsfiler. Exempelvis kan både Chat ZIP, Custom GPT, Claude och OpenCode vara realiseringar av samma canonical `runtime_package`.

Begrepp som "nedladdningsbar fil", "länk i chatten" eller en viss plattforms artifact-UI hör hemma i runtime-adaptern och ska inte krävas av canonical kontrakt.

### `workspace_state`

Beskriver assistentens plattformsneutrala krav på arbetsyta och runtime-state.

Exempel:

```yaml
workspace_state:
  contract_version: 1
  schema: schemas/workspace-state-contract.schema.json
  workspace:
    requirement: required
    persistence: required
    portable: true
    separate_from_assistant: true
    artifact: project_package
  state:
    requirement: required
    persistence: required
    authority: workspace_file
    format: yaml
    path: project-status.yaml
    conversation_fallback: false
  runtime_preferences:
    chat: conversation_or_file
    agent: workspace_file
```

Kontraktet skiljer mellan:

- **assistentpaketet** – instruktioner, knowledge, schemas, scripts och runtime-adapter,
- **workspace** – användarens konkreta arbetsprojekt eller arbetsdata,
- **runtime-state** – den status som behövs för att fortsätta ett flerstegsarbete.

Detta får inte förväxlas med GPT Byggarens egen utvecklingsstatus för källprojektet. Ett genererat projekt kan ha `project-status.yaml` som sin runtime-state, men andra assistenter kan använda exempelvis `state/research-state.yaml` eller ingen persistent state alls.

### `tools`

Beskriver assistentens **körbara verktyg** plattformsneutralt. Kontraktet är separat från `capabilities`: en capability beskriver *vad assistenten behöver kunna*, medan ett tool beskriver *en konkret körbar mekanism* som kan realisera en del av behovet.

Exempel:

```yaml
tools:
  contract_version: 1
  schema: schemas/tool-contract.schema.json
  tools:
    - id: validate-model
      type: script
      requirement: required
      purpose: Validera canonical modell.
      script: scripts/validate.py
      deterministic: true
      mutates_workspace: false
      runtime_fallback: block
```

Initialt stöds typerna:

- `script`
- `local_command`
- `mcp`
- `api_action`

En fil under `scripts/` blir **inte automatiskt** ett runtimeverktyg. Verktyg ska deklareras uttryckligen så att utvecklings- och buildscript inte exponeras av misstag.

`required_runtime_dependencies` i core contract fortsätter beskriva nödvändiga **filer/beroenden**, medan `tools` beskriver körbara operationer.

### `workflow`

Beskriver den centrala arbetsmodellen:

```text
idé → analys → plan.md → projekt-ZIP → stegvis utveckling → distribution
```

## Viktigt om plattformsgränser

Custom GPT-gränser lagras som konfiguration:

```yaml
platform_limits:
  instruction_max_characters: 8000
  knowledge_max_files: 20
```

De ska inte dupliceras som styrande värden på flera ställen i projektet.

Om plattformsgränser ändras ska konfiguration och validering kunna uppdateras utan att canonical beteende behöver skrivas om.

## Projektstatus och progression

Projektstatus representeras maskinläsbart i `project-status.yaml` och kompletteras av den mänskligt läsbara `STATUS.md`.

Vid återupptagning ska maskinläsbar status vara auktoritativ. Utvecklingsplanen är vägledande och nästa steg ska rekommenderas utifrån faktisk projektstatus, blockerare och valideringsresultat.

## Core behavior contract

För nya projekt bör `gpt-project.yaml` innehålla `instructions.core_contract`. Kontraktet gör kritiska beteenden och obligatoriska filberoenden verifierbara utan att skapa en separat runtime för enklare modeller.

Rekommenderad baslinje:

```yaml
instructions:
  canonical: src/instructions/system.md
  core_contract:
    enabled: true
    required_markers:
      - "<kort kritisk invariant>"
    required_runtime_dependencies: []
    max_required_file_hops: 1
    knowledge_may_not_be_required_for_core_behavior: true
```

Markörerna ska representera verkligt obligatoriska beteenden. De är ett regressionsskydd, inte en full kopia av systeminstruktionen.
