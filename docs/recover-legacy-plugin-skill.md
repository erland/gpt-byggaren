# Rekonstruera saknad äldre Plugin-skill

Den bifogade Marknadskartläggaren deklarerar `skills/marknadskartlaggaren/SKILL.md`, men filen saknas. Kör `python scripts/recover_legacy_plugin_skill.py --project-root PROJECT` i **en säker migrerad kopia** av projektet.

Verktyget läser den i projektkontraktet angivna canonical instruktionen och skapar ett fristående förslag under `reconstructed-canonical/plugin-skill-candidate/skills/<namn>/SKILL.md`. Instruktionstexten behålls ordagrant som innehåll i förslaget, och en SHA-256-spårbarhetsrapport skrivs till `RECOVERY.json`.

Äldre skill-entrypoint, originalinstruktioner, projektkontrakt och andra distributioner ändras inte. Kandidaten kräver fortsatt granskning av canonical beteende, Knowledge och hostberoenden. Den placeras avsiktligt inte i ordinarie skill-katalog eller aktiveras för byggning. Särskilt `runtime.openai_plugin.enabled` får inte misstas för en verifierad modern `runtime.plugin`-aktivering.

Nästa steg är att validera en modern Plugin-adapter från källmaterialet med ordinarie Plugin-byggare och därefter verifiera dess funktionalitet, resurser och mobilimport. `mcp.json` får aldrig följa med Plugin-ZIP.
