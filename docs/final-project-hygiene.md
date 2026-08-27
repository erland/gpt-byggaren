# Projektstädning och slutlig hygiene – GPT Byggaren

## Syfte

GPT Byggaren ska kunna hålla projektets HEAD ren under hela utvecklingen och genomföra en striktare slutkontroll inför release.

Grundprincip:

> Git är historiken. Projektträdet ska representera nuvarande canonical projekt, inte en samling äldre kopior och lokala artefakter.

## Två nivåer

### Checkpoint hygiene

Körs efter relevanta utvecklingssteg.

Mål:

- rensa säkra temporära artefakter,
- upptäcka historiska kopior,
- upptäcka caches,
- upptäcka gamla distributioner,
- kontrollera brutna referenser,
- dokumentera osäkra fynd.

### Final hygiene

Körs inför release.

Mål:

- inga caches eller temporära filer,
- inga gamla build/dist-resultat i source tree,
- inga uppenbart superseded canonical filer,
- inga brutna pathreferenser,
- inga tomma placeholder-filer,
- inga utvecklingsartefakter i runtime-distributioner,
- inga blockerande lint findings.

## Säker automatisk städning

Får auto-rensas:

- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.DS_Store`
- `*.tmp`
- `*.temp`
- genererade `build/`
- genererade `dist/`

Auto-rensning ska endast ske när filen/katalogen är känd som genererad eller temporär.

## Osäkra historiska filer

Exempel:

```text
plan-old.md
config-backup.yaml
instructions-v2.md
final-final.md
```

Dessa ska flaggas för bedömning, inte automatiskt raderas enbart på filnamn.

## Kandidater för historik

Indikatorer:

- `old`
- `backup`
- `bak`
- `previous`
- `copy`
- versionssuffix som `v2`, `v3`
- `final-final`

Indikatorer är inte bevis.

## Canonical duplicering

Om två filer innehåller exakt samma data kan linter/hygiene rapportera det.

Semantisk duplicering behöver bedömas av GPT Byggaren.

## Projektträdet

Före release ska project source normalt innehålla:

```text
README.md
PROJECT.md
STATUS.md
gpt-project.yaml
project-status.yaml
test-manifest.yaml

docs/
src/
knowledge/
templates/
schemas/
scripts/
tests/
evals/
research/        # endast om faktiskt relevant
.github/
```

Villkorade kataloger utan relevant innehåll bör inte finnas.

## Build och dist

`build/` och `dist/` är genererade kataloger.

De ska:

- skapas vid behov,
- kunna raderas utan dataförlust,
- inte vara canonical source,
- normalt inte ligga i projekt-ZIP som arbetsprodukt.

## Runtime hygiene

Separat från project source hygiene ska varje runtime kontrolleras.

Chat ZIP ska normalt inte innehålla:

- `tests/`
- `evals/`
- `research/`
- `.github/`
- projektstatus
- utvecklingsplan
- caches

Custom GPT ZIP ska endast innehålla Builder-underlag och distributionsmetadata.

## Hygiene-resultat

Resultat:

- `pass`
- `warning`
- `blocked`

### pass
Inga blockerande problem.

### warning
Osäkra eller manuellt bedömningskrävande fynd finns.

### blocked
Projektet är inte releasebart.

## Maskinläsbar rapport

Exempel:

```yaml
result: pass
mode: final
removed:
  - .pytest_cache/
findings: []
```

## Release gate

Final hygiene måste vara `pass` eller uttryckligen accepterad `warning` innan release.

`blocked` stoppar release.

## Resume

När ett projekt återupptas kan checkpoint hygiene köras efter initial inventering.

Detta ska inte radera osäkra filer innan projektets roll är förstådd.

## Definition of Done

Steg 22 är klart när:

- checkpoint hygiene kan köras,
- final hygiene kan köras,
- säker auto-clean finns,
- osäkra historiska filer flaggas,
- maskinläsbar rapport skapas,
- release gate kan använda resultatet,
- build/dist och caches kan rensas utan att canonical source påverkas.
