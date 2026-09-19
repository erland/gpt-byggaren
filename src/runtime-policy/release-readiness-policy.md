# Release readiness policy

- Resultat: ready, ready_with_warnings, blocked.
- Blockerande kvalitetsgates stoppar release.
- Project ZIP och samtliga aktiverade runtime-distributioner i build target-registret bedöms separat.
- Samma readinessmodell används lokalt och i GitHub Release.

- Nya runtime-targets ska automatiskt omfattas av readiness utan plattformsspecifik kod.
