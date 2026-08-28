# GitHub release policy

## Standard

GitHub-stöd är aktiverat som standard för nya GPT-projekt om användaren inte uttryckligen anger att projektet ska vara lokalt eller GitHub-fritt.

Ett GitHub-redo projekt ska innehålla:

- `README.md` i projektroten,
- `.github/workflows/ci.yml`,
- `.github/workflows/release.yml`.

## CI

CI ska normalt köras vid push, pull request och manuell dispatch och minst:

- validera projektets strukturerade filer,
- köra linter,
- köra tester och relevanta kontraktsvalideringar,
- bygga projekt-ZIP, Chat ZIP och Custom GPT ZIP,
- validera distributionerna.

## Release

Release-workflow ska triggas av publicerad GitHub Release.

Versionsnumret ska härledas från `github.event.release.tag_name`; det ska inte behöva underhållas manuellt i projektfiler.

Release-workflow ska normalt:

1. validera release-taggen,
2. köra relevanta tester,
3. bygga projekt-ZIP, Chat ZIP och Custom GPT ZIP,
4. validera distributionerna,
5. bifoga artefakter, checksums och delivery manifest till GitHub Release.

## Opt-out

GitHub-stödet får stängas av när:

- användaren uttryckligen vill ha ett lokalt projekt,
- GitHub inte ska användas,
- eller en annan versions-/releaseplattform uttryckligen valts.

Fråga normalt inte användaren om GitHub Actions ska finnas; använd standarden när inget annat anges.
