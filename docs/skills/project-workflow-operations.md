# Projektarbetsflöde: återuppta och välj nästa steg

Detta är det bevarade detaljerade arbetsflödet från canonical systeminstruktionen.

## Återupptagning

Vid en tidigare projekt-ZIP:

1. läs `gpt-project.yaml`,
2. läs `project-status.yaml`,
3. läs utvecklingsplanen,
4. verifiera projektets skick,
5. rekommendera nästa steg.


## Nästa steg

När användaren ber om nästa steg ska du utgå från faktisk projektstatus.

Prioritera blockerare, valideringsfel, project hygiene, korrigeringssteg och saknade beroenden före nästa planerade nummer.

Planen är vägledande, inte mekanisk. Du får införa, hoppa över, dela eller slå ihop steg när det är motiverat och dokumenterat.


## Återuppta tidigare projekt

När användaren bifogar en tidigare projekt-ZIP ska du läsa `gpt-project.yaml`, `project-status.yaml`, `docs/development-plan.md`, `STATUS.md` och `PROJECT.md` i den ordningen.

Använd `project-status.yaml` som primär statuskälla, verifiera projektet och beräkna nästa steg innan du fortsätter.

Be inte användaren återberätta projekthistorik som redan finns i projekt-ZIP:en.




## Vid okänt äldre projektformat

Förvänta inte en given filstruktur när ett gammalt projekt ännu inte har en canonical modell. Kör generell inventering och evidensbaserad tolkning genom `legacy-project-analysis`. Använd statusfilernas etablerade ordning endast när projektet faktiskt följer den äldre kontraktslayouten.

## Verifiering

Uppdatera aldrig auktoritativ status till klar före relevanta valideringar och tester. Om källor, byggmiljö eller runtime saknas ska utfallet redovisas som ej verifierat. Använd projektets faktiska status för nästa rekommendation.
