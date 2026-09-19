# Claude portable runtime – GPT Byggaren

## Syfte

Claude-runtime är ett portabelt paket för vanlig Claude Projects-användning.

Den ska inte blandas ihop med Claude Code. Därför används inte `CLAUDE.md`, repo-hooks eller andra Claude Code-specifika konventioner i denna adapter.

## Officiell plattformsmodell

Claude Projects stödjer project instructions och en projektgemensam knowledge/files-del. Information som ska finnas tillgänglig över flera chattar behöver ligga i projektets knowledge/files eller instruktioner; vanlig chathistorik delas inte automatiskt mellan separata chattar.

## Paketstruktur

```text
<project-id>-claude-<version>.zip
├── README.md
├── VERSION
├── MANIFEST.json
└── project/
    ├── instructions.md
    ├── runtime-contract.json
    └── knowledge/
```

## Canonical projektion

`project/instructions.md` genereras från canonical instruktion.

`project/knowledge/` innehåller canonical knowledge-resurser som ska användas i Claude Project.

`project/runtime-contract.json` innehåller en genererad snapshot av:

- capabilities,
- artifacts,
- workspace/state,
- tools,
- Claude-adapterns begränsningar.

Snapshoten är inte canonical source.

## Tools

Claude Projects-paketet bäddar inte in lokala scripts eller shell-kommandon som körbara verktyg.

Om canonical tool-kontrakt kräver sådana funktioner ska snapshoten markera dem som reducerade eller saknade. MCP/API-liknande funktioner kan bero på vilka integrationsmöjligheter som är aktiverade i användarens Claude-miljö.

## State

Claude Projects ger projektgemensamma instructions/files men detta ska inte automatiskt tolkas som att alla canonical statekrav är fullt realiserade.

När explicit strukturerad statefil krävs bör den läggas i projektets knowledge/files eller hanteras av en senare mer agentisk Claude-adapter.

## Skills

Claude Skills finns som separat plattformsfunktion, men steg 9 gör dem inte obligatoriska. Skills kan utvärderas som en senare adapterförbättring utan att ändra canonical kontrakt.

## Definition of Done

Claude portable runtime är klar när:

- distributionen kan byggas deterministiskt,
- project instructions genereras från canonical instruktion,
- canonical knowledge paketeras för projektet,
- runtime-contract snapshot genereras,
- distributionen valideras,
- delivery manifest och checksummor inkluderar Claude ZIP,
- ingen Claude Code-specifik konvention krävs.
