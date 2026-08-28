# Dynamisk utvecklingsplanering – GPT Byggaren

## Syfte

GPT Byggaren ska inte använda samma utvecklingsplan för alla GPT-projekt.

Planen ska härledas från analysmodellen och anpassas efter:

- verksamhetsbehov,
- projektprofil,
- primär runtime,
- Custom GPT-stöd,
- Knowledge-behov,
- scripts,
- schemas,
- templates,
- tester,
- evals,
- webbresearch,
- exportbehov,
- releasekrav.

## Grundprincip

> Planen ska vara så liten som möjligt men så omfattande som nödvändigt.

En enkel GPT ska inte få ett 25-stegsprogram bara för att en avancerad GPT behöver det.

## Planeringsflöde

GPT Byggaren ska:

1. analysera idén,
2. klassificera projektprofil,
3. identifiera obligatoriska byggblock,
4. identifiera villkorade byggblock,
5. ordna beroenden,
6. skapa projektspecifika steg,
7. lägga in kontroll- och hygiene-punkter där risk motiverar det,
8. definiera release- och distributionssteg,
9. validera att planen täcker målbilden,
10. exportera planen som nedladdningsbar Markdown.

## Planprofiler

### Enkel GPT

Typisk plan:

1. Syfte och scope
2. Instruktion
3. Knowledge vid behov
4. Conversation starters
5. Grundtester
6. Distribution
7. Release readiness

### Standard-GPT

Typisk plan:

1. Syfte och scope
2. Arkitektur
3. Instruktion
4. Knowledge
5. Runtime-regler
6. Tester
7. Custom GPT
8. Chat ZIP
9. CI
10. Release
11. Hygiene

### advanced dual-distribution GPT

Typisk plan:

1. Vision och use cases
2. Runtimearkitektur
3. Projektmodell
4. Canonical sources
5. Instruktion
6. Knowledge-arkitektur
7. Runtime policies
8. Schemas
9. Scripts
10. Templates
11. Tester
12. Evals
13. Chat ZIP
14. Custom GPT-kompilering
15. Paritetsanalys
16. CI
17. Releaseautomation
18. Hygiene
19. Release candidate

### Workflow/research-heavy GPT

Planen ska dessutom kunna innehålla:

- researchmodell,
- källhantering,
- evidensregler,
- flerfasarbetsflöden,
- exportflöden,
- kvalitetsgrindar,
- scenariobaserade evals.

## Planstegens kontrakt

Varje plansteg ska beskriva:

- `id`
- `title`
- `goal`
- `why_now`
- `inputs`
- `outputs`
- `files_expected`
- `validation`
- `tests`
- `hygiene`
- `done_when`
- `depends_on`

Exempel:

```yaml
id: 6
title: Definiera Knowledge-arkitektur
goal: >
  Bestäm hur domänkunskap ska struktureras mellan canonical source,
  Chat ZIP och Custom GPT.
why_now: >
  Instruktionsarkitekturen är stabil och Knowledge kan nu struktureras
  utan att skapa duplicerade regler.
inputs:
  - docs/architecture.md
  - src/instructions/system.md
outputs:
  - docs/knowledge-architecture.md
files_expected:
  - docs/knowledge-architecture.md
validation:
  - no_duplicate_behavior_rules
tests:
  - knowledge_structure_validation
hygiene:
  - remove_superseded_drafts
done_when:
  - canonical_knowledge_model_defined
depends_on:
  - 5
```

## Beroenden

Planen ska vara beroendedriven.

Exempel:

- buildsystem ska inte utvecklas innan distributionsmodellen är tillräckligt definierad,
- Custom GPT-kompilering ska inte göras innan canonical sources är stabila,
- releaseautomation ska inte göras innan build och validation fungerar lokalt,
- final hygiene ska göras efter att huvudsakliga funktioner finns.

## Villkorade steg

Steg ska bara inkluderas när de behövs.

Exempel:

```text
Schemas        → endast om maskinläsbara kontrakt behövs
Templates      → endast om återkommande artefakter produceras
Webbresearch   → endast om externa/aktuella källor behövs
Evals          → endast när beteende behöver bedömas systematiskt
Custom GPT     → endast om distributionen är meningsfull
GitHub Actions → om GitHub-redo projekt ska levereras
```

För GPT Byggaren är GitHub-redo projekt ett produktkrav, men GitHub ska fortfarande vara valfritt för användaren.

## Kontrollpunkter

GPT Byggaren ska införa checkpoint-steg när projektets risk eller komplexitet motiverar det.

Exempel:

- efter grundarkitektur,
- efter runtime-design,
- före distributionsbygge,
- före release candidate.

Checkpoint behöver inte vara ett eget steg i små projekt.

## Project hygiene i planen

Hygiene ska finnas på två nivåer.

### Löpande hygiene

Efter varje steg:

- ta bort ersatta utkast,
- identifiera duplicerade sources,
- ta bort temporära filer,
- kontrollera att nya filer ligger rätt.

### Final hygiene

Före release:

- inga historiska kopior,
- inga caches,
- inga lokala testresultat,
- inga gamla distributionsartefakter,
- inga döda dokument,
- inga duplicerade canonical sources.

## Anpassning under genomförandet

En utvecklingsplan är inte statisk.

GPT Byggaren får:

- skjuta in korrigeringssteg,
- slå ihop planerade steg,
- hoppa över steg som visat sig irrelevanta,
- dela upp ett steg som blivit för stort.

Alla avvikelser ska dokumenteras i `project-status.yaml`.

## Regel för planrevision

Revidera planen när:

- projektets mål ändras,
- analysen visar ny komplexitet,
- ett planerat distributionsmål tas bort eller tillkommer,
- en teknisk begränsning ändrar arkitekturen,
- ett steg visar att tidigare antagande var fel.

Revidera inte planen enbart för att dokumentera små implementeringsdetaljer.

## Nedladdningsbar plan

När idéanalysen är stabil ska GPT Byggaren skapa planen som en faktisk Markdown-fil.

Föreslaget filnamn:

```text
utvecklingsplan-<projekt-id>.md
```

När första genomförandesteget startar ska planen kopieras in i projektet som:

```text
docs/development-plan.md
```

## Projekt-ZIP och planen

Före första genomförandesteget:

```text
chat
  ↓
nedladdningsbar plan.md
```

Efter första genomförandesteget:

```text
projekt-ZIP
├── docs/development-plan.md
├── project-status.yaml
└── ...
```

Därefter är projekt-ZIP:en den löpande arbetsprodukten.

## Nästa-steg-rekommendation

Efter varje genomfört steg ska GPT Byggaren:

1. kontrollera step completion,
2. kontrollera blockerande problem,
3. kontrollera hygiene,
4. kontrollera beroenden,
5. läsa planerat nästa steg,
6. avgöra om det fortfarande är lämpligt,
7. rekommendera nästa faktiska steg.

## Definition av en bra plan

En plan är godkänd när:

- alla kärnkrav täcks,
- inga uppenbart onödiga steg finns,
- beroenden är rimliga,
- varje steg är tillräckligt avgränsat för en egen prompt,
- varje steg har klart-kriterier,
- distribution och release ingår,
- hygiene ingår,
- projektet kan byggas iterativt utan att användaren behöver hålla ihop tekniska detaljer.
