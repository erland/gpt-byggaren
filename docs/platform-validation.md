# Plattformsvalidering – GPT Byggaren

## Syfte

GPT Byggaren ska validera att en Custom GPT-distribution faktiskt går att använda i målplattformen innan den betraktas som releasbar.

Grundprincip:

> Validera den byggda distributionen, inte bara källprojektet.

Det räcker alltså inte att canonical source ser korrekt ut. Den faktiska Custom GPT-artefakten måste kontrolleras.

## Valideringsnivåer

### 1. Projektkonfiguration

Kontrollera att projektet innehåller de konfigurationer som behövs för Custom GPT.

Exempel:

- instruktionstrategi,
- Knowledge-strategi,
- Builder-filer,
- capability-rekommendationer,
- plattformsgränser.

### 2. Instruktion

Kontrollera:

- fil finns,
- filen är läsbar,
- teckenlängd håller sig inom konfigurerad gräns,
- innehållet inte är tomt,
- obligatoriska kärnsektioner finns när projektet kräver dem.

Exempel:

```text
Instructions
✓ 7 612 / 8 000 characters
```

### 3. Knowledge

Kontrollera:

- antal filer,
- filstorlekar när sådan gräns är konfigurerad,
- filformat när formatbegränsning är konfigurerad,
- inga tomma Knowledge-filer,
- inga dubbletter,
- inga runtime- eller utvecklingsfiler av misstag.

Exempel:

```text
Knowledge
✓ 18 / 20 files
```

### 4. Conversation starters

Kontrollera:

- fil finns,
- minst en starter finns om projektet använder starters,
- inga tomma poster,
- formatet är begripligt för Builder.

### 5. Capabilities

Kontrollera att rekommendationerna är konsekventa med analysmodellen.

Exempel:

```text
Web: enable
Data analysis: enable
Image generation: disable
```

### 6. Builder-paket

Kontrollera att distributionen innehåller:

```text
builder/
├── instructions.md
├── conversation-starters.md
├── capabilities.md
└── knowledge-package/
```

Saknade obligatoriska filer är blockerande.

### 7. Compatibility

Om Custom GPT är reducerad ska `COMPATIBILITY.md` finnas.

Den ska beskriva:

- primär runtime,
- reducerade funktioner,
- saknade funktioner,
- paritet.

## Plattformsgränser

Gränser ska läsas från `gpt-project.yaml`.

Exempel:

```yaml
platform_limits:
  instruction_max_characters: 8000
  knowledge_max_files: 20
```

Build- eller valideringsscript ska inte duplicera dessa värden som hårdkodade konstanter.

## Konfigurerbara framtida gränser

Valideringsmodellen ska även kunna utökas med:

- max filstorlek,
- tillåtna filformat,
- max antal conversation starters,
- andra Builder-krav.

## Resultatnivåer

Valideringsresultat ska vara:

- `pass`
- `warning`
- `blocked`

### `pass`

Distributionen uppfyller alla blockerande krav.

### `warning`

Distributionen går att använda men har reducerad funktion eller annan icke-blockerande avvikelse.

### `blocked`

Distributionen ska inte publiceras.

## Blockerande fel

Minst följande är blockerande:

- instruktion över maxgräns,
- för många Knowledge-filer,
- obligatorisk Builder-fil saknas,
- tom instruktion,
- deklarerad Knowledge-fil saknas,
- missvisande kärnfunktion,
- invalid manifest,
- build innehåller förbjudna utvecklingsartefakter.

## Varningar

Exempel:

- Custom GPT har lägre paritet än Chat ZIP,
- Knowledge har konsoliderats kraftigt,
- viss funktion saknas men kärnuppgiften fungerar,
- capability-rekommendation har ändrats från tidigare analys.

## Valideringsrapport

Builden ska skapa en rapport, exempelvis:

```text
Custom GPT Validation

Instructions
✓ 7 612 / 8 000 characters

Knowledge
✓ 18 / 20 files

Conversation starters
✓ 4 configured

Capabilities
✓ configured

Builder package
✓ complete

Compatibility
⚠ reduced functionality documented

RESULT: WARNING
```

## Maskinläsbar rapport

Samma resultat ska kunna representeras i JSON/YAML för CI.

Exempel:

```yaml
result: warning
checks:
  instruction_length:
    status: pass
    actual: 7612
    limit: 8000
  knowledge_files:
    status: pass
    actual: 18
    limit: 20
```

## Release gate

Custom GPT-distributionen får bifogas en release endast om resultatet är:

- `pass`
- eller `warning` när varningen är uttryckligen accepterad av projektets regler.

`blocked` stoppar release.

## Lokal och GitHub-baserad validering

Samma valideringslogik ska användas:

- när GPT Byggaren bygger artefakter direkt åt användaren,
- i CI,
- i GitHub Release-workflow.

## Aktuella plattformsgränser

GPT Byggaren ska behandla plattformsgränser som konfiguration som kan ändras över tid.

När en gräns är osäker eller kan ha ändrats bör användaren kunna uppdatera projektkonfigurationen utan att buildscript behöver skrivas om.

## Definition of Done

Plattformsvalideringen är definierad när:

- instruktion kan valideras,
- Knowledge kan valideras,
- Builder-paket kan valideras,
- capabilities kan kontrolleras,
- kompatibilitet kan kontrolleras,
- blockerande fel är definierade,
- rapportformat finns,
- release gate är definierad,
- samma modell fungerar lokalt och i GitHub.
