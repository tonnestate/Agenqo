# Agenqo

**Eigenständiger KI-nativer Dienstleistungsmarktplatz für Menschen, Unternehmen und autonome Käufer-/Anbieteragenten.**

## Fachlicher Stand (v3.0)

- [Führendes Agenqo-Gesamtkonzept v3.0](docs/AGENQO_GESAMTKONZEPT_V3.md)
- [Branchen- und Leistungskatalog v3.0](docs/AGENQO_BRANCHENKATALOG_V3.md)
- [Konzept v2.0 – historischer Stand](docs/AGENQO_GESAMTKONZEPT.md)
- [Älterer MVP-Plan – bei Widersprüchen gilt v3](docs/MVP_UND_VALIDIERUNG.md)

## Implementierung (Core 0.1.0)

**Neu: Es liegt ausführbarer Backend-Prototypcode vor. Es ist noch kein öffentliches oder produktionsreifes Produkt.**

- [Aktueller Implementierungsstatus und bekannte Lücken](docs/IMPLEMENTIERUNG_STAND.md)
- `agenqo/domain.py`: Zustandsautomaten, Decimal-Beträge, Angebotsfingerprints und Token-Prüfung.
- `agenqo/models.py`: erste eigenständige SQLAlchemy-Transaktionsmodelle.
- `agenqo/api.py`: geschützte Pilot-API für Kundenanfragen, Anbieter-Einladungen, Angebotsabgabe, Prüfung, Freigabe, Buchungsbestätigung und evidenzgestützten Abschluss.
- `tests/`: Fachregel- und API-Integrationstests, ausgeführt über GitHub Actions.
- `docker-compose.yml`: lokales PostgreSQL 16 und Backend, ohne TonnEstate-Laufzeitabhängigkeit.

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

Für Docker Compose sind `AGENQO_DB_PASSWORD` und `AGENQO_ADMIN_KEY` erforderlich. Die API bindet in Compose nur an localhost:8080. Die automatische Tabellenanlage ist nur für lokale Entwicklung vorgesehen.

### Sicherheit und Scope

Die Einladungs-API **versendet noch keine externen Nachrichten**; sie stellt nur manuell zu übermittelnde, zeitlich begrenzte Tokens bereit. Es gibt noch keine produktionsfähige Anbieteridentitätsprüfung, Click-Wrap-Vertragsvorlage, Migrationsverwaltung, Rechnungsstellung, n8n-Sendestrecke, Website oder MCP-Integration.

**Nicht öffentlich deployen, bevor Rechtsprüfung, Authentifizierung, Abuse-Schutz, Schema-Migrationen, Token-Lifecycle und Datenrechtsprüfung abgeschlossen sind.**

## Architekturgrundsätze

Agenqo besitzt eigene Daten, APIs und Geschäftsregeln. TonnEstate, LemonMe, DragonFruitMe, BlackberryMe und CherryMe sind allenfalls geprüfte Donoren. n8n dient als austauschbare Orchestrierung, nicht als verbindliche Geschäftsführung. Dienstleistungen sind der einzige initiale Markt; Produkte sind ausgeschlossen.

**Wirtschaftliches Ziel:** reale, rechtlich zulässige Auftragsvermittlung mit positivem Deckungsbeitrag – einschließlich Kosten für erfolglose Anfragen.
