# Agenqo v0.6 — OIDC-Anbieterportal und MySQL-Transaktionssicherheit

**Implementiert am 27.10.2026; internes Pilot-Artefakt. Kein freigegebener Livebetrieb.**

## Tatsächlicher Stand

1. Bestehende Anbieter-API ist über Firmenmitgliedschaften an JWT-Subjects gebunden. Die Oberfläche nutzt Authorization Code + PKCE über oidc-client-ts.
2. Server liefert minimale **öffentliche** Auth-Konfiguration an \`GET /v1/public/auth-config\`: \`authority\`, \`client_id\`, \`scope\`. Die API gibt niemals geheime Schlüssel oder Tokens aus. Wenn OIDC nicht konfiguriert ist, meldet sie \`enabled:false\`.
3. Bereitgestellte Oberfläche \`/provider\` und Callback \`/provider/callback\`. OIDC-Token wird nur im Arbeitsspeicher der SPA gehalten, PKCE-Autorisierungsstatus kurzfristig in sessionStorage. Damit geht die Sitzung bei einem Browser-Reload verloren (bewusster Prototyp-Kompromiss). Keine Passwörter bei Agenqo.
4. Registrierte Anbieter sehen **nur eigene** freigegebene Unternehmen, veröffentlichte Golden Fields, vorgeschlagene Änderungen und zugeordnete Einladungen.
5. Mit \`GET /v1/public/companies?q=...\` können Anbieter Firmen zum Übernahmeantrag finden. Die Suche liefert nur Name, PLZ, Kategorie und interne Kandidaten-ID (maximal 15 Treffer), niemals Kontaktadressen oder Anbieter-Geheimnisse.
6. Übernahmeanträge werden mit Nachweisreferenz eingereicht, bleiben \`PENDING\` und benötigen die bereits implementierte manuelle Admin-Freigabe. Eine selbstbehauptete Firmenzugehörigkeit erteilt keine Rechte.
7. Angebote können angemeldete Firmenmitglieder über ihre *eigene Einladung* einreichen, ohne Zugang zu den früheren, nur manuell verteilten Einladungs-Tokens. Buchungen können sie über die autorisierte Firmenmitgliedschaft bestätigen. Beide Operationen nutzen die **bestehenden** Geschäftsregeln und die Buchungs-Outbox.
8. \`SELECT ... FOR UPDATE\` auf Anfrage vor der Käuferfreigabe, Einladung vor der Angebotsabgabe und Buchung vor der Anbieterbestätigung verhindert konkurrierende Doppelbuchungen im InnoDB-Pfad; bei bereits erfasster identischer Freigabe liefert die API einen idempotenten Replay.
9. GitHub CI enthält neben Python-/UI-Build jetzt einen echten MySQL-8.4-Konkurrenztest, ausgeführt gegen die unveränderte \`approve_offer\`-Operation. SQLite-Testroutinen sind kein Ersatz für diesen Test.

## Konfiguration

Das bestehende **MySQL** bleibt führende relationale Datenbank. DuckDB ist optional, eingebettet und nicht an den Login-Pfad gekoppelt. Kein PostgreSQL. Keine neuen Datenbankserver.

Erforderliche Variablen für Anbieter-Login:

- \`AGENQO_OIDC_ISSUER\` (https, Token-\`iss\`, OIDC-Discovery-Autorität)
- \`AGENQO_OIDC_JWKS_URL\` (https, issuer-kontrollierte öffentliche Schlüssel)
- \`AGENQO_OIDC_AUDIENCE\` (exakter \`aud\`-Wert des API-Access-Tokens)
- \`AGENQO_OIDC_CLIENT_ID\` (öffentliche SPA-Client-ID; **kein Client-Secret**)

Der externe Provider muss einen Public Client mit Authorization Code + PKCE anbieten. Registrierte Redirect-URI: \`https://<agenqo-host>/provider/callback\`. Die API akzeptiert gegenwärtig nur RS256-signierte Access-Tokens mit \`typ=at+jwt\`, nicht unspezifische ID- oder Refresh-Tokens. Beim Provider muss das gewünschte \`aud\` für die API explizit eingerichtet sein. Server und Browser müssen über TLS kommunizieren; der OIDC-Provider muss passende CORS-/Redirect-Regeln konfigurieren.

**Es wurde kein Keycloak/OIDC-Server auf dem Nutzersystem eingerichtet und keine echten Konten registriert.** Ohne externe OIDC-Konfiguration zeigt die Oberfläche erklärend an, dass die Anmeldung noch nicht aktiviert ist.

## Weitere notwendige Sicherheits- und Produktionsgates

- Echte Admin-Authentifizierung mit MFA und detaillierten Rollen statt eines globalen API-Schlüssels.
- CSRF-/XSS-Review, Content-Security-Policy und strikte Header für alle dynamischen Endpunkte.
- Rate Limits und Bot-/Abuse-Schutz für öffentliche Firmensuche, Anträge und Einladungslinks.
- Verifikationsprozess der Unternehmensvertretung und gesetzeskonforme Speicherung der Nachweise.
- Einladungs-Tokenrotation/-Widerruf und gesichertes n8n-Outbox-Dispatching (noch keine externe Zustellung).
- Rechtssichere Click-Wrap-Bedingungen mit dauerhaftem Nachweis der tatsächlich akzeptierten Version.
- Storno/Dispute/Refund-Ketten, echte E-Mail-Zustellung und Betriebshandbuch.
- Vollständige MySQL-Konkurrenztests für weitere kritische Transaktionen, einschließlich Provisionsbuchungen, Endzuständen und gleichzeitigen Übernahmeanträgen.
- Bedienbarkeit auf Mobilgeräten, Accessibility-Audit, echte Käuferoberfläche und anbieterbezogene Kapazitäten/Verfügbarkeiten.

Diese Umsetzung ist eine funktional integrierte und getestete **Pilot-Grundlage**, keine Aussage über Produktivbetrieb oder tatsächliche Vermittlungsumsätze.
