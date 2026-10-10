# Portabla Skills och skript – första implementationen (PR #37)

Den canonical källmodellen består av en **obligatorisk kärninstruktion** och separata skillmoduler. Varje modul har en egen `SKILL.md`, frivilliga `references` och `assets`, samt deklarerade skript. En skriptdeklaration måste ange körmotor, externa beroenden, krav på nätverk/filsystem/kodkörning/persistent state och fallback när exekvering inte är möjlig.

Använd `python scripts/validate_portable_skills.py --project-root PROJECT --contract portable-skills.json` för att kontrollera att alla deklarerade filer finns och ligger inom källprojektet, att varje skript har kompletta körmiljökrav och att var och en av `chat_zip`, `plugin`, `claude` och `opencode` har ett explicit fallbackförfarande.

Exempel på en modul i `portable-skills.json`:

```json
{
  "schema_version": 1,
  "core": "src/instructions/core.md",
  "modules": [
    {
      "id": "project-audit",
      "skill": "skills/project-audit/SKILL.md",
      "references": ["skills/project-audit/references/checklist.md"],
      "scripts": [
        {
          "path": "skills/project-audit/scripts/audit.py",
          "engine": "python",
          "dependencies": [],
          "requirements": {
            "filesystem_read": "required",
            "filesystem_write": "none",
            "network": "none",
            "code_execution": "required",
            "persistent_state": "none"
          },
          "fallback": "manual"
        }
      ]
    }
  ],
  "fallback": {
    "chat_zip": "Behåll kärninstruktionen och tillgängliga resursfiler",
    "plugin": "Behåll kärninstruktionen och blockera otillgänglig skriptkörning",
    "claude": "Använd Claude Skills när de är installerade; annars manuell kärnväg",
    "opencode": "Använd skills i stödd miljö; blockera otillgänglig skriptkörning"
  }
}
```

## Skillnad mellan miljöer

- **ChatGPT Plugin:** skillpaket med `SKILL.md`; inga `mcp.json` i ZIP, inte ens nästlade.
- **Claude:** stöd för Claude Skills med `SKILL.md` och resurser. Distribution till Claude.ai Skills/Claude Code är inte liktydig med uppladdning i Claude Projects; bygg och installation måste kontrolleras separat. Skriptexekvering kräver kompatibel host.
- **OpenCode:** separata skills med körbara verktyg när lokalt stöd och behörigheter finns.
- **Chat ZIP:** behöver en explicit text- och resursfallback; anta inte automatisk skillaktivering.

## Avsiktlig avgränsning

PR #37 inför **kontrakt och tester**, inte en automatisk uppdelning av GPT Byggarens stora instruktion och inte nya releasepaket. Att `validate_portable_skills.py` ger `review_ready` bevisar endast strukturell integritet – **inte** runtimefunktion, exekvering, semantisk likvärdighet eller distributionsparitet. Nästa steg är att dela utvalda förmågor i en granskad canonical kärna, behålla instruktionernas fulla betydelse och sedan utöka runtime-byggarna stegvis med faktiska acceptanstester.
