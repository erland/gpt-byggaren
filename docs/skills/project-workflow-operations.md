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

## Nya projekt: modulär Skill-arkitektur

Före första distribution ska projektets förmågor delas upp och dokumenteras enligt `docs/skills/skill-decomposition.md`. Säkerställ att samma Skill-karta styr samtliga fem runtime-distributioner. Skapa inte en monolitisk Skill för flera oberoende förmågor utan dokumenterad motivering.

## Generering av körbart distributionssystem

Skapa först en projektunik konfiguration enligt det **fullständiga** kontraktet i den medföljande distributionsmotorns `gpt-project.yaml`-referens. `build_system.runtime_targets` ska vara en mapping med fem nycklar (`chat`, `plugin`, `claude_project`, `claude_skills`, `opencode`) och respektive `builder`, `runtime_key`, `runtime_id`, `artifact_type` och `filename_pattern`. En lista med plattformsnamn är **inte** giltig. Projektet behöver även en `runtime`-mapping med `chat_zip`, `plugin`, `claude`, `opencode` och `custom_gpt`, samt canonical `instructions`, `structure` och `skills` som faktiskt pekar på projektets egna resurser. Återanvänd inte GPT Byggarens projektspecifika Skills eller instruktioner som Manualguidens innehåll.

Kör den medföljande `scripts/install_distribution_engine.py --source <medföljande distribution-engine> --project-root <projektkatalog>` först efter att projektkonfigurationen är fullständig. Avbryt och redovisa konkreta kontraktsfel om den saknas. Skapa aldrig fem likadana ersättningsarkiv.

## Offline-distributionsmotor i steg 6

GPT Byggarens ChatGPT Chat- och Plugin-arkiv innehåller `distribution-engine/` med distributionsbyggaren, installeraren, skript och mallar. Vid skapande av ett nytt GPT-projekt ska dessa redan medföljande filer användas; extern hämtning från GitHub får inte vara ett obligatoriskt steg.

1. Skapa projektets kanoniska konfiguration och resurser.
2. Kopiera `distribution-engine/` från GPT Byggarens egen runtime-distribution till projektets arbetsyta, eller kör dess `scripts/install_distribution_engine.py` med `--source` satt till den medföljande motorns rot och `--project-root` satt till projektet.
3. Kontrollera deklarerade skript, mallar och projektunika resurser utan att ersätta egna projektskript.
4. Kör `scripts/build_distributions.py` och verifiera fem plattformsspecifika arkiv. Skapa CI och releaseworkflow först med verifierade byggsteg.
5. Om runtime saknar filåtkomst eller exekvering, leverera motorn i projekt-ZIP och låt GitHub Actions köra den. Markera inte byggda distributioner som verifierade innan bygg och validering lyckats.

Ingen nedladdning från GitHub ska krävas för själva distributionsmotorn.
