# Canonical core / Skills: ansvarsfördelning och acceptanskriterier

Denna matris är avsedd att granska uppdelningen innan fler stycken tas bort ur systeminstruktionen. Den gäller samma källprojekt och alla fyra aktivt byggda distributioner.

| Område | Måste finnas i kärnan | Detaljer i Skill |
| --- | --- | --- |
| Identitet och verksamhetsbehov | Uppdrag, idé-först, fråga bara vid verkliga verksamhetsval | gpt-project-workflow: planeringsmetodik |
| Genomförande | Operativ algoritm, verifiera innan status uppdateras, blockerare först | gpt-project-workflow: filordning, resume, dynamiska steg |
| Äldre projekt | Bevara beteende, inventera verkliga källor, inga ogrundade aktiveringar | legacy-project-analysis: inventering, provenance, osäkerhet |
| Distribution | Alla runtime-kandidater, peer-paritet, inga falska exekveringspåståenden | distribution-and-parity: format, begränsningar, hostkrav |
| Release | Release blockeras vid fel; status/test/build/hygiene måste kontrolleras | distribution-and-parity: detaljerade tester och leverans |
| Modell och UI | Textfallback, gemensamt kärnbeteende, ingen modellversionsspecifik instruktion | Fördjupning i runtime-policy/referenser |

## Gränsregler
1. En Skill får utöka detaljer men **inte** vara enda källan till releasegates, säkerhet, statusauktoritet eller textfallback.
2. Ingen runtime får tappade moduler eller referenser när en canonical definition ändras. Testa de **byggda** paketen, inte bara YAML.
3. Fullständiga skillfiler i Chat ZIP och Claude Projects innebär **inte** att respektive värdmiljö har installerat eller exekverat dem. Kontroll av värdmiljö krävs separat.
4. Skript utan verifierade körmiljökrav får inte beskrivas som exekverbara.
5. Äldre projekts filstruktur får inte antas. En AI-föreslagen gräns mellan Skills kräver källstöd och granskning.

## Fortsättning
Fortsätt efter att testet för denna gränsmatris är grönt: extrahera ett smalt policyområde i taget, återanvänd befintliga Skills, och komplettera med verkliga hostacceptanstester för Claude Skills och ChatGPT Plugin när dessa kan köras.
