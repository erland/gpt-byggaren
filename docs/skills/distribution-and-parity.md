# Skill: bygga och verifiera distributioner

## När denna förmåga används
När ett granskat canonical GPT-projekt ska byggas, testas eller levereras för Chat ZIP, ChatGPT Plugin, Claude eller OpenCode.

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

