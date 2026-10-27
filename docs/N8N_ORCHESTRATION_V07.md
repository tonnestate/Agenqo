# Agenqo n8n-Orchestrierung v0.7 — MySQL-Outbox und interne Review-Aufgaben

**Stand 27.10.2026.** Implementiert als Code + importierbare n8n-Workflowdatei. Das Workflow-JSON ist **nicht** auf der vorhandenen n8n-Instanz importiert, aktiviert oder live ausgeführt worden. Keine externe Nachricht wurde versendet.

## Zielarchitektur

\`\`\`text
Agenqo (FastAPI, MySQL / InnoDB, verbindliche Geschäftslogik)
     |
     +-- INSERT outbox_events in derselben DB-Transaktion
                    |
                    v
    vorhandenes n8n (Schedule Trigger, eine Abholung / Minute)
                    |
          POST /v1/integrations/n8n/claim
          X-Agenqo-Bridge-Key: <n8n-only secret>
                    |
          {event_id, lease_token, type, allowlisted IDs}
                    |
          POST /v1/integrations/n8n/complete
          {event_id, lease_token, execution_ref}
                    |
                    v
      Agenqo MySQL: DONE + eindeutige interne Review-Aufgabe
                    |
                    v
      Admin: GET /v1/admin/automation/review-tasks
\`\`\`

**Agenqo entscheidet** über Einladungen, Angebotsbindung, Buchungen, Provisionen, Datenschutz und Zulässigkeit der Kommunikation. **n8n führt kontrollierte Nebenwirkungen aus**, verwaltet weder Buchungszustände noch Verträge. Eingebettetes DuckDB bleibt ein getrenntes Analysewerkzeug. Es werden weder PostgreSQL noch ein weiterer n8n-Server oder eine zusätzliche Queue installiert.

## Eingebaute Ereignisse

| Ereignis | Auslöser | Erlaubte Verarbeitung v0.7 |
|---|---|---|
| \`invitation.review_requested\` | Admin legt eine Anbieter-Einladung an | Nur interne Kontrollaufgabe – **kein** Anbieter-E-Mail-Versand |
| \`quote.review_requested\` | Anbieter reicht Angebot ein | Interne Angebotsprüfung |
| \`booking.confirmed\` | Anbieter bestätigt Käuferfreigabe | Interne Buchungs-/Qualitätsaufgabe |

Die fachlichen Ereignisse werden in derselben MySQL-Transaktion wie der Geschäftszustand erstellt. Zulässige Payloads enthalten ausschließlich interne IDs und \`policy=INTERNAL_REVIEW_ONLY\`. Historische \`booking.confirmed\`-Ereignisse aus v0.2 ohne Policy werden ausschließlich als interne Aufgaben behandelt, sofern ihr Feldschema exakt zur Allowlist passt. Keine Adressen, Rohbedarfe, personenbezogene Daten, E-Mail-Ziele, Download-URLs, Provider-Tokens oder freiformulierte Chat-Inhalte gehen an n8n.

## Integration in die bestehende n8n-Installation

1. MySQL der bestehenden Agenqo-Installation **gezielt sichern** und Alembic-Migration \`0003_n8n\` separat mit \`alembic upgrade head\` anwenden; bei bestehenden Bestandsdaten vorher Schema prüfen.
2. Ein **zufälliges, mindestens 32-stelliges** Bridge-Geheimnis erzeugen und als \`AGENQO_N8N_BRIDGE_KEY\` ausschließlich serverseitig setzen. Weder dieses Geheimnis noch Zugangsdaten auf GitHub ablegen. Für ein späteres produktives Rollout Geheimnisse rotieren und Rate-Limits/IP-ACL/TLS durch den vorhandenen Reverse Proxy erzwingen.
3. Datei \`n8n/workflows/agenqo_internal_review_outbox.json\` in die vorhandene n8n-Instanz importieren. **Inaktiv lassen**, bis Verbindung und Rechte geprüft sind.
4. Bei beiden HTTP Request Nodes die Platzhalter-URL durch eine **aus n8n erreichbare, TLS-abgesicherte** Agenqo-API-Adresse ersetzen. Die Docker-Adresse \`127.0.0.1\` zeigt innerhalb eines Containers nicht automatisch auf Agenqo.
5. In n8n genau eine verschlüsselte Credential vom Typ **HTTP Header Auth** erstellen: Name \`X-Agenqo-Bridge-Key\`, Value derselbe 32+-Zeichen-Wert. Beide HTTP Nodes mit dieser Credential verbinden. Kein Key als URL-Parameter oder Node-JSON hinterlegen.
6. Zunächst \`POST /v1/integrations/n8n/claim\` in n8n manuell gegen ein berechtigtes **Testevent** ausführen und \`/complete\` prüfen. Danach \`GET /v1/admin/automation/status\` und \`/review-tasks\` auf \`DONE\` bzw. eine einzige interne Aufgabe kontrollieren.
7. Erst nach dieser Prüfung den Workflow in n8n aktivieren. Er führt **keinen Mail-, SMS-, WhatsApp-, Zahlungs- oder Buchungsaufruf** aus.

n8n importiert üblicherweise keine Credentials aus fremden Workflow-JSONs. Ein Import-Buildtest belegt nur gültiges JSON/Node-Struktur, nicht die Runtime-Kompatibilität mit der installierten n8n-Version; diese ist separat zu prüfen.

## Interne Bridge-Endpunkte

- \`POST /v1/integrations/n8n/claim\` — Atomare Übernahme eines Ereignisses per \`SELECT ... FOR UPDATE SKIP LOCKED\` auf MySQL 8; 120 Sekunden Lease, höchstens fünf Versuche.
- \`POST /v1/integrations/n8n/complete\` — Quittiert nur mit aktivem Lease-Token, legt idempotent eine eindeutig identifizierte \`AutomationReviewTask\` an und committed \`DONE\` in derselben Transaktion. Wiederholung mit identischem \`execution_ref\` liefert Replay.
- \`POST /v1/integrations/n8n/fail\` — Abbruchcode aus fester Allowlist und exponentielle Wartezeit. Keine sensiblen Fehlermeldungen im Event gespeichert.
- \`GET /v1/admin/automation/status\` — Anzahl PENDING, LEASED, DONE, DEAD sowie offene interne Tasks.
- \`GET /v1/admin/automation/review-tasks\` — Interne Kontrollaufgaben, nach Admin-Key gesichert (später OIDC/RBAC).
- \`POST /v1/admin/automation/events/{event_id}/retry\` — Admin kann DEAD nach dokumentiertem Grund erneut freigeben.

Die Bridge authentifiziert sich unabhängig von der alten globalen Admin-Credential über den Header \`X-Agenqo-Bridge-Key\`. Ohne Bridge-Konfiguration antwortet sie \`503\` (fail-closed).

**Fehlersemantik:** Ein n8n-Absturz während einer Lease erzeugt keinen angenommenen Erfolg. Nach 120 Sekunden wird ein nicht quittiertes Ereignis erneut verfügbar. Spätestens nach fünf gescheiterten Leases geht es in die DEAD Queue. Erfolg bedeutet ausschließlich **interne Aufgabenpersistierung**; **nicht** dass ein Partner kontaktiert wurde. Alle Nebenwirkungen müssen später eigene Idempotenzschlüssel auf Basis der unveränderlichen Event-ID verwenden. Kein Exactly-once-Versprechen für externe APIs.

## Recht und Betrieb

- Das initiale n8n-Workflow-JSON enthält **keine externen Kommunikationskanäle**. Eine geschäftliche Anbieteranfrage darf nicht allein aufgrund eines recherchierten Firmenprofils als erlaubt behandelt werden. UWG/DSGVO, berechtigte Kontaktaufnahme, Kanal-Opt-in, Widerruf und Nachweis benötigen ein eigenes Policy-Gate vor einem zukünftigen Sendeschritt.
- n8n läuft im Betreiberinteresse intern. Nutzer konfigurieren **keine eigenen** n8n-Workflows. Für Kunden zugängliche Workflow-Builder-/Embedding-Geschäftsmodelle sind vor Aktivierung gegen die jeweils geltende n8n-Lizenz zu prüfen.
- Workflows und Credentials nur autorisierten n8n-Administratoren freigeben; ausführungsbezogene Speicherung sensibler Daten deaktivieren; Zugriff auf internen API-Pfad am Reverse Proxy absichern.
- Zuerst eine Staging-Installation mit MySQL-Testdaten verwenden. Keine Änderungen auf dem bereits vorhandenen produktiven MySQL oder n8n in diesem GitHub-Schritt.
- Noch offen: echte Kontaktkanal-Integrationen, rechtliche Kontaktfreigabe, Widerrufsablauf, Rechtsversionen/Click-Wrap, Escalation/SLA, Beobachtbarkeit der n8n-Execution-ID über das UI, alarmierende Fehlerbenachrichtigungen, Last-/Concurrency-Tests mit mehreren n8n-Workern und n8n-Version-Kompatibilität.

## Status und Abnahme

CI muss grün sein für Unit-Tests, vollständige frische MySQL-Alembic-Migration (0001–0003), parallel konkurrierende Claims mit \`SKIP LOCKED\`, Browser-Frontend und JSON-Schema des n8n-Exports. Produktionsabnahme verlangt zusätzlich ein erfolgreiches Ende-zu-Ende-Szenario mit der bestehenden n8n-Installation und verifizierter Identität des Workflow-Betreibers.

Dokumentation:
- n8n HTTP Request credentials: https://docs.n8n.io/integrations/builtin/credentials/httprequest/
- n8n workflows import/export: https://docs.n8n.io/workflows/export-import/
