# Rekonstruerat projektutkast

Vid säker migrering av en äldre distributions-ZIP utan `gpt-project.yaml` identifierar GPT Byggaren kända format och återställer ett exakt instruktionsexemplar där källan är entydig.

Utöver `RECOVERY.json` skrivs nu `reconstructed-canonical/project-draft.json` med:
- källfil och sökväg till återställda instruktioner,
- kandidater till Knowledge, skriptverktyg och integrationsmanifest,
- explicit markerade verifieringsluckor,
- inaktiverade runtime-mål och tydliga granskningssteg.

Utkastet är **inte** ett fullständigt `gpt-project.yaml`. Ingen ny runtime aktiveras, och resultatet är aldrig releaseklart automatiskt. Det är avsiktligt: en äldre distribution kan vara komprimerad eller sakna kritiska beroenden. Originalet skrivs inte över.

Användarupplevelsen ska förbli: **”Uppgradera denna GPT”**. GPT Byggaren ska själv utföra inventering och rekonstruktion och endast be om verkligt nödvändiga verksamhetsbeslut när materialet inte räcker. Fortsatt arbete ska omvandla *verifierat* utkast till canonical kontrakt samt validera funktionell paritet i moderna distributioner.
