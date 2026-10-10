# Granskad upphöjning av ett återställt GPT-projekt

Efter `migrate_legacy_copy.py` kan ett entydigt återställt projektutkast finnas i `reconstructed-canonical/project-draft.json`. Innan ett canonical projektkontrakt skapas måste instruktioner, Knowledge och verktygsberoenden bedömas utifrån faktiskt källmaterial. GPT Byggaren hanterar tekniska frågor internt och frågar enbart om verkligt olösta verksamhetsval.

En intern granskningsfil anger ett projekt-ID, projektnamn, SHA-256 för de återställda instruktionerna och uttryckligen verifierade fält `instruction_semantics`, `knowledge_completeness` och `tool_dependencies`.

Kör `python scripts/promote_reconstructed_project.py --project-root PROJECT --review-file REVIEW.json` efter verifiering.

Verktyget skapar en minimal canonical instruktion och `gpt-project.yaml` men **ingen runtime aktiveras** och resultatet har `reconstruction.status=requires_runtime_validation` samt `release_ready=false`. Det skriver inte över befintliga kontrakt eller instruktioner. Detta är ett mellanläge, inte ett komplett lint-/build-kompatibelt GPT-projekt eller en release.

Granskningsgodkännanden får aldrig genereras automatiskt enbart för att passera spärrarna. Nästa steg kräver kompletterade canonical kontrakt, runtimeparitet och separat releasevalidering.

## Återupptagningsbar projektstruktur

Efter godkänd upphöjning skapas även `docs/development-plan.md`, `project-status.yaml`, `STATUS.md` och `PROJECT.md`. Projektstatus följer `schemas/project-status.schema.json` och är uttryckligen **blocked** tills canonical kontrakt, runtimeparitet och distributionernas funktioner har verifierats. Därmed kan arbetet återupptas från filer utan att chatthistoriken behöver fungera som enda statuskälla.

Den här PR:en skapar inte en fullständig körbar distribution och kringgår inga releasegates. Befintliga filer skrivs inte över.
