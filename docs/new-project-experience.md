# New-project UX – GPT Byggaren

## Mål

En användare ska kunna starta ett nytt GPT-projekt genom att beskriva verksamhetsbehovet. Användaren ska normalt inte behöva välja runtime, adapter, schemaformat, testnivå eller paketeringsmodell.

## Grundflöde

1. användaren beskriver vad assistenten ska göra,
2. GPT Byggaren identifierar input, output, aktualitet, workspace/state och tool-behov,
3. plattformsneutrala capability-, artifact-, workspace/state- och tool-kontrakt härleds,
4. möjliga runtimes bedöms mot samma canonical kontrakt,
5. lämpliga runtimes aktiveras som peer targets,
6. skillnader och reducerad funktion dokumenteras,
7. användaren tillfrågas endast om olösta verksamhetsval.

## Runtime-resultat

Nya projekt använder:

```yaml
runtime:
  strategy: peer_candidates
  candidates:
    - runtime_id: chatgpt_chat
      suitability: equivalent
      activate_by_default: true
      rationale: ...
```

`suitability` är:

- `equivalent`
- `reduced`
- `not_recommended`

Ingen runtime ska göras primär enbart på grund av historisk GPT Byggaren-arkitektur.

## När användaren ska frågas

Fråga endast när svaret är ett verkligt verksamhetskrav, exempelvis:

- assistenten måste fungera i en viss organisationsplattform,
- en viss output är obligatorisk,
- filer får inte lämna en viss miljö,
- användaren uttryckligen vill begränsa antalet distributioner.

Fråga normalt inte:

- ChatGPT eller Claude?
- Ska OpenCode användas?
- Vill du ha schemas?
- Ska scripts finnas?
- Ska persistent state användas?
- Ska tester skapas?

Tekniska beslut härleds först och presenteras som rekommendationer med motivering.

## Default-aktivering

Flera runtimes får aktiveras samtidigt när de har hög paritet och inte innebär missvisande funktion.

En runtime med reducerad eller onödig funktion kan finnas som kandidat utan att aktiveras som default.

## Canonical först

Runtimeval görs efter canonical kontrakt.

Förbjuden ordning:

```text
välj plattform → designa beteende efter plattformen
```

Rätt ordning:

```text
förstå behov → canonical kontrakt → bedöm runtimes → bygg adapters
```

## Presentation till användaren

Analysen ska normalt uttryckas i verksamhetsnära språk:

- vad assistenten ska kunna,
- vilka runtimes som fungerar bra,
- vilka som har begränsningar,
- varför GPT Byggaren föreslår de aktiverade målen.

Adapterdetaljer behöver bara visas när de påverkar beslutet.

## Definition of Done

Nyprojektsupplevelsen är klar när:

- analyskontraktet är runtime-neutralt,
- referensprofiler saknar primär-runtime-antagande,
- blank-idea E2E verifierar peer candidates,
- nya projekt kan ha flera default runtimes,
- användaren inte behöver förstå adapterarkitekturen för att komma igång.
