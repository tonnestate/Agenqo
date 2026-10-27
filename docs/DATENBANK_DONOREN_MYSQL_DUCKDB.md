# Agenqo: Datenbankentscheidung und zusätzliche Donoren

**Entscheidung vom 27.10.2026:** Bestehendes **MySQL** ist das führende transaktionale System. **DuckDB** ist optional als **eingebettete analytische Engine** nutzbar. Vorhandenes **MongoDB** bleibt für dokumentenorientierte Daten eine mögliche Integration, wird durch Agenqo nicht zusätzlich gestartet.

## Verbindliche Architektur

| Aufgabe | Technologie | Grund |
|---|---|---|
| Anbieter, Berechtigungen, RFQs, Angebote, Buchungen, Provisionen, Outbox | **MySQL (bereits vorhanden)** | Mehrbenutzertransaktionen, Fremdschlüssel, row-level locking mit InnoDB |
| Marktplatz-Kennzahlen, Regionen, Angebots-/Nachfrage-Analysen | **DuckDB `:memory:`** | Eingebettete vektorisierte SQL-Analyse ohne zusätzlichen Server |
| Unstrukturierte Webdokumente/Quellenbelege (optional) | Vorhandenes MongoDB | Nur nach Quellen- und Datenschutzprüfung |

**PostgreSQL wird nicht verwendet.** Das Deployment-Compose enthält ausschließlich den Agenqo-API-Dienst; die MySQL-Datenbank läuft separat auf dem vorhandenen System. GitHub Actions verwendet einen kurzlebigen MySQL-Testcontainer, keinen zusätzlichen Produktionsdienst.

## Umsetzung

- `AGENQO_DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:3306/agenqo?charset=utf8mb4` als vom Betreiber bereitgestellte Variable.
- `docker-compose.yml` referenziert ausschließlich die bestehende MySQL-Datenbank. In Linux-Docker lässt sich bei Bedarf `host.docker.internal` über host-gateway erreichen. **Keine Zugangsdaten committen.**
- SQLAlchemy/PyMySQL sind operative Persistenz; Alembic-Migrationen werden auf frischem MySQL 8.4 in CI getestet.
- SQLite ist nur für ausdrücklich freigegebene lokale Entwickler-/Unit-Testumgebungen erlaubt (`AGENQO_ALLOW_SQLITE_DEV=1`).
- `agenqo/analytics.py` erstellt eine DuckDB-In-Memory-Verbindung, verarbeitet nur Kategorie, **zweistellige PLZ-Region**, bestätigte Buchungen sowie zuvor protokollierte Kosten/Einnahmen und schließt die Verbindung danach. Keine PII-Exporte oder dauerhafte DuckDB-Datei. Kein DuckDB-MySQL-Schreibzugriff.
- `GET /v1/admin/analytics/liquidity` ist der geschützte Marktplatzbericht (anfragebasierte Auswertung inklusive Nichtabschluss).
- Noch keine Einbindung des bestehenden MongoDB, keine automatische Analytik-Synchronisation, keine produktiv aufgenommene Nutzer-/Anbieterkommunikation.

## Neue GitHub-Donoren und Bewertung

| Repo | Lizenz nach GitHub | Möglicher Nutzen | Aktueller Status |
|---|---|---|---|
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | MIT | Embedded OLAP, JSON/Parquet-Analytik, Marktliquidität | **Eingebaut: `duckdb` Python optional** |
| [duckdb/duckdb-mysql](https://github.com/duckdb/duckdb-mysql) | MIT | Direkte SQL-Leseabfragen auf existierendem MySQL ohne Export | **Option, nicht installiert** |
| [duckdb/duckdb-spatial](https://github.com/duckdb/duckdb-spatial) | MIT | Geografische Distanz-/Gebietsanalysen, Polygon-Überdeckung, GDAL | **Option, nicht installiert** |
| [PyMySQL/PyMySQL](https://github.com/PyMySQL/PyMySQL) | MIT | SQLAlchemy-MySQL-Treiber | **Integriert** |
| [pola-rs/polars](https://github.com/pola-rs/polars) | MIT | Alternative große DataFrame-/Parquet-Pipelines | **Derzeit redundant zu DuckDB** |
| [ibis-project/ibis](https://github.com/ibis-project/ibis) | Apache-2.0 | Einheitliche Anfrageschicht für viele Engines | **Später prüfen** |
| [apache/superset](https://github.com/apache/superset) | Apache-2.0 | Dashboarding / BI | **Derzeit für Concierge-MVP zu aufwendig** |

Die offizielle DuckDB-Dokumentation beschreibt direkte MySQL-Abfragen und räumliche Funktionen. Die DuckDB-MySQL-Extension kann auch schreiben; in Agenqo wird **bewusst kein schreibfähiger Adapter installiert**. Bei künftiger direkter Datenbankanbindung: separate **read-only** MySQL-Berechtigungen und DuckDB-Secret-Management, kein Passwort im `ATTACH`-SQL-String.

**Nuance bei Parallelität:** Neuere DuckDB-Versionen unterstützen neben parallelen Threads auch zusätzliche Multi-Prozess-Optionen wie das Quack-Protokoll. Für Agenqos gleichzeitige, unmittelbar bindende Buchungs- und Geldzustände bleibt vorhandenes MySQL mit InnoDB derzeit die einfachere, bereits vorhandene Wahl. DuckDB kann innerhalb derselben Architektur anspruchsvolle Analysen und Matching-Vorselektion ermöglichen.

## Prüfung vor externer Nutzung

1. Tatsächliche vorhandene MySQL-Version und Rechte sowie Tabellen-Präfix/Datenbankschema prüfen; CI belegt **MySQL 8.4**, nicht alle Vorgängerversionen.
2. In MySQL Transaktionssperren, Idempotenz und Revisionen unter Konkurrenz testen. Gegenwärtige App-Level-Checks sind kein Ersatz für Row Locks/optimistische Sperren.
3. Bei DuckDB auch Erweiterungen und Netzwerkrechte restriktiv halten. `INSTALL mysql`/`INSTALL spatial` sind keine erforderlichen MVP-Startoperationen.
4. Für Golden-Record-Provenienz und große Unternehmenskataloge zunächst bestehende Daten nutzen und Importberechtigungen klären; **kein Kopieren fremder Mandantendaten**.
5. End-to-End nachweisen, dass Kosten je Anfrage, Anbieterreaktionen und erfolgreiche Vermittlungen real gemessen werden.

**Status:** Architektur umgesetzt; kein produktiver Datenbankumzug auf dem Nutzer-Server, keine Beschaffung echter MySQL-Zugangsdaten und keine Aussage über tatsächlich dort vorhandene Tabellen.
