# AI-stödd projektförståelse – generellt tolkningskontrakt

Den generella inventeringen från `discover_legacy_project.py` utgör källförteckningen. Nästa steg är att GPT Byggaren själv **läser relevanta källfiler** och föreslår en plattformsneutral tolkning, oberoende av katalogstruktur.

## Analysinstruktion

Analysera projektets syfte, kritiska beteende, instruktioner, Knowledge, verktyg, beroenden och arbetsflöden. Varje sakpåstående måste styrkas av minst en konkret källfil i inventeringen, med exakt `path` och `sha256`. Att en fil har ett visst namn är inte tillräckligt för att härleda dess innehåll. Ange osäkerhet och frågor som inte kan avgöras av underlaget i `unresolved`. Var särskilt försiktig med körbara verktyg och behörigheter: existensen av skript betyder inte att de kan eller bör köras. Markera aldrig releaseklart eller aktivera en runtime.

Analysen lämnas som JSON, exempel:

```json
{
  "schema_version": 1,
  "release_ready": false,
  "runtime_activated": false,
  "claims": [
    {
      "role": "instructions",
      "confidence": "medium",
      "description": "Den angivna filen innehåller arbetsinstruktioner",
      "evidence": [
        {
          "path": "unusual/location/my-file.txt",
          "sha256": "<sha256 från inventeringen>"
        }
      ]
    }
  ],
  "unresolved": ["Verktygsberoenden behöver granskas"]
}
```

Kör `python scripts/validate_legacy_interpretation.py --discovery DISCOVERY.json --interpretation INTERPRETATION.json`. Valideraren kontrollerar deklarerad roll, confidence, beskrivning, evidenssökväg och kontrollsumma samt tydliga release-/runtime-spärrar. Den godkänner **endast för fortsatt granskning**, inte som canonical kontrakt.

Viktigt: En korrekt källhänvisning bevisar att källfilen finns och är oförändrad, inte att AI:ns tolkning är semantiskt riktig. Därför behövs fortsatt mänsklig eller oberoende verifiering vid tvetydigheter och innan distributioner aktiveras. Detta steg implementerar ett AI-kompatibelt arbetskontrakt och deterministisk kontroll, inte ett externt modell-API eller automatisk sammanfattning i Python. Befintliga igenkänningsregler kan fortfarande fungera som valfria genvägar.
