# Verifiering av modulär migrering

När användaren begär modulära Skills ska en migration inte räknas som aktiverad enbart för att Skill-mappar skapats. Projektprofilen måste ange `instructions.mode: modular_skills`, `instructions.core` och separata beteendekällor per Skill.

Verktyget `migrate_legacy_copy.py --activate-modular-skills` använder granskad `canonical/assembly.json` och bevarar den ursprungliga instruktionen. Det stöder både avsnittsvisa sökvägar och formatet med `sources` och `sections` som Novellskaparen v1.6.16 använder. Ändringar av avsnittsordning kan påverka beteendet även vid exakt källtäckning och kräver granskning.

Med `--upgrade-build` granskas även skapade ZIP-arkiv. Chat, Claude Projects och OpenCode ska innehålla det fullständiga sammanställda beteendet. Plugin och Claude Skills ska bära kärnan och varje Skills egen specialisering, utan andra Skills beteenden. Resultatet redovisas i `MIGRATION-REPORT.json` under `modular_distribution_verification`.

En godkänd arkivkontroll motsvarar inte faktisk runtimeparitet. Releaseberedskap kräver dessutom godkänd CI, funktionsprov och slutlig dokumentationsgranskning.
