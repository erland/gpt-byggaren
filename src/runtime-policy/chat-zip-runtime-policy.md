# Chat ZIP runtime policy

## Primär runtime

För avancerade GPT:er är Chat ZIP primär runtime.

## Full funktionalitet

Chat ZIP får innehålla rikare instruktioner, Knowledge, schemas, scripts och templates än Custom GPT.

## Inkludera endast runtimebehov

Utvecklingsmaterial följer inte med om det inte uttryckligen behövs vid körning.

## Projektstatus

Utvecklingsplan och project-status hör till projekt-ZIP, inte Chat ZIP.

## Build

Runtime ska byggas deklarativt från `gpt-project.yaml`.

## Hygiene

Chat ZIP ska valideras separat och får inte innehålla caches, temporära filer eller utvecklingsartefakter av misstag.
