# Agenqo – MVP-, Integrations- und Validierungsplan

**Stand:** 27. Oktober 2026 · **Version:** 1.0 · **Bezug:** [Gesamtkonzept](AGENQO_GESAMTKONZEPT.md)

## 1. Ziel und Nichtziele

**Ziel:** Ein vollständig eigenständiges Webprodukt nimmt einen realen Entrümpelungsauftrag entgegen, ermöglicht mindestens zwei tatsächlich geeigneten Anbietern strukturierte Angebote, erstellt einen transparenten Vergleich, führt bei Bedarf eine zulässige Nachverhandlung, nimmt die autorisierte Entscheidung des Kunden entgegen, dokumentiert die Anbieterbestätigung und erfasst die wirtschaftlichen Ergebnisse.

**Nichtziele des ersten Durchlaufs:** Produkte, Idealo/Geizhals, flächendeckende deutsche Dienstleisterabdeckung, autonomes Bezahlen, ein verpflichtender MCP-Client für Nutzer, hundert Dienstleistungskategorien, ein zweites CRM oder automatisierte Kaltkontakt-Massenkampagnen.

Agenqo darf in keinem Kernprozess davon abhängen, dass TonnEstate erreichbar ist.

## 2. Architekturvertrag

### 2.1 Eigene Kernkomponenten

- **Agenqo Backend:** Autorisierungs- und Geschäfts-APIs, Request/Offer/Booking/Commission State Machines.
- **Agenqo DB:** Identitäten, Kontakte, Provenienz, Services, Mandate, Angebote, Transaktionen, Audit.
- **Agenqo Website:** Öffentliches Portal, Käuferkonto, Anbieter-Claim/Onboarding, Profil- und Angebotsverwaltung, Vergleich und Buchungsfreigabe.
- **Agenqo n8n Workflows:** Zustellung, Eingang, Erinnerung, Eskalation. n8n besitzt keine führende Auftrags- oder Provisionsbuchführung.
- **Agenqo Agent Service:** strukturierte Interpretation und Vorschläge; bei fehlender Verlässlichkeit menschliche Nacharbeit.
- **Agenqo API/MCP Gateway:** spätere Buyer-/Provider-MCPs, dieselben Business-Operationen wie die Website.

### 2.2 Austauschbare Donoren

Die existierenden TonnEstate-Komponenten für ProviderOrder, Notare, GoldenCompany, Verhandlungsmandate, Kalender, Outbox und signierte n8n-Events sind **Vorlagen**. Vor Code-Portierung sind Lizenz, Abhängigkeiten, Mandantenannahmen und Testbarkeit zu prüfen.

Externe Quellen werden nur über klar versionierte Importadapter und verifizierte Nutzungsrechte angebunden. Kein versteckter Schreibzugriff auf die ursprüngliche CRM-Datenbank.

### 2.3 Systemzuständigkeit

| Fachobjekt | Verantwortliches System |
|---|---|
| Anbieteridentität/Golden Record | Agenqo DB/Golden Record Service |
| Anbieter-Mitgliedschaft und Rollen | Agenqo IAM |
| Dienstleistungs- und Angebotsdefinition | Agenqo Service/Offer Engine |
| Anfragen, Mandate, Buchungen | Agenqo Transaction Engine |
| Nachweisbare Nachrichten und Wiedervorlage | Agenqo DB plus n8n Transport |
| Fachliche Preis-/Gebührenregeln | Agenqo Pricing/Billing |
| LLM-Interpretation | Agenqo Agent Service mit Beleg/Unsicherheit |
| Zahlungsdienstleistungen | Externer lizenzierter PSP, nicht n8n |

## 3. Kern-Stories und Abnahmen

### Käufer

**B-01** Ich kann ohne KI-Installation ein Anliegen im Browser beschreiben und eine Request-ID erhalten.  
**B-02** Ich erkenne, ob angebotene Preise Schätzungen, Angebote mit Vorbehalt oder verbindlich sind.  
**B-03** Ich kann Angebote einschließlich Steuern, Anfahrt, weiteren Pflichtkosten, Leistungsumfang und Termin vergleichen.  
**B-04** Ich kann ein begrenztes Verhandlungsmandat erteilen und widerrufen.  
**B-05** Ich kann exakt das zuletzt bestätigte Angebot autorisieren; nach Angebotsänderung muss ich erneut freigeben.  
**B-06** Ich kann Buchung, Storno und Reklamation nachverfolgen.

### Anbieter

**P-01** Ich kann einen neuen Betrieb registrieren oder ein vorhandenes Unternehmen nach Autorisierungsnachweis beanspruchen.  
**P-02** Ich kann Leistungen, PLZ-Einsatzgebiete und Kontaktkanäle pflegen; historische Quellen werden dabei nicht überschrieben.  
**P-03** Ich kann ohne Account via begrenztem Quote-Link eine einmalige, zu meinem Vorgang passende Angebotsabgabe durchführen.  
**P-04** Ich kann Bruttopreis, Steuern, Anfahrt, Termin, Gültigkeit und Vorbehalte eindeutig erfassen.  
**P-05** Ich kann ein überarbeitetes Angebot mit neuer Version bestätigen; alte Versionen bleiben revisionssicher.  
**P-06** Ich kann später Mitarbeiter und eigene Agenten mit eingeschränkten Berechtigungen registrieren.

### Plattform

**A-01** Geschäftsvorfälle sind idempotent; wiederholte Webhooks lösen keine doppelte Annahme aus.  
**A-02** Es gibt keinen verbindlichen Auftrag ohne freigegebenes, unverändertes Angebot und bestätigenden Anbieter.  
**A-03** Kommerzielle Beziehungen beeinflussen das neutrale Haupt-Ranking nicht verdeckt.  
**A-04** Provisionen werden ausschließlich nach geprüftem Vertrag und nachweisbarem Auslöser angesetzt.  
**A-05** Alle Eingaben, Annahmen, Angebotsversionen und Bearbeitungsschritte sind dokumentiert.  
**A-06** Die Plattform bleibt ohne TonnEstate-Konnektivität und ohne KI-Modell grundsätzlich bedienbar.

## 4. Funktionaler MVP-Durchlauf

**Schritt A:** Kunde gibt Ort, Objektgröße, Volumenhinweise, Etagen, Zugang, Sondergegenstände und Wunschtermin ein. Fotos sind optional und gesondert geschützt. KI-Sichtanalyse markiert Schätzungen als unsicher.

**Schritt B:** Search/Match wählt eine begrenzte Anzahl qualifizierter Unternehmen mit nachvollziehbaren Kriterien aus. Nicht belegte Fähigkeiten werden nicht unterstellt. Die Anbieteransprache muss rechtlich zulässig sein.

**Schritt C:** Im System entsteht ein Request mit deduplizierbaren Einladungsereignissen. n8n versendet Anfragen oder Benachrichtigungen; jeder Versuch hat einen Zustellstatus.

**Schritt D:** Der Anbieter liefert über einen zeitlich begrenzten Quote-Link ein strukturiertes Angebot. Der Link berechtigt ausschließlich zu diesem Vorgang.

**Schritt E:** Die Engine prüft Vollständigkeit, Kostenbestandteile, Angebotsgültigkeit und Vergleichbarkeit. Offene Punkte führen zu einer Rückfrage oder Besichtigung.

**Schritt F:** Wenn fachlich sinnvoll, wird maximal eine begrenzte „Best and Final“-Nachverhandlung mit zugelassenen Konditionen ausgelöst; echtes Gegenangebot erfordert echte Anbieterbestätigung.

**Schritt G:** Der Kunde sieht eine neutrale Vergleichsansicht und autorisiert das gewählte Angebot. Die Autorisierung ist an Versions-/Fingerprint und Gesamtsumme gebunden.

**Schritt H:** Anbieter bestätigt den konkreten Auftrag und Termin. Der Status wechselt nur bei erfüllten Geschäftsbedingungen. Eine Annahme allein im LLM zählt nicht.

**Schritt I:** Erfüllung, Storno, Beschwerde und Gebührenereignis werden vom System dokumentiert. Bei Nichtleistung werden die vereinbarten Regeln angewandt.

## 5. Minimales Datenmodell

### Tabellen/Aggregate

- golden_company, company_source_observation, company_claim, company_verification, company_location, service_area, provider_capability;
- provider_account, provider_membership, company_ownership_claim, agent_delegation;
- service_template, service_requirement, requirement_attachment;
- service_request, provider_invitation, delivery_attempt, provider_reply;
- provider_quote, quote_line, quote_revision, quote_condition;
- negotiation_mandate, negotiation_message, negotiation_decision;
- appointment_offer, booking, booking_confirmation;
- customer_approval, commission_agreement, fee_rule, commission_event, payment_reference;
- complaint, refund_or_adjustment, audit_event, outbox_event.

Fachliche Datentypen und tatsächliche Tabellenzuschnitte sind während der Umsetzung zu normalisieren; die Liste ist ein logisches Modell, kein verbindlicher SQL-DDL-Entwurf.

### Transaktionszustände

**Anfrage:** DRAFT → QUALIFIED → PROVIDERS_SELECTED → INVITATIONS_SENT → COLLECTING → QUOTES_READY → DECISION_PENDING → BOOKED/EXPIRED/CANCELLED.  
**Angebot:** DRAFT → SUBMITTED → INDICATIVE/CONDITIONAL/BINDING → REVISED/ACCEPTED/EXPIRED/DECLINED.  
**Buchung:** CUSTOMER_APPROVED → PROVIDER_CONFIRMATION_PENDING → CONFIRMED → COMPLETED/CANCELLED/DISPUTED.

Jeder Zustandswechsel wird serverseitig validiert; spätere Änderungen erfordern eine neue Version und gegebenenfalls neue Kundenfreigabe.

## 6. MCP-Verträge (nach Backend-MVP)

Die MCP-Schnittstellen sind **Thin Adapters** über der Agenqo Business API.

### Buyer MCP – nur mit relevanten Käuferrechten

- search_services
- search_providers
- create_service_request
- request_provider_quotes
- get_service_request
- compare_service_quotes
- negotiate_with_mandate
- get_available_appointments
- authorize_booking
- get_booking_status

### Provider MCP – nur mit Organisationsberechtigung

- get_my_provider_profile
- propose_provider_profile_change
- update_my_capabilities
- update_my_availability
- list_my_requests
- submit_my_quote
- revise_my_quote
- respond_to_counteroffer
- confirm_my_booking

**Scope-Beispiele:** services.read, requests.create, buyer.quotes.read, buyer.booking.approve, provider.profile.write, provider.quotes.write, provider.booking.confirm. Eine andere Persona bzw. fremde Provider-ID darf niemals durch freie Tool-Argumente Zugriff erhalten.

Web und beide MCP-Zugänge müssen bei gleichem fachlichen Input identische Preis- und Zustandsprüfungen erzeugen.

## 7. n8n-Verträge

Eingehende und ausgehende Events haben versioniertes Envelope mit event_id, aggregate_id, correlation_id, causation_id, tenant/org scope, idempotency_key, occurred_at, event_type und signierter Payload.

- Versand aus der Outbox mit kontrollierten Wiederholungen und Zustellstatus.
- Webhook-/E-Mail-Rücklauf mit Zuordnung zum Vorgang; unsichere Zuordnung wird manuell geprüft.
- Keine stillen Wiederholungen von verbindlichen Aktionen.
- Dead-Letter Queue für nicht auflösbare Kommunikationsfehler.
- Backoff/Rate Limits sowie Anbieter-Opt-out/Kommunikationspräferenzen.
- Test auf Doppelausführung bei Timeouts und Webhook-Retry.

## 8. Wirtschaftlicher Pilot

### 8.1 Partnerangebot

Testkohorte freiwilliger und erreichbarer Entrümpelungsbetriebe in **einer** Pilotregion. Pilotverträge regeln Teilnahme, Auftragsdaten, Provision bzw. kostenfreie Probephase, Kundenschutz, Angebotsverbindlichkeit, Storno und Kontaktwege.

### 8.2 Nachfrage

20 echte, mit Kundenmandat versehene Entrümpelungsanfragen. Die Zahl dient dazu, operative Fehler und Angebotsverhalten zu entdecken; sie genügt **nicht** für belastbare Langfristprognosen.

### 8.3 Metriken je Anfrage

- Source of Demand / Kundengewinnungskosten;
- Anzahl passender und kontaktierter Anbieter;
- rechtmäßige Zustellung;
- Antwortquote (Antworten pro zugestellter Anfrage);
- Anteil vollständiger Angebote;
- Zeit bis erstes Angebot und Zeit bis zwei vergleichbare Angebote;
- Buchungsquote;
- Preisverbesserung ohne Leistungsverschlechterung;
- Erfolgsvergütung, Inkassoerfolg und Storno;
- direkte KI-/Kommunikationskosten, Betreuung, rechtliche oder operative Sonderkosten;
- Deckungsbeitrag und Kundenzufriedenheit;
- Wiederholungsquote auf Käufer- und Anbieterseite.

### 8.4 Go-/No-Go-Gates (vorläufige Hypothesen)

Die Grenzwerte werden **vor dem Pilot** festgelegt und sind nicht behauptete Marktbenchmarks.

- **Antwortbereitschaft:** vorläufiges Warnsignal bei weniger als 25 % verwertbaren Rückmeldungen auf zulässige Zustellungen.
- **Angebotsvergleich:** Pilot muss wiederholt mehr als ein hinreichend vergleichbares Angebot erzeugen; andernfalls ist das Versprechen „Vergleich“ noch nicht eingelöst.
- **Buchbarkeit:** dokumentierte Kunden- und Anbieterbestätigung muss technisch reproduzierbar sein.
- **Wirtschaftlichkeit:** positiver Deckungsbeitrag unter plausiblen realistischen Kostenannahmen oder nachweisbarer Plan zur Schließung der Lücke.
- **Compliance:** kritische Datenschutz-/UWG-/Vertrags-/Sicherheitsmängel führen unabhängig von Conversion zu No-Go.

Bei No-Go: Kanal, Kategorie, Vergütung oder Produktumfang ändern, **nicht** allein zusätzliche Agenten entwickeln.

## 9. Monetarisierungsversuche (getrennt messen)

**Anbieterprovision:** nur mit vorherigem Anbieter-Vertrag, je Kategorie und ggf. Mindestbetrag. Ein bestehender Golden Company Record ist kein Provisionsvertrag.

**Kundenbeschaffungsgebühr:** nur mit vorab transparenter Preis- und Leistungsvereinbarung; ein optionales Einsparmodell setzt belastbare Ausgangs- und Vergleichspreise voraus.

**Anbieter-Premium:** optionaler Automatisierungs- und Integrationsservice; nicht notwendig für ein Grundprofil oder die manuelle Angebotsabgabe.

Wichtig: Nicht pauschal jeden Euro Bruttoumsatz als Agenturumsatz buchen. Eigene Plattformerträge, Fremdleistungen, Umsatzsteuer, Zahlungsströme und Stornos getrennt führen.

## 10. Ausdrückliche Prüfpflichten vor Livebetrieb

1. **Datenrechte:** Was darf aus TonnEstate/GCR übernommen, veröffentlicht und aktualisiert werden?
2. **Unternehmens-Claim:** Wie wird Vertretungsmacht ausreichend geprüft und Missbrauch verhindert?
3. **§ 7 UWG:** konkrete Kundenanfrage, Werbe-Erstansprache, Telefon und Opt-out differenzieren.
4. **AGB & Mandate:** Käuferauftrag, Anbieterbedingungen, Vermittlungs- und ggf. Beschaffungsvertrag.
5. **Preis-/Ranking-Transparenz:** Endpreis, Steuerlogik, Provisionseinfluss und Verbindlichkeit.
6. **DSGVO:** Foto-/Adress-/E-Mail-Daten, Löschung, Auftragsverarbeitung, berechtigte Interessen.
7. **DSA/AI Act/Regulierungen:** nach tatsächlicher Rolle und Branche prüfen.
8. **Payments:** Kein eigenständiges Halten von Kundengeldern ohne regulatorische Grundlage.
9. **Reklamation:** Verantwortlichkeit des ausführenden Dienstleisters und Rolle der Plattform klar kommunizieren.
10. **Security:** OAuth, Firmendelegation, Token-Rotation, Idempotenz und kompromittierte Anbieterinhalte.

## 11. Reihenfolge des praktischen Aufbaus

| Meilenstein | Liefergegenstand | Harte Abnahme |
|---|---|---|
| M0 – Audit & Verträge | Reuse-Matrix, Datenlizenzprüfung, Pilotpartner und Auftraggeber | Kein produktiver Kontakt ohne geklärten Kanal |
| M1 – Eigenständige Identität | Agenqo DB, Auth, Firmenregistrierung, Profil-Claim | Kein Zugriff auf fremde Organisation |
| M2 – Service & Quote | Entrümpelungsprofil, Intake, sicherer Quote-Link | Reale strukturierte Anbieterantwort |
| M3 – n8n E2E | Outbox, Versand, Rücklauf, Status, Fehlerbehandlung | Kein Verlust/keine Doppelzustellung bei Retry |
| M4 – Comparison & Booking | Konditionen, Verhandlung, Freigabe, Anbieterbestätigung | Tatsächlich bestätigter Pilotauftrag |
| M5 – Wirtschaftlicher Pilot | 20 Fälle, Gebühren- und Kostenbuch | Dokumentierter Go-/No-Go-Beschluss |
| M6 – Remote MCPs | Buyer-/Provider-MCP über identischen APIs | Berechtigungs- und E2E-Agententests |
| M7 – Expansion | Zweite Kategorie und weitere Region | Positiver wirtschaftlicher Nachweis im Kernsegment |

## 12. Definition of Done für das Repo

Dokumentation allein ist **nicht** Implementierung. Mit der ersten Konzeptveröffentlichung sind M0–M7 **nicht abgeschlossen**.

Jedes implementierte Modul benötigt:

- API-/Schema-Vertrag, Tests und dokumentierte Fehlercodes;
- Nachweis des Aufrufs in einer realistischen Laufzeitumgebung;
- Beispielvorgang mit nachvollziehbarem Datensatz und Audit;
- Kostenerfassung und sichere Standardkonfiguration;
- klare Zuordnung **implemented / integrated / tested / deployed / production-verified**;
- keine stillschweigenden Änderungen in anderen Repositories.

**Erstes finanzielles Ziel:** Einen realen Vermittlungsvorgang mit vorab vereinbartem Erlösmodell durchführen und seinen **tatsächlich erzielten Deckungsbeitrag** nachweisen – erst danach skalieren.
