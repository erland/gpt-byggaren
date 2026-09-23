# Modellkompatibilitet och robusthet

## Mål

GPT Byggaren ska använda samma canonical beteende oavsett om host-runtimen använder en stark eller enklare LLM. Projektet ska inte skapa separata instruktioner för enskilda modellfamiljer.

Robusthet uppnås i stället genom explicit workflow-state, små operativa steg, strukturerad status och deterministisk validering.

## Designprincip

Modellen ska främst fatta avgränsade semantiska beslut. Sådant som kan kontrolleras maskinellt ska kontrolleras av schemas, scripts eller tester.

Det innebär att modellen normalt ska arbeta enligt:

1. läs kontrakt och status,
2. välj ett state eller avgränsat mål,
3. läs endast direkt relevant policy,
4. utför ändringen,
5. validera deterministiskt,
6. korrigera fel innan status uppdateras,
7. gå vidare först efter godkänd gate.

## Varför detta hjälper enklare modeller

Mindre modeller är typiskt mer känsliga för långa kedjor av indirekta instruktioner, många samtidiga mål och regler som endast finns som naturligt språk. Den här arkitekturen minskar behovet av att modellen själv håller hela projektets styrmodell i arbetsminnet.

## Modellmatris

Beteendeevaluationer under `evals/model-compatibility/` är modellneutrala. Resultat från faktisk körning dokumenteras separat per modell och version.

Minst följande scenarier ska täckas:

- ny enkel GPT från vag idé,
- komplett runtime-bedömning,
- lång serie av "Gör nästa steg",
- korrigering efter validerings- eller CI-fel,
- återupptagning från projekt-ZIP,
- migrering av äldre projekt när sådan funktion berörs.

Ett misslyckande för en modell ska i första hand analyseras som en signal om att workflow eller validering är för implicit. Lösningen ska normalt förbättra canonical kontrakt i stället för att skapa en modellunik prompt.

## Release gate

Den statiska modellrobusthetsvalidatorn är en obligatorisk CI-kontroll. Där faktisk modell-eval kan köras bör kritiska scenarier ingå i releaseunderlaget, men frånvaro av extern modellkörning får inte hindra deterministiska kontrakttester.
