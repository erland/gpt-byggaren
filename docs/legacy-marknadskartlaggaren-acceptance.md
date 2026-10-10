# Acceptanstest: äldre Marknadskartläggaren

Underlag: användarens `gpt-marknadskartlaggaren-main.zip` (ett komplett äldre GPT-projekt med `gpt-project.yaml`, källinstruktioner, Knowledge, egna byggskript, Chat ZIP-, äldre Plugin- och Custom GPT-inställningar).

Det äldre projektet klarade sin medföljande `lint_gpt_project.py`, men dess releasevalidering rapporterade saknad leveransmanifest/checksummor och misslyckad runtimeparitetsgrind. Därmed kan man inte utgå från att ett lint-godkänt äldre projekt också är redo för moderna distributioner.

## Säker migrering

Kör `python scripts/migrate_legacy_copy.py --source LEGACY.zip --destination OUTPUT`. Käll-ZIP bevaras. Rapporten innehåller nu `existing_project_assessment` när projektkontrakt finns. Den identifierar äldre `runtime.openai_plugin` som kräver granskad mappning till modern `runtime.plugin`, saknade runtime build-target-kontrakt och behov av oberoende paritetsgranskning. Resurser och möjliga verktygsberoenden inventeras utan att automatiskt godkännas.

Denna PR testar motsvarande projektstruktur med en **liten syntetisk regression-fixture**. Den bifogade original-ZIP-filen checkas inte in i repot. Detta är inte ett godkänt fyr-runtime-end-to-end-test: att skapa fungerande moderna paket kräver ytterligare verifiering av adapterkontrakt och dokumenterad funktionell paritet.
