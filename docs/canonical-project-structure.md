# Kanonisk projektstruktur – GPT Byggaren

## Syfte

Detta dokument definierar den generella projektstruktur som GPT Byggaren ska använda när den skapar och vidareutvecklar GPT-projekt.

Strukturen ska vara:

- enkel nog för små GPT:er,
- tillräckligt rik för avancerade ZIP-first GPT:er,
- tydlig kring vad som är canonical source,
- tydlig kring vad som är utvecklingsmaterial,
- tydlig kring vad som är runtime,
- tydlig kring vad som är genererat,
- möjlig att paketera både direkt och via GitHub Actions.

## Strukturprincip

Alla projekt behöver inte innehålla alla kataloger.

GPT Byggaren ska skapa **minsta tillräckliga struktur** utifrån projektets behov.

Följande kategorier används:

- **OBLIGATORISK** – ska finnas i alla GPT-projekt.
- **VILLKORAD** – ska finnas när projektets behov kräver den.
- **GENERERAD** – ska skapas av build eller releaseprocess och är normalt inte canonical source.
- **UTVECKLING** – används för test, eval, research eller arbetsstöd men följer normalt inte med runtime.
- **RUNTIME** – följer med i Chat/ZIP-distributionen när relevant.

## Rekommenderad basstruktur

```text
gpt-project/
├── README.md                         # OBLIGATORISK
├── PROJECT.md                        # OBLIGATORISK
├── STATUS.md                         # OBLIGATORISK
├── gpt-project.yaml                  # OBLIGATORISK
│
├── docs/                             # OBLIGATORISK
│   ├── development-plan.md
│   ├── product-vision.md
│   └── ...
│
├── src/                              # OBLIGATORISK
│   ├── instructions/                 # canonical instruktioner
│   ├── conversation-starters/        # canonical starters
│   └── runtime-policy/               # vid behov
│
├── knowledge/                        # VILLKORAD
├── templates/                        # VILLKORAD
├── schemas/                          # VILLKORAD
├── scripts/                          # VILLKORAD
├── tests/                            # VILLKORAD / UTVECKLING
├── evals/                            # VILLKORAD / UTVECKLING
├── research/                         # VILLKORAD / UTVECKLING
│
├── build/                            # GENERERAD
│   ├── custom-gpt/
│   ├── chat/
│   └── reports/
│
├── dist/                             # GENERERAD
│
└── .github/
    └── workflows/                    # VILLKORAD
```

## Obligatoriska delar

### `README.md`

Ska ge en kort introduktion till projektet och beskriva hur det används.

### `PROJECT.md`

Ska beskriva:

- syfte,
- scope,
- styrande principer,
- viktiga arkitekturbeslut.

### `STATUS.md`

Ska göra projektet självbärande mellan konversationer och visa:

- genomförda steg,
- aktuellt steg,
- rekommenderat nästa steg,
- blockerande problem,
- senaste validering,
- senaste hygiene-status.

### `docs/`

Ska minst innehålla utvecklingsplanen när en plan har skapats.

### `src/`

Ska innehålla canonical GPT-källor.

Detta är en viktig förändring jämfört med enklare projekt där runtimefiler ibland underhålls direkt i distributionskataloger.

## Canonical source

Canonical source ska ligga under `src/` eller i tydligt deklarerade källkataloger.

Exempel:

```text
src/
├── instructions/
│   └── system.md
├── conversation-starters/
│   └── starters.md
└── runtime-policy/
    └── routing.md
```

Distributionsspecifika instruktioner ska genereras från canonical source när det är möjligt.

## Knowledge

`knowledge/` används när GPT:n behöver referensmaterial.

Knowledge kan innehålla:

- Markdown,
- YAML,
- JSON,
- text,
- andra filer som runtime behöver.

Custom GPT Knowledge ska **inte** behöva motsvara denna struktur direkt. En separat kompileringsprocess får konsolidera eller välja ut material.

## Templates

`templates/` används bara om GPT:n faktiskt producerar eller bearbetar strukturerade artefakter som behöver mallar.

## Schemas

`schemas/` används för maskinläsbara kontrakt såsom:

- JSON Schema,
- YAML-schema,
- strukturella runtime-kontrakt.

## Scripts

`scripts/` används för:

- build,
- lint,
- validation,
- packetering,
- transformation,
- runtimehjälp.

Scripts som endast används i utveckling behöver inte följa med i Chat ZIP.

## Tests

`tests/` används för deterministiska tester.

Exempel:

- strukturvalidering,
- buildtest,
- instruction lint,
- Knowledge-validering,
- manifestkontroll.

## Evals

`evals/` används när beteendet behöver bedömas med scenarier eller kvalitativa kriterier.

Det är inte obligatoriskt för små GPT:er.

## Research

`research/` är uttryckligen utvecklingsmaterial.

Det ska normalt inte följa med i runtime eller distribution.

## Build

`build/` innehåller mellanresultat och genererade filer.

Exempel:

```text
build/
├── chat/
├── custom-gpt/
└── reports/
```

Detta är inte canonical source.

## Dist

`dist/` innehåller färdigpaketerade artefakter såsom:

```text
my-gpt-project.zip
my-gpt-chat-v1.0.0.zip
my-gpt-custom-gpt-v1.0.0.zip
SHA256SUMS.txt
```

Katalogen ska normalt kunna återskapas och behöver inte versionshanteras.

## GitHub Actions

`.github/workflows/` skapas när GitHub-stöd aktiveras.

Projektet ska fortfarande fungera utan GitHub.

## Runtimeklassificering

Filer ska kunna klassificeras i fem praktiska grupper:

| Klass | Syfte | Med i projekt-ZIP | Med i Chat ZIP | Med i Custom GPT |
|---|---|---:|---:|---:|
| Canonical source | Ursprungliga GPT-källor | Ja | Via build | Via build |
| Runtime | Behövs vid körning | Ja | Ja | Vid behov |
| Development | Test, eval, research | Ja | Nej | Nej |
| Generated | Build- och distributionsresultat | Valfritt | N/A | N/A |
| Historical/temporary | Tillfälligt eller ersatt | Nej | Nej | Nej |

## Minimal struktur för enkel GPT

```text
gpt-project/
├── README.md
├── PROJECT.md
├── STATUS.md
├── gpt-project.yaml
├── docs/
│   └── development-plan.md
└── src/
    ├── instructions/
    │   └── system.md
    └── conversation-starters/
        └── starters.md
```

## Struktur för avancerad ZIP-first GPT

```text
gpt-project/
├── README.md
├── PROJECT.md
├── STATUS.md
├── gpt-project.yaml
├── docs/
├── src/
│   ├── instructions/
│   ├── conversation-starters/
│   └── runtime-policy/
├── knowledge/
├── templates/
├── schemas/
├── scripts/
├── tests/
├── evals/
├── research/
├── build/
├── dist/
└── .github/
    └── workflows/
```

## Regler för GPT Byggaren

GPT Byggaren ska:

1. skapa minsta tillräckliga struktur,
2. undvika tomma kataloger som inte fyller ett omedelbart syfte,
3. hålla canonical source separat från genererade distributioner,
4. undvika dubbla källor för samma instruktion eller regel,
5. hålla utvecklingsmaterial borta från runtime,
6. skapa `build/` och `dist/` först när buildsystemet införs,
7. använda Git för historik i stället för gamla filkopior,
8. göra project hygiene före varje release,
9. uppdatera `STATUS.md` efter varje steg,
10. låta `gpt-project.yaml` bli maskinläsbar källa för strukturen från nästa steg.

## Beslut för GPT Byggaren-projektet

Det aktuella GPT Byggaren-projektet ska använda följande struktur framåt:

```text
gpt-byggaren/
├── README.md
├── PROJECT.md
├── STATUS.md
├── PROJECT-MANIFEST.json
├── docs/
├── src/
│   ├── instructions/
│   ├── conversation-starters/
│   └── runtime-policy/
├── knowledge/
├── templates/
├── schemas/
├── scripts/
├── tests/
├── evals/
└── .github/
    └── workflows/
```

`build/` och `dist/` införs först när buildsystemet utvecklas.

`research/` införs endast om faktisk research behöver sparas i projektet.

## Maskinläsbart projektkontrakt

Från och med steg 3 är `gpt-project.yaml` obligatorisk.

Den deklarerar projektstruktur, runtime, distributionsmål, buildregler,
project hygiene och releaseprinciper och ska fungera som single source of
truth för kommande automation.
