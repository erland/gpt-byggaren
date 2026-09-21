# OpenAI Plugin Runtime Policy

OpenAI Plugin är en peer runtime som byggs från samma canonical projektkontrakt som övriga distributioner.

## Grundregler

1. Canonical instruktioner ska kompileras till en eller flera skills.
2. Plugin-specifik metadata ska genereras från canonical projektdata.
3. Knowledge och andra resurser ska klassificeras för plugin-runtime som instruktioner, references, assets eller runtime-relevanta scripts.
4. Runtime-specifika filer får inte bli nya canonical sanningskällor när motsvarande information redan finns i projektkontraktet.
5. Pluginpaketet ska vara deterministiskt byggbart.

## Paketgränser

Pluginpaketet får inte innehålla utvecklings- eller historikmaterial som inte behövs vid körning.

Följande ska exkluderas:

- tests/
- evals/
- research/
- .github/
- .git/
- build/
- dist/
- lokala cache- och temporärfiler

## Scripts

Scripts får endast inkluderas när de faktiskt behövs av plugin-runtime.

Att ett script finns i canonical projektet innebär inte automatiskt att det ska distribueras med pluginet.

## Skills

Varje distribuerad skill ska ha ett giltigt `SKILL.md` med minst:

- name
- description

Skillstruktur ska härledas från canonical projektdata och inte dupliceras som separat handunderhållen runtimekonfiguration.

## Version 1-avgränsning

Plugin v1 är skills-first.

Följande ingår inte i v1:

- generering av MCP-serverkod
- avancerad MCP-konfiguration
- ChatGPT UI-komponenter
- lifecycle hooks
- plugin marketplace
- automatisk publicering till Plugin Directory

Dessa funktioner ska endast införas när ett konkret use case motiverar dem.

## State och workspace

Plugin ska inte vara beroende av tidigare chatthistorik när canonical workflow och workspace/state-kontraktet redan definierar en annan auktoritativ tillståndskälla.

## Kompatibilitet

Om plugin-runtime inte kan uppnå full funktionell parity med canonical projektkontraktet ska skillnaden dokumenteras i runtime parity och inte döljas genom runtime-specifika specialregler.
