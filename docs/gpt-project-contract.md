# Projektkontrakt – `gpt-project.yaml`

## Syfte

`gpt-project.yaml` är det maskinläsbara kontraktet för ett GPT-projekt.

Filen ska på sikt användas av:

- GPT Byggaren själv,
- buildscript,
- linter,
- validering,
- GitHub Actions,
- distributionspaketering,
- projektåterupptagning.

## Designprincip

Regler som behöver användas av flera delar av toolchainen ska deklareras här i stället för att dupliceras i Python-script, GitHub Actions och dokumentation.

## Huvudsektioner

### `project`

Projektets identitet och språk.

### `development`

Var utvecklingsplan, status och centrala projektdokument finns.

### `structure`

Deklarerar canonical och villkorade kataloger.

### `runtime`

Beskriver primär runtime och distributionsmål.

### `capabilities`

Anger att capabilities normalt ska rekommenderas utifrån användningsfallet i stället för att frågas fram tekniskt.

### `project_hygiene`

Deklarerar projektets städregler.

### `build`

Deklarerar krav på deterministiskt bygge, manifest, checksummor och direktbyggda artefakter.

### `release`

Anger att GitHub är valfritt och att GitHub Release-taggen är versionskälla när GitHub används.

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

De ska inte dupliceras på flera ställen i projektet.

När toolchainen senare byggs ska dessa värden vara lätta att uppdatera.

## Nästa utvecklingssteg

Steg 4 ska definiera hur projektstatus och planprogression representeras maskinläsbart och hur `STATUS.md` relaterar till detta kontrakt.
