# Uppdelning av nya GPT-projekt i Skills

Vid skapande av ett nytt projekt ska GPT Byggaren härleda en **modulär Skill-karta** från användningsfall och förmågekontraktet innan distributionerna byggs.

## Obligatoriskt arbetsflöde

1. Identifiera användningsfall, arbetsflöden, verktyg, kunskapskällor och separata ansvarsområden.
2. Gruppera sammanhängande förmågor i Skills. Skapa inte en Skill per trivial operation, men undvik en enda monolitisk Skill när flera självständiga förmågor finns.
3. För varje Skill: ange ett unikt stabilt ID, namn, syfte, utlösande användningsfall, gränser, beroenden, förväntat resultat, egna referenser, assets och eventuella skript.
4. Lägg gemensamma regler och identitet i canonical kärninstruktion. Duplicera inte kärnan i källmodulerna.
5. Registrera varje Skill under `skills.definitions` i `gpt-project.yaml` och skapa tillhörande filer enligt projektets Skill-kontrakt.
6. Kontrollera att samtliga förmågor täcks, att ansvar inte överlappar oavsiktligt och att resurser faktiskt existerar.
7. Bygg alla aktiverade distributioner från **samma** Skill-definitioner: ChatGPT Chat (text/fallback), ChatGPT Plugin, Claude Projects (text/fallback), Claude Skills (moduler/resurser) och OpenCode.

## Anpassning till projektets storlek

En enkel GPT med ett enda sammanhängande ansvar får ha en Skill. Två eller fler tydligt oberoende förmågor ska normalt resultera i separata Skills. Motivera uttryckligen om en flerfunktions-GPT ändå får en enda Skill.

## Acceptanskriterier för nya projekt

- Projektplanen innehåller en Skill-karta och ansvarsfördelning.
- `gpt-project.yaml` deklarerar varje Skill med unik ID och dess resurser.
- Samtliga fem runtime-distributioner är konfigurerade och bygger från samma canonical definitioner, med runtime-specifika begränsningar dokumenterade.
- Skill-resurser valideras före release; avsaknad av resurser är ett byggfel.
- Ingen distribution får skapa en egen, divergerande uppsättning förmågor.

Detta är ett krav på projektgenerering och granskning, inte en garanti att en befintlig godtycklig projektbeskrivning automatiskt delas upp utan analys.
