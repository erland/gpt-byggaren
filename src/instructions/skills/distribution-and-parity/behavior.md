## Engine för nya GPT-projekt

När en ny GPT behöver exekvera egna skript via Plugin ska projektprofilen deklarera `engine.enabled: true`, en explicit lista `engine.resources` över skript och tillhörande resurser, `engine.selftest` med ett verkligt körbart självtest och vid GitHub-leverans `engine.release_repository` i formatet owner/repo. Paketeringen görs av den befintliga kanoniska byggaren och levererar `<project-id>-engine.zip` som en **separat** artefakt, inte inuti Plugin. Plugin ska tidigt be om Engine ZIP och för en publicerad GitHub-version ge en direktlänk till exakt motsvarande release. En GPT utan exekverbara Plugin-skript ska inte ha ett Engine-paket (`engine.enabled: false` eller utelämnad sektion). Kräv aldrig Engine för enbart dokumentation, instruktioner eller vanliga Knowledge-filer. Dokumentera när koden kräver en extern runtime eller en tjänst som inte går att köra med en bifogad ZIP. Testa både en skriptbaserad GPT och en textbaserad GPT och markera runtimeparitet utifrån faktisk testbarhet.


**Direktkörning av installerad originalmotor i Work.** Vid första uppgiften som kräver deterministisk exekvering: kontrollera i första hand den installerade Skillens verkliga filsystem, inte bara dess läsbara textresurser. För GPT Byggaren ligger originalmotorn under `skills/distribution-and-parity/scripts/distribution-engine/`. Använd den faktiska absoluta sökvägen som observeras i värdmiljön, utan hårdkodade cacheprefix. Kör originalfilen `scripts/selftest_distribution_engine.py` med `--source` pekande mot motorns rot. Kräv verklig stdout, stderr och exitkod och redovisa misslyckat test utan att simulera resultat. Vid PASS körs befintlig installerare, byggare och validatorer från samma motor. Projektets arbetskatalog ska vara separat och skrivbar; ändra aldrig pluginens cache som projektworkspace. Om originalfilen inte är körbar eller filsystemet inte är tillgängligt, använd Engine ZIP som reservväg. Om faktisk exekvering har skett men misslyckats: rapportera felet; byt inte tyst till fallback. Denna kontroll ska endast göras när en exekverbar uppgift påbörjas.

**Körmiljö och paritet.** Work har i Plugin Script Probe verifierat direkt körning av ett medföljande Python-skript med relativ åtkomst till en asset. Det bevisar inte att hela GPT Byggarens motor är verifierad i Work. Plugin Skill, Chat ZIP och den separat levererade Engine ZIP ska fortsatt använda samma kanoniska motor; alla fem runtime-distributioner ska valideras separat.


## Genererings- och verifieringsparitet

Skapa aldrig en ny GPT-projektprofil som refererar till ett obligatoriskt testmanifest, en verifieringsmodell, en linter eller en modellkompatibilitetsrapport utan att motsvarande fil finns i projekt-ZIP. Om projektet inte behöver en viss verifieringsfunktion, utelämna den deklarationen i stället för att kopiera GPT Byggarens egna projektprofiler eller tillverka platshållare. Kontrollera deklarerade resursfiler före varje canonical distributionsbygge för såväl Chat som Plugin.

Rapportera alltid verifieringsomfattning separat: (1) strukturella och deterministiska projektkontroller, (2) kanonisk GPT-lint som faktiskt har körts, (3) runtime-/värdmiljötester som faktiskt har utförts och (4) ej verifierade kontroller. Ange aldrig ”0 lintvarningar” som ett bevis på att fullständig kanonisk lint är utförd om endast projektspecifik lint har körts. Ett passerat byggtest får inte rubriceras som ett funktionellt språkmodellstest. När Chat och Plugin får samma projektprofil och samma kanoniska motor ska de använda samma obligatoriska resurskontroller och samma resultatskala. Bilagefunktion per värdmiljö är en separat runtimeverifiering, inte ett generellt lintfel.

## Reservläge för Plugin

Om den kanoniska distributionsmotorn inte är körbar i ChatGPT Plugin får projektets källfiler tas fram deklarativt som overifierat utkast. Inga fem distributionsarkiv får deklareras byggda och ingen release får godkännas utan kanoniskt bygg- och valideringsresultat. Behåll användarens ZIP/GitHub-val. Detta undantag gäller inte Chat ZIP eller andra runtime-distributioner. Följ `docs/skills/plugin-declarative-fallback.md`.

## Plugin: tidig kontroll och nedladdning

Vid första konkreta projektstarten eller återupptagningen, kontrollera en gång om användaren redan bifogat `gpt-byggaren-engine-<VERSION>.zip` och att filen är verkligt åtkomlig i Python-arbetsytan. Sök inte efter en inbyggd Engine ZIP i Plugin: sådana duplicerade resurser har tagits bort. Stör inte vanliga frågor och upprepa inte kontrollen varje meddelande. Om motorn finns, packa upp originalfilerna med bibehållna sökvägar och kör kanoniskt självtest, integritetskontroller, installerare, byggare och validatorer.

Om motorn saknas: skriv tydliga instruktioner i användarens språk: (1) öppna den direkta Release-länken, (2) ladda ned Engine ZIP för exakt den installerade Plugin-versionen, (3) bifoga den nedladdade ZIP-filen här i konversationen, och (4) fortsätt med ”Gör nästa steg”. Förklara att det är en separat fil och att den inte kan hämtas automatiskt från Plugin. Ge inte bara en benämning på motorn eller en allmän uppmaning att tillföra den.

Om motorn saknas: för en publicerad Plugin-version erbjud den direkta versionsbundna filen `https://github.com/erland/gpt-byggaren/releases/download/v<VERSION>/gpt-byggaren-engine-<VERSION>.zip` där VERSION är den installerade Plugin-versionen. För CI-/testversioner, hitta inte på någon release och hänvisa inte till GitHub Actions; be i stället användaren bifoga Engine ZIP. Fortsätt annars med ett tydligt overifierat deklarativt källutkast. Använd ingen GitHub-hämtning i Python och ingen alternativ paketerare.

## Leverans- och runtime-gates för nya projekt

- Nya projekt ska ha en **projektunik** `gpt-project.yaml`. Kopiera inte GPT Byggarens interna `reference_profiles` till en annan GPT om den inte faktiskt har egna profiler. Om `reference_profiles` anges måste katalogen och alla namngivna profilfiler existera före leverans; dölj inte felet med en tom platshållarkatalog. GitHub Actions får följa med även i ZIP-läge utan att GitHub därmed blir ett krav.


- Vid projektstart: skapa den fullständiga projektunika `gpt-project.yaml` med fem runtime-mål `chat`, `plugin`, `claude_project`, `claude_skills`, `opencode`. Alla fem aktiveras som standard; eventuella tekniska hinder ska redovisas, inte döljas genom att bara bygga två.
- Kopiera och installera kanoniska motorn före första distributionsbygget. Stoppa om installeraren saknas; skriv aldrig en förenklad egen distributionsbyggare.
- `custom_gpt` är historiskt stöd och ska **inte** aktiveras, genereras eller erbjudas som sjätte runtime. Runtime-listan omfattar exakt fem mål om användaren inte uttryckligen väljer bort någon.
- `.gitignore` är endast en källprojektfil i projekt-ZIP, inte en fil i de fem runtime-ZIP:arnas rot. Motorns mall `templates/generated-project.gitignore` får medfölja som **installationsresurs** i `distribution-engine/`, inte som aktiv `.gitignore` i runtimepaketet.
- Vid varje leverans: erbjud projekt-ZIP samt alla fem distributionerna separat med faktiska nedladdningslänkar. Ingen GitHub-release krävs för ZIP-läge.

## Registrerade peer runtimes

Bedöm explicit ChatGPT Chat, ChatGPT Custom (historisk, ej aktiv distribution), Claude Projects och Claude Skills, OpenCode samt OpenAI Plugin vid nya och migrerade projekt. Behandla OpenAI Plugin som en skills-first peer runtime. Behandla aktiva distributioner som jämbördiga; utgå från samma canonical kontrakt och dokumentera runtime parity och anta aldrig funktionell paritet bara för att filer eller skript kan paketeras. Använd skillen `distribution-and-parity` för runtime-lämplighet, skillresurser, hostkrav och detaljerade skillnader. Om en funktion kräver persistent state, lokal exekvering, genererad MCP-server, UI eller hooks ska den inte förklaras likvärdig enbart för att resurser kan paketeras. Aktivera inte runtime utan verifierad kompatibilitet.

## Release readiness

Innan en GPT betraktas som releaseklar ska project status, lint, tester, build, distributionsvalidering, final hygiene och runtime-specifika kontroller vägas samman.

Blockerande resultat stoppar release. Icke-blockerande varningar dokumenteras tydligt.


