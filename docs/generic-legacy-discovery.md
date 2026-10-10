# Generell migrationsanalys

Alla migrerade äldre GPT-projekt, både med och utan kända manifest, får nu ett separat `generic_discovery` i `MIGRATION-REPORT.json`. Det innehåller en strukturagnostisk inventering med relativa sökvägar, storlekar, SHA-256 och **kandidater** till instruktioner, Knowledge, skript och konfiguration. Okända filnamn inventeras också; de kastas inte bort bara för att en äldre GPT-version saknar känd kataloglayout.

## Uppdelning av ansvar

Den deterministiska delen öppnar ZIP säkert, kopierar till separat projekt, registrerar källmaterial och föreslår kandidater. En AI-stödd analys får därefter tolka innehållet och föreslå en plattformsneutral modell. Varje slutsats måste peka tillbaka på ursprunglig fil och SHA-256. Flera möjliga tolkningar måste redovisas som osäkerhet och granskas, inte ersättas med påhittad funktionalitet.

Därmed är äldre formatsignaturer **valfria genvägar**, aldrig ett krav för inventering. Denna första PR för den generella arkitekturen implementerar inte automatisk AI-klassificering eller färdiga moderna distributioner. Projektet ska fortsatt vara `analysis_required` och `release_ready=false` till dess att materialet förståtts och validerats.

Utveckla vidare genom att lägga till ett tydligt, granskningsbart analysresultat och en konverterare till canonical kontrakt. Acceptanstester ska omfatta okänd katalogstruktur, äldre kompletta projekt, Chat ZIP och andra distributionspaket, inte bara Marknadskartläggaren.
