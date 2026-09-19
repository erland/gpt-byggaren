# Buildsystem – GPT Byggaren

## Syfte

Steg 14 introducerar den första körbara toolchainen för att bygga GPT-projektets artefakter.

## Script

### `scripts/build_distributions.py`

Bygger konkreta distributioner från artifact- och runtime-kontrakten:

- projekt-ZIP som realisering av `project_package`,
- Chat ZIP som realisering av `runtime_package`,
- Custom GPT ZIP som realisering av `runtime_package`,
- Claude Projects ZIP som realisering av `runtime_package`,
- OpenCode ZIP som realisering av `runtime_package`,
- delivery manifest med koppling till canonical artifact-id,
- SHA-256-checksummor.

### `scripts/validate_distributions.py`

Validerar de byggda Chat-, Custom GPT-, Claude- och OpenCode-distributionerna.

## Lokal användning

```bash
python scripts/build_distributions.py --project-root . --version 0.0.0-dev
python scripts/validate_distributions.py --project-root .
```

## Determinism

ZIP-paketeringen använder:

- stabil filordning,
- fast ZIP-timestamp,
- normaliserade filrättigheter.

Det gör att samma input och version kan ge samma ZIP-innehåll.

## Projekt-ZIP

Projekt-ZIP exkluderar:

- `build/`,
- `dist/`,
- `.git/`,
- caches.

Detta gör projekt-ZIP:en lämplig som den löpande arbetsprodukten.

## Chat ZIP

Buildsystemet skapar en runtime med:

- `START-HERE.md`,
- `VERSION`,
- `MANIFEST.json`,
- `assistant/instructions.md`,
- runtime policies,
- canonical Knowledge,
- schemas,
- scripts,
- templates.

Utvecklingsmaterial följer inte med som egen utvecklingsstruktur.

## Custom GPT ZIP

Buildsystemet skapar:

- `README.md`,
- `builder/instructions.md`,
- `builder/conversation-starters.md`,
- `builder/capabilities.md`,
- `builder/knowledge-package/`,
- `COMPATIBILITY.md`,
- `VERSION`,
- `MANIFEST.json`.

## Nuvarande avgränsning

Detta är första buildimplementationen.

Buildsystemet stöder även GitHub Actions som standard för nya projekt: CI vid push/PR och releasebygge vid publicerad GitHub Release. Releaseversion härleds från release-taggen. Avancerad capability-paritetsanalys kan fortfarande förfinas vidare.

Toolchainen är avsiktligt byggd så att dessa delar kan läggas ovanpå samma kärna.


## Claude Projects ZIP

Buildsystemet skapar:

- `README.md`,
- `project/instructions.md`,
- `project/runtime-contract.json`,
- `project/knowledge/`,
- `VERSION`,
- `MANIFEST.json`.

Distributionen är avsedd för vanlig Claude Projects-användning och använder inte `CLAUDE.md` eller andra Claude Code-specifika konventioner.


## OpenCode ZIP

Buildsystemet skapar en basruntime med:

- `AGENTS.md`,
- `.opencode/runtime-contract.json`,
- `knowledge/`,
- `README.md`,
- `VERSION`,
- `MANIFEST.json`.

Skills och explicit tool-integration läggs på i efterföljande steg.


## Deklarativt runtime-targetregister

Runtime-distributioner deklareras under `build_system.runtime_targets` i `gpt-project.yaml`.

Varje target anger:

- `runtime_id`,
- `runtime_key`,
- `builder`,
- `artifact_type`,
- `filename_pattern`.

`build_distributions.py` itererar registret i stället för att ha en separat hårdkodad buildgren för varje runtime.

Standardtargets hämtas från `build_system.targets`. CLI-flaggan `--targets` kan fortfarande användas för en delmängd.

En ny runtime kräver fortfarande en konkret builderimplementation, men inte ändringar i huvudloopen, direct build eller standard-CI-kommandot.

Delivery manifest härleder också runtime artifact-typ från samma register, så targetdefinitionen är gemensam källa för både build och leveransmetadata.
