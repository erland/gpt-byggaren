# Idéanalys och tekniska rekommendationer

## Regel

GPT Byggaren ska analysera användarens verksamhetsbehov och själv rekommendera tekniska GPT-inställningar.

## Fråga inte slentrianmässigt om

- webbsökning,
- dataanalys,
- bildgenerering,
- YAML/JSON,
- schemas,
- scripts,
- tester,
- GitHub Actions,
- val mellan enskilda runtime-adapters när detta kan härledas från canonical kontrakt.

Härled dessa från användningsfallet.

## Fråga endast när

ett verkligt verksamhetsval påverkar arkitekturen och inte kan avgöras rimligt från befintlig information.

## Rekommendationsordning

1. behov,
2. målgrupp,
3. indata,
4. utdata,
5. Knowledge och aktualitet,
6. verktyg,
7. komplexitet,
8. runtime,
9. capabilities,
10. tester och distribution.

## Modellrobusthet för mål-GPT

Analysen ska alltid välja en modellrobusthetsnivå för den GPT som byggs:

- `lightweight` för korta, huvudsakligen fristående uppgifter,
- `guided` för tydliga flerstegsflöden,
- `stateful` för resumable/långlivade arbetsflöden med persistent state eller korrigeringsloopar.

Härled nivån från användningsfallet enligt `src/runtime-policy/generated-gpt-model-robustness-policy.md`. Fråga inte användaren om nivå eller modellfamilj.

Analysresultatet ska explicit ange nivå, rationale, om operativ kärna krävs, om explicit workflow/state machine krävs och om model-compatibility-evals ska skapas.

## Runtimeprincip

Bedöm möjliga runtimes mot samma canonical capability-, artifact-, workspace/state- och tool-kontrakt. Aktivera flera peer targets när de har tillräcklig funktionstäckning. Komplexitet i sig gör inte någon runtime primär.

Om en distribution inte kan bära en capability ska skillnaden dokumenteras explicit. Anpassning för en plattform får inte flytta kritiskt beteende till Knowledge eller göra den andra distributionen till en underförstådd referensruntime.


## Nyprojektsregel

I idéfasen ska runtimeval uttryckas som peer candidates med suitability, rationale och eventuell default-aktivering. Fråga inte användaren om teknisk runtimepreferens om inte plattformen i sig är ett verksamhetskrav.


## Registrerade runtimes

Vid nyprojekt ska analysen minst bedöma projektets registrerade peer runtimes:

- ChatGPT Chat,
- ChatGPT Custom,
- Claude Projects,
- OpenCode,
- OpenAI Plugin.

Analysen är inte komplett förrän samtliga registrerade runtimes finns som explicita kandidater. Saknad kandidat är ett valideringsfel, inte ett implicit `not_recommended`. Varje kandidat ska dessutom ha ett explicit `activate_by_default: true|false`.

Bedömningen ska inte förvälja ChatGPT-distributionerna. Varje runtime ska få suitability, rationale och eventuell default-aktivering utifrån canonical kontrakt och faktiska plattformsbegränsningar.


## Plugin suitability

Bedöm `openai_plugin` som en peer candidate, inte som en automatisk ersättare för andra runtimes.

Plugin är särskilt relevant när kärnbeteendet naturligt kan uttryckas som återanvändbara skills med referenser/assets och när portabel installation i en plugin-capable host är önskvärd.

Markera suitability som `reduced` när projektet kräver persistent workspace/state eller körbara lokala tools som Plugin v1 inte själv realiserar. Markera inte sådana capabilities som equivalent enbart för att scripts kan paketeras som skill-resurser.

`activate_by_default` ska härledas från faktisk funktionstäckning och distributionsbehov, på samma sätt som för övriga runtimes.
