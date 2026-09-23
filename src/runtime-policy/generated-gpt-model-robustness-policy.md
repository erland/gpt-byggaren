# Modellrobusthet för genererade GPT-projekt

## Syfte

GPT Byggaren ska anpassa nya GPT-projekts instruktioner och styrmodell så att de fungerar stabilt även med enklare LLM-modeller, utan att överbygga enkla användningsfall eller skapa modellspecifika instruktioner.

## Robusthetsnivåer

### lightweight

Använd när GPT:n främst utför enstaka eller korta uppgifter utan lång progression.

Krav:

- deklarera `instructions.core_contract`,
- lägg allt kritiskt kärnbeteende direkt i canonical instruktionen,
- Knowledge får inte vara obligatorisk för kärnflödet,
- håll obligatoriska filhopp till normalt högst ett,
- inkludera instruction-adherence-evals.

Ingen state machine krävs.

### guided

Använd när GPT:n har ett tydligt flerstegsflöde men normalt inte behöver långlivat persistent state.

Krav utöver `lightweight`:

- lägg en kort operativ kärna direkt i canonical instruktionen,
- exekvera ett tydligt avgränsat mål åt gången,
- definiera gates där progression kan valideras,
- inkludera model-compatibility-evals för multi-turn retention, felåterhämtning och terminal behavior.

En full generell state machine är valfri och ska bara införas när den förenklar arbetsflödet.

### stateful

Använd när GPT:n behöver kunna återupptas, arbeta över många steg, hålla strukturerad projekt-/researchstatus eller korrigera arbete efter validerings- eller CI-fel.

Krav utöver `guided`:

- definiera explicit workflow/state machine i projektkontraktet,
- gör strukturerad state till auktoritativ källa,
- definiera exit-kriterier/gates för state-övergångar,
- flytta maskinellt avgörbara regler till deterministiska validators/scripts,
- inkludera model-compatibility-evals för resume, långa sekvenser och återhämtning efter fel.

## Härledning

GPT Byggaren ska själv välja nivå från användningsfallet.

Väg särskilt in:

- antal beroende arbetssteg,
- om arbetet ska återupptas i senare konversation/session,
- om status behöver vara persistent,
- om fel behöver korrigeras innan progression,
- om flera filer/policies annars måste hållas samtidigt i modellens arbetsminne,
- om deterministiska gates kan minska modellens orkestreringsansvar.

Fråga inte användaren vilken robusthetsnivå den vill ha.

## Principer

- Skapa inte Luna-, Sol- eller andra modellunika canonical instruktioner.
- Välj minsta nivå som täcker användningsfallet.
- `lightweight` är inte en sämre nivå; den är rätt val för enkla GPT:er.
- Robusthetsregler ska följa med i det genererade GPT-projektet och dess runtime-distributioner när de är relevanta.
- Runtime-adaptrar får komprimera eller transformera formuleringar men får inte ta bort obligatoriskt kärnbeteende.
