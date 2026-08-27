# Slutlig arkitektur- och förenklingsrevision – GPT Byggaren

## Syfte

Steg 28 granskar projektet som helhet efter att hela kedjan från idé till distribution nu finns på plats.

Målet är inte att ta bort funktionalitet. Målet är att:

- minska dubblering,
- tydliggöra vilken fil som är canonical,
- minska risken att olika scripts implementerar samma regel olika,
- separera modeller/policies från exekverbar logik,
- förenkla vidare underhåll inför release candidate.

---

## Huvudobservationer

### 1. För många scripts hade delvis överlappande beslut

Före revisionen fanns separata scripts för bland annat:

- profilval,
- next-step recommendation,
- resume,
- hygiene,
- release readiness,
- referensprojektsvalidering,
- E2E.

Det är rimligt att dessa finns separat som CLI-kommandon, men kärnlogiken bör inte dupliceras mellan dem.

### 2. Profilval duplicerades

Profilvalslogik förekom i:

- `scripts/select_reference_profile.py`
- `scripts/evaluate_reference_projects.py`
- `scripts/run_e2e_blank_idea.py`
- testkod

Detta är en tydlig risk för drift.

### 3. Statusläsning och projektidentifiering återkommer

Resume, next-step och release readiness läser samma centrala filer.

### 4. Dokumentation och runtime-policy har olika roller

Det är bra att båda finns, men rollerna tydliggörs:

- `docs/` = förklaring och design,
- `src/runtime-policy/` = korta runtime-regler,
- `scripts/lib/` = canonical exekverbar logik.

### 5. Buildsystemet ska förbli separat

Build- och distributionsskripten är tillräckligt centrala för att inte slås ihop med analys-/statuslogik.

---

## Beslut i steg 28

### Gemensamt Python-bibliotek införs

Ny canonical katalog:

```text
scripts/lib/
```

Den innehåller återanvändbar logik för:

- projektläsning,
- profilval,
- status,
- next-step-grunder.

CLI-scripts blir tunna wrappers.

### Profilval centraliseras

Canonical funktion:

```python
scripts/lib/project_model.py::select_reference_profile()
```

Följande använder samma funktion:

- `select_reference_profile.py`
- `evaluate_reference_projects.py`
- `run_e2e_blank_idea.py`

Det eliminerar tre implementationer av samma regel.

### Projektläsning centraliseras

Canonical helpers:

```python
load_yaml()
load_project_config()
load_project_status()
```

Resume och senare scripts kan använda samma kontrakt.

### Ingen aggressiv filkonsolidering

Policies och docs slås inte samman automatiskt eftersom de har olika målgrupp.

### Inga historiska kopior behålls

Git ska vara historiken.

---

## Canonical lager efter revision

```text
gpt-project.yaml
        ↓
scripts/lib/project_model.py
        ↓
CLI scripts
        ↓
tests / evals / CI / release
```

Dokumentation:

```text
docs/
```

Runtime-regler:

```text
src/runtime-policy/
```

Maskinläsbara kontrakt:

```text
schemas/
```

---

## Förenklingsprincip framåt

När ny funktion tillkommer:

1. lägg regel i canonical modell/bibliotek,
2. använd CLI-wrapper vid behov,
3. lägg schema om output är maskinläsbar,
4. lägg test/eval,
5. undvik att kopiera beslutslogik till fler scripts.

---

## Resultat

Revisionen bedömer arkitekturen som lämplig för release candidate efter denna konsolidering.

Kvarvarande komplexitet är huvudsakligen avsiktlig eftersom GPT Byggaren stödjer:

- projektutveckling,
- två runtime-targets,
- CI/release,
- validering,
- resume,
- hygiene,
- test/eval,
- dynamisk planering.

---

## Definition of Done

Steg 28 är klart när:

- duplicerad profilvalslogik är borttagen,
- gemensamt scriptbibliotek finns,
- canonical ansvar är dokumenterat,
- CLI-kommandon använder gemensam logik,
- projektet fortfarande kan kompileras och paketeras,
- inga överflödiga historiska filer finns kvar.
