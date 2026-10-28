# Agenqo v3.0 — P0-Ausführungsvertrag für die Vermittlungszentrale (ACX)

**Stand:** 28.10.2026  
**Status:** verbindliche Umsetzungsvorlage / kein Nachweis eines Produktivstarts  
**Führendes Zielbild:** [Gesamtkonzept v3.0](AGENQO_GESAMTKONZEPT_V3.md)  
**Taxonomie:** [Branchenkatalog v3.0](AGENQO_BRANCHENKATALOG_V3.md)  
**Technische Ist-Entscheidung:** [MySQL + DuckDB](DATENBANK_DONOREN_MYSQL_DUCKDB.md)

## 0. Zweck und Verbindlichkeit

Dieses Dokument übersetzt das ACX-Zielbild in einen überprüfbaren ersten Betriebs- und Umsatzkreislauf. Es ersetzt **nicht** die übergreifende B2C-/B2B-/Agentenstrategie. Es priorisiert ausdrücklich Implementierungen gegenüber weiteren Konzeptrunden.

**Geschäftskreislauf:** autorisierter Bedarf → qualifizierte Leistungspakete → geeignete Anbieter → rechtlich zulässiger Kontakt / freiwillig abonnierte RFQ → echte vergleichbare Angebote → kundenseitige autorisierte Wahl → anbieterseitige Bestätigung → dokumentierte Durchführung / Streitfall → tatsächlich vereinnahmte Plattformgebühr → kohortenbasierter Deckungsbeitrag inklusive Fehlversuche.

**P0:** Ein vollständiger erfolgreicher und ein gescheiterter Vorgang müssen Ende-zu-Ende korrekt, belegbar, rechtskonform und wirtschaftlich nachverfolgbar durchführbar sein. Erst danach werden 20–50 reale Vorgänge als Marktvalidierung ausgewertet. Dieses Ziel ist nicht gleichbedeutend mit Produktivbetrieb oder rechtlicher Freigabe.

## 1. Kontrollierter Ist-Stand (Quelle: GitHub main am 28.10.2026)

- Python/FastAPI, SQLAlchemy, PyMySQL, MySQL/InnoDB und Alembic-Migrationen 0001–0003; ein neuer PostgreSQL-/PostGIS-Server ist **nicht** beabsichtigt.
- DuckDB ist für eingebettete Analytik optional, nicht transaktionales System of Record.
- Deterministische Domain-Regeln, Angebots-Fingerprints, einfache RFQ-/Invitation-/Quote-/Booking-/Commission-States, OIDC-gebundenes Provider-Portal und RFQ-Kostenjournal sind als Quellcode vorhanden.
- n8n/MySQL-Outbox-Brücke v0.7: atomare Claims/Leases, interne Review-Tasks, Retry/Dead-Letter; Workflow ist laut Betriebsdokumentation noch nicht auf einer laufenden Instanz aktiviert; kein produktiver E-Mail-Versand nachgewiesen.
- Käufer-Frontend für selbstständige B2C/B2B-RFQs, rechtlich freigegebener externer Versand, vollständige Contact-Policy-Engine, reife Geo-/Kapazitätslogik, Quote-Revisionen und Dispute-UI sind nicht als vollständig validiert anzusehen.
- API-Router in agenqo/api.py sind stark gebündelt; provider_portal.py nutzt gemeinsame Funktionen aus api.py. Ein Big-Bang-Refactoring ist kein zulässiger Ersatz für fehlende Pilotfunktionen.

**Doku-Konflikt:** v3.0 erwähnt noch PostgreSQL und PostGIS, obwohl die später dokumentierte verbindliche Datenbankentscheidung MySQL + DuckDB lautet. Für sämtliche neuen Tickets gilt **MySQL/InnoDB als transaktionaler Bestand**. Eine abweichende DB-Architektur benötigt eine explizite ADR und eine Migrationsentscheidung, nicht nur einen Textwechsel.

## 2. Produkt-USP, aus Sicht beider Marktseiten

**B2C:** „Einmal beschreiben, welche Arbeit erledigt werden soll. Agenqo fragt passende Dienstleister, sammelt reale vergleichbare Endpreise und Termine, erklärt die Unterschiede und begleitet die bestätigte Buchung.“ Angebotshäufigkeit und Reaktionsgeschwindigkeit werden erst nach Pilotdaten zugesichert.

**B2B:** „Mehrere Standorte und Gewerke in einem Auftrag; kontrollierte Angebotseinholung, transparente Freigaben, Kostenstellen-/Budgetreferenzen und Wiederholungsaufträge.“ Ein Projekt besteht aus einzeln beschaffbaren WorkPackages.

**Dienstleister:** „Keine Pflicht zu KI oder neuer Software. Qualifizierte Anfragen mit klarem Scope und realem Käuferinteresse; Antwort über sicheren Link, Portal, API oder eigenen Agenten; keine Lead-Abrechnung ohne ausdrückliche Vereinbarung.“ Die tatsächliche Abschlussquote, Akquisitionsersparnis und faire Gebührenhöhe sind zu messen, nicht zu behaupten.

**Agenten:** ein stabiler, dokumentierter Remote-API-/MCP-Einstieg für Suche, RFQ und Status. Ein Anbieteragent kann indikative Angebote liefern und **nur innerhalb einer nachgewiesenen Organisationsvollmacht und Preis-/Kapazitätsregel** verbindlich handeln. Asynchrone Arbeit mit persistentem RFQ/Job-ID, Polling/Webhooks und Ablaufzeiten statt mehrtägigem synchronem Toolaufruf.

## 3. ACX als kanonische Vermittlungszentrale

Es gibt einen fachlich führenden RFQ/Project/WorkPackage-Datensatz, unabhängig von Anfrage- und Angebotskanal. Implementierungen verwenden dieselben Domänenservices und Zustandsübergänge.

1. **Intake:** Buyer (Gast mit gesichertem Link, registriert, Unternehmen oder delegierter Agent) liefert Leistungsort/-umfang/-termin, Dateien und ausdrückliche Anfrage- und Datenfreigaben.
2. **Qualification:** Service-Schema, Risikokategorie, fehlende Merkmale, verbotene oder genehmigungspflichtige Tätigkeiten.
3. **Matching:** ServiceCapability + Einsatzgebiet + harte Qualifikationen + Kapazitäts-/Verfügbarkeitsgrad + Anfahrts-/Mindestpreisregel; nur zulässige Kandidaten.
4. **Channel Planner:** priorisiert registrierte opt-in-Partner, deren Agenten/Webhooks, öffentliche eigene RFQ-Börse, manuell geführte Einzelfallansprache und erst nach vertraglicher Freigabe Drittplattformen.
5. **Legal Dispatch Gate:** jeder Zustellversuch braucht eine erfolgreiche kanalbezogene Policy-Entscheidung; n8n darf keine eigene rechtliche Freigabe generieren. DENY ist Standard.
6. **Submission:** menschliches Angebot via Portal/Quote-Link oder signiertes maschinelles Angebot, jeweils mit Zeit, Source, Revision, Bindungsstatus, Leistungsausnahmen, Netto-/Bruttobetrag und Steuerbehandlung.
7. **Comparison:** vollständige Leistungs-/Preisvergleichbarkeit; fehlende Positionen werden sichtbar markiert. INDICATIVE ist keine verbindliche Offerte.
8. **Buyer Authorization:** exakte Angebotrevision/Fingerprint, Kostenobergrenze, Laufzeit und Identität; rechtsverbindlicher Schritt nur nach passenden Verbraucher-/B2B-Bedingungen.
9. **Provider Confirmation:** separater bestätigender Zustandsübergang; verbindliche Buchung nur nach erforderlichen Annahmen/Schritten.
10. **Fulfillment & Dispute:** Ausführungsnachweis, Storno-/Reklamationsfenster und widersprechende Evidenz; keine fiktive Auftragsdurchführung allein aus Schweigen.
11. **Settlement & Analytics:** Provision/kundenseitige Gebühren nur auf wirksamer Vertragsgrundlage; Umsatz erst als realisiert zählen, wenn vereinnahmt und belegt. Fehlversuche erzeugen ausdrücklich Kostenereignisse.

## 4. Anbieterkatalog, Registrierung und Kontaktwege

**Getrennte Zustandsachsen** statt einer einzigen Anbieter-Stufe:
- Discovery: DISCOVERED / SOURCE_REVIEWED / VERIFIED_DATA;
- Ownership: UNCLAIMED / CLAIM_PENDING / CLAIM_VERIFIED;
- Communication: UNKNOWN / RFQ_OPT_IN / CHANNEL_APPROVED / SUPPRESSED;
- Commercial: NO_AGREEMENT / TERMS_ACCEPTED / CONTRACTED;
- Integration: MANUAL / PORTAL / WEBHOOK / PROVIDER_AGENT;
- Capability: LISTED / RFQ_ENABLED / AGENT_QUOTABLE / BOOKABLE / PAUSED.

Ein recherchiertes Firmenprofil darf – nach Quellen-/Datenschutzprüfung – vorhanden sein, ohne dass der Betrieb Kunde, Vertragspartner, einwilligender Empfänger oder verifizierter Profilinhaber ist. Claim-Your-Business erfordert Nachweis der Vertretungsmacht. Das Unternehmen sieht Quellen und eigene Behauptungen getrennt.

**Für den Pilot grundsätzlich:** 10–15 persönlich gewonnene Anbieter, dokumentierte Kommunikationspräferenzen, gebilligte Vertragsbedingungen, geeignetes Einsatzgebiet und geprüfte Qualifikation. Kein automatischer Erstkontakt mit fremden E-Mail-Adressen aus recherchierten Daten.

**Rechtliche Trennung:** Eine DSGVO-Rechtsgrundlage für die Verarbeitung von Kontaktdaten beantwortet **nicht** die eigenständige UWG-Frage, ob der konkrete Kommunikationskanal zum konkreten Zweck genutzt werden darf. Für werbliche E-Mails ist eine ausdrückliche Einwilligung grundsätzlich nötig, sofern nicht die Voraussetzungen einer engen gesetzlichen Ausnahme bestehen. Die B2B-„mutmaßliche Einwilligung“ betrifft insbesondere bestimmte werbliche Telefonanrufe und begründet keine pauschale E-Mail-Erlaubnis. Ob eine individuelle, im Namen eines realen Käufers versandte Anfrage als Werbung einzustufen ist, bedarf einer konkreten rechtlichen Prüfung; bis dahin keine automatisierte Cold-Mail-RFQ als Standardkanal. Quelle: https://www.gesetze-im-internet.de/uwg_2004/__7.html

**ContactPolicyDecision je Dispatch (Mindestfelder):** request_id, package_id, provider_id, recipient_contact_id, purpose, buyer_authorization_id, channel, gdpr_legal_basis, uwg_classification, consent_or_exception_evidence, source_reference, policy_version, suppression_checked_at, cooldown_until, reviewed_by_or_rule_id, decision(ALLOW/REVIEW/DENY), decision_at, explanation_code. Ein positiver Datensatz erlaubt nur den genau geprüften Kontakt, nicht ein generelles Newsletter-/Outreach-Recht. Opt-out blockiert relevante Folgemitteilungen. Kein Datenabfluss an n8n bei DENY.

**Drittportale:** MyHammer, Kleinanzeigen und andere Kanäle werden als ChannelAdapter mit Status MANUAL_ONLY, CONTRACTED_API, PROHIBITED, REVIEW_REQUIRED geführt. Keine automatisierte Account-Bedienung, Datenabsaugung, Fremdauftragsausschreibung oder kommerzielle Rückführung fremder Daten ohne geeignete Rechte. Sie sind Zusatzkanäle, niemals führendes RFQ-System.

## 5. Eignung und Umkreissuche

Einsatzgebiet ist **nicht** identisch mit Entfernung zum Firmensitz.

**MVP-Hard-Filters:** (a) Servicecode/Capability, (b) PLZ-/Gebietsabdeckung, (c) relevante Berechtigung/Haftpflicht soweit erforderlich, (d) aktiver Channel, (e) Termin-/Sperrstatus. Ein Treffer wird als „anfragbar“, „vorläufig verfügbar“ oder „verbindlich bestätigt“ getrennt gekennzeichnet.

**Route- und Kostenmodell (nur final qualifizierte Kandidaten):**
- Betriebsstandort/Depot, Standort des Auftrags und ggf. Zieladresse getrennt.
- ServiceArea-Regel: POLYGON, POSTAL_LIST, ROAD_TIME_LIMIT, RADIUS_APPROX, REGIONAL_NATIONWIDE, REMOTE; pro Kategorie und Anbieter individuell.
- Kostengünstiger geo-/PLZ-basierter Vorfilter; dann für Shortlist optional zeit- und kostenkontrollierter Routing-Dienst. Straßen-km sind nicht Luftlinie, und prognostizierte Fahrtzeit ist keine Garantie.
- Anbieter hinterlegt max. Reisezeit, Anfahrtpauschale, Kilometerstaffel, Mindestauftragswert, Tages-/Wochenkapazität. Ohne verifizierte Kalenderdaten nie „sofort frei“ behaupten.
- Entrümpelung: Volumen, Stockwerk, Parken, Müllarten, Aufzug, Entsorgungsnachweise; Umzug: Quell- UND Zielort; Fotografie: Terminfenster, Bildrechte und Reisezeit; Drohnen: Wetter-/Luftraum-/Operator-/Pilot-Gates.
- Implementierung kompatibel zu **MySQL und bestehenden Deployments**; bei komplexen Geometrien geeignete MySQL-Spatialfunktionen/Anwendungslogik oder zulässige eingebettete Analyse. Kein PostGIS-Zwang, keine neue Datenbank als Prämisse.

Metriken: Precision@k nach erfüllter ServiceArea, Einladungs-Fehlquote, Median Fahrtzeit der gebuchten Anbieter, tatsächliche Anfahrtsabweichung, Anteil falscher „verfügbar“-Anzeigen, Kosten je Route-API-Abfrage.

## 6. Vollständiger Katalog vs. aktivierter Markt

Der v3-Branchenkatalog mit 24 Domänen ist die **Such- und Datenarchitektur**, nicht eine Zusage, dass sämtliche Leistungen in Deutschland buchbar sind.

- LISTED: fachliche Discovery und Anbieterprofil, gegebenenfalls keine aktive Anfrage.
- RFQ_ENABLED: geprüftes RFQ-Schema, geeignetes rechtliches Gate, sinnvolle Anbieter- oder Sourcingbasis.
- AGENT_QUOTABLE: Preise und Kapazitäten aus überprüften Anbieterregeln maschinell berechenbar; INDICATIVE/BINDING unterscheiden.
- BOOKABLE: verifizierte Geschäfts-/Vertretungs-/Vertrags-/Terminlogik.
- PAUSED: rechtlicher/qualitativer/operativer Stop.

**Pilotbuchbar:** Entrümpelung/Haushaltsauflösung in begrenzter Region, B2C und B2B. **Benachbarte Lernkategorien:** allgemeine Fotografie, Drohnenfotografie und Reinigung dürfen im Katalog/als begrenztes RFQ vorkommen, aber nicht vor dem jeweiligen Fachgate als sofort buchbar beworben werden.

## 7. Einheitliche API und Agenten-Readiness

Drei Interfaces, ein Geschäftsprozess:
- Buyer Web: Request anlegen, Dateien, Angebote vergleichen, Fingerprint-Version freigeben, Status/Storno/Dispute sehen.
- Provider Web / Quote-Link: Einladungen, Angebote/Revisionen, Anfahrt/Termine, bestätigte Buchungen, Profil-Claim.
- Buyer-/Provider-Remote MCP: dieselben Business-APIs, eigene rollen- und objektbezogene OAuth-Scopes, delegierte Mandate, Rate Limits, Idempotency-Key und Audit.

Technische Trennung: routes/admin.py, routes/customer.py, routes/provider.py, routes/quotes.py, routes/bookings.py, routes/analytics.py; domain-Funktionen bleiben rein; Services/Use-Cases bündeln Transaktionen. Keine neuen Fachentscheidungen in Routern oder n8n. Bei jeder P0-Änderung die berührten Endpoints aus der alten api.py herauslösen und Regressionstests verlangen; **kein** großflächiges Refactoring als ungeprüften P0-Blocker.

API-Responses: einheitliche Problem-Details (RFC 9457), dokumentierter 401/403/409/410/422-Vertrag, Token-Rotation/-Widerruf/-Ablauf, kontrollierte Scope- und Leak-Tests. Anbieter A darf keine Angebote von Anbieter B sehen. Gasttoken-Zugriff wird streng auf einen Vorgang begrenzt.

## 8. P0-Tickets mit prüfbarer Definition of Done

| ID | Priorität | Umsetzung | Abnahmekriterium |
|---|---|---|---|
| P0-01 | BLOCKER | Contact Policy + auditierte kanalbezogene Freigabe | Standard DENY; Test: ohne Freigabe kein Versand, Sperrliste immer geprüft, Rechtsversion gesichert |
| P0-02 | BLOCKER | Buyer-Frontend B2C/B2B | Gast-/Organisations-Intake → eigene Statusseite → Vergleich → exakt revisiongebundene Freigabe; Tests |
| P0-03 | BLOCKER | End-to-End-Zustände Quote-Revision, Storno, Completion, Dispute | abgelaufene/geänderte Offerte nicht buchbar; widersprochener Abschluss erzeugt keine unbestrittene Provision |
| P0-04 | BLOCKER | Freigegebener Auslieferungsadapter über vorhandene Outbox/n8n-Brücke | nur ALLOW-Ereignisse, dedupliziert, Retry/Dead Letter, Zustell- und Bounce-/Opt-out-Nachweis |
| P0-05 | BLOCKER | Wiederverwendbare fachliche Matching-/ServiceArea-Regeln | zwei PLZ- und zwei Kategorievarianten, harte Ausschlüsse und Kandidatenbegründung dokumentiert |
| P0-06 | BLOCKER | Verifiziertes Pilot-Onboarding und kommerzielle Bedingungen | 10–15 zustimmende Betriebe; ein Vertrag/Kommunikationspräferenz je Betrieb; reale Qualifikationen |
| P0-07 | BLOCKER | Unit-Economics bei Erfolg UND Misserfolg | jede RFQ hat Kostenquelle, Zeit, Kanal, Zahlungsnachweis; unbezahlte Forderung nicht als realisierter Umsatz |
| P0-08 | BLOCKER | Sicherheits-/Betriebstests | Token-Ablauf/Rotation/Revocation, Multi-Tenant, Race-Tests, CI, DB-Migrationen und Restoretest |
| P0-09 | BLOCKER | Rechts-/Datenschutz- und Verbraucherprozessprüfung | verifizierte Kanal-, Vermittlungs-, AGB-, Widerrufs-, Daten- und Abfallfachrechtsregeln vor Livekontakt |
| P0-10 | GATE | Vollständiger Staging-Loop | Erfolgsfall mit zwei Anbietern UND ein erfolgloser/stornierter Fall über UI und Outbox mit Audit/Economics |
| P1-01 | nach G1 | Provider Claim & Dashboard ausbauen | Vertreterprüfung, Profiländerung, Einladungen, Angebot, Termine, Provision |
| P1-02 | nach G1 | Agenten-API-Vertrag / Remote MCP in kontrollierter Beta | Such- und RFQ-/Status-Tools, Scope-Tests; bindende Aktionen separat freigeben |
| P1-03 | nach G1 | Anbieter-Premium-/B2B-Gebühren-Experiment | vertraglich sauber, kohortenrein, keine Doppelvergütung ohne Offenlegung |
| P2-01 | nach G2 | Drittportale und mehr Kategorien/Regionen | pro Adapter nachgewiesene Nutzungsrechte und Kanalprofitabilität |

**Unmittelbare Reihenfolge:** P0-01, P0-02 und P0-06 **parallel** beginnen (Recht/Partnerakquise/Buyer UI); P0-03–05 und P0-07–08 in schmalen vertikalen Slices anschließen; erst nach P0-09/10 echte externe Kommunikation und reale Buchungen. P0-01 allein ist keine Rechtsprüfung; Software kann rechtswidrige Zwecke nicht legalisieren.

## 9. Pilot-Gates: wirtschaftliche und fachliche Evidenz

**G0 – vor externen Pilotkontakten:** dokumentiertes zulässiges Kontaktverfahren; rechtlich geprüfte Vertragsstruktur, 10–15 opt-in-Anbieter als Ziel, erste reale Nachfragequellen und funktionsfähige interne Testumgebung.

**G1 – technische und betriebliche Schleife:** ein realer, autorisierter End-to-End-Buchungsfall und ein nicht erfolgreicher Fall; keine unautorisierten Sendungen, keine Cross-Tenant-Datenpannen, vollständiger Audit- und Wirtschaftsnachweis. Eingegangene oder fällige Gebühren differenzieren.

**G2 – Marktbeobachtung:** zunächst 20–50 echte RFQs, im Vorfeld festgelegte Schwellen; Segmentierung nach B2C/B2B, Kategorie, Region, Kanal, Auftragswert und Anbieter-Antwortweg. Stichprobe als explorativ kennzeichnen, keine statistische Marktführerschaft daraus ableiten.

Vor Pilotstart zu fixierende Zielwerte als **Hypothesen, nicht wissenschaftliche Garantien**:
- 100 % der externen Einladungen besitzen überprüfbare positive Contact-Policy-Entscheidung.
- 100 % der Buchungen basieren auf gültiger, exakt referenzierter Angebotsversion und erforderlicher Autorisierung.
- >/= 70 % der qualifizierten RFQs erhalten innerhalb von 72 h mindestens ein vergleichbares Angebot.
- >/= 50 % erhalten innerhalb von fünf Kalendertagen mindestens zwei vergleichbare Angebote.
- >/= 20 % der qualifizierten RFQs werden gebucht; separate Auswertung „durchgeführt“ und „Provision vereinnahmt“.
- Sämtliche RFQs (auch Fehlschläge) besitzen vollständige manuelle Zeit-/Kanal-/KI-/Reisekostenaufzeichnungen.
- Kohorten-DB/RFQ: reale Erlöse minus sämtliche direkt zurechenbaren RFQ- und Akquisitionskosten. Zusätzlich DB/Buchung und DB/aktive Anbieterorganisation berichten.
- Wiederholungsauftrag/Provider-SLA, tatsächlicher Fahrkostenfehler, Kundenzufriedenheit und Anbieterattraktivität erfassen.

**Kein automatisches „Stop“ bei einem einzigen kleinen Sample:** Schwellen und Risikogrenzen vorher festlegen; nach 20 Fällen über Weiter / begrenzter Anpassungstest / Stop entscheiden. Sicherheits-/Rechtsverletzungen sind unabhängig davon Stop-Ereignisse.

## 10. Demand-Akquise und skalierbare Distribution

**B2C:** SEO auf echten kategorien-/regionenbezogenen Fragen, gezielte eigene Inserate, Empfehlungen, nachvollziehbare Verbraucher-Preisbeispiele und Short-Form-Videos. 10.000–20.000 KI-Videos sind keine Wachstumsgarantie; Start mit kontrollierten kreativen Kohorten und Tracking von View → Klick → qualifizierte RFQ → Buchung → wirtschaftlichem Beitrag. Spam-/Urheber-/Werberegeln der Plattformen beachten.

**B2B:** Hausverwaltungen, Makler, Nachlass, kleine Filialketten, Facility-Management; bezahlte Beschaffung bzw. wiederkehrende RFQs erst mit realen Wiederholungsraten bewerten.

**Agentenvertrieb:** öffentliche Tool-Dokumentation, stabiler Remote-Endpunkt, Maschinenlesbarkeit, Entwicklerbeispiele, Rate Limits und echte Kundenberechtigung. Discoverability garantiert keine Integration in ChatGPT/Claude; Nutzung muss separat gemessen werden.

**Drittportale:** rechtlich erlaubter Zusatzkanal mit gesondertem CAC/Fees, ohne Unternehmensdaten oder Kontakte widerrechtlich zu übernehmen.

## 11. Betriebs- und Sicherheitsnachweise

Mindestens erforderlich: JSON-Logs mit correlation_id, request_id, package_id, invitation_id, booking_id; keine personenbezogenen Inhalte/Token in Standardlogs. DB-/Migration-/Outbox-Health, sichere Berechtigungsfehler, Rate Limits je IP/Organisationskonto/Token, Token-Hashing, Version/Revoke, stornierungsfeste Angebotsrevisionen, strukturierte Alarmierung bei Dead-Letter, wiederherstellbares Backup und verständliche Betreiber-Handbücher.

**CI ≠ Produktion:** Code, Tests, importierbare Workflows und ein deaktivierter n8n-Plan dürfen nie als aktiv zugestellt, produktiv überwacht oder rechtlich freigegeben dargestellt werden.

## 12. Offene sachliche Entscheidungen

1. Exakte Organisation/Vertragspartei und Zuständigkeit im Verhältnis zu bestehenden Immobiliengeschäften.
2. Rechtsbewertung konkret beauftragter RFQs gegenüber unregistrierten Betrieben nach Kanal/Absenderrolle.
3. Pilotregion, Providerkohorte, gewerbe-/abfallrechtlicher Qualifikationsnachweis.
4. Transparente B2C-/B2B-Preisexperimente; Provision, kundenseitige Gebühr und Premium sauber trennen.
5. Geo-/Route-Anbieter und monatliche harte Spend Limits für API/LLM/Kommunikation.
6. Integrationsgenehmigungen fremder Plattformen; bis dahin MANUAL_ONLY/REVIEW_REQUIRED.
7. Verantwortliche Abnahmeinstanz und Unterschrift unter Pilot-Gates vor Start.

## 13. Prioritätendisziplin

Neue Architektur-, Dashboard-, MCP-, Verhandlungs-, Blockchain-, Drittplattform- und Marketing-Funktionen dürfen P0-01 bis P0-10 **nicht** verdrängen. Es gibt keinen neuen Datenbankserver und keinen Rewrite von v3 als Ersatz für fehlende End-to-End-Nachweise.

Quellen: [v3.0](AGENQO_GESAMTKONZEPT_V3.md), [aktueller Implementierungsstand](IMPLEMENTIERUNG_STAND.md), [n8n-Brücke v0.7](N8N_ORCHESTRATION_V07.md), [Datenspeicherentscheidung](DATENBANK_DONOREN_MYSQL_DUCKDB.md), § 7 UWG (https://www.gesetze-im-internet.de/uwg_2004/__7.html), aktuelle MyHammer-Nutzungsbedingungen (https://www.my-hammer.de/allgemeine-geschaefts-bedingungen).
