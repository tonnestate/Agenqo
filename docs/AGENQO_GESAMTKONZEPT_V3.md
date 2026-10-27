# Agenqo v3.0 – Vollständiges Strategie-, Geschäfts- und Architekturkonzept

**Stand:** 27. Oktober 2026  
**Produkt:** Agenqo – eigenständiger KI-nativer Dienstleistungsmarktplatz  
**Status:** Sollkonzept und umsetzungsfähige Spezifikation, noch kein Produktivnachweis  
**Vorgänger:** [Agenqo v2.0](AGENQO_GESAMTKONZEPT.md) · **Branchen:** [Leistungskatalog v3.0](AGENQO_BRANCHENKATALOG_V3.md)

## 0. Verbindliche Leitentscheidungen

1. **Vollständig eigenes Produkt:** eigener Backend-/Frontend-Code, Datenbank, Auth, Unternehmensprofile, Golden Company Record, Rechte, Geschäftsvorfälle, MCPs, Verträge, Abrechnung, Betrieb und Marke. Keine Laufzeitabhängigkeit zu TonnEstate. Altprojekte sind nur geprüfte Donoren.
2. **Zweiseitiger Markt für B2C und B2B:** Privatpersonen, gewerbliche Käufer, Unternehmen, Dienstleister und ihre jeweiligen Agenten nutzen dieselbe fachliche Engine mit unterschiedlichen Rechten.
3. **Kern ist die Vermittlungszentrale:** Ein Bedarf kann als interner Auftrag ausgeschrieben und gleichzeitig über verschiedene zulässige Anbieterkanäle eingeholt werden. Angebote laufen einheitlich zurück, werden verglichen, verhandelt und nach Autorisierung gebucht.
4. **Golden Company Record von Beginn an:** identifizierte Unternehmen können vor Registrierung im eigenständigen Verzeichnis stehen. Belegte Identität und Kontaktdaten sind aber kein Provisionsvertrag, kein Marketing-Opt-in und keine Garantie, dass ein Anbieter antwortet.
5. **Agent-fähig, kein Agent-Zwang:** vollständiges Webfrontend, registrierte Anbieter können Angebote manuell bearbeiten; eigene Anbieteragenten via MCP/API sind optional. Kunden können Website oder externen Käuferagenten verwenden.
6. **Dienstleistungen, keine Waren:** Foto-, Drohnen-, Bau-, Umzugs-, Reinigungs-, IT-, Beratungs- und viele weitere Services werden taxonomisch abgebildet. Aktivierung je Kategorie nur nach fachlichem/rechtlichem Qualitätsgate.
7. **Erlös ist ein Geschäftsprozess:** Provisionen nur aufgrund wirksamer Vereinbarung; alternative Kundengebühr und Anbieter-Premium werden früh getestet. Fixkosten, Anfrageverluste, Inbound-Marketing und Anbieterakquise fließen in Unit Economics ein.
8. **Kein ungeprüfter Spam und kein fremdes Scraping:** Kontaktwege haben eine rechtliche Policy-Engine. MyHammer und Kleinanzeigen sind nur genehmigte/zulässige Adapter, keine Datenquelle mit automatisch eingeräumter Weiterverwendungsberechtigung.
9. **Keine Blockchain im MVP:** differenzierte Zugriffsrechte, Zustimmung, zeitlich begrenzte Objektfreigaben, verschlüsselte Dateien, revisionsfähige Ereignisse und Integritätsnachweise lösen den beschriebenen Anwendungsfall einfacher.
10. **Keine voreilige Zusage der Marktlücke:** Wettbewerbsvorteil entsteht durch wiederholbar profitable, schnelle und vertrauenswürdige Vermittlung, nicht durch eine bloße MCP-Schnittstelle.

## 1. Das Produktversprechen und die klaren USPs

**Kunde/Privatnutzer:** „Sag Agenqo, was du erledigen lassen möchtest. Wir finden geeignete Firmen, beschaffen echte Angebote über mehrere Kanäle, vergleichen Gesamtpreise und Termine, verhandeln nach Freigabe und organisieren den Auftrag.“ Nutzbar per Suchseite, Formular, Chat und künftig verbundenem Remote Buyer-MCP.

**Kunde/Unternehmen:** „Stelle mehrere Maßnahmen als Projekt ein. Agenqo zerlegt sie in Gewerke, holt parallel Angebote ein, verfolgt Fristen, berücksichtigt Abhängigkeiten und liefert nach Tagen – bei angebundenen Agenten schneller – eine vergleichbare Entscheidungsvorlage.“ Nutzer- und Budgetrechte sowie Genehmigungsketten unterstützen B2B; dieselbe Infrastruktur funktioniert für B2C.

**Dienstleister:** „Finde dein bereits bekanntes Unternehmen, übernimm nach Nachweis das Profil, pflege Leistungen, Einsatzgebiete und Preis-/Kapazitätsregeln. Erhalte qualifizierte Anfragen, antworte mit einem Klick oder lasse deinen Agenten Angebote machen. Bezahle nur vereinbarte Leistungen.“ Grundfunktionen ohne KI und komplizierte Registrierung nutzbar.

**Externe Agenten:** „Ein einheitlicher Remote-MCP/API-Zugang zu verifizierbaren Unternehmensprofilen, RFQs, Angeboten, Terminen, Mandaten und Buchungsstatus; rollenbasiert, asynchron und belegbar.“

Der gemeinsame wirtschaftliche Nutzen lautet **weniger Such- und Vertriebsaufwand, bessere Angebotsqualität und höhere Abschlusswahrscheinlichkeit**. Diese Vorteile sind Hypothesen, bis der Pilot sie misst.

## 2. Agenqo Central Exchange (ACX): die eigentliche Vermittlungszentrale

ACX ist die einzige fachliche Transaktionsführung. Die Domänen:

- **Identity / Directory:** Golden Company Record, Standorte, Marken, Kontaktdaten, Leistungsfähigkeit, Provenienz, Unternehmensübernahme, Verifikation und Anbieterorganisation.
- **Service Catalog:** branchenübergreifende ServiceTaxonomy, genaue Leistungsprofile, fachliche Eingabefelder, Eignungs- und Rechtsgates, Preisbestandteile.
- **Demand / RFQ:** Kundenauftrag, Projekt, Gewerke/Leistungspakete, Anforderungen, vertrauliche Unterlagen, Autorisierungen, Fristen.
- **Matching / Routing:** geeignete Anbieter nach Leistung, Geografie, tatsächlichem Servicegebiet, Entfernung, Fahrtzeit, Anfahrtkosten, Verfügbarkeit, Kapazität, Vertrauensdaten und Kontaktstatus.
- **Channel Orchestrator:** Zustellung durch interne Einladungen, Portal, Provider-MCP/API, Einmal-Angebotslinks, rechtlich freigegebene Einzelanfrage oder genehmigte Drittplattformen.
- **Offers / Negotiation:** strukturierte Angebote, Versionen, Preis- und Leistungsnormalisierung, Vorbehalte, Rückfragen, eine optional abschließende Nachverhandlungsrunde, Gegenangebote.
- **Booking / Settlement:** genaue Kundenfreigabe, Anbieterbestätigung, Termin, Abschluss, Storno, Reklamation, vertragliche Gebühr und Abrechnung.
- **Audit / Data Access:** Identity and Access Management (IAM), Mandate, Claims, Objektzugriff, Datenherkunft, Zweckbindung, Benachrichtigung, Integritätslog.

### Ein Geschäftsvorfall, viele Kanäle

Ein Auftrag erhält **genau eine kanonische Request-ID**, egal ob Angebot via Webseite, Quote-Link, MCP, E-Mail oder genehmigter Fremdplattform kommt. **Source-Channel**, Roh-Nachweis, Angebotsbedingungen und Rechte bleiben getrennt gespeichert. Bloßes Kopieren fremder Plattformdaten ist ohne passende Rechte kein zulässiger Import.

### Beispiel „Mehrere Gewerke“

Ein Unternehmer: „In drei Ladenlokalen brauche ich Malerarbeiten, Reinigung und zwei Schaufensterfotos vor dem 15. November. Gesamtbudget maximal 7.000 €.“

Agenqo legt ein Projekt mit sechs Paketen an, fragt passende Dienstleister nach Einsatzort und Leistungsverfügbarkeit getrennt oder kombiniert an, wartet asynchron auf Antworten und erstellt nach Ablauf einer Deadline einen Vergleich mit offenen Risiken und zusammenhängendem Zeitplan. Anbieteragenten können sofortige indikative Preise oder echte vertraglich gültige Angebote liefern, wenn ihre Regeln und Kapazitätsdaten dies zulassen; Menschen antworten später. Verbindlicher Abschluss erfolgt nur mit passendem Mandat und Angebotsfreigabe.

## 3. Anbieterzustände und operative Kontaktstrategie

Unternehmensidentität, Profilinhaberschaft, Anbieterkommunikation, Partnervertrag und agentenfähige Schnittstelle sind **unabhängige Dimensionen**:

| Anbieterstufe | Was wir wissen | Kontakt-/Geschäftspfad | Provision |
|---|---|---|---|
| Recherchiert | Firmeneintrag mit Quellen/Unsicherheit | In Suche zeigen, Daten überprüfen; Einzelansprache nur nach Kanal-/Rechtsprüfung | Kein automatischer Anspruch |
| Kontaktierbar | geeigneter, aktueller Kanal | konkrete autorisierte RFQ, wenn rechtlich zulässig; kein Werbe-Drip | Ohne Vertrag kein Anspruch |
| Antwortaktiv | reales bestätigtes Feedback | strukturierter Quote-Link und kontextuelle Folgefragen | nur bei vereinbartem Vertrag |
| Registriert | Konto, verifizierte Unternehmensvertretung | Portal-/E-Mail-Benachrichtigung nach Nutzerpräferenzen | gemäß akzeptierten Terms |
| Vertragspartner | Provisionsbedingungen gültig | Transaktionsabschluss und Abrechnung | gemäß vereinbartem Ereignis |
| Agent-connected | verifizierte Agentendelegation | Provider-MCP, Webhooks, API-Tools, automatische Quote-Berechnung | wie vereinbart |

**Claim Your Business:** Ein registrierter Nutzer findet einen katalogisierten Betrieb, weist Organisationsvertretung nach (z. B. Domäne, verifizierte Geschäftsadresse, Register oder manuelle Prüfung), beansprucht das Profil und aktualisiert Selbstangaben. Amtliche Belege werden nicht überschrieben; Self-Assertions sind versioniert und gekennzeichnet. Missbrauch, fremde Zahlungs- oder Agentenrechte benötigen erhöhte Prüfungen.

**Unregistrierter Betrieb:** Eine Antwort per zeitlich begrenztem, vorgangsgebundenem Quote-Link ist ohne dauerhaftes Konto möglich, wenn die Anfrage ihn auf zulässigem Weg erreicht. Für eine Provisionspflicht muss die rechtlich geprüfte kommerzielle Vereinbarung vor der provisionspflichtigen Leistung wirksam geschlossen sein; kein stillschweigender Vertrag allein durch den Datenkatalog.

## 4. § 7 UWG und Provider Outreach: exakte Trennung

Ein **echtes, individualisiertes Käuferinteresse** und eine **Werbebotschaft für Agenqo** sind nicht identisch. Dennoch darf Agenqo nicht pauschal behaupten, jede automatisierte RFQ sei rechtlich unproblematisch.

1. **Partner, die RFQs ausdrücklich abonnieren:** klarer, vereinbarter Kommunikationskanal, passende Leistung/Region/Rate Limits; besonders sicherer Start.
2. **Unternehmen ohne Vertrag:** rechtliche Einzelfallprüfung, ob eine konkrete kundenbeauftragte Leistungsanfrage eine zulässige Anfrage oder tatsächlich Werbung ist; Versand nicht allein aus öffentlicher E-Mail-Adresse ableiten. Separates Opt-out, Häufigkeitskontrolle und Beleg.
3. **Werbung für eine Anbieterregistrierung:** eigenständiger Werbeprozess. Werbliche B2B-E-Mails benötigen grundsätzlich eine ausdrückliche Einwilligung, soweit keine enge gesetzliche Ausnahme greift (§ 7 Abs. 2 Nr. 2, Abs. 3 UWG). Mutmaßliche Einwilligung bei B2B-Telefonwerbung ist keine pauschale E-Mail-Ausnahme.
4. **KI-Telefonanrufe:** hohe Prüfungspflicht zu Kennzeichnung, kanalbezogenen UWG-/TKG-Regeln, Einwilligung und Gesprächs-/Aufzeichnungsregeln; nicht im Pilot automatisch ausrollen.
5. **Keine „einfach riskieren“-Strategie:** eine skalierte Belästigungs- und Abmahnstrategie zerstört Marge und Anbieterbeziehung. Ein anwaltlich geprüfter Kontaktleitfaden mit konkreten zulässigen Kommunikationsvarianten ist vor Live-Automatisierung notwendig.

**Technische Compliance:** \`contact_policy_decision\` pro Einladung: sender, buyer_authorization, provider, category, channel, lawful_basis, marketing_classification, opt_in, opt_out, cooldown, source, policy_version, approved_at. Ohne positive Entscheidung kein Versand. Kein Umgehen von Unterdrückungslisten durch Kanalwechsel.

Quelle: https://www.gesetze-im-internet.de/uwg_2004/__7.html

## 5. Sourcing: eigenes Ausschreibungsnetz plus fremde Portale

Agenqo hat selbst die **Ausschreibungs-/RFQ-Funktion**, damit die Plattform unabhängig ist. Externe Kanäle können ergänzend dienen:

| Kanal | Rolle | Bedingung |
|---|---|---|
| Agenqo Marktplatz | eingehende Bewerbungen / Matching / Angebote | eigener Betriebsstandard |
| Provider-Portal/Quote-Link | einmalige strukturierte manuelle Antwort | gültiges Token und vorliegende zulässige Anfrage |
| Provider-MCP/API | automatische Quote-/Slot-Antwort | Organisationsrecht, Scope und valide Regeln |
| Direkte E-Mail | Rückfrage / Einladung | kanal- und fallbezogene Kontaktfreigabe |
| MyHammer | fremder Ausschreibungskanal | nur erlaubte Partnerintegration oder explizit vertragskonforme Kundennutzung; keine Datenbankabsaugung |
| Kleinanzeigen | **Nachfrage- und Angebotsgewinnung** über eigene korrekt gewerbliche Inserate sowie zulässige Einzelfallnutzung | keine automatisierte Account-Bedienung oder Drittprofilernte ohne schriftliche Erlaubnis/geeignete Schnittstelle |
| Weitere Branchenportale | Vermarktung oder zusätzlicher RFQ-Kanal | je Betreiber expliziter Connector-Vertrag |

**MyHammer:** Die aktuellen Auftraggeber-AGB untersagen die gleichzeitige Mehrfachveröffentlichung desselben Auftrags und die Veröffentlichung von Aufträgen anderer Parteien; auch Datensammlung/-verwertung ist beschränkt. Browserautomatisierung ist daher kein naiver Umgehungsweg. Ein offizieller kommerzieller Adapter benötigt Erlaubnis. https://www.my-hammer.de/allgemeine-geschaefts-bedingungen

**Kleinanzeigen:** eigene Anzeigen und Gesuche sind grundsätzlich möglich, aber gewerbliche Nutzungsregeln, Kategorie, Anzeigengebühren und Plattform-AGB gelten. Gewerbliche Dienstleistungen haben seit 01.09.2026 ein kostenloses Inserat innerhalb 30 Tagen; weitere kostenpflichtige Dienstleistungsanzeigen laut Betreiber 3,99–8,99 € inkl. MwSt. pro Anzeige (kategorieabhängig), standardmäßig 30 Tage Laufzeit. Die Plattform untersagt Scraper und automatische Mechanismen ohne ausdrückliche schriftliche Zustimmung. Folglich zuerst **offizielle eigene Anzeigen/Traffic-Akquise und zulässige manuelle Bearbeitung**, automatisierte Fremdplattform-Workflows nur nach Lizenz/Kooperation.  
Quellen: https://themen.kleinanzeigen.de/gewerblich-handeln/ · https://themen.kleinanzeigen.de/nutzungsbedingungen/

**Source-Attribution:** Jeder Auftrag speichert \`acquisition_channel\`, Anzeigen-/Kampagnen-ID, Fremdplattformkosten, Referral-/Vertragsbedingungen, Lizenzen, Kommissionsanspruch und Importrechte. Kein Rankingvorteil aus verdeckter Herkunft.

## 6. Standort- und Umkreissuche: keine starre Kilometerlösung

Die geografische Matching-Engine muss zwischen **Firmensitz**, **operativem Standort**, **Servicegebiet**, **tatsächlicher Anfahrtsroute**, **Einsatz-/Travel-Kosten** und **Termin-/Kapazitätsradius** unterscheiden. Ein rein geometrischer 20-km-Kreis ist für Umzüge, Drohnenfotografie und Fernberatung unbrauchbar.

### Stufenmodell

1. **Normierte Geokoordinaten:** Ortsadresse/PLZ mit Quellen- und Genauigkeitsstufe. Für Kundenadressen im öffentlichen Kontext initial PLZ/Gebiet, genaue Anschrift nur bei berechtigtem Bedarf.
2. **Grobe Suchmenge:** PostGIS räumlicher Index und geometrische Distanz (Haversine/ST_DWithin) als günstiger Vorfilter, nicht als behauptete Fahrstrecke.
3. **Service Area Policy:** Anbieter definiert nicht nur Radius, sondern ggf. einzelne PLZ-Listen, Polygone, Länder, Depotstandorte, mobile Einsätze, Start-/Endorte und Ausschlüsse.
4. **Routen-/Fahrzeitprüfung:** Nur qualifizierte Kandidaten über OSRM/OpenRouteService/Google Routes Matrix o. Ä. prüfen; Rückgabe unterscheidet Straßendistanz, Reisezeit, Maut und Routing-Confidence. Anbieter kann Reisezeitgrenzen sowie Mindestauftrag und Anfahrtszuschlag angeben.
5. **Zeit/Kapazität:** Slot, Schicht, Anfahrt und bestehende Terminbindung prüfen. Ohne aktuelle Kalender-/Agentenantwort nur „Anfrage möglich“ ausgeben, nicht „frei“.
6. **Fachliche Sonderfälle:** Ein Umzug hat Quell- und Zieladresse; Drohneneinsatz Flugzonen/Startsicherheitsprüfung; Fotograf zeitliche Dauer und Referenzgebiete; Remote-Dienstleistung kann überregional sein.
7. **Transparenz:** Suchresultat zeigt „Anfahrt laut Anbieter inklusiv“, „Entfernung circa X km“ oder „Servicegebiet laut Anbieter“. Keine erfundenen exakten Reisezeiten/Preise.

Routenmatrizen sind kostenpflichtig oder limitiert; erst günstiges Spatial Filtering, danach gezielte Route-API. Google rechnet Route-Matrix nach Elementen ab. Quelle: https://developers.google.com/maps/documentation/routes/usage-and-billing

## 7. Mehrkategorie-Katalog und Gewerke

Agenqo verwaltet eine **vollständige, erweiterbare Dienstleistungstaxonomie**, keine vorgetäuschte vollständige Aufzählung aller deutschen Berufe. Der Katalog ist versioniert und mit Branchenklassifikationen, Synonymen, Leistungsanforderungen und Anbietercapabilities verbunden.

Die erste Katalogfassung steht in [AGENQO_BRANCHENKATALOG_V3.md](AGENQO_BRANCHENKATALOG_V3.md), insbesondere:
- Entrümpelung, Umzug, Transport und Logistik;
- Immobilienservices, Hausverwaltung, Reinigung, Garten, Hausmeister/Winterdienst;
- Elektro, Sanitär/Heizung, Dach, Maler, Tischler, Boden, Bau-/Sanierung;
- Schädlingsbekämpfung, Notdienste, Fahrzeuge, Reparaturen;
- Fotografen, **Drohnenfotografen**, Film, virtuelle Rundgänge, 3D-Scans, Grundrisse, Medien, Design;
- IT, Websites, Daten, Sicherheit, Übersetzung, Bildung, Veranstaltungen, Büro-/Beratungsleistungen und weitere Kategorien.

Pro Leistungsart: Qualifikationen, Gewerke, Arbeitsort, Reisetyp, Erlaubnisse, Preisstruktur, Gefahr-/Haftungsklasse und Standard-Servicegebiet. In regulierten Bereichen (z. B. Drohnenflüge in geografischen UAS-Gebieten, Abfallbeförderung) vor Buchung Zulässigkeit und erforderliche Nachweise prüfen. Quellen: https://verwaltung.bund.de/leistungsverzeichnis/DE/leistung/99080103001000/ · https://www.gesetze-im-internet.de/krwg/__53.html

Der **Katalog kann deutschlandweit erscheinen**, ohne dass jede Kategorie sofort automatisch buchbar ist. Servicezustände sind \`LISTED\`, \`RFQ_ENABLED\`, \`AGENT_QUOTABLE\`, \`BOOKABLE\`, \`PAUSED\`.

## 8. Golden Company Record – eigenständig und von Anbietern bearbeitbar

Agenqo trennt **juristische Firma, Handelsname, Geschäftsstandort, Leistungsstandort, Branchencapability, Servicegebiet, Kontaktkanal und Anbieterplattformorganisation**.

Mindestens folgende Datenobjekte:
- \`Company\`, \`Brand\`, \`Location\`, \`CompanyContact\`, \`CompanyCapability\`, \`ServiceArea\`, \`Credential\`;
- \`SourceObservation\`, \`Claim\`, \`Evidence\`, \`PublishedGoldenField\`, \`MatchDecision\`, \`DataLicense\`;
- \`ProviderOrganization\`, \`ProviderMembership\`, \`OwnershipClaim\`, \`AgentDelegation\`, \`CommunicationPreference\`, \`CommercialAgreement\`;
- \`ServiceProfile\`, \`ServiceProject\`, \`WorkPackage\`, \`ServiceRequest\`, \`ProviderInvitation\`, \`Offer\`, \`OfferRevision\`, \`NegotiationMandate\`, \`Booking\`, \`CommissionEvent\`, \`Dispute\`, \`AuditEvent\`.

**Recherchierte Daten sind nicht automatisch zur Veröffentlichung oder kommerziellen Weiterverarbeitung lizenziert.** Datensätze werden pro Quelle auf Dateneigentum, Lizenz, erlaubte Zwecke, Gültigkeit und personenbezogene Daten geprüft.

**Claim:** Firmenvertreter legitimiert Konto und Unternehmensbeziehung; ohne Nachweis keine Administration. Änderungen werden als versionierte Self-Assertions gespeichert; kritische Felder (rechtlicher Name, Steuer-ID, Zahlungen, Agentenberechtigungen) erhalten zusätzliche Prüfungen. Unternehmen können die Quellenlage einsehen, Widerspruch einreichen und Berichtigung beantragen.

**Pilot:** keine komplizierte Volluniversums-Migration, aber ein echtes eigenes Golden-Record-Modell für Pilotfirmen. Erweiterte Evidence-/Conflict-Pipelines werden graduell implementiert, nicht gestrichen.

## 9. Angebotsaufnahme: Mensch oder Agent, ein gemeinsamer Vertrag

### RFQ

Ein Kundenprojekt besteht aus einem oder mehreren \`WorkPackage\`-Objekten mit Standort, Leistungsscope, Medien, Budget, Deadline, Datenschutzfreigabe und verlangtem Angebotsstatus. Die Anfrage kann als **öffentliche Ausschreibung** für geeignete Anbieter oder als gezielte Einladung gestartet werden. Sensible Angaben sind nie pauschal öffentlich.

### Antwortpfade

- Anbieter mit \`AGENT_CONNECTED\`: Agent prüft Unternehmensregelwerk, Preise, Reisezeit, Kalender und Auftragspipeline, dann liefert er **signiertes** strukturiertes Angebot und ggf. Termin.
- Registrierter Anbieter ohne Agent: Dashboard oder Benachrichtigung, antwortet manuell; optional Agenqo-AI erzeugt **Entwurf**, den Anbieter freigibt.
- Nicht registrierter, zulässig kontaktierter Anbieter: zeitlich begrenzter Quote-Link ohne Konto. Keine bloße Anzeige einer öffentlichen Mailadresse als Opt-in.
- Drittplattform: erst bei erlaubter Einbindung, mit Quellnachweis und beschränkter Datenverwendung; notfalls bleibt der Prozess außerhalb Agenqo.

### Preis-/Verfügbarkeitsstufen

\`INDICATIVE\` (automatisch kalkulierte Schätzung), \`CONDITIONAL\` (mit Vorbehalten), \`INSPECTION_REQUIRED\`, \`BINDING_UNTIL\` (echt autorisierte Anbietererklärung), \`EXPIRED\`, \`WITHDRAWN\`, \`ACCEPTED\`. Ein Anbieteragent kann nur mit expliziten Freigaberegeln \`BINDING_UNTIL\` erzeugen.

### Vergleich

Preis als vollständiger Kunden-Bruttobetrag mit Anfahrt, Material, Zuschlägen, gegebenenfalls Steuern; Leistungsbedingungen, Termin, Validität und Vertrauenslage separat. Verglichen werden nur gleiche oder transparent abgeglichene Scopes. Rankinggrundlagen werden offen gelegt; Provisionsbetrag ist kein verdecktes Qualitätsmerkmal.

### Verhandlung und Annahme

Eine optionale „Best and Final“-Runde mit maximal definierter Frist, ohne vertrauliche Wettbewerberangebote weiterzugeben. Vollständige Agent-to-Agent-Verhandlung ist Zielbild; MVP kontrolliert. Kunde genehmigt **Fingerprint des genauen Angebots**. Anbieter bestätigt denselben Stand und eine reale Verfügbarkeit. Kein Vertragsschluss allein aus unvalidierter LLM-Textausgabe.

## 10. Kundenerlebnis – vollständiger Ablauf mit Tagen und Sofortantworten

Beispiel Privatkunde: „Fotograf für meine Hochzeit in vier Wochen“. Agenqo fragt Datum, Ort, Umfang, Bildrechte, Budget und gewünschte Lieferung; sucht Anbieter nach realer Anfahrtszeit und verfügbarem Slot; sendet Ausschreibung und gezielte Einladungen; sammelt innerhalb festgelegter Frist Angebote, prüft Referenzen/Leistungsumfang und liefert Auswahl. Anbieteragenten können innerhalb von Sekunden/Minuten antworten, menschliche Anbieter innerhalb von Stunden/Tagen.

Beispiel gewerblicher Kunde: „Entrümpelung, Reinigung und Drohnenaufnahmen für vier Immobilien bis Freitag“. Agenqo erzeugt getrennte Arbeitspakete und Abhängigkeiten (Entrümpelung vor Foto), sammelt parallel Angebote, konsolidiert und verhandelt ggf. die Kombination. Drohnenbilder dürfen erst nach geoprüfungs- und fachrechtlichen Freigaben gebucht werden.

**Service-Level ohne Überversprechen:** \`immediate_quotes\` nur für nachweislich aktuelle automatisch autorisierte Angebote; andernfalls \`COLLECTING_UNTIL\` mit Deadline, Anzahl Einladungen, Anzahl Antworten, offenen Rückfragen, nächstem Update. Als Default kann nach 48–72 Stunden verglichen werden, bei fehlenden Angeboten wird der Sachstand erklärt und ggf. die Suche nach Nutzerfreigabe erweitert. Ein später eintreffendes Angebot ändert keinen bereits genehmigten Buchungsstand.

## 11. Zugriffsmodell statt Blockchain

**Keine Blockchain notwendig:** ACL/ABAC bzw. RBAC mit Objekt- und Zweckgrenzen, OAuth2/OIDC, Agent Delegation, Scope-Tokens, signierte URL für Dokumente, verschlüsselte Speicherung und Audit mit Hash-Ketten. Anbieter A darf nur an A gerichtete Vorgänge und seine eigenen Angebote sehen; Kunde darf erhaltene Angebote sehen; Konkurrenten dürfen keine fremden Kalkulationen abrufen. Unternehmensagent darf nur nach nachgewiesener Delegation handeln.

Für besonders manipulationssensitive Nachweise können später **periodische externe Hash-Anker oder qualifizierte Zeitstempel** bewertet werden; weder Kundendaten noch vertrauliche Angebotstexte gehören auf eine öffentliche Blockchain. Berechtigungen sind widerrufbar und zeitlich begrenzt.

## 12. Plattform-MCP, Agenten-Discovery und Kosten

Agenqo betreibt **Remote-MCP**, keine Pflicht-Desktopsoftware und keinen individuellen MCP-Server pro Dienstleister. Website und MCP sind Fassaden über einer versionierten REST-Business-API.

**Buyer-MCP** (Beispiele): \`discover_services\`, \`search_providers\`, \`create_project\`, \`create_rfq\`, \`get_rfq_status\`, \`list_offers\`, \`compare_offers\`, \`request_negotiation\`, \`approve_offer\`, \`get_booking_status\`.

**Provider-MCP** (Beispiele): \`claim_company\`, \`get_my_company\`, \`propose_company_update\`, \`list_invitations\`, \`submit_quote\`, \`update_availability\`, \`counteroffer\`, \`confirm_booking\`, \`view_settlement\`.

Scopes u. a. \`catalog.read\`, \`buyer.rfq.write\`, \`buyer.booking.approve\`, \`provider.profile.write\`, \`provider.quote.write\`, \`provider.booking.confirm\`. Freigaben werden **serverseitig geprüft** und nicht aus freien Toolargumenten abgeleitet.

Tool Discovery: öffentlich dokumentierter stabiler HTTPS-Endpunkt, JSON-Schemas, Ressourcenmetadaten und gegebenenfalls Veröffentlichung im offiziellen MCP Registry (https://registry.modelcontextprotocol.io/); das garantiert keine automatische Verwendung durch ChatGPT/Claude. n8n ist kein öffentliches System of Record.

### Schätzung der Plattformkosten – Szenario, keine Anbieterpreise

Ein selbstgehosteter Remote-MCP ist zunächst Software, nicht automatisch eine laufende Gebühr pro registriertem Unternehmen. Kosten entstehen durch Betrieb, Requests, Auth, Rechenmodelle, Geokodierung/Route, Kommunikation, Monitoring und menschliche Rückfragen.

Für erste Budgetplanung als **Prüfhypothese**: gemeinsamer Server/MCP-Betrieb und Monitoring 50–250 € pro Monat bei kleiner Pilotlast (ohne bezahlte Entwicklung, Haftpflicht, Rechtsprüfung, Marketing und Support), plus variable Kommunikation/AI/Geo je Vorgang. Bei 1.000 aktiven Agenten oder hohen AI-Sprach-/Routing-Volumina muss Last- und Kostentest gesondert durchgeführt werden. Gratisnutzung der API ist eine Geschäftsentscheidung, kein technischer Zwang.

**MCP-Preismodell:** kostenlose Suche/Profilverwaltung, kontingentierte RFQs oder Erfolgsgebühr, Premium für erweiterte Automatisierung/CRM-/Kalenderintegration; missbrauchssichere Rate Limits und Organisationsbudgets.

## 13. Rolle von n8n und technologischer Umsetzungsstack

**Backend:** eigenständige Python/FastAPI-API und deterministische Domänenmodelle; **Datenhaltung:** PostgreSQL + PostGIS (räumliche Suche), versionierte Migrationen. **Frontend:** eigene responsive SEO-fähige Webanwendung für Käufer, Anbieter und Backoffice. **Agent Runtime:** austauschbarer Modellrouter (nicht auf einen einzigen Provider und nicht auf „FREE_ONLY“ festlegen); LLM für Intake, Parsing, Erklärung und Entwürfe, niemals allein für Rechtsverbindlichkeit. **n8n:** Benachrichtigungen, E-Mail- und Webhook-Zustellung, Wartezustände, Wiederholung, Kanaladapters, Monitoring.

Ereignisse: \`PROJECT_CREATED\`, \`PACKAGE_QUALIFIED\`, \`RFQ_PUBLISHED\`, \`INVITATION_APPROVED\`, \`INVITATION_SENT\`, \`QUOTE_RECEIVED\`, \`OFFER_NORMALIZED\`, \`NEGOTIATION_STARTED\`, \`OFFER_APPROVED\`, \`BOOKING_CONFIRMED\`, \`WORK_COMPLETED\`, \`DISPUTE_OPENED\`, \`COMMISSION_ELIGIBLE\`.

Outbox, Deduplizierung, Idempotency Keys, Retry-/Dead-Letter-Regeln; Agenten-Prompt-Injection-Abwehr und Tenant Isolation. n8n erzeugt **keine** eigenmächtigen verbindlichen Zahlungen oder Bestellungen.

**Architekturrisiko:** Nutzerseitige Kommunikation und parallele Anbieterantworten erfordern echte asynchrone Vorgänge; ein langer synchroner MCP-Toolcall ist ungeeignet.

## 14. Provisions- und Erlösstrategie

**A. Anbieter-Erfolgsprovision:** Vertraglich vorab vereinbarte Provision. Der Golden Record allein ist keine Vertragsgrundlage. Testtarif 8 % vom ausgewiesenen Netto-Leistungswert mit möglichem Mindestbetrag; je Kategorie müssen Umsatzsteuer, Kleinunternehmerregelung, Vertragsinhalt und wirtschaftliche Tragfähigkeit gesondert modelliert werden.

**B. Kunden-Beschaffungsgebühr:** Transparente einmalige Gebühr oder B2B-Kontingent bei nicht provisionierbaren Aufträgen, hohen Servicekosten oder unabhängiger Ausschreibung; beim Verbraucher kostenpflichtiger Abschluss nur mit korrekter Bestellinformation und Autorisierung. Einsparprämie nur mit belastbarer Referenz.

**C. Anbieter-Premium:** Kalender-Sync, Kalkulationsagent, Regeln, CRM/ERP-Connector, Agenten-MCP mit erweiterten Kontingenten, Auto-Response, Analyse. Dabei nicht den Basis-Marktplatzzugang unbrauchbar machen.

**D. B2B-API/White-Label:** später bezahlte RFQ-/Beschaffungsdienste für Partneragenten; unabhängig vom Umsatz anderer Plattformen.

**Wichtig:** Ob Kunden- und Anbietergebühren kumuliert werden, welche Interessen offenzulegen sind und ob es für einzelne Berufsgruppen rechtliche Schranken gibt, muss vertraglich geprüft werden. Keine pauschalen Provisionsaufschläge auf fremde Endpreise.

### Unit Economics – Beispiel und echte Verlustfälle

Bei 1.500 € brutto Auftrag und 19 % unterstellter USt im Dienstleisterpreis: Netto 1.260,50 €, 8 % Provision = **100,84 € Netto-Plattformertrag**. Bei 45 € direkten und zugeordneten variablen Kosten je Buchung verbleiben **55,84 € je Buchung vor Fixkosten**. Das ist nur eine Rechenannahme.

**Zwingende Ergänzung:** RFQ-Kosten bei **nicht** gebuchten Aufträgen müssen mitgerechnet werden! Beispiel: 20 RFQs, fünf Buchungen, 45 Minuten manueller Aufwand je RFQ und 30 €/Stunde = 450 € allein für Begleitung; Provisionsertrag 5 × 100,84 € = 504,20 €; damit fast kein Ertrag vor AI, Marketing, Support und Hosting. Auch Provider-Akquise, Storno, Inkassorisiko, CAC je Kanal, Instagram-/Kleinanzeigen-Ausgaben werden je Kanal erfasst.

Formeln:
- \`RFQ Deckungsbeitrag = realisierte Plattformumsätze aus der Kohorte - sämtliche direkt zurechenbaren Kosten für erfolgreiche UND erfolglose RFQs\`.
- \`CAC pro Buchung = gesamte Kundengewinnungsausgaben eines Kanals / zurechenbare erfolgreiche Buchungen\`.
- \`Anbieter-Aktivierungs-CAC = vertraglich zurechenbare Vertriebskosten / neu aktive Anbieter\`.

Der B2B/B2C-Mix und Auftragswert je Gewerk werden getrennt erhoben. Keine ungeprüften „1.600 € Durchschnittsauftrag“ als bewiesener Marktwert.

## 15. B2C + B2B Nachfragegewinnung, Social und Kleinanzeigen

**B2C** ist von Tag 1 produktfähig: persönliche Dienstleistungen, einmalige Privataufträge, flexible Fristen, transparente Preise. **B2B** hat dieselben Kernoperationen plus Projektpakete, Teams, Kostenträger und Freigaben.

**Kanäle:** eigene SEO-Landingpages zu Service × Region, direkte Markenpräsenz, lokale Partnerschaften, Google, Kleinanzeigen (gewerbliche echte Inserate), Instagram-Reels, TikTok, YouTube Shorts, Empfehlungslinks, bestehende Netzwerke, Agenten-MCP-Discovery/Apps.

**10.000–20.000 Videos** sind keine Erfolgsgarantie und dürfen nicht blind als Spam ausgerollt werden. Erforderliche Stufen: testbare 20–50 kreative Konzepte pro Kategorie, echte Ergebnis-/Kostendaten, Variation und teilautomatisierte Erstellung, Prüfung von Wiederholung/Plattformregeln, Steigerung nur bei messbaren qualifizierten RFQs und positivem CAC. Vermeiden: irreführende Vorher-/Nachher-Videos, ungeklärte Bildrechte, künstliche Anbieterbewertungen.

**Kleinanzeigen:** eigenes gewerbliches Profil, lokale Dienstleistungen korrekt anbieten, Klicks/Leads in Agenqo nur mit erlaubten Tracking-/Vertragswegen; Kontakt und Veröffentlichung ausschließlich regelkonform. Nicht als kostenlose, unbegrenzt automatisierbare Daten- oder Spamquelle behandeln. Anzeigenkosten müssen in CAC einfließen.

**Anbietergewinnung:** kostenloses Claim-Your-Business, attraktive Anfragequalität, kurze Antwortformulare, optionaler Agent, klare Provision. Reale Aufträge stärker als massenhaft abstrakte „Jetzt registrieren“-Botschaften.

## 16. Pilot-/Rolloutkonzept – schnell und trotzdem echtes Marktplatzprodukt

**Keine Festlegung auf B2B als einzigen Kunden.** Erste Kategorie: Entrümpelung/Wohnungsauflösung für B2C und B2B in einer Pilotregion; gleichzeitig zwei kleinere Neben-Serviceprofile, z. B. Immobilienfotografie und Reinigung, zunächst als eingeschränkter RFQ-Test. Der **Katalog** darf deutschlandweit vollständig strukturiert werden, aber nur Kategorien mit brauchbaren Daten und Partnern dürfen als unmittelbar buchbar erscheinen.

### Phase 0: Vorbereitungen

- eigene Agenqo-Repo-/Betriebs- und Datenarchitektur;
- Rechte-/Daten-Audit möglicher Donoren;
- Basistaxonomie, Eignungs- und Geographic-Service-Area-Schemas;
- Rechtsprüfung der Provider-Ansprache nach Kommunikationskanal, Marketplace-Verträgen, Preis-/Vergleichs-/Ranking-Transparenz sowie Fachrecht;
- frühe Partner- und Nachfragegespräche, Pilotgebühren/Einwilligungen;
- **Entscheidungsvorlage** für Kleinanzeigen/MyHammer-Connectoren: erlaubt, nur manuell, Partnervertrag nötig oder verboten.

### Phase 1: Minimale funktionsfähige Exchange

- öffentliches Search-/Service-Frontend, B2C/B2B-Intake;
- eigenes Golden-Company-Minimum mit Quell-/Statusmerkmalen;
- einfache Anbieterregistrierung, Profil-Claim-Grundprozess und Anbieterprofil;
- RFQ-Ausschreibung + gezielte Einladungen + sichere Quote-Links;
- Geo-Engine mit Servicegebieten und realen Route-Prüfungen für finale Kandidaten;
- n8n-Kanal für freigegebene Einladungen, Portalantwort;
- strukturierte Angebote, Kosten-/Steuerlogik, Vergleich, Autorisierung und Anbieterbestätigung;
- Provisionsvertrags- und Gebührenereignis; Dashboards mit vollständigen Kosten je RFQ.

### Phase 2: Echte Transaktionen

20–50 echte Vorgänge mit menschlicher Kontrolle, Antwortzeit, Zahl zugelassener/vergleichbarer Angebote, Bookings, Stornos, Reklamationen und Deckungsbeitrag. Bezahlung nicht simulieren. Initiale mehrkanalige Demand-Akquise messen.

### Phase 3: Remote MCPs – gestufte Veröffentlichung

Buyer-MCP \`search\`, \`create_rfq\`, \`status\`, \`compare\`, nach Genehmigung \`approve\`; Provider-MCP \`list\`, \`submit_quote\`, \`update_availability\`, nach Mandats-/Sicherheitstest \`confirm_booking\`. Dieselbe API wird intern schon in Phase 1 genutzt. Ein Agent kann sich via Discovery über die MCP Registry informieren; Hosts erfordern separate Integration.

### Phase 4: Multi-Category, Provider-Automation, Drittadapter

Vollständiger, gepflegter Servicekatalog mit weiteren Branchen; Anbieter-Agent-Preisregeln und echte Availability-Feeds; genehmigte Plattform-Connectoren; erweiterte Agent-to-Agent-Verhandlung; SaaS- und B2B-API-Preise. Scale nur bei wirtschaftlich positiver Kategorie-/Region-Kohorte.

### Gates

**G0:** rechtlich freigegebener Kontaktweg; Anbieter-/Auftraggeberinteresse; kein unklarer Provisionsvertrag.  
**G1:** ein realer RFQ mit mindestens zwei vergleichbaren Angeboten, nachvollziehbarem Auftrag/Bestätigung und einem wirtschaftlich erfassten Gebührenereignis.  
**G2:** nach mindestens 20 realen RFQs: Antwort- und Buchungsraten, RFQ-Deckungsbeitrag inkl. erfolgloser Fälle und Supportminuten, Kundennutzen und Anbieterqualität dokumentiert; Schwellen vor Pilot verbindlich festlegen.  
**G3:** nach erfolgreichem Wiederholungstest werden MCPs/weitere Kategorien ausgebaut. Kein „100 % autonom“ als Product Claim ohne Livebeleg.

## 17. Recht, Haftung und Vertrauen

- **§ 7 UWG:** Kanal-/Anlass-/Werbeprüfung vor externer Ansprache. Marktplatzprofil ist kein generelles Newsletter-Opt-in.
- **DSGVO:** Kundenort, Foto, Auftrag, Angebot, Unternehmensansprechpartner nur zweckgebunden; öffentliche Katalogansicht und provider-private Daten getrennt; Lösch-/Widerspruchs- und Herkunftsmechanismen.
- **Vertrag:** Klare Rolle Vermittler vs. Leistungserbringer, Allgemeine Geschäftsbedingungen, gegebenenfalls Widerruf und Verbraucher-Bestellprozess (§ 312j BGB); Autorisierungen, Vollmacht, beidseitige Annahmen.
- **Ranking:** Hauptparameter, tatsächliche Verfügbarkeit und Vergütungsbeziehungen transparent; keine erfundenen Bewertungen und Termine.
- **Handwerk/Abfall/Drohnen:** Qualifikations- und Erlaubnispflichten je Kategorie, z. B. § 53 KrWG und geografische UAS-Gebiete.
- **DSA/P2B-Verordnung, AI Act:** Anwendbarkeit, Händleridentifikation, Transparenz und Plattformpflichten nach konkretem Modell prüfen.
- **Zahlungen:** Im MVP direkte Kunden-/Dienstleisterzahlung, Agenqo fakturiert vereinbarte Gebühren; später lizenzierter Payment-Partner. Keine pauschale Treuhandpflicht oder Kundengeldverwahrung.
- **Disintermediation:** Statt aggressiver Kontaktblockaden messbarer Mehrwert (Vergleich, sichere Freigabe, Qualitätsbelege, Termine, Wiederholung, Dokumente); Nachprovision nur bei wirksamer, fairer Vertragsregel.
- **Integrität:** Anbieterantworten sind nicht vertrauenswürdige LLM-Anweisungen; nie automatische Vollmachtserweiterung.
- **Missbrauch:** Agenten-/Account-Verifikation, Bot-Limits, Anti-Fraud, Doppelprofilprüfung, keine massenhaft gefälschten Gesuche.

## 18. Umsetzbare Entwickler-Tickets

1. Eigenständiges Repo/CI, Container, PostgreSQL + PostGIS, API-Auth/Organisationen; keine TonnEstate-Referenz zur Laufzeit.
2. Golden Company Minimum + Contact Policy + Source Metadata + verifizierter Anbieter-Claim.
3. Versionierter branchenübergreifender Servicekatalog, ServiceArea-Typen und Regionalmatching mit Routenprüfung.
4. Projekt, WorkPackage, Request, RFQ, Public/Targeted Invitation und kanalunabhängige Rücklaufzuordnung.
5. Anbieterportal + Einmal-Quote-Link, revisionssichere Angebote/Angebotsstatus.
6. Preis-/Steuer-/Leistungs-Vergleich, Kundengesamtpreis und neutrale Rankings.
7. n8n-Outbox, E-Mail/Webhooks und Rate Limits mit dokumentierter Kontaktfreigabe.
8. Angebots-Autorisierung, Provider-Bestätigung, Slot, Booking-Fingerprint, Storno und Dispute.
9. Vertragsbasierte Commission Engine, Kunden-Servicegebühren-Option, Nettoerlös und Kosten je RFQ.
10. B2C/B2B-Kunden-Frontend, Firmenprofil, Anbieter-Dashboard, Ops-Backoffice.
11. Audit, Idempotenz, Multi-Tenant/Objektzugriff und Attachment-Zugriff, Backups.
12. Buyer- und Provider-Remote-MCP (zunächst read/query/RFQ; mutierende Aktionen gated).
13. Drittkanal-Registry mit **Capability & Permission Matrix**, beginnend bei Kleinanzeigen als eigener Marketingkanal und MyHammer nur mit überprüfter Erlaubnis.
14. Konversions-/Akquisitionsmessung für Instagram/SEO/Kleinanzeigen, Kanal-CAC und RFQ-Effizienz.
15. End-to-End-Tests mit drei Anbietertypen: Mensch im Web, Quote-Link, autonomer Anbieteragent; alle laufen über dieselbe Request-ID.

**Definition of Done:** Kein Modul gilt als „fertig“, ohne Tests, reale Integration wo vorgesehen, Status-/Audit-Kontrolle, Berechtigungsprüfung, Kostenmessung und unabhängigen Agenqo-Betrieb.

## 19. Offene Entscheidungen (mit Standardvorschlag)

| ID | Entscheidung | Empfehlung |
|---|---|---|
| D1 | Markt | Deutschland, B2C und B2B gleichberechtigt |
| D2 | erster Buchungspilot | Entrümpelung/Wohnungsauflösung in einer Region |
| D3 | Katalog | breiter Servicekatalog ab Start, Kategorien je nach Reife freigeben |
| D4 | Golden Record | eigener Datenbestand und von Anbietern bearbeitbare Claims; Belege stufenweise |
| D5 | Anfragewege | internes RFQ, Anbieter-MCP/API, Quote-Link, zulässige Einzelanfrage, genehmigte Fremdplattformen |
| D6 | Anbieter-Vergütung | 8 % Netto-Provision als Testwert, Alternative kundenseitige Servicegebühr |
| D7 | Agenten | Buyer-/Provider-MCP gleicher fachlicher API; zuerst verlässlicher Kern |
| D8 | Geografie | Vorfilter + Service Area + optionale Route-/Fahrzeitmatrix |
| D9 | Recht | Anwaltlicher Kanal-/Terms-Check vor automatischer Kontaktierung |
| D10 | Datenschutz | strikt zweckgebundene Objektfreigaben, keine Blockchain |
| D11 | Marketing | SEO, Kleinanzeigen, Instagram/Short Video, B2B, Empfehlungen; CAC je Kanal |
| D12 | Fremdplattformen | Adapter nur nach bestätigten Nutzungs-/Automatisierungsrechten |

## 20. Referenzen

**Eigene Donoren:** https://github.com/tonnestate/TonnEstate · https://github.com/tonnestate/LemonMe · https://github.com/tonnestate/DragonFruitMe · https://github.com/tonnestate/BlackberryMe · https://github.com/tonnestate/CherryMe

**Standards:** https://modelcontextprotocol.io/ · https://registry.modelcontextprotocol.io/ · https://docs.n8n.io/

**Recht:** https://www.gesetze-im-internet.de/uwg_2004/__7.html · https://www.gesetze-im-internet.de/krwg/__53.html · https://verwaltung.bund.de/leistungsverzeichnis/DE/leistung/99080103001000/

**Drittplattformen:** https://www.my-hammer.de/allgemeine-geschaefts-bedingungen · https://themen.kleinanzeigen.de/nutzungsbedingungen/ · https://themen.kleinanzeigen.de/gewerblich-handeln/

**Geo/Budget:** https://developers.google.com/maps/documentation/routes/usage-and-billing

**Wichtig:** Die Erwähnung externer Systeme ist keine bestätigte Partnerschaft, Lizenz oder Zugangsberechtigung. Die realen Datenrechte, Apps und operativen API-Fähigkeiten müssen separat geprüft werden.
