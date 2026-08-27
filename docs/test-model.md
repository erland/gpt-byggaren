# Testmodell – GPT Byggaren

## Syfte

GPT Byggaren ska skapa rätt typ av tester för rätt typ av GPT-projekt.

Alla kvalitetsproblem kan inte fångas av vanliga enhetstester. Testmodellen skiljer därför mellan:

1. deterministiska tester,
2. kontrakts- och schematester,
3. build- och distributionstester,
4. runtime smoke tests,
5. beteendeevalueringar,
6. regressionsfall,
7. referensfallsvalidering.

Grundprincip:

> Deterministiska fel ska fångas deterministiskt. Beteendekvalitet ska utvärderas som evals.

## Testlager

### 1. Deterministiska tester

Lämpligt för sådant där samma input alltid ska ge samma resultat.

Exempel:

- parserfunktioner,
- transformationsscript,
- filklassificering,
- versionslogik,
- manifest,
- checksummor,
- template-rendering.

Placering:

```text
tests/
```

### 2. Kontrakts- och schematester

Kontrollerar att maskinläsbara resurser följer projektets kontrakt.

Exempel:

- `gpt-project.yaml`,
- `project-status.yaml`,
- runtime manifests,
- analysrekommendationer,
- paritetsrapporter,
- leveransmanifest.

### 3. Build- och distributionstester

Kontrollerar att:

- projekt-ZIP byggs,
- Chat ZIP byggs,
- Custom GPT ZIP byggs,
- obligatoriska filer finns,
- förbjudna filer inte följer med,
- validering passerar.

### 4. Runtime smoke tests

Bekräftar att en runtime åtminstone kan initialiseras och att dess centrala resurser finns.

Exempel:

```text
START-HERE.md finns
assistant/instructions.md finns
Knowledge-manifest kan läsas
runtime scripts startar
```

### 5. Beteendeevalueringar

Används när utfallet inte kan bedömas med vanlig `assert`.

Exempel:

- följer GPT:n arbetsflödet?
- frågar den bara när ett verkligt verksamhetsval saknas?
- använder den rätt detaljnivå?
- väljer den rätt runtimeprofil?
- separerar den fakta från rekommendation?
- följer den outputformatet?

Placering:

```text
evals/
```

### 6. Regressionsfall

När ett verkligt fel upptäcks ska det om möjligt bli ett permanent test- eller evalfall.

Princip:

```text
bugg
  ↓
reproducerbart fall
  ↓
fix
  ↓
regressionstest
```

### 7. Referensfallsvalidering

För GPT Byggaren är referensprojekt särskilt viktiga.

Exempelprofiler:

- enkel GPT,
- standard-GPT,
- ZIP-first avancerad GPT,
- workflow/research-heavy GPT.

Dessa används för att kontrollera att analys- och planeringsmodellen ger rimliga arkitekturval.

## Skillnad mellan test och eval

### Test

Använd när rätt svar kan fastställas exakt.

Exempel:

```python
assert knowledge_file_count <= max_files
```

### Eval

Använd när kvalitet måste bedömas mot kriterier.

Exempel:

```text
Scenario:
En användare vill skapa en GPT för remissanalys.

Kriterier:
- ZIP-first rekommenderas
- webbresearch rekommenderas
- strukturerad Knowledge rekommenderas
- Custom GPT beskrivs som sekundär
- användaren frågas inte om tekniska schemas
```

## Eval-format

Ett evalfall bör minst innehålla:

```yaml
id: analysis-zip-first-001
title: Avancerad workflow-GPT
input:
  idea: ...
expected:
  required:
    - ...
  forbidden:
    - ...
scoring:
  pass_threshold: 0.8
```

## Testnivå per projektprofil

### Simple

Normalt:

- schema/kontrakt,
- build smoke test,
- några kärnevals.

### Standard

Normalt:

- deterministiska tester,
- schema,
- build,
- runtime smoke,
- centrala beteendeevalueringar.

### ZIP-first advanced

Normalt:

- alla ovan,
- script- och querytester,
- strukturerad data,
- runtime integration,
- paritetskontroll,
- fler regressionsfall.

### Workflow/research-heavy

Normalt:

- arbetsflödesevals,
- källa/evidens-evals,
- outputstruktur,
- felhantering,
- återupptagning,
- runtime parity.

## Kritikalitet

Testfall och evals kan märkas:

- `critical`
- `important`
- `optional`

Release ska blockeras när critical tester eller evals fallerar.

## Testmanifest

Projektet ska kunna ha ett maskinläsbart manifest:

```yaml
schema_version: 1

suites:
  deterministic:
    path: tests/
    blocking: true

  behavioral:
    path: evals/
    blocking: true
```

## CI

CI ska köra deterministiska tester automatiskt.

Beteendeevalueringar kan senare köras:

- i CI när de är automatiserbara,
- i särskilt evalflöde,
- inför release candidate.

## Release gate

Minimikrav för release:

- alla critical deterministiska tester PASS,
- alla blockerande schemas PASS,
- build PASS,
- distributionsvalidering PASS,
- critical evals över definierad tröskel.

## Project hygiene

Tester och evals är development-material och ska normalt inte följa med runtime-distributioner.

De ska finnas kvar i projekt-ZIP och Git.

## Definition of Done

Testmodellen är klar när:

- deterministiska tester och evals är tydligt separerade,
- testnivå kan anpassas efter projektprofil,
- regressionsstrategi finns,
- kritikalitet finns,
- release gate finns,
- CI-rollen är definierad,
- maskinläsbart testmanifest finns.
