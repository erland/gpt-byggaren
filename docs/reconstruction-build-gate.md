# Distributionsbygge efter rekonstruktion

En rekonstruerad GPT kan genomgå schema- och projektlint, men det är inte likvärdigt med verifierad funktionell paritet i Chat ZIP, Plugin, Claude och OpenCode.

Distributionsbyggaren och distributionsvalideraren blockerar därför nu projekt med `reconstruction.release_ready != true` eller annat rekonstruktionsläge än `runtime_parity_verified`. Spärren utförs innan någon `build/`- eller `dist/`-katalog skapas. Vanliga projekt utan rekonstruktionsmetadata hanteras oförändrat.

Dessa fält är en skyddsgrind, **inte ett automatiskt intyg**. Nästa arbete behöver en separat, reproducerbar validering av instruktionernas bevarande, Knowledge, explicit deklarerade verktyg, installerade frivilliga integrationer, adapters och faktisk runtimeparitet. Ingen status får sättas till `runtime_parity_verified` enbart för att kringgå spärren. Först efter denna evidensbaserade kontroll får distributioner byggas.

Detta steg producerar ännu inga rekonstruerade distributioner och är inte ett slutligt end-to-end-test i faktisk runtime.
