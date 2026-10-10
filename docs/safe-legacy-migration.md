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
