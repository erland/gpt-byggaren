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


## Deklarativ artefaktverifiering

CI använder `scripts/verify_distribution_outputs.py` för att härleda förväntade filer från `build_system.targets` och `build_system.runtime_targets`.

När en ny runtime läggs till i registret behöver CI därför inte kompletteras med en ny hårdkodad filkontroll.


## OpenAI Plugin

När `runtime.plugin.enabled: true` och `plugin` finns i `build_system.targets` omfattas Plugin av samma CI-kedja som övriga peer runtimes:

1. distributionen byggs av den registrerade runtime-buildern,
2. `validate_distributions.py` validerar Plugin-layout och skills,
3. `verify_distribution_outputs.py` kräver Plugin-ZIP:en,
4. `dist/*.zip` gör att Plugin-ZIP:en laddas upp som CI-artefakt.

CI ska inte hårdkoda projektnamn eller Plugin-filnamn. Runtime-registret är auktoritativt.
