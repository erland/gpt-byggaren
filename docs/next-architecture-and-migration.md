# Målarkitektur och migrationsstrategi – nästa generation GPT Byggaren

Status: **Förslag / beslutsunderlag**. Detta dokument ändrar inte runtimekontrakt eller aktiva distributionsmål.

## Produktprinciper (icke förhandlingsbara)

1. **Idé först.** Användaren kan börja med en enda mening. GPT Byggaren analyserar behov, väljer lämpliga runtimes, tools, arkitektur och presentation själv. Tekniska val ska inte flyttas till användaren.
2. **Samma canonical kärna.** Beteende, kunskap, verktyg, artefakter och status är plattformsoberoende; runtime-adapters får inte ändra kärnbeteendet.
3. **Progressiv presentation.** Använd text som komplett bas. Använd Intelligent UI när hosten faktiskt kan visa det och det förbättrar en konkret uppgift; kräv aldrig UI för att slutföra den.
4. **Mobilkompatibel plugin som standard.** Generera **ingen `mcp.json` någonstans i plugin-ZIP**. Erfarenhet från installation visar att sådana paket riskerar att endast kunna importeras från dator. Kontrollera faktisk import separat på mobil och desktop; statisk ZIP-validering är inte tillräcklig.
5. **Inga implicita runtimegarantier.** Paketerade scripts innebär inte att de kan köras; deklarera hostkrav, fallback och skillnader i parityrapport.
6. **Bevara originalsäkert.** Migrering ska vara idempotent, spårbar och icke-destruktiv och aldrig tyst tappa instruktioner eller Knowledge.

## Föreslagen målbild

```text
En idé / ett befintligt projekt eller ZIP
                  |
       Detektera och analysera
                  |
  Canonical projekt + status + skills
                  |
      Förmåge- och runtimeanalys
                  |
       +----------+----------+-----------+
       |          |          |           |
    Chat ZIP   Plugin     Claude      OpenCode
       |          |          |           |
     text      text +     text         text
              valfri UI
```

Custom GPT / ChatGPT Builder avvecklas som **nytt aktivt mål** i ett senare steg. Äldre Custom GPT-paket fortsätter vara **importkällor**. Inget annat runtime-mål får försämras som bieffekt av ChatGPT-specifika förbättringar.

## Nya kontrakt (förslag; inte implementerat ännu)

```yaml
presentation:
  mode: adaptive
  text_fallback: required
  interactive_ui: when_supported_and_useful
  logic_independent_of_presentation: true

runtime_dependencies:
  external_tools:
    discovery: optional
    missing_tool_behavior: explain_or_fallback
  plugin:
    package_must_not_include:
      - "**/mcp.json"
    mobile_import_verification: manual_release_gate
```

Undvik att hårdkoda `GPT-6` eller `GPT-5.6` som presentationsvillkor. Hostens faktiska stöd avgör. Formulär och valkontroller får bara användas när de *minskar* användarens arbete, aldrig för obligatorisk runtimekonfiguration.

## Migration som normal användarresa

Utgångspunkter:
- Projekt-ZIP med gpt-project.yaml och status
- Äldre Chat ZIP
- Äldre Custom GPT/Builder-export eller instruktioner + Knowledge
- Plugin ZIP
- Claude-/OpenCode-distribution där innehållet kan extraheras

Arbetsflöde:

1. **Identifiera** källtyp, projektversion och vilka filer som är canonical respektive genererade.
2. **Inventera** instruktioner, Knowledge, skills, verktyg, fallback och status. Registrera saknade originalkällor, t.ex. vid import av enbart distributions-ZIP.
3. **Planera** deterministiska transformationer till aktuellt canonical-kontrakt; för osäker rekonstruktion använd tydliga antaganden och markera `review_required`.
4. **Migrera till nytt projekt/ny version**, inte över originalet. Behåll provenance och migrationsrapport med filinventering, transformationslista, bevarat, ersatt, ej återvunnet och kända begränsningar.
5. **Validera** schema, policy, scriptreferenser, runtimeparitet, deterministiskt build och säkerhet; kontrollera att plugin-ZIP saknar `mcp.json`.
6. **Regressionskontrollera** avgörande beteendescenarier före release. Om ett kritiskt krav går förlorat, blockera berörd runtime och redovisa varför.

Migrering från distribution till fullständigt utvecklingsprojekt är best effort; genererade paket kan sakna ursprungskontrakt. Presentera aldrig rekonstruerad data som om den säkert kom från källprojektet.

## Genomförande i separata PR:er

### PR 1 – denna arkitektur- och migrationsplan
- Förankra principerna och testmatrisen; inga ändringar i aktiv byggpipeline.
- Kontrollera befintliga `scripts/migrate_legacy_project.py`, `scripts/migrate_project_for_runtime.py` och runtime parity före implementering.

### PR 2 – Avveckla Custom GPT som aktiv runtime
- Sluta rekommendera och generera Custom GPT i nya projekt.
- Migrera äldre `runtime.custom_gpt` till historisk indata utan dataförlust.
- Anpassa schemas, build, validering, CI, release, instruktioner, mallar och tester atomärt.
- Bevara historik och legacy-fixtures, separera dem från aktiva regressionsfall.

### PR 3 – Hårda plugin- och mobilkrav
- Behåll skills-first; förbjud alla `mcp.json` i plugin-ZIP med test över ZIP-poster.
- Stöd frivilliga externa verktyg via capability discovery och textbaserad fallback.
- Validera faktiska paketgränser för plugin mot aktuell dokumentation och verifiera manuell mobil-/desktopimport inför release.
- Lägg inte till krav på att användaren installerar MCP eller själv väljer adapter.

### PR 4 – Intelligent UI som valfri presentationsadapter
- Inför presentation i canonical-kontrakt och runtime parity.
- UI-instruktioner får inte ersätta affärslogik eller stegvis textdialog.
- Testa samma scenario med och utan Intelligent UI, inklusive när hosten saknar stöd.
- Separera dynamiskt Intelligent UI från egenutvecklade plugin-komponenter.

### PR 5 – Migreringsautomatik och regressionsmatris
- Stöd ovanstående källtyper; idempotens, versionsmärkning, rapport och blockerande säkerhetskontroller.
- Testa nya projekt från en enda idé, många `Gör nästa steg`, legacy-import, mobilkompatibel plugin-ZIP, saknade externa tools, återupptagning och modellneutral textfallback.

## Definition of Done för hela förändringen

- En idé räcker fortfarande för att få analys och rekommenderat nästa steg.
- Ingen teknikdialog om runtimes/MCP/UI krävs vid normal användning.
- Chat ZIP, Plugin, Claude och OpenCode bygger, valideras och följer samma canonical kontrakt.
- Inga genererade plugin-ZIP innehåller `mcp.json`; faktisk mobil-/desktopimport har verifierats.
- Äldre projekt går att läsa och migrera utan att original skrivs över; saknade data anges uttryckligen.
- Textbaserad upplevelse klarar hela uppgiften även utan Intelligent UI.
- CI testar deterministiska krav och kör inte onödigt dyr extern exekvering.
