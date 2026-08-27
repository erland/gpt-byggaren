# End-to-end-test från blank idé – GPT Byggaren

## Scenario

Användaren säger:

> Jag vill skapa en GPT som hjälper en projektledare att analysera mötesanteckningar, identifiera beslut, risker och aktiviteter samt skapa en strukturerad uppföljning.

## Förväntad resa

```text
idé
↓
analys
↓
profil = standard
↓
utvecklingsplan
↓
första projektstruktur
↓
gpt-project.yaml + project-status.yaml
↓
canonical instruktion
↓
projekt-ZIP
↓
Chat ZIP
↓
Custom GPT ZIP
↓
checksummor + delivery manifest
```

## Vad testet verifierar

Det isolerade E2E-testet verifierar att hela kontraktskedjan kan representeras och produceras från en blank idé:

- profilval,
- plan,
- projektkontrakt,
- status,
- canonical instruktion,
- projekt-ZIP,
- Chat ZIP,
- Custom GPT ZIP,
- checksummor,
- leveransmanifest.

## Viktig avgränsning

Testet använder en deterministisk E2E-harness. Själva kvalitativa LLM-analysen av användarens fria text testas separat via evals.

Detta gör att regressioner i projekt- och distributionskedjan kan fångas utan att testresultatet beror på variation i en språkmodells formulering.

## Resultat

Scenario `blank-idea-001` ska ge:

```text
profile: standard
project: mötesuppföljaren
project ZIP: PASS
Chat ZIP: PASS
Custom GPT ZIP: PASS
delivery manifest: PASS
checksums: PASS
```

## Arkitekturell observation

Steg 27 visar också att GPT Byggaren nu har alla centrala kontrakt för hela resan. En framtida förenklingsrevision kan avgöra vilka delar som bör konsolideras till färre scripts och modeller innan release.
