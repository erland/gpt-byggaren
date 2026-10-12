# Skill: bygga och verifiera distributioner

## När denna förmåga används
När ett granskat canonical GPT-projekt ska byggas, testas eller levereras för Chat ZIP, ChatGPT Plugin, Claude eller OpenCode.

## Obligatoriskt för nygenererade projekt

Generera **inte** ett förenklat projektspecifikt `build_distributions.py` som lägger samma `INSTRUCTIONS.md` och `SKILL.md` i fem ZIP-filer. Nya projekt måste använda GPT Byggarens kanoniska distributionsbyggare och dess deklarativa `build_system.runtime_targets`, med projektspecifika data och Skills som indata. Kopiera eller versionera den befintliga bygg- och valideringsimplementationen tillsammans med dess nödvändiga kontrakt och mallar; kontrollera att alla beroenden finns i det genererade projektet. Om ett fullständigt körbart byggsystem inte kan levereras ska projektet markeras som ofullständigt, inte förses med fem missvisande ZIP-filer.

Varje runtime har ett eget installationskontrakt: Chat ZIP med assistant-instruktioner och portabla moduler, OpenAI Plugin med pluginmanifest och Skills, Claude Projects med projektinstruktioner och kunskap, Claude Skills med Skills och resurser, OpenCode med `AGENTS.md`, `.opencode/skills` och relevanta verktyg. Bygg och validera var och en med befintliga runtime-specifika funktioner. En identisk fillista i alla fem runtime-ZIP-filerna är ett regressionsfel.

## Plugin-reservläge

Om originalmotorn inte kan köras i OpenAI Plugin, följ `docs/skills/plugin-declarative-fallback.md` för ett overifierat källutkast. Sätt generation.mode till declarative_fallback, build.status till pending_canonical_verification och build.release_ready till false. Behåll delivery.mode. Skapa inte distributionsarkiv utan körd kanonisk byggare. Denna reservväg gäller inte Chat ZIP.

## Plugin: tidig kontroll och nedladdning

Vid första konkreta projektstarten eller återupptagningen, kontrollera en gång om den inbyggda `distribution-engine.zip` är verkligt åtkomlig för Python, eller om användaren redan bifogat motorn. Stör inte vanliga frågor och gör inte om kontrollen vid varje meddelande. Kör originalmotorns självtest när filerna finns tillgängliga.

Om den interna filens bytes är tillgängliga men inte kan användas direkt, försök exponera just dessa bytes som en faktisk nedladdningsbar fil. Uppge aldrig att en bilaga skapats om filens bytes inte kunde nås. För en **released** Plugin-version: ge en direktlänk till `https://github.com/erland/gpt-byggaren/releases/download/v<VERSION>/distribution-engine.zip` med den installerade Plugin-versionen insatt, aldrig senaste eller annan version. För **CI-/testversioner**: hänvisa inte till GitHub Actions eller CI-artefakter och hitta inte på någon release; be endast om att användaren bifogar motorn om ingen riktig nedladdningsbar fil kunde skapas. Fortsätt annars med tydligt overifierat deklarativt källutkast. Ingen GitHub-hämtning från Python, ingen alternativ paketerare.

## Plugin: bifogad kanonisk motor

När GPT Byggaren körs som Plugin och behöver bygga distributioner: kontrollera först om den inbyggda `assets/distribution-engine.zip` faktiskt kan läsas som fil i Python-arbetsytan. Om den inte är tillgänglig, leta efter en vanlig användarbifogad `distribution-engine.zip`. Packa upp originalmotorn med bibehållna sökvägar och kör dess befintliga självtest, integritetskontroller, installerare, byggare och validatorer. Om ingen fil är tillgänglig, ge användaren en direkt nedladdningsmöjlighet för exakt pluginversion endast när releaseartefakten har verifierats finnas; be annars om manuell uppladdning. Hämta aldrig motorn genom GitHub API eller Releases från Python som fallback. Påstå inte att pluginens interna Skill-fil automatiskt kan exporteras till en nedladdningsbar bilaga. Om motorn fortfarande saknas, fortsätt med ett tydligt overifierat deklarativt källutkast. Detta påverkar inte Chat ZIP eller övriga distributioners byggflöden.

## Arbetsgång
1. Utgå från samma canonical instruktioner, förmågor, resurs- och verktygskontrakt.
2. Kontrollera skriptens hostkrav och fallback; tillgång till filerna är inte bevis för körbarhet.
3. Använd befintliga builders och validators. Kontrollera att Chat ZIP och Claude får fungerande instruktioner och relevanta resurser även utan automatisk skillaktivering.
4. För Plugin: paketera Skills och resurser men aldrig mcp.json, även i nästlade mappar.
5. Kör strukturella tester och faktisk runtimeparitet där värdmiljöerna medger det; skilj tydligt mellan offlinekontroll och hosttest.
6. Om något blockerar: redovisa skillnader och släpp inte igenom release_ready.

## Operativa verktyg
- scripts/build_distributions.py
- scripts/validate_distributions.py
- scripts/validate_portable_skills.py

## Fallback
Om runtime eller hostkodkörning saknas: beskriv vad som verifierats offline och vilka runtimekrav som inte har testats. Inga uppdiktade lyckade tester.

## Äldre canonical runtimebedömning (bevarad vid extraktion)

## Registrerade peer runtimes

Vid analys av ett nytt eller migrerat projekt ska minst följande runtime-kandidater bedömas explicit:

- ChatGPT Chat,
- ChatGPT Custom,
- Claude Projects,
- OpenCode,
- OpenAI Plugin.

Saknad bedömning av en registrerad runtime är ett ofullständigt analysresultat.

OpenAI Plugin ska bedömas som en skills-first peer runtime. Aktivera den när kärnbeteendet lämpar sig för återanvändbara skills och relevanta references/assets utan krav på funktioner som Plugin v1 inte själv realiserar.

Om projektet kräver persistent workspace/state, lokal tool-exekvering, genererad MCP-server, UI-komponenter eller hooks ska Plugin inte behandlas som fullständigt equivalent enbart för att resurser kan paketeras i ZIP:en. Beskriv skillnaden genom runtime parity och välj suitability utifrån faktisk funktionstäckning.

