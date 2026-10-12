# Kanoniska Skills – modulär källa

För nya GPT-projekt kan GPT Byggaren välja `instructions.mode: modular_skills`.
Detta är ett opt-in-kontrakt. Befintliga projekt med en enda kanonisk instruktion
fortsätter byggas som tidigare.

## Rekommenderad struktur

```text
canonical/
  core.md
  skills/
    write/behavior.md
    revise/behavior.md
```

`gpt-project.yaml`:

```yaml
instructions:
  mode: modular_skills
  canonical: canonical/core.md # bakåtkompatibelt för kontraktsverktyg
  core: canonical/core.md
skills:
  definitions:
    - id: write
      name: write
      description: Skriv en ny berättelse
      source: canonical/skills/write/behavior.md
      references: []
      assets: []
      scripts: []
    - id: revise
      name: revise
      description: Revidera en berättelse
      source: canonical/skills/revise/behavior.md
      references: []
      assets: []
      scripts: []
```

`core.md` ska endast innehålla gemensamma regler. Varje Skill-källa innehåller
det specialiserade beteendet. Skill-metadata ligger i projektmodellen; Skillens
`behavior.md` ska vara en Markdown-text utan en andra YAML-frontmatter.

## Byggprojektion

- Chat ZIP och Claude Projects: kärna + alla Skills som en komplett instruktion.
- OpenAI Plugin och Claude Skills: en Skill per deklaration med gemensam kärna
  och **bara den Skillens** specialbeteende.
- OpenCode: sammanhängande AGENTS.md samt separat Skills. Värden kan ladda Skills
  när uppgiften kräver det; instruktionerna måste vara kompletta även om dynamisk
  Skill-laddning inte kan förutsättas.

Den kanoniska Skill-källan ersätts inte av genererade distributions-SKILL.md.
En migration från en äldre monolitisk instruktion kräver en genomgång av
ursprungliga ansvar, kopplingar och informationsförlust före godkännande.
`scripts/lib/skill_architecture_analysis.py` tar fram konservativa kandidater
men gör inte automatiskt en semantisk uppdelning eller godkänner funktionell paritet.

## Verifiering

Verifiera att varje avsnitt i legacy-källan återfinns i core eller rätt Skill,
att olika Skills inte får varandras specialbeteende och att samtliga fem
distributioner fortfarande byggs och kan användas enligt sina kontrakt.

## Beslutsregel: separation och duplicering

Välj det minsta antal Skills som ger tydliga självständiga ansvarsområden, aktiveringsvillkor och arbetsflöden. Rubriker och arbetslägen är kandidater, inte automatiskt egna Skills. Motivera varje föreslagen Skill utifrån sammanhållning och låg koppling.

**Kanonisk källduplicering** är upprepade beteenderegler i core och i flera specialiserade källor, eller i två specialiserade källor. Den ska i regel elimineras genom att gemensamma regler ligger i `core.md`.

**Genererad distributionsduplicering** är när byggmotorn kopierar samma gemensamma kärna till flera självständiga distribuerade Skills. Det är tillåtet och ofta önskvärt för portabilitet. En hög textlikhet mellan färdiga `SKILL.md` är inte i sig ett fel och ska inte användas som gränsvärde för att slå ihop Skills.

Exempel: en skrivassistent kan motivera separata Skills för ny text, fortsättning och revision även om gemensamma språk-, kvalitets- och målgruppsregler utgör merparten av varje genererat paket. Bedöm skillnader i arbetsflöde och aktivering, inte procenten gemensam text efter release.
