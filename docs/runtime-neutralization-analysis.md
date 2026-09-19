# Runtime-neutralization analysis

## Syfte

Detta dokument genomför steg 1 i planen för bredare runtime-stöd i GPT Byggaren.

Målet är att identifiera var nuvarande projektmodell, instruktioner, schemas, tester och build/release-flöden antar att de enda runtime-målen är Chat ZIP och Custom GPT. Steget ska **inte** ändra runtimebeteende. Det skapar endast ett konkret underlag för kommande neutralisering.

Målbilden för nästa utvecklingsfas är att samma canonical assistant-projekt ska kunna ligga till grund för åtminstone:

- ChatGPT Chat ZIP,
- ChatGPT Custom GPT,
- Claude portable ZIP,
- OpenCode.

Senare runtime-mål, exempelvis Gemini och Microsoft Copilot, ska kunna läggas till utan att canonical domänbeteende behöver dupliceras.

## Sammanfattning

GPT Byggaren har redan flera egenskaper som underlättar neutralisering:

- canonical instruktion ligger separat från distributionerna,
- Knowledge, schemas, templates och scripts har egna lager,
- Chat ZIP och Custom GPT byggs redan som projektioner från samma projekt,
- runtime-paritet bedöms per capability,
- projektstatus och återupptagning är maskinläsbara,
- buildsystemet har tydliga targets och deterministiska distributionsartefakter.

Den huvudsakliga begränsningen är därför inte projektstrukturen i sig utan att flera kontrakt fortfarande modellerar **två konkreta ChatGPT-orienterade runtime-mål direkt** i stället för att först beskriva plattformsneutrala behov.

De viktigaste neutraliseringsområdena är:

1. capability-modellen,
2. artifact/output-modellen,
3. workspace och state,
4. tool/runtime dependencies,
5. runtime-paritet,
6. analysprofiler och rekommendationer,
7. buildtargets och artefaktnamn,
8. release readiness och platform validation,
9. tester/evals,
10. dokumentation och terminologi.

## Klassificeringsmodell

Varje identifierad koppling klassificeras som en av följande typer.

### CANONICAL

Domän- eller assistentbeteende som ska vara gemensamt för alla runtimes.

Exempel:

- analysera verksamhetsbehov före teknikval,
- rekommendera nästa steg från faktisk projektstatus,
- testa och validera efter relevanta utvecklingssteg.

### GENERAL_CAPABILITY

Ett behov som bör uttryckas plattformsneutralt.

Exempel:

- webbresearch,
- filsystem read/write,
- kod- eller kommandokörning,
- persistent state,
- strukturerad data,
- externa verktyg.

### GENERAL_ARTIFACT

Ett krav på vad assistenten ska producera, men inte hur en viss plattform levererar det.

Exempel:

- Markdownrapport,
- ZIP-projekt,
- JSON/YAML-data,
- PDF.

### GENERAL_WORKFLOW_STATE

Regler för hur ett flerstegsarbete fortsätter och hur state lagras.

Exempel:

- `Gör nästa steg`,
- projektstatus,
- researchjournal,
- workspace,
- resume.

### PLATFORM_ADAPTER

Beteende eller format som hör hemma i en konkret runtime-adapter.

Exempel:

- ChatGPT Custom GPT Builder-filer,
- OpenCode `AGENTS.md`,
- OpenCode Skills,
- Claude-specifik startfil.

### BUILD_DISTRIBUTION

Paketering, filnamn, distributionslayout, checksummor och releaseartefakter.

---

# 1. `gpt-project.yaml`

## Nuvarande koppling

`runtime` modellerar explicit:

- `chat_zip`,
- `custom_gpt`.

`primary` är visserligen `none`, vilket redan stödjer tanken om jämbördiga distributioner, men runtimekontraktet är fortfarande strukturellt begränsat till de två nuvarande målen.

Custom GPT-delen innehåller dessutom plattformsspecifika begrepp:

- instruction character limit,
- Knowledge file limit,
- Builder-layout,
- compatibility templates,
- platform validation.

Chat ZIP-delen innehåller egen layout, include/exclude-regler och entrypoint.

## Klassificering

- runtimebehov: **GENERAL_CAPABILITY**
- Chat ZIP-layout: **PLATFORM_ADAPTER / BUILD_DISTRIBUTION**
- Custom GPT-limits och Builder-format: **PLATFORM_ADAPTER**
- artifacts: **GENERAL_ARTIFACT + BUILD_DISTRIBUTION**

## Senare åtgärd

Behåll runtimeadaptrarna, men lägg plattformsneutrala kontrakt ovanför dem:

- capabilities,
- artifacts,
- workspace/state,
- tools.

Runtime-adaptrar ska läsa dessa kontrakt i stället för att canonical beteende härleds från adapteregenskaper.

---

# 2. Capability-modellen

## Nuvarande koppling

Projektet har idag generella capabilitynamn som:

- web,
- data_analysis,
- image_generation,
- file_handling,
- structured_knowledge.

Det är en bra grund, men delar av Custom GPT-flödet och genererade projekt använder mer plattformsspecifika uttryck, exempelvis Code Interpreter/data analysis eller Builder-capabilities.

## Klassificering

**GENERAL_CAPABILITY**

## Problem

Samma verksamhetsbehov kan realiseras olika:

- ChatGPT kan erbjuda fil- och analysverktyg,
- Claude kan ha andra fil-/verktygsmekanismer,
- OpenCode kan använda lokalt filsystem, shell och scripts.

Canonical modellen bör därför beskriva **förmågan som krävs**, inte produktnamnet på verktyget.

## Senare åtgärd

Inför ett capability-schema som minst kan beskriva:

- web,
- filesystem read/write,
- shell,
- code execution,
- structured data,
- persistent state,
- external tools/MCP.

Legacyfält ska kunna mappas till den nya modellen.

---

# 3. Runtime parity

## Nuvarande koppling

Följande delar antar uttryckligen Chat ZIP och Custom GPT:

- `docs/runtime-parity.md`,
- `src/runtime-policy/runtime-parity-policy.md`,
- `schemas/runtime-parity.schema.json`,
- kompatibilitetsrapportering.

Schemafält och exempel har runtime-specifika kolumner och `primary_runtime` begränsas till `chat_zip` eller `custom_gpt`.

## Klassificering

Själva idén: **CANONICAL / GENERAL_CAPABILITY**

Nuvarande representation: **PLATFORM_ADAPTER**

## Senare åtgärd

Gör paritetsrapporten runtime-oberoende.

I stället för fasta fält:

```yaml
chat_zip: equivalent
custom_gpt: reduced
```

bör den kunna uttrycka:

```yaml
runtimes:
  chatgpt_chat: equivalent
  chatgpt_custom: reduced
  claude: equivalent
  opencode: equivalent
```

Detta bör vara en av de viktigaste strukturella förändringarna.

---

# 4. Analysmodell och referensprofiler

## Nuvarande koppling

`docs/analysis-model.md` och profilerna kodar bland annat:

- `chat_zip_or_custom_gpt`,
- `custom_gpt_or_chat`,
- `zip_first_advanced`.

Profilen `zip_first_advanced` har redan delvis neutraliserats semantiskt genom beskrivningen "advanced dual distribution", men ID och rekommendationsfält bär historisk runtimebetydelse.

## Klassificering

Profilens verksamhets-/komplexitetsnivå: **CANONICAL**

Runtimeval: **PLATFORM_ADAPTER**

## Problem

Profilval och runtimeval är idag för tätt kopplade. En avancerad workflow-GPT kan i framtiden vara bäst lämpad för OpenCode utan att dess analysprofil egentligen förändras.

## Senare åtgärd

Separera:

- assistant complexity/profile,
- capability requirements,
- runtime suitability.

Behåll gamla profil-ID:n som legacy aliases under migrationsperiod om det behövs.

---

# 5. Buildsystem

## Nuvarande koppling

`scripts/build_distributions.py` känner explicita targets:

- project,
- chat,
- custom-gpt.

Scriptet innehåller separata builderfunktioner och artifactklassificering som identifierar `-chat-` och `-custom-gpt-` i filnamn.

`build_direct.py`, CI och releaseworkflow förväntar samma artefakter.

## Klassificering

**BUILD_DISTRIBUTION**

## Bedömning

Detta är en naturlig adapterpunkt och behöver inte "neutraliseras bort". Buildsystemet bör fortsatt ha konkreta runtime-targets.

Förändringen bör i stället vara att builders konsumerar ett gemensamt canonical kontrakt.

## Senare mål

Targets kan utvecklas mot:

```text
project
chatgpt-chat
chatgpt-custom
claude
opencode
```

Legacyaliaset `chat` kan behållas temporärt.

---

# 6. Direct build och delivery manifest

## Nuvarande koppling

`docs/direct-build.md` och buildverktygen förväntar tre centrala ZIP-artefakter:

- project,
- chat,
- custom-gpt.

Delivery manifest klassificerar artefakter utifrån nuvarande filnamn.

## Klassificering

**BUILD_DISTRIBUTION**

## Senare åtgärd

Gör artifact-typer extensibla och runtime-ID-baserade, men behåll checksummor och delivery manifest som generell mekanism.

---

# 7. Release readiness

## Nuvarande koppling

`scripts/assess_release_readiness.py` har explicit:

- Custom GPT enabled-check,
- runtime parity gate,
- custom GPT platform validation gate,
- Chat build-state checks.

## Klassificering

Release readiness-konceptet: **CANONICAL**

Runtime-specifika gates: **PLATFORM_ADAPTER**

## Senare åtgärd

Bygg en generell gate-modell:

- canonical project validation,
- required runtime builds,
- runtime compatibility,
- runtime-specific validation.

Varje adapter ska kunna registrera sina egna gates.

---

# 8. Platform validation

## Nuvarande koppling

`platform_validation` i `gpt-project.yaml` är huvudsakligen utformat runt Custom GPT:

- instruction length,
- knowledge file count,
- builder package,
- conversation starters,
- capabilities,
- compatibility report.

## Klassificering

Valideringsmekanismen: **CANONICAL**

Kontrollerna: **PLATFORM_ADAPTER**

## Senare åtgärd

Dela upp:

```text
canonical validation
runtime validation
```

Exempel:

- ChatGPT Custom: instruction/Knowledge limits,
- Claude: package/start-instruction consistency,
- OpenCode: AGENTS.md, skillstruktur, lokala tool paths.

---

# 9. Schemas

## Identifierade hårda kopplingar

Minst följande schemas innehåller runtimeantaganden som måste ses över:

- `schemas/runtime-parity.schema.json`
- `schemas/e2e-scenario.schema.json`
- `schemas/analysis-recommendation.schema.json`
- Custom GPT-specifika schemas

## Klassificering

Blandat:

- generiska schemas ska neutraliseras,
- adapterschemas ska förbli plattformsspecifika.

## Senare åtgärd

Undvik ett enda gigantiskt "alla runtimes"-schema.

Föredragen modell:

```text
schemas/
  canonical/
  runtime/
    chatgpt/
    claude/
    opencode/
```

Exakt katalogstruktur beslutas i senare steg; detta steg inför ingen flytt.

---

# 10. Tests och E2E

## Nuvarande koppling

`evals/e2e/blank-idea-001.yaml` förväntar bland annat:

- `primary_runtime: chat_zip`,
- `custom_gpt_enabled: true`.

`scripts/run_e2e_blank_idea.py` skapar runtimekonfiguration direkt för Chat ZIP och Custom GPT.

Referensprojekten uttrycker också runtimeutfall med nuvarande två runtimefamiljer.

## Klassificering

Scenariointention: **CANONICAL**

Nuvarande runtimeförväntningar: **PLATFORM_ADAPTER**

## Senare åtgärd

Dela tester i:

1. canonical behavior/capability expectations,
2. runtime projection expectations.

Exempel:

```yaml
required_capabilities:
  - web
  - persistent_artifact

expected_runtimes:
  chatgpt_chat: supported
  claude: supported
  opencode: supported
```

---

# 11. GPT linter

## Nuvarande koppling

`scripts/lint_gpt_project.py` känner symboliska runtimevärden som:

- `chat_zip`,
- `custom_gpt`.

Den validerar även runtime dependencies utifrån dagens kontrakt.

## Klassificering

Lintermekanism: **CANONICAL**

Symboliska runtime-ID:n: **PLATFORM_ADAPTER**

## Senare åtgärd

Låt linter läsa registrerade runtime-ID:n från projekt-/schema-konfiguration i stället för hårdkodad lista där det är praktiskt.

---

# 12. Instruktionsarkitekturen

## Nuvarande styrka

`src/instructions/system.md` innehåller flera verkligt canonical regler:

- analysera verksamhetsbehov före teknikval,
- håll Knowledge separat från beteenderegler,
- validera projekt,
- rekommendera nästa steg från faktisk status,
- återuppta projekt från projektfiler snarare än tidigare chatthistorik.

Detta bör bevaras.

## Nuvarande koppling

Kärnkontraktet säger också att GPT Byggaren normalt bygger både Chat ZIP och Custom GPT från samma canonical kontrakt.

Det är korrekt historiskt men bör på sikt generaliseras till flera runtime-projektioner.

## Klassificering

Domänregler: **CANONICAL**

Namngivna distributioner i kärnkontraktet: **PLATFORM_ADAPTER**

---

# 13. Knowledge-arkitekturen

## Nuvarande styrka

Knowledge behandlas redan som canonical material och Custom GPT har en projektion/komprimeringsstrategi.

Detta är mycket nära önskad framtida modell.

## Klassificering

Canonical Knowledge: **CANONICAL**

Custom GPT file-limit/packing: **PLATFORM_ADAPTER**

## Senare åtgärd

Låt varje adapter välja Knowledge-strategi:

- full,
- filtered,
- consolidated,
- referenced/on-demand.

OpenCode kan exempelvis använda filerna direkt eller via skill references.

---

# 14. Artifact/output

## Nuvarande koppling

GPT Byggarens workflow säger bland annat:

- utvecklingsplan som nedladdningsbar Markdown,
- projekt-ZIP efter utvecklingssteg,
- distributionsartefakter som ZIP.

Dessa regler blandar delvis **vad** som ska produceras med **hur en chattruntime levererar det**.

## Klassificering

Format/artefaktkrav: **GENERAL_ARTIFACT**

"Nedladdningsbar"/"länkad i chatten": **PLATFORM_ADAPTER**

## Senare åtgärd

Inför explicit artifact-kontrakt.

Exempel:

```yaml
artifacts:
  development_plan:
    format: markdown
    persistent: true
  project:
    format: zip
    persistent: true
```

Runtime-adaptern bestämmer leveransmekanism.

---

# 15. Workspace och state

## Nuvarande styrka

GPT Byggaren själv har en stark modell för persistent projektstatus:

- `gpt-project.yaml`,
- `project-status.yaml`,
- utvecklingsplan,
- resume-flöde.

Det är redan plattformsneutralt i grunden.

## Begränsning

Genererade GPT:er har inte ännu ett generellt kontrakt för:

- eget runtime-state,
- separat användarworkspace,
- projektdata som är skild från assistentpaketet.

Det blir särskilt viktigt för OpenCode och för GPT:er som System Modeller.

## Klassificering

**GENERAL_WORKFLOW_STATE**

## Senare åtgärd

Återanvänd GPT Byggarens egen filosofi: chatthistorik ska inte vara enda sanningskällan när en assistent behöver persistent state.

---

# 16. Tool/runtime dependencies

## Nuvarande koppling

Projektet har `required_runtime_dependencies`, men modellen uttrycker främst fil-/kontraktsberoenden och är inte ett fullständigt verktygskontrakt.

## Klassificering

**GENERAL_CAPABILITY / GENERAL_WORKFLOW_STATE**

## Senare åtgärd

Inför tool-kontrakt som kan uttrycka exempelvis:

- local command,
- script,
- MCP,
- web capability,
- API/action.

Detta ska beskriva vad verktyget gör och vilka preconditions som gäller.

---

# 17. Dokumentation och terminologi

## Nuvarande koppling

Aktiv dokumentation använder genomgående:

- GPT,
- Chat ZIP,
- Custom GPT,
- ChatGPT Builder.

Det är korrekt för nuvarande release och ska **inte** massändras i steg 1.

## Senare princip

Behåll produktnamnet **GPT Byggaren** om så önskas, men använd mer generella interna begrepp där modellen faktiskt blir bredare:

- assistant project,
- canonical assistant contract,
- runtime adapter,
- capability contract.

Användarnära dokumentation kan fortsatt säga "GPT" där det är begripligast.

---

# 18. Föreslagen migrationsordning

Följande ordning minimerar risken att OpenCode blir en parallell speciallösning:

1. capability contract,
2. artifact contract,
3. workspace/state contract,
4. tool contract,
5. generaliserad runtime parity,
6. migrera Chat ZIP till nya kontrakten,
7. migrera Custom GPT,
8. Claude portable runtime,
9. OpenCode base adapter,
10. OpenCode Skills/tool integration,
11. migration av legacyprojekt,
12. cross-runtime evals.

---

# 19. Bakåtkompatibilitetskrav

Kommande steg ska följa dessa regler.

## Legacy read

Projekt som använder nuvarande fält ska kunna läsas och analyseras.

## Explicit migration

Strukturellt större förändringar ska migreras explicit i stället för att gammal semantik tyst tolkas om.

## No domain rewrite

Migration ska inte skriva om en befintlig GPT:s domänbeteende om det inte krävs för att eliminera en konkret runtimekoppling.

## Existing runtime regression gate

Chat ZIP och Custom GPT ska fortsätta byggas och valideras medan den nya modellen införs.

## Adapter-specific degradation

En runtime får ha reducerad funktion, men detta ska uttryckas som capability-paritet och får inte döljas.

---

# 20. Referensprojekt för kommande steg

Två projekt bör användas som kompletterande regressionstest.

## Marknadskartläggaren

Täcker:

- aktuell webbresearch,
- flerstegsworkflow,
- state,
- källhantering,
- Markdownartefakt.

Det är ett bra test för konversations- och researchorienterade assistenter.

## System Modeller

Täcker:

- separat workspace,
- YAML som canonical data,
- schemas,
- lokala scripts,
- deterministiska modelloperationer,
- validering,
- packaging.

Det är ett bra test för agentiska assistenter och OpenCode.

Tillsammans minskar de risken att den nya arkitekturen optimeras för endast en GPT-typ.

---

# 21. Konkreta filer som sannolikt berörs i senare steg

Denna lista är avsiktligt bred och innebär inte att alla filer måste ändras.

## Projektkontrakt

- `gpt-project.yaml`
- `docs/gpt-project-contract.md`
- `docs/analysis-model.md`
- `docs/instruction-architecture.md`
- `docs/runtime-parity.md`
- `docs/platform-validation.md`

## Policies

- `src/runtime-policy/runtime-parity-policy.md`
- `src/runtime-policy/platform-validation-policy.md`
- `src/runtime-policy/analysis-policy.md`
- relevanta build/release policies

## Schemas

- `schemas/runtime-parity.schema.json`
- `schemas/e2e-scenario.schema.json`
- `schemas/analysis-recommendation.schema.json`
- framtida capability/artifact/state/tool schemas

## Scripts

- `scripts/build_distributions.py`
- `scripts/build_direct.py`
- `scripts/validate_distributions.py`
- `scripts/lint_gpt_project.py`
- `scripts/assess_release_readiness.py`
- `scripts/run_e2e_blank_idea.py`
- gemensamt projektmodellbibliotek

## Profiles och evals

- `profiles/*.yaml`
- `evals/e2e/*.yaml`
- `evals/reference-projects/*.yaml`

## CI/release

- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`

---

# 22. Vad som inte ska ändras i steg 1

Detta analyssteg ska inte:

- ändra `gpt-project.yaml`,
- ändra schemas,
- ändra buildtargets,
- ändra Chat ZIP,
- ändra Custom GPT,
- lägga till Claude-runtime,
- lägga till OpenCode-runtime,
- ändra releaseartefakter,
- ändra projektstatus,
- ändra canonical instruktion.

Det gör steg 1 lågrisk och ger ett stabilt underlag för steg 2.

---

# 23. Slutsats

Nuvarande GPT Byggaren behöver inte byggas om från grunden.

Arkitekturen har redan rätt grundidé:

```text
canonical source
      ↓
runtime projection
```

Det som behöver förändras är främst mellanlagret.

Nuvarande modell:

```text
Canonical GPT
   ├── Chat ZIP
   └── Custom GPT
```

bör stegvis utvecklas mot:

```text
Canonical Assistant Project
   ├── capability contract
   ├── artifact contract
   ├── workspace/state contract
   ├── tool contract
   │
   └── runtime adapters
          ├── ChatGPT Chat
          ├── ChatGPT Custom
          ├── Claude
          └── OpenCode
```

Första implementationen efter detta analyssteg bör därför vara **steg 2: ett plattformsneutralt capability-kontrakt**, med bakåtkompatibel läsning av nuvarande projektmodell.
