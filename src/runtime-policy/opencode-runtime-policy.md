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

Projektlokala Skills får genereras under `.opencode/skills/<skill-id>/SKILL.md` från deklarerade canonical workflows och referenser. Skills ska ha tydlig description, giltigt kebab-case-id och får inte bli en ny canonical source.

## Tools

Steg 10 gör ingen explicit tool-integration. Tool-kontraktet finns med i snapshoten men integrationen implementeras i steg 12.

## Canonical source

`AGENTS.md` och runtime snapshot är genererade projektioner och får aldrig bli canonical source.
