# Knowledge policy

## Grundregel

Instruktion och runtime policies beskriver beteende.
Knowledge beskriver referensmaterial och domäninformation.

## GPT Byggaren ska själv rekommendera

- om Knowledge behövs,
- struktur,
- format,
- konsolidering,
- runtimefördelning.

## Chat ZIP

Får innehålla full canonical Knowledge.

## Custom GPT

Får använda konsoliderad eller prioriterad Knowledge.

## Förbjuden genväg

Flytta inte beteenderegler till Knowledge enbart för att kringgå instruktionsbudgeten.

## Kvalitet

Kontrollera duplicering, konflikter, döda resurser och onödigt små eller splittrade filer.

## Small-model-safe kärna

Obligatoriskt kärnworkflow ska kunna förstås från canonical instruktionen utan att modellen först måste hitta en specifik Knowledge-fil. Knowledge får fördjupa analys, fakta och referensmaterial men ska inte vara den enda platsen för kritiska beteenderegler.
