# Agenqo – vollständiges Produkt- und Geschäftskonzept

**Version:** 1.0 · **Datum:** 27. Oktober 2026 · **Status:** verbindliches Zielbild, wirtschaftliche und technische Annahmen gesondert gekennzeichnet

## 1. Executive Summary

**Agenqo wird ein vollständig eigenständiger, KI-nativer und zweiseitiger Dienstleistungsmarktplatz für Deutschland.** Privatkunden, Unternehmen und bevollmächtigte KI-Agenten können Dienstleistungen suchen, Angebote einholen, vergleichen, verhandeln und nach gültiger Autorisierung beauftragen. Dienstleister können sich selbst registrieren, bestehende Unternehmensprofile beanspruchen, Leistungen und Kapazitäten pflegen, Anfragen beantworten und dieselben Vorgänge optional über eigene Agenten und einen Anbieter-MCP bearbeiten.

Agenqo ist **nicht** lediglich ein KI-Chatbot, ein Lead-Generator, eine TonnEstate-Erweiterung oder eine Website mit nachträglich angeschlossener KI. Die Website, die Käufer- und Anbieterzugänge, der Golden Company Record, die Auftrags- und Verhandlungsengine sowie die Abrechnung gehören Agenqo selbst. ChatGPT, Claude und weitere externe Agenten sind mögliche Vertriebskanäle, aber keine notwendige Laufzeitumgebung.

**Kundennutzen:** „Sag, welche Dienstleistung du brauchst – Agenqo organisiert passende, nachvollziehbare Angebote, verhandelt zulässige Konditionen und bereitet die Buchung vor.“  
**Anbieternutzen:** „Erhalte passende Anfragen und verwalte Angebot, Kalender und Vertriebsautomatisierung zentral – selbst, über dein Team oder deinen Agenten.“  
**Plattformnutzen:** Einnahmen aus vorab vereinbarten Transaktionsprovisionen, kundenseitigen Beschaffungsservices und optionalen Anbieter-/Agenten-Abonnements.

**Geschäftsfeld zum Marktstart:** ausschließlich Dienstleistungen. Ein Produktpreisvergleich mit Idealo, Geizhals und Commerce-Protokollen ist *nicht* Bestandteil des ersten MVP.

## 2. Strategischer Ausgangspunkt und USP

Vergleichsplattformen, Vermittlungsportale und KI-Assistenten decken einzelne Teile des Beschaffungsprozesses bereits ab. Alleinstellungsbehauptungen gegenüber CHECK24, MyHammer, Aroundhome oder neuen KI-Startups sind ohne vollständigen aktuellen Wettbewerbsnachweis nicht zulässig.

Der **angestrebte, praktisch zu beweisende USP** ist die Kombination von:

1. **Offenem Unternehmensbestand:** Verifizierbare Firmen unabhängig vom Status als zahlender Plattformpartner auffindbar.
2. **Selbstverwalteter Anbieterseite:** Betriebe können Unternehmensprofile beanspruchen, Leistungsdaten korrigieren, Verfügbarkeiten und Preisregeln pflegen oder Agenten dazu bevollmächtigen.
3. **Zweiseitiger KI-Fähigkeit:** Käufer- und Anbieteragenten kommunizieren über kontrollierte standardisierte Schnittstellen; Menschen können alles im Webfrontend erledigen.
4. **Aktiver Beschaffung:** Angebote werden nicht nur aus einem bestehenden Katalog angezeigt, sondern bei passenden, rechtmäßig kontaktierbaren Dienstleistern angefragt.
5. **Strukturiertem Gesamtpreisvergleich und Verhandlung:** Inklusive verpflichtender Zusatzkosten, fachlicher Vergleichbarkeit, Preisverbindlichkeit und dokumentierter Anbieterannahme.
6. **Transaktionsabschluss:** Kundenfreigabe, Anbieterbestätigung, Termin, Reklamations- und Provisionsereignisse sind Teil derselben Plattform.
7. **Agentenoffener Infrastruktur:** Externe Assistenten integrieren Agenqo über einen Remote-MCP oder eine API, ohne die Geschäftslogik neu zu implementieren.

**Differenzierung entsteht nur, wenn Antworten, echte Angebote, Buchungen, Anbieterzufriedenheit und positiver Deckungsbeitrag nachweisbar sind.** Ein MCP-Endpunkt allein ist kein geschäftlicher Burggraben.

## 3. Produktgrenzen und Unabhängigkeit

- Agenqo ist eine **eigene Produkt- und Betriebsdomäne**: eigener Code- und Datenbestand, Authentifizierung, Mandanten-/Organisationsmodell, Datenhaltung, Deployment, Monitoring, Backup, Verträge und Abrechnung.
- TonnEstate ist ein **möglicher Donor von Wissen, Quellcode und Daten**. Die neue Plattform darf dessen Datenbank oder Flask-Monolith **nicht zur Laufzeit voraussetzen**.
- Übernahmen erfolgen als geprüfte, lizenzrechtlich zulässige Code-Ports, Datenimporte oder versionierte API-Anbindungen. Interne CRM-Kundendaten werden nicht ungeprüft übernommen.
- n8n dient als austauschbare Workflow-/Kommunikationsinfrastruktur, **nicht** als System of Record für Aufträge, Geld oder Vollmachten.
- LLMs dürfen Vorschläge formulieren, aber keine rechtlich verbindlichen Zustandsänderungen ohne deterministische Prüfung auslösen.
- Angebots- und Vermittlungsfunktionen müssen auch ohne ein externes LLM bedienbar sein; KI verbessert die Automatisierung, ersetzt keine fachlichen Sicherheitsregeln.

## 4. Marktseiten und Rollen

### 4.1 Käufer

Privatpersonen sowie Unternehmen und deren Mitarbeiter können Leistungen suchen, Anforderungen formulieren, Fotos hochladen, Anbieter vergleichen, Budgets/Verhandlungsmandate erteilen und Buchungen freigeben.

Zugang: responsive Website, eigener KI-Assistent im Portal, ChatGPT/Claude über verbundene Agenqo-App beziehungsweise Remote-MCP und externe Einkaufsagenten über API/MCP.

**Ein lokaler MCP-Client muss nicht installiert werden.** Verfügbarkeit und Freigabe hängen vom jeweiligen Host ab. Die Website funktioniert unabhängig davon.

### 4.2 Anbieter

Ein Handwerks-, Umzugs-, Entrümpelungs- oder sonstiger Dienstleistungsbetrieb kann:

- sich registrieren und seine geschäftliche Identität nachweisen;
- ein bereits recherchiertes Firmenprofil beanspruchen (Claim-Your-Business);
- Leistungen, Einsatzgebiete, Kontaktwege, Zulassungen, Preisregeln und Verfügbarkeiten verwalten;
- strukturierte Angebotsanfragen empfangen, beantworten oder ablehnen;
- eigene Mitarbeiter und KI-Agenten mit spezifischen Rollen bevollmächtigen;
- Angebote nachbessern, Termine bestätigen, Buchungen und Reklamationen bearbeiten;
- Partnervereinbarungen und provisionspflichtige Vorgänge nachvollziehen.

Ein Anbieter benötigt **weder einen installierten Agenten noch einen MCP**, um am Marktplatz teilzunehmen.

### 4.3 Externe Agenten

Ein Käuferagent kann einen strukturierten Beschaffungsauftrag einreichen und Ergebnisse abrufen. Ein Anbieteragent kann nach erteilter Organisationsvollmacht Firmenprofil, Angebotsregeln, Rückmeldungen und Terminangebote bearbeiten. Ein Agent darf weder seine eigene Berechtigung erteilen noch außerhalb seines Mandats Verträge schließen.

### 4.4 Agenqo als Plattformbetreiber

Agenqo stellt Suche, Vertrauen, Matching, Anfrageprozess, Kommunikationsnachweise, Angebotsvergleich, Verhandlungsregeln, Buchungsmanagement und monetarisierbare Zusatzdienste bereit. Die eigentliche Leistung erbringt in der Regel ein externer Anbieter auf Grundlage seines Vertrags mit dem Kunden.

## 5. Webfrontend: klassischer Marktplatz und vollwertiger AI-Flow

Agenqo erhält eine **eigenständige CHECK24-artige Benutzererfahrung** für menschliche Nutzer, die nicht auf KI-Chat angewiesen sind.

### 5.1 Öffentliches Portal

Branchen- und regionale Landingpages, Suchfilter, Vergleichsansichten, Anbieterprofile, geprüfte Kontaktdaten, Preiskennzeichnung, Erklärungen zu Rankingkriterien, FAQs und transparente Buchungswege.

Anbieterlisten müssen den Status unterscheiden: **identifiziert**, **qualifiziert**, **antwortaktiv**, **registriert**, **vertraglich angebunden**. Recherchierte Firmen dürfen nicht als verifizierte Partner erscheinen.

### 5.2 Käufer-Cockpit

Intake-Assistent, Angebotsanfragen, Vorgangsstatus, Benachrichtigungen, Dokumente/Fotos, Vergleichstabelle, Mandat und Buchungsfreigabe, Termine, Rechnungs-/Provisionshinweise soweit einschlägig sowie Reklamation/Bewertung.

### 5.3 Anbieter-Cockpit

Firmendaten, Claim-Antrag, Nachweise, Leistungen, Einsatzgebiete, Geschäftszeiten, Termine/Kalender, Angebotsformulare, Preiskalkulation, Anfragenliste, Kommunikationsjournal, Mitarbeiter-/Agentenrechte, abgeschlossene Aufträge und Plattformabrechnung.

### 5.4 Verwaltung

Quellenprüfung und Datenkonflikte, Freigabe von Unternehmens-Claims, Qualitäts- und Missbrauchsmanagement, Dispute-Bearbeitung, Compliance, Verträge, Provisionen, Support und Betriebskennzahlen.

## 6. Golden Company Record: eigenständig, versioniert, bearbeitbar

### 6.1 Entscheidung

**Ja, ein eigener Golden Company Record ist sinnvoll und ein wichtiges Startkapital für Agenqo.** Der bestehende TonnEstate-Katalog demonstriert bereits ein quellenbezogenes Modell mit GoldenCompany, CatalogClaim, CatalogServiceLocation, CatalogContactPoint, CatalogCapability, CatalogCredential und Golden Fields.

Für Agenqo entsteht jedoch eine **eigene kanonische Datenhaltung**. Die vorhandene Implementierung dient als Vorlage; Datenübernahme setzt Datenherkunft, Nutzungsrechte, Datenschutz und technische Qualität voraus.

### 6.2 Datenmodell

Mindestens:

- Company (rechtliche Identität), Brand, Location, ServiceArea und ContactPoint;
- Capability/ServiceProfile mit Taxonomie, Leistungsumfang und optionalen Qualifikationen;
- SourceObservation und Claim mit Herkunft, Zeitpunkt, Vertrauen, Konfliktstatus, Lizenz/Nutzungszweck;
- ProviderOrganization/ProviderAccount als tatsächliche Nutzerbeziehung zur Plattform;
- ProfileOwnershipClaim, VerificationEvidence und AgentDelegation;
- ProviderAvailability, PricingRule, Quote, QuoteRevision, Request, Mandate, Booking, CommissionAgreement und CommissionEvent;
- QualitySignal, Complaint, Dispute und AuditEvent.

**Ein Unternehmen ist nicht mit seinem Plattform-Account identisch.** Ein recherchierter Firmeneintrag kann ohne Nutzerkonto existieren; registrierte Anbieter erhalten erst nach Eigentums-/Vertretungsprüfung Änderungsrechte.

### 6.3 Profilbearbeitung durch Unternehmen oder Agenten

- Der Anbieter beantragt und beweist seine Vertretungsbefugnis, z. B. per Domain-/E-Mail-Verifikation und gegebenenfalls weiteren Unternehmensnachweisen.
- Er bearbeitet Leistungen, Einsatzgebiete und eigene Kontaktdaten direkt oder über seinen autorisierten Agenten.
- Eigene Angaben werden als **Self-Assertion mit Urheber, Zeit und Beleg** gespeichert.
- Daten mit amtlicher oder drittseitiger Evidenz werden nicht stillschweigend überschrieben; Konflikte und Historie bleiben sichtbar.
- Kritische Änderungen an Unternehmensidentität, Zahlungsanschluss, Verträgen und Agentenrechten benötigen erhöhte Prüfungen.
- Für Marketing- oder Rankingzwecke werden nur rechtmäßig erworbene, hinreichend aktuelle Daten verwendet.

### 6.4 Qualitätsgrenzen

„Wir kennen alle deutschen Schädlingsbekämpfer“ ist kein belegter Ist-Zustand. Der Ausbau misst je Kategorie und Region getrennt Identifizierungs-, Kontakt-, Qualifikations-, Antwort- und Vertragsabdeckung.

## 7. Golden Service Record und Golden Offer Record

### 7.1 Service Record

Ein standardisiertes Leistungsprofil definiert Pflicht- und optionale Intake-Felder, Vergleichsattribute, Qualifikationen, erlaubte Varianten, Besichtigungsbedarf, rechtliche Besonderheiten, Preisbestandteile und Abnahmekriterien.

Beispiele: Entrümpelung (Volumen, Zugänglichkeit, Sondermüll, Termin); Umzug (Strecke, Volumen, Tragewege); Schädlingsbekämpfung (Art, Standort, Schutzrecht, Dringlichkeit, fachliche Voraussetzungen).

### 7.2 Offer Record

Ein Angebot speichert Anbieter, Leistungs-Snapshot, Einzelpositionen, Steuerstatus, brutto relevanten Gesamtpreis, Vorbehalte, Termin, Gültigkeit, Bindungswirkung, Nachweise, Angebotsrevisionen und Kommunikationsquelle.

Erforderliche Zustände u. a.: **UNVOLLSTÄNDIG**, **INDIKATIV**, **BESICHTIGUNG_ERFORDERLICH**, **VERBINDLICH_BIS**, **ABGELAUFEN**, **ANGENOMMEN**, **ABGELEHNT**.

**Ein Fotoupload erzeugt keinen rechtlich garantierten Festpreis.** Ein Anbieter muss die Bedingungen ausdrücklich festlegen und bestätigen. Alternativ wird eine Besichtigung vorgeschlagen.

### 7.3 Vergleichbarkeit

Nur Angebote mit fachlich vergleichbarem Umfang werden unmittelbar gegeneinander gerankt. Unterschiedliche Leistungen, Vorbehalte oder fehlende Preisbestandteile werden klar angezeigt statt mit einer künstlichen Gesamtpunktzahl verdeckt.

## 8. Durchgehende Customer Journey

1. Kunde beschreibt den Bedarf im Portal oder über seinen KI-Assistenten.
2. Agent/Intake erstellt mit Kundeneinwilligung einen überprüfbaren Requirement Record; offene Parameter werden gezielt nachgefragt.
3. Matching prüft Entfernung, Einsatzgebiet, Kompetenz, rechtliche Eignung, Verfügbarkeitssignale und Datenqualität.
4. Ein Angebotsvorgang wird erzeugt, bevor irgendeine externe Anfrage ausgelöst wird.
5. Geeignete, rechtmäßig kontaktierbare Anbieter werden über bevorzugte Kanäle eingeladen.
6. Anbieter antworten über sicheren Quote-Link, Portal, API, Anbieter-MCP oder – als Fallback – E-Mail.
7. Antworten werden evidenzbasiert strukturiert und auf Vergleichbarkeit geprüft.
8. Bei Bedarf folgen Rückfragen, Besichtigung oder eine begrenzte „Best and Final“-Nachverhandlung.
9. Kunde erhält dokumentierten Vergleich nach gewünschter Priorität: Preis, Termin, Vertrauen oder Gesamtwert.
10. Nach wirksamer Freigabe und Anbieterbestätigung wird die Buchung verbindlich gespeichert.
11. Abschluss, Storno, Reklamation und provisionsrelevanter Erfolg werden nachvollziehbar nachgehalten.

Ein Anbieter kann Anfragen auch ohne vorhandenen Partnervertrag beantworten. Daraus folgt **nicht** automatisch ein Provisionsanspruch von Agenqo.

## 9. Anbieterakquise und Quote-Link

Das **strukturierte Angebotsformular** ist eine entscheidende operative Komponente. Es enthält bereits das normalisierte Leistungsprofil und benötigt für die Antwort keine vollständige Registrierung.

Der personalisierte Zugangslink ist ablaufbegrenzt, an einen einzelnen Vorgang gebunden und serverseitig autorisiert; sensible Unterlagen werden separat geschützt. Preise, Termine, Zusatzkosten und Vorbehalte werden validiert. Eine Angebotsänderung erstellt eine Revision statt den ursprünglichen Nachweis zu überschreiben.

Anbieter können per E-Mail/API oder über das Portal antworten. LLM-basierte Mailinterpretation ist ein Fallback mit Konfidenz- und Belegkontrollen.

Der Start soll möglichst über **freiwillige Pilotanbieter beziehungsweise aktiv onboardete Partner** erfolgen. Eine echte Kundenanfrage ist nicht automatisch Werbung; dies stellt jedoch **keine pauschale rechtliche Freigabe** für automatisierte Kalt-E-Mails oder -Anrufe dar. Anbieterakquise und konkret beauftragte Leistungsanfragen sind rechtlich gesondert zu prüfen.

## 10. Matching, Neutralität und Gesamtpreis

Matching ist zweistufig:

- **Eignungsgate:** Fachliche Berechtigung, Einzugsgebiet, belastbare Identität, erforderliche Leistungsfähigkeit und andere harte Anforderungen.
- **Angebotsranking:** Nur geeignete, hinreichend vergleichbare Angebote werden nach nachvollziehbaren Kundenpräferenzen bewertet.

Der Kunde sieht insbesondere Leistung, **Bruttogesamtpreis**, Liefer-/Einsatz- und Zusatzkosten, Termin, Vorbehalte, Preisgültigkeit, Anbieteridentität und Qualifikation.

Preisregel: Pflichtkosten, Anfahrt und Steuern dürfen nicht ausgeblendet oder doppelt addiert werden. Ein niedriger Basispreis mit hohen Zuschlägen ist kein günstigeres Gesamtangebot.

Anbieterprovisionen dürfen das neutrale Haupt-Ranking nicht verdeckt beeinflussen. Kommerzielle Beziehungen und wesentliche Rankingparameter sind offenzulegen. Nicht provisionierbare Anbieter können sichtbar bleiben, wenn dies fachlich und rechtlich möglich ist.

## 11. Mandatsgebundene KI-Verhandlung

Der Käufer kann einen begrenzten Auftrag erteilen: zulässiger Leistungsumfang, Ziel- und Höchstpreis, Zeitfenster, erlaubte Zugeständnisse, Verhandlungsrunden, Gültigkeit und Freigaberegeln.

Die KI formuliert Verhandlungsvorschläge; die Engine verhindert bindende Zusagen außerhalb des Mandats. Als anfänglicher Standard genügt **eine optionale abschließende Angebotsverbesserung** statt beliebig vieler aggressiver Verhandlungsrunden.

Ein Anbieteragent darf ebenfalls nur innerhalb einer vom Betrieb erteilten Kompetenz Angebote abgeben oder bestätigen. Wettbewerberdetails werden nicht unberechtigt offengelegt; Vergleichshinweise können anonymisiert oder auf freigegebene Kennzahlen begrenzt werden.

Verbindliche Zusagen setzen authentifizierte Rückmeldungen und dokumentierte Annahmen voraus.

## 12. Doppel-MCP und direkte API

### 12.1 Buyer-MCP

Ein öffentlich integrierbarer Remote-MCP für ChatGPT, Claude und beliebige kompatible Kundenagenten stellt eingeschränkt verfügbare Geschäftsoperationen bereit, z. B.:

- search_services, find_providers, get_provider_profile;
- create_service_request, request_quotes, get_request_status;
- compare_quotes, request_negotiation, get_appointment_options;
- authorize_booking, get_booking_status, open_dispute.

Die Werkzeuge können zunächst **ohne automatisch bereitgestellte Personendaten** suchen; personenbezogene Angaben und Auftragsvollmachten werden gezielt und zweckgebunden eingeholt.

### 12.2 Provider-MCP

Anbieter erhalten optional einen gesondert berechtigten Remote-MCP-Zugang, z. B.:

- claim_company, get_my_company_profile, propose_profile_update;
- set_service_capabilities, update_service_area, update_availability;
- list_incoming_requests, submit_quote, revise_quote;
- submit_counteroffer, propose_slots, confirm_booking;
- list_settlement_events.

Provider-MCP-Aktionen verlangen nachgewiesene Organisationszugehörigkeit und enge Rechte. Kritische Mutationen benötigen abgestufte Freigaben. **Kein Dienstleister muss eigene MCP-Server hosten oder einen Agenten installieren.**

### 12.3 Technische Topologie

Buyer- und Provider-MCP können zwei logische Endpunkte oder zwei strikt getrennte Tool-Surfaces derselben Remote-MCP-Implementierung sein. Dahinter liegen dieselben versionierten Geschäfts-APIs. Für Agenten und ERP-/CRM-Systeme kann zusätzlich ein REST-/Webhook-Angebot bestehen.

Für alle: OAuth-/Token-basierte Identität, Rollen und Scopes, zweckgebundene Mandate, Tenant-Isolation, Rate Limits, Agentenaudits, Prompt-Injection-Schutz, Idempotenz und serverseitige Zustandsprüfung.

**MCP-Veröffentlichung garantiert keine Aufnahme, Empfehlung oder Aufrufhäufigkeit in ChatGPT, Claude oder Gemini.** Das sind separate Distributionsrisiken.

## 13. n8n und Geschäftsprozess-Orchestrierung

n8n ist die asynchrone Prozessschicht: Einladungen, E-Mails, Webhooks, Fristen, Erinnerungen, Antwortzuordnung und Eskalationen. Hauptprozesse sind **Create Request**, **Invite Providers**, **Capture Quote**, **Clarify**, **Negotiate**, **Book**, **Complete**, **Dispute** und **Settle**.

Die Agenqo-Backend-Engine ist alleiniger Owner von Provider Orders, verbindlichen Konditionen, Mandaten, Gebühren und Autorisierungen. Geschäftsvorfälle werden per transaktionaler Outbox veröffentlicht; n8n meldet Resultate über signierte und idempotente APIs zurück.

Längere Vorgänge liefern sofort eine stabile Request-ID; Statusupdates können über Polling, Webhooks oder vom Host unterstützte Benachrichtigungen zugestellt werden. n8n-Ausfälle dürfen weder Aufträge verlieren noch Doppelbuchungen auslösen.

## 14. Wirtschaftliches Modell: drei unabhängige Erlöspfade

### A – Vertragliche Erfolgsprovision von Anbietern

Registrierung und Grundprofil können kostenlos sein. Bei vertraglich angebundenen Anbietern wird eine im Voraus vereinbarte Vermittlungsvergütung bei genau definiertem Erfolg fällig. Rate und Ereignis werden nach Kategorie festgelegt. **Keine automatische Provision für bloß im Golden Record bekannte Firmen.**

### B – Beschaffungsgebühr auf Kundenseite

Bei nicht provisionsgebundenen Anbietern oder aufwendigen Leistungen kann der Käufer eine **vorab transparent vereinbarte** fixe Servicegebühr, ein B2B-Kontingent oder ein Erfolgsmodell mit objektiv messbarer Ersparnis zahlen. Kostenpflichtige Aktionen müssen eindeutig autorisiert werden. Eine nicht zuverlässig belegbare „Ersparnis“ ist keine tragfähige Abrechnungsgrundlage.

### C – Premium-Automatisierung für Dienstleister

Kostenpflichtige Anbieterfunktionen, z. B. Agenten-MCP, Kalender-Sync, CRM-/ERP-Integration, regelbasierte Angebotsautomatisierung, Teamrechte, erweitertes Reporting und technische SLA. **MCP selbst ist nicht zwingend kostenpflichtig; bezahlt wird ein messbarer Nutzen.**

### 14.1 Rechenbeispiel, ausschließlich Szenario

Bei einem Kundenauftrag über **600,00 € brutto** und einem zugrunde gelegten Umsatzsteuersatz von 19 % beträgt der rechnerische Netto-Leistungswert **504,20 €**. Bei **8 % vertraglicher Anbieterprovision auf diesen Netto-Leistungswert** ergäbe sich ein Provisionsentgelt **von 40,34 € netto**, zuzüglich auf die Vermittlungsleistung gegebenenfalls anwendbarer Umsatzsteuer.

Bei angenommenen direkten Kosten von 6 € (KI/Kontakt), 9 € (Support/Abwicklung) und 15 € (zugeordneten Akquisitionskosten) verblieben **10,34 € vor Fixkosten und Steuern auf den Plattformgewinn**. Kein Marktwert ist hier nachgewiesen; alle Preis- und Kostenannahmen sind zu validieren.

Die Provision wird **nicht automatisch auf den dem Kunden vom Anbieter angebotenen Gesamtpreis aufgeschlagen**. Wer sie trägt, wie sie ausgewiesen wird und wann sie entsteht, wird vertraglich definiert.

### 14.2 Wirtschaftliche Kernfrage

Formel: **Deckungsbeitrag pro abgeschlossenem Auftrag = tatsächlich realisierte Netto-Plattformerträge – variable KI-, Kommunikations-, Payment-, Support-, Reklamations- und Akquisitionskosten.**

Maßgeblich sind außerdem Antwortquote, Anzahl brauchbarer Angebote je Anfrage, Abschlussquote, durchschnittlicher Auftragserlös, Zeit bis Angebot und Wiederholungskäufe. Ein großes Firmenverzeichnis ohne Transaktionen erzielt keine Erträge.

## 15. Go-to-Market: zwei Marktseiten aufbauen

Agenqo benötigt gleichzeitig **Nachfrage und reaktionsfähige Anbieter**. Deshalb wird das Onboarding zunächst regional und kategoriebezogen konzentriert, ohne das gesamte Unternehmen auf Immobilienmakler zu beschränken.

Der Pilot kann mit gewerblichen Auftraggebern aus dem Immobilienumfeld starten, sofern konkrete wiederkehrende Aufträge verfügbar sind. Gleichzeitig werden freiwillig teilnehmende Entrümpelungsbetriebe gewonnen.

Anbieterseite: kostenlose Profilbeanspruchung, unkomplizierter Quote-Link, sichtbare Qualitätssignale, keine versteckten Leadgebühren, optionaler Automatisierungsmehrwert.  
Käuferseite: Portal mit regionalen Landingpages, Suchmaschinenpräsenz, Direktkundennachfrage, wiederkehrende B2B-Auftraggeber und später MCP-Distribution.

Die Plattform sollte nicht allein auf SEO vertrauen; externe Assistenten sind ebenfalls ein möglicher, aber nicht garantierter Akquisitionskanal.

## 16. Pilotkategorie und Beispiele

**Erste Kategorie: Entrümpelung/Wohnungsauflösung.** Gründe: vergleichsweise strukturierbarer Intake und naheliegende wiederkehrende Nachfrage; gleichzeitig sind Volumen, Sondermüll und Besichtigungsbedarf echte Komplexitätsfaktoren.

Intake: Objektart, ungefähres Volumen, Stockwerke, Zugänglichkeit, Fotos/Video, Entsorgungsklassen, Termin, optionale Besichtigung. Ein Vision-Modell liefert nur dokumentierte Schätzungen; Anbieter setzen die verbindlichen Konditionen.

**Zweite Kategorie nach Pilot:** Schädlingsbekämpfung, einschließlich Prüfung fachlicher Qualifikation und natur-/artenschutzrechtlicher Grenzen. „Wespennest entfernen“ ist nicht in jedem Fall eine zulässige Leistung.

Spätere Kategorien: Umzug, Möbeltransport, Reinigung, Handwerker und weitere Dienstleistungen. **Keine parallele Produkteinführung** vor einem validierten Dienstleistungsmodell.

## 17. Recht, Compliance und Vertrauen

Das folgende sind Konzeptanforderungen, **keine individuelle Rechtsberatung**:

- **UWG § 7:** Eine konkrete, bevollmächtigte Anfrage ist nicht automatisch Werbung; Kaltakquise, Werbemails, automatische Anrufe und wiederholte Belästigung sind gesondert zu bewerten. Nicht von einer pauschalen Erlaubnis ausgehen.
- **Vollmacht/Vertrag:** Der Kunde erteilt definierte Befugnisse; bindende Erklärungen erfordern wirksame Autorisierung. Anbieter- und Kundenannahme sowie Angebotsfrist sind nachweisbar.
- **KI-Offenlegung:** Gegenüber Interaktionspartnern erkennbar machen, wann ein KI-Agent kommuniziert; konkret anwendbare AI-Act-Pflichten prüfen.
- **Ranking/Verbraucherrecht:** Hauptparameter, Provisionseinflüsse, unvermeidbare Gesamtkosten, Preisverbindlichkeit und Verbraucherschutzanforderungen transparent ausweisen.
- **DSGVO:** Rechtmäßigkeit, Zweckbindung, Lösch-/Berichtigungsrechte, Datenminimierung, sichere Foto-/Adressverarbeitung und Löschkonzepte für Unternehmens- und Personendaten.
- **DSA:** Je nach tatsächlicher Rolle als Vermittlungsplattform/Online-Marktplatz anwendbare Pflichten einschließlich Händleridentifikation prüfen.
- **Payments:** Kundengeld grundsätzlich direkt bei Dienstleistern/lizenzierten Zahlungsdienstleistern halten; eigene Zahlungsverarbeitung nur nach regulatorischer Prüfung.
- **Qualität:** Reklamationen, Storno, Rückerstattung, schlechte Anbieterleistung und Gegendarstellung sind eigene Prozesse; Bewertungsmissbrauch erkennen.
- **Quellenrechte:** Recherchierte Firmendaten, Datenbanken, Fotos und Fremdintegrationen dürfen nur im erlaubten Umfang kopiert, gespeichert und veröffentlicht werden.

## 18. Wettbewerb, Risiken und Verteidigbarkeit

Agenqo konkurriert nicht nur mit CHECK24/MyHammer/Aroundhome, sondern potenziell mit neuen deutschen KI-Ausschreibungsdiensten sowie großen Plattformen, die Agentenfunktionen nachrüsten.

Die Verteidigbarkeit entsteht durch **hohe Angebots- und Buchungsqualität**, wiederkehrende Anbieterbeziehungen, autorisierte Service- und Termindaten, kurze Antwortzeiten, belastbare Bewertungssignale, prozesssichere Transaktionshistorie und echte Marktdistribution – nicht durch ein generisches LLM.

Die größten Risiken sind niedrige Antwortquoten, hohe Akquisitionskosten, unzureichende Provisionsbasis, Anbieterumgehung, rechtliche Kontaktbeschränkungen, schlechte Datenqualität und unzuverlässige Bestellfreigaben.

Gegenmaßnahmen: regional fokussiertes Onboarding, freiwillige Partnerkanäle, transparenter Quote-Link, differenzierte Gebühren, Auditierung, klarer Buchungs- und Reklamationsmehrwert.

## 19. Verantwortlichkeiten und technische Sicherheit

**Fachengine:** einzige Quelle für Zustandsübergänge und Geldbeträge.  
**Golden Record:** einzige Quelle für veröffentlichte Unternehmensidentität und Quellenkonflikte.  
**n8n:** keine eigene verbindliche Buchungs- oder Provisionsentscheidung.  
**LLM/Agent:** Vorschläge und Kommunikation innerhalb Mandat, keine eigenmächtige Berechtigungsvergabe.  
**Buyer-/Provider-MCP:** separate Tool-Berechtigungen, keine gemeinsame ungeschützte Schreiboberfläche.  
**Backoffice:** manuelle Freigabe, Konfliktbehandlung, Betrugsprävention, Support.

Technischer Mindeststandard: Verschlüsselung, Secret-Management, Audit-Log, klare Mandantentrennung, idempotente Requests, Bestätigungen mit Hash/Fingerprint des exakten Angebots, Wiederanlauf per Outbox, belastbare Tests und überwachte Fehlerquoten.

## 20. Umsetzung und Investitionslogik

### Phase 0 – Definition, Reuse-Audit und Geschäftsvalidierung

Eigene Agenqo-Domäne und Repo-Struktur festlegen; bestehende TonnEstate-/FruitStack-Bausteine ausschließlich auf **Funktionsebene** gegen das Zielbild prüfen. Code, Daten und Lizenzen werden nicht ungeprüft übernommen. Parallel Markthypothese, Pilotregion, Auftraggeber und anbieterseitige Zustimmung validieren.

### Phase 1 – Eigenständige Plattformgrundlage

Eigenes Backend, eigene Datenbank, Authentifizierung, Golden Company Record, Anbieter-Claim-Prozess, Servicekatalog, buyer/provider Accounts, Quote-Link, Mandats-/Request-/Offer-Modelle und ein webbasiertes Minimal-Frontend.

### Phase 2 – End-to-End-Vermittlung

n8n-Integration, Anbietereinladung, strukturierte Angebotsabgabe, tatsächlicher Vergleich, eine Verhandlungsrunde, Kundenfreigabe, bestätigte Buchung, Storno und Provisions-/Servicegebührennachweis.

### Phase 3 – Reale Pilottransaktionen

Mindestens **20 echte Auftragsfälle** mit kontrollierter menschlicher Begleitung; Pilotumfang ist ein Lerninstrument, keine statistisch abgesicherte Skalierbarkeitsprognose. Kosten und Erträge dokumentieren. Vor Ausbau explizite Fortsetzungs-/Änderungs-/Abbruchentscheidung.

### Phase 4 – Remote-MCPs und Partner-APIs

Buyer- und Provider-MCP auf der stabilen Fachengine veröffentlichen. Mit einem echten Käuferassistenten und einem echten Anbieteragenten testbar machen; OAuth- und Berechtigungstests bestehen. Öffentliche Veröffentlichung nach Distributions- und Sicherheitsprüfung.

### Phase 5 – Vertikalisierung und Skalierung

Weitere Regionen/Kategorien nur nach positiver Unit Economics und ausreichend aktiver Angebotsabdeckung. Zusätzliche Vertriebs- und Automatisierungsmodelle datenbasiert priorisieren.

## 21. Verbindliche MVP-Abnahme

Ein MVP ist erst angenommen, wenn in einem kontrollierten realen Fall:

1. Ein Kunde ohne Entwicklerhilfe eine Dienstleistungsanfrage stellen kann.
2. Geeignete Anbieter mit nachvollziehbaren Quellen und Eignungskriterien gefunden werden.
3. Ein Anbieter sich selbst registrieren oder sein Profil rechtssicher beanspruchen kann.
4. Mindestens ein Anbieter ein strukturiertes Angebot über Portal/Quote-Link abgeben kann.
5. Mehrere Angebote mit vollständigen Preisbestandteilen verglichen werden können.
6. Eine zulässige Nachverhandlung nachweisbar durchgeführt oder begründet übersprungen wird.
7. Der Kunde einen konkreten Angebotsstand wirksam freigibt.
8. Der Anbieter die Buchung bestätigt und Doppelausführung verhindert wird.
9. Storno/Reklamation und Provisionsstatus im Vorgang nachvollziehbar sind.
10. Die variablen Prozesskosten und der Deckungsbeitrag gemessen werden.
11. Die Plattform **ohne TonnEstate-Laufzeit** funktionsfähig ist.
12. Die technischen Rechte von Kunde, Anbieter, Betreiber und Agenten getrennt sind.

Die erste Fassung braucht noch keinen öffentlich gelisteten MCP, aber die späteren MCP-Operationen sollen dieselben APIs nutzen, die das Webfrontend bereits verwendet.

## 22. Was ausdrücklich nicht als vorhandene Funktion ausgegeben wird

- Kein laufender Agenqo-Marktplatz.
- Keine bestätigte Übernahme des TonnEstate-Golden-Company-Datenbestands.
- Keine bestätigten Anbieterpartner oder unterschriebenen Provisionsverträge.
- Kein produktiver Buyer-/Provider-MCP.
- Keine live automatisierte deutschlandweite Anbieteransprache oder KI-Verhandlung.
- Keine gesicherten Umsätze, Conversion Rates oder Marktführerschaft.
- Keine verifizierte öffentliche Integration in Google „Ask for Me“.
- Kein Produktpreisvergleich als initialer Scope.

## 23. Offene Entscheidungen mit wirtschaftlicher Priorität

1. **Pilotregion und anfängliche Anbieterzahl:** anhand real erreichbarer Vertragspartner und Kundenaufträge festlegen.
2. **Preisgestaltung:** Kundengebühr vs. Anbieterprovision je Segment testen; Vergleichsneutralität vertraglich sichern.
3. **Partner-Onboarding:** Einladungs-/Claim-Verfahren und revisionsfähige Terms definieren.
4. **Buchungsereignis:** rechtlich eindeutigen Zeitpunkt für Vermittlungserfolg und Provision festlegen, inkl. Storno.
5. **Golden-Record-Datenübernahme:** Lizenz-/Datenschutzprüfung, Exportvertrag, eigene Quellenpipeline und Aktualität.
6. **Kanäle:** zunächst Web und Quote-Link; Buyer-/Provider-MCP nach belastbarer Backend-Kette.
7. **Marke:** Agenqo ist Projekt- und Repositoryname; Domain und Markenfreiheit separat recherchieren.

## 24. Erfolgskriterium

**Agenqo ist erfolgreich, wenn es nachweislich regelmäßig echte, passende Dienstleistungen zu nachvollziehbaren Gesamtkonditionen vermittelt und nach allen variablen Kosten einen positiven Deckungsbeitrag erzielt.**

Nicht die Zahl der GitHub-Repositories, Agenten oder katalogisierten Firmen ist das Geschäftsergebnis, sondern **qualifizierte Nachfrage × Antwortwahrscheinlichkeit × Buchungswahrscheinlichkeit × realisierbarer Plattformertrag – Gesamtkosten**.

---

## Referenzen und potenzielle Donoren (nicht bereits integrierte Partner)

**Eigener Kontext:**  
- https://github.com/tonnestate/TonnEstate  
- https://github.com/tonnestate/LemonMe  
- https://github.com/tonnestate/DragonFruitMe  
- https://github.com/tonnestate/BlackberryMe  
- https://github.com/tonnestate/CherryMe

**Schnittstellen/Technologie:**  
- https://modelcontextprotocol.io/  
- https://docs.n8n.io/  
- https://github.com/idealo/mcp-server-guide (Produktpreisvergleich **außerhalb MVP**)  
- https://github.com/Nolpak14/agorio (Commerce-Referenz **außerhalb MVP**)  

**Rechts- und Regulierungsfelder zur fachlichen Prüfung:** § 7 UWG; §§ 164 ff. und 312j BGB; DSGVO; § 5b UWG; PAngV; DSA; EU AI Act; je nach Kategorie einschlägiges Fachrecht.

**Dokumentenstatus:** Strategisches Sollkonzept mit bisher geprüftem TonnEstate-Codebestand als technischer Referenz. Es ist weder Umsetzungsnachweis noch Rechtsgutachten.
