# GPT-linter – GPT Byggaren

## Syfte
GPT-lintern hittar statiska projektfel före full build och beteendeevaluering.

## Severity
- `error` – blockerande
- `warning` – bör bedömas
- `info` – observation

## Kontroller
- projektkontrakt och deklarerade explicita paths
- canonical instruktion
- Knowledge-struktur och Custom GPT-gränser
- project hygiene
- testmanifest och evalschemas
- CI- och release-workflows
- enkla dupliceringsindikatorer

## Output
Lintern stöder både läsbar text och JSON.

## CI
Rekommenderad ordning:

```text
parse → lint → tests → build → distribution validation
```

Lint-errors blockerar CI. Warnings blockerar normalt inte.

## Auto-fix
Steg 19 inför inte aggressiv auto-fix. Osäkra filer raderas aldrig bara utifrån namn.
