# OpenCode base runtime – GPT Byggaren

## Syfte

OpenCode-adaptern är en agentisk workspace-runtime som genereras från samma canonical assistant-kontrakt som övriga distributioner.

Steg 10 etablerar basadaptern. Steg 11 lägger till projektlokala Skills. Explicit tool-integration byggs i ett senare steg.

## Officiell OpenCode-modell

OpenCode använder `AGENTS.md` för persistent projektguidance. I OpenCode V2 används inte `CLAUDE.md` som fallback.

OpenCode kan dessutom upptäcka projektlokala Skills under `.opencode/skills/<name>/SKILL.md`. Dessa införs separat i steg 11 så att `AGENTS.md` förblir adapter-entrypoint och inte canonical source.

## Paketstruktur

```text
<project-id>-opencode-<version>.zip
├── AGENTS.md
├── README.md
├── VERSION
├── MANIFEST.json
├── knowledge/
└── .opencode/
    └── runtime-contract.json
```

## AGENTS.md

`AGENTS.md` genereras från canonical instruktion och får endast ett litet adaptertillägg för OpenCode-specifika regler.

Den genererade filen är inte canonical source.

## Contract snapshot

`.opencode/runtime-contract.json` innehåller snapshot av:

- capabilities,
- artifacts,
- workspace/state,
- tools,
- adapterstatus.

I steg 10 sätts:

- `skills_included: false`
- `tool_integration: deferred`

Detta gör basadaptern explicit ofullständig för de delarna i stället för att låtsas att tools/skills redan är integrerade.

## Knowledge

Canonical knowledge kopieras till `knowledge/` och kan läsas av OpenCode-agenten i workspace.

## Workspace/state

OpenCode är workspace-orienterat och passar därför väl för assistenter som behöver persistent projektstruktur. Själva stateprojektionen styrs fortfarande av canonical workspace/state-kontraktet och får inte ersättas av OpenCode-specifik state som ny sanningskälla.

## Skills

OpenCode Skills genereras under `.opencode/skills/<skill-id>/SKILL.md` med giltig YAML-frontmatter och en beskrivning som gör att agenten kan upptäcka dem vid rätt uppgift.

GPT Byggaren genererar initialt `gpt-project-workflow`, som kapslar flerstepsflödet för planering, resume och next-step-hantering. Tillhörande referensdokument kopieras till skillens privata `references/`-katalog så att skillen kan ladda dem vid behov.

Skillen är en runtimeprojektion. Canonical instruktion, policies och projektdokumentation förblir sanningskälla.

## Tools

Explicit integration av canonical tool-kontrakt sker först i steg 12. Basadaptern får inte härleda eller exponera extra verktyg bara för att scripts råkar finnas i projektet.

## Definition of Done

Basadaptern är klar när:

- root `AGENTS.md` genereras,
- canonical knowledge följer med,
- runtime contract snapshot genereras,
- paketet valideras,
- CI/release/direct build producerar OpenCode ZIP,
- projektlokala Skills genereras från deklarerade canonical workflowkällor,
- ingen implicit tool-integration görs ännu.
