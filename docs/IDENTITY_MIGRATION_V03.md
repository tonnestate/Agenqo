# Agenqo v0.3 — Provider-Identität und Datenbankmigration

Stand 27.10.2026. Status: code- und CI-geprüfter Implementierungsschritt, keine Produktionsfreigabe.

## Recherche/Donoren (aktuell geprüft)

- [sqlalchemy/alembic](https://github.com/sqlalchemy/alembic), MIT: versionierte SQLAlchemy-Schemamigrationen. Übernommen: Alembic-Integration und manuell fixierte erste Revision.
- [jpadilla/pyjwt](https://github.com/jpadilla/pyjwt), MIT: asymmetrische Access-Token-Prüfung und JWKS. Übernommen: Bibliothek über feste Version-Ranges und ein enges Resource-Server-Interface.
- [authlib/authlib](https://github.com/authlib/authlib), BSD-3-Clause: alternative OAuth/OIDC-Infrastruktur; nicht zusätzlich eingebaut, da Agenqo derzeit nur JWT-Resource-Server-Funktionalität benötigt.
- [keycloak/keycloak](https://github.com/keycloak/keycloak), Apache-2.0: künftiger optionaler OIDC-Provider; **nicht** in Agenqo integriert.
- [openfga/openfga](https://github.com/openfga/openfga), Apache-2.0: möglicher späterer Beziehungsgraf für komplexe Agentenrechte; aktuell wären Netzwerklaufzeit und Betriebsaufwand unnötig.

Die JWT-Prüfung setzt RFC 9068 voraus: Access-Token-Typ (nicht ID-Token), Issuer, Audience, Signatur, Algorithmus und Ablauf werden serverseitig geprüft. Ohne konfigurierte Vertrauensanker wird keine Provider-Funktion freigeschaltet.

## Kernablauf

1. Externer vertrauenswürdiger OIDC-Provider authentifiziert den Menschen oder autorisierten Agenten und stellt ein \`at+jwt\`-Access-Token für Audience \`agenqo-api\` aus.
2. \`POST /v1/provider/companies/{id}/claim\` registriert \`sub\`, Nachweisreferenz und E-Mail; es entsteht nur \`PENDING\`.
3. Ein Admin prüft Firmenvertretung **außerhalb** dieses API-Prototyps und gibt \`/v1/admin/ownership-claims/{id}/review\` frei.
4. In einer Transaktion wird \`CompanyMembership(company_id, subject, role=OWNER)\` mit Nachweisreferenz angelegt.
5. Nur dieser JWT-Subject darf \`GET /v1/provider/companies\` und \`POST /v1/provider/companies/{id}/proposed-updates\` für sein Unternehmen verwenden. Fremde Firmen liefern HTTP 403.
6. Anbieteränderungen werden als Beobachtungen dokumentiert; kanonische Golden Fields verändern sich erst nach separater administrativer Prüfung und expliziter Publikation.

## Sicherheitsgrenzen

- JWKS-URL wird ausschließlich in Server-Konfiguration gesetzt, niemals aus Benutzerwerten übernommen.
- HTTPS ist für JWKS erforderlich; zulässiger Algorithmus ist explizit RS256.
- Bearer-Token werden weder protokolliert noch persistiert.
- Firmenrollen kommen aus der Agenqo-Datenbank, **nicht** aus untrusted JWT-Rollen-Claims.
- Alte manuell erfasste Ownership-Claims ohne gültiges OIDC-Subject können keine Mitgliedschaft erzeugen.
- Selbstbestätigte E-Mail oder Domain genügt nicht zum Erwerb einer Mitgliedschaft.
- API-Schlüssel für Adminzugriffe sind weiterhin nur ein interner Prototypenmechanismus; ersetzen vor Livebetrieb durch OIDC/RBAC mit MFA und Audit.
- Ausfall/JWKS-Rotation/Revocation, Tokenmissbrauch, HTTP-Sicherheitsheader, Anti-Spam, Datenschutz, DSGVO und rechtliche Buchungsfreigaben erfordern weitere Arbeit.

## Migration

Auf leerer Datenbank:

\`\`\`bash
export AGENQO_DATABASE_URL='postgresql+psycopg://...'
alembic upgrade head
\`\`\`

Für alte, nie migrierte Prototypdatenbanken wird **kein blindes STAMP empfohlen**. Ein eigenes Bestandsdaten- und Constraints-Diff ist vor jeder Übernahme zu erstellen. SQLite wird im CI gegen eine frische Datei getestet; PostgreSQL erhält eine frische Schema-Migration im separaten CI-Service.

Künftige Änderungen als neue Alembic-Revisionen aufsetzen und nicht die Baseline überschreiben.

## Keine Produktionsbehauptung

GitHub Actions, SQLite-Test und PostgreSQL-Migration sind technische Prüfungen. Identitätsausgabe, reale Kunden-/Anbieterdaten, Registrierungs-UX, Vertragsannahme und wirtschaftliche Nutzung sind noch nicht deployed oder live validiert.
