# Offline-smoketest av rekonstruerade distributioner

Kör `python scripts/smoke_test_reconstructed_distributions.py --project-root PROJECT --chat-zip CHAT.zip --claude-zip CLAUDE.zip --opencode-zip OPENCODE.zip --plugin-zip PLUGIN.zip` mot redan byggda ZIP-filer.

Verktyget kontrollerar arkivens grundstruktur, viktiga runtime-filer, checksummor i manifest, instruktionernas byteidentitet för Chat/Claude/OpenCode samt att Plugin inte innehåller `mcp.json` ens i underkataloger. Plugin kontrolleras som skills-first med minst ett `SKILL.md`, men adaptersemantik verifieras inte automatiskt. En ZIP kan lämnas bort från kommandot; en sådan runtime har **inte** testats.

Det här är en **offline-förkontroll**, inte ett verktyg som bygger eller attesterar färdig runtimeparitet. Särskilt krävs fortfarande verklig funktionell provning av de fyra runtime-miljöerna och deras förmågor, verktyg och Knowledge. Verktyget ändrar aldrig `release_ready`, kringgår inte build-spärren och gör inga antaganden om externt installerade MCP-tjänster.
