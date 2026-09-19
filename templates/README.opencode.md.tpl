# {{GPT_NAME}} – OpenCode-distribution

Detta paket är en basruntime för OpenCode.

## Användning

1. Packa upp ZIP-filen som ett projekt/workspace.
2. Öppna projektet i OpenCode.
3. OpenCode läser root `AGENTS.md` som projektinstruktion.
4. `.opencode/runtime-contract.json` dokumenterar hur adaptern realiserar canonical kontrakt.
5. `knowledge/` innehåller portabelt referensmaterial som agenten kan läsa vid behov.

## Avgränsning i denna version

- Skills under `.opencode/skills/` läggs till i nästa steg.
- Explicit tool-integration läggs till efter skills-steget.
- `CLAUDE.md` används inte; OpenCode V2 använder `AGENTS.md` för projektinstruktioner.

## Version

{{VERSION}}
