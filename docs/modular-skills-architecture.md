# Modulära skills som canonical arkitektur

## Rekommendation

**Ja till mindre, sammanhängande skills – men inte i stället för alla instruktioner.** GPT Byggarens kärna ska fortsatt vara direkt läsbar och robust även om en runtime inte kan hitta eller dynamiskt aktivera en skill.

Använd en tvådelad källmodell:

1. **Kort canonical kärninstruktion:** uppdrag, säkerhetsgränser, idé-först-flöde, övergång mellan steg, status- och granskningskrav, fallback när skills eller verktyg saknas.
2. **Små canonical skills:** självständiga förmågor med tydlig avgränsning, till exempel idéanalys, projektinventering, migrationsanalys, arkitektur, kontrakt, byggning, paritet och leverans. En skill beskriver när den ska användas, nödvändiga resurser, förväntade resultat och verifiering. Separata resurser och skript hör till rätt skill.

Canonical projektmodell ska beskriva förmågorna **plattformsneutralt**. Runtime-adaptrarna avgör hur de paketeras:

| Runtime | Rekommenderad kompilering |
| --- | --- |
| OpenCode | Separata skills och verktyg, där agenten kan ladda förmågor vid behov |
| ChatGPT Plugin | Skills-first distribution med individuella SKILL.md, references och scripts utan mcp.json |
| Chat ZIP | Behåll kort kärna, index och alla nödvändiga skill-/resursfiler; tydligt navigeringsflöde och textfallback när dynamisk laddning saknas |
| Claude | Kompilera kärninstruktion och hänvisningar till separata kunskaps-/skillmoduler inom stödd Claude Project-layout; anta inte identisk runtimeaktivering |

**Kritiska regler får inte kräva en specifik skill som enda källa** om det skulle försvaga en annan distribution. Kärnan ska fungera ensam för grundbeteende, och resten ska ge fördjupning. Kontrollera funktionell paritet per runtime, inte bara att samma Markdown-filer har kopierats.

## Migrering från långa instruktioner

För äldre projekt analyseras hela texten först. En AI kan föreslå skillgränser, men varje skillförslag måste ha källevidens och en jämförelse med ursprunglig funktion. Ingen automatisk uppdelning från filnamn eller rubriker accepteras som sanningskälla. Ett olöst förmågeberoende håller projektet i review_required och förhindrar distribution.

## Nästa implementation

Implementera canonical skillmodellens semantiska definitioner och en kompileringsstrategi med gemensam regressionssvit för de fyra distributionerna. Säkerställ kort kärna och explicit fallback i Chat ZIP och Claude, och enskilda SKILL.md i OpenCode och Plugin. Detta arbete ska ske i en separat PR efter att den generella analysprojektionen validerats.
