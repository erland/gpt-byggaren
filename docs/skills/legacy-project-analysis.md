# Skill: analysera ett äldre GPT-projekt

## När denna förmåga används
När användaren anger ”Uppgradera denna GPT”, lämnar en äldre ZIP eller vill fortsätta ett okänt GPT-projekt.

## Arbetsgång
1. Gör en säker, icke-destruktiv inventering. Använd den generella inventeringen även om formatet är okänt.
2. Läs faktiska källfiler och identifiera instruktioner, Knowledge, verktyg, arbetsflöden och beroenden.
3. Gör en evidensbaserad tolkning. Varje sakpåstående ska knytas till källa och SHA-256. Filnamn räcker inte som bevis.
4. Validera tolkningen, för över den till ett plattformsneutralt granskningsutkast och redovisa kvarstående osäkerheter.
5. Sätt aldrig release_ready eller aktivera runtime enbart utifrån inventering eller AI-tolkning.

## Operativa verktyg
- scripts/discover_legacy_project.py
- scripts/validate_legacy_interpretation.py
- scripts/project_legacy_analysis.py

## Fallback
Om verktyg inte går att köra: läs materialet manuellt, redovisa underlag och osäkerhet och blockera påståenden om fullständig migrering.
