# Agenqo v0.4 – Wirtschaftliche Transparenz je Beschaffungsanfrage

**Ziel:** Der Pilot soll auch nach erfolglosen Anfragen wirtschaftlich messbar sein.

## Tatsächlich implementiert

- Eigene, mit Alembic migrierte Tabelle \`request_economic_events\` mit einmaliger Ereignis-ID, Anfragebezug, Art COST/RECEIPT, Kategorie, positivem EUR-Centbetrag und Nachweisreferenz.
- Ein Ereignis darf über dieselbe \`event_key\` nicht mehrfach gezählt werden. Wird für denselben Schlüssel später ein anderer Betrag oder Zweck eingereicht, liefert die API HTTP 409.
- Operator-gesicherte Erfassung: \`POST /v1/admin/requests/{id}/economic-events\`.
- Abfrage je Kundenanfrage einschließlich gescheiterter: \`GET /v1/admin/requests/{id}/economics\`.
- Aggregat für den gesamten Concierge-Pilot: \`GET /v1/admin/economics/summary\`.
- Getrennte Größen für **provisionsfähige Forderungen** und **als tatsächlich erhalten dokumentierte Gebühren**. Ein nur erwarteter Provisionsbetrag ist keine Einnahme.
- Prüffälle für Kosten ohne Abschluss, ausbleibende Einnahmen, doppelte Ereignisse und Übermittlung nicht zulässiger Beträge.

## Abgrenzung

Das Journal ist **kein Finanzbuchhaltungs-, Steuer- oder Zahlungsdienstleister-Ersatz**. Die Einnahmen beruhen auf manuell hinterlegten Nachweisreferenzen; diese werden vom Prototyp nicht automatisch gegen Bank/PSP verifiziert. Das Aggregat ist ein **operativer, unvollständiger Deckungsbeitrag vor Fixkosten, Steuern und noch nicht erfassten Aufwänden**, nicht Gewinn oder rechtlich korrekt bilanzierter Umsatz.

Provisionsansprüche werden nur über die bestehende vertragsspezifische Kommissionsengine erzeugt. Einnahmen werden erst erfasst, wenn ihr tatsächlicher Eingang unabhängig belegt und als \`RECEIPT\` dokumentiert ist. Für Stornos und Korrekturen ist vor Produktion ein revisionssicheres Gegenbuchungsverfahren erforderlich; die erste API erlaubt ausdrücklich kein Löschen oder stilles Editieren.

## Offene Aufgaben

- Automatische n8n-/LLM-Kostenzuordnung mit tatsächlichen Provider-Preisen und Tokenverbrauch.
- CAC- und Provider-Onboarding-Kosten konsistent auf Anfragen und Kohorten verteilen.
- Zahlungseingänge über einen externen Anbieter verifizieren, Rückerstattungen separat ausgleichen.
- Gesamtunternehmens-Fixkosten und wiederkehrende Premium-Abos in eigenen Aggregaten führen.
- Eine dokumentierte Go-/No-Go-Entscheidung nach ausreichend echten Vorgängen treffen.

**Wichtig:** Zero-Turnover-Probleme werden sichtbar; die Zahl der bekannten Firmen allein ist keine ökonomische Erfolgskennzahl.
