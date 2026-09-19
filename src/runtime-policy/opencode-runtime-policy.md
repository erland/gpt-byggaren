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

## Target project

OpenCode-runtime-workspace och det GPT-projekt som ska bearbetas är separata begrepp.

Målprojektet bör normalt ligga som en underkatalog i runtime-workspace eller adresseras via en tydlig relativ `projectRoot`. Dokumentationen får inte ge intryck av att runtime-ZIP:en i sig innehåller målprojektets `gpt-project.yaml` eller projektstatus.

## Tools

Script-tools som uttryckligen deklarerats i canonical tool-kontrakt får projiceras till OpenCode custom tools under `.opencode/tools/`.

Kopiera endast de deklarerade runtime-scripten och nödvändigt delat bibliotek. Exponera aldrig hela `scripts/` implicit.

Genererade tool-wrappers ska använda begränsade, typade argument. Fri shell-input ska inte införas för ett script-tool om canonical kontrakt inte kräver det.

Tools som arbetar mot ett GPT-projekt ska stödja ett explicit `projectRoot`; om det utelämnas används runtime-workspace-roten.

Muterande tools ska som standard kräva godkännande i `opencode.json`; icke-muternade canonical tools kan tillåtas direkt.

## Canonical source

`AGENTS.md` och runtime snapshot är genererade projektioner och får aldrig bli canonical source.
