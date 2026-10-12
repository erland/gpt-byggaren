# Skill: bygga och verifiera distributioner

## När denna förmåga används
När ett granskat canonical GPT-projekt ska byggas, testas eller levereras för Chat ZIP, ChatGPT Plugin, Claude eller OpenCode.

## Obligatoriskt för nygenererade projekt

Generera **inte** ett förenklat projektspecifikt `build_distributions.py` som lägger samma `INSTRUCTIONS.md` och `SKILL.md` i fem ZIP-filer. Nya projekt måste använda GPT Byggarens kanoniska distributionsbyggare och dess deklarativa `build_system.runtime_targets`, med projektspecifika data och Skills som indata. Kopiera eller versionera den befintliga bygg- och valideringsimplementationen tillsammans med dess nödvändiga kontrakt och mallar; kontrollera att alla beroenden finns i det genererade projektet. Om ett fullständigt körbart byggsystem inte kan levereras ska projektet markeras som ofullständigt, inte förses med fem missvisande ZIP-filer.

Varje runtime har ett eget installationskontrakt: Chat ZIP med assistant-instruktioner och portabla moduler, OpenAI Plugin med pluginmanifest och Skills, Claude Projects med projektinstruktioner och kunskap, Claude Skills med Skills och resurser, OpenCode med `AGENTS.md`, `.opencode/skills` och relevanta verktyg. Bygg och validera var och en med befintliga runtime-specifika funktioner. En identisk fillista i alla fem runtime-ZIP-filerna är ett regressionsfel.

## Plugin-reservläge

Om originalmotorn inte kan köras i OpenAI Plugin, följ `docs/skills/plugin-declarative-fallback.md` för ett overifierat källutkast. Sätt generation.mode till declarative_fallback, build.status till pending_canonical_verification och build.release_ready till false. Behåll delivery.mode. Skapa inte distributionsarkiv utan körd kanonisk byggare. Denna reservväg gäller inte Chat ZIP.

## Plugin: tidig kontroll och nedladdning

Vid första konkreta projektstarten eller återupptagningen, kontrollera en gång om användaren redan bifogat `gpt-byggaren-engine.zip` och att filen är verkligt åtkomlig i Python-arbetsytan. Sök inte efter en inbyggd Engine ZIP i Plugin: sådana duplicerade resurser har tagits bort. Stör inte vanliga frågor och upprepa inte kontrollen varje meddelande. Om motorn finns, packa upp originalfilerna med bibehållna sökvägar och kör kanoniskt självtest, integritetskontroller, installerare, byggare och validatorer.

Om motorn saknas: skriv tydliga instruktioner i användarens språk: (1) öppna den direkta Release-länken, (2) ladda ned Engine ZIP för exakt den installerade Plugin-versionen, (3) bifoga den nedladdade ZIP-filen här i konversationen, och (4) fortsätt med ”Gör nästa steg”. Förklara att det är en separat fil och att den inte kan hämtas automatiskt från Plugin. Ge inte bara en benämning på motorn eller en allmän uppmaning att tillföra den.\n\nOm motorn saknas: för en publicerad Plugin-version erbjud den direkta versionsbundna filen `https://github.com/erland/gpt-byggaren/releases/download/v<VERSION>/gpt-byggaren-engine.zip` där VERSION är den installerade Plugin-versionen. För CI-/testversioner, hitta inte på någon release och hänvisa inte till GitHub Actions; be i stället användaren bifoga Engine ZIP. Fortsätt annars med ett tydligt overifierat deklarativt källutkast. Använd ingen GitHub-hämtning i Python och ingen alternativ paketerare.

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

