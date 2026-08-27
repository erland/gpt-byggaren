# Projektstatus och planprogression

## Syfte

GPT Byggaren måste kunna fortsätta ett GPT-projekt i en ny konversation utan att användaren behöver återberätta tidigare arbete.

Därför används två statusrepresentationer:

- `project-status.yaml` – maskinläsbar sanningskälla för progression och återupptagning,
- `STATUS.md` – mänskligt läsbar sammanfattning.

## Rollfördelning

### `project-status.yaml`

Ska användas av:

- GPT Byggaren vid återupptagning,
- framtida valideringsscript,
- framtida buildverktyg,
- framtida CI,
- automatiska nästa-steg-bedömningar.

### `STATUS.md`

Ska ge användaren en lättläst överblick.

Den ska genereras eller hållas synkroniserad med `project-status.yaml`.

## Statusmodell

Statusen innehåller:

- projektidentitet,
- sökväg till utvecklingsplan,
- totalt antal planerade steg,
- aktuellt steg,
- senast genomfört steg,
- genomförda steg,
- eventuellt överhoppade steg,
- eventuellt inskjutna korrigeringssteg,
- blockerande problem,
- varningar,
- senaste validering,
- senaste project hygiene,
- rekommenderat nästa steg,
- stöd för återupptagning.

## Grundprincip

Planen är **styrande men inte mekanisk**.

GPT Byggaren ska inte anta att nästa steg alltid är `current_step + 1`.

Den ska bedöma:

1. om föregående steg verkligen är klart,
2. om blockerande fel finns,
3. om ett extra hygiene-pass behövs,
4. om ett korrigeringssteg behöver skjutas in,
5. om planen behöver revideras,
6. om planerat nästa steg fortfarande är lämpligt.

## Inskjutna steg

Om ett extra steg behövs ska det dokumenteras i `inserted_steps`.

Exempel:

```yaml
inserted_steps:
  - id: 8a
    after_step: 8
    title: Konsolidera överlappande runtime-policy
    reason: >
      Två filer beskriver samma regel och bör konsolideras innan
      Knowledge-arkitekturen byggs.
    status: completed
```

Planens ursprungliga stegnummer behöver då inte skrivas om.

## Blockerande problem

Blockeringar ska dokumenteras uttryckligen.

Exempel:

```yaml
state:
  overall: blocked
  blocking_issues:
    - id: custom-gpt-knowledge-limit
      description: Custom GPT package exceeds configured Knowledge file limit.
      discovered_in_step: 12
```

GPT Byggaren ska då rekommendera korrigering före fortsatt arbete om problemet påverkar nästa steg.

## Återupptagning

När en projekt-ZIP öppnas i en ny konversation ska GPT Byggaren i normalfallet läsa följande i denna ordning:

1. `gpt-project.yaml`
2. `project-status.yaml`
3. `docs/development-plan.md`
4. relevant projektdokumentation
5. endast därefter övriga källfiler som behövs för nästa steg

## Minimikrav för återupptagning

Följande filer är obligatoriska:

```text
gpt-project.yaml
project-status.yaml
docs/development-plan.md
```

`STATUS.md` rekommenderas men är inte den maskinläsbara sanningskällan.

## Synkronisering

Efter varje genomfört steg ska GPT Byggaren:

1. uppdatera `project-status.yaml`,
2. uppdatera `STATUS.md`,
3. uppdatera relevanta projektdokument,
4. köra project hygiene,
5. bygga en ny komplett projekt-ZIP.

## Statusvärden

Rekommenderade värden för `state.overall`:

- `pass`
- `warning`
- `blocked`
- `failed`

## Definition av genomfört steg

Ett steg får markeras som genomfört först när:

- dess huvudsakliga leverans finns,
- relevanta kontroller har körts,
- status har uppdaterats,
- project hygiene har bedömts,
- projekt-ZIP kan byggas.
