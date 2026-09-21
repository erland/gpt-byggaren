# Runtime compatibility och paritet – GPT Byggaren

## Syfte

GPT Byggaren ska kunna beskriva hur väl varje runtime realiserar samma canonical assistant-kontrakt.

Modellen får inte anta att det bara finns två runtimes. ChatGPT Chat och ChatGPT Custom är de första registrerade runtime-målen, men samma schema ska senare kunna användas för Claude, OpenCode och andra adapters.

## Referens

Canonical projektkontrakt är alltid referens:

```text
behavior
capabilities
artifacts
workspace/state
tools
```

Ingen runtime är automatiskt norm för de andra.

## Vad som jämförs

Paritet bedöms per requirement i fem kategorier:

- `behavior`
- `capability`
- `artifact`
- `workspace_state`
- `tool`

Det gör att exempelvis OpenCode senare kan vara `equivalent` för lokala scripts och persistent workspace även om en chattruntime är `reduced`, samtidigt som båda kan vara `equivalent` för kärnbeteendet.

## States

Varje runtime får per requirement ett av:

- `equivalent`
- `reduced`
- `missing`
- `not_applicable`

Reducerad eller saknad funktion ska motiveras.

## Kritikalitet

Varje requirement klassificeras som:

- `critical`
- `important`
- `optional`

En saknad critical requirement kan göra just den runtime-distributionen `not_viable`.

## Generisk runtime-matris

Exempel:

```text
Requirement                    ChatGPT Chat  ChatGPT Custom  OpenCode
--------------------------------------------------------------------
Core workflow                      ✓              ✓             ✓
Persistent workspace               ~              ~             ✓
Local validation script            ~              -             ✓
Markdown report                    ✓              ✓             ✓
```

OpenCode i exemplet är illustrativt; en runtime får inte registreras som stödd förrän dess adapter faktiskt finns och valideras.

## Maskinläsbar modell

```yaml
schema_version: 2
reference:
  type: canonical_contract

runtimes:
  chatgpt_chat:
    level: high
    weighted_score: 92
    release_recommendation: publish

  chatgpt_custom:
    level: moderate
    weighted_score: 76
    release_recommendation: publish_with_warning

requirements:
  - category: capability
    id: filesystem-write
    title: Skriv filer
    criticality: important
    runtime_states:
      chatgpt_chat:
        state: equivalent
      chatgpt_custom:
        state: reduced
        reason: Begränsad filhantering i denna runtime.

  - category: tool
    id: validate-model
    title: Deterministisk modellvalidering
    criticality: critical
    runtime_states:
      chatgpt_chat:
        state: reduced
      chatgpt_custom:
        state: missing
        reason: Runtime saknar den deklarerade lokala tool-implementationen.
```

Runtime-ID:n är dynamiska objektkeys och är inte hårdkodade i schemat.

## Sammanfattande nivå

Per runtime används:

- `full`
- `high`
- `moderate`
- `low`
- `not_viable`

Poäng får användas som stöd men får aldrig ersätta requirement-matrisen.

## Viktning

Standard:

```text
equivalent = 1.0
reduced    = 0.5
missing    = 0.0
```

Kritikalitet:

```text
critical  = 3
important = 2
optional  = 1
```

`not_applicable` ska normalt inte dra ned poängen.

## Releasebeslut

Per runtime:

- `full` / `high` → `publish`
- `moderate` / `low` → `publish_with_warning` när kärnbeteendet fortfarande är meningsfullt
- `not_viable` → `do_not_publish`

Det ska inte finnas en generell `prefer_chat_zip`-regel. En runtime kan rekommenderas framför en annan endast när konkret compatibilitydata motiverar det.

## Bakåtkompatibilitet

Legacyrapporter med:

- `primary_runtime`
- en gemensam `summary`
- fasta `chat_zip`- och `custom_gpt`-fält i capabilities

kan normaliseras till schema version 2.

Legacyformatet är läsbart under migration men ska inte genereras av nya projekt.

## Rapport

Mänsklig rapport ska minst innehålla:

- registrerade runtimes,
- nivå och releasebedömning per runtime,
- requirement-matris,
- reducerade requirements,
- saknade requirements,
- motiveringar.

## Definition of Done

Paritetsmodellen är generaliserad när:

- godtyckliga runtime-ID:n kan representeras,
- canonical kontrakt är enda referensen,
- capability, artifact, workspace/state och tools kan jämföras,
- releasebedömning sker per runtime,
- gamla två-runtime-rapporter kan normaliseras,
- inga ännu ej implementerade runtimes deklareras som stödda.


## OpenAI Plugin v1

`openai_plugin` är en registrerad peer runtime och ska bedömas mot samma canonical kontrakt som övriga runtimes.

För Plugin v1 gäller särskilt:

- behavior kan projiceras genom skills,
- runtimepaketet kan genereras som artifact,
- persistent workspace/state beror på host-runtime,
- lokala canonical script tools paketeras som resurser men får inte automatiskt räknas som exekverbara tools,
- MCP, UI och hooks genereras inte i v1.

Dessa skillnader ska uttryckas som `reduced` eller `missing` i en konkret parityrapport när de är relevanta för projektets requirements; de får inte döljas genom att markera plugin som generellt equivalent.
