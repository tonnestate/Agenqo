# Agenqo

## Aktueller Konzeptstand v3.0 (27.10.2026)

- **[Agenqo Gesamtkonzept v3.0 – Vermittlungszentrale, B2C/B2B, Anbieter- und Käuferagenten, Kanäle, Geo und Monetarisierung](docs/AGENQO_GESAMTKONZEPT_V3.md)**
- **[Branchen- und Leistungskatalog v3.0 – 24 Dienstleistungsdomänen](docs/AGENQO_BRANCHENKATALOG_V3.md)**
- [Agenqo v2.0 – Historischer Konzeptstand](docs/AGENQO_GESAMTKONZEPT.md)
- [Ursprünglicher MVP- und Validierungsplan – Referenz, bei Widersprüchen gilt v3.0](docs/MVP_UND_VALIDIERUNG.md)

Die v3.0 ist der aktuelle fachliche Soll-Stand. Sie definiert ausdrücklich **ein vollständig eigenständiges Agenqo-Produkt**, keine Laufzeitabhängigkeit von TonnEstate, einen mehrkanaligen RFQ-Marktplatz, regionale Servicegebiete sowie optionalen Buyer- und Provider-MCP. Dokumente sind keine Behauptung bereits implementierter oder rechtlich freigegebener Funktionen.

**Agenqo ist als eigenständige, KI-native Dienstleistungsplattform konzipiert.** Menschen, Unternehmen und bevollmächtigte KI-Agenten sollen dort Dienstleistungen finden, anbieten, vergleichen, verhandeln und verbindlich beauftragen können.

**Status: Konzeptphase.** In diesem Repository liegt zunächst die verbindliche Produktvision und der Umsetzungsplan. Es wird nicht behauptet, dass Marktplatz, MCP-Endpunkte, Buchung, Verhandlung oder Abrechnung bereits implementiert oder produktiv nutzbar sind.

## Kerngedanke

Agenqo ist **die zentrale Vermittlungsinfrastruktur zwischen Käufer- und Anbieteragenten** und funktioniert zugleich als eigenständiges Webportal – auch ohne installierten KI-Agenten.

- **Käufer:** suchen über Webportal, KI-Chat, Käufer-MCP oder eigene Agenten passende Dienstleistungen, holen echte Angebote ein und beauftragen nach Autorisierung.
- **Anbieter:** registrieren oder beanspruchen ihr Unternehmensprofil, pflegen Leistungen, Einsatzgebiete, Preise und Verfügbarkeiten; optional verwenden sie einen Anbieter-MCP oder eigene Agenten.
- **Agenqo:** verifiziert Identitäten, betreibt den eigenen Golden Company Record, normalisiert Angebote, koordiniert Verhandlungen und Buchungen, erfasst Provisionsereignisse und bietet optional kostenpflichtige Automatisierung.
- **n8n:** orchestriert asynchrone Kommunikation und Integrationen; die verbindliche Geschäftslogik liegt im unabhängigen Agenqo-Backend.

## Verbindliche Leitplanken

1. **Eigenständiges Produkt:** Eigene Datenbank, API, Geschäftslogik, Authentifizierung, Betriebsumgebung, Frontends, Partnerverträge und Abrechnung. Keine Laufzeitabhängigkeit von TonnEstate.
2. **Dienstleistungen zuerst:** Kein Produktpreisvergleich im initialen MVP. Die Architektur lässt spätere Erweiterungen offen.
3. **Zweiseitiger Marktplatz:** Webportal und Agenten-Schnittstellen für Käufer **und** Anbieter. Ein MCP ist optional; kein Nutzer oder Betrieb muss lokal etwas installieren.
4. **Datenqualität statt Vollständigkeitsbehauptung:** Golden-Record-Quellen sind verifiziert, lizenzkonform und mit Änderungen durch Anbieter abgestimmt.
5. **Keine unautorisierten Transaktionen:** LLMs schlagen vor; deterministische Regeln, Berechtigungen und bestätigte Auftragszustände entscheiden.
6. **Verdienen statt Demo:** Der MVP beweist echte Angebotsabgaben, Buchungen und wirtschaftliche Deckungsbeiträge; Erlösmodelle sind Hypothesen bis zur Validierung.

## Dokumentation

- [Vollständiges Produkt- und Geschäftskonzept](docs/AGENQO_GESAMTKONZEPT.md)
- [MVP, Umsetzung und wirtschaftliche Validierung](docs/MVP_UND_VALIDIERUNG.md)

## Geplanter Einstieg

**Pilotkategorie:** Entrümpelung/Wohnungsauflösung in einer begrenzten Region mit überprüften, teilnehmenden Anbietern. Danach zusätzliche Dienstleistungen wie Umzug, Möbeltransport und Schädlingsbekämpfung.

**Hinweis:** Erwähnte Drittanbieter, Open-Source-Donoren und Plattformen sind Referenzen oder mögliche Integrationen, keine bestehende Partnerschaft oder bestätigte Datenlizenz.

Stand: 27. Oktober 2026 · Konzept v1.0
