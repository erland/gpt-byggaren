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

## Äldre migrationsregler från canonical instruktionen (bevarade)


Om användaren uttryckligen ber att ett befintligt GPT-projekt ska fungera i en ny runtime, behandla det som en migrationsintention.

- Inventera projektet och identifiera canonical sources.
- Bevara domänbeteende och canonical instruktion.
- Applicera säkra beteendebevarande migrationer utan att fråga om tekniska adapterdetaljer.
- Aktivera mål-runtimen endast när compatibility är ready.
- Lämna manual-review-områden orörda och redovisa den konkreta nästa åtgärden.
- Exponera inte CLI-flaggor som ett krav för användaren; de är intern implementation.
