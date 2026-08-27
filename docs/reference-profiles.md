# Referensprofiler – GPT Byggaren

## Syfte

Referensprofilerna gör analysresultatet konkret.

De är inte hårda mallar. GPT Byggaren använder dem som utgångspunkt och justerar efter användningsfallet.

## Profiler

### Simple

Passar när:

- uppgiften är relativt enkel,
- Knowledge är litet eller saknas,
- inga lokala scripts behövs,
- Custom GPT kan vara likvärdig med Chat runtime.

Typiska val:

- Custom GPT och/eller Chat,
- få filer,
- grundläggande tester,
- liten evaluppsättning.

### Standard

Passar när:

- GPT:n har tydligt arbetsflöde,
- viss Knowledge finns,
- strukturerade outputs eller templates kan behövas,
- både Chat ZIP och Custom GPT är realistiska mål.

Typiska val:

- schemas vid strukturerad data,
- templates för återkommande outputs,
- runtime smoke tests,
- centrala beteendeevalueringar.

### ZIP-first advanced

Passar när:

- GPT:n behöver många runtimefiler,
- scripts eller schemas är centrala,
- den manipulerar projekt-ZIP/repositories,
- Custom GPT-plattformen riskerar att reducera funktionaliteten.

Typiska val:

- Chat ZIP som primär runtime,
- scripts + schemas,
- rik strukturerad Knowledge,
- omfattande tester och regression,
- Custom GPT som sekundär distribution.

### Workflow / research heavy

Passar när:

- GPT:n arbetar i en flerstegsprocess,
- webbresearch/källor/evidens är centralt,
- output måste vara spårbar,
- flera delprodukter eller beslut skapas.

Typiska val:

- Chat ZIP som primär runtime,
- strukturerad Knowledge,
- templates,
- workflow-evals,
- käll-/evidens-evals,
- felhantering och resume.

## Hur profil väljs

GPT Byggaren väger bland annat:

- arbetsflödets komplexitet,
- filvolym,
- behov av scripts,
- behov av schemas,
- strukturerad Knowledge,
- käll/evidenskrav,
- projekt-ZIP-manipulation,
- Custom GPT-begränsningar.

## Profiler är startpunkter

Exempel:

```text
Profile: standard
Adjustments:
- scripts required
- Custom GPT secondary
```

Projektet behöver alltså inte passa exakt i en enda profil.

## Maskinläsbar form

Profilerna ligger under:

```text
profiles/
```

och kan läsas av analys- och planeringslogiken.

## Definition of Done

Referensprofilerna är klara när:

- fyra profiler finns maskinläsbart,
- varje profil har runtime-, Knowledge-, script-, schema-, test- och CI-standarder,
- profilerna används som rekommendationsbas,
- individuella projekt får avvika med dokumenterad motivering.
