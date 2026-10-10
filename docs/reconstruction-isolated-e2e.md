# Isolerad testbyggning av rekonstruerade GPT-projekt

Kör `python scripts/exercise_reconstructed_runtimes.py --project-root PROJECT --targets chat,claude,opencode,plugin`.

Verktyget kopierar ett ännu blockerat rekonstruerat projekt till en temporär arbetskatalog och anropar **de riktiga runtimebyggarna** därifrån. Paketen granskas med befintliga offline-smoketester. Originalfiler, status och releaseflagga ändras inte. Ordinarie byggspärr från PR #26 kvarstår.

Adapterfel redovisas per runtime i `build_errors`; ofullständigt återställda projekt förväntas kunna sakna mallar, policyfiler och deklarerade runtimeinställningar. Dessa fel ska åtgärdas genom verifierad komplettering av projektkontrakt, inte genom automatiskt påhittade inställningar. Kontrollen kan uttryckligen köras på valda mål, men full paritetsattestering kräver alla fyra samt fungerande beteendetestning.

**Begränsning:** Detta är en isolerad bygg-/paketövning och inte ett bevis för identiskt beteende i ChatGPT, Claude eller OpenCode. Det ger inte ett projekt status `release_ready`.
