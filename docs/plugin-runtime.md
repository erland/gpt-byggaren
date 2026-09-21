# OpenAI Plugin Runtime

## Syfte

OpenAI Plugin är en peer runtime i GPT Byggaren. Den byggs från samma canonical projektkontrakt som Chat ZIP, Custom GPT, Claude och OpenCode.

Version 1 är **skills-first** och fokuserar på portabla instruktioner, referenser, assets och runtime-relevanta scripts.

## Canonical → runtime

Pluginruntime ska härledas från canonical projektdata.

Primära källor är:

- `project`
- `instructions`
- `knowledge_architecture`
- `capabilities`
- `tools`
- `artifacts`
- `workspace_state`
- framtida canonical skill-definitioner

Runtime-specifika pluginfiler är genererade artefakter och ska inte vara nya sanningskällor.

## Skillstruktur

Plugin v1 distribuerar en eller flera skills.

En typisk struktur är:

```text
plugin.json
skills/
  <skill-id>/
    SKILL.md
    references/
    assets/
    scripts/
README.md
VERSION
MANIFEST.json
```

Varje `SKILL.md` ska minst ha frontmatter med:

```yaml
---
name: <skill-name>
description: <skill-description>
---
```

Om projektet senare har explicita canonical skill-definitioner ska dessa styra hur många skills som byggs.

Om sådana definitioner saknas kan buildern skapa en default-skill från projektets canonical instruktion.

## Knowledge och resurser

Canonical material ska klassificeras efter runtimefunktion.

### references

Material som modellen använder som referens, till exempel:

- metodbeskrivningar
- regler
- checklistor
- begreppsmodeller
- bakgrundsmaterial

### assets

Material som främst används som mall eller leveransunderlag, till exempel:

- rapportmallar
- Markdown-mallar
- statiska resursfiler
- exempelartefakter

### scripts

Endast scripts som faktiskt behövs i plugin-runtime ska följa med.

Att ett script finns i projektet innebär inte automatiskt att det ska distribueras.

## Resource resolution i v1

Explicit metadata på en canonical skill har företräde för respektive resursklass.

Om en resursklass saknar explicit innehåll används följande konservativa fallback i Plugin v1:

- canonical Knowledge → `references/`
- canonical templates → `assets/`
- endast scripts som uttryckligen deklarerats som runtime tools → `scripts/`

Fallbacken ska vara deterministisk och får inte dra in tests, evals, research eller godtyckliga utvecklingsscript.

## Skillnad mot övriga runtimes

### Chat ZIP

Chat ZIP är en portabel ChatGPT-runtime där ett helt runtimepaket bifogas till en konversation.

Plugin är i stället en installerbar förmåga som kan användas i en vanlig ChatGPT-konversation.

### Custom GPT

Custom GPT kompilerar projektet för ChatGPT Builder och måste förhålla sig till plattformens instruktion- och Knowledge-begränsningar.

Plugin bygger återanvändbara skills och är inte bundet till samma Builder-modell.

### Claude Projects

Claude-distributionen paketerar Project Instructions och Knowledge för Claude Projects.

Plugin använder skillstrukturen som primär beteendeenhet.

### OpenCode

OpenCode är en agentisk workspace-runtime med `AGENTS.md`, skills och explicita tools.

Plugin v1 delar skilltänket men ska inte automatiskt anta samma lokala workspace-, shell- eller toolkapacitet.

## Version 1

Plugin v1 omfattar:

- plugin som peer runtime
- `plugin.json`
- en eller flera skills
- `SKILL.md`
- references
- assets
- runtime-relevanta scripts
- README
- VERSION
- MANIFEST
- deterministiskt ZIP-bygge
- validering
- runtime parity
- CI och release

## Utanför scope i version 1

Följande ingår inte:

- generering av MCP-serverkod
- avancerad MCP-konfiguration
- ChatGPT UI-komponenter
- lifecycle hooks
- plugin marketplace
- automatisk publicering till Plugin Directory

Dessa funktioner kan införas senare när ett konkret use case motiverar dem.

## Installation och användning

Den färdiga pluginartefakten ska vara självinstruerande via sin README.

Exakt installationsflöde kan skilja sig mellan ChatGPT-planer och workspacekonfigurationer och ska därför dokumenteras som runtime-/plattformsspecifik användarinformation, inte kodas som canonical beteende.

## Validation

En giltig Plugin v1-distribution ska minst uppfylla:

- giltigt `plugin.json`
- minst en giltig skill
- `SKILL.md` med obligatoriskt frontmatter
- inga förbjudna development-paths
- inga cache- eller temporärfiler
- giltigt `MANIFEST.json`
- version som matchar byggversionen

## Parity

Plugin ska ingå i samma runtime parity-modell som övriga peer runtimes.

Om canonical funktionalitet blir reducerad eller saknas i plugin-runtime ska detta beskrivas i parityrapporten i stället för att döljas genom plugin-specifika specialfall.

## Framtida utveckling

Möjliga senare utökningar är:

- deklarativa App/MCP-beroenden
- stöd för befintliga MCP-servrar
- MCP-serverstubs
- ChatGPT UI
- hooks
- workspace marketplace
- publiceringsflöden

Dessa ska behandlas som separata funktioner och inte vara ett krav för skills-first Plugin v1.
