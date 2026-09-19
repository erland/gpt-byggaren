# Claude portable runtime policy

## Mål

Bygg en portable runtime för vanlig Claude Projects-användning.

## Avgränsning

Använd inte `CLAUDE.md` eller andra Claude Code-specifika konventioner som canonical entrypoint.

## Instructions

Project Instructions ska härledas från canonical instruktion.

## Knowledge

Canonical knowledge ska paketeras så att användaren kan lägga till det i Claude Project Files/Knowledge.

## Contract snapshot

Skriv `project/runtime-contract.json` som genererad adapter-snapshot.

## Tools

Lokala scripts och local commands är inte automatiskt körbara i Claude Projects och ska därför markeras som reducerade eller saknade när de krävs.

## Portabilitet

Paketet ska kunna installeras manuellt i Claude Projects utan GitHub eller Claude Code.
