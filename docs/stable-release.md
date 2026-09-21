# Stabil release – GPT Byggaren 1.0.0

## Status

GPT Byggaren är nu markerad som stabil release:

```text
v1.0.0
```

## Stabilitetskrav

Före stabil release verifieras:

- projektkontrakt,
- projektstatus,
- arkitekturmodell,
- referensprofiler,
- referensprojektregressioner,
- blank-idea E2E-kontrakt,
- Python compile,
- project hygiene,
- Custom GPT-instruktionsgräns,
- Custom GPT-Knowledge-gräns,
- stabil distributionspaketering,
- checksummor och delivery manifest.

## Distributionsartefakter

Stabil release bygger:

```text
gpt-byggaren-project-1.0.0.zip
gpt-byggaren-chat-1.0.0.zip
gpt-byggaren-custom-gpt-1.0.0.zip
gpt-byggaren-claude-1.0.0.zip
gpt-byggaren-opencode-1.0.0.zip
gpt-byggaren-plugin-1.0.0.zip
gpt-byggaren-SHA256SUMS-1.0.0.txt
gpt-byggaren-DELIVERY-MANIFEST-1.0.0.json
gpt-byggaren-RELEASE-READINESS-1.0.0.json
gpt-byggaren-RELEASE-NOTES-1.0.0.md
```

## Versionskälla i GitHub

Vid GitHub-release ska versionen fortfarande härledas från release-taggen.

För denna stabila version:

```text
v1.0.0 → 1.0.0
```

Ingen separat manuell versionssynkning ska krävas i releaseflödet.

## Efter release

Projektet går över från utvecklingsplan 1–30 till normalt underhåll.

Nya ändringar ska hanteras som:

- korrigeringssteg,
- förbättringssteg,
- ny minor/patch release,
- vid större förändringar: ny projektplan.

## Resultat

Release v1.0.0 är stabil när samtliga blockerande gates passerar och de slutliga distributionerna kan reproduceras deterministiskt.


## Deklarativ releaseverifiering

Release-workflowen använder `verify_distribution_outputs.py` för att härleda hela filuppsättningen från `build_system.targets` och `build_system.runtime_targets`.

Det innebär att en aktiverad OpenAI Plugin-runtime automatiskt byggs med release-taggen som version, valideras tillsammans med övriga distributioner, krävs av releaseverifieringen, inkluderas i filuppsättningen från `--print-files` och laddas upp med samma `gh release upload`-kommando som övriga artefakter.

Plugin-filnamnet ska därför inte hårdkodas i workflowen.
