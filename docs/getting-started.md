# Kom igång med GPT Byggaren

## Vad GPT Byggaren gör

GPT Byggaren hjälper dig att skapa en egen GPT från idé till färdig, testad och paketerad lösning.

Du behöver inte kunna:

- YAML,
- JSON Schema,
- GitHub Actions,
- testautomatisering,
- runtime-arkitektur,
- paketering.

GPT Byggaren väljer sådant åt dig när det går att avgöra från användningsfallet.

Du behöver främst kunna beskriva **vad GPT:n ska hjälpa till med**.

---

## Så arbetar du

Det normala arbetsflödet är:

1. Beskriv vad du vill bygga.
2. GPT Byggaren analyserar behovet.
3. Du får en utvecklingsplan.
4. GPT Byggaren skapar första projekt-ZIP:en.
5. Du ber om nästa steg.
6. GPT Byggaren uppdaterar projektet och ger dig en ny ZIP.
7. När projektet är klart bygger GPT Byggaren färdiga distributioner.

---

## 1. Börja med idén

Du kan skriva enkelt.

Exempel:

```text
Jag vill skapa en GPT som hjälper mig analysera remisser
och bedöma hur de påverkar min organisation.
```

Du behöver inte skriva:

```text
Använd ZIP-first runtime, schemas och evals.
```

Sådana tekniska beslut ska GPT Byggaren normalt göra åt dig.

---

## 2. GPT Byggaren analyserar behovet

GPT Byggaren försöker förstå:

- vad GPT:n ska göra,
- vilka som ska använda den,
- vilka typer av underlag den får,
- vilket resultat den ska skapa,
- om den behöver webbsökning,
- om den behöver arbeta med filer,
- om den behöver strukturerad information,
- om scripts eller schemas behövs,
- hur avancerad testningen behöver vara,
- vilken runtime som passar bäst.

Den ska bara fråga dig om sådant som verkligen kräver ett verksamhetsbeslut.

---

## 3. Du får en utvecklingsplan

Innan projektet skapas får du normalt en nedladdningsbar Markdown-fil med utvecklingsplanen.

Planen är anpassad efter just din GPT.

Den är en riktning, inte ett låst kontrakt.

GPT Byggaren får senare:

- lägga in korrigeringssteg,
- hoppa över onödiga steg,
- dela ett steg,
- slå ihop steg,

om projektets faktiska tillstånd motiverar det.

---

## 4. Första projekt-ZIP:en

När du ber GPT Byggaren börja genomföra planen får du en komplett projekt-ZIP.

Projekt-ZIP:en innehåller bland annat:

```text
gpt-project.yaml
project-status.yaml
PROJECT.md
STATUS.md
docs/
src/
knowledge/
schemas/
scripts/
tests/
evals/
```

Du behöver normalt inte redigera dessa filer själv.

Projekt-ZIP:en är den fil du använder för fortsatt utveckling.

---

## 5. Fortsätt steg för steg

Efter varje steg kan du normalt bara skriva:

```text
Gör nästa steg och ge mig en uppdaterad zip
```

GPT Byggaren ska då:

1. läsa aktuell projektstatus,
2. avgöra vilket steg som faktiskt bör göras,
3. genomföra arbetet,
4. kontrollera projektet,
5. uppdatera status,
6. ge dig en ny komplett projekt-ZIP.

Den ska inte automatiskt anta att nästa steg alltid är föregående steg + 1.

---

## 6. Om något går fel

Om lint, test, build eller validation hittar ett problem kan GPT Byggaren lägga in ett korrigeringssteg.

Exempel:

```text
Steg 12 klart
↓
validation hittar problem
↓
korrigeringssteg
↓
regressionstest
↓
fortsätt planen
```

Detta är förväntat och betyder inte att utvecklingsplanen har misslyckats.

---

## 7. Projektstädning

GPT Byggaren håller projektet rent under arbetets gång.

Den kan automatiskt ta bort säkra artefakter som:

- caches,
- temporära filer,
- genererade build-mappar.

Misstänkt historiska filer raderas inte blint.

Git används som historik när projektet ligger i Git.

---

## 8. Fortsätta i en ny konversation

Du kan starta en ny konversation och bifoga senaste projekt-ZIP:en.

Skriv exempelvis:

```text
Fortsätt utveckla detta GPT-projekt.
```

GPT Byggaren ska då kunna läsa:

1. projektkontraktet,
2. projektstatus,
3. utvecklingsplanen,
4. relevanta projektdokument,

och fortsätta utan att du behöver återberätta hela historiken.

---

## 9. Vilka typer av ZIP finns?

Det finns tre viktiga typer.

### Projekt-ZIP

Detta är hela utvecklingsprojektet.

Använd den för:

- fortsatt utveckling,
- Git,
- GitHub,
- nya ChatGPT-konversationer.

### Chat ZIP

Detta är den primära runtime-distributionen för större GPT:er.

Du kan bifoga den i en ChatGPT-konversation och använda den som GPT-kontext.

### Custom GPT ZIP

Detta innehåller materialet för att skapa eller uppdatera en Custom GPT.

Custom GPT kan ibland ha färre funktioner än Chat ZIP eftersom plattformen har andra begränsningar.

---

## 10. Måste jag använda GitHub?

Nej.

GPT Byggaren ska kunna bygga färdiga artefakter direkt.

Du kan få:

```text
project.zip
chat.zip
custom-gpt.zip
SHA256SUMS.txt
DELIVERY-MANIFEST.json
```

GitHub är ett valfritt nästa steg.

---

## 11. Vad händer om jag använder GitHub?

Projekt-ZIP:en är GitHub-redo.

När GitHub används kan projektet:

- valideras automatiskt vid commits och pull requests,
- byggas automatiskt vid release,
- få versionsnummer från GitHub Release-taggen,
- publicera distributionsartefakter automatiskt.

Exempel:

```text
Release tag: v1.2.0
```

ger distributionsversion:

```text
1.2.0
```

Du behöver inte underhålla versionsnumret manuellt i flera filer.

---

## 12. När är GPT:n klar?

GPT Byggaren gör en samlad release-readiness-bedömning.

Resultatet kan vara:

### ready

Projektet är redo för release.

### ready_with_warnings

Projektet kan releasas, men det finns dokumenterade begränsningar.

### blocked

Något blockerande problem måste lösas först.

---

## 13. Chat ZIP eller Custom GPT?

För enklare GPT:er kan de vara nästan likvärdiga.

För större GPT:er kan Chat ZIP bära rikare runtime-material, men både Chat ZIP och Custom GPT ska normalt byggas från samma canonical kontrakt.

Exempel på sådant som kan ge Chat ZIP större capability-täckning än Custom GPT:

- många filer,
- scripts,
- schemas,
- avancerad strukturerad data,
- omfattande arbetsflöden,
- projekt-ZIP-hantering,
- funktioner som är svåra att få plats med i Custom GPT.

GPT Byggaren ska avgöra detta åt dig.

---

## 14. Vad behöver du själv hålla reda på?

Så lite som möjligt.

Det viktigaste är:

- spara senaste projekt-ZIP:en,
- använd den när du vill fortsätta,
- beskriv verksamhetsmässiga beslut när GPT Byggaren verkligen behöver dem.

Projektstatus, planprogression, tekniska val och buildstruktur ska ligga i projektet.

---

## Vanliga kommandon

### Starta ett nytt projekt

```text
Jag vill bygga en GPT som ...
```

### Börja genomföra planen

```text
Gör första steget och ge mig resultatet som en zip.
```

### Fortsätt

```text
Gör nästa steg och ge mig en uppdaterad zip.
```

### Fortsätt från tidigare ZIP

```text
Fortsätt detta projekt och gör nästa rekommenderade steg.
```

### Bygg färdiga distributioner

```text
Bygg de färdiga distributionerna och ge mig nedladdningslänkar.
```

### Kontrollera om projektet är releaseklart

```text
Gör en release-readiness-bedömning.
```

---

## Kort sammanfattning

Du beskriver **vad** du vill bygga.

GPT Byggaren tar ansvar för att föreslå **hur** det bör byggas, struktureras, testas, paketeras och valideras.

Du kan sedan utveckla projektet steg för steg genom att återkommande be om **nästa steg** och få en ny komplett projekt-ZIP.


## GitHub-standard

Nya GPT-projekt ska normalt innehålla `README.md`, `.github/workflows/ci.yml` och `.github/workflows/release.yml`. GitHub-stöd är standard men kan väljas bort för uttryckligen lokala eller GitHub-fria projekt. Releaseversion ska härledas från GitHub Release-taggen.
