# Implementierungsstand – Agenqo Core 0.1.0

**Status:** Erste eigenständige Backend-Implementierung; KEIN Produktionsrelease.

## Tatsächlich implementiert

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

## Noch nicht vorhanden

- Weder öffentliche Suchwebsite noch Firmen-Claim / selbstständige Unternehmensregistrierung.
- Keine tatsächliche E-Mail/SMS-Zustellung, kein n8n-Prozess. Invitations bleiben READY; Tokens werden dem Admin nur zur kontrollierten Zustellung ausgegeben.
- Kein rechtlich abgenommenes Click-Wrap; ein adminseitiger Agreement-String ist KEIN Nachweis einer wirksamen Vereinbarung.
- Kein verifiziertes Anbietervertretungsverhältnis; Tokenbesitz allein reicht nicht für externen Livebetrieb.
- Keine Angebotsrevisionen, Stornos, Disputes, Web-Dashboards, Rechnungsstellung oder Payment.
- Keine Alembic-Migrationen, keine PostgreSQL-Transaktions-/Lasttests, keine vollständige Taxonomie, kein Golden-Record-Quellenmanagement.
- Keine OAuth/OIDC-, Abuse-/Rate-Limit- oder mandantenfähige Produktionssicherheit.
- Kein n8n-Outbox-Worker, kein MCP, keine KI-Verhandlung oder automatische Modellanbindung.
- Keine echten Aufträge, Gebühreneinnahmen oder bestätigten Marktzahlen.

## Ausführen (rein lokal)

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

## Nächste Integrationsschritte

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
