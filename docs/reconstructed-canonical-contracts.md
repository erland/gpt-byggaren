# Canonical kontrakt efter projektrekonstruktion

När ett äldre projekt har inventerats, rekonstruerats och granskats kan `scripts/complete_reconstructed_contracts.py --project-root PROJECT` komplettera ett redan upphöjt projekt.

Verktyget skapar fyra schema-validerade kontrakt: capabilities, artifacts, workspace/state och tools. Dessa utgår från sådant som med säkerhet finns i återställt projekt; okända verktygsbehov, MCP-integrationer och Knowledge-fullständighet **måste fortfarande bedömas separat**.

En tom capability- eller tool-lista innebär **inte** att dessa saknas i det ursprungliga projektet. Den betyder endast att inga sådana krav får påstås verifierade ännu. Evidens om möjliga beroenden finns kvar i projektutkastet och speglas i `reconstructed-canonical/CONTRACT-VALIDATION.json`.

Samtliga runtimes ska förbli avaktiverade, `release_ready=false`, och status ska förbli blockerad. Dokumentet beskriver ett mellanläge, inte en fullständig modern GPT-distribution. Verifiering av runtimeparitet, komplettering av verktygskontrakt, releasegates och faktisk byggkompatibilitet återstår. Befintliga projektkontrakt och scheman skrivs inte över.
