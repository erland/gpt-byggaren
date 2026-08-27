# Project hygiene policy

## Obligatoriskt beteende

Efter varje genomfört steg ska GPT Byggaren bedöma projektets filhygien.

## Klassificering

Använd:

- CANONICAL
- RUNTIME
- DEVELOPMENT
- GENERATED
- TEMPORARY
- HISTORICAL

## Radera automatiskt endast med hög säkerhet

Säkra kandidater:

- caches,
- temporära filer,
- lokala debugartefakter,
- genererad output på fel plats,
- uppenbart ersatta filer som inte längre refereras.

## Vid osäkerhet

Markera fyndet och rekommendera åtgärd i stället för att radera.

## Historik

Git ska vara historikkälla. Behåll inte gamla filversioner i HEAD endast för spårbarhet.

## Release

Final hygiene är en release gate.
