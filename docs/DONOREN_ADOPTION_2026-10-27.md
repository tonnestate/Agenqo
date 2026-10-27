# Agenqo – Donoren-Entscheidung und erster Integrationsstand

Stand 27.10.2026. Nur die hier als INTEGRATED gekennzeichneten Funktionen wurden tatsächlich eingebaut.

| Donor / Quelle | Wiederverwendeter Mechanismus | Status |
| --- | --- | --- |
| TonnEstate: catalog_survivorship_service.py | Quellennachweise und freigegebener Feldstand; unabhängiges SQLAlchemy-Modell in Agenqo | ADAPTED |
| TonnEstate: catalog_quality_service.py | Datenvalidierung und getrennte Quellen-/Reviewzustände | ADAPTED |
| React JSON Schema Form (rjsf-team/react-jsonschema-form), Apache-2.0 | Dynamisches Anbieterformular aus Agenqo-JSON-Schema | INTEGRATED |
| PomeloMe, Apache-2.0 | Geschäftseffekt-Outbox mit PENDING-Ereignis; keine Zustellung oder externe Reconciliation | PATTERN ONLY |
| TonnEstate: cooperation_settlement_ledger_service.py | Historischer Tarifsnapshot als Denkmodell; keine Übernahme des gesamten Ledger-Systems | PARTIAL PATTERN |

Aus TonnEstate wurden keine vorhandenen Unternehmensdaten in Agenqo kopiert. Die neue Provenienzstruktur benötigt zunächst manuelle, geprüfte Beobachtungen. Eine geprüfte Lizenz ist mehr als ein Textfeld; die Admin-Angabe PUBLIC_REUSE_APPROVED ist nur ein technisches Gate, kein juristischer Nachweis.

## Mercur – geprüft und für den unmittelbaren Kern zurückgestellt

Quelle: https://github.com/mercurjs/mercur · GitHub-Metadaten: MIT, aktive Entwicklung am 27.10.2026.
Mercur bietet Verkäufer- und Administrationsflächen sowie Multi-Vendor- und Kommissionsfunktionen. Sein Stack ist auf Medusa/Commerce und auf Warenbestellungen ausgerichtet, während Agenqo bei individueller Dienstleistungsanfrage, Besichtigung, Angebot, Termin und kundenautorisierter Buchung ansetzt.

Entscheidung: DEFERRED als fachliche Kernplattform. Die direkte Integration wäre eine Plattformmigration, nicht nur eine kleine UI-Komponente. Oberflächenmuster können später vergleichend evaluiert werden. Es wurde kein Mercur-Code kopiert.

## Nachweis / Nichtnachweis

- Python-Backend akzeptiert optional strukturierte Entrümpelungsanforderungen gemäß festem JSON-Schema.
- Angefragter Dienstleister kann seine Einladung ohne URL-Token-Parameter im neuen Header-Endpunkt anzeigen und einmalig antworten.
- Angebotsfingerprint bindet optional strukturierte Angebotsattribute.
- Ein Golden Record besteht aus quellengebundenen Beobachtungen, manueller Prüfung und explizit publizierten Feldern.
- Ownership-Claims können für den Pilot manuell geprüft werden, aber es gibt **noch keine Kontoanmeldung und keine resultierenden Zugriffsrechte**.
- Ein bestätigter Auftrag erzeugt ein PENDING-Outbox-Ereignis ohne Kontakt-/Zugriffstokens; **es gibt noch keinen n8n-Dispatcher**.
- Das React-Formular wird im Entwicklungsmodus von Vite und im Docker-Image statisch ausgeliefert, aber ohne fertige Auth-/DDoS-Abwehr. Kein externer Produktivbetrieb.
- Keine Anbietergewinnung, kein rechtliches Click-Wrap, keine Abrechnungsinkassofunktion und keine nachgewiesenen Umsätze.
