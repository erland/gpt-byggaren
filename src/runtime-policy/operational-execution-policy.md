# Operativ exekveringspolicy

## Syfte

GPT Byggaren ska vara möjlig att köra stabilt även med modeller som har begränsad förmåga att hålla många indirekta regler och långa arbetsflöden i minnet.

Modellen ska därför i första hand exekvera ett explicit, validerbart workflow i stället för att själv orkestrera hela projektet från fria instruktioner.

## Operativ kärna

För varje genomförandesteg:

1. Läs `gpt-project.yaml`.
2. Läs `project-status.yaml`.
3. Bestäm exakt ett aktuellt workflow-state och ett konkret mål.
4. Läs endast de policies och projektfiler som behövs för detta mål.
5. Utför ändringen.
6. Kör relevant deterministisk validering, test eller build.
7. Vid fel: korrigera felet och markera inte steget eller state som klart.
8. Vid godkänt resultat: uppdatera strukturerad status.
9. Bygg om projekt-ZIP när projektets regler kräver det.
10. Rekommendera nästa steg från faktisk projektstatus.

## Regler

- Utför normalt bara ett workflow-state eller ett tydligt avgränsat delmål per användarens "Gör nästa steg".
- Hoppa inte över obligatoriska gates.
- Härled inte sådant på nytt som redan finns i strukturerade kontrakt.
- När en validator kan avgöra en regel deterministiskt ska validatorns resultat väga tyngre än fri modellbedömning.
- Vid valideringsfel ska felmeddelandet användas som konkret korrigeringsuppgift.
- Håll obligatoriska filhopp få. Kärnflödet ska normalt kunna styras från canonical instruktion + ett direkt relevant kontrakt eller policy.
- Separata modellvarianter av canonical instruktionen ska inte skapas för att kompensera för modellskillnader.

## Workflow-states

Canonical huvudflöde:

`idea_analysis -> architecture -> planning -> implementation -> validation -> packaging -> release`

`maintenance` är ett stabilt post-release-state. `blocked` och `paused` är kontrollstates och får endast användas när ett verkligt blockerande fel respektive verksamhetsbeslut finns.

Övergångar ska ske först när föregående states exit-kriterier är uppfyllda.
