# Agenqo – Branchen- und Leistungskatalog v3.0

**Datum:** 27. Oktober 2026 · **Status:** versionierbare fachliche Starttaxonomie, kein Anspruch auf vollständige Erfassung aller deutschen Dienstleistungen.

## 1. Systematik und Vollständigkeit

Agenqo katalogisiert **konkrete vermittelbare Leistungen**, nicht nur Unternehmensbranchen. Ein Betrieb kann mehrere Leistungen, Qualifikationen, Marken und Leistungsstandorte besitzen.

**Hierarchie:** ServiceDomain → ServiceFamily → ServiceCategory → ServiceType → ServiceVariant → Leistungsattribute (und Synonyme). Branchen-/Unternehmensdaten aus WZ 2025 und Gewerberegister sind Mapping-Quellen, **keine 1:1-Dienstleistungstaxonomie**. Quelle: https://www.destatis.de/DE/Methoden/Klassifikationen/Gueter-Wirtschaftsklassifikationen/klassifikation-wz-2025.html

Für jede konkrete Leistung zwingend: \`code\`, \`label_de\`, \`aliases\`, \`category_version\`, \`required_intake_fields\`, \`price_components\`, \`location_mode\`, \`service_area_rule\`, \`regulatory_gate\`, \`qualification_evidence\`, \`supports_fixed_quote\`, \`needs_visit\`, \`fulfillment_mode\`, \`activation_status\`, \`source_mapping\`.

**Status:** LISTED (nur Suche), RFQ_ENABLED, AGENT_QUOTABLE, BOOKABLE, PAUSED. Katalog sichtbar ≠ alle Unternehmen vorhanden ≠ sofortiger Buchungsservice.

## 2. Startkatalog: 24 Domänen mit Leistungsfamilien und Beispielen

Die unten aufgeführten rund 200 typischen Leistungsbezeichnungen bilden den **breiten initialen Navigations- und Suchwortschatz**, nicht die Vollständigkeit der deutschen WZ-Unterklassen. Die Feinerschließung erfolgt über offizielle WZ-2025-Daten, Handwerksrollen und echte Anbieter-Selbstauskünfte.

### D01 – Entsorgung, Haushaltsauflösung und Rückbau
Entrümpelung Wohnung; Kellerentrümpelung; Dachbodenräumung; Garagenräumung; Haushaltsauflösung; Nachlassauflösung; Firmenauflösung; Büroauflösung; Sperrmüllabholung; Möbelentsorgung; Elektroschrottabholung; Containerdienst; Aktenvernichtung; Demontage nichttragender Einbauten; besenreine Übergabe; Wertanrechnung; Messie-Reinigung als separate Spezialleistung; kontaminierte Materialien nur nach Fachprüfung.

**Basisattribute:** Raumtyp, Fläche/Volumen, Etagen, Aufzug, Zufahrt, zu trennende Materialien, Sondermüll, Fotos, Termin, Umfang, Entsorgungsbelege. **Gate:** Abfallrecht (u. a. § 53 und ggf. § 54 KrWG), Gefahren-/Schadstoffprüfung.

### D02 – Umzug, Transport und Logistik
Privatumzug; Firmenumzug; Seniorenumzug; Fernumzug; Möbeltaxi; Möbeltransport; Klaviertransport; Tresortransport; Kleintransport; Kurierdienst; Expresslieferung; Lagerung; Verpackungsservice; Möbelmontage; Umzugskartons; Halteverbotszone organisieren; Außenaufzug; Schwerlasttransport; Akten-/IT-Transport.

**Attribute:** Abhol-/Lieferort, Distanz und Route, Volumen/Gewicht, Etagen/Tragewege, Parken, Versicherung, Termin, Montagen. **Gate:** Transportrecht abhängig von Art/Gewicht/Gewerbe.

### D03 – Reinigung und Hygiene
Wohnungsreinigung; Büroreinigung; Unterhaltsreinigung; Grundreinigung; Fensterreinigung; Fassadenreinigung; Teppich-/Polsterreinigung; Baureinigung; Endreinigung; Treppenhausreinigung; Industriereinigung; Praxisreinigung; Desinfektion; Tatortreinigung als Spezialbereich; Graffiti-Entfernung; Solaranlagenreinigung; Dachrinnenreinigung; Hochdruckreinigung.

**Attribute:** Fläche, Intervall, Fenster, Chemikalien, Zugang, Hygienevorgaben, Arbeitshöhen. **Gate:** Schutz-/Hygiene- und ggf. Gefahrstoffanforderungen.

### D04 – Haus, Garten und Außenanlagen
Gartenpflege; Rasenmähen; Heckenschnitt; Baumpflege; Baumfällung; Wurzelfräsen; Beetpflege; Grünflächenpflege; Terrassenpflege; Pflasterarbeiten; Zaunmontage; Bewässerungsanlagen; Landschaftsbau; Teichpflege; Winterdienst; Laubbeseitigung; Außenbeleuchtung durch qualifizierte Fachkräfte; Gartenplanung; Baumpflanzung.

**Attribute:** Grundstücksgröße, Maschinen, Entsorgung, Hanglage, Baumschutz, Saison. **Gate:** Baumschutz, Betriebsmittel und ggf. Genehmigungen.

### D05 – Allgemeiner Hausmeister-/Objektservice
Objektkontrolle; Hausmeisterdienst; Kleinreparaturen; Schließdienst; Winterdienst; Mülltonnenservice; Schlüsselübergabe; Wohnungsabnahmeunterstützung; Mängeldokumentation; Aufzugs-/Technikprüfung nur durch Berechtigte; Objektbegehung; Wartungskoordination; Ferienimmobilienbetreuung.

### D06 – Elektro, Energie und Gebäudetechnik
Elektroinstallation; Steckdosen; Beleuchtung; Sicherungskasten; Fehlerdiagnose; E-Check; Wallbox; PV-Montage; PV-Elektrik; Batteriespeicher; Smart Home; Netzwerkkabel; Türsprechanlagen; Alarmanlagen; KNX; Außenstrom; Netzanschlussvorbereitung; Haushaltsgeräte-Reparatur.

**Gate:** Handwerksordnung/erforderliche Eintragung und Fachberechtigung, Netzbetreiber-/Arbeitsschutzregeln.

### D07 – Sanitär, Heizung, Lüftung und Klima
Rohrreparatur; Abflussreinigung; Badumbau; Armaturen; Warmwasser; Heizungsausfall; Heizungswartung; Wärmepumpe; Gasinstallation; Fußbodenheizung; Lüftung; Klimaanlage; Dichtheitsprüfung; Leckortung; Rohrsanierung; Schimmeldiagnostik; Wasserschadentrocknung.

**Gate:** Qualifikationen, Kälte-/Gas-/Installationsvorschriften.

### D08 – Bau, Innenausbau und Renovierung
Malerarbeiten; Tapezieren; Putz; Trockenbau; Fliesen; Parkett; Laminat; Estrich; Abdichtung; Fassade; Dachreparatur; Zimmererarbeiten; Tischler; Türen/Fenster; Rollläden; Sonnenschutz; Metallbau; Glas; Treppenrenovierung; Kellerausbau; Küchenmontage; Badsanierung; barrierefreier Umbau; Gerüstbau; Kernbohrung; Baugrunduntersuchung; Abriss; Schadstoffsanierung als qualifikationspflichtiger Spezialbereich.

**Gate:** Anlage A der Handwerksordnung, Baugenehmigung, Schadstoffe, Statik.

### D09 – Immobilien und Grundstücksservices
Immobilienfotografie; Exposé-Erstellung; Grundrisszeichnung; Energieausweis durch Berechtigte; Wertermittlung; Verkehrswertgutachten; Objektbesichtigung; Home Staging; Immobilienverwaltung; Mietverwaltung; WEG-Verwaltung; Vermietungsservice; Maklervermittlung; Flächenaufmaß; Baubegleitung; Gebäudeinspektion; Schlüsselservice; Wohnungsübergabe; Eigentümerservice.

**Gate:** Qualifikationen und Genehmigungen je Tätigkeit, z. B. § 34c GewO, Energieausweisregeln.

### D10 – Foto, Film, Medien und Drohnen
Portraitfotografie; Bewerbungsfotos; Familienfotos; Hochzeitsfotografie; Eventfotografie; Produktfotografie; Immobilienfotografie; Architekturaufnahmen; Baustellendokumentation; Drohnenfotografie; Drohnenvideo; Thermografie; Dach-/Fassadeninspektion mit Drohne; 360°-Rundgang; Matterport/3D-Scan; Videoproduktion; Schnitt; Livestream; Fotobearbeitung; Social-Media-Content; Werbefilm; Tonaufnahme.

**Attribute:** Ort, Datum, Zeit, Licht, Bildmenge, Bearbeitung, Nutzungsrechte, Portfolio, Anfahrt. **Drohnen-Gate:** Pilot-/Betreiberpflichten, Luftraum, UAS-Geozonen, Versicherung, Eigentümer-/Datenschutzrechte. Quelle https://verwaltung.bund.de/leistungsverzeichnis/DE/leistung/99080103001000/

### D11 – Schädlingsbekämpfung, Hygiene und Naturschutz
Schädlingsinspektion; Bettwanzenbehandlung; Schabenbekämpfung; Nagetierbekämpfung; Motten; Ameisen; Taubenabwehr; Marderschutz; Wespenbegutachtung; zulässige Wespennestumsiedlung; Holzschädlingsdiagnostik; Vorratsschutz; Präventionskonzept.

**Gate:** fachlicher Sachkundenachweis, Gefahrstoffe/Biozide, Artenschutz; keine automatische Zusage zur Entfernung geschützter Tiere.

### D12 – Notdienste
Schlüsseldienst; Glasnotdienst; Rohrbruch; Heizungsnotdienst; Elektro-Notdienst; Wasserschadensicherung; Sturmfolgen; Gebäudesicherung; Pannenhilfe; Nottransport.

**Besonderheiten:** Echtzeit-Verfügbarkeit, transparente Nacht-/Wochenendzuschläge, Höchstpreis-/Standortprüfung, Missbrauchsschutz.

### D13 – Fahrzeug, Mobilität und Maschinen
Kfz-Reparatur; Inspektion; Reifenservice; Reifenwechsel mobil; Fahrzeugaufbereitung; Scheibenreparatur; Lackaufbereitung; Oldtimerservice; Fahrradreparatur; E-Bike-Wartung; Motorradreparatur; Caravanservice; mobile Starthilfe; Fahrzeugtransport; Maschinenreparatur.

### D14 – IT, Software und Telekommunikation
PC-/Mac-Reparatur; WLAN-Einrichtung; Netzwerkadministration; Helpdesk; Cloudmigration; Website-Erstellung; WordPress; SEO; Softwareentwicklung; API-Integration; CRM-Einführung; Datenmigration; SQL-/BI-Beratung; Cybersecurity-Audit; Backup/Recovery; Automatisierung; KI-Agenten-Integration; Digitalisierung von Geschäftsprozessen; Schulungen.

**Ort:** regional oder remote; Anbieter kann remote deutschlandweit/überregional anbieten. **Gate:** bei sicherheitssensitiven Services NDA, datenschutz-/zugangsspezifische Freigaben.

### D15 – Marketing, Design und Kommunikation
Grafikdesign; Logo; Corporate Design; Werbemittel; Text/Copywriting; Lektorat; Übersetzung; Lokalisierung; Social-Media-Management; Podcast-Produktion; Video-Editing; Online-Werbung; Suchmaschinenoptimierung; Content-Produktion; PR; Medienplanung; Kampagnenbetreuung; Printdesign; Branding; Fotomarketing.

### D16 – Business-, Büro- und Verwaltungsdienste
Buchhaltungsunterstützung; Büroservice; virtuelle Assistenz; Sekretariat; Datenerfassung; Dokumentenmanagement; Prozessoptimierung; Projektmanagement; Personalvermittlung; Recruiting; Übersetzungsbüro; Beschaffung; Qualitätsmanagement; Zertifizierungsbegleitung; Callcenter; Eventorganisation; Unternehmensberatung.

**Gate:** Steuer- und Rechtsberatung nur durch Berechtigte, keine nicht autorisierte Rechts-/Steuerleistung.

### D17 – Recht, Notar und regulierte Fachberatung
Notarielle Beurkundung; anwaltliche Beratung; Steuerberatung; Wirtschaftsprüfung; Insolvenzberatung (berechtigungspflichtig); Patentrecht; Datenschutzberatung; Mediation; Sachverständige; technische Gutachten; öffentlich bestellte Gutachten.

**Gate:** besondere Berufsrechte, Gebührenordnungen, Werbe- und Vermittlungsbeschränkungen. Nicht automatisch Provisionen oder Preisnachverhandlungen für regulierte Berufe aktivieren.

### D18 – Bildung, Coaching und Unterricht
Nachhilfe; Sprachunterricht; Musikunterricht; IT-Schulung; Prüfungsvorbereitung; Bewerbungstraining; Fahrschulangebote; Unternehmensworkshops; berufliche Weiterbildung; Sportcoaching; Tanzunterricht; künstlerischer Unterricht; Online-Coaching.

**Gate:** Kinder-/Jugenddatenschutz, Qualifikation und fachspezifische Anforderungen.

### D19 – Veranstaltung, Kultur und Freizeit
DJ; Eventfotograf; Musiker; Moderator; Caterer; Eventlocationvermittlung; Dekoration; Licht-/Tontechnik; Veranstaltungsaufbau; Künstler; Hochzeitsplanung; Partyservice; Zeltverleih mit Service; Sicherheitspersonal; Ticketservice; Reisebegleitung.

**Gate:** Bewachungs-/Gaststätten-/Lebensmittel-/Veranstaltungsrecht je Leistung.

### D20 – Gesundheit, Pflege und körpernahe Leistungen
Pflegedienst; Haushaltshilfe; Alltagshilfe; Physiotherapie; Ergotherapie; Massage; Friseur; Kosmetik; Fußpflege; medizinische Fußpflege; Fitnessbetreuung; Ernährungsberatung; Gesundheitscoaching.

**Gate:** Approbation, Heilberufs-, Pflege-, Sozialleistungs- und Datenschutzregeln. Keine generelle offene Vermittlungsprovision bei geschützten Berufen ohne Prüfung.

### D21 – Betreuung, Haustiere und Familie
Kinderbetreuung; Seniorenbetreuung; Haustierbetreuung; Gassiservice; Tierpension; Tiertraining; Umzugshilfe für Senioren; Alltagshilfe; Haushaltsorganisation.

**Gate:** Zuverlässigkeit, Versicherung, Genehmigungen und Schutz sensibler Personen.

### D22 – Produktion, Industrie und Gewerbeservice
CNC-Auftragsfertigung; 3D-Druckservice; Reparatur von Produktionsanlagen; Maschinenwartung; Prüfung elektrischer Anlagen; Facility Management; Gebäudetechnik-Wartung; Lagerdienst; Inventarisierung; Montage; technische Reinigung; industrielle Fotodokumentation; Qualitätssicherung; Verpackungsdienst.

### D23 – Umwelt, Energie und Nachhaltigkeit
Energieberatung; Wärmebildanalyse; Gebäudebilanzierung; PV-Reinigung; CO₂-Bilanzierung; Energieaudit; Umweltsachverständige; Lärmmessung; Schadstoffprüfung; Wasseranalyse; Sanierungsberatung; Fördermittelberatung; Entsorgungsnachweis.

**Gate:** förderrechtliche und berufsrechtliche Qualifikationen, Messlabor-/Nachweisvorschriften.

### D24 – Spezial-, Remote- und neue Services
Datenannotation; Transkription; Untertitel; Voiceover; Virtuelle Rundgänge; Drohnenvermessung; Laser-Scanning; CAD-Zeichnung; Fotogrammetrie; digitale Archivierung; digitale Nachlassverwaltung; Forschungsassistenz; Lokalrecherche; technische Dokumentation; Übersetzungsautomatisierung mit fachlicher Abnahme; Agentenentwicklung; KI-Workflow-Automatisierung.

## 3. Branchenübergreifende Eignungs- und Preislogik

Pro ServiceType müssen mindestens die Attribute \`service_unit\` (Stunde, Festprojekt, m², m³, Stück, Fahrt, Tag, Monat), \`pricing_basis\`, \`required_evidence\`, \`travel_cost_model\`, \`quote_binding_supported\`, \`appointment_length\`, \`credential_policy\`, \`service_area_type\`, \`quote_deadline_policy\` gepflegt werden.

Beispiele:
- Entrümpelung: m³/Projekt, Etagen, Zugang, Entsorgungsnachweise, Fotos, Besichtigung.
- Fotograf: Termin, Stunden, Zahl bearbeiteter Fotos, Fahrtkosten, Nutzungsrechte.
- Drohnenfotograf: Termin, Flugort und UAS-Zulässigkeit, Fluggerät/Pilot, Wetterfenster, Nachbearbeitung, Nutzungsrechte.
- Elektriker: erforderliche Handwerksrolle, Material, Sicherheit, Vor-Ort-Termin.
- Remote-Webdesign: deutschlandweit/online, Abnahmemilestones, IP-Rechte und Leistungsbeschreibung.

**Suchreichweite:** Keinen pauschalen Branchenradius hinterlegen. Jeder Anbieter kann spezifische PLZ-Listen, Polygone, Fahrzeiten, Servicegebiete, Fernbedienung und Mindesteinsatzwerte pflegen. Der Algorithmus prüft zuerst grobe Geodistanz, anschließend tatsächliche Anbieter-Service-Areas und nur für eine Kandidatenauswahl konkrete Straßenrouten/Fahrzeiten.

## 4. Zulassungs- und Rechtsklassen

| Klasse | Bedeutung | Produktregel |
|---|---|---|
| L0 | grundsätzlich unregulierte Dienstleistung | normale Identitäts-/Qualitätsprüfung |
| L1 | berufs-/gewerberechtliche Voraussetzungen | Qualifikation/Berechtigung vor buchbarem Angebot |
| L2 | behördliche/situative Genehmigungen am Einsatzort | Buchung nur vorbehaltlich oder nach Nachweis |
| L3 | besonders sensible personenbezogene Daten/Personengruppen | Datenschutz-/Zugriffs- und Schutzregeln |
| L4 | höheres physisches, finanzielles oder Haftungsrisiko | erweiterte Nachweise und Freigaben |
| L5 | besondere berufs- oder gebührenrechtliche Vermittlungsbeschränkungen | Provisions-/Verhandlungsfunktion standardmäßig gesperrt bis Rechtsprüfung |

Es sind mehrere Klassen je Service möglich. Die Einordnung im Katalog ist eine **Implementierungshypothese**, keine rechtsverbindliche Klassifikation.

Referenzen: https://www.gesetze-im-internet.de/hwo/anlage_a.html ; https://www.gesetze-im-internet.de/krwg/__53.html ; https://verwaltung.bund.de/leistungsverzeichnis/DE/leistung/99080103001000/

## 5. Pilot- und Ausbaupriorität

| Welle | Kategorien | Grund |
|---|---|---|
| P0 / Buchungspilot | Entrümpelung, Haushaltsauflösung | klarer RFQ-Kern und erkennbare Nachfrage |
| P0 / eingeschränkter RFQ-Test | Immobilienfotografie, Reinigung | prüft andere Preismodelle und Termine mit denselben Engines |
| P1 | Umzug, Möbeltransport, allgemeine Fotografie, Hausmeister, Garten | verwandte Geo-, Angebots- und Slotlogik |
| P2 | übliche Handwerksleistungen und ausgewählte Wartung | Fach- und Zulassungsprüfung |
| P3 | Drohnenservices, regulierte Berufe, Gesundheits-/Pflegeleistungen | erhöhte Regeln, Nachweise, Haftung |
| Katalog ab Start | alle 24 Domänen | Sucharchitektur und Firmen-Mapping, **ohne implizite Livebuchbarkeit** |

## 6. Wie der Katalog vollständig wird

Die vollständige kommerzielle Taxonomie entsteht **methodisch**:

1. Einlesen der offiziellen WZ-2025-Klassifikationsstruktur zur Mapping-Ebene (nicht mit einem abgeschlossenen Servicekatalog verwechseln).
2. Zuordnung zulassungspflichtiger Handwerke und Gewerbe (HwO und sektorspezifische Register).
3. Ergänzung um nutzerorientierte Tätigkeits-Synonyme aus erlaubten Quellen, tatsächlichen Anfragen und Firmenangaben.
4. Zuordnung eigener \`service_type\`-Codes, Parameter-Schemas, Preis-/Terminregeln, Genehmigungen und geografischer Einsatzmodelle.
5. Review je Unterkategorie durch geeignete Fachpersonen/Branchenanbieter und Veröffentlichung als versionierte Taxonomie.
6. Laufendes Monitoring neuer Leistungen, Berufe und Nachweise. Eine Kategorie gilt erst nach separatem Test als RFQ_ENABLED oder BOOKABLE.

**Abnahmekriterium:** Für jede veröffentlichte Dienstleistung ist erkennbar, ob sie nur recherchierbar, anfragbar, agentenfähig oder nach Anbieterbestätigung buchbar ist. Ein Unternehmen wird nicht automatisch allen branchenverwandten Services zugeordnet.

## 7. Verbindungen zu Einkaufskanälen

Jeder Katalogeintrag kann erlaubte Kanäle zugewiesen bekommen: interne Agenqo-Ausschreibung, registrierte Anbieter-MCPs, Quote-Link, Partner-API, eigene korrekt deklarierte Kleinanzeigen-Anzeigen als Nachfragegewinnung oder freigegebene Drittplattform-Einreichung. **Plattformbedingungen steuern die Nutzung.** Weder eine Webadresse noch ein technisch möglicher Browseragent verleiht Rechte zur massenhaften Ernte oder automatisierten Veröffentlichung.

## 8. Wissenschaftlich und wirtschaftlich sauber bleiben

Wir veröffentlichen **nicht** „Agenqo enthält sämtliche Dienstleister Deutschlands“ ohne Coverage-Audit. Der Unterschied zwischen identifizierten Betrieben, verifizierten Einträgen, gültigen Servicecapabilities, vertragsgebundenen Partnern und antwortaktiven Firmen bleibt sichtbar.

Marketing und Marktausbau werden anhand echter RFQ-Bearbeitungszeiten, Antwortquoten, Vertragsquoten, Auftragswerten, Beschwerden sowie Deckungsbeiträgen je Kategorie gesteuert. Suchvolumen, Klassifikationsbreite und Menge importierter Unternehmensprofile ersetzen keinen Liquiditätsnachweis.
