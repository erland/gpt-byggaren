# PROJECT – GPT Byggaren

## Syfte

Skapa en GPT som kan stödja hela livscykeln för utveckling av andra GPT:er.

## Primära mål

- behovsdriven design,
- ZIP-first för avancerade GPT:er,
- Custom GPT som separat distributionsmål,
- stegvis projektutveckling,
- komplett projekt-ZIP efter varje steg,
- automatisk project hygiene,
- direktbyggda distributioner utan GitHub,
- GitHub-redo releaseautomation,
- versionsnummer från GitHub Release-taggen,
- självbärande projekt som kan återupptas i ny konversation.

## Styrande principer

1. Fråga om verksamhetsbehov, inte implementation, när implementationen kan härledas.
2. Projekt-ZIP är den löpande arbetsprodukten.
3. Git är historiken; HEAD ska hållas rent.
4. Distributionsfiler ska genereras från canonical sources.
5. ZIP-runtime får vara rikare än Custom GPT.
6. GitHub ska vara valfritt.
7. Projektstatus och utvecklingsplan ska följa med projektet.
8. Nästa steg rekommenderas utifrån faktisk status, inte bara stegnummer.


## Beslut efter steg 2

- Canonical GPT-källor ska ligga under `src/`.
- `src/instructions/` är primär källa för GPT-instruktioner.
- `src/conversation-starters/` är primär källa för conversation starters.
- `src/runtime-policy/` används för runtime-regler vid behov.
- `knowledge/`, `templates/`, `schemas/`, `scripts/`, `tests/` och `evals/` är villkorade efter projektets behov.
- Genererade buildresultat ska senare ligga i `build/`.
- Färdiga distributionsartefakter ska senare ligga i `dist/`.
- Utvecklingsmaterial ska inte blandas ihop med runtime.
- Tomma eller historiska kataloger ska inte behållas enbart för framtida möjlighet.


## Beslut efter steg 3

- `gpt-project.yaml` är projektets maskinläsbara kontrakt.
- Toolchain-regler ska i möjligaste mån läsas från projektkontraktet.
- Chat ZIP är deklarerad som primär runtime.
- Custom GPT är deklarerad som sekundär och får reduceras eller transformeras.
- GitHub är valfritt.
- GitHub Release-taggen är versionskälla när GitHub används.
- Direktbyggda distributionsartefakter utan GitHub är ett krav.
- Project hygiene är obligatoriskt.
- Projekt-ZIP ska byggas om efter varje genomfört steg.


## Beslut efter steg 4

- `project-status.yaml` är maskinläsbar sanningskälla för projektprogression.
- `STATUS.md` är mänskligt läsbar sammanfattning och ska hållas synkroniserad.
- Projektet ska kunna återupptas från `gpt-project.yaml`, `project-status.yaml` och utvecklingsplanen.
- Planen är styrande men inte mekanisk.
- Extra korrigerings- eller hygiene-steg får skjutas in utan att ursprungsplanen skrivs om.
- Blockerande problem ska dokumenteras strukturerat.
- Nästa steg ska rekommenderas från faktisk projektstatus.


## Beslut efter steg 5

- GPT Byggaren ska analysera verksamhetsbehov före tekniska lösningar.
- Tekniska capabilities ska normalt härledas, inte frågas fram.
- Fyra projektprofiler används som vägledning: enkel, standard, ZIP-first avancerad och workflow/research-heavy.
- Runtime ska rekommenderas från faktisk komplexitet och funktionella behov.
- Chat ZIP ska prioriteras när Custom GPT-begränsningar annars skulle försämra lösningen.
- Custom GPT får vara likvärdig, sekundär eller avrådas från.
- Frågor till användaren ska reserveras för verkliga verksamhetsval.
- Rekommendationer ska motiveras.


## Beslut efter steg 6

- Utvecklingsplaner ska genereras dynamiskt från analysresultatet.
- Projektprofil styr vilka steg som behövs men fungerar inte som en låst mall.
- Varje plansteg ska ha mål, leveranser, validering och klart-kriterier.
- Plansteg ska ordnas efter beroenden.
- Villkorade tekniksteg ska bara inkluderas när de behövs.
- Planen får revideras under arbetets gång.
- Korrigeringssteg får skjutas in utan att ursprungsplanen skrivs om.
- Planen ska levereras som nedladdningsbar Markdown före projektstart.
- Planen ska följa med projekt-ZIP:en från första genomförandesteget.


## Beslut efter steg 7

- Alla relevanta filer ska kunna klassificeras som CANONICAL, RUNTIME, DEVELOPMENT, GENERATED, TEMPORARY eller HISTORICAL.
- Git är historikkällan; gamla filkopior ska normalt inte ligga kvar i HEAD.
- Project hygiene ska köras efter varje steg och fördjupas vid checkpoints.
- Automatisk radering får ske endast med hög säkerhet.
- Osäkra fynd ska flaggas för granskning.
- Final hygiene är en release gate.
- Distributioner ska hygiene-valideras separat från källprojektet.
- `.gitignore` ska exkludera caches, temporära filer och genererade distributionsresultat.


## Beslut efter steg 8

- `src/instructions/system.md` är canonical huvudinstruktion.
- Runtime policies hålls separata under `src/runtime-policy/`.
- Distributionsspecifika instruktioner ska genereras.
- Chat ZIP får använda full instruktion och rikare policies.
- Custom GPT får använda komprimerad eller kompilerad instruktion.
- Custom GPT:s instruktionsbudget får inte begränsa canonical ZIP-runtime.
- Samma beteenderegel ska inte underhållas manuellt på flera ställen.
- Instruktion beskriver beteende; Knowledge beskriver i första hand referensmaterial.


## Beslut efter steg 9

- `knowledge/` är canonical root för referensmaterial.
- Beteenderegler ska ligga i instruktion eller runtime policy, inte flyttas till Knowledge för att kringgå instruktionsbudget.
- Chat ZIP får bära full canonical Knowledge.
- Custom GPT Knowledge är ett separat kompileringsmål.
- Custom GPT får använda identisk, konsoliderad, prioriterad eller hybrid Knowledge-strategi.
- Custom GPT:s filgräns är konfigurerbar via projektkontraktet.
- Reducerad Knowledge och funktionell skillnad ska dokumenteras.
- Tomma Knowledge-understrukturer ska inte skapas innan de behövs.


## Beslut efter steg 10

- Chat ZIP är full primär runtime för avancerade GPT:er.
- `START-HERE.md`, `VERSION` och `MANIFEST.json` är centrala runtimeartefakter.
- Runtimeinnehåll ska väljas deklarativt från `gpt-project.yaml`.
- Utvecklingsplan och projektstatus ska normalt inte följa med Chat ZIP.
- Tomma runtimekataloger ska inte skapas.
- Chat ZIP ska hygiene-valideras separat.
- Samma runtime-buildprincip ska kunna användas både direkt och i GitHub Actions.
- Builden ska vara deterministisk och manifest/checksummor ska skapas.


## Beslut efter steg 11

- Custom GPT är ett separat kompileringsmål från samma canonical sources.
- Instruktion stöder `identical`, `compressed` och `compiled`.
- Knowledge stöder `identical`, `consolidate`, `prioritize` och `hybrid`.
- Builder-underlag ska genereras under `builder/`.
- Capabilities ska härledas från analysmodellen.
- `COMPATIBILITY.md` är obligatorisk när funktionaliteten reduceras.
- Paritet ska bedömas per capability.
- Build ska blockeras vid överskridna plattformsgränser eller missvisande kärnfunktion.
- Chat ZIP förblir primär runtime när Custom GPT behöver reduceras.


## Beslut efter steg 12

- Den byggda Custom GPT-distributionen ska valideras, inte bara källprojektet.
- Plattformsgränser ska läsas från `gpt-project.yaml`.
- Instruktion, Knowledge, conversation starters, capabilities, Builder-paket och kompatibilitet ska valideras.
- `pass`, `warning` och `blocked` används som valideringsnivåer.
- `blocked` stoppar release.
- Reducerad funktion får ge `warning` om den är dokumenterad.
- Samma valideringsregler ska användas lokalt, i CI och i GitHub Release.


## Beslut efter steg 13

- Paritet ska mätas per funktionell capability, inte per fil.
- Chat ZIP är referensruntime för ZIP-first projekt.
- Capability-status är equivalent, reduced, missing eller not_applicable.
- Capabilities klassificeras som critical, important eller optional.
- Sammanfattad paritetsnivå är full, high, moderate, low eller not_viable.
- Viktad paritetspoäng får användas som översikt men ersätter inte capability-matrisen.
- `not_viable` ska normalt stoppa Custom GPT-publicering.
- Paritetsrapport ska kunna levereras som separat releaseartefakt.


## Beslut efter steg 14

- En gemensam Python-toolchain bygger projekt-ZIP, Chat ZIP och Custom GPT ZIP.
- Samma buildkärna ska senare användas av GitHub Actions.
- ZIP-filer ska byggas deterministiskt.
- Manifest och SHA-256-checksummor skapas.
- Projekt-ZIP exkluderar genererade build/dist-resultat och caches.
- Distributionsvalidering sker mot byggda artefakter.
- Instruktionskomprimering och avancerad Knowledge-konsolidering är medvetet senare steg.


## Beslut efter steg 15

- GitHub är inte ett krav för att bygga eller leverera GPT-artefakter.
- `scripts/build_direct.py` är wrapper för direktleverans.
- Lokal standardversion är `0.0.0-dev` om ingen releaseversion anges.
- Direktleverans ska skapa projekt-ZIP, Chat ZIP, Custom GPT ZIP när aktiverad, checksummor och leveransmanifest.
- Samma kärnbuild ska senare användas av GitHub Actions.
- Validering ska passera innan artefakterna betraktas som leveransbara.


## Beslut efter steg 16

- Publicerad GitHub Release triggar distributionsbygget.
- GitHub Release-taggen är enda versionskälla för releaseartefakterna.
- Samma build- och valideringsscript används lokalt och i GitHub Actions.
- Tester och distributionsvalidering körs före uppladdning.
- Ingen manuell versionsuppdatering ska behövas inför release.

## Beslut efter steg 17

- CI körs på push och pull requests före release.
- Samma build- och valideringsscript används lokalt, i CI och i release.
- CI använder utvecklingsversionen `0.0.0-ci`.
- YAML/JSON-parse, tester, build, distributionsvalidering och hygiene ingår.
- CI-artefakter laddas upp för inspektion.


## Beslut efter steg 18

- Deterministiska tester och beteendeevalueringar är separata testlager.
- Projektprofil styr hur djup testningen ska vara.
- Reproducerbara buggar ska om möjligt bli regressionsfall.
- Critical tester och evals blockerar release.
- `test-manifest.yaml` är maskinläsbar testkonfiguration.
- `tests/` och `evals/` är development-material och ska normalt inte följa med runtime.

## Beslut efter steg 19

- Statisk lint körs före tester och build.
- Errors blockerar CI; warnings blockerar normalt inte.
- Linter använder explicita konfigurationsfält för pathdetektion för att undvika falska positiva substring-matchningar.
- Linter kontrollerar projektkontrakt, instruktion, Knowledge, testing, GitHub-flöden och hygiene.
- JSON-output stöds.

## Beslut efter steg 20

- Nästa steg härleds från faktisk projektstatus, inte `current_step + 1`.
- Blockerare, failed validation och hygiene prioriteras före planordning.
- Korrigeringssteg får införas dynamiskt.
- Planned steps får skip/split/merge med dokumenterad motivering.
- `pause` används endast när ett verkligt verksamhetsbeslut saknas.

## Beslut efter steg 21

- Projekt-ZIP ska kunna återupptas utan tidigare chathistorik.
- `project-status.yaml` är primär statuskälla.
- Resume följer definierad läsordning och verifierar projektet före fortsatt arbete.
- Projekt utan `gpt-project.yaml` klassificeras som legacy/unknown.

## Beslut efter steg 22

- Checkpoint hygiene körs löpande och final hygiene inför release.
- Kända genererade/cachade artefakter får auto-rensas säkert.
- Historiskt namngivna filer flaggas men raderas inte blint.
- Final hygiene är en release gate.
- CI kör checkpoint hygiene och release-workflow kör final hygiene.

## Beslut efter steg 23

- Release readiness är en sammanvägd gate.
- Resultaten är `ready`, `ready_with_warnings` och `blocked`.
- Project ZIP, Chat ZIP och Custom GPT bedöms separat.
- Blockerande kvalitetsresultat stoppar release.
- Samma assessment används lokalt och i GitHub Release.

## Beslut efter steg 24

- Nybörjare ska kunna använda GPT Byggaren genom att beskriva verksamhetsbehovet.
- Tekniska val ska härledas när de går att avgöra från användningsfallet.
- Projekt-ZIP förklaras som den artefakt användaren främst behöver spara för fortsatt utveckling.
- Skillnaden mellan Project ZIP, Chat ZIP och Custom GPT ska vara begriplig utan arkitekturkunskap.
- GitHub beskrivs som valfritt.

## Beslut efter steg 25

- Fyra referensprofiler används som arkitekturella startpunkter.
- Profilval ska härledas från användningsfallet, inte normalt väljas av användaren.
- Profiler anger standarder för runtime, Knowledge, scripts, schemas, templates, tester, evals och CI.
- Projektspecifika avvikelser från profil är tillåtna och ska dokumenteras.

## Beslut efter steg 26

- Läroboksskaparen används som standardreferens.
- Tullverket Remiss används som workflow/research-heavy referens.
- ArchiMate Modeller används som ZIP-first advanced referens.
- Referensfallen är blockerande regressionstest för profilval.

## Beslut efter steg 27

- Ett deterministiskt E2E-scenario används för att testa hela projekt- och distributionskedjan från blank idé.
- LLM-kvaliteten i fri text separeras från den deterministiska kontrakts-/buildkedjan.
- Blank-idea-scenariot måste skapa profil, plan, projektkontrakt, status, canonical instruktion och tre distributionsartefakter.
- E2E-testet är blockerande regressionstest.

## Beslut efter steg 28

- Gemensam exekverbar projektmodell ligger i `scripts/lib/project_model.py`.
- Profilval får inte dupliceras mellan CLI-scripts eller tester.
- CLI-scripts ska vara tunna wrappers runt canonical logik.
- `docs/`, `src/runtime-policy/`, `schemas/` och `scripts/lib/` har tydligt separerade roller.
- Buildsystemet behålls separat eftersom dess ansvar är distinkt.
- Projektet bedöms arkitekturellt redo för release candidate.

## Beslut efter steg 29

- Release candidate-versionen är `1.0.0-rc.1`.
- RC är en pre-release och inte stabil v1.0.0.
- RC måste passera projektkontrakt, referensregressioner, E2E, compile, hygiene och Custom GPT-plattformsgränser.
- Godkänd RC leder till steg 30: stabil release.

## Beslut efter steg 30

- Stabil release är `v1.0.0`.
- Utvecklingsplan steg 1–30 är slutförd.
- Projektet går över i maintenance mode.
- GitHub Release-tag är fortsatt source of truth för versionsnummer i GitHub-releaseflödet.
- RC-information behålls som dokumenterad releasehistorik, men aktuell lifecycle state är stable.
