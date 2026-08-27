# Utvecklingsplan – GPT Byggaren

## 1. Syfte och målbild

**GPT Byggaren** ska hjälpa en användare från idé till en fungerande, testad och paketerad GPT utan att användaren behöver känna till detaljerna i Custom GPT Builder, GitHub Actions, distributionsformat eller tekniska plattformsbegränsningar.

GPT Byggaren ska kunna:

- analysera en idé till en GPT och rekommendera lämplig arkitektur,
- själv rekommendera capabilities, runtime-strategi, struktur, tester och distributionsmodell,
- skapa en stegvis utvecklingsplan som nedladdningsbar Markdown,
- skapa en första komplett projekt-ZIP när planens första genomförandesteg utförs,
- bygga vidare på samma projekt-ZIP steg för steg,
- rekommendera nästa steg utifrån både planen och projektets faktiska status,
- automatiskt identifiera och rensa bort ersatta, historiska eller tillfälliga arbetsfiler,
- stödja **ZIP-first** som primär runtime för större GPT:er,
- skapa en reducerad eller transformerad **Custom GPT-distribution** när det är lämpligt,
- validera plattformsbegränsningar, inklusive instruktionens storlek och antal Knowledge-filer,
- skapa GitHub Actions som bygger releaseartefakter med versionsnummer från GitHub Release-taggen,
- bygga distributionsartefakterna direkt och ge användaren nedladdningslänkar även om GitHub inte används.

Den centrala användarresan ska vara:

```text
Idé i chatten
    ↓
Analys och rekommenderad målbild
    ↓
Nedladdningsbar utvecklingsplan.md
    ↓
Steg 1 genomförs
    ↓
Projekt-ZIP skapas
    ↓
Projekt-ZIP byggs på steg för steg
    ↓
Tester + validering + project hygiene
    ↓
├─ Chat/ZIP-distribution
├─ Custom GPT-distribution
└─ Komplett projekt-ZIP
    ↓
Valfritt:
Packa upp projekt-ZIP i Git-repo
    ↓
GitHub Release
    ↓
GitHub Actions bygger distributionsartefakter
```

---

# Grundprinciper

Följande principer ska vara styrande under hela utvecklingen.

## A. ZIP-first för avancerade GPT:er

ZIP-distributionen är primär runtime för större eller mer avancerade GPT:er.

Custom GPT-begränsningar får inte tvinga fram en sämre arkitektur i den primära GPT:n.

## B. Custom GPT är ett distributionsmål

Custom GPT behöver inte vara identisk med ZIP-runtime.

Den kan vara:

- reducerad,
- konsoliderad,
- komprimerad,
- transformerad,
- eller sakna funktioner som inte kan representeras inom Custom GPT-plattformens begränsningar.

## C. Single source of truth

Kanoniska instruktioner, modeller, mallar och regler ska underhållas på ett ställe.

Distributionsspecifika filer ska så långt möjligt genereras.

## D. Git är historiken

Gamla versioner av instruktioner, planer eller runtimefiler ska normalt inte ligga kvar i projektets aktuella HEAD enbart för historik.

## E. Automatisk project hygiene

GPT Byggaren ska själv identifiera:

- tillfälliga arbetsfiler,
- ersatta filer,
- duplicerad dokumentation,
- gamla genererade artefakter,
- caches,
- lokala testresultat,
- historiska kopior som Git redan bevarar.

Städning ska ske löpande och alltid före release.

## F. Behovsdriven design

Användaren beskriver **vad GPT:n ska åstadkomma**.

GPT Byggaren ska själv analysera och rekommendera:

- webbsökning,
- dataanalys,
- bildgenerering,
- filhantering,
- strukturerad Knowledge,
- scripts,
- schemas,
- templates,
- tester,
- evals,
- runtime-strategi,
- distributionsformat.

Tekniska frågor ska bara ställas när ett verkligt verksamhetsval inte kan härledas.

## G. Projekt-ZIP är den löpande arbetsprodukten

När utvecklingsplanen är klar och första genomförandesteg utförs skapas en komplett projekt-ZIP.

Varje efterföljande steg ska returnera en ny komplett projekt-ZIP.

## H. Releaseversion kommer från GitHub Release

Vid GitHub-baserad release ska GitHub Release-taggen vara sanningskälla för versionsnumret.

Exempel:

```text
v1.4.0
```

ska ge distributionsfiler med version `1.4.0`.

## I. GitHub ska vara valfritt

Användaren ska kunna få färdiga distributionsartefakter direkt från GPT Byggaren utan att använda GitHub.

Samma projekt ska samtidigt kunna packas upp i ett Git-repo och få identiska eller funktionellt motsvarande distributionsartefakter via GitHub Actions.

---

# Utvecklingssteg

## Steg 1 – Definiera produktvision och användarresa

### Mål

Definiera exakt vad GPT Byggaren är, vem den är till för och hur den ska användas.

### Ta fram

- produktvision,
- målgrupper,
- huvudsakliga användningsfall,
- centrala användarresor,
- vad GPT Byggaren ska göra själv,
- vilka frågor den ska undvika att lägga på användaren,
- skillnaden mellan idéfas, planfas, projektfas och releasefas.

### Viktiga scenarier

Minst:

1. ny användare med bara en GPT-idé,
2. erfaren användare som vill skapa en avancerad ZIP-first GPT,
3. användare som vill skapa både ZIP- och Custom GPT-version,
4. användare som inte använder GitHub,
5. användare som vill lägga projektet i GitHub efteråt,
6. användare som återkommer med en tidigare projekt-ZIP,
7. användare som vill fortsätta från nästa steg i planen.

### Leverans

Första projekt-ZIP:en skapas här.

Projektet ska redan innehålla utvecklingsplanen och en initial projektstatus.

---

## Steg 2 – Definiera projektets kanoniska struktur

### Mål

Skapa en generell men flexibel projektstruktur.

### Utred

Vilka kataloger som ska vara:

- obligatoriska,
- valfria,
- genererade,
- endast för utveckling,
- endast för runtime.

### Exempel på möjlig struktur

```text
gpt-project/
├── README.md
├── PROJECT.md
├── STATUS.md
├── gpt-project.yaml
│
├── docs/
│   └── development-plan.md
│
├── src/
├── runtime/
├── knowledge/
├── templates/
├── schemas/
├── scripts/
├── tests/
├── evals/
│
├── distributions/
│
└── .github/
    └── workflows/
```

Strukturen ska kunna reduceras för enkla GPT:er.

---

## Steg 3 – Skapa `gpt-project.yaml`

### Mål

Definiera ett maskinläsbart kontrakt för GPT-projektet.

### Specifikationen bör kunna beskriva

- projektidentitet,
- GPT-namn,
- språk,
- primär runtime,
- capabilities,
- canonical instruction source,
- Knowledge-källor,
- runtimefiler,
- templates,
- schemas,
- scripts,
- tester,
- distributionsmål,
- plattformsgränser,
- buildregler,
- releaseversionering,
- GitHub-releasekonfiguration.

### Exempel

```yaml
schema_version: 1

project:
  id: example-gpt
  name: Example GPT

runtime:
  primary: chat_zip

distributions:
  chat_zip:
    enabled: true

  custom_gpt:
    enabled: true

release:
  version_source: github_release_tag
```

---

## Steg 4 – Definiera projektstatus och planprogression

### Mål

Göra projektet självbärande mellan konversationer.

### Ta fram

Ett format för exempelvis `STATUS.md` eller `project-status.yaml`.

Det ska visa:

- genomförda steg,
- aktuellt steg,
- rekommenderat nästa steg,
- avvikelser från planen,
- blockerande problem,
- senaste valideringsresultat,
- senaste hygiene-pass,
- distributionsstatus.

GPT Byggaren ska kunna läsa en projekt-ZIP i en ny konversation och fortsätta utan att användaren återberättar historiken.

---

## Steg 5 – Definiera GPT Byggarens analysmodell

### Mål

Skapa regler för hur GPT Byggaren analyserar en GPT-idé.

### GPT Byggaren ska själv bedöma

- GPT:ns komplexitet,
- lämplig ambitionsnivå,
- om ZIP-first rekommenderas,
- om Custom GPT bör stödjas,
- behov av Knowledge,
- behov av strukturerade data,
- behov av scripts,
- behov av schemas,
- behov av templates,
- behov av webbsökning,
- behov av dataanalys,
- behov av bildgenerering,
- behov av tester och evals.

### Resultat

En rekommenderad målarkitektur med motiveringar.

---

## Steg 6 – Definiera dynamisk utvecklingsplanering

### Mål

GPT Byggaren ska skapa en projektspecifik plan i stället för att använda samma antal steg för alla GPT:er.

### Planen ska anpassas efter

- komplexitet,
- runtime,
- Knowledge,
- verktyg,
- distributionskrav,
- testbehov,
- risknivå.

### Varje plansteg ska innehålla

- mål,
- ändringar,
- förväntade filer,
- tester,
- valideringar,
- hygiene-kontroller,
- kriterium för klart,
- beroenden till nästa steg.

---

## Steg 7 – Definiera filklassificering och project hygiene

### Mål

Förhindra att projektet samlar på sig onödiga filer under stegvis utveckling.

### Klassificera filer som

- `CANONICAL`
- `RUNTIME`
- `DEVELOPMENT`
- `GENERATED`
- `TEMPORARY`
- `HISTORICAL`

### Regler

- `TEMPORARY` tas bort när uppgiften är avslutad.
- `HISTORICAL` ska normalt inte ligga i HEAD.
- `GENERATED` ska kunna byggas om.
- duplicerade canonical sources ska undvikas.
- caches och lokala testresultat ska inte distribueras.

---

## Steg 8 – Definiera instruktionarkitektur

### Mål

Skapa en generell modell för GPT-instruktioner.

### Utred

Hur instruktioner delas upp i exempelvis:

- identitet,
- syfte,
- scope,
- arbetsflöde,
- beslutsregler,
- verktygsregler,
- outputregler,
- källhantering,
- osäkerhet,
- kvalitetskontroll.

ZIP-runtime ska få använda en rikare instruktionarkitektur än Custom GPT när det behövs.

---

## Steg 9 – Definiera Knowledge-arkitektur

### Mål

Skilja tydligt mellan instruktioner och referensmaterial.

### GPT Byggaren ska kunna rekommendera

- antal Knowledge-filer,
- struktur,
- ämnesindelning,
- maskinläsbara format,
- konsolidering,
- när material bör ligga i instruktionen,
- när material bör vara runtime-stöd i ZIP i stället för Custom GPT Knowledge.

---

## Steg 10 – Definiera ZIP-runtime

### Mål

Skapa standarden för den primära portable Chat ZIP-distributionen.

### Definiera

- `START-HERE.md`,
- instruktioner,
- Knowledge,
- runtime policies,
- schemas,
- scripts,
- templates,
- modeller,
- manifest,
- versionsfil.

ZIP-runtime ska kunna innehålla mer stöd än Custom GPT.

---

## Steg 11 – Definiera Custom GPT-kompilering

### Mål

Skapa ett separat distributionsmål för Custom GPT.

### Stöd för

- identisk instruktion för enkla projekt,
- komprimerad instruktion för avancerade projekt,
- konsolidering av Knowledge,
- urval av Knowledge,
- genererade Knowledge bundles,
- tydlig dokumentation av reducerad funktionalitet.

Custom GPT ska betraktas som ett kompileringsmål, inte nödvändigtvis projektets canonical runtime.

---

## Steg 12 – Definiera plattformsvalidering

### Mål

Kontrollera att Custom GPT-distributionen går att installera.

### Validera minst

- instruktionens teckenlängd,
- antal Knowledge-filer,
- filstorlekar,
- tillåtna format,
- obligatoriska Builder-filer,
- conversation starters,
- capability-rekommendationer.

Plattformsgränser ska vara konfigurerbara och inte spridas som hårdkodade konstanter.

---

## Steg 13 – Definiera funktionell paritet mellan runtimes

### Mål

Synliggöra skillnader mellan ZIP och Custom GPT.

### Exempel

```text
Capability                     ZIP   Custom GPT
------------------------------------------------
Grundarbetsflöde                ✓        ✓
Strukturerad runtime            ✓        ~
Lokala scripts                  ✓        -
Utökad Knowledge               ✓        ~
```

### Resultat

En automatisk paritetsrapport.

---

## Steg 14 – Skapa buildsystem

### Mål

Bygga distributionsartefakter deterministiskt.

### Ska kunna bygga

- projekt-ZIP,
- Chat ZIP,
- Custom GPT ZIP.

### Krav

- deterministisk paketering,
- checksummor,
- manifest,
- inga temporära filer,
- inga caches,
- korrekt versionsinformation.

---

## Steg 15 – Skapa direktbyggnad utan GitHub

### Mål

Användaren ska kunna få färdiga artefakter direkt från GPT Byggaren.

När ett projekt når distributionsbar status ska GPT Byggaren kunna skapa och ge länkar till:

```text
my-gpt-project.zip
my-gpt-chat-v1.0.0.zip
my-gpt-custom-gpt-v1.0.0.zip
```

Versionshanteringen kan använda en lokal utvecklingsversion innan en riktig GitHub Release finns.

### Viktigt

GitHub ska inte krävas för att använda GPT Byggaren.

---

## Steg 16 – Skapa GitHub Actions-releaseflöde

### Mål

Projekt-ZIP:en ska kunna packas upp i ett Git-repo och fungera direkt.

### GitHub Actions ska

1. triggas på publicerad GitHub Release,
2. läsa release-taggen,
3. validera taggformat,
4. härleda distributionsversion,
5. bygga Chat ZIP,
6. bygga Custom GPT ZIP om den är aktiverad,
7. köra tester,
8. köra distributionsvalidering,
9. skapa checksummor,
10. publicera releaseartefakter.

Ingen manuell versionsuppdatering ska behövas.

---

## Steg 17 – Skapa CI för commits och pull requests

### Mål

Fånga fel före release.

### Kontrollera exempelvis

- projektschema,
- instruktioner,
- Knowledge,
- tester,
- build,
- plattformsgränser,
- broken references,
- manifest,
- project hygiene.

Releaseflödet ska därmed inte vara första gången distributionerna testas.

---

## Steg 18 – Definiera testmodell

### Mål

Skapa en gemensam modell för GPT-tester.

### Testtyper

- strukturella tester,
- instruktionsvalidering,
- Knowledge-validering,
- runtime-tester,
- distributionsvalidering,
- regressionsfall,
- evals.

Testnivån ska anpassas efter GPT:ns komplexitet.

---

## Steg 19 – Skapa GPT-linter

### Mål

Ge begriplig kvalitetsfeedback.

### Exempel

```text
Instructions
✓ 7 054 / 8 000 characters

Knowledge
✗ 31 / 20 Custom GPT files

Runtime
✓ ZIP runtime complete

Project hygiene
⚠ 3 obsolete files detected

Release
✓ version derived from GitHub tag

RESULT: FAILED
```

---

## Steg 20 – Definiera nästa-steg-rekommendation

### Mål

GPT Byggaren ska efter varje genomfört steg analysera vad som bör göras härnäst.

Den ska inte mekaniskt säga ”nästa nummer”.

### Bedöm

- är föregående steg verkligen klart?
- finns blockerande fel?
- behövs ett extra hygiene-pass?
- behöver planen revideras?
- är nästa steg fortfarande lämpligt?

### Normal återkoppling

```text
Steg 8 klart.

Validering: PASS
Project hygiene: PASS

Rekommenderat nästa steg:
Steg 9 – Knowledge-arkitektur

Projekt-ZIP:
[download]
```

---

## Steg 21 – Skapa återupptagningsflöde

### Mål

En tidigare projekt-ZIP ska kunna användas i en ny chat.

GPT Byggaren ska:

1. inventera ZIP:en,
2. läsa projektdefinitionen,
3. läsa status,
4. läsa utvecklingsplanen,
5. validera projektets skick,
6. rekommendera nästa steg.

Användaren ska inte behöva återge tidigare konversation.

---

## Steg 22 – Skapa projektrensning och final hygiene

### Mål

Göra projektet rent inför release.

### Kontrollera

- temporära filer,
- historiska kopior,
- ersatta utkast,
- dubbla canonical sources,
- genererade artefakter som inte ska versionshanteras,
- caches,
- lokala loggar,
- testoutput,
- gamla distributionsfiler.

---

## Steg 23 – Skapa release readiness-bedömning

### Mål

Avgöra om GPT:n är redo att distribueras.

### Rapportera

- projektstatus,
- teststatus,
- ZIP-runtime,
- Custom GPT-status,
- kända funktionsskillnader,
- plattformsbegränsningar,
- hygiene,
- GitHub Actions,
- release readiness.

---

## Steg 24 – Skapa dokumentation för nybörjare

### Mål

En användare som aldrig skapat en GPT ska förstå hur resultatet används.

### Dokumentation

- vad projekt-ZIP:en är,
- hur ZIP-runtime används i ChatGPT,
- hur Custom GPT-paketet installeras,
- hur projektet läggs i GitHub,
- hur första releasen skapas,
- hur GitHub Actions fungerar,
- hur en senare version byggs,
- hur projektet återöppnas i GPT Byggaren.

---

## Steg 25 – Skapa referensprofiler

### Mål

GPT Byggaren ska kunna känna igen olika GPT-typer.

Minst:

### Enkel GPT

- liten instruktion,
- få Knowledge-filer,
- Custom GPT och ZIP nära identiska.

### Standard-GPT

- strukturerad Knowledge,
- tester,
- två distributioner,
- GitHub Actions.

### ZIP-first avancerad GPT

- rik runtime,
- scripts,
- schemas,
- templates,
- modeller,
- reducerad Custom GPT.

### Workflow/research-heavy GPT

- styrda arbetsflöden,
- källhantering,
- analyssteg,
- exporter,
- omfattande tester/evals.

---

## Steg 26 – Testa GPT Byggaren på referensprojekt

### Mål

Verifiera designen mot realistiska GPT-projekt.

### Testa mot minst

- en enkel GPT,
- en GPT som fungerar både som Custom GPT och ZIP,
- en avancerad ZIP-first GPT,
- en workflow-heavy GPT.

### Kontrollera

- kan projektet återskapas?
- rekommenderas rätt runtime?
- identifieras överflödiga filer?
- blir distributionerna korrekta?
- fungerar GitHub Actions?
- upptäcks Custom GPT-begränsningar?

---

## Steg 27 – End-to-end-test från blank idé

### Mål

Simulera en helt ny användare.

### Scenario

1. användaren beskriver en idé,
2. GPT Byggaren analyserar den,
3. målarkitektur rekommenderas,
4. plan skapas,
5. steg 1 skapar projekt-ZIP,
6. projektet byggs stegvis,
7. tester skapas,
8. hygiene utförs,
9. distributioner byggs,
10. länkar ges direkt,
11. projektet packas upp i GitHub,
12. release skapas,
13. GitHub Actions producerar motsvarande artefakter.

---

## Steg 28 – Slutlig arkitektur- och förenklingsrevision

### Mål

Säkerställa att GPT Byggaren inte blivit mer komplicerad än användaren behöver.

### Kontrollera

- onödiga obligatoriska filer,
- onödiga frågor,
- duplicerade regler,
- för mycket process för enkla GPT:er,
- för svag modell för avancerade GPT:er,
- för hård koppling till GitHub,
- för hård koppling till Custom GPT.

---

## Steg 29 – Release candidate

### Mål

Skapa första kompletta releasekandidaten.

### Leveranser

- komplett projekt-ZIP,
- Chat ZIP,
- Custom GPT ZIP,
- installationsinstruktion,
- GitHub Actions,
- tester,
- valideringsrapport,
- funktionell paritetsrapport,
- checksummor.

---

## Steg 30 – Första stabila release

### Mål

Släppa GPT Byggaren som en självhostande GPT-utvecklingsmiljö.

Den färdiga GPT Byggaren ska därefter kunna användas för att utveckla nästa version av sig själv enligt samma process.

---

# Förväntat arbetssätt under genomförandet

Efter att denna plan accepterats bör genomförandet ske så här:

```text
Användare:
Gör steg 1.

GPT Byggaren:
- genomför steg 1
- skapar första projektstrukturen
- lägger in denna utvecklingsplan
- skapar projektstatus
- kör relevanta kontroller
- skapar komplett projekt-ZIP
- ger nedladdningslänk
- rekommenderar nästa steg
```

Vid nästa prompt:

```text
Användare:
Gör nästa steg.
```

GPT Byggaren ska:

1. läsa aktuell projekt-ZIP,
2. verifiera status,
3. avgöra rekommenderat nästa steg,
4. genomföra steget,
5. testa resultatet,
6. utföra lämplig project hygiene,
7. uppdatera projektstatus,
8. skapa en ny komplett projekt-ZIP,
9. ge nedladdningslänk,
10. rekommendera fortsatt arbete.

---

# Slutliga distributionskrav

När GPT Byggaren har skapat en färdig GPT ska användaren normalt få tre artefakter.

## 1. Projekt-ZIP

Exempel:

```text
my-gpt-project.zip
```

Den ska kunna:

- packas upp lokalt,
- versionshanteras,
- checkas in i Git,
- publiceras på GitHub,
- vidareutvecklas av GPT Byggaren.

## 2. Chat ZIP

Exempel:

```text
my-gpt-chat-v1.0.0.zip
```

Detta är den primära runtime-distributionen för större GPT:er.

Den ska kunna bifogas direkt i en ChatGPT-konversation och användas som GPT-kontext.

## 3. Custom GPT ZIP

Exempel:

```text
my-gpt-custom-gpt-v1.0.0.zip
```

Den ska innehålla allt som behövs för att konfigurera motsvarande Custom GPT, inom plattformens aktuella begränsningar.

Om full funktionell paritet inte är möjlig ska det dokumenteras tydligt.

---

# GitHub som valfri distributionskanal

Projekt-ZIP:en ska alltid vara GitHub-redo, men GitHub ska vara frivilligt.

Två likvärdiga vägar ska stödjas:

```text
A. Direkt från GPT Byggaren

Projekt-ZIP
Chat ZIP
Custom GPT ZIP
```

eller:

```text
B. Via GitHub

Projekt-ZIP
    ↓
Git-repo
    ↓
GitHub Release v1.0.0
    ↓
GitHub Actions
    ↓
Chat ZIP
Custom GPT ZIP
Checksummor
```

Användaren ska alltså aldrig behöva lägga projektet i GitHub enbart för att få en fungerande GPT-distribution.

---

# Definition of Done för GPT Byggaren

GPT Byggaren v1.0 är klar när den kan:

- ta emot en GPT-idé från en nybörjare,
- rekommendera lämplig GPT-arkitektur,
- skapa en anpassad utvecklingsplan,
- skapa en projekt-ZIP från första genomförandesteg,
- fortsätta utvecklingen steg för steg,
- själv rekommendera nästa steg,
- hålla projektstatus,
- rensa överflödiga arbetsfiler,
- bygga en rik ZIP-runtime,
- bygga en Custom GPT-runtime,
- mäta och beskriva funktionell paritet,
- validera Custom GPT-begränsningar,
- bygga alla artefakter direkt åt användaren,
- skapa ett GitHub-redo projekt,
- bygga releaseartefakter från GitHub Release-taggen,
- återuppta ett projekt från en tidigare ZIP i en ny konversation.
