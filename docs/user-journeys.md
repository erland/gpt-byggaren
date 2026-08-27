# Användarresor – GPT Byggaren

## Scenario 1 – Ny användare med endast en idé

1. Användaren beskriver GPT-idén i naturligt språk.
2. GPT Byggaren analyserar behovet.
3. GPT Byggaren rekommenderar runtime, capabilities och ambitionsnivå.
4. GPT Byggaren beskriver eventuella viktiga avgränsningar.
5. När målbilden är tillräckligt tydlig skapas en nedladdningsbar utvecklingsplan.
6. Användaren säger exempelvis: `Gör steg 1`.
7. Första projekt-ZIP:en skapas.
8. GPT Byggaren rekommenderar nästa steg.

## Scenario 2 – Erfaren användare som vill skapa en avancerad ZIP-first GPT

1. Användaren beskriver ett komplext problem.
2. GPT Byggaren identifierar behov av rik runtime.
3. ZIP-first rekommenderas.
4. Custom GPT behandlas som sekundärt distributionsmål.
5. Planen inkluderar runtimefiler, schemas, scripts, tester och distribution.
6. Projekt-ZIP:en byggs på stegvis.
7. Full Chat-ZIP byggs även om Custom GPT måste reduceras.

## Scenario 3 – Både ZIP och Custom GPT

1. GPT Byggaren designar en canonical implementation.
2. Chat-ZIP byggs från full runtime.
3. Custom GPT kompileras separat.
4. Skillnader i funktionalitet dokumenteras.
5. Båda artefakterna valideras.
6. Användaren får direkta nedladdningslänkar.

## Scenario 4 – Användaren vill inte använda GitHub

1. GPT Byggaren utvecklar projektet normalt.
2. Projekt-ZIP byggs.
3. Distributionsartefakter byggs lokalt av GPT Byggaren.
4. Användaren får länkar till projekt-ZIP, Chat-ZIP och eventuell Custom GPT-ZIP.
5. Ingen GitHub-konfiguration krävs för att använda GPT:n.

## Scenario 5 – Användaren vill lägga projektet i GitHub

1. Användaren laddar ner projekt-ZIP.
2. Projektet packas upp i ett Git-repo.
3. GitHub Actions finns redan i projektet när de relevanta utvecklingsstegen är klara.
4. En GitHub Release skapas.
5. Release-taggen används som versionskälla.
6. Actions bygger distributionsartefakterna och publicerar dem på releasen.

## Scenario 6 – Användaren återkommer med en tidigare projekt-ZIP

1. Projekt-ZIP:en bifogas i en ny konversation.
2. GPT Byggaren inventerar projektet.
3. `docs/development-plan.md` läses.
4. `STATUS.md` läses.
5. Projektet valideras.
6. GPT Byggaren rekommenderar nästa steg.
7. Användaren kan säga `Gör nästa steg`.

## Scenario 7 – Planen behöver avvika

1. GPT Byggaren genomför ett steg.
2. Validering visar ett nytt arkitekturproblem.
3. GPT Byggaren stoppar inte arbetet mekaniskt.
4. Ett extra korrigerings- eller hygiene-steg rekommenderas.
5. Planstatus uppdateras.
6. Projektet fortsätter när det nya problemet är hanterat.

## Grundregel

Planen är styrande men inte blind.

GPT Byggaren ska alltid välja det **mest lämpliga nästa steget utifrån projektets faktiska skick**.
