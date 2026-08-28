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

### Advanced dual distribution (`zip_first_advanced` legacy id)

Passar när:

- GPT:n behöver många runtimefiler,
- scripts eller schemas är centrala,
- den manipulerar projekt-ZIP/repositories,
- Custom GPT-plattformen riskerar att reducera funktionaliteten.

Typiska val:

- Chat ZIP och Custom GPT som två distributionsmål från samma canonical kontrakt,
- scripts + schemas,
- rik strukturerad Knowledge,
- omfattande tester och regression,
- Custom GPT som parallell distribution med dokumenterade plattformsbegränsningar vid behov.

### Workflow / research heavy

Passar när:

- GPT:n arbetar i en flerstegsprocess,
- webbresearch/källor/evidens är centralt,
- output måste vara spårbar,
- flera delprodukter eller beslut skapas.

Typiska val:

- Chat ZIP och Custom GPT som två distributionsmål från samma canonical kontrakt,
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

## Runtime robustness

Alla referensprofiler anger nu samma modellneutrala baslinje för enklare modeller:

- ett `core_contract` ska finnas,
- kritiskt beteende ska ligga i canonical instruktionen,
- Knowledge ska inte krävas för kärnworkflow,
- normalt högst ett obligatoriskt filhopp i kärnflödet.

Profilen får fortfarande använda många stödresurser för fördjupning. Begränsningen gäller bara sådant som måste läsas för att GPT:n över huvud taget ska följa sitt centrala arbetsflöde.
