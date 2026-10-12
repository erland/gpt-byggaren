# GPT Engine Package – portabelt kontrakt (v1)

Ett GPT-specifikt Engine ZIP innehåller exekverbara resurser som en Plugin
inte säkert kan materialisera från installerade Skill-assets. Det är **inte**
en sjätte runtime-distribution eller en ersättningsbyggare.

## Namn och innehåll

Format: `<gpt-id>-engine.zip`, exempel `gpt-byggaren-engine.zip`.
Varje GPT väljer själv sina nödvändiga skript, mallar, schemafiler,
konfiguration och andra filer som faktiskt krävs för lokal exekvering.
Ta inte med irrelevanta källfiler bara för att de finns i projektet.

ZIP-roten innehåller `engine-package.json`:
- `schema_version`: 1
- `engine_id`: GPT:ns stabila id
- `version`: samma version som den tillhörande Plugin-distributionen
- `entrypoint`: relativ sökväg till en exekverbar verifieringsrutin
- `required_files`: obligatoriska relativa sökvägar
- `python_dependencies`: deklarerade Python-beroenden
- `files`: samtliga paketerade resursers relativa sökvägar → SHA-256-hex

Alla sökvägar måste vara relativa och får inte lämna ZIP-roten. Ingen fil
får saknas eller avvika från manifestet. Manifestet ersätter inte en betrodd
källa för checksummor; verifiera arkivets ursprung/version före exekvering.
Självtest ska kontrollera installation och faktisk funktion, inte enbart
filnärvaro.

## Plugin-flöde

Vid första konkreta projektstarten testar Plugin åtkomst till motorn en gång.
En lokalt läsbar motor självtestas; om den inte är åtkomlig får användaren
en **direkt länk till exakt samma GitHub Release-version** av
`<gpt-id>-engine.zip`. För testversioner utan release får ingen påhittad
URL erbjudas. Användaren kan bifoga ZIP-filen till konversationen; den
materialiseras därefter i Python och verifieras innan körning.

Lita aldrig på att en intern Skill-asset automatiskt kan kopieras,
exponeras eller köras i ChatGPT:s Python-miljö. Inga alternativa
modellgenererade paketerare. Om ingen körbar motor finns: redovisa ett
overifierat källutkast och fortsätt med möjliga projektsteg.

## GPT Byggaren

Dess inventering definieras av `scripts/package_distribution_engine.py`.
Utöver skript ingår mallar, schema- och konfigurationsmaterial. Samma
paketerare bygger `gpt-byggaren-engine.zip` för CI, release och
eventuell Plugin-/Skill-resurs. Chat ZIP:s existerande
`distribution-engine/`-layout ska inte ändras av namngivningen.
