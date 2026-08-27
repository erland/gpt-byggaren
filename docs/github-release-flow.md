# GitHub Actions-releaseflöde – GPT Byggaren

En publicerad GitHub Release triggar `.github/workflows/release.yml`. Release-taggen är versionskälla; `v1.4.2` ger distributionsversion `1.4.2`. Workflowen validerar taggen, kör fokuserade tester, bygger med samma scripts som lokal direktbyggnad, validerar distributionerna och laddar upp projekt-ZIP, Chat ZIP, Custom GPT ZIP, checksummor och leveransmanifest till samma release. Ingen manuell versionsuppdatering ska behövas inför release.
