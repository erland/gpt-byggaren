# Custom GPT-kompilering – GPT Byggaren

## Syfte

Custom GPT är ett separat distributionsmål som kompileras från samma canonical sources som Chat ZIP.

Grundprincip:

> Custom GPT ska bevara canonical kärnfunktionalitet inom Custom GPT-plattformens gränser. Chat ZIP och Custom GPT är jämbördiga distributionsmål från samma canonical kontrakt.

Custom GPT får därför vara:

- likvärdig,
- reducerad,
- konsoliderad,
- transformerad,
- eller avrådd från om en meningsfull distribution inte kan skapas.

## Kompileringspipeline

```text
Canonical project
├── src/instructions/system.md
├── src/runtime-policy/
├── src/conversation-starters/
├── knowledge/
├── templates/
├── schemas/
└── scripts/
        ↓
Custom GPT compiler
        ↓
build/custom-gpt/
├── README.md
├── builder/
│   ├── instructions.md
│   ├── conversation-starters.md
│   ├── capabilities.md
│   └── knowledge-package/
├── COMPATIBILITY.md
├── VERSION
└── MANIFEST.json
        ↓
dist/<project-id>-custom-gpt-<version>.zip
```

## Builder-underlag

Custom GPT-distributionen ska ge användaren allt som behövs för att konfigurera GPT:n i Builder.

Minimikrav:

```text
builder/
├── instructions.md
├── conversation-starters.md
├── capabilities.md
├── compilation-report.json
└── knowledge-package/
```

### `instructions.md`

Den kompilerade Custom GPT-instruktionen.

### `conversation-starters.md`

De conversation starters som ska användas.

### `capabilities.md`

En mänskligt läsbar rekommendation av vilka capabilities som bör aktiveras.

Exempel:

```text
Webbsökning: Aktivera
Dataanalys: Aktivera
Bildgenerering: Behövs inte
```

### `knowledge-package/`

Exakt de filer som ska laddas upp som Knowledge.

### `compilation-report.json`

Maskinläsbar rapport över instruktionsbudget och Knowledge-urval: canonical/compiled tecken, verifierade core-markörer, valda och bortvalda Knowledge-filer samt använda priority-globs.

## Instruktionskompilering

Custom GPT-instruktionen ska skapas från canonical instruktion och relevanta runtime policies.

Kompilatorn ska stödja tre lägen:

### `identical`

Använd canonical instruktion oförändrad.

Lämpligt när den ryms naturligt och inga ZIP-specifika regler behöver tas bort.

### `compressed`

Korta och konsolidera deterministiskt utan att ändra betydelsen. Kompilatorn ska alltid verifiera att deklarerade `core_contract.required_markers` finns kvar efter kompilering.

### `compiled`

Generera en distributionsspecifik instruktion där endast Custom GPT-relevanta regler tas med. Explicit urval kan införas per projekt, men kärnmarkörer får aldrig tas bort.

För avancerade GPT:er är `compressed` eller `compiled` normalt lämpligast.

## Instruktionsprioritet

Om instruktionen måste reduceras ska följande prioriteras:

1. identitet och syfte,
2. scope och kärnflöde,
3. beslutskriterier,
4. kvalitets- och säkerhetsregler,
5. relevanta verktygsregler,
6. outputregler,
7. återupptagning om den stöds i Custom GPT,
8. exempel,
9. ZIP-specifika regler.

## Knowledge-kompilering

Custom GPT Knowledge kan byggas med fyra strategier:

### `identical`

Använd canonical Knowledge direkt.

### `consolidate`

Slå ihop flera canonical filer till färre runtimefiler.

### `prioritize`

Välj endast de viktigaste resurserna.

### `hybrid`

Kombinera konsolidering och prioritering.

## Knowledge-gräns

Kompilatorn ska läsa gränsen från `gpt-project.yaml`.

Exempel:

```yaml
runtime:
  custom_gpt:
    platform_limits:
      knowledge_max_files: 20
```

Ingen buildlogik ska hårdkoda samma värde separat.

## Filstorlek och format

Plattformsbegränsningar för filstorlek och format ska på samma sätt vara konfigurerbara när de införs.

## Capability-mappning

Capabilities ska härledas från analysmodellen.

Exempel:

```yaml
capabilities:
  web:
    recommendation: required
    builder_action: enable
  data_analysis:
    recommendation: required
    builder_action: enable
  image_generation:
    recommendation: not_recommended
    builder_action: disable
```

Användaren ska inte behöva fatta dessa tekniska val utan rekommendation.

## Funktionsreduktion

När Custom GPT inte kan bära full funktionalitet ska skillnaden dokumenteras.

Exempel:

```text
Chat ZIP:
- full modellhantering
- 48 runtimefiler
- lokala valideringsscripts
- avancerade exporttemplates

Custom GPT:
- kärnanalys
- 18 konsoliderade Knowledge-filer
- inga lokala projektscripts

Reducerad funktion:
- full projektnavigering
- lokal schema-validering
```

## `COMPATIBILITY.md`

Varje reducerad Custom GPT-build ska innehålla en kompatibilitetsrapport.

Den ska beskriva:

- funktioner som är likvärdiga,
- funktioner som är reducerade,
- funktioner som saknas,
- varför skillnaden finns,
- rekommenderad primär runtime.

## Paritet

Paritet ska bedömas per capability, inte bara som antal filer.

Exempel:

```text
Capability                     Chat ZIP   Custom GPT
----------------------------------------------------
Grundarbetsflöde                  ✓           ✓
Webbresearch                      ✓           ✓
Strukturerad modellhantering      ✓           ~
Lokala projektscripts             ✓           -
```

Symboler:

- `✓` – likvärdig
- `~` – reducerad
- `-` – saknas

## Buildresultat

Kompilatorn ska rapportera minst:

```text
Instructions: 7 612 / 8 000 characters
Knowledge: 18 / 20 files
Conversation starters: 4
Capabilities: configured
Compatibility: reduced
Result: PASS
```

## Blockerande fel

Builden ska blockeras när:

- instruktionen överskrider konfigurerad gräns,
- Knowledge överskrider filgräns,
- obligatoriska Builder-filer saknas,
- kärnfunktionalitet blir missvisande,
- kompilerad instruktion motsäger canonical beteende.

## Varningar

Varning ska kunna ges när:

- pariteten är reducerad,
- Knowledge har konsoliderats kraftigt,
- vissa ZIP-funktioner saknas,
- Custom GPT rekommenderas endast som sekundär runtime.

## När Custom GPT ska avrådas

GPT Byggaren ska rekommendera `not_recommended` när:

- kärnfunktionen kräver runtimeförmågor som inte kan representeras,
- funktionsreduktionen blir så stor att användaren får fel bild av produkten,
- distributionen skulle kräva att viktiga beteenderegler flyttas till fel lager,
- underhållskostnaden blir oproportionerlig.

## README för Custom GPT-distributionen

Distributionen ska innehålla en kort installationsguide:

1. öppna GPT Builder,
2. klistra in `builder/instructions.md`,
3. lägg in conversation starters,
4. aktivera rekommenderade capabilities,
5. ladda upp filerna i `builder/knowledge-package/`,
6. använd `COMPATIBILITY.md` för att förstå skillnader mot Chat ZIP.

## Definition of Done

Custom GPT-kompileringen är definierad när:

- instruktionstrategi finns,
- Knowledge-strategi finns,
- capabilities kan härledas,
- Builder-underlag är definierat,
- plattformsgränser läses från projektkontraktet,
- kompatibilitetsrapport är definierad,
- blockerande valideringar är definierade,
- reducerad funktionalitet dokumenteras explicit.
