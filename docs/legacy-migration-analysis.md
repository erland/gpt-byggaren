# Legacy migration analysis – GPT Byggaren

## Syfte

Detta dokument definierar hur befintliga GPT Byggaren-projekt ska analyseras inför migration till den nya plattformsneutrala modellen med canonical kontrakt och flera runtime-adapters.

Målet är att migrera **struktur och metadata utan att skriva om domänbeteendet**.

Steg 13 är analys och migrationskontrakt. Automatisk förändring av legacyprojekt införs först i efterföljande steg.

## Grundprinciper

1. Canonical instruktion och domänbeteende ska bevaras.
2. Migration får lägga till kontrakt och runtime-adapters men får inte byta betydelse på befintliga regler.
3. Befintliga Chat ZIP- och Custom GPT-distributioner ska fortsätta kunna byggas under migrationen.
4. Osäker information ska markeras som osäker, inte gissas.
5. En `scripts/`-katalog är inte bevis på runtime-tools.
6. Generated/runtime-filer får inte göras till canonical source.
7. Migration ska vara idempotent: ett redan migrerat kontrakt ska inte migreras på nytt.

## Legacyklasser

### L0 – saknar GPT Byggaren-kontrakt

Projektet saknar `gpt-project.yaml` eller har en okänd struktur.

Åtgärd:

- inventera filer,
- identifiera canonical instruktion,
- identifiera eventuell status/plan,
- skapa migrationsrapport,
- kräva explicit migration innan normal adapterbuild.

Automatisk omskrivning ska inte ske.

### L1 – äldre GPT Byggaren-projekt

Projektet har `gpt-project.yaml` men använder äldre Chat ZIP/Custom GPT-orienterade fält.

Typiska signaler:

- platt `capabilities` utan `contract_version`,
- workflow med `project_zip`,
- runtime parity med fasta `chat_zip` och `custom_gpt`,
- ingen `artifacts`, `workspace_state` eller `tools`-sektion.

Detta är huvudmålgruppen för automatisk migration.

### L2 – delvis migrerat projekt

Projektet har ett eller flera nya kontrakt men saknar andra.

Åtgärd:

- behåll befintliga nya kontrakt oförändrade,
- migrera endast saknade delar,
- rapportera konflikter mellan legacyfält och nya kontrakt.

### L3 – aktuellt projekt

Projektet har versionerade capability-, artifact-, workspace/state- och tool-kontrakt och använder generisk runtime compatibility.

Ingen migration behövs.

## Migrationsbeslut

Varje förändring klassificeras som:

- `safe_auto` – entydig och beteendebevarande,
- `auto_with_warning` – rimlig härledning men kräver synlig varning,
- `manual_review` – flera möjliga betydelser eller risk för beteendeförändring,
- `not_applicable`.

Migration ska kunna producera dessa beslut maskinläsbart i ett senare steg.

## Capability migration

### Safe auto

Äldre capabilityfält kan normaliseras via den befintliga aliasmappningen:

| Legacy | Canonical |
| --- | --- |
| `web` | `web` |
| `data_analysis` | `code_execution` |
| `file_handling` | `filesystem` |
| `image_generation` | `image_generation` |
| `structured_knowledge` | `structured_data` |

Äldre nivåer normaliseras:

- `likely_required` → `recommended`
- `not_recommended` → `not_required`

### Auto with warning

`file_handling` kan inte alltid avgöra skillnaden mellan read och write. Om legacyvärdet bara uttrycker ett gemensamt behov får migrationen sätta samma nivå för read/write men rapportera att riktningen härletts.

### Manual review

Capability som inte finns i aliasmappningen får inte tappas. Den ska ligga kvar i migrationsrapporten som okänd requirement tills användningsfallet eller projektets instruktion ger tillräcklig evidens.

## Artifact migration

### Safe auto

Legacy-output kan mappas:

| Legacy | Canonical |
| --- | --- |
| `project_zip` | `project_package` |
| `chat_zip` | `runtime_package` |
| `custom_gpt_zip` | `runtime_package` |
| `claude_zip` | `runtime_package` |
| `opencode_zip` | `runtime_package` |
| `validation_report` | `validation_report` |
| `parity_report` | `parity_report` |
| `checksums` | `checksums` |

Konkreta ZIP-namn ska fortsatt vara delivery/runtime-detaljer, inte separata canonical artifactdefinitioner.

### Manual review

Projekt som producerar domänspecifika outputfiler, exempelvis en modell, rapport, bok eller export, måste inventeras separat. Dessa artefakter får inte automatiskt kollapsas till `runtime_package`.

## Workspace/state migration

### Safe auto

Om legacyprojektet uttryckligen stödjer:

- `resume_from_project_zip`, eller
- `resume_from_project_package`,

och tidigare chatthistorik inte krävs för att fortsätta, kan migrationen härleda:

- persistent workspace,
- portable workspace,
- state authority `workspace_file`,
- `project-status.yaml` som statefil när den finns.

### Auto with warning

Om resume stöds men status bara finns i mänsklig dokumentation kan persistent state rekommenderas men inte deklareras fullt realiserad förrän en strukturerad statefil identifierats eller skapats.

### Manual review

Om arbetsflödet uttryckligen använder chatthistorik som enda progresskälla måste migrationen inte låtsas att persistent state redan finns.

## Tool migration

Tool-migration är avsiktligt den mest konservativa delen.

### Safe auto

Endast redan explicit deklarerade legacy-tools får normaliseras automatiskt.

### Inte safe auto

Följande får **inte** automatiskt bli runtime-tools:

- alla filer i `scripts/`,
- CI-scripts,
- release-scripts,
- migrationsscripts,
- engångsverktyg,
- testscripts.

Att en canonical instruktion nämner ett script är evidens men inte ensam tillräckligt för att definiera requirement, mutationsegenskap eller runtime fallback.

### Manual review

För varje potentiellt runtime-tool ska migrationen avgöra:

- semantic operation/id,
- purpose,
- requirement,
- type,
- om det muterar workspace,
- determinism,
- fallback när runtime saknar verktyget.

System Modeller är referensfallet där flera lokala scripts sannolikt ska bli tools. Marknadskartläggaren är referensfallet där tool-kontraktet kan förbli minimalt eller tomt.

## Runtime migration

### Chat ZIP och Custom GPT

Befintliga runtimeinställningar ska bevaras och kopplas till de nya canonical kontrakten.

Legacy `primary_runtime` ska inte användas som canonical norm. Om projektet uttryckligen har ett produktbeslut om primär runtime får det bevaras som runtime preference, men compatibility ska fortfarande bedömas mot canonical kontrakt.

### Claude

Claude ska inte läggas till enbart för att migration sker. Lägg till adaptern först när projektets canonical beteende kan representeras meningsfullt i Claude Projects.

### OpenCode

OpenCode ska inte aktiveras mekaniskt för alla legacyprojekt.

Aktivering är normalt säker när:

- canonical instruktion finns,
- workspace kan representeras som filer,
- required state inte enbart ligger i chatthistorik,
- required tools antingen kan projiceras eller tydligt markeras reducerade/missing.

Projekt med lokala scripts behöver tool-inventering innan OpenCode kan betraktas som fullvärdig.

## Runtime parity migration

Legacyrapporter med fasta `chat_zip`/`custom_gpt`-fält kan normaliseras till schema version 2.

Migrationen ska:

1. använda canonical kontrakt som referens,
2. skapa dynamisk runtime-matris,
3. bevara gamla states där betydelsen är tydlig,
4. inte fabricera Claude/OpenCode-states innan adaptrarna analyserats.

## Canonical source preservation

Följande ordning ska användas för att identifiera sanningskällor:

1. explicit canonical instruction enligt `gpt-project.yaml`,
2. canonical policies/schemas enligt projektkontrakt,
3. strukturerad projektstatus,
4. projektplan/dokumentation,
5. runtime-generated files endast som evidens,
6. dist/build-filer aldrig som canonical source.

Om samma beteenderegel finns både canonical och i runtimefil ska canonical version vinna.

Om regeln bara finns i en generated runtimefil ska den flaggas för manuell bedömning innan migration.

## Migreringsrapport

Steg 14 bör producera en maskinläsbar rapport med minst:

```yaml
migration:
  source_class: L1
  target_contract_version: 1
  status: ready_with_warnings

decisions:
  - area: capabilities
    action: normalize
    confidence: safe_auto

  - area: workspace_state
    action: derive_from_resume
    confidence: safe_auto

  - area: tools
    action: inventory
    confidence: manual_review
    evidence:
      - scripts/validate_model.py

warnings:
  - Scripts were found but were not promoted to runtime tools automatically.
```

Rapporten ska vara möjlig att granska innan projektet skrivs om.

## Föreslagen migrationspipeline

```text
legacy project
    ↓
inventory
    ↓
classify legacy level
    ↓
detect canonical sources
    ↓
normalize safe contracts
    ↓
collect warnings/manual-review items
    ↓
migration report
    ↓
apply migration
    ↓
lint + tests + existing runtime build
    ↓
optional new runtime adapters
```

## Idempotens

Efter migration ska en andra körning:

- känna igen versionerade kontrakt,
- inte skriva över explicita användarval,
- inte duplicera runtimekonfiguration,
- inte skapa nya tool-definitioner utan ny evidens,
- ge `no_changes` när projektet redan är aktuellt.

## Konflikter

Om legacyfält och nytt kontrakt säger olika saker ska migrationen:

1. behålla det nya explicita kontraktet,
2. rapportera legacyfältet som konflikt,
3. inte automatiskt skriva över den nyare modellen.

## Teststrategi för nästa steg

Automatisk migration bör minst testas med:

1. enkelt legacyprojekt utan scripts,
2. legacyprojekt med Chat ZIP + Custom GPT,
3. resume-projekt med `project-status.yaml`,
4. projekt med scripts som **inte** ska bli tools,
5. projekt med explicit legacy-tool,
6. delvis migrerat projekt,
7. redan aktuellt projekt,
8. konflikt mellan legacy- och canonical kontrakt.

## Referensprojekt

### Marknadskartläggaren

Förväntad migration:

- capability normalisering,
- artifact-kontrakt för Markdownrapport + runtime package,
- persistent research state om projektet använder flerstepsjournal,
- få eller inga lokala runtime-tools,
- OpenCode kan läggas till utan omfattande tool-wrapperlager.

### System Modeller

Förväntad migration:

- portable workspace är central,
- strukturerad state bör vara explicit,
- modell-/validerings-/paketeringsscripts måste inventeras som runtime-tools,
- OpenCode kan ge hög paritet när tool-kontraktet är korrekt deklarerat,
- scripts får inte masspromoteras; varje operation behöver semantic id och purpose.

## Definition of Done för steg 13

Steg 13 är klart när:

- legacyklasser är definierade,
- safe-auto kontra manual-review är definierat per kontraktsområde,
- canonical source-preservation är definierat,
- migrationsrapportens minimiinnehåll är definierat,
- OpenCode-aktivering för legacyprojekt har tydliga kriterier,
- testfallen för automatisk migration är definierade,
- nästa steg kan implementera migration utan att behöva fatta nya arkitekturbeslut.


## Automatisk migration – steg 14

Migreringsverktyget finns i:

```text
scripts/migrate_legacy_project.py
```

Standardkörning gör endast inventory/report:

```bash
python scripts/migrate_legacy_project.py --project-root /path/to/project
```

Maskinläsbar JSON:

```bash
python scripts/migrate_legacy_project.py --project-root /path/to/project --json
```

Spara YAML-rapport:

```bash
python scripts/migrate_legacy_project.py \
  --project-root /path/to/project \
  --report-file migration-report.yaml
```

Applicera säkra förändringar:

```bash
python scripts/migrate_legacy_project.py \
  --project-root /path/to/project \
  --apply
```

### Apply-semantik

`--apply` skriver endast nya canonical kontraktssektioner för områden där migrationen är `safe_auto` eller `auto_with_warning`.

Om ett område innehåller `manual_review`:

- det området lämnas oförändrat,
- andra oberoende säkra områden får fortfarande migreras,
- osäker legacyinformation får inte tappas.

Exempel:

- okänd legacy-capability → `capabilities` lämnas oförändrad,
- domänspecifik legacy-artifact → `artifacts` lämnas oförändrad,
- scripts utan explicit legacy-tool-kontrakt → inget tomt `tools`-kontrakt skrivs, eftersom det skulle kunna dölja ett framtida tool-inventeringsbehov.

### Vad verktyget aldrig ändrar i steg 14

- canonical instruktion,
- domänregler,
- runtime-generated files,
- scripts,
- tester,
- Knowledge,
- domänspecifika outputs.

### Idempotens

En andra `--apply` på ett redan migrerat projekt ska ge `no_changes` och inte skriva om explicita kontrakt.
