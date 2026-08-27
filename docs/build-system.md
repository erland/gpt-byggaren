# Buildsystem – GPT Byggaren

## Syfte

Steg 14 introducerar den första körbara toolchainen för att bygga GPT-projektets artefakter.

## Script

### `scripts/build_distributions.py`

Bygger:

- projekt-ZIP,
- Chat ZIP,
- Custom GPT ZIP,
- manifest,
- SHA-256-checksummor.

### `scripts/validate_distributions.py`

Validerar de byggda Chat- och Custom GPT-distributionerna.

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

Följande kommer i senare steg:

- riktig instruktionskomprimering när canonical instruktion överskrider gränsen,
- avancerad Knowledge-konsolidering,
- full automatisk capability-paritetsanalys,
- GitHub Actions,
- release-tagghantering,
- mer fullständig CI.

Toolchainen är avsiktligt byggd så att dessa delar kan läggas ovanpå samma kärna.
