# Instruktionsefterlevnad

## Syfte

GPT Byggaren ska hjälpa nya GPT-projekt att testa om ett deklarerat beteendekontrakt faktiskt går att följa över en hel konversation, inte bara om filer och schemas är korrekta.

## Minsta evalpaket

1. **Bootstrap** – canonical instruktionen förblir auktoritativ efter att en Chat ZIP aktiverats.
2. **Multi-turn retention** – kärnregler följs även efter flera turer.
3. **Terminal behavior** – obligatoriskt slutbeteende utförs om projektet har ett sådant.
4. **Knowledge independence** – kärnflödet fungerar utan optional Knowledge.

## Modellkompatibilitet

Evalfallen beskriver avsett beteende. Resultat för specifika modeller ska dokumenteras separat. Ett modellmisslyckande ändrar inte automatiskt GPT-specifikationen.

## Release

Critical instruction-adherence-evals ska ingå i releasebedömningen när de kan köras. Där automatisk modell-eval saknas ska åtminstone evaldefinitionerna och det statiska core-contractet valideras.
