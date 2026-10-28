# Agenqo v0.8 — Kontaktfreigabe und Käuferansicht

**Stand:** 28.10.2026 · **Status:** im Repository implementierte Pilotfunktionen; **kein produktiver Outreach oder vollständiger öffentlicher Marktplatz**.

## 1. Hintergrund / Schnitt zum v3.0-P0-Ausführungsvertrag

Umgesetzt wurden zwei geschlossene technische Teilabläufe:

1. **P0-01, Kontakt-Policy:** administrative, beweisbezogene Anbieterzustimmung für E-Mail-RFQs; versionierte Widerrufe; gesicherte und auditierte Prüfung einer bestehenden Einladung; selbstständiges Opt-out über den individuellen Anbieterlink. Kein automatischer Versand.
2. **P0-02, Käuferentscheidung:** aus einem bereits administrativ angelegten RFQ eine kundenseitige, geschützte Vorgangs-/Angebotsansicht und exakte Freigabe des Angebots. **Noch kein selbstständiges öffentliches Anlegen von RFQs**; keine Zahlungsabwicklung.

Es bleibt zwingend bei **MySQL/InnoDB** als operativem Store und der vorhandenen n8n-Outbox-Brücke. Das neue Schema ist Alembic **0004_contact_policy**. Keine neue Datenbank/Blockchain, kein automatisches E-Mail-Tool.

## 2. Contact-Policy-Entscheidung

Dateien:
- \`agenqo/contact_policy.py\`: reine deterministische Entscheidung \`evaluate_rfq_email()\`, Policy-Version \`CONTACT_V1_OPT_IN_ONLY\`.
- \`agenqo/contact_policy_api.py\`: admin-geschützte Proof-/Opt-out- und Preflight-APIs; Anbieter-Opt-out per zeitlich begrenztem oder bereits abgelaufenem Einladungstoken (Widerruf muss nach Einladungsablauf möglich bleiben).
- \`agenqo/models.py\`: append-only \`ProviderContactPermission\` und \`ContactPolicyDecision\`.
- \`alembic/versions/0004_contact_policy.py\`: Tabellenmigration.

**Gesetzliche Abgrenzung:** Eine rechtlich erlaubte Verarbeitung einer öffentlich gefundenen Firmenadresse bedeutet nicht, dass wir eine Werbe-E-Mail schicken dürfen. \`SIGNED_PILOT_AGREEMENT\` bezeichnet einen **manuell überprüften Nachweisverweis**, nicht dessen automatische Echtheitsprüfung. Rechtliche Prüfung der konkreten Vertrags-/Kommunikationsmodelle ist vor Liveversand erforderlich. Die aktuelle Entscheidung erlaubt **nur** dokumentiertes Opt-in für E-Mail-Einladungen an den exakt gespeicherten Empfänger. Keine „mutmaßliche Einwilligung“ als pauschales B2B-E-Mail-Recht.

**Fail-closed:**
- Keine dokumentierte aktive Zustimmung ⇒ \`DENY / NO_RECORDED_OPT_IN\`.
- Opt-out ⇒ \`DENY / OPTED_OUT\`.
- E-Mail-Adresse wurde verändert ⇒ \`DENY / RECIPIENT_CHANGED\`.
- Einladung geschlossen/abgelaufen, Anfrage unqualifiziert, falsche Leistung ⇒ \`DENY\`.
- Positive Zustimmung mit unverändertem Empfänger, aktiver Einladung und qualifiziertem Vorgang ⇒ \`ALLOW / RECORDED_OPT_IN\`.

**Wichtig:** Eine positive Bewertung ist nur eine zeitpunktbezogene Vorprüfung; sie erteilt **keine** generelle oder spätere Versanderlaubnis. Ein zukünftiger Versandworker muss die neueste Permission und Widerrufsliste **unmittelbar vor dem tatsächlichen Senden** erneut prüfen und die atomare Versandfreigabe mit Zustellung/Bounce protokollieren. Der aktuelle n8n-Workflow erstellt ausschließlich interne Review-Tasks.

### Administrative Pilotbedienung

\`\`\`http
POST /v1/admin/companies/{company_id}/contact-permissions
X-Admin-Key: <operator-secret>
Content-Type: application/json

{
  "enabled": true,
  "evidence_kind": "SIGNED_PILOT_AGREEMENT",
  "evidence_reference": "signed-pilot-contract-2026-001",
  "reviewer_reference": "manual-check-2026-001"
}
\`\`\`

Die unterschriebene und geprüfte Vereinbarung ist extern sicher aufzubewahren. Der Nachweisverweis darf keine sensitiven Dokumenteninhalte enthalten.

\`\`\`http
POST /v1/admin/invitations/{invitation_id}/contact-preflight
X-Admin-Key: <operator-secret>
\`\`\`

Ergebnis ist \`ALLOW\` oder \`DENY\` mit Policy-Version, Reason-Code und Decision-ID, unabhängig von der Nachrichtenzustellung. Einladungen bleiben technisch \`READY\`; \`external_delivery_performed\` ist **immer false**.

\`\`\`http
POST /v1/provider/contact/opt-out
X-Invitation-Key: <private-invitation-token>
\`\`\`

Widerruf ist idempotent, wird mit einer neuen unveränderlichen Permission-Revision dokumentiert und benötigt kein registriertes Benutzerkonto. Die Reaktivierung darf nur nach neuem, belegtem Opt-in durch den Betreiber erfolgen.

### Audit und Datentrennung

Admin-History: \`GET /v1/admin/companies/{company_id}/contact-permissions\`; Entscheidungen: \`GET /v1/admin/invitations/{invitation_id}/contact-decisions\`. Allgemeine AuditEvents speichern keine Mailadresse und keinen Einladungstoken. Die Datenbank enthält bei Permission die gehashte exakte Zieladresse, keine Versendeberechtigung für andere Ziele. Unternehmensprofil und ContactPermission sind getrennte Datenobjekte.

## 3. Käuferansicht mit Angebot und Freigabe

Bestands-API plus Ergänzung:

- \`GET /v1/requests/{request_id}/status\` (neu): schmaler Vorgangsstatus, Anforderungen, ggf. Buchungsstatus; ausschließlich mit \`X-Customer-Key\`.
- \`GET /v1/requests/{request_id}/offers\` (vorhanden): geprüfte, gültige Angebote mit Brutto-/Netto-Preis und Fingerprint; ausschließlich mit \`X-Customer-Key\`.
- \`POST /v1/requests/{request_id}/approve\` (vorhanden): referenziert exakt die Angebotsrevision; anschließend ist eine Anbieterbestätigung erforderlich.
- \`/request/{request_id}#<customer_token>\` (neu): React-Käuferportal. Das \`#\`-Fragment wird nicht an den Webserver übertragen; Token werden weder in localStorage noch in Query-Parametern verwaltet.

**Pilotablauf:** Betreiber legt via geschützter Admin-API einen realen RFQ an, qualifiziert ihn und erhält das **einmalig ausgegebene** Customer-Token. Ein individueller Link kann dem berechtigten Kunden über einen zuvor autorisierten/sicheren Weg übermittelt werden. Der Kunde sieht seine RFQ, vergleichbare Angebote, die Bedingungen und den späteren Buchungsstatus. Der Kunde wählt eine Offerte und bestätigt aktiv seine Freigabe. Der Provider muss danach separat bestätigen.

Die UI ist ein **Pilot-Prototyp**. Rechtlich vollständige Verbraucher-Informationen, verbindliche AGB, Widerrufs-/Vertragsmodell, Datei-Uploads, Registrierung und Self-Service-RFQ-Intake fehlen. Für einen öffentlichen Launch ist dieser Stand nicht ausreichend. Keine automatische Beschaffung, keine Zahlungsverarbeitung.

## 4. Deployment und Tests

1. Änderungen an bestehender MySQL-Datenbank **vorher sichern**. \`alembic upgrade head\` mit \`0004_contact_policy\` ausführen; in Staging zuerst prüfen.
2. \`python -m pip install -e ".[test]"\`, dann \`pytest\`.
3. Frontend: \`cd web && npm install && npm run build\`.
4. \`docker compose\` nutzt wie zuvor die existierende MySQL-Instanz; der Code startet kein PostgreSQL. Statische \`/request/{uuid}\`-Route wird nur aus dem vorhandenen \`web_dist\` im Container ausgeliefert.
5. Testfälle: Permission fehlt, Empfängerwechsel, Opt-out, wiederholter Opt-out, abgelaufene Einladung, unqualifizierte Anfrage, fremder Käufer-Token, exakte Angebotsfreigabe, bestehende MySQL-Race-Tests. CI prüft die Migrationskette.

**Produktiv nicht freigeben**, solange insbesondere externer Kontaktkanal, Rate Limiting, finale Rechtstexte, Buyer-Intake, Zustellnachweise, Storno/Disputes, OIDC-Providerkonfiguration und Sicherheitstests fehlen.

## 5. Weiterhin offene P0-Schritte

- Kontaktfreigabe mit tatsächlichem Send-Adapter und genau einmaliger, nachgeprüfter Zustellung verbinden; Opt-out, Bounce, Consent-Widerruf und Race-Conditions im gesamten Workflow testen.
- Buyer-Self-Service-Intake mit Abuse-Schutz und einem DSGVO-/AGB-konformen Bestellprozess.
- Einheitliche API-Fehlerstruktur, Token-Rotation/Revocation und Rate Limits für offene Einladungen/Kundenlinks.
- Quote-Revision, Buchungsstorno, Disputes, Completion-Evidence, realer Zahlungseingang.
- ServiceArea-/Fahrzeit-/Anfahrtskosten-Matching, echte Provider-Kapazitätsdaten.
- Pilotpartner und reale Anfragen: 10–15 vertraglich teilnehmende Betriebe, 20–50 qualifizierte RFQs, kohortenbasierter Deckungsbeitrag einschließlich gescheiterter Anfragen.

**Grundsatz:** Quellcode + Tests ≠ Livebetrieb. Die Resultate der tatsächlichen wirtschaftlichen Vermittlung werden erst nach dem Pilot gemessen.

Verweise: [P0-Ausführungsvertrag](AGENQO_V3_P0_EXECUTION_CONTRACT.md), [Gesamtkonzept v3](AGENQO_GESAMTKONZEPT_V3.md), [Datenbankentscheidung](DATENBANK_DONOREN_MYSQL_DUCKDB.md), [n8n-Bridge](N8N_ORCHESTRATION_V07.md), § 7 UWG: https://www.gesetze-im-internet.de/uwg_2004/__7.html
