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

## Plugin: bifogad kanonisk motor

När GPT Byggaren körs som Plugin och behöver bygga distributioner: kontrollera först om den inbyggda `assets/distribution-engine.zip` faktiskt kan läsas som fil i Python-arbetsytan. Om den inte är tillgänglig, leta efter en vanlig användarbifogad `distribution-engine.zip`. Packa upp originalmotorn med bibehållna sökvägar och kör dess befintliga självtest, integritetskontroller, installerare, byggare och validatorer. Om ingen fil är tillgänglig, ge användaren en direkt nedladdningsmöjlighet för exakt pluginversion endast när releaseartefakten har verifierats finnas; be annars om manuell uppladdning. Hämta aldrig motorn genom GitHub API eller Releases från Python som fallback. Påstå inte att pluginens interna Skill-fil automatiskt kan exporteras till en nedladdningsbar bilaga. Om motorn fortfarande saknas, fortsätt med ett tydligt overifierat deklarativt källutkast. Detta påverkar inte Chat ZIP eller övriga distributioners byggflöden.

## Verifiering

Uppdatera aldrig auktoritativ status till klar före relevanta valideringar och tester. Om källor, byggmiljö eller runtime saknas ska utfallet redovisas som ej verifierat. Använd projektets faktiska status för nästa rekommendation.

## Nya projekt: modulär Skill-arkitektur

Före första distribution ska projektets förmågor delas upp och dokumenteras enligt `docs/skills/skill-decomposition.md`. Säkerställ att samma Skill-karta styr samtliga fem runtime-distributioner. Skapa inte en monolitisk Skill för flera oberoende förmågor utan dokumenterad motivering.

## Generering av körbart distributionssystem

Skapa först en projektunik konfiguration enligt det **fullständiga** kontraktet i den medföljande distributionsmotorns `distribution-engine/gpt-project.yaml`-referens. `build_system.runtime_targets` ska vara en mapping med fem nycklar (`chat`, `plugin`, `claude_project`, `claude_skills`, `opencode`) och respektive `builder`, `runtime_key`, `runtime_id`, `artifact_type` och `filename_pattern`. En lista med plattformsnamn är **inte** giltig. Projektet behöver även en `runtime`-mapping med `chat_zip`, `plugin`, `claude`, `opencode` och `custom_gpt`, samt canonical `instructions`, `structure` och `skills` som faktiskt pekar på projektets egna resurser. Återanvänd inte GPT Byggarens projektspecifika Skills eller instruktioner som Manualguidens innehåll. Referensfilen är ett schemaexempel, **inte** en konfiguration som får kopieras oförändrad: skriv projektets egna `project`, `instructions`, `skills`, `tools` och sökvägar och kontrollera att alla deklarerade filer finns.

Kör den medföljande `scripts/install_distribution_engine.py --source <medföljande distribution-engine> --project-root <projektkatalog>` först efter att projektkonfigurationen är fullständig. Avbryt och redovisa konkreta kontraktsfel om den saknas. Skapa aldrig fem likadana ersättningsarkiv.

## Offline-distributionsmotor i steg 6

GPT Byggarens ChatGPT Chat- och Plugin-arkiv innehåller `distribution-engine/` med distributionsbyggaren, installeraren, skript och mallar. Vid skapande av ett nytt GPT-projekt ska dessa redan medföljande filer användas; extern hämtning från GitHub får inte vara ett obligatoriskt steg.

1. Skapa projektets kanoniska konfiguration och resurser.
2. Kopiera `distribution-engine/` från GPT Byggarens egen runtime-distribution till projektets arbetsyta, eller kör dess `scripts/install_distribution_engine.py` med `--source` satt till den medföljande motorns rot och `--project-root` satt till projektet.
3. Kontrollera deklarerade skript, mallar och projektunika resurser utan att ersätta egna projektskript.
4. Kör `scripts/build_distributions.py` och verifiera fem plattformsspecifika arkiv. Skapa CI och releaseworkflow först med verifierade byggsteg.
5. Om runtime saknar filåtkomst eller exekvering, leverera motorn i projekt-ZIP och låt GitHub Actions köra den. Markera inte byggda distributioner som verifierade innan bygg och validering lyckats.

Ingen nedladdning från GitHub ska krävas för själva distributionsmotorn.


## Leveransval och kontinuitet

Vid första behovet av att spara eller publicera projektet: erbjud **ZIP** eller **GitHub** som två likvärdiga arbetsformer, helst som två valbara alternativ och alltid som text. Fråga **en gång**, dokumentera `delivery.mode: zip` eller `delivery.mode: github` i `project-status.yaml` (eller motsvarande auktoritativa projektstatus) och respektera det vid återupptagning.

- **ZIP**: bygg och lämna ut projekt-ZIP och fem runtime-ZIP direkt; lägg inte in GitHub-remote, GitHub Actions eller releaseworkflow som krav. Föreslå inte GitHub igen efter valet. Byte sker endast på användarens initiativ.
- **GitHub**: lägg till GitHub Actions/releaseworkflow och publicera källprojektet enligt användarens önskemål. Skapa fortfarande samma sex artefakter.
- Avvakta GitHub-förslag tills användaren nått detta val; GitHub är inte ett naturligt obligatoriskt första steg i en ny GPT.
- Om val redan är registrerat får du inte återställa det när projektets status uppdateras.

## Projektunika konfigurationsreferenser

Härled `gpt-project.yaml` från den nya GPT:ns egna behov, inte genom att kopiera hela GPT Byggarens projektkonfiguration. Fältet `reference_profiles` är valfritt och används endast om den nya GPT:n faktiskt har egna profildefinitioner. Ta bort GPT Byggarens `reference_profiles` vid skapandet om sådana profiler inte behövs. Om fältet används måste `reference_profiles.root` och samtliga namngivna `.yaml`, `.yml` eller `.json`-profiler finnas i projekt-ZIP före leverans. Skapa inte tomma kataloger enbart för att tysta lintern.

GitHub Actions-filer får finnas även när `delivery.mode: zip` används. ZIP-valet innebär att GitHub inte är obligatoriskt och inte ska föreslås igen, inte att användbar CI-konfiguration ska raderas.

## Obligatoriskt leveranskontrakt för nya projekt

Innan projektet får markeras klart:

1. Skapa `gpt-project.yaml` i projektroten med projektets egen identitet, canonical instruktion, Skill-kontrakt, runtime-konfiguration och fem runtime_targets. Installera den medföljande kanoniska distributionsmotorn **innan den första runtime-distributionen byggs** och använd den konsekvent under hela utvecklingen. Avbryt hellre än att bygga Chat/Plugin med en tillfällig egen byggare. Kör därefter den kanoniska distributionsbyggaren för **alla fem** runtime-mål från första leveranstillfället. Skapa **inte** en projektspecifik ersättning för `scripts/build_distributions.py`.
2. Aktivera inte `custom_gpt` som runtime-mål. Eventuella äldre `custom_gpt`-konfigurationsblock måste ha `enabled: false` och får inte finnas i aktiva `build_system.targets`.
3. Skapa `.gitignore` från `distribution-engine/templates/generated-project.gitignore` innan första Git-commit. Genererade `dist/`, `build/`, release-artefakter, cache och lokala filer får inte checkas in.
4. Projekt-ZIP ska innehålla källfiler och konfiguration men aldrig `.git/`, `dist/`, `build/`, cache eller andra genererade artefakter. Filtrera explicit vid ZIP-skapande: `.gitignore` skyddar inte ZIP-paketering.
5. Kontrollera att **runtime-ZIP:arnas rot saknar `.gitignore`**. Motorns inbyggda `templates/generated-project.gitignore` är en avsiktlig installationsmall och får ligga i `distribution-engine/` för Chat/Plugin.
6. Bygg, validera och länka **sex** separata nedladdningar: projekt-ZIP samt ChatGPT Chat, OpenAI Plugin, Claude Projects, Claude Skills och OpenCode. Visa en separat klickbar länk per faktisk artefakt. Om en fil inte skapats får den inte presenteras som nedladdningsbar.
5. Vid varje leverans, sammanfatta verifieringsstatus per distribution. Byggd ZIP är inte samma sak som hostverifierad runtime. Inkludera SHA256/manifest när det finns.
6. Presentera nästa rekommenderade steg som en konkret uppföljningsfråga eller valbar åtgärd. Använd interaktiva nästa-steg-knappar när gränssnittet stödjer dem, men behåll alltid ett tydligt textalternativ. Hitta inte på knappar eller länkar som runtime inte kan rendera.
7. Kör `scripts/validate_generated_delivery.py --project-root <projektkatalog> --version <version>` när skriptet finns tillgängligt. Åtgärda samtliga fel innan leverans. Saknas exekvering, redovisa kontrollen som ej utförd, inte godkänd.

Dessa regler gäller även när användaren ber att publicera på GitHub. `dist/` är ett tillfälligt byggresultat och hör inte till källrepon.
