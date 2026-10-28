# Implementierungsstand Agenqo – aktueller Snapshot v0.8 (28.10.2026)

**Status:** technisch fortgeschrittener Pilotkern, **kein produktiver Marktplatz und kein nachgewiesener Live-Umsatz**. Die Bezeichnung v0.8 beschreibt die neu hinzugefügte Kontakt-Policy und Käuferansicht; die Paketversionsnummer in pyproject.toml ist derzeit 0.5.0. Technische Versionsstände sind keine Produktreifegrade.

## Was aktuell im Repository liegt

- Python/FastAPI, SQLAlchemy, **MySQL/InnoDB** als verbindliche Transaktionsdatenbank, Alembic-Migrationen 0001–0003, optionales eingebettetes DuckDB für Analytik. PostgreSQL ist **nicht** Bestandteil des aktuellen Soll-Deployments.
- Zustandsautomaten, Angebotshashes, Betragslogik, Pilot-APIs, Provider-Portal mit OIDC-Validierung, Golden-Record-Beobachtungen/Claims, Service-Schema für Entrümpelung, Kosten- und Erlösjournal pro RFQ einschließlich Fehlfällen.
- Interne v0.7-n8n-Brücke mit MySQL-Outbox, Lease, Retry/Dead Letter und importierbarem **inaktivem** Workflow. Keine externen Mails/SMS, keine produktiven n8n-Credentials und kein Liveversand nachgewiesen.
- **Neu in v0.8:** append-only Kontaktzustimmungen und Opt-outs mit manueller Nachweisreferenz, auditierte fail-closed Einladungs-Vorprüfung, Selbst-Widerruf per Anbieter-Token; Käuferstatus-API und React-Angebotsvergleich mit exakt gebundener Freigabe. Tests und neue Alembic-Migration 0004 im Repository.
- GitHub-Actions-Testkonfiguration für MySQL-Migrationen, Konkurrenztests, API- und Frontend-Build; CI-Ergebnisse pro Commit kontrollieren, sie sind kein Nachweis einer realen Deploymentabnahme.

## Was aktuell nicht als fertig oder produktiv gelten darf

- Vollständiges selbstständiges B2C-/B2B-Käufer-Frontend mit öffentlichem, abuse-geschütztem Intake; eine geschützte Ansicht für **bereits angelegte** Anfragen einschließlich Vergleich, Freigabe und Status ist seit v0.8 vorhanden.
- **Rechtsgeprüfte** kanalbezogene Outreach-Regeln und sichere tatsächliche Zustellung; die v0.8-Policy implementiert zunächst ausschließlich dokumentiertes Anbieter-Opt-in, Widerruf und Versandvorprüfung, aber keinen Livekontakt.
- Vollständige Quote-Revisionen, Storno-/Dispute-/Completion-Belege, rechtswirksamer Provisionsvertrag samt Rechnung/Zahlung.
- Ausgereifte Matching-Engine mit ServiceArea/Fahrzeit/Kapazität, weitere buchbare Kategorien, externe Agenten-MCPs.
- Reale, bezahlte Vermittlungskohorten und positiver RFQ-Deckungsbeitrag; verbindlicher rechtlicher Live-Check.

**Neu v0.8:** [Kontakt-Policy und Käufer-Pilotportal](CONTACT_POLICY_AND_BUYER_PILOT_V08.md). **Verbindliche nächste Schritte:** [Agenqo v3 P0-Ausführungsvertrag](AGENQO_V3_P0_EXECUTION_CONTRACT.md). **Datenbankentscheidung:** [MySQL + DuckDB](DATENBANK_DONOREN_MYSQL_DUCKDB.md). **Führendes Zielbild:** [v3.0](AGENQO_GESAMTKONZEPT_V3.md).

---

## Historischer Entwicklungsverlauf – Angaben älterer Versionen nicht als Ist-Stand lesen

### Historische Ausgangsversion v0.1.0

**Historische Momentaufnahme:** Erste eigenständige Backend-Implementierung; KEIN Produktionsrelease.

### Damals implementiert (v0.1)

- Python/FastAPI API, SQLAlchemy-Persistenz, PostgreSQL via Docker Compose und SQLite für lokale Tests.
- Deterministische Zustandsautomaten für Anfrage, Einladung, Angebot, Buchung und Provision.
- Cent-genaue Decimal-Rechnung von Netto/Brutto und vertraglich referenzierter Provision.
- SHA-256-Angebotsfingerprint zur Prüfung des genauen freigegebenen Angebotsstandes.
- Zufällige Zugriffs-Tokens, von denen serverseitig nur SHA-256-Digests gespeichert werden.
- Admin-API: Anbieteranlage, Kundenanfrage, manuelle Qualifikation und Auswahl von maximal acht Anbietern.
- Strukturierte Anbieter-Angebotsabgabe mit privatem Token und expliziter Anbieterbindungserklärung.
- Manuelle Admin-Angebotsprüfung; Käufervergleich, exakte Angebotsfreigabe, Provider-Bestätigung.
- Manuell belegter Abschluss; Provisionsereignis nur mit vorher referenzierter Vereinbarung.
- Audit- und Outbox-Tabellen sowie pytest-Tests; GitHub Actions Workflow.

### Damals noch nicht vorhanden (v0.1)

- Weder öffentliche Suchwebsite noch Firmen-Claim / selbstständige Unternehmensregistrierung.
- Keine tatsächliche E-Mail/SMS-Zustellung, kein n8n-Prozess. Invitations bleiben READY; Tokens werden dem Admin nur zur kontrollierten Zustellung ausgegeben.
- Kein rechtlich abgenommenes Click-Wrap; ein adminseitiger Agreement-String ist KEIN Nachweis einer wirksamen Vereinbarung.
- Kein verifiziertes Anbietervertretungsverhältnis; Tokenbesitz allein reicht nicht für externen Livebetrieb.
- Keine Angebotsrevisionen, Stornos, Disputes, Web-Dashboards, Rechnungsstellung oder Payment.
- Keine Alembic-Migrationen, keine PostgreSQL-Transaktions-/Lasttests, keine vollständige Taxonomie, kein Golden-Record-Quellenmanagement.
- Keine OAuth/OIDC-, Abuse-/Rate-Limit- oder mandantenfähige Produktionssicherheit.
- Kein n8n-Outbox-Worker, kein MCP, keine KI-Verhandlung oder automatische Modellanbindung.
- Keine echten Aufträge, Gebühreneinnahmen oder bestätigten Marktzahlen.

### Historischer lokaler Start (v0.1)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
export AGENQO_ADMIN_KEY="einen-langen-zufaelligen-schluessel-setzen"
export AGENQO_AUTO_CREATE_SCHEMA=1
uvicorn agenqo.api:app --reload
pytest
```

Für Docker Compose zusätzlich `AGENQO_DB_PASSWORD` setzen. API-Port ist auf localhost:8080 gebunden; **keine ungeprüfte öffentliche Exposition**.

### Damals geplante nächste Schritte (v0.1)

1. Versionierte Alembic-Migrationen und PostgreSQL-Integrationstests.
2. Verifizierte Company Claims, Golden-Record-Provenienz und Provider-Rollen.
3. Strukturierte Angebotspositionen, echte Revisionen und belastbare Steuer-/Kleinunternehmerbehandlung.
4. Quote-Link-Frontend sowie n8n-Versand über Outbox und rechtlich zulässige Kontaktentscheidung.
5. Storno/Reklamation, Einwilligung/AGB und Kosten je RFQ, Billing und Support.
6. Buyer-/Provider-Remote-MCP über denselben geprüften Geschäfts-APIs.

**Sicherheitshinweis:** Der Code ist als internes Entwicklungsartefakt gedacht. Keine produktive Vermittlung und kein externer Livebetrieb ohne zusätzliche Sicherheits-, Vertrags- und Datenschutzprüfung.


## Finanzielle Verbindlichkeit im Prototyp

Der bei Kundenfreigabe dokumentierte Vermittlungsvertrag einschließlich Provisionssatz und Mindestprovision wird nun als **Buchungssnapshot** gespeichert. Spätere Änderungen des Provider-Profils lösen weder Nachberechnungen noch nachträgliche Provisionsansprüche für die frühere Buchung aus. Dieser Snapshot ersetzt **keinen** rechtsverbindlich unterzeichneten oder anderweitig wirksam angenommenen Vertrag; dessen Beweisführung bleibt ausstehend.


## Ergänzung: Donor-Integration (v0.2, 27.10.2026)

Umgesetzt: eigenständige Golden-Record-Beobachtungen und Publikationsgates (aus TonnEstate-Mechanismen adaptiert); schema-validierte Entrümpelungsanforderungen; dynamisches React-JSON-Schema-Form für Angebotsabgaben; Header-basierter Tokenzugriff auf Einladungsdaten und Angebotseinreichung; Buchungsbestätigungen nur über Header-Token; PENDING-Outbox-Ereignis nach Bestätigung.

**Nicht implementiert:** Übernahme echter TonnEstate-Unternehmensdaten, echtes Selfservice-Onboarding, voll funktionsfähiges Anbieterportal, produktives Login, rechtliches Click-Wrap, E-Mail/n8n-Versand, Auszahlungen, Migrationsschema, ausgerollte Website oder bestätigte wirtschaftliche Transaktion. Mercur ist bewusst als möglicher Donor evaluiert, nicht eingebunden.

Technische Einzelheiten: docs/DONOREN_ADOPTION_2026-10-27.md.


## Ergänzung v0.3 – Provider-Identität / Migrationen

- JWT-Resource-Server nach OAuth2: RS256, feste Audience, Issuer, Expiry und `typ=at+jwt`, Signaturprüfung über JWKS. Fail-closed ohne Konfiguration. Kein selbst betriebener Identity Provider.
- Anbieterbeantragte Ownership Claims mit kryptografisch identifiziertem `sub`; nur Admin-Verifizierung legt Firmenmitgliedschaften an.
- Firmenmitgliedschaften sind serverseitig, aktiv/deaktivierbar, pro `company_id` isoliert. Mitglieder können nur für eigene Unternehmen vorgeschlagene Quellenbeobachtungen abgeben; Änderungen benötigen weiterhin Admin-Verifikation und Quellenfreigabe.
- Baseline-Migration mit Alembic, einschließlich bestehender Angebots-/Buchungsdatenmodelle und neuer Provider-Tabelle.
- CI testet Anspruch/Abweisung, fremde Firmen, fehlerhafte JWTs, SQLite-Migrationen und frisches PostgreSQL-Schema.

**Nicht vorhanden:** Echtbetrieb eines OIDC-Providers, Provider-Login-UI, Passwortwiederherstellung, Benutzer-Management, automatische Firmenverifikation, vollständige Delegation von Mitarbeitern/Agenten, IP-/Token-Rate-Limits, Betrieb/Monitoring, produktive Vertragsprüfung. Nicht öffentlich deployen.

## Ergänzung v0.4 – Unit Economics

RequestEconomicEvent führt immutable, idempotente, per RFQ zugeordnete COST-/RECEIPT-Ereignisse. Zwei Admin-Reporting-Endpunkte berechnen erfasste Kosten, erhaltene Beträge und einen vorläufigen Deckungsbeitrag, einschließlich nicht erfolgreich abgeschlossener Anfragen. Eine nur provisionsfähige Forderung wird getrennt ausgewiesen, nicht als Zahlung verbucht.

**Weiter offen:** PSP-/Bank-Reconciliation, echte Buchhaltung, Kostenautomatisierung, Rückerstattungskorrekturen, Fixkosten, Premium-Abos und erhobene reale Pilotdaten. Details: docs/UNIT_ECONOMICS_V04.md.


## Datenbankentscheidung v0.5 – frühere PostgreSQL-Angaben historisch

**Aktueller Stand:** Das Deployment verwendet vorhandenes **MySQL** statt PostgreSQL; CI testet die Alembic-Migration auf einem temporären MySQL-Service. Eingebettetes **DuckDB** ist optional für anonymisierte analytische Berichte. Die alten Abschnitte oben beschreiben den damaligen Prototypen und sind hinsichtlich der Datenbank überholt.

Details: docs/DATENBANK_DONOREN_MYSQL_DUCKDB.md.


## Implementierung v0.7: n8n-Brücke (intern, gesichert)

Agenqo verfügt jetzt über eine MySQL-Outbox mit Leasing, idempotenter Quittierung, Retry/Backoff, Dead-Letter und explizitem manuellen Wiederanlauf. Geschäftlich zulässige Ereignisse werden atomar mit den relevanten Geschäftszuständen persistiert. Das importierbare Workflow-JSON ist absichtlich INAKTIV und erstellt bei erfolgreicher Verarbeitung ausschließlich interne Review-Aufgaben. Es gibt noch keine tatsächliche externe Zustellung, rechtlich freigegebene Marketingkontakte oder Verbindung zu einer produktiven n8n-Instanz.

Hinweise zur Inbetriebnahme und Sicherheitsgrenzen in docs/N8N_ORCHESTRATION_V07.md.
