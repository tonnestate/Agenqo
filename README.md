# Agenqo

**Eigenständiger KI-nativer Dienstleistungsmarktplatz für Menschen, Unternehmen und autonome Käufer-/Anbieteragenten.**

## Fachlicher Stand (v3.0)

- [Führendes Agenqo-Gesamtkonzept v3.0](docs/AGENQO_GESAMTKONZEPT_V3.md)
- [Branchen- und Leistungskatalog v3.0](docs/AGENQO_BRANCHENKATALOG_V3.md)
- [Konzept v2.0 – historischer Stand](docs/AGENQO_GESAMTKONZEPT.md)
- [Älterer MVP-Plan – bei Widersprüchen gilt v3](docs/MVP_UND_VALIDIERUNG.md)

## Implementierung (Core 0.1.0)

**Es liegt ein eigenständiger Backend- und Anbieterformular-Prototyp vor. Er ist noch kein produktionsreifes öffentliches Produkt.**

### Donoren-Integration v0.2

- [Donorenentscheidung und tatsächlich adaptierte Funktionen](docs/DONOREN_ADOPTION_2026-10-27.md)
- [Anbieterformular mit React JSON Schema Form](web/): dynamisch vom Backend bereitgestelltes Angebotsformular.
- [Quellenbasierter Golden Record](agenqo/company_records.py): Beobachtungen, Quellenfreigabe, Publikation und überprüfte Ownership-Claims (ohne automatische Rechtevergabe).
- [Entrümpelung als versioniertes Dienstleistungs-Schema](agenqo/service_catalog.py): strukturierte Anforderungen und Angebotsattribute.
- PENDING-Outbox-Ereignis bei einer bestätigten Buchung, **ohne aktiven Versand**.

**Frontend lokal:** Im Verzeichnis web einmal npm install ausführen, dann npm run dev; FastAPI muss separat auf localhost:8080 laufen. Ein Pilot-Link hat die Form http://127.0.0.1:5173/quote#EINLADUNGS_TOKEN. Token niemals in Logs, Analytics oder Screenshots veröffentlichen. Der Browser sendet ihn an die API im Header X-Invitation-Key. Vite leitet /v1 an das lokale Backend weiter.

**Frontend im Docker-Image:** Das Mehrstufen-Dockerfile baut React und liefert die statische Oberfläche auf /quote aus. Nur intern verwenden; der gesamte Prototyp besitzt noch keine produktionsfähige Identitätsprüfung, Brute-Force-Abwehr, rechtliche Click-Wrap-Freigabe oder Datenbankmigrationen.

- [Aktueller Implementierungsstatus und bekannte Lücken](docs/IMPLEMENTIERUNG_STAND.md)
- `agenqo/domain.py`: Zustandsautomaten, Decimal-Beträge, Angebotsfingerprints und Token-Prüfung.
- `agenqo/models.py`: erste eigenständige SQLAlchemy-Transaktionsmodelle.
- `agenqo/api.py`: geschützte Pilot-API für Kundenanfragen, Anbieter-Einladungen, Angebotsabgabe, Prüfung, Freigabe, Buchungsbestätigung und evidenzgestützten Abschluss.
- `tests/`: Fachregel- und API-Integrationstests, ausgeführt über GitHub Actions.
- `docker-compose.yml`: nur Agenqo-API, verbunden mit dem bereits vorhandenen MySQL; kein zusätzlicher Datenbankserver.

### Entwicklung lokal

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
export AGENQO_ADMIN_KEY="ersetzen-durch-langes-geheimes-token"
export AGENQO_AUTO_CREATE_SCHEMA=1
uvicorn agenqo.api:app --reload
pytest
```

Für Docker Compose sind `AGENQO_DATABASE_URL` (vorhandenes MySQL) und `AGENQO_ADMIN_KEY` erforderlich. Die API bindet in Compose nur an localhost:8080. Die automatische Tabellenanlage ist nur für lokale Entwicklung vorgesehen.

### Sicherheit und Scope

Die Einladungs-API **versendet noch keine externen Nachrichten**; sie stellt nur manuell zu übermittelnde, zeitlich begrenzte Tokens bereit. Es gibt noch keine produktionsfähige Anbieteridentitätsprüfung, Click-Wrap-Vertragsvorlage, Migrationsverwaltung, Rechnungsstellung, n8n-Sendestrecke, Website oder MCP-Integration.

**Nicht öffentlich deployen, bevor Rechtsprüfung, Authentifizierung, Abuse-Schutz, Schema-Migrationen, Token-Lifecycle und Datenrechtsprüfung abgeschlossen sind.**

## Architekturgrundsätze

Agenqo besitzt eigene Daten, APIs und Geschäftsregeln. TonnEstate, LemonMe, DragonFruitMe, BlackberryMe und CherryMe sind allenfalls geprüfte Donoren. n8n dient als austauschbare Orchestrierung, nicht als verbindliche Geschäftsführung. Dienstleistungen sind der einzige initiale Markt; Produkte sind ausgeschlossen.

**Wirtschaftliches Ziel:** reale, rechtlich zulässige Auftragsvermittlung mit positivem Deckungsbeitrag – einschließlich Kosten für erfolglose Anfragen.


### Provider-Identität und Datenbankmigrationen (v0.3)

**Verifizierbare Anbieteridentität:** OIDC/OAuth-Access-Token als RS256-JWT mit `typ=at+jwt`, validiert über externen vertrauenswürdigen JWKS-Endpunkt (Issuer, Audience, Expiry, Subject). Anbieter-Claims erhalten **keine** Mitgliedschaft vor manueller Admin-Freigabe. Danach können autorisierte Anbieter Änderungen als prüfpflichtige Quellenbeobachtungen vorschlagen. Ein Anbieter kann keine Daten fremder Betriebe ändern.

Erforderliche Server-Konfiguration: `AGENQO_OIDC_ISSUER`, `AGENQO_OIDC_AUDIENCE`, `AGENQO_OIDC_JWKS_URL` (HTTPS). Ohne diese Einstellungen verweigert die Provider-API den Zugriff. **Es ist noch kein Login-/Registrierungsfrontend und kein OIDC-Provider eingerichtet.** Kein selbst ausgestellter JWT-Schlüssel und keine unsichere Dev-Bypass-Rolle.

`alembic upgrade head` erzeugt das gesamte Agenqo-Datenbankschema auf einer **frischen** Datenbank. Für bestehende, durch `create_all` erzeugte lokale DBs ist vor `alembic stamp` eine individuelle Schema-/Versionsprüfung erforderlich. Die führende Produktionsdatenbank ist MySQL. Die Docker-Compose-Entwicklungsumgebung führt Migrationen vor dem API-Start aus. Für produktive Deployments sollte die Migration separat unter Change Control laufen.

Weitere Details: [Provider-Sicherheits-/Migrationsstand](docs/IDENTITY_MIGRATION_V03.md).

### Erfasste Wirtschaftlichkeit je Anfrage (v0.4)

Das neue [RFQ-Kosten- und Erlösjournal](docs/UNIT_ECONOMICS_V04.md) erfasst variable Kosten **auch bei erfolglosen Anfragen** und tatsächlich belegte Zahlungseingänge. Eine fällige oder erwartete Vermittlungsprovision wird nicht automatisch als bezahlter Umsatz gezählt. Die internen Pilot-APIs liefern eine Kosten-/Erlösübersicht pro Anfrage und aggregiert über den gesamten Pilot. Die Angaben sind **keine** geprüfte Buchhaltung, sondern bislang manuell erfasste operative Messdaten.


### Datenhaltung v0.5 – MySQL + DuckDB, ohne zusätzlichen Datenbankserver

**Verbindlich:** vorhandenes MySQL für Transaktionen, optional eingebettetes DuckDB für anonymisierte Markt-/Kostenanalysen. PostgreSQL ist aus dem aktuellen Deployment und der CI entfernt. MongoDB wird nicht zusätzlich betrieben; eine Anbindung an den bestehenden Dienst ist nur bei Bedarf vorgesehen.

- [Datenbankentscheidung und weitere Donoren](docs/DATENBANK_DONOREN_MYSQL_DUCKDB.md)
- [Optionaler DuckDB-Analyseadapter](agenqo/analytics.py) – rein im Speicher, keine neue Datenbankdatei und keine externe Extension.
- [Alembic-Migrationen](alembic/versions/) – neuer Standard: MySQL, SQLite nur isolierte Tests.
- [Geschützter Liquiditätsbericht](agenqo/api.py) – `GET /v1/admin/analytics/liquidity`.

Lokale Tests: `pip install -e ".[test]"` und `pytest`. Für den echten API-Start müssen MySQL-Zugang und Datenbankschema eingerichtet sein. Es wurden keine Zugangsdaten hinterlegt und keine Daten auf dem vorhandenen Server geändert.


### Anbieterportal v0.6 (authentifiziert, Pilot)

- [Technische Umsetzung, OIDC-Konfiguration und Grenzen](docs/PROVIDER_PORTAL_V06.md).
- `/provider`: Anmelden mit Authorization Code + PKCE, Firmen suchen und übernehmen, Mitgliedschaften und Profilvorschläge bearbeiten, Einladungen und Angebote anzeigen und Buchungen bestätigen.
- Browser-Login bleibt gesperrt, bis ein bestehender/extern bereitgestellter OIDC-Provider mit `AGENQO_OIDC_CLIENT_ID`, Issuer, JWKS und passender API-Audience konfiguriert ist. Es wird kein neuer Identitätsserver gestartet.
- InnoDB-Zeilensperren sichern konkurrierende Käuferfreigaben, Anbieterangebote und Bestätigungen. GitHub Actions führt einen echten MySQL-Konkurrenztest aus.
