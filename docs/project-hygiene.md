# Filklassificering och Project Hygiene – GPT Byggaren

## Syfte

GPT Byggaren ska aktivt hålla GPT-projekt rena under stegvis utveckling.

Problemet som modellen ska lösa är att iterativt arbete lätt skapar:

- tillfälliga analysfiler,
- gamla instruktioner,
- ersatta Knowledge-utkast,
- testoutput,
- lokala byggartefakter,
- caches,
- parallella versioner av samma canonical source.

Git ska vara historiken. Projektets aktuella HEAD ska representera den bästa nuvarande strukturen.

## Filklasser

Varje relevant fil eller katalog ska kunna klassificeras i en av följande kategorier.

### `CANONICAL`

Källan som ska vidareutvecklas och förvaltas.

Exempel:

- `src/instructions/system.md`
- canonical Knowledge
- schemas som utgör projektkontrakt
- centrala templates

Regel:
Det ska normalt bara finnas en canonical source för samma ansvar.

### `RUNTIME`

Filer som behövs av en runtime-distribution.

Exempel:

- `START-HERE.md`
- runtime policies
- Knowledge-filer i Chat ZIP
- scripts som används av runtime
- templates som används under körning

En runtimefil kan genereras från canonical source.

### `DEVELOPMENT`

Filer som behövs för att utveckla eller verifiera projektet men inte för att köra GPT:n.

Exempel:

- tester
- evals
- research
- utvecklingsdokumentation
- CI-konfiguration

### `GENERATED`

Filer som kan byggas om deterministiskt.

Exempel:

- `build/`
- `dist/`
- genererad Custom GPT Knowledge bundle
- manifest
- checksummor
- release-ZIP

Regel:
Generated ska inte bli canonical source.

### `TEMPORARY`

Tillfälliga filer som skapats för ett pågående steg.

Exempel:

- analysutkast,
- jämförelser,
- konverterade mellanformat,
- tillfälliga paket,
- lokala debugfiler.

Regel:
Ska tas bort när de inte längre behövs för aktuellt arbete.

### `HISTORICAL`

Äldre versioner som endast finns kvar för historik.

Exempel:

- `instructions-old.md`
- `knowledge-v2.md`
- `before-refactor.yaml`
- `step-14-notes-final-final.md`

Regel:
Ska normalt tas bort från HEAD eftersom Git bevarar historiken.

## Klassificeringsmetadata

GPT-projekt ska kunna deklarera katalogroller maskinläsbart.

Exempel:

```yaml
file_classes:
  canonical:
    - src/
    - knowledge/
    - templates/
    - schemas/
  development:
    - tests/
    - evals/
    - research/
    - docs/
  generated:
    - build/
    - dist/
```

Enskilda undantag ska kunna deklareras om en katalog innehåller flera roller.

## Hygiene-kontroller

GPT Byggaren ska kontrollera minst följande.

### 1. Historiska kopior

Identifiera namn som antyder ersatta versioner:

- `old`
- `backup`
- `bak`
- `copy`
- `v2`, `v3` när parallella versioner saknar tydligt skäl
- `final-final`
- `before-*`
- `previous`

Dessa ska granskas, inte automatiskt raderas enbart på namn.

### 2. Temporära filer

Identifiera:

- `*.tmp`
- `*.temp`
- swapfiler
- lokala konverteringsfiler
- arbetskopior

### 3. Caches

Exempel:

- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.DS_Store`

### 4. Lokala testresultat

Exempel:

- coverage output
- junit XML
- snapshots som inte är canonical testdata
- lokala loggar

### 5. Gamla distributionsartefakter

Gamla ZIP-filer och releaseartefakter ska inte blandas med canonical source.

### 6. Duplicerade canonical sources

GPT Byggaren ska leta efter flera filer som verkar beskriva samma instruktion, policy eller modell.

Detta kräver semantisk bedömning, inte bara filnamn.

### 7. Döda referenser

Om en fil tas bort ska referenser från:

- README,
- PROJECT,
- gpt-project.yaml,
- project-status.yaml,
- scripts,
- docs

uppdateras.

## Säker städning

GPT Byggaren ska inte radera filer aggressivt endast för att de ser gamla ut.

Före borttagning ska den bedöma:

1. används filen av runtime?
2. används filen av build?
3. används filen av tester?
4. refereras filen av projektkontrakt?
5. är filen enda källan för viss information?
6. finns innehållet redan i canonical source?
7. bevarar Git historiken?

## Löpande hygiene

Efter varje utvecklingssteg ska GPT Byggaren:

1. inventera nya och ändrade filer,
2. klassificera deras roll,
3. identifiera ersatta filer,
4. ta bort säkert identifierade temporära artefakter,
5. uppdatera brutna referenser,
6. dokumentera vad som rensats,
7. uppdatera status.

## Checkpoint hygiene

Vid större arkitektursteg ska GPT Byggaren göra en djupare kontroll av:

- dubbla policies,
- duplicerad Knowledge,
- flera canonical instruktioner,
- obsolete schemas,
- scripts som inte längre används.

## Final hygiene

Före release ska följande gälla:

- inga temporära filer,
- inga onödiga historiska kopior,
- inga caches,
- inga lokala testresultat,
- inga gamla distributionsartefakter,
- inga duplicerade canonical sources,
- inga brutna interna referenser,
- generated artefakter kan återskapas,
- runtime innehåller bara avsedda filer.

## Hygiene-resultat

Resultat ska kunna vara:

- `pass`
- `warning`
- `blocked`

Exempel:

```yaml
project_hygiene:
  last_result: warning
  findings:
    - id: duplicate-instruction-draft
      class: historical
      path: src/instructions/system-old.md
      recommendation: remove
```

## Automatisk borttagning

GPT Byggaren får automatiskt radera när filen med hög säkerhet är:

- cache,
- temporär arbetsfil,
- genererad output i fel plats,
- ersatt kopia vars innehåll redan finns canonical och som inte refereras.

Vid osäkerhet ska filen markeras för bedömning i stället för att raderas.

## Gitignore

Projekt som använder Git ska normalt generera en `.gitignore` som exkluderar:

- caches,
- lokala buildresultat,
- `dist/`,
- temporära filer,
- OS-metadata.

Vilka genererade kataloger som ignoreras ska styras av projektets faktiska buildmodell.

## Distribution hygiene

Chat ZIP och Custom GPT ZIP ska valideras separat från projektet.

Det räcker inte att källprojektet är rent.

Kontrollera:

- inga tests/evals/research om de inte uttryckligen behövs i runtime,
- inga Git-filer,
- inga lokala artefakter,
- inga interna utvecklingsplaner om de inte behövs,
- inga secrets,
- endast deklarerade runtimefiler.

## Princip

> Behåll det som behövs för nuvarande produkt, inte det som behövs för att minnas hur produkten blev till.
