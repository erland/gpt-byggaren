# Validera rekonstruerade GPT-projekt

Kör `python scripts/validate_reconstructed_project.py --project-root PROJECT` efter granskad upphöjning och komplettering av canonical kontrakt.

Kontrollen återanvänder GPT Byggarens ordinarie projektlint och validerar capabilities, artifacts, workspace/state, tools samt project-status mot befintliga JSON-scheman. Resultatet redovisar samtliga verifierade scheman, lintfynd och kvarstående blockerare. Inga distributioner byggs.

Även om alla scheman och lint är godkända returneras `validated_pending_runtime_review`: release readiness förblir falsk och runtimes ska förbli avstängda. Verktyget aktiverar inga runtimes och tar inga tekniska beslut i stället för användaren.

En särskild förutsättning är att `schemas/project-status.schema.json` finns i det rekonstruerade projektet. Saknas den eller andra scheman markeras valideringen blockerad; det går inte att behandla ofullständig projektstruktur som klar.

Nästa steg är att föra över verifierat källmaterial och komplettera runtime-anpassningar, jämföra funktionell paritet och först därefter eventuellt aktivera distributioner med sina ordinarie bygg- och releasekontroller.
