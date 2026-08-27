# CI för commits och pull requests

CI ska fånga fel före release och använda samma buildkärna som direktbyggnad och GitHub Release.

## Trigger
- push till huvud-, work-, feature- och fix-brancher
- pull requests
- manuell `workflow_dispatch`

## Kontroller
1. YAML/JSON-parse
2. tester
3. distributionsbuild med `0.0.0-ci`
4. distributionsvalidering
5. kontroll av förväntade artefakter
6. project hygiene
7. uppladdning av CI-artefakter

CI har endast `contents: read`. Release-workflowen behåller separat skrivbehörighet.
