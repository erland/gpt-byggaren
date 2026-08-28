# Instruktionarkitektur – GPT Byggaren

## Syfte

GPT Byggaren ska kunna skapa GPT-projekt där instruktioner är:

- tydligt strukturerade,
- möjliga att underhålla över tid,
- separerade från Knowledge,
- möjliga att kompilera till flera runtimes,
- fria från onödig duplicering.

Grundprincip:

> Canonical instruktion ska vara sanningskällan. Distributionsspecifika instruktioner ska genereras eller härledas.

## Tre nivåer

### 1. Canonical huvudinstruktion

Placering:

```text
src/instructions/system.md
```

Innehåller GPT:ns kärnbeteende:

- identitet,
- syfte,
- scope,
- arbetsflöde,
- beslutsregler,
- verktygsregler,
- outputregler,
- kvalitetsregler,
- regler för osäkerhet och källor.

### 2. Runtime policies

Placering:

```text
src/runtime-policy/
```

Används för regler som:

- är större eller mer specialiserade än vad som lämpar sig i huvudinstruktionen,
- endast behövs i viss runtime,
- bör kunna återanvändas av scripts eller validering,
- behöver vara separata för tydlighet.

Exempel:

- analys-policy,
- planerings-policy,
- hygiene-policy,
- routing-policy,
- export-policy.

### 3. Distributionsspecifika instruktioner

Ska vara genererade.

Exempel:

```text
build/chat/instructions.md
build/custom-gpt/instructions.md
```

Dessa ska inte underhållas manuellt som separata canonical sources.

## Canonical instruktionens struktur

Rekommenderade sektioner:

1. Identitet
2. Syfte
3. Scope
4. Primära användarflöden
5. Beslutsprinciper
6. Verktygsregler
7. Filhantering
8. Outputregler
9. Käll- och evidensregler
10. Kvalitetskontroll
11. Project hygiene
12. Återupptagning och status
13. Begränsningar

Alla GPT:er behöver inte alla sektioner.

## Vad som inte ska ligga i huvudinstruktionen

Undvik att lägga:

- lång referenskunskap,
- historik,
- stora tabeller,
- omfattande domänmaterial,
- genererade listor,
- distributionsspecifika filinventeringar,

i huvudinstruktionen om de bättre hör hemma i Knowledge eller runtimefiler.

## ZIP-runtime

Chat ZIP får använda:

- full canonical instruktion,
- runtime policies,
- rikare stödmaterial,
- scripts och schemas.

ZIP-runtime ska inte begränsas för att Custom GPT har ett mindre instruktionsutrymme.

## Custom GPT

Custom GPT får använda en transformerad instruktion.

Kompileringen får:

- korta ned formuleringar,
- slå ihop sektioner,
- flytta referensmaterial till Knowledge,
- hänvisa till konsoliderade Knowledge-filer,
- ta bort ZIP-specifika regler som inte gäller i Custom GPT.

Kompileringen får inte:

- ändra kärnsyftet,
- ändra säkerhets- eller kvalitetsregler,
- skapa motsägande beteende,
- dölja viktiga funktionella skillnader.

## Instruktionskompilering

Föreslagen pipeline:

```text
src/instructions/system.md
        +
src/runtime-policy/*.md
        ↓
instruction compiler
        ↓
├── build/chat/instructions.md
└── build/custom-gpt/instructions.md
```

## Regler för duplicering

Samma regel ska inte underhållas manuellt på flera ställen.

Om en regel behöver finnas i flera distributioner:

- håll den canonical,
- generera distributionsversionerna.

## Instruktionsbudget

Custom GPT:s instruktionsbudget ska behandlas som en konfigurerbar plattformsbegränsning.

Kompilatorn ska kunna rapportera:

```text
Canonical instruction: 12 480 characters
Chat ZIP: 12 480 characters
Custom GPT: 7 612 / 8 000 characters
```

## Prioritering vid komprimering

När Custom GPT-instruktionen måste kortas:

1. behåll identitet och kärnsyfte,
2. behåll arbetsflöde,
3. behåll beslutsregler,
4. behåll kvalitets- och säkerhetsregler,
5. behåll verktygsregler som är relevanta i Custom GPT,
6. korta exempel,
7. flytta referensmaterial till Knowledge,
8. ta bort ZIP-specifika instruktioner.

## Instruktion vs Knowledge

Instruktion beskriver främst:

- hur GPT:n ska bete sig,
- vilka regler den ska följa,
- hur arbetsflödet ser ut.

Knowledge beskriver främst:

- fakta,
- referensmaterial,
- modeller,
- mallinnehåll,
- domäninformation.

## Validering

Instruktionsarkitekturen ska validera:

- canonical huvudinstruktion finns,
- inga motsägande policies,
- inga tydliga dupliceringar,
- Custom GPT-instruktion håller sig inom konfigurerad budget,
- distributionsinstruktioner går att härleda från canonical source.

## Metadata

Instruktionskällor ska kunna beskrivas maskinläsbart.

Exempel:

```yaml
instructions:
  canonical: src/instructions/system.md
  policies:
    include:
      - src/runtime-policy/*.md
  compilation:
    chat:
      mode: full
    custom_gpt:
      mode: compressed
```

## Regel för GPT Byggaren

När GPT Byggaren skapar en ny GPT ska den själv rekommendera hur mycket som ska ligga i:

- huvudinstruktion,
- runtime policies,
- Knowledge.

Användaren ska inte behöva designa denna uppdelning manuellt.

## Core behavior contract och enklare modeller

Nya GPT-projekt bör deklarera ett litet maskinläsbart `instructions.core_contract` i `gpt-project.yaml`.

Syftet är inte att skapa modellspecifika instruktioner, utan att kontrollera två modellneutrala robusthetsregler:

1. kritiskt workflow ska finnas direkt i canonical instruktionen och inte bara i Knowledge eller stödpolicies,
2. kärnflödet ska kräva så få obligatoriska filhopp som möjligt, normalt högst ett.

Exempel:

```yaml
instructions:
  canonical: src/instructions/system.md
  core_contract:
    enabled: true
    required_markers:
      - "Choose exactly one recommendation"
      - "Offer the available export formats"
    required_runtime_dependencies: []
    max_required_file_hops: 1
    knowledge_may_not_be_required_for_core_behavior: true
```

`required_markers` ska vara korta invariants, inte en kopia av hela instruktionen. Supporting policies och Knowledge får ge fördjupning men får inte vara enda platsen där ett obligatoriskt kärnbeteende definieras.
