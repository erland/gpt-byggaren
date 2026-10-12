# Plugin: deklarativt källutkast utan distributionsmotor

Detta reservläge gäller enbart när GPT Byggaren körs som OpenAI Plugin och det är verifierat att den kanoniska distributionsmotorn inte kan installeras och köras i värdens arbetsyta.

1. Fortsätt skapa projektets källmaterial från de etablerade kanoniska kontrakten: projektspecifika instruktioner, Skills, kontrakt, projektprofil, utvecklingsplan, tester och status. Skapa inte egna ersättningar för bygg- eller valideringsskript.
2. Behåll det valda arbetssättet i `delivery.mode`: ZIP eller GitHub. Föreslå inte GitHub igen för ZIP-användaren. Om GitHub är valt kan källutkastet läggas i en PR; GitHub Actions får då senare utföra det verkliga kanoniska bygget.
3. Ange i `project-status.yaml`:
   ```yaml
   generation:
     mode: declarative_fallback
     canonical_engine_available: false
   build:
     status: pending_canonical_verification
     release_ready: false
   ```
   Dokumentera konkret blockerare och saknade filer.
4. Leverera enbart filer som miljön faktiskt kan skapa, tydligt märkta som overifierat källutkast. Utge aldrig fem ZIP-filer för att vara verifierade distributionsartefakter om originalmotorn inte har byggt och validerat dem.
5. Vid fortsatt arbete i en körmiljö med kanonisk motor: validera projektprofil, installera originalmotorn, bygg projekt-ZIP och de fem runtime-distributionerna, kör ordinarie validering och uppdatera status med faktiska testresultat.

Detta ändrar inte Chat ZIP, Claude Project, Claude Skills eller OpenCode. De använder oförändrat den kanoniska distributionsmotorn där den finns tillgänglig.
