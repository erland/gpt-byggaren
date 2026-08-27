# Chat/ZIP-runtime – GPT Byggaren

## Syfte

Chat/ZIP-runtime är den primära runtime-distributionen för större och mer avancerade GPT:er.

Den ska kunna bära mer stöd än Custom GPT utan att begränsas av Custom GPT:s instruktions- eller Knowledge-budget.

Grundprincip:

> ZIP-runtime ska representera den fulla avsedda funktionaliteten. Custom GPT är ett separat distributionsmål.

## Runtime-layout

Föreslagen generell struktur:

```text
<project-id>-chat/
├── START-HERE.md
├── VERSION
├── MANIFEST.json
│
├── assistant/
│   ├── instructions.md
│   ├── conversation-starters.md
│   └── policies/
│
├── knowledge/
├── schemas/
├── scripts/
├── templates/
└── runtime/
```

Alla kataloger är villkorade utom de som krävs för att starta och identifiera runtime.

## Obligatoriska runtimefiler

### `START-HERE.md`

Ska beskriva:

- vad ZIP:en är,
- att den ska användas som GPT-kontext i chatten,
- vilken instruktion som är canonical för runtime,
- vilka kataloger som är viktiga,
- hur runtime ska initialiseras,
- eventuella begränsningar.

### `VERSION`

Innehåller distributionsversion.

Vid GitHub Release ska värdet härledas från release-taggen.

Vid lokal utvecklingsbuild får en utvecklingsversion användas.

### `MANIFEST.json`

Ska beskriva:

- runtime-id,
- version,
- filer,
- checksummor,
- entrypoint,
- buildinformation,
- inkluderade capabilities eller runtimefeatures.

## Assistant

`assistant/` innehåller runtime-kompilerad assistentkonfiguration.

Exempel:

```text
assistant/
├── instructions.md
├── conversation-starters.md
└── policies/
```

### `instructions.md`

Genereras från canonical instruktion.

### `conversation-starters.md`

Genereras från canonical conversation starters.

### `policies/`

Innehåller runtime policies som verkligen behövs i Chat ZIP.

Alla utvecklingspolicies behöver inte följa med.

## Knowledge

`knowledge/` får innehålla full canonical Knowledge när runtime behöver den.

Detta kan inkludera:

- Markdown,
- YAML,
- JSON,
- tabeller,
- referensmodeller.

## Schemas

`schemas/` inkluderas när runtime behöver validera eller förstå maskinläsbara kontrakt.

Utvecklingsscheman som endast används av CI behöver inte följa med.

## Scripts

`scripts/` inkluderas endast för script som är användbara eller nödvändiga i runtime.

Exempel:

- query-script,
- transformation,
- validering,
- rapportgenerering,
- filmanipulation.

Buildscript som bara används för att skapa distributionen ska inte följa med.

## Templates

`templates/` inkluderas när GPT:n behöver dem under körning.

## Runtime

`runtime/` används för övrigt genererat eller runtime-specifikt material som inte naturligt hör hemma i andra kataloger.

Det ska inte bli en allmän restkatalog.

## Exkluderas normalt

Följande ska normalt inte följa med i Chat ZIP:

```text
docs/
tests/
evals/
research/
.github/
.git/
build/
dist/
project-status.yaml
PROJECT.md
utvecklingsanteckningar
lokala loggar
caches
```

Undantag får göras när en fil faktiskt behövs av runtime.

## Projektstatus och utvecklingsplan

Chat ZIP ska normalt inte bära utvecklingsplan eller projektstatus.

Dessa hör till projekt-ZIP:en, inte runtime-distributionen.

## Canonical → runtime

Föreslagen kompilering:

```text
src/instructions/system.md
src/runtime-policy/*.md
src/conversation-starters/*
knowledge/
schemas/
scripts/
templates/
        ↓
runtime build
        ↓
build/chat/
        ↓
dist/<project-id>-chat-<version>.zip
```

## Inkluderingsregler

Runtimeinnehåll ska styras av `gpt-project.yaml`.

Exempel:

```yaml
runtime:
  chat_zip:
    include:
      instructions:
        - src/instructions/system.md
      policies:
        - src/runtime-policy/*.md
      knowledge:
        - knowledge/**
      schemas:
        - schemas/runtime/**
```

Detta ska vara deklarativt så att Python-script och GitHub Actions inte behöver duplicera urvalslogiken.

## Entrypoint

`START-HERE.md` är mänsklig entrypoint.

Maskinläsbar entrypoint deklareras i manifestet.

Exempel:

```json
{
  "entrypoint": "START-HERE.md",
  "assistant_instruction": "assistant/instructions.md"
}
```

## Deterministiskt bygge

Chat ZIP ska kunna byggas deterministiskt från samma källor.

Builden ska:

- sortera filer stabilt,
- normalisera metadata där rimligt,
- skapa manifest,
- skapa checksummor,
- exkludera otillåtna filer,
- faila på brutna deklarerade paths.

## Runtime hygiene

Före paketering ska builden kontrollera:

- inga caches,
- inga tests/evals/research om de inte explicit inkluderats,
- inga secrets,
- inga gamla ZIP-filer,
- inga temporära filer,
- inga brutna manifestreferenser.

## Funktionell fullständighet

Chat ZIP ska valideras mot projektets deklarerade fulla capability-set.

Om något canonical runtime-stöd saknas ska builden faila eller ge blockerande fel.

## Direktleverans

GPT Byggaren ska kunna bygga Chat ZIP direkt åt användaren utan GitHub.

Det innebär att samma buildlogik måste fungera:

- lokalt i GPT Byggaren,
- i GitHub Actions.

## GitHub Release

Vid GitHub Release:

```text
release tag
    ↓
version
    ↓
build chat runtime
    ↓
validate
    ↓
zip
    ↓
attach to release
```

## Regel för GPT Byggaren

När en ny GPT skapas ska GPT Byggaren själv avgöra vilka runtimekataloger som behövs.

Den ska inte skapa tomma `schemas/`, `scripts/` eller `templates/` i Chat ZIP om de saknar innehåll.

## Definition of Done

ZIP-runtime är definierad när:

- layout är beslutad,
- entrypoint är definierad,
- include/exclude-regler är definierade,
- canonical → runtime-kompilering är definierad,
- manifestkrav är definierade,
- hygiene är definierad,
- lokal och GitHub-baserad build använder samma principer.
