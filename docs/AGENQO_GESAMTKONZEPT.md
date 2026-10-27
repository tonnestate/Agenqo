# Agenqo – Produkt-, Geschäfts- und Umsetzungskonzept

**Version:** 2.0 · **Datum:** 27. Oktober 2026 · **Status:** Zielbild unverändert, Umsetzung hypothesengetrieben mit Gates. Alle wirtschaftlichen Werte sind Annahmen, bis der Pilot sie ersetzt.

---

## 0. Was sich gegenüber Version 1.0 ändert

| # | Änderung | Grund |
|---|----------|-------|
| 1 | Phasenreihenfolge umgedreht: erst **Concierge-Pilot mit 20 realen Fällen**, dann Plattformausbau | Nachfrage, Antwortquote und Provisionsakzeptanz sind unbewiesen; Golden Record, Claim-Prozess und Self-Service-Cockpit sind es, was am meisten Aufwand kostet |
| 2 | Golden Record im MVP nur als **schlanke Tabelle** (Firma, Kontakt, Einsatzgebiet, Status) | Evidence-Modell, Self-Assertions und Claim-Prüfung erst bauen, wenn Piloten zeigen, was gebraucht wird |
| 3 | **Provisionsgrundlage per Click-Wrap** beim Absenden des Angebots (Abschnitt 8) | v1 ließ offen, wann der Vermittlungsvertrag zustande kommt |
| 4 | **Anti-Umgehung** (Kontaktfreigabe erst nach Buchung, Nachprovision) | größtes Erlösrisiko, in v1 nur benannt |
| 5 | **Mindestprovision** und Pilot auf mittlere/große Aufträge (Wohnungsauflösung) | Bei 600 € Auftragswert bleiben nur 10,34 € Deckungsbeitrag (Abschnitt 11) |
| 6 | **Messbare Gate-Kriterien** mit Entscheidungsregel (Abschnitt 14) | v1 forderte eine Fortsetzungsentscheidung ohne Schwellen |
| 7 | Fachrecht Entrümpelung (Abfall) im Eignungsgate, nicht erst bei Schädlingsbekämpfung | Entsorgung ist Kernbestandteil des Angebots |
| 8 | **Doppelrolle Makler** und **P2B-Verordnung** ergänzt (Abschnitt 13) | in v1 nicht behandelt |
| 9 | Provider-MCP, Mandatsverhandlung, Kundengebühr, Kalender-Sync **hinter das Gate G1** verschoben | kein Entrümpler wartet 2026 auf einen Anbieteragenten |
| 10 | Konkretes **Datenmodell, Zustandsautomaten, Tech-Stack, Ticketliste** (Abschnitte 5–7, 15, Anhang B) | damit die Umsetzung sofort beginnen kann |

---

## 1. Executive Summary

Agenqo wird ein eigenständiger, KI-gestützter Dienstleistungsmarktplatz für Deutschland. Kunden beschreiben einen Bedarf, Agenqo holt strukturierte, vergleichbare Angebote geeigneter Anbieter ein, stellt den Gesamtpreis transparent gegenüber, ermöglicht eine begrenzte Nachverhandlung und bereitet die verbindliche Buchung vor. Anbieter müssen sich dafür weder registrieren noch einen Agenten betreiben: Sie antworten über einen personalisierten Quote-Link.

**Kundennutzen:** Ein Bedarf, mehrere verbindliche Angebote, ein ehrlicher Gesamtpreisvergleich.
**Anbieternutzen:** Qualifizierte, strukturierte Anfragen mit allen Angaben, ohne Leadgebühr; Gebühr nur bei Erfolg.
**Agenqo-Ertrag:** vertragliche Erfolgsprovision je durchgeführtem Auftrag; später Kunden-Service und Anbieter-Automatisierung.

**Marktstart:** ausschließlich Dienstleistungen, Pilotkategorie Haushalts-/Wohnungsauflösung und Entrümpelung, Pilotregion Metropolregion Hamburg (Radius ca. 50 km, siehe Entscheidung D1).

**Prinzip dieser Version:** Zuerst beweisen, dass der Kernkreislauf (Anfrage → Angebote → Buchung → Provision) mit echten Menschen funktioniert und Geld verdient. Erst dann Self-Service, Agenten-Schnittstellen und Skalierung.

---

## 2. Geschäftshypothesen und wie sie widerlegt werden

Alle Stärken von Agenqo sind bis zum Pilot **Hypothesen**. Ein Alleinstellungsmerkmal gegenüber CHECK24, MyHammer, Aroundhome oder neuen KI-Diensten wird nicht behauptet, sondern gemessen.

| ID | Hypothese | Messung im Pilot | Gate-Schwelle |
|----|-----------|------------------|---------------|
| H1 | Anbieter antworten auf strukturierte Quote-Links ohne Registrierung | Antwortquote eingeladener Anbieter binnen 48 h | ≥ 30 % |
| H2 | Anbieter akzeptieren eine Erfolgsprovision ohne Sonderverhandlung | Anteil antwortender Anbieter, die Click-Wrap akzeptieren | ≥ 70 % |
| H3 | Pro Vorgang entstehen vergleichbare, verbindliche Angebote | Vorgänge mit ≥ 2 bzw. ≥ 3 verbindlichen Angeboten | ≥ 2 in 80 %, ≥ 3 in 50 % |
| H4 | Kunden buchen über die Plattform | gebuchte / abgeschlossene Vorgänge | ≥ 25 % |
| H5 | Der Kreislauf ist wirtschaftlich | Deckungsbeitrag je gebuchtem Auftrag mit realen Kosten | > 0 € |
| H6 | Der Ablauf lässt sich automatisieren | manuelle Minuten je Vorgang | Ø ≤ 45 min ab Fall 11 |

---

## 3. Produktgrenzen und Unabhängigkeit

- Agenqo ist eine **eigene Produkt- und Betriebsdomäne**: eigener Code, eigene Datenbank, Authentifizierung, Deployment, Verträge und Abrechnung.
- **TonnEstate** ist Donor von Wissen und Schema-Vorlagen (Golden-Company-Modell), **keine Laufzeitabhängigkeit**. Datenübernahme nur nach Prüfung von Herkunft, Lizenz und Datenschutz (frühestens Phase 3).
- **n8n** ist austauschbare Prozessschicht (Mails, Fristen, Erinnerungen), kein System of Record für Aufträge, Geld oder Vollmachten.
- **LLMs** formulieren und strukturieren; Zustandsänderungen und Beträge entscheidet ausschließlich die deterministische Fachengine.
- Alle Kernfunktionen müssen **ohne externes LLM** bedienbar sein; KI verbessert Automatisierung, ersetzt keine Sicherheitsregeln.
- Kein Produktpreisvergleich im ersten Scope.

---

## 4. Rollen

| Rolle | MVP (Phase 1) | Später |
|-------|---------------|--------|
| **Kunde** (Privat, Unternehmen, Makler als Auftraggeber) | Intake-Formular, Magic-Link-Vorgangsseite ohne Konto | Konto, Cockpit, Buyer-MCP |
| **Anbieter** | Quote-Link pro Vorgang, kein Konto nötig | Registrierung, Claim, Cockpit, Team-/Agentenrechte, Provider-MCP |
| **Betreiber (Admin)** | Backoffice: Vorgänge anlegen, Anbieter einladen, Angebote vergleichen, Buchung begleiten | Qualitäts-/Dispute-/Compliance-Werkzeuge |
| **Externe Agenten** | nicht im MVP | Buyer-MCP (read + create_request), dann Provider-MCP |

---

## 5. Phasenplan

Zeitannahme: Umsetzung neben anderen Verpflichtungen, daher Kalenderwochen statt Stunden. Alle Zeiten sind Planwerte.

### Phase 0 – Entscheidungen, Recht, Zusagen (Woche 0–1)

- Entscheidungen D1–D10 (Abschnitt 17) treffen.
- Rechts-Quick-Check (Fragenliste in Abschnitt 13) beauftragen.
- Pilotanbieter ansprechen: **Soft-Commitments** von mindestens 8 Entrümpelungs-/Haushaltsauflösungsbetrieben in der Region.
- Nachfragequellen klären: mindestens 5 reale Fälle in Aussicht (Makleraufträge, Nachlass, Hausverwaltung, Notare, Privatkunden).
- Repo-Grundgerüst, Arbeitsname, Domain-Reservierung.

**Gate G0:** ≥ 8 Anbieter mit Bereitschaft, ≥ 5 Fälle in Aussicht, Rechts-Quick-Check ohne Showstopper. Sonst: Region/Kategorie/Ansprache anpassen, bevor Code entsteht.

### Phase 1a – Concierge-Kern (Woche 1–3)

Gebaut wird genau der Kreislauf, nicht mehr: Intake → Einladung → Quote-Link → Angebotserfassung → Vergleich → Kundenfreigabe → Anbieterbestätigung → Provisionsereignis. Details in Abschnitt 6 und 15.

### Phase 1b – 20 reale Vorgänge (Woche 3–8)

Mit menschlicher Begleitung, vollständiger Zeit- und Kostenerfassung. **Ausdrücklich keine** Kaltakquise in der Fläche, nur konkrete Kundenaufträge.

**Gate G1:** Entscheidung nach Abschnitt 14 (Weiter / Anpassen / Stoppen).

### Phase 2 – Plattformausbau (nach G1)

Anbieter-Registrierung und Claim-Prozess, Anbieter- und Kunden-Cockpit mit Konto, Rechnungsstellung der Provisionen, Kalender-Grundfunktionen, Bewertungen/Reklamationsprozess.

### Phase 3 – Datenbasis und zweite Region/Kategorie (nach G2)

Golden-Record-Ausbau (Evidence, Self-Assertions), geprüfter Datenimport, zweite Kategorie oder Region nur bei positivem Deckungsbeitrag.

### Phase 4 – Agenten-Schnittstellen

Buyer-MCP (suchen, Vorgang anlegen, Status lesen), danach Provider-MCP. Dieselben APIs wie das Webfrontend.

### Phase 5 – Skalierung und Zusatzerlöse

Mandatsverhandlung, Kundengebühr (Modell B), Premium-Automatisierung (Modell C), weitere Kategorien.

---

## 6. Concierge-MVP im Detail (Phase 1a)

### 6.1 Ablauf

1. **Intake:** Kunde füllt ein strukturiertes Webformular aus (Anhang A). Der Admin kann Vorgänge auch **im Auftrag** des Kunden anlegen (Telefon, Makleranfrage).
2. **Prüfung:** Admin prüft Vollständigkeit und Ausschlusskriterien (Asbestverdacht, Schadstoffsanierung → nicht im MVP, Verweis an Fachbetrieb).
3. **Auswahl:** System schlägt geeignete Anbieter vor (Einsatzgebiet, Kategorie, Qualifikationsstatus, Kontaktfähigkeit); Admin gibt frei. **Maximal 8 Einladungen je Vorgang.**
4. **Einladung:** n8n versendet je Anbieter eine E-Mail mit personalisiertem Quote-Link. Die Mail enthält die Leistungsbeschreibung **ohne** Name und genaue Adresse des Kunden.
5. **Angebot:** Anbieter akzeptiert die Vermittlungsbedingungen (Click-Wrap, Abschnitt 8) und gibt ein strukturiertes Angebot ab oder lehnt ab.
6. **Vergleich:** Admin und Kunde sehen eine Vergleichstabelle mit allen Preisbestandteilen und Vergleichbarkeitsstatus.
7. **Best and Final (optional):** Die engeren Anbieter erhalten eine Aufforderung, bis zu einer Frist ein finales Angebot abzugeben (Abschnitt 10).
8. **Freigabe:** Kunde wählt über seinen Magic-Link ein verbindliches Angebot und gibt es frei. Gespeichert wird der Fingerprint des exakten Angebotsstands.
9. **Bestätigung:** Anbieter bestätigt die Buchung über seinen Quote-Link. Erst jetzt werden Kunden-Name und genaue Adresse freigegeben.
10. **Abschluss:** Nach Durchführung bestätigt der Kunde (oder automatisch 7 Tage nach Termin ohne Widerspruch). Das Provisionsereignis entsteht.

### 6.2 Was bewusst manuell bleibt

Anbieterfreigabe, Plausibilitätsprüfung der Angebote, Rückfragenklärung, Eskalationen, Reklamationen, Rechnungsstellung der Provision. Jede manuelle Handlung wird mit Dauer erfasst (Kennzahl H6).

### 6.3 Was automatisiert wird

Einladungsversand, Erinnerung (max. 1), Fristüberwachung, Statusbenachrichtigungen, Angebotsvalidierung (Pflichtpositionen, Summen, Steuer), Fingerprint, Audit-Log.

---

## 7. Pilot: Kategorie, Region, Nachfrage

**Kategorie:** Haushalts-/Wohnungsauflösung und Entrümpelung. Auftragswerte sind höher als bei reiner Kleinentrümpelung (typisch mehrere hundert bis einige tausend Euro, Annahme), der Intake ist strukturierbar, die Nachfrage wiederkehrend (Nachlass, Verkauf, Auszug).

**Region:** Metropolregion Hamburg (Radius ca. 50 km). Begründung: hohe Anbieterdichte, kurze Wege für Besichtigungen und Pilotbegleitung.

**Nachfrage-Seeds** (nach Priorität):
1. Aufträge aus dem Immobilienumfeld (Verkauf, Nachlass, Räumung vor Übergabe), unter Beachtung der Doppelrollen-Regeln (Abschnitt 13).
2. Nachlassverwalter, Notare, Hausverwaltungen als wiederkehrende B2B-Auftraggeber.
3. Privatkunden über Landingpage (SEO ab Phase 1b parallel).

**Ausschlüsse im MVP:** Schadstoff-/Asbestsanierung, Schimmelsanierung, Messie-Fälle mit Hygienerisiko ohne Besichtigung. Diese Vorgänge werden an Fachbetriebe verwiesen.

**Eignungsgate Anbieter (hart):** gültiges Gewerbe, Einsatzgebiet deckt PLZ ab, belastbare Identität, nachweisbare Entsorgungs-/Beförderungsberechtigung für anfallende Abfallarten (konkrete Nachweise nach Rechts-Quick-Check festlegen), Haftpflichtversicherung (Nachweis erfragen).

---

## 8. Quote-Link, Vermittlungsbedingungen und Provisionsmechanik

### 8.1 Quote-Link (technische Spezifikation)

- Token: 32 zufällige Bytes (`secrets.token_urlsafe(32)`), **nur der SHA-256-Hash wird gespeichert**.
- Gebunden an genau **einen Vorgang und eine Firma** (Tabelle `invitations`), standardmäßig 7 Tage gültig (Annahme).
- Serverseitige Autorisierung bei jedem Aufruf; Rate-Limit je Token und IP.
- Medien (Fotos) nur über kurzlebige signierte URLs (15 Minuten).
- Jede Angebotsänderung erzeugt eine **Revision** mit neuer Nummer; der Vorgänger wird `ersetzt`, nie überschrieben.
- Jede Mail enthält einen **Abmeldelink**; Abmeldung setzt `company_contacts.suppressed_at` und blockiert weitere Einladungen.

### 8.2 Click-Wrap Vermittlungsbedingungen

Beim Absenden des ersten Angebots akzeptiert der Anbieter versionierte Bedingungen (`terms_versions`, `terms_acceptances` mit Zeitpunkt, Name, E-Mail, gehashter IP). Eckpunkte als **Verhandlungsbasis für die anwaltliche Prüfung**:

1. **Provision:** Satz und Mindestbetrag (Pilotstandard: 8 % des Netto-Leistungswerts, mindestens 40 € netto, Annahme).
2. **Bemessungsgrundlage:** vereinbarter Netto-Auftragswert laut freigegebenem Angebot, ohne Umsatzsteuer; bei Kleinunternehmern der Rechnungsbetrag.
3. **Fälligkeit:** Provisionsereignis entsteht mit Abschluss (Durchführung bestätigt oder 7 Tage nach Termin ohne Widerspruch). Bei Storno vor Durchführung keine Provision.
4. **Folgeaufträge:** Aufträge mit demselben Kunden für denselben Gegenstand innerhalb einer festzulegenden Frist (Vorschlag: 12 Monate) sind provisionspflichtig.
5. **Umgehungsschutz:** Kontaktdaten des Kunden werden erst nach Buchungsfreigabe offengelegt; bei nachgewiesener Umgehung pauschalierter Schadensersatz (Ausgestaltung und AGB-Kontrolle auch im B2B-Verkehr anwaltlich prüfen).
6. **Ranking-Transparenz:** Provision beeinflusst das Ranking nicht; Anbieter stimmen einem anonymisierten Rangsignal im Best-and-Final-Verfahren zu.
7. **Preisbindung:** Ein als „verbindlich bis“ markiertes Angebot bindet den Anbieter bis zum angegebenen Zeitpunkt.
8. **Datenverwendung:** Zweck, Speicherdauer, Betroffenenrechte.

### 8.3 Provisionsberechnung

`provision_netto = max(mindest_cent, round_half_up(netto_cent × satz / 100))` – in ganzen Cent mit `Decimal`, nie mit Fließkomma.

---

## 9. Angebot, Gesamtpreis und Vergleichbarkeit

### 9.1 Angebotszustände

`unvollstaendig` → `indikativ` | `besichtigung_erforderlich` | `verbindlich` → `angenommen` | `abgelehnt` | `abgelaufen` | `zurueckgezogen` | `ersetzt`

Ein Fotoupload erzeugt **keinen** rechtlich garantierten Festpreis. Ein verbindliches Angebot entsteht nur, wenn der Anbieter es ausdrücklich so markiert und eine Gültigkeit setzt.

### 9.2 Pflichtpositionen Entrümpelung

Arbeitsleistung, Entsorgung inklusive Gebühren, Anfahrt, Halteverbot/Parkgenehmigung (falls nötig), Besenreinigung (falls Teil des Umfangs), Verwertungsgutschrift (negativ), Zuschläge (Etage, Sondermüll), Umsatzsteuer, **Bruttogesamtpreis**. Fehlt eine Pflichtposition, bleibt das Angebot `unvollstaendig`.

### 9.3 Vergleichbarkeit

Das System kennzeichnet je Angebot: **voll vergleichbar** (gleicher Umfang, alle Pflichtpositionen), **teilweise vergleichbar** (abweichender Umfang oder Vorbehalte, werden angezeigt) oder **nicht vergleichbar** (nur indikativ). Es gibt im MVP **keine** künstliche Gesamtpunktzahl. Sortierung nach der vom Kunden gewählten Priorität (Preis, Termin, Vertrauen, Gesamtwert).

### 9.4 Fingerprint

SHA-256 über kanonisches JSON (sortierte Schlüssel, UTF-8) aus Angebots-ID, Revision, Positionen, Summen, Steuersatz, Gültigkeit, Leistungsbeschreibung und Vorbehalten. Die Kundenfreigabe speichert diesen Wert. Eine Buchung ist nur zulässig, wenn Angebotsstatus `verbindlich`, Fingerprint identisch und `jetzt < gültig_bis`.

---

## 10. Verhandlung (MVP und später)

**MVP:** Genau eine optionale Runde **Best and Final**. Die zwei bis drei besten Anbieter erhalten die Aufforderung, bis zu einer Frist ein finales Angebot abzugeben. Preise anderer Anbieter werden nicht offengelegt; ein anonymisiertes, wahrheitsgemäßes Rangsignal („im oberen Preisdrittel“) ist zulässig, sofern in den Bedingungen vereinbart.

**Später (Phase 5):** Mandatsgebundene KI-Verhandlung mit Ziel- und Höchstpreis, erlaubten Zugeständnissen und Freigaberegeln. Die Engine verhindert Zusagen außerhalb des Mandats; Anbieteragenten handeln nur im Rahmen einer vom Betrieb erteilten Kompetenz.

---

## 11. Erlösmodell und Unit Economics

### 11.1 Erlöspfade

- **A – Erfolgsprovision der Anbieter** (Pilot): Satz und Mindestbetrag laut Abschnitt 8. Keine Provision für bloß bekannte Firmen ohne akzeptierte Bedingungen.
- **B – Servicegebühr für Kunden** (erst nach G1 testen): vorab transparent vereinbart, ausdrücklich autorisiert, keine Gebühr auf „Ersparnis“ ohne belastbaren Nachweis.
- **C – Anbieter-Automatisierung** (Phase 5): bezahlt wird messbarer Nutzen (Kalender, CRM/ERP, Regelautomatik), nicht „MCP“.

**Pilot:** Kunden zahlen nichts. Die Provision wird **ab dem ersten Fall** vertraglich vereinbart, damit H2 und H5 echte Zahlungsbereitschaft messen (Voraussetzung: Rechtsträger steht, siehe D3).

### 11.2 Rechenszenarien (Annahmen, nachgerechnet)

Provision 8 %, Mindestprovision 40 € netto, Umsatzsteuer 19 %. Variable Kosten je gebuchtem Auftrag (KI, Kommunikation, Support, anteilige Akquise) als Annahme gestaffelt.

| Szenario | Brutto | Netto | Provision | Variable Kosten | Deckungsbeitrag |
|----------|-------:|------:|----------:|----------------:|----------------:|
| klein | 600 € | 504,20 € | 40,34 € | 30 € | **10,34 €** |
| mittel | 1.500 € | 1.260,50 € | 100,84 € | 45 € | **55,84 €** |
| groß | 3.000 € | 2.521,01 € | 201,68 € | 60 € | **141,68 €** |

**Break-even-Aufträge pro Monat** bei 1.500 € monatlichen Fixkosten (Annahme): klein ≈ 145, mittel ≈ 27, groß ≈ 11.
Schlussfolgerung: Das Modell trägt erst bei mittleren und großen Aufträgen. Der Pilot zielt deshalb auf Wohnungs-/Haushaltsauflösung und Makler-/Nachlassaufträge.

### 11.3 Kernformel

`Deckungsbeitrag je Auftrag = realisierte Netto-Plattformerträge − variable KI-, Kommunikations-, Payment-, Support-, Reklamations- und Akquisitionskosten`

Im Pilot wird der Concierge-Aufwand **getrennt** ausgewiesen (Minuten × interner Satz), damit sichtbar ist, was Automatisierung bringen muss.

---

## 12. Golden Company Record

### 12.1 MVP-Scheibe (Phase 1)

Tabellen `companies`, `company_contacts`, `company_service_areas` (Anhang B). Statuskette: `identifiziert` → `qualifiziert` → `antwortaktiv` → `registriert` → `vertraglich`. Recherchierte Firmen dürfen **nie** als verifizierte Partner erscheinen. Jeder Kontakt führt Herkunft und Beobachtungszeitpunkt.

### 12.2 Ausbau (Phase 3)

SourceObservation/Claim mit Konfliktstatus und Lizenz, VerificationEvidence, ProfileOwnershipClaim, AgentDelegation. Eigene Angaben des Anbieters werden als **Self-Assertion** mit Urheber, Zeit und Beleg gespeichert; amtlich oder drittseitig belegte Daten werden nie stillschweigend überschrieben. Kritische Änderungen (Identität, Zahlungsanschluss, Verträge, Agentenrechte) erfordern erhöhte Prüfung.

### 12.3 Qualitätsmessung

Keine Behauptung „wir kennen alle Anbieter“. Gemessen wird je Kategorie und Region getrennt: Identifizierung, Kontaktfähigkeit, Qualifikation, Antwort, Vertrag.

---

## 13. Recht, Compliance, Doppelrolle

Konzeptanforderungen, **keine Rechtsberatung**. Vor Phase 1b wird ein **Rechts-Quick-Check** durch eine Kanzlei für IT-/Wettbewerbsrecht durchgeführt mit folgenden Fragen:

1. **UWG § 7:** Zulässigkeit der Einladung von Anbietern per E-Mail zu einem konkreten Kundenauftrag (B2B, mutmaßliche Einwilligung), inkl. Abmeldeverfahren und Häufigkeitsgrenzen.
2. **Click-Wrap/AGB:** Wirksamkeit der Provisions-, Nachprovisions- und Umgehungsklauseln im B2B-Verkehr (§§ 305 ff. BGB), Gestaltung des pauschalierten Schadensersatzes.
3. **Vertragsstruktur:** Wer ist Vertragspartner des Kunden? Vermittler vs. Auftragnehmer, Haftung, Gewährleistung, Widerrufsrecht bei Verbrauchern.
4. **DSGVO:** Weitergabe von Kundendaten erst nach Freigabe, Foto-/Adressverarbeitung, Auftragsverarbeitung (E-Mail-Dienst, Hosting, LLM), Löschfristen (Vorschlag: Medien 90 Tage nach Abschluss).
5. **Transparenz/Ranking:** § 5b UWG, PAngV, **P2B-Verordnung (EU) 2019/1150** (Anwendbarkeit als Online-Vermittlungsdienst gegenüber gewerblichen Anbietern prüfen), DSA je nach Rolle.
6. **KI-Offenlegung:** erkennbar machen, wann KI kommuniziert; AI-Act-Pflichten prüfen.
7. **Fachrecht Abfall:** Anforderungen an Beförderung/Entsorgung (Anzeige-/Erlaubnispflichten, Nachweisführung) und welche Nachweise der Eignungsgate verlangen muss.
8. **Doppelrolle Makler:** Agenqo vermittelt Dienstleister auch für Aufträge aus der Immobilientätigkeit des Gründers. Zu klären: Interessenkonflikt, Offenlegung gegenüber dem Auftraggeber, Zulässigkeit von Provisionen Dritter. **Empfehlung:** Agenqo wird von der Maklertätigkeit rechtlich und buchhalterisch getrennt; kein Provisionsfluss an die Maklerperson; Offenlegung in der Auftragsbestätigung.
9. **Rechtsträger und Nebentätigkeit:** Gründungszeitpunkt, Haftungsstruktur, etwaige Genehmigungs-/Anzeigepflichten aus bestehenden Beschäftigungsverhältnissen.

**Zahlungen:** Kundengeld bleibt beim Dienstleister bzw. lizenzierten Zahlungsdienstleister; Agenqo rechnet **nur seine Provision** per Rechnung ab. Keine eigene Zahlungsabwicklung ohne regulatorische Prüfung.

**Quellenrechte:** Firmendaten, Fotos und Fremdintegrationen nur im erlaubten Umfang.

---

## 14. Gate G1: Fortsetzungsentscheidung

Messung über mindestens **20 reale** Vorgänge (echter Bedarf, keine Testfälle), erfasst über `audit_events` und Zeitprotokoll.

**Muss-Kriterien**

| Kriterium | Schwelle |
|-----------|----------|
| Antwortquote eingeladener Anbieter binnen 48 h | ≥ 30 % |
| Vorgänge mit ≥ 2 verbindlichen Angeboten | ≥ 80 % |
| Vorgänge mit ≥ 3 verbindlichen Angeboten | ≥ 50 % |
| Abschlussquote (gebucht / Vorgänge) | ≥ 25 % |
| Click-Wrap-Akzeptanz ohne Sonderverhandlung | ≥ 70 % |
| Deckungsbeitrag je gebuchtem Auftrag (ohne Concierge-Zeit) | > 0 € |

**Soll-Kriterien**

| Kriterium | Schwelle |
|-----------|----------|
| Median Zeit bis erstes verbindliches Angebot | ≤ 48 h |
| Manuelle Minuten je Vorgang ab Fall 11 | Ø ≤ 45 min |
| Reklamationsquote | ≤ 10 % |
| Kundenzufriedenheit (eine Frage, positiv) | ≥ 80 % |

**Entscheidungsregel** (Schwellen als Vorschlag, in Phase 0 bestätigen):

- Alle Muss-Kriterien erfüllt → **Phase 2**.
- Genau ein Muss-Kriterium verfehlt → **ein** Anpassungszyklus von 4 Wochen (Preismodell, Ansprache, Region oder Angebotsformular), dann erneute Messung über 10 Vorgänge.
- Zwei oder mehr verfehlt oder Wiederholung verfehlt → **Pause oder Archivierung**; Erkenntnisse dokumentieren.

---

## 15. Architektur und Tech-Stack (Entscheidungsvorschlag)

### 15.1 Stack

| Schicht | Vorschlag | Begründung |
|---------|-----------|------------|
| Backend | Python 3.12, **FastAPI**, SQLAlchemy 2, Alembic | eigene Python-Stärke, saubere Domänenlogik, gute Testbarkeit |
| Datenbank | **PostgreSQL 16** | JSONB, Constraints, Row-Level-Security später für Mandantentrennung; Alternative MariaDB möglich |
| Frontend | server-gerendert mit **Jinja2 + HTMX**, schlichtes CSS | ein Deployment, kein SPA-Aufwand, schnell, SEO-fähig für Landingpages |
| Prozessschicht | **n8n** (self-hosted) hinter signierten, idempotenten Endpunkten | wie in v1 |
| Mail | EU-Anbieter oder eigener SMTP, Auftragsverarbeitung nötig | Zustellbarkeit, DSGVO |
| LLM | **Claude API** (Produktivflows), strukturierte Ausgaben | nur Intake-Normalisierung und Angebots-Parsing-Fallback; Vision in Phase 1 aus |
| Hosting | Rechenzentrum in Deutschland, Docker Compose, Reverse Proxy mit TLS, tägliches Backup | DSGVO, einfach |
| Storage | S3-kompatibel oder lokales Volume mit Verschlüsselung | Fotos mit Löschfrist |

### 15.2 Repo-Struktur

```
agenqo/
  app/
    main.py
    config.py
    db.py
    models/            # SQLAlchemy-Modelle
    domain/            # reine Funktionen: Zustandsautomaten, Preis, Fingerprint, Provision, Tokens
    api/               # Router: public, quote_link, customer_link, admin, internal (n8n)
    templates/         # Jinja2
    static/
  migrations/          # Alembic
  tests/               # pytest; domain/ zu 100 % Zeilenabdeckung
  n8n/                 # exportierte Workflows (JSON)
  docs/
  docker-compose.yml
```

### 15.3 Verantwortlichkeiten

- **Fachengine (`domain/`):** einzige Quelle für Zustandsübergänge, Beträge, Fingerprints, Provision.
- **Golden Record:** einzige Quelle für veröffentlichte Firmenidentität und Quellenkonflikte.
- **n8n:** keine eigene Buchungs-/Provisionsentscheidung; Ereignisse kommen über die **Outbox** (`outbox_events`), Rückmeldungen über signierte HMAC-Endpunkte mit `Idempotency-Key`.
- **LLM:** Vorschläge und Texte innerhalb enger Schemas, keine Rechtsfolgen.
- **Backoffice:** manuelle Freigabe, Konfliktbehandlung, Betrugsprävention.

### 15.4 Sicherheits-Mindeststandard

TLS überall, Secrets nur über Umgebung/Secret-Store, Passwort-Hashing mit Argon2 und TOTP für Admins, Audit-Log für jede Zustandsänderung, Eingabevalidierung (Pydantic), Upload-Prüfung (Typ, Größe, Malware-Scan), Prompt-Injection-Schutz bei jedem LLM-Aufruf (Kundentext und Anbieterantworten sind Daten, keine Anweisungen), Tests für Autorisierung (Anbieter A sieht nie Daten von Anbieter B oder fremden Vorgängen).

---

## 16. Zustandsautomaten (verbindlich)

Übergänge, die nicht aufgeführt sind, sind verboten und werden von der Engine mit Fehler abgelehnt.

### 16.1 Vorgang (`service_requests.status`)

| Von | Nach | Auslöser |
|-----|------|----------|
| `entwurf` | `offen` | Admin gibt frei, Einladungen erzeugt |
| `offen` | `vergleich` | erstes Angebot im Status `verbindlich` oder `indikativ` eingegangen |
| `offen` | `abgelaufen` | Frist ohne Angebot |
| `vergleich` | `freigabe` | Kunde gibt ein verbindliches Angebot frei |
| `vergleich` | `abgelaufen` | alle Angebote abgelaufen/abgelehnt |
| `freigabe` | `gebucht` | Anbieter bestätigt Buchung |
| `freigabe` | `vergleich` | Anbieter lehnt Bestätigung ab oder Angebot läuft ab |
| `gebucht` | `abgeschlossen` | Durchführung bestätigt |
| `gebucht` | `storniert` | Storno vor Durchführung |
| `gebucht` / `abgeschlossen` | `streitfall` | Reklamation oder Dispute eröffnet |
| `entwurf` / `offen` / `vergleich` | `storniert` | Kunde oder Admin bricht ab |

### 16.2 Einladung (`invitations.status`)

`geplant` → `gesendet` → `geoeffnet` → `beantwortet` | `abgelehnt`; aus `gesendet`/`geoeffnet` → `abgelaufen`; aus `geplant`/`gesendet` → `bounce`.

### 16.3 Angebot (`quotes.status`)

`indikativ` | `besichtigung_erforderlich` | `verbindlich` (Startzustände nach Validierung);
`verbindlich` → `angenommen` | `abgelaufen` | `zurueckgezogen` | `ersetzt`;
`indikativ` / `besichtigung_erforderlich` → `verbindlich` (neue Revision) | `abgelehnt` | `ersetzt`.

### 16.4 Buchung (`bookings.status`)

`angefragt` → `bestaetigt` → `durchgefuehrt`; `angefragt` | `bestaetigt` → `storniert`; `bestaetigt` | `durchgefuehrt` → `streitfall`.

### 16.5 Provisionsereignis (`commission_events.status`)

`entstanden` → `gestellt` → `bezahlt`; `entstanden` | `gestellt` → `erlassen` | `storniert`.

---

## 17. Entscheidungen mit Standardvorschlag

Damit die Umsetzung nicht an offenen Fragen hängt, gilt der **Standard**, solange nichts anderes entschieden ist.

| ID | Frage | Standardvorschlag |
|----|-------|-------------------|
| D1 | Pilotregion | Metropolregion Hamburg, Radius ca. 50 km |
| D2 | Pilotkategorie | Haushalts-/Wohnungsauflösung inkl. Entrümpelung |
| D3 | Rechtsträger | Eigene Gesellschaft oder eigener Geschäftsbereich einer zu gründenden Gesellschaft, vor dem ersten **bezahlten** Fall klären (Steuerberater); bis dahin Vorbereitung ohne Provisionsvereinbarung |
| D4 | Provision | 8 % netto, Mindestprovision 40 € netto, Fälligkeit bei Durchführung |
| D5 | Kundengebühr | 0 € im Pilot |
| D6 | Tech-Stack | Abschnitt 15.1 |
| D7 | Marke/Domain | Pilot unter Arbeitsname; vor öffentlichem Launch Recherche DPMA/EUIPO und Domain |
| D8 | LLM-Einsatz Phase 1 | nur Intake-Normalisierung und Angebots-Parsing-Fallback, Vision aus |
| D9 | Datenhaltung | Rechenzentrum in Deutschland |
| D10 | TonnEstate-Reuse | nur Schema-Vorlage; Datenimport frühestens Phase 3 nach Lizenz-/Datenschutzprüfung |

---

## 18. Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|--------|---------------|
| Niedrige Antwortquote | Quote-Link ohne Registrierung, nur konkrete Kundenaufträge, vorab Soft-Commitments (G0), Erinnerung nach 24 h |
| Zu geringe Marge | Mindestprovision, Fokus auf mittlere/große Aufträge, Aufwandsmessung |
| Anbieterumgehung | Kontaktfreigabe erst nach Buchung, Nachprovision, Bedingungen anwaltlich geprüft |
| Rechtliche Einwände gegen Ansprache | Rechts-Quick-Check, Abmeldelink, Häufigkeitsgrenze, keine Massenansprache |
| Schlechte Anbieterqualität | harter Eignungsgate, Bewertung nach Abschluss, Sperrliste |
| Datenqualität Golden Record | Quelle und Zeitpunkt je Kontakt, Aktualitätsprüfung vor Einladung |
| Unklare Preisverbindlichkeit | Zustandsmodell, Pflichtpositionen, Fingerprint |
| Einzelperson als Engpass | enger MVP-Umfang, Automatisierung nach G1, klare Abbruchkriterien |
| Distributionsabhängigkeit von Assistenten | Web und Quote-Link zuerst; MCP ist Zusatzkanal ohne Aufnahmegarantie |

---

## 19. Nicht-Ist-Liste (Stand 27.10.2026)

- Kein laufender Agenqo-Marktplatz.
- Keine bestätigte Übernahme des TonnEstate-Golden-Company-Datenbestands.
- Keine bestätigten Anbieterpartner und keine unterschriebenen Provisionsverträge.
- Kein produktiver Buyer-/Provider-MCP.
- Keine automatisierte deutschlandweite Anbieteransprache, keine KI-Verhandlung.
- Keine gesicherten Umsätze, Conversion Rates oder Marktführerschaft.
- Kein Produktpreisvergleich.

---

## 20. Umsetzungsstart: Tickets für Phase 1a

Jedes Ticket gilt erst als erledigt, wenn **Tests grün** sind und die Akzeptanzkriterien erfüllt sind (Definition of Done: Migration vorhanden, Unit-/Integrationstest, Audit-Eintrag, keine ungeprüften Platzhalter).

| # | Ticket | Akzeptanzkriterium |
|---|--------|--------------------|
| T1 | Repo-Gerüst, Docker Compose (App, Postgres, n8n, Proxy), CI mit pytest | `docker compose up` startet; Health-Endpunkt antwortet; CI grün |
| T2 | Datenmodell und Alembic-Migration (Anhang B) | Migration läuft vorwärts und rückwärts auf leerer DB |
| T3 | `domain/`: Zustandsautomaten (Abschnitt 16) | Tests: jeder erlaubte Übergang ok, jeder andere abgelehnt |
| T4 | `domain/`: Preis, Steuer, Provision, Fingerprint, Token | Tests mit den Rechenfällen aus Abschnitt 11.2; Rundung in Cent; Hash reproduzierbar |
| T5 | Intake-Formular (Anhang A) und Admin-Erfassung im Auftrag | Pflichtfelder validiert; Ausschlussfälle werden markiert |
| T6 | Backoffice: Firmenverwaltung, Anbieterauswahl, Einladungsfreigabe (max. 8) | Auswahl nach PLZ/Kategorie/Status; Audit-Log |
| T7 | Outbox + n8n-Flow F1 „Einladung versenden“ | Mail enthält Quote-Link; erneuter Aufruf erzeugt keine Doppelmail (Idempotenz) |
| T8 | Quote-Link-Seite mit Click-Wrap und Angebotsformular | Token-Hash-Prüfung, Ablauf, Revision statt Überschreiben, Pflichtpositionen |
| T9 | Vergleichsansicht (Admin und Kunden-Magic-Link) | Gesamtpreis brutto, Vergleichbarkeitsbadge, Sortierung nach Priorität |
| T10 | Best-and-Final-Runde | Nur Top 2–3; keine Preise anderer Anbieter sichtbar |
| T11 | Kundenfreigabe mit Fingerprint und Anbieterbestätigung | Buchung nur bei `verbindlich`, gleichem Fingerprint und gültiger Frist; Kontaktfreigabe erst danach |
| T12 | Abschluss, Storno, Provisionsereignis, CSV-Export | Provision korrekt gerundet; Storno vor Durchführung erzeugt keine Provision |
| T13 | n8n-Flows F2 Erinnerung, F3 Eskalation, F4 Kundenbenachrichtigung | Max. 1 Erinnerung; Alarm an Admin nach 48 h ohne verbindliches Angebot |
| T14 | Kennzahlen-Ansicht (Abschnitt 14) und Zeiterfassung manueller Schritte | alle Gate-Kennzahlen aus der DB berechenbar |
| T15 | Autorisierungs- und Sicherheitstests | Anbieter A kann weder Angebote von B noch fremde Vorgänge abrufen |

Empfohlene Reihenfolge: **T1 → T2 → T3 → T4** (Fundament mit Tests) → **T5 → T6 → T8 → T7** (Daten rein, Anbieter antworten) → **T9 → T11 → T12** (Entscheidung und Geld) → **T10, T13, T14, T15**.

---

## 21. MVP-Abnahme (zweistufig)

**Stufe 1 – technische Abnahme (Ende Phase 1a):** Ein vollständiger Testvorgang läuft von Intake über zwei Anbieterangebote, Vergleich, Freigabe, Bestätigung bis zum Provisionsereignis; alle Tests aus T3, T4 und T15 sind grün; ein zweiter, simulierter Anbieter kann keine Daten des ersten sehen.

**Stufe 2 – Marktabnahme (Gate G1):** Kriterien aus Abschnitt 14 über 20 reale Vorgänge. Die Plattform läuft **ohne TonnEstate-Laufzeit**.

---

## Anhang A – Intake Entrümpelung / Haushaltsauflösung

**Pflichtfelder:** Objektart (Wohnung, Haus, Keller, Dachboden, Garage, Gewerbe); PLZ und Ort; Etage; Aufzug ja/nein; Zugang und Parksituation (Tragewege, Halteverbot nötig); Größe (Zimmer oder m²); Füllgrad in vier Stufen (leer, normal, stark gefüllt, extrem gefüllt); Wunschzeitraum und Flexibilität; Besichtigung vor Ort möglich ja/nein; mindestens drei Fotos (empfohlen, bei „extrem gefüllt“ Pflicht); Berechtigung (Eigentümer, Erbe, Verwalter, Mieter) mit Hinweis auf Vollmacht bei Nachlass; Kontaktangaben.

**Optionale Felder:** geschätztes Volumen in Kubikmetern; Sperrmüll/Elektrogeräte/Kühlgeräte; Verwertung gewünscht (Ankauf wertvoller Gegenstände); Besenreinigung; Demontage (Küche, Einbauten); Anlass (Nachlass, Verkauf, Auszug, Übergabe).

**Ausschlussmarker:** Asbestverdacht, Schimmel, Schadstoffe, Hygienerisiko, Gefahrstoffe in größerer Menge → Vorgang wird markiert und nicht eingeladen; Verweis an Fachbetrieb.

**Datenschutz im Einladungstext:** Der Anbieter erhält PLZ, Ort, Etage, Aufzug, Füllgrad, Volumen, Besonderheiten, Fotos (signierte URLs) und Zeitraum. Name und genaue Adresse erst nach Buchungsfreigabe.

---

## Anhang B – Datenmodell-Entwurf (PostgreSQL 16)

Beträge immer in ganzen Cent (`integer`). Alle Zeitstempel `timestamptz`. Dies ist die Vorlage für die erste Alembic-Migration (T2).

```sql
CREATE TABLE companies (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    legal_name    text NOT NULL,
    display_name  text,
    website       text,
    status        text NOT NULL DEFAULT 'identifiziert'
                  CHECK (status IN ('identifiziert','qualifiziert','antwortaktiv','registriert','vertraglich')),
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE company_contacts (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id     uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    kind           text NOT NULL CHECK (kind IN ('email','phone','form')),
    value          text NOT NULL,
    is_preferred   boolean NOT NULL DEFAULT false,
    source         text NOT NULL,
    observed_at    timestamptz NOT NULL DEFAULT now(),
    suppressed_at  timestamptz
);

CREATE TABLE company_service_areas (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id   uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    category     text NOT NULL,
    center_plz   text NOT NULL CHECK (center_plz ~ '^[0-9]{5}$'),
    radius_km    integer NOT NULL CHECK (radius_km BETWEEN 1 AND 300)
);

CREATE TABLE terms_versions (
    version        text PRIMARY KEY,
    rate_percent   numeric(5,2) NOT NULL CHECK (rate_percent >= 0 AND rate_percent <= 100),
    min_cents      integer NOT NULL CHECK (min_cents >= 0),
    text_md        text NOT NULL,
    published_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE service_requests (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    public_ref          text NOT NULL UNIQUE,
    customer_name       text NOT NULL,
    customer_email      text NOT NULL,
    customer_phone      text,
    category            text NOT NULL,
    postal_code         text NOT NULL CHECK (postal_code ~ '^[0-9]{5}$'),
    city                text,
    requirements        jsonb NOT NULL DEFAULT '{}'::jsonb,
    window_start        date,
    window_end          date,
    priority            text NOT NULL DEFAULT 'gesamtwert'
                        CHECK (priority IN ('preis','termin','vertrauen','gesamtwert')),
    status              text NOT NULL DEFAULT 'entwurf'
                        CHECK (status IN ('entwurf','offen','vergleich','freigabe','gebucht',
                                          'abgeschlossen','storniert','abgelaufen','streitfall')),
    exclusion_flag      boolean NOT NULL DEFAULT false,
    created_by          text NOT NULL DEFAULT 'kunde' CHECK (created_by IN ('kunde','admin')),
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    closed_at           timestamptz
);

CREATE TABLE request_media (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id    uuid NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
    storage_key   text NOT NULL,
    content_type  text NOT NULL,
    size_bytes    integer NOT NULL CHECK (size_bytes > 0),
    delete_after  date,
    created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE invitations (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id    uuid NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
    company_id    uuid NOT NULL REFERENCES companies(id),
    channel       text NOT NULL DEFAULT 'email' CHECK (channel IN ('email','portal','api')),
    token_hash    text NOT NULL UNIQUE,
    expires_at    timestamptz NOT NULL,
    status        text NOT NULL DEFAULT 'geplant'
                  CHECK (status IN ('geplant','gesendet','geoeffnet','beantwortet',
                                    'abgelehnt','abgelaufen','bounce')),
    sent_at       timestamptz,
    opened_at     timestamptz,
    responded_at  timestamptz,
    UNIQUE (request_id, company_id)
);

CREATE TABLE terms_acceptances (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id          uuid NOT NULL REFERENCES companies(id),
    invitation_id       uuid NOT NULL REFERENCES invitations(id),
    terms_version       text NOT NULL REFERENCES terms_versions(version),
    accepted_at         timestamptz NOT NULL DEFAULT now(),
    accepted_by_name    text NOT NULL,
    accepted_by_email   text NOT NULL,
    ip_hash             text,
    user_agent          text
);

CREATE TABLE quotes (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id          uuid NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
    company_id          uuid NOT NULL REFERENCES companies(id),
    invitation_id       uuid NOT NULL REFERENCES invitations(id),
    revision            integer NOT NULL DEFAULT 1 CHECK (revision >= 1),
    status              text NOT NULL
                        CHECK (status IN ('unvollstaendig','indikativ','besichtigung_erforderlich',
                                          'verbindlich','angenommen','abgelehnt','abgelaufen',
                                          'zurueckgezogen','ersetzt')),
    vat_rate            numeric(4,2) NOT NULL DEFAULT 19.00 CHECK (vat_rate >= 0),
    total_net_cents     integer CHECK (total_net_cents >= 0),
    total_gross_cents   integer CHECK (total_gross_cents >= 0),
    valid_until         timestamptz,
    earliest_date       date,
    scope_text          text,
    reservations        text,
    comparability       text CHECK (comparability IN ('voll','teilweise','nicht')),
    fingerprint         text,
    supersedes_id       uuid REFERENCES quotes(id),
    created_at          timestamptz NOT NULL DEFAULT now(),
    UNIQUE (request_id, company_id, revision)
);

CREATE TABLE quote_items (
    id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id          uuid NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    position          integer NOT NULL CHECK (position >= 1),
    kind              text NOT NULL
                      CHECK (kind IN ('arbeit','entsorgung','anfahrt','halteverbot','reinigung',
                                      'zuschlag','verwertung','rabatt','sonstiges')),
    description       text NOT NULL,
    amount_net_cents  integer NOT NULL,
    is_mandatory      boolean NOT NULL DEFAULT true,
    UNIQUE (quote_id, position)
);

CREATE TABLE bookings (
    id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id             uuid NOT NULL UNIQUE REFERENCES service_requests(id),
    quote_id               uuid NOT NULL UNIQUE REFERENCES quotes(id),
    status                 text NOT NULL DEFAULT 'angefragt'
                           CHECK (status IN ('angefragt','bestaetigt','durchgefuehrt','storniert','streitfall')),
    customer_approved_at   timestamptz NOT NULL,
    approved_fingerprint   text NOT NULL,
    provider_confirmed_at  timestamptz,
    scheduled_start        timestamptz,
    scheduled_end          timestamptz,
    completed_at           timestamptz,
    cancelled_at           timestamptz,
    cancel_reason          text
);

CREATE TABLE commission_events (
    id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id           uuid NOT NULL REFERENCES bookings(id),
    terms_version        text NOT NULL REFERENCES terms_versions(version),
    base_net_cents       integer NOT NULL CHECK (base_net_cents >= 0),
    rate_percent         numeric(5,2) NOT NULL,
    min_cents            integer NOT NULL,
    amount_net_cents     integer NOT NULL CHECK (amount_net_cents >= 0),
    status               text NOT NULL DEFAULT 'entstanden'
                         CHECK (status IN ('entstanden','gestellt','bezahlt','erlassen','storniert')),
    created_at           timestamptz NOT NULL DEFAULT now(),
    invoiced_at          timestamptz,
    paid_at              timestamptz
);

CREATE TABLE outbox_events (
    id            bigserial PRIMARY KEY,
    topic         text NOT NULL,
    payload       jsonb NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    delivered_at  timestamptz,
    attempts      integer NOT NULL DEFAULT 0
);

CREATE TABLE audit_events (
    id           bigserial PRIMARY KEY,
    at           timestamptz NOT NULL DEFAULT now(),
    actor_type   text NOT NULL CHECK (actor_type IN ('kunde','anbieter','admin','system','n8n','llm')),
    actor_id     text,
    entity_type  text NOT NULL,
    entity_id    uuid,
    action       text NOT NULL,
    details      jsonb NOT NULL DEFAULT '{}'::jsonb,
    minutes_spent numeric(6,1)
);

CREATE INDEX idx_requests_status      ON service_requests (status);
CREATE INDEX idx_invitations_request  ON invitations (request_id);
CREATE INDEX idx_quotes_request       ON quotes (request_id);
CREATE INDEX idx_outbox_undelivered   ON outbox_events (id) WHERE delivered_at IS NULL;
CREATE INDEX idx_audit_entity         ON audit_events (entity_type, entity_id);
```

---

## Anhang C – Fachliche Testfälle für `domain/` (Mindestumfang)

1. **Provision:** Netto 50.420 Cent, Satz 8,00 %, Mindestprovision 4.000 Cent → 4.034 Cent. Netto 20.000 Cent → 4.000 Cent (Mindestprovision greift). Netto 252.101 Cent → 20.168 Cent.
2. **Brutto aus Netto:** 50.420 Cent bei 19 % → 60.000 Cent; Kleinunternehmer mit 0 % → Netto = Brutto.
3. **Fingerprint:** gleicher Inhalt in anderer Schlüsselreihenfolge → gleicher Hash; Änderung eines Cent-Betrags → anderer Hash.
4. **Buchung:** abgelehnt bei Status ≠ `verbindlich`, abweichendem Fingerprint oder abgelaufener Gültigkeit.
5. **Token:** Hash gespeichert, Klartext nie; abgelaufener oder fremder Token → kein Zugriff.
6. **Zustandsautomat:** jeder nicht aufgeführte Übergang erzeugt einen Fehler.
7. **Autorisierung:** Anbieter A erhält 403/404 für Vorgänge und Angebote von Anbieter B.
8. **Idempotenz:** doppelter Outbox-Versand oder doppelter n8n-Callback erzeugt weder zweite Mail noch zweites Provisionsereignis.

---

## Anhang D – Referenzen

**Eigener Kontext (Donor):** tonnestate/TonnEstate, LemonMe, DragonFruitMe, BlackberryMe, CherryMe.
**Technologie:** modelcontextprotocol.io, docs.n8n.io.
**Rechtsfelder zur fachlichen Prüfung:** § 7 UWG, §§ 164 ff., 305 ff., 312j BGB, DSGVO, § 5b UWG, PAngV, P2B-VO (EU) 2019/1150, DSA, EU AI Act, Abfallrecht (Beförderung/Entsorgung).

**Dokumentenstatus:** Strategisches Sollkonzept mit Umsetzungsplan. Weder Umsetzungsnachweis noch Rechtsgutachten.
