# Säker migrering av äldre GPT-projekt

Migrationsflödet ska fungera med en enkel instruktion som "Uppgradera denna GPT". Användaren behöver inte välja runtime, kontrakt eller CLI-flaggor. GPT Byggaren inventerar materialet och rekommenderar nästa steg.

## Kopierande migrering

```bash
python scripts/migrate_legacy_copy.py --source old-project.zip --destination upgraded-project
```

Även kataloger stöds. Destinationen måste vara ny och separat från källan. Ursprungligt material lämnas orört. `MIGRATION-REPORT.json` beskriver utförda förändringar, kvarstående osäkerheter och om underlaget går att migrera automatiskt.

Om `gpt-project.yaml` saknas, exempelvis i en gammal distributions-ZIP, bevaras materialet men automatisk migrering blockeras och kräver inventering. Verktyget uppfinner inte canonical metadata.

För tillfället normaliseras existerande kontrakt genom det etablerade `migrate_legacy_project.py`. Detta **aktiverar inte automatiskt nya runtime-adapters** och konverterar ännu inte Builder-exporter eller distributioner utan projektkontrakt till fullständiga nya projekt. Nästa utvecklingssteg behöver komplettera versionsanpassning av runtime-register, rapportering av Custom GPT-avveckling och fullständig runtimeanalys.

### Säkerhetsregler

- Skriv aldrig över befintlig destination.
- Bevara källprojektet och originalets domäninstruktioner och kunskapsfiler.
- Avvisa ZIP-traversal och symboliska länkar.
- Dokumentera ofullständiga källor och osäkra tolkningar i rapporten.
- Följ upp med lint, schema-/paritetsvalidering och byggtester innan en uppgraderad distribution kan rekommenderas för release.

De äldre in-place-kommandona kvarstår för bakåtkompatibilitet men är inte rekommenderad standard för användarstyrd uppgradering.

## Äldre Custom GPT-konfigurationer

Om ett äldre projekt innehåller en aktiv `runtime.custom_gpt` behålls hela den historiska konfigurationen, men dess `enabled` sätts till `false` i **kopian**. Aktiva Custom GPT-build targets, parityregisterposter och direkta releaseartefakter tas bort från kopians konfiguration. Övriga distributioner påverkas inte. Rapportfältet `custom_gpt_retirement` redovisar ändringen och markerar uttryckligen att automatisk Plugin-konvertering **inte** har genomförts. Källprojektet förblir orört.

## Inventering av distributions-ZIP utan projektkontrakt

När `gpt-project.yaml` saknas identifieras kända paketlayouter: Chat ZIP, OpenAI Plugin, Custom GPT Builder-material, Claude Projects och OpenCode. Rapporten redovisar detekterade format, indikatorfiler, antal identifierade kunskapsfiler och osäkerhet. Vid flera träffar anges `ambiguous` och ingen automatisk rekonstruktion görs.

Innehållet bevaras i kopian. Avsaknad av canonical projektkontrakt och auktoritativ projektstatus markeras `review_required`; det ska inte tolkas som en färdig uppgradering till senaste arkitektur.

## Återställd instruktion för granskning

När en äldre distributions-ZIP entydigt innehåller instruktioner från Chat ZIP, Custom GPT, Claude Projects eller OpenCode kan ett **exakt innehållskopierat** instruktionsutkast placeras i `reconstructed-canonical/instructions.md`. Ursprungsfilen anges i `reconstructed-canonical/RECOVERY.json`. Resultatet är uttryckligen **inte ett verifierat canonical projekt**, skapar inte `gpt-project.yaml` och är inte releaseklart. Komprimerade Builder-instruktioner kan sakna delar av originalets beteende; Knowledge och tool-beroenden måste bedömas före konvertering. Plugin ZIP med flera skills saknar ofta en entydig sammanhängande instruktion och markeras därför för granskning i stället för att sammanfogas på måfå.

## Evidensbaserad beroendeinventering

`MIGRATION-REPORT.json` innehåller `dependency_inventory` med återfunna Knowledge-/referens-/asset-filer, tänkbara skriptverktyg och integrationsmanifest (inklusive historiska `mcp.json`). Detta är en inventering av **källmaterial**, inte ett beslut att aktivera externa verktyg. `tools_verified=false` och `knowledge_completeness_verified=false` gäller tills faktisk funktion och fullständighet har verifierats. Befintlig `mcp.json` i en äldre käll-ZIP får bevaras i den isolerade migrationskopian för spårbarhet men får inte kopieras till en ny plugin-distribution.

## Engine- och Plugin-reparation vid migrering

Migrationskopian rapporterar nu `engine_migration` i `MIGRATION-REPORT.json` med
`engine_required`, `engine_status`, `plugin_repair_status`,
`runtime_parity_status`, kandidatskript och kvarstående åtgärder.
För en textbaserad GPT utan exekverbara resurser ska Engine inte aktiveras.
Python-filer är **kandidater**, inte bevis för att Plugin behöver Engine:
byggskript, testskript och lokal körkod måste särskiljas före aktivering.

För ett gammalt Plugin-kontrakt måste den migrerade GPT:n få uppdaterad
`runtime.plugin`, verifierade Skill-resurser och en ombyggnad genom den aktuella
kanoniska byggaren. Om dess Plugin-förmågor kräver verklig lokal exekvering
måste `engine.resources`, `engine.selftest`, versionsbunden Engine ZIP och
instruktion om nedladdning/bifogning etableras. Ingen selftest får fabriceras,
och gamla Plugin-resurser får inte antas fungera utan värdmiljötest.

Den säkra kopieringsmigreringen installerar **inte** automatiskt en ny motor
över äldre projektspecifika filer och intygar inte att fem runtime-versioner
är byggbara. Det ska göras först efter schema-/resurskontroll och följas av
kanonisk lint, fem distributionsbyggen, Engine-integritetskontroll (om aktiv),
och värdmiljöspecifik Plugin-acceptans. Alla dessa statusar förblir
`unverified`/icke releaseklara tills kontrollen verkligen utförts.

### Valfri bygguppgradering i migrationskopian

Om projektprofilen redan har kompletta fem canonical runtime-mål kan den
aktuella distributionsmotorn installeras och distributionsbygget provas i den
separata migrationskopian:

```bash
python scripts/migrate_legacy_copy.py --source old-project.zip \\
  --destination upgraded-project --upgrade-build --version 0.1.0
```

Om projektprofilen är ofullständig får `canonical_build_upgrade.status=blocked`
med ett konkret installations- eller byggfel; verktyget uppfinner inte
runtime-kontrakt. Om bygget lyckas får rapporten
`built_pending_host_acceptance`: det är **inte** ett verifierat
värdmiljötest eller ett releasegodkännande. Originalprojektet ändras aldrig.

När `--upgrade-build` används får en modern Plugin med befintlig, entydig
canonical instruktion en enkel Skill-deklaration om sådan saknas. Befintliga
Skills bevaras. Om `tools.tools` deklarerar nödvändiga Python-skript och
`scripts/selftest.py` redan finns kan `engine` deklareras med dessa
befintliga filer. Utan dokumenterat självtest aktiveras ingen Engine; en
`review_required`-status kvarstår. En lyckad arkivbyggnad verifierar Plugin
Skills och Engine-artefakten strukturellt, men är ännu inte ett funktionellt
värdmiljötest och innebär inte releasegodkännande.

## Stegvis migrationsupplevelse och hygiengranskning

Migrationsrapporten innehåller `migration_steps` (inventering, modell,
Engine, distributioner, dokumentationshygien och slutverifiering), `next_step`
och `project_hygiene`. Stegstatusen är uttryckligt skiljd från
värdmiljöverifiering. Dessa strukturer kan visas som intelligent UI där värden
stöder det, och läsbara textsteg annars.

Hygiengranskningen identifierar saknade huvudokument, möjliga inaktuella
GPT Byggaren-versioner, historiska CI-numren i STATUS och äldre
valideringsskript som kandidater till borttagning. Den raderar **inga** filer
och ändrar inte dokumentationen automatiskt: först ska anrop, funktioner,
historik och tester jämföras med ersättningen. Migrationsassistenten ska
sedan genomföra dokumentationsuppdatering och säker städning som del av
arbetsflödet, inte invänta en extra användaruppmaning. Slutligt
merge-/releasebeslut kräver reviderad dokumentation och verifierad CI.

En specifik versionslåst GPT Byggaren-release som byggberoende i ett
migrerat projekts GitHub Actions är ett godtagbart upplägg. Ange både
projektversion och motorversion så att leveransen kan reproduceras.
