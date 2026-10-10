# Mappning av äldre OpenAI Plugin-kontrakt

Den bifogade Marknadskartläggaren använder `runtime.openai_plugin` med `skills_first`, en explicit `skills/marknadskartlaggaren/SKILL.md` och runtimeberoenden för webb, filer, kodkörning och tillstånd. Nyare GPT Byggaren använder `runtime.plugin` och ett separat, modernare adapterkontrakt.

Efter `migrate_legacy_copy.py` skapas nu `reconstructed-canonical/plugin-migration-plan.json` för sådana kompletta äldre projekt. Planen dokumenterar källan, kontrollerar om den deklarerade skill-filen finns, inventerar hostberoenden och ger ett avaktiverat förslag för `runtime.plugin`.

**Ingen automatisk aktivering eller release:** förslaget skrivs separat och äldre konfiguration bevaras. Den gamla `openai_plugin.enabled=true` representerar bara ett historiskt kontrakt, inte bevis för modern kompatibilitet. Planen måste kompletteras med canonical skills, resursmappning, faktiska verktygs-/hostkontroller, nya templates, byggning och paritetstest. Plugin ZIP får aldrig innehålla `mcp.json` (även i underkataloger).

Regressionsfixturen bygger på det verkliga äldre projektets konfiguration. Originalfilen ingår inte i versionshanteringen.
