# GPT Byggaren

## Distributionsprincip

GPT Byggaren skapar normalt både **Chat ZIP** och **Custom GPT** från samma canonical beteende- och capability-kontrakt. Ingen av dem är automatiskt primär bara för att GPT:n är avancerad. Faktiska plattformsbegränsningar och capability-skillnader dokumenteras i runtime-paritetsrapporten.

## Projekt

Detta repository innehåller källprojektet för **GPT Byggaren**.

GPT Byggaren ska hjälpa användare att skapa andra GPT:er genom en stegvis, självbärande utvecklingsprocess.

## Aktuell fas

Steg 30 – Stabil release v1.0.0 – är genomfört.

## Centrala projektartefakter

- `docs/development-plan.md` – full utvecklingsplan
- `docs/product-vision.md` – produktvision och målbild
- `docs/user-journeys.md` – centrala användarresor
- `docs/canonical-project-structure.md` – beslutad generell projektstruktur
- `docs/gpt-project-contract.md` – dokumentation av projektkontraktet
- `docs/project-status-model.md` – status-, progression- och återupptagningsmodell
- `docs/analysis-model.md` – behovsdriven analys- och rekommendationsmodell
- `docs/dynamic-planning.md` – dynamisk, projektspecifik utvecklingsplanering
- `docs/project-hygiene.md` – filklassificering och automatisk projektstädning
- `docs/instruction-architecture.md` – canonical instruktioner och runtime-kompilering
- `docs/knowledge-architecture.md` – canonical Knowledge och runtime-kompilering
- `docs/chat-zip-runtime.md` – full primär Chat/ZIP-runtime
- `docs/custom-gpt-compilation.md` – kompilerad Custom GPT-distribution
- `docs/platform-validation.md` – plattformsgränser, Builder-kontroller och release gate
- `docs/runtime-parity.md` – funktionell jämförelse mellan Chat ZIP och Custom GPT
- `docs/build-system.md` – körbar toolchain för projekt-, Chat- och Custom GPT-artefakter
- `docs/direct-build.md` – direktbyggnad och leverans utan GitHub
- `project-status.yaml` – maskinläsbar projektstatus och progression
- `STATUS.md` – mänskligt läsbar projektstatus
- `PROJECT.md` – projektets syfte och styrande principer

## Nästa rekommenderade steg

Utvecklingsplan 1–30 är slutförd. Projektet går över i maintenance mode.

## Arbetsmodell

Projektet ska vidareutvecklas genom att den aktuella projekt-ZIP:en används som input till nästa steg.

Varje genomfört steg ska normalt ge en ny komplett projekt-ZIP.

- `docs/github-release-flow.md` – automatiserad GitHub Release-paketering
- `docs/ci-flow.md` – CI för commits och pull requests
- `docs/test-model.md` – deterministiska tester, evals och regressionsstrategi
- `docs/gpt-linter.md` – statisk projektlint före test och build
- `docs/next-step-recommendation.md` – statusdrivet val av faktiskt nästa steg
- `docs/resume-flow.md` – återupptagning från tidigare projekt-ZIP
- `docs/final-project-hygiene.md` – checkpoint- och slutlig project hygiene
- `docs/release-readiness.md` – sammanvägd releasebedömning
- `docs/getting-started.md` – nybörjarguide från idé till release
- `docs/beginner-faq.md` – vanliga frågor för nya användare
- `docs/reference-profiles.md` – återanvändbara projektprofiler
- `docs/reference-project-validation.md` – kalibrering mot kända GPT-projekt
- `docs/end-to-end-test.md` – hela kedjan från blank idé till distribution
- `docs/architecture-simplification-review.md` – slutlig arkitektur- och konsolideringsrevision

- `docs/release-candidate.md` – release candidate och RC-gates

- `docs/stable-release.md` – stabil v1.0.0-release och maintenance transition


## Custom GPT-budgetering

Custom GPT-builden använder konservativ instruktionskompilering med verifiering av core-contract och semantisk Knowledge-prioritering före filordning. `builder/compilation-report.json` visar hur 8 000-teckens- och 20-filsbudgeterna användes.


## Steg 4 – instruktionsefterlevnad

Projektet har nu ett standardiserat evalpaket för bootstrap, multi-turn retention, terminal behavior och Knowledge-independence. Evalfallen beskriver avsett beteende och modellresultat ska dokumenteras separat från specifikationen.
