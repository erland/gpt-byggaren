# Dogfood – GPT Byggaren som OpenAI Plugin

## Syfte

Detta dokument verifierar att GPT Byggaren själv kan byggas med den OpenAI Plugin-runtime som projektet genererar.

Dogfood-testet ska skilja mellan två frågor:

1. Kan GPT Byggaren byggas och distribueras som Plugin?
2. Är Plugin v1 funktionellt equivalent med GPT Byggarens övriga runtimes?

Svaret är **ja** på den första frågan och **nej** på den andra.

## Byggbarhet

GPT Byggaren har en aktiverad `openai_plugin`-target och bygger:

```text
gpt-byggaren-plugin-<version>.zip
```

Distributionen innehåller minst:

- `plugin.json`
- `README.md`
- `VERSION`
- `MANIFEST.json`
- `runtime-contract.json`
- `skills/gpt-project-workflow/SKILL.md`
- skill-referenser för planering, resume och next-step-flöde

Build, validering, output-verifiering och deterministisk ZIP testas i ordinarie testsvit.

## Canonical funktionalitet

GPT Byggaren kräver bland annat:

- persistent workspace,
- persistent state i `project-status.yaml`,
- filesystem read/write,
- flera obligatoriska script-tools för lint, hygiene, nästa steg, build och distributionsvalidering.

Plugin v1 paketerar skill-resurser och runtime-relevanta scripts. Dessa script-resurser kan
användas direkt när host-runtimen erbjuder kompatibel code execution, så avsaknad av MCP
innebär inte automatiskt att scripts saknar exekveringsmöjlighet. Plugin v1 genererar däremot
inte ett garanterat, explicit MCP-tool-gränssnitt.

## Paritetsbedömning

För GPT Byggaren själv är Plugin v1 därför en **reducerad peer runtime**:

- **behavior:** kärninstruktionen kan projiceras genom skillen,
- **artifact:** pluginpaketet kan byggas och distribueras,
- **workspace/state:** reducerad eftersom host-runtimen måste tillhandahålla persistent workspace/state,
- **tools:** hostberoende; script-resurser kan vara fullt användbara med kompatibel code execution, men GPT Byggaren kräver flera scripts med filesystem/workspace-beroenden och Plugin v1 garanterar inte den exekveringsmiljön eller ett MCP-tool-gränssnitt,
- **capabilities:** vissa capabilities beror på host-runtimen.

Det är korrekt att bygga Plugin-artefakten som ett distributionsmål, men den får inte beskrivas som fullständigt equivalent för GPT Byggaren v1.

## Dogfood-regel

Framtida ändringar ska bevara följande:

- GPT Byggaren ska fortsatt kunna bygga sin egen Plugin-ZIP.
- Den genererade skillen ska innehålla canonical GPT Byggaren-beteende.
- De deklarerade skill-referenserna ska följa med.
- Runtime snapshot ska uttryckligen redovisa skillnaden mellan paketerade script-resurser, hostens code execution och ett garanterat MCP-tool-gränssnitt.
- Tester får inte anta att avsaknad av MCP automatiskt gör paketerade scripts oanvändbara.
- Tester får samtidigt inte anta att varje host kan köra scripts med projektets dependency-, filesystem- och workspacekrav.

## Slutsats

Dogfood-resultatet är godkänt för Plugin v1 när distributionen är reproducerbar och självbärande som skills-first paket samtidigt som reducerad funktionalitet redovisas öppet.
