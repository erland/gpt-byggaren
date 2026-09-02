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
8. När projektet är redo byggs distributionsartefakter för Chat ZIP och Custom GPT.
9. Projektet kan byggas lokalt eller via GitHub Actions och GitHub Releases.

Utvecklingsplanen är vägledande, inte mekanisk. GPT Byggaren kan lägga in korrigeringssteg, hoppa över onödiga steg eller omplanera när projektets faktiska tillstånd motiverar det.

## Distributionsmodell

GPT Byggaren bygger normalt två jämbördiga distributionsmål från samma canonical beteende- och capability-kontrakt:

- **Chat ZIP** – en portabel runtime som kan bifogas i en ChatGPT-konversation och användas som GPT-kontext. Den kan bära rikare runtime-material när det behövs.
- **Custom GPT** – ett paket för att skapa eller uppdatera en Custom GPT inom plattformens instruktion- och Knowledge-begränsningar.

Ingen av distributionerna är automatiskt primär. Om plattformsbegränsningar gör att de inte kan vara funktionellt identiska dokumenteras skillnaderna i runtime-paritets- och kompatibilitetsrapporter.

Utöver runtime-distributionerna finns **projekt-ZIP:en**, som innehåller hela utvecklingsprojektet och används för fortsatt utveckling, Git och återupptagning i nya konversationer.

## Kom igång som användare

Det enklaste sättet är att använda en byggd release av GPT Byggaren.

### Alternativ 1 – Chat ZIP

1. Hämta den senaste Chat ZIP-distributionen från GitHub Releases.
2. Bifoga ZIP-filen i en ny ChatGPT-konversation.
3. Be ChatGPT använda ZIP-filen som GPT Byggaren-kontext.
4. Beskriv GPT:n du vill skapa, till exempel:

```text
Jag vill bygga en GPT som hjälper mig analysera remisser och bedöma hur de påverkar min organisation.
```

Därefter kan du normalt fortsätta med enkla instruktioner som:

```text
Gör nästa steg och ge mig en uppdaterad zip.
```

### Alternativ 2 – Custom GPT

Custom GPT-distributionen innehåller det material som behövs för att konfigurera GPT Byggaren i ChatGPT Builder, inklusive kompilerade instruktioner, conversation starters, capabilities och Knowledge-paket.

Se paketets README och kompatibilitetsrapport för exakt innehåll och eventuella plattformsbegränsningar.

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
  --version 0.0.0-dev \
  --targets project,chat,custom-gpt

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
- versionsmärkt Chat ZIP,
- versionsmärkt Custom GPT ZIP,
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
- [`docs/gpt-linter.md`](docs/gpt-linter.md)
- [`docs/project-hygiene.md`](docs/project-hygiene.md)
- [`docs/final-project-hygiene.md`](docs/final-project-hygiene.md)
- [`docs/next-step-recommendation.md`](docs/next-step-recommendation.md)
- [`docs/resume-flow.md`](docs/resume-flow.md)

Dokument som `development-plan.md`, release-candidate-dokumenten, arkitekturrevisionen och maintenance-fixar beskriver projektets utvecklings- och releasehistorik. De är kvar för spårbarhet men ska inte tolkas som aktuell runtimepolicy om de skiljer sig från `gpt-project.yaml`, `project-status.yaml` eller canonical instruktioner.

## Aktuell status

Utvecklingsplanens steg 1–30 är genomförda och version **v1.0.0** är den första stabila releasen. Projektet är i **maintenance mode**.

Aktuell maskinläsbar status finns i [`project-status.yaml`](project-status.yaml).
