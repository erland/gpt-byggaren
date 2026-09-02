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

Anger att capabilities normalt ska rekommenderas utifrån användningsfallet i stället för att frågas fram tekniskt.

### `project_hygiene`

Deklarerar projektets städregler.

### `build`

Deklarerar krav på deterministiskt bygge, manifest, checksummor och direktbyggda artefakter.

### `release`

Beskriver GitHub-baserad releaseautomation och lokal/direct build. För GPT Byggaren är GitHub-stöd standard, medan samma distributionsartefakter också ska kunna byggas utan GitHub. När GitHub Release används är release-taggen versionskälla.

### `artifacts`

Beskriver vilka leveranser en färdig GPT normalt ska producera.

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
