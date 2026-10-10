# Paritetsevidens för rekonstruerade GPT-projekt

Kör `python scripts/collect_reconstruction_parity.py --project-root PROJECT` på den separata, rekonstruerade projektkopian.

Kontrollen jämför bytes i den återställda ursprungsinstruktionen med canonical instruktion. Om det finns redan byggda runtime-kataloger inspekteras instruktionerna för Chat ZIP, Claude, OpenCode och Plugin. Saknad byggkatalog redovisas som `not_tested`, inte som godkänt. Den inventerar också kvarvarande Knowledge-filer med SHA-256 och visar upptäckta verktygs- och integrationskandidater som ännu är obevisade.

En byte-jämförelse är bara **filevidens**, inte beteendeparitet. Skillnader i adapterformat kan vara legitima och måste analyseras separat; exempelvis behöver ett plugin SKILL.md inte vara identiskt med canonical instruktion. Projektets `release_ready` ändras inte och verktyget utfärdar aldrig `runtime_parity_verified`.

Nästa steg är att göra faktiska, säkra distributionstester med representativa GPT-ZIP och verifiera adaptersemantik, verktygsbehörigheter samt Knowledge-fullständighet innan paritet kan attestera byggning. Verktyget är avsiktligt observationsbaserat och kringgår inte byggspärren från PR #26.
