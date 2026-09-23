# GPT Byggaren

GPT Byggaren hjälper dig att gå från en idé om en GPT till ett **strukturerat, testat, paketerat och versionshanterat GPT-projekt**.

Du beskriver främst **vad GPT:n ska hjälpa till med**. GPT Byggaren tar ansvar för att föreslå hur projektet bör struktureras, vilka capabilities som behövs, hur det ska testas och hur det ska distribueras.

Projektet är byggt för stegvis utveckling där projektets status lagras i filer och kan återupptas i en ny konversation utan att tidigare chatthistorik krävs.

## Vad GPT Byggaren gör

Ett normalt arbetsflöde är:

1. Du beskriver GPT-idén och verksamhetsbehovet.
2. GPT Byggaren analyserar målgrupp, arbetsflöden, underlag och önskat resultat.
3. Den rekommenderar lämplig arkitektur, capabilities och ambitionsnivå.
4. Den skapar en projektspecifik utvecklingsplan.
5. När utvecklingen startar skapas en komplett projekt-ZIP.
6. Projektet vidareutvecklas stegvis utifrån faktisk projektstatus.
7. Efter relevanta steg körs lint, tester, validering och project hygiene.
8. När projektet är redo byggs de runtime-distributioner som analysen har aktiverat, exempelvis ChatGPT Chat, Custom GPT, Claude Projects, OpenCode och OpenAI Plugin.
9. Projektet kan byggas lokalt eller via GitHub Actions och GitHub Releases.

Utvecklingsplanen är vägledande, inte mekanisk. GPT Byggaren kan lägga in korrigeringssteg, hoppa över onödiga steg eller omplanera när projektets faktiska tillstånd motiverar det.

## Distributionsmodell

GPT Byggaren bygger peer runtimes från samma canonical behavior-, capability-, artifact-, workspace/state- och tool-kontrakt.

Registrerade mål är:

- **ChatGPT Chat / Chat ZIP** – portabel ChatGPT-runtime.
- **Custom GPT** – paket för ChatGPT Builder med plattformens instruktion- och Knowledge-begränsningar.
- **Claude Projects** – portabel Project Instructions + Knowledge-distribution för Claude Projects.
- **OpenCode** – agentisk workspace-runtime med `AGENTS.md`, Skills och explicita custom tools.
- **OpenAI Plugin** – skills-first runtime med `plugin.json`, `SKILL.md`, references, assets och runtime-relevanta scripts.

Vilka av dessa som aktiveras bestäms av användningsfallet. Ingen runtime är automatiskt primär och Chat ZIP + Custom GPT är inte ett obligatoriskt standardpar.

Utöver runtime-distributionerna finns **projekt-ZIP:en**, som innehåller hela utvecklingsprojektet och används för fortsatt utveckling, Git och återupptagning.

## Kom igång som användare

Det enklaste sättet är att använda en byggd release av GPT Byggaren. Välj den runtime som passar arbetssättet; de bygger på samma canonical beteende men installeras olika.

### ChatGPT Chat / Chat ZIP

1. Hämta Chat ZIP-distributionen från GitHub Releases.
2. Bifoga ZIP-filen i en ny ChatGPT-konversation.
3. Be ChatGPT använda ZIP-filen som GPT Byggaren-kontext.
4. Beskriv GPT:n du vill skapa.

### Custom GPT

Custom GPT-distributionen innehåller material för ChatGPT Builder: kompilerade instruktioner, conversation starters, capabilities och Knowledge-paket.

### Claude Projects

Claude-distributionen innehåller Project Instructions, Knowledge-material och runtime-contract för att sätta upp GPT Byggaren som ett Claude Project.

### OpenCode

OpenCode-distributionen är ett agentiskt workspace med `AGENTS.md`, projektlokala Skills och explicita custom tools. Den passar särskilt när GPT Byggaren ska arbeta stegvis mot ett persistent projekt/workspace.

### OpenAI Plugin

Plugin-distributionen är en portabel skills-first runtime. Den innehåller `plugin.json`, en eller flera skills under `skills/`, relevanta references/assets/scripts samt runtime-kontrakt och manifest.

Byggd artefakt heter normalt:

`<project-id>-plugin-<version>.zip`

Plugin v1 genererar inte MCP-servrar, UI-komponenter eller hooks. Om ett projekt kräver persistent workspace/state eller körbara lokala tools måste host-runtimen bära den funktionen, annars ska Plugin bedömas som reducerad.

Oavsett runtime ska nyprojektsanalysen bedöma **alla registrerade peer runtimes** för GPT:n som byggs. Den ska inte automatiskt begränsa det nya projektet till samma runtime som GPT Byggaren själv råkar köras i.

Mer detaljerad användarguide finns i [`docs/getting-started.md`](docs/getting-started.md).

## Återuppta ett tidigare GPT-projekt

GPT-projekt som skapats av GPT Byggaren är självbärande. Bifoga den senaste projekt-ZIP:en i en ny konversation och be GPT Byggaren fortsätta projektet.

Den läser normalt projektet i följande ordning:

1. `gpt-project.yaml`
2. `project-status.yaml`
3. `docs/development-plan.md`
4. `STATUS.md`
5. `PROJECT.md`

Maskinläsbar status är auktoritativ när den skiljer sig från äldre löptext eller historiska dokument.

## Bygga projektet lokalt

Projektet kräver Python 3 samt de beroenden som används av CI, främst `pyyaml`, `jsonschema` och `pytest`.

Kör tester:

```bash
python -m pytest -q -p no:cacheprovider
```

Kör linter:

```bash
python scripts/lint_gpt_project.py --project-root .
```

Bygg och validera alla direktleveransartefakter utan GitHub:

```bash
python scripts/build_direct.py --project-root . --version 0.0.0-dev
```

Eller bygg distributionsmålen separat:

```bash
python scripts/build_distributions.py \
  --project-root . \
  --version 0.0.0-dev

python scripts/validate_distributions.py --project-root .
```

Genererade filer hamnar i `build/` och `dist/` och ska inte checkas in.

## GitHub Actions och release

CI körs vid push, pull request och manuell körning. Den validerar bland annat:

- YAML och JSON,
- project hygiene,
- GPT-lint,
- instruction-adherence-kontrakt,
- tester,
- distributionsbygge,
- distributionsvalidering,
- förväntade releaseartefakter.

När en GitHub Release publiceras härleds distributionsversionen från release-taggen, exempelvis:

```text
v1.2.0 → 1.2.0
```

Releaseflödet bygger och publicerar normalt:

- projekt-ZIP,
- samtliga aktiverade runtime-distributioner enligt target-registret,
- `SHA256SUMS.txt`,
- `DELIVERY-MANIFEST.json`.

## Projektstruktur

De viktigaste delarna är:

```text
src/instructions/        canonical GPT-instruktion
src/runtime-policy/      återanvändbara runtimepolicies
knowledge/               canonical Knowledge
profiles/                referensprofiler för olika projekttyper
schemas/                 maskinläsbara kontrakt
scripts/                 build-, lint-, status- och valideringsverktyg
tests/                   deterministiska tester
evals/                   beteende- och regressionsscenarier
templates/               genererade runtime- och rapportmallar
docs/                    design- och användardokumentation
.github/workflows/        CI och releaseautomation
```

Centrala kontrakt och statusfiler:

- `gpt-project.yaml` – maskinläsbart projekt- och runtimekontrakt.
- `project-status.yaml` – auktoritativ projektstatus och progression.
- `PROJECT.md` – projektets syfte och styrande principer.
- `STATUS.md` – mänskligt läsbar nulägesbild.
- `architecture.yaml` – översikt över den interna arkitekturen.

## Dokumentation

För att hålla README:n användbar ligger detaljerna i separata dokument.

### Börja här

- [`docs/getting-started.md`](docs/getting-started.md) – från idé till färdig GPT.
- [`docs/beginner-faq.md`](docs/beginner-faq.md) – vanliga frågor.
- [`PROJECT.md`](PROJECT.md) – produktens syfte och styrande principer.
- [`STATUS.md`](STATUS.md) – aktuell projektstatus.

### Arkitektur och projektmodell

- [`docs/product-vision.md`](docs/product-vision.md)
- [`docs/canonical-project-structure.md`](docs/canonical-project-structure.md)
- [`docs/gpt-project-contract.md`](docs/gpt-project-contract.md)
- [`docs/project-status-model.md`](docs/project-status-model.md)
- [`docs/analysis-model.md`](docs/analysis-model.md)
- [`docs/dynamic-planning.md`](docs/dynamic-planning.md)
- [`docs/instruction-architecture.md`](docs/instruction-architecture.md)
- [`docs/knowledge-architecture.md`](docs/knowledge-architecture.md)
- [`docs/reference-profiles.md`](docs/reference-profiles.md)

### Runtime, build och release

- [`docs/chat-zip-runtime.md`](docs/chat-zip-runtime.md)
- [`docs/custom-gpt-compilation.md`](docs/custom-gpt-compilation.md)
- [`docs/claude-portable-runtime.md`](docs/claude-portable-runtime.md)
- [`docs/opencode-runtime.md`](docs/opencode-runtime.md)
- [`docs/plugin-runtime.md`](docs/plugin-runtime.md)
- [`docs/runtime-parity.md`](docs/runtime-parity.md)
- [`docs/platform-validation.md`](docs/platform-validation.md)
- [`docs/build-system.md`](docs/build-system.md)
- [`docs/direct-build.md`](docs/direct-build.md)
- [`docs/ci-flow.md`](docs/ci-flow.md)
- [`docs/github-release-flow.md`](docs/github-release-flow.md)
- [`docs/release-readiness.md`](docs/release-readiness.md)

### Kvalitet och underhåll

- [`docs/test-model.md`](docs/test-model.md)
- [`docs/instruction-adherence-testing.md`](docs/instruction-adherence-testing.md)
- [`docs/model-compatibility.md`](docs/model-compatibility.md) – robust exekvering även med enklare LLM-modeller.
- [`docs/gpt-linter.md`](docs/gpt-linter.md)
- [`docs/project-hygiene.md`](docs/project-hygiene.md)
- [`docs/final-project-hygiene.md`](docs/final-project-hygiene.md)
- [`docs/next-step-recommendation.md`](docs/next-step-recommendation.md)
- [`docs/resume-flow.md`](docs/resume-flow.md)

Dokument som `development-plan.md`, release-candidate-dokumenten, arkitekturrevisionen och maintenance-fixar beskriver projektets utvecklings- och releasehistorik. De är kvar för spårbarhet men ska inte tolkas som aktuell runtimepolicy om de skiljer sig från `gpt-project.yaml`, `project-status.yaml` eller canonical instruktioner.

## Aktuell status

Utvecklingsplanens steg 1–30 är genomförda och version **v1.0.0** är den första stabila releasen. Projektet är i **maintenance mode**.

Aktuell maskinläsbar status finns i [`project-status.yaml`](project-status.yaml).
