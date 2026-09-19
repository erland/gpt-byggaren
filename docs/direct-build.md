# Direktbyggnad utan GitHub – GPT Byggaren

## Syfte

GPT Byggaren ska kunna färdigställa en GPT och producera persistenta artefakter direkt, utan att GitHub används.

Canonical artifact-kontrakt beskriver **vad** som ska produceras. Den interaktiva runtime-adaptern avgör **hur** användaren får åtkomst till resultatet, exempelvis som nedladdningslänk i ChatGPT eller som fil i ett lokalt workspace.

GitHub ska vara en valfri kanal för versionshantering och releaseautomation, inte ett krav för att få en fungerande GPT.

## Normal direktleverans

När en GPT är distributionsbar ska GPT Byggaren normalt kunna leverera:

```text
<project-id>-project.zip
<en eller flera runtime-distributioner enligt build target-registret>
SHA256SUMS.txt
DELIVERY-MANIFEST.json
```

Om Custom GPT inte är aktiverad eller inte är meningsfull ska den artefakten utelämnas.

## Versionsstrategi utan GitHub

Före en riktig GitHub Release ska en lokal utvecklingsversion kunna användas.

Rekommenderat format:

```text
0.0.0-dev
0.0.0-dev.1
0.0.0-rc.1
```

GPT Byggaren ska inte låtsas att en utvecklingsbuild är en officiell release om ingen sådan har skapats.

## Direktbyggnadsflöde

```text
Projekt-ZIP / projektkällor
        ↓
project hygiene
        ↓
build
        ↓
distribution validation
        ↓
runtime parity
        ↓
checksums
        ↓
direkta nedladdningslänkar
```

## Lokal buildprofil

Direktbyggnaden ska använda samma buildscript som GitHub Actions senare kommer använda.

Exempel:

```bash
python scripts/build_distributions.py   --project-root .   --version 0.0.0-dev
```

Därefter:

```bash
python scripts/validate_distributions.py   --project-root .
```

## Leveransmanifest

GPT Byggaren ska kunna skapa ett maskinläsbart leveransmanifest med:

- projekt-id,
- version,
- skapade artefakter,
- SHA-256,
- valideringsresultat,
- runtime-strategi,
- aktiverade runtime-targets.

Exempel:

```json
{
  "project": "example-gpt",
  "version": "0.0.0-dev",
  "artifacts": [
    {
      "type": "project_zip",
      "file": "example-gpt-project.zip"
    },
    {
      "type": "chat_zip",
      "file": "example-gpt-chat-0.0.0-dev.zip"
    }
  ]
}
```

## Direktleveransens användarupplevelse

När runtime stöder fil-/länkleverans ska GPT Byggaren normalt svara kort och ge tydliga länkar. Detta är adapterbeteende och inte en del av det canonical artifact-kontraktet.

Exempel:

```text
GPT:n är byggd och validerad.

Projekt:
[Hämta project.zip]

Chat ZIP:
[Hämta chat.zip]

Custom GPT:
[Hämta custom-gpt.zip]

Checksummor:
[Hämta SHA256SUMS.txt]
```

## Projekt-ZIP

Projekt-ZIP är den fortsatta utvecklingsprodukten.

Den ska kunna:

- bifogas igen i en ny konversation,
- packas upp lokalt,
- checkas in i Git,
- användas för framtida build,
- vidareutvecklas steg för steg.

## Chat ZIP

Chat ZIP och Custom GPT byggs normalt båda för större GPT:er; ingen är automatiskt primär.

Den ska kunna bifogas direkt i en ChatGPT-konversation.

## Custom GPT ZIP

Custom GPT ZIP innehåller Builder-underlaget.

Den ska bara levereras om:

- distributionen är aktiverad,
- plattformsvalideringen inte är blockerad,
- den funktionella pariteten är tillräcklig för att distributionen ska vara meningsfull.

## Valideringskrav

Direktleverans ska inte ske om:

- build misslyckas,
- project hygiene är blockerad,
- distributionsvalidering är blockerad,
- Custom GPT överskrider plattformsgränser,
- manifest eller checksummor inte kan skapas.

## GitHub senare

Projekt-ZIP:en ska vara GitHub-redo.

Användaren ska kunna:

1. packa upp projekt-ZIP,
2. skapa Git-repo,
3. pusha till GitHub,
4. skapa GitHub Release,
5. få motsvarande distributioner byggda automatiskt.

## Definition of Done

Direktbyggnad utan GitHub är klar när:

- samma buildkärna används som framtida CI/release,
- lokal utvecklingsversion stöds,
- alla relevanta artefakter skapas,
- checksummor skapas,
- leveransmanifest skapas,
- validering körs före leverans,
- den aktiva runtime-adaptern kan göra artefakterna tillgängliga på ett korrekt sätt.
