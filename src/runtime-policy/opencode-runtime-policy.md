# OpenCode runtime policy

## Mål

Bygg en portabel OpenCode workspace-runtime från canonical assistant-kontrakt.

## Instructions

Root `AGENTS.md` är OpenCode-adapterns projektinstruktion och ska genereras från canonical instruktion.

Använd inte `CLAUDE.md` som fallback eller primär instruktion.

## Contract snapshot

Skriv `.opencode/runtime-contract.json` som genererad adapter-snapshot.

## Knowledge

Canonical knowledge får kopieras till workspace för läsning vid behov.

## Skills

Steg 10 skapar inga Skills. Dessa läggs till separat i steg 11.

## Tools

Steg 10 gör ingen explicit tool-integration. Tool-kontraktet finns med i snapshoten men integrationen implementeras i steg 12.

## Canonical source

`AGENTS.md` och runtime snapshot är genererade projektioner och får aldrig bli canonical source.
