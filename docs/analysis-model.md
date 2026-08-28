# Analysmodell – GPT Byggaren

## Syfte

Analysmodellen beskriver hur GPT Byggaren ska gå från en användares idé till en rekommenderad GPT-arkitektur utan att lägga tekniska designval på användaren i onödan.

Grundprincip:

> Användaren beskriver behovet. GPT Byggaren härleder implementationen.

## Analysflöde

GPT Byggaren ska analysera idén i följande ordning:

1. förstå verksamhetsbehovet,
2. identifiera användare och huvudsakliga arbetsuppgifter,
3. identifiera typer av indata,
4. identifiera typer av utdata,
5. identifiera kunskaps- och aktualitetsbehov,
6. identifiera behov av verktyg och strukturerad runtime,
7. bedöma komplexitet,
8. rekommendera hur Chat ZIP och Custom GPT ska realiseras och dokumentera eventuella faktiska skillnader,
9. rekommendera capabilities,
10. rekommendera projektprofil,
11. identifiera risker och begränsningar,
12. avgöra om någon verksamhetsfråga verkligen behöver ställas till användaren.

## 1. Verksamhetsbehov

GPT Byggaren ska först formulera:

- vilket problem GPT:n ska lösa,
- vilket resultat användaren vill uppnå,
- vilka beslut eller arbetsmoment GPT:n ska stödja,
- vilka delar som är kärnfunktion och vilka som är sekundära.

Tekniska lösningar ska inte introduceras innan behovet är förstått.

## 2. Användare

Identifiera:

- primär målgrupp,
- eventuell sekundär målgrupp,
- användarnas förkunskaper,
- om GPT:n ska vara pedagogisk, expertorienterad eller båda,
- om arbetsflödet behöver vara styrt eller fritt.

## 3. Indata

Klassificera förväntade indata.

Exempel:

- fri text,
- bifogade dokument,
- PDF,
- Word,
- Markdown,
- ZIP-projekt,
- tabeller,
- strukturerad YAML/JSON,
- webblänkar,
- bilder,
- kod,
- GitHub-repon.

Indatatypen påverkar rekommenderade capabilities och runtime.

## 4. Utdata

Identifiera vilka resultat GPT:n förväntas producera.

Exempel:

- svar i chatten,
- Markdown,
- Word,
- PDF,
- ZIP,
- kod,
- konfigurationsfiler,
- YAML/JSON,
- diagram,
- bilder,
- releaseartefakter.

Om GPT:n ska skapa filer eller paket ska detta behandlas som ett explicit arkitekturkrav.

## 5. Kunskapsmodell

Bedöm om GPT:n behöver:

### Ingen särskild Knowledge

Lämpligt när all relevant information finns i användarens prompt eller aktuella webbkällor.

### Liten statisk Knowledge

Lämpligt för enkla regler, begrepp eller domänreferenser.

### Strukturerad Knowledge

Lämpligt när GPT:n behöver:

- modeller,
- klassificeringar,
- tabeller,
- schemas,
- relationer,
- maskinläsbara regler.

### Rik ZIP-runtime

Lämpligt när GPT:n behöver mer stöd än vad som rimligen kan representeras i Custom GPT Knowledge och instruktion.

## 6. Aktualitetsbehov och webbsökning

Webbsökning ska rekommenderas när uppgiften regelbundet kräver aktuell eller extern information.

Exempel:

- lagar och regler som förändras,
- aktuella produkter eller priser,
- nyheter,
- organisationer,
- externa publikationer,
- aktuell dokumentation.

Webbsökning ska inte aktiveras slentrianmässigt om GPT:n främst arbetar med bifogat eller statiskt material.

## 7. Dataanalys och kodexekvering

Dataanalys ska rekommenderas när GPT:n behöver:

- bearbeta filer,
- transformera data,
- analysera tabeller,
- generera strukturerade artefakter,
- bygga ZIP-filer,
- köra valideringar,
- skapa diagram,
- exekvera stödscript.

För GPT-projekt som själva hanterar filer eller paket är detta normalt ett starkt behov.

## 8. Bildgenerering

Bildgenerering ska rekommenderas endast när användningsfallet faktiskt behöver genererade bilder eller illustrationer.

Det ska inte aktiveras enbart för att funktionen finns.

## 9. Filhantering

Filhantering ska rekommenderas när GPT:n behöver:

- läsa användarens dokument,
- skapa nedladdningsbara artefakter,
- manipulera projekt,
- uppdatera ZIP-paket,
- analysera filer mellan steg.

För GPT Byggaren är detta obligatoriskt.

## 10. Behov av scripts

Scripts rekommenderas när uppgifter behöver vara:

- deterministiska,
- repeterbara,
- validerbara,
- identiska lokalt och i CI,
- möjliga att köra utan LLM-tolkning.

Exempel:

- build,
- lint,
- manifest,
- checksummor,
- schemas,
- paketering,
- release.

## 11. Behov av schemas

Schemas rekommenderas när projektet använder maskinläsbara kontrakt som ska valideras.

Exempel:

- projektstatus,
- gpt-project-konfiguration,
- Knowledge-modeller,
- exportformat.

## 12. Behov av templates

Templates rekommenderas när GPT:n återkommande ska skapa artefakter med stabil struktur.

Exempel:

- rapporter,
- analyser,
- projektdokument,
- YAML-objekt,
- exportformat.

## 13. Behov av tester

GPT Byggaren ska alltid bedöma två separata testbehov.

### Deterministiska tester

För:

- filstruktur,
- schema,
- build,
- instruktionens storlek,
- antal Knowledge-filer,
- manifest,
- checksummor,
- releasepaketering.

### Beteendeevalueringar

För:

- följsamhet till arbetsflöde,
- kvalitet i analys,
- konsekventa rekommendationer,
- osäkerhetshantering,
- outputkvalitet.

Små GPT:er behöver inte alltid omfattande evals.

## Komplexitetsmodell

GPT Byggaren ska klassificera projektet i en av fyra profiler.

### Profil 1 – Enkel

Typiska kännetecken:

- liten instruktion,
- inga eller få Knowledge-filer,
- få arbetsflöden,
- inga scripts,
- inga schemas,
- Custom GPT och ZIP kan vara nästan identiska.

### Profil 2 – Standard

Typiska kännetecken:

- strukturerad instruktion,
- flera Knowledge-filer,
- testsupport,
- två distributioner,
- GitHub Actions,
- begränsad runtime-logik.

### Profil 3 – ZIP-first avancerad

Typiska kännetecken:

- rik runtime,
- scripts,
- schemas,
- templates,
- strukturerad Knowledge,
- projekt-ZIP som aktiv arbetsprodukt,
- Custom GPT som reducerad distribution.

### Profil 4 – Workflow/research-heavy

Typiska kännetecken:

- flera styrda analyssteg,
- källhantering,
- webbresearch,
- evidensmodell,
- exporter,
- omfattande validering,
- evals,
- ofta ZIP-first.

Profilerna är vägledning, inte låsta mallar.

## Runtimebeslut

### När Chat ZIP kan bära capabilities som Custom GPT inte kan

- GPT:n behöver många runtimefiler,
- scripts är viktiga,
- projekt-ZIP ska manipuleras,
- Custom GPT-gränser sannolikt blir ett hinder,
- funktionalitet måste vara rikare än Custom GPT tillåter.

### Rekommendera Custom GPT som likvärdig runtime när

- instruktion och Knowledge ryms naturligt,
- inga ZIP-specifika scripts behövs,
- funktionaliteten kan representeras utan större kompromisser.

### När Custom GPT kan behöva reducerad capability-täckning

- kärnfunktionaliteten kan bevaras,
- men delar av ZIP-runtime behöver reduceras.

### Rekommendera att inte bygga Custom GPT när

- funktionen skulle bli missvisande eller alltför reducerad,
- runtimekrav inte kan representeras meningsfullt.

## Capabilitybeslut

GPT Byggaren ska uttrycka rekommendationer som:

```text
Webbsökning: Rekommenderas
Motivering: GPT:n behöver regelbundet verifiera aktuell extern information.

Dataanalys: Krävs
Motivering: GPT:n ska läsa, transformera och paketera filer.

Bildgenerering: Rekommenderas inte
Motivering: Inget användningsfall kräver genererade bilder.
```

Möjliga nivåer:

- `required`
- `recommended`
- `optional`
- `not_recommended`

## Arkitekturresultat

Efter analysen ska GPT Byggaren kunna producera ett sammanfattat designbeslut.

Exempel:

```yaml
recommended_profile: zip_first_advanced  # legacy id; semantics = advanced dual distribution

runtime:
  primary: none
  chat_zip: peer_distribution
  custom_gpt: peer_distribution

capabilities:
  web: recommended
  data_analysis: required
  image_generation: not_recommended
  file_handling: required

project_features:
  structured_knowledge: true
  scripts: true
  schemas: true
  templates: false
  deterministic_tests: true
  evals: recommended
```

## När GPT Byggaren ska fråga användaren

Fråga endast när svaret påverkar verksamhetsmålet och inte kan härledas rimligt.

Bra frågor:

- Vilken av två helt olika målgrupper ska prioriteras?
- Ska GPT:n kunna ändra originalfiler eller bara skapa kopior?
- Är en viss output obligatorisk för processen?
- Måste GPT:n fungera helt offline från externa källor?

Undvik frågor som:

- Vill du ha webbsökning?
- Vill du ha dataanalys?
- Vill du använda YAML?
- Vill du ha schemas?
- Ska vi ha tester?
- Ska vi använda GitHub Actions?

Dessa ska normalt härledas.

## Rekommenderad analysoutput i idéfasen

Analysen bör normalt innehålla:

1. tolkning av idén,
2. rekommenderad GPT-profil,
3. rekommenderad primär runtime,
4. Custom GPT-bedömning,
5. capabilities,
6. Knowledge- och runtimebehov,
7. testbehov,
8. viktiga risker eller begränsningar,
9. frågor endast om verkliga verksamhetsval återstår,
10. rekommendation att skapa utvecklingsplan när målbilden är stabil.

## Kvalitetsregel

GPT Byggaren ska hellre motivera ett härlett tekniskt beslut än be användaren fatta det utan nödvändig bakgrund.


## Referensprofiler

Analysresultatet ska kopplas till närmaste maskinläsbara profil under `profiles/`.

Profilen är en utgångspunkt och får justeras med projektspecifika avvikelser.
