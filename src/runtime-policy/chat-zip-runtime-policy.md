# Chat ZIP runtime policy

## Distributionsroll

Chat ZIP är ett av två normala distributionsmål tillsammans med Custom GPT. Den ska inte automatiskt behandlas som primär runtime för avancerade GPT:er.

## Funktionalitet

Chat ZIP får innehålla rikare runtime-material, schemas, scripts och templates när plattformen kräver det, men ska härledas från samma canonical behavior-, capability-, artifact-, workspace/state- och tool-kontrakt som övriga runtimes. Mer runtime-material innebär inte automatiskt högre instruktionsefterlevnad eller högre prioritet.

## Inkludera endast runtimebehov

Utvecklingsmaterial följer inte med om det inte uttryckligen behövs vid körning.

## Projektstatus

Utvecklingsplan och project-status hör till projekt-ZIP, inte Chat ZIP.

## Build

Runtime ska byggas deklarativt från `gpt-project.yaml`.

## Hygiene

Chat ZIP ska valideras separat och får inte innehålla caches, temporära filer eller utvecklingsartefakter av misstag.


## Contract snapshot

Builden ska skriva en maskinläsbar snapshot av de canonical kontrakten till `assistant/runtime-contract.json`. Snapshoten är genererad runtimeinformation och får inte bli en ny canonical källa.

## Tools

Endast explicit deklarerade runtimeverktyg ska tas med som scripts. En källkatalog med scripts är inte i sig ett include-beslut.
