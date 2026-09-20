# Dynamisk planeringspolicy

## Regel

GPT Byggaren ska skapa en projektspecifik utvecklingsplan från analysresultatet.

## Gör

- anpassa antal steg efter komplexitet,
- inkludera endast relevanta teknikområden,
- håll varje steg tillräckligt litet för en separat prompt,
- ange mål och klart-kriterier,
- ordna steg efter beroenden,
- lägg in hygiene och validering,
- inkludera distribution och release,
- skapa plansteg för varje runtime som analysresultatet markerat `activate_by_default: true`,
- inkludera runtime parity över samtliga aktiverade runtimes, inte bara Chat ZIP och Custom GPT,
- tillåt korrigeringssteg när projektstatus kräver det.

## Gör inte

- använd samma fasta plan för alla GPT:er,
- fråga användaren hur många tekniska steg planen ska ha,
- skapa schemas/scripts/evals-steg om användningsfallet inte behöver dem,
- behandla planen som oföränderlig,
- anta att Chat ZIP och Custom GPT är de enda distributionsmålen,
- utelämna Claude/OpenCode eller andra registrerade runtimes när analysresultatet har aktiverat dem.

## Leverans

När målbilden är stabil ska planen ges som nedladdningsbar Markdown.

När första genomförandesteget görs ska planen följa med i projekt-ZIP:en som `docs/development-plan.md`.


## Runtime-planering

Utvecklingsplanen ska härledas från analysens `runtime.candidates`.

Innan planen skapas ska analysen valideras mot `schemas/analysis-recommendation.schema.json`. Skapa inte en utvecklingsplan från ett partiellt runtime-resultat.

För varje kandidat med `activate_by_default: true` ska planen innehålla ett konkret runtime-/adaptersteg eller tydligt kombinera flera likvärdiga adapters i samma steg när det är praktiskt.

En kandidat med `suitability: reduced` får aktiveras endast om analysen uttryckligen motiverar det. En kandidat med `not_recommended` ska normalt inte byggas.

Projektets `build_system.targets` ska innehålla varje default-aktiverad runtime. Om en aktiverad runtime saknas från build-targets är planen ogiltig och ska korrigeras före fortsatt genomförande.

Runtime parity och release readiness ska omfatta samtliga aktiverade runtimes.
