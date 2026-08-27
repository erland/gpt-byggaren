# GitHub release policy

- Publicerad GitHub Release triggar bygget.
- `github.event.release.tag_name` är versionskälla.
- Samma build- och valideringsscript används lokalt och i GitHub Actions.
- Tester, build och validering måste passera före uppladdning.
- Artefakter laddas upp till releasen som triggade workflowen.
