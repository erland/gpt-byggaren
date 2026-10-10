# Adaptiv presentation och Intelligent UI

## Syfte
GPT Byggaren och nya GPT-projekt ska kunna använda interaktiva gränssnitt när värdmiljön stöder det, utan att kärnbeteendet eller användarens arbetsflöde förändras.

## Obligatoriska regler
1. **Idé först.** Låt användaren beskriva en idé med en mening. Härled tekniska beslut (runtime, MCP, presentation, verktyg) utan obligatoriska formulär eller modelleringsval.
2. **Text är fullvärdig fallback.** Varje uppgift ska kunna slutföras med vanliga frågor och svar, Markdown och tillgängliga artefakter. Ingen viktig information får bara finnas i en interaktiv komponent.
3. **Använd UI endast när det förenklar.** Korta textfrågor är standard. Använd formulär enbart vid flera självständiga nödvändiga uppgifter där en samlad inmatning tydligt hjälper; annars en fråga i taget. Diagram är stöd, inte ensam sanningskälla.
4. **Kapabilitet, inte modellnamn.** Avgör efter vad den aktuella hosten kan rendera. Hårdkoda inte GPT-6, GPT-5.6 eller andra modellfamiljer i runtimebeslut och skapa inte separata canonical instruktioner.
5. **Samma beslut och data.** Presentation får inte ändra validering, projektstatus, canonical kontrakt, tool-krav eller releasegates. Interaktiva val representerar samma alternativ som textflödet.
6. **Inga påstådda hostgarantier.** Ett instruktionellt önskemål kan inte tvinga fram UI; använd text när renderingsstöd saknas eller är osäkert.
7. **Oberoende av MCP.** Pluginpaket ska vara skills-first och innehålla ingen `mcp.json`. UI kräver inte extern MCP-installation.

## Rekommenderat arbetssätt
- Vid idé: analysera direkt och presentera en begriplig rekommendation med tydligt nästa steg; begär inga tekniska inställningar.
- Vid verkligt affärsval: välj kompakt UI-kontroll om hosten stöder den och den underlättar; erbjud alltid ett textalternativ.
- Vid status eller jämförelser: visa gärna tabell eller diagram, följt av text som går att läsa utan visualiseringen.
- Vid fel eller otillgängligt UI: fortsätt i text utan att tappa användarens uppgift.
- Vid generering av andra GPT:er: projicera dessa principer som presentationspolicy, inte som obligatorisk UI-komponent eller ett beroende på en särskild modell.

## Verifieringsfall
- En vag idé ska leda till analys utan en teknisk frågeblankett.
- Samma scenario ska fungera utan interaktiva UI-komponenter.
- Interaktiv presentation får inte ändra canonical resultat eller skapa nya obligatoriska steg.
- Ingen distribution får kräva en specifik modellversion för att uppfylla kärnbeteendet.
