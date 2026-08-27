# Knowledge-arkitektur – GPT Byggaren

## Syfte

GPT Byggaren ska kunna skilja tydligt mellan:

- beteenderegler som hör hemma i instruktion,
- referensmaterial som hör hemma i Knowledge,
- strukturerade modeller som behöver maskinläsbar representation,
- runtime-stöd som endast behöver finnas i Chat ZIP,
- reducerad eller konsoliderad Knowledge för Custom GPT.

Grundprincip:

> Instruktion beskriver hur GPT:n ska bete sig. Knowledge beskriver vad GPT:n ska kunna slå upp, förstå eller använda som referens.

## Knowledge-nivåer

### 1. Ingen särskild Knowledge

Lämpligt när:

- all relevant information kommer i prompten,
- webbsökning står för aktuell information,
- GPT:n endast har generella instruktioner.

### 2. Liten statisk Knowledge

Lämpligt för:

- begreppslistor,
- policies,
- korta referensdokument,
- begränsade regelverk.

### 3. Strukturerad Knowledge

Lämpligt när GPT:n behöver:

- YAML/JSON-modeller,
- tabeller,
- taxonomier,
- klassificeringar,
- relationer,
- schemas,
- maskinläsbara kataloger.

### 4. Rik ZIP-runtime

Lämpligt när GPT:n behöver:

- många filer,
- flera kunskapslager,
- scripts,
- schemas,
- mallar,
- datafiler,
- referensmodeller,

som inte praktiskt bör pressas in i Custom GPT.

## Canonical Knowledge

Canonical Knowledge ska ligga under:

```text
knowledge/
```

Den ska vara den källa som underhålls över tid.

Exempel:

```text
knowledge/
├── domain/
├── reference/
├── structured/
└── examples/
```

Alla projekt behöver inte dessa underkataloger.

## Rekommenderade roller

### `domain/`

Domänkunskap som behövs för GPT:ns kärnuppgift.

### `reference/`

Dokumentation, standarder, regler, definitioner och andra referenser.

### `structured/`

Maskinläsbara modeller i exempelvis YAML eller JSON.

### `examples/`

Exempel som verkligen behövs som runtime-referens.

Utvecklingsexempel ska i stället ligga i tester eller evals.

## Knowledge vs runtime policy

Följande ska normalt ligga i runtime policy eller instruktion:

- arbetsflödesregler,
- beslutskriterier,
- regler för hur verktyg används,
- outputkrav,
- quality gates.

Följande passar bättre i Knowledge:

- fakta,
- domänmodeller,
- exempeldata,
- referensstrukturer,
- taxonomier,
- standardtexter.

## Chat ZIP

Chat ZIP får innehålla hela canonical Knowledge om det behövs.

Exempel:

```text
chat/
├── assistant/
├── knowledge/
│   ├── domain/
│   ├── reference/
│   └── structured/
├── schemas/
└── scripts/
```

Det ska inte finnas någon artificiell gräns som hämtas från Custom GPT om Chat ZIP-runtime behöver mer material.

## Custom GPT

Custom GPT Knowledge är ett separat kompileringsmål.

Kompileringen får:

- slå ihop filer,
- skapa bundles,
- välja bort ZIP-specifikt material,
- flytta referensmaterial mellan filer,
- skapa kortare sammanställningar,
- prioritera kärnkunskap.

Kompileringen får inte:

- tappa nödvändig kärnkunskap utan att detta dokumenteras,
- flytta beteenderegler till Knowledge enbart för att kringgå instruktionsgränsen,
- skapa otydlig duplicering mellan instruktion och Knowledge.

## Knowledge-budget

Custom GPT:s Knowledge-gräns ska behandlas som en konfigurerbar plattformsparameter.

Exempel:

```yaml
platform_limits:
  knowledge_max_files: 20
```

Buildsystemet ska kunna rapportera:

```text
Canonical Knowledge files: 43
Chat ZIP Knowledge files: 43
Custom GPT Knowledge files: 18 / 20
```

## Konsolideringsstrategier

### 1. Sammanfogning per ämne

Exempel:

```text
knowledge/reference/legal/*.md
    ↓
custom-gpt/legal-reference.md
```

### 2. Sammanfogning per funktion

Exempel:

```text
analysis rules reference
output reference
domain reference
```

### 3. Maskinläsbar bundle

Flera små YAML-filer kan konsolideras till en större bundle om detta inte försämrar användbarheten.

### 4. Prioriterat urval

Om allt material inte behöver vara tillgängligt i Custom GPT kan kärnmaterial prioriteras.

## Knowledge-manifest

Projektet ska kunna beskriva Knowledge maskinläsbart.

Exempel:

```yaml
knowledge:
  canonical_root: knowledge
  include_in_chat:
    - knowledge/**
  custom_gpt:
    strategy: consolidate
    priority:
      - knowledge/domain/**
      - knowledge/reference/core/**
```

## Metadata per Knowledge-resurs

För avancerade projekt bör resurser kunna beskrivas med:

- id,
- title,
- role,
- source,
- runtime,
- priority,
- format,
- generated/not generated.

Exempel:

```yaml
id: capability-model
title: Förmågemodell
role: structured_reference
source: knowledge/structured/capabilities.yaml
runtime:
  chat: true
  custom_gpt: true
priority: high
```

## Kvalitetsregler

GPT Byggaren ska kontrollera:

- duplicerad Knowledge,
- beteenderegler som felaktigt ligger i Knowledge,
- för små filer som bör konsolideras,
- för stora blandade filer som bör delas,
- döda eller oanvända resurser,
- konflikter mellan Knowledge och instruktion,
- trasiga interna referenser.

## Custom GPT-kompatibilitet

När Custom GPT inte kan bära all Knowledge ska GPT Byggaren beskriva skillnaden.

Exempel:

```text
Chat ZIP:
Full domänmodell och 47 referensfiler.

Custom GPT:
16 konsoliderade Knowledge-filer.

Reducerad funktion:
Djup projektnavigering över historiska modellversioner ingår inte.
```

## Struktur för GPT Byggaren-projektet

GPT Byggaren behöver själv Knowledge främst för:

- plattformsregler,
- referensarkitekturer för GPT-projekt,
- exempel på vanliga GPT-profiler,
- framtida referensprojekt.

Dessa ska införas först när faktiskt innehåll finns.

Tomma underkataloger ska inte skapas i förväg.

## Regel för GPT Byggaren

När en ny GPT designas ska GPT Byggaren själv rekommendera:

- om Knowledge behövs,
- vilken struktur som är lämplig,
- om material bör vara Markdown, YAML eller JSON,
- vad som ska finnas i Chat ZIP,
- vad som ska finnas i Custom GPT,
- om konsolidering behövs.

Användaren ska inte behöva designa Knowledge-arkitekturen manuellt.

## Definition av god Knowledge-arkitektur

En Knowledge-arkitektur är godkänd när:

- beteenderegler och referensmaterial är separerade,
- canonical source är tydlig,
- Chat ZIP kan bära full funktionalitet,
- Custom GPT-kompilering är definierad,
- filgränser kan valideras,
- duplicering minimeras,
- reducerad funktionalitet dokumenteras.
