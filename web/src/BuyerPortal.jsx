import React, {useCallback, useEffect, useState} from "react";

const formatEUR = cents => new Intl.NumberFormat("de-DE", {
  style: "currency", currency: "EUR",
}).format(cents / 100);

function readAccess() {
  const match = window.location.pathname.match(/^\/request\/([a-f0-9-]{36})\/?$/i);
  if (!match) return {error: "Ungültiger Vorgangslink."};
  let token = "";
  try { token = decodeURIComponent(window.location.hash.slice(1)); }
  catch { return {error: "Der Zugangslink ist beschädigt."}; }
  if (!token || token.length > 256) return {error: "Der persönliche Zugriffsschlüssel fehlt."};
  return {requestId: match[1], token};
}

export default function BuyerPortal() {
  const [access] = useState(readAccess);
  const [details, setDetails] = useState(null);
  const [offers, setOffers] = useState([]);
  const [selected, setSelected] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(access.error || "");
  const [message, setMessage] = useState("");

  const load = useCallback(async () => {
    if (access.error) { setLoading(false); return; }
    setError("");
    try {
      const prefix = "/v1/requests/" + encodeURIComponent(access.requestId);
      const headers = {"X-Customer-Key": access.token};
      const [status, quotes] = await Promise.all([
        fetch(prefix + "/status", {headers, cache: "no-store"}),
        fetch(prefix + "/offers", {headers, cache: "no-store"}),
      ]);
      if (!status.ok || !quotes.ok) {
        throw Error(
          status.status === 403 || quotes.status === 403
            ? "Zugriff verweigert. Bitte den persönlichen Vorgangslink verwenden."
            : "Der Vorgang konnte nicht geladen werden."
        );
      }
      const detail = await status.json();
      const offerData = await quotes.json();
      setDetails(detail);
      setOffers(offerData.offers || []);
    } catch (e) { setError(String(e.message || e)); }
    finally { setLoading(false); }
  }, [access]);

  useEffect(() => { load(); }, [load]);

  async function approve() {
    const quote = offers.find(o => o.quote_id === selected);
    if (!quote || !confirmed || details?.status !== "QUOTES_READY") return;
    setSubmitting(true); setError(""); setMessage("");
    try {
      const response = await fetch(
        "/v1/requests/" + encodeURIComponent(access.requestId) + "/approve",
        {
          method: "POST", cache: "no-store",
          headers: {"Content-Type": "application/json", "X-Customer-Key": access.token},
          body: JSON.stringify({
            quote_id: quote.quote_id,
            offer_fingerprint: quote.fingerprint,
          }),
        }
      );
      if (!response.ok) {
        const responseBody = await response.json().catch(() => ({}));
        throw Error(
          typeof responseBody.detail === "string" ? responseBody.detail :
          responseBody.error || "Die Freigabe ist fehlgeschlagen. Bitte erneut prüfen."
        );
      }
      setMessage("Ihre Auswahl wurde erfasst. Der Dienstleister muss den Auftrag noch bestätigen.");
      setConfirmed(false);
      await load();
    } catch (e) { setError(String(e.message || e)); }
    finally { setSubmitting(false); }
  }

  const canSelect = details?.status === "QUOTES_READY" && !submitting;
  const chosen = offers.find(o => o.quote_id === selected);

  return <main className="buyer-portal">
    <header><div className="brand">agenqo</div><p>Meine Dienstleistungsanfrage</p></header>
    <section aria-live="polite">
      {error && <div className="error" role="alert">{error}</div>}
      {message && <div className="success portal-panel" role="status">{message}</div>}
      {loading && <p>Vorgang wird geladen…</p>}
      {details && <>
        <div className="portal-toolbar">
          <h1>Auftragsübersicht</h1>
          <button className="buyer-secondary" type="button" onClick={load} disabled={submitting}>
            Aktualisieren
          </button>
        </div>
        <div className="portal-panel">
          <p><strong>Leistung:</strong> {details.category}</p>
          <p><strong>Einsatzgebiet:</strong> PLZ {details.postal_code}</p>
          <p><strong>Status:</strong> {details.status}</p>
          {details.booking_status && <p><strong>Buchung:</strong> {details.booking_status}</p>}
          <p className="req">{details.requirements}</p>
          {Object.keys(details.structured_requirements || {}).length > 0 &&
            <details><summary>Leistungsangaben anzeigen</summary>
              <pre>{JSON.stringify(details.structured_requirements, null, 2)}</pre>
            </details>}
        </div>
        <h2>Angebote ({offers.length})</h2>
        {offers.length === 0 && <p>Es liegt noch kein geprüftes, gültiges Angebot vor.
          Sobald ein Anbieter verbindlich antwortet und das Angebot geprüft wurde, erscheint es hier.</p>}
        <div className="buyer-offers">
          {offers.map(o => <article className="buyer-offer" key={o.quote_id}>
            <div className="buyer-offer-heading">
              <h3>{o.company_name}</h3>
              <strong>{formatEUR(o.gross_cents)} inkl. angegebener USt.</strong>
            </div>
            <p>{o.description}</p>
            <p><strong>Bedingungen:</strong> {o.conditions || "Keine Angaben"}</p>
            <p className="note">Gültig bis: {new Date(o.valid_until).toLocaleString("de-DE")}
              {" · "}Netto: {formatEUR(o.net_cents)}{" · "}USt: {o.vat_percent} %</p>
            {canSelect && <label className="buyer-choice">
              <input type="radio" name="selectedOffer" value={o.quote_id}
                checked={selected === o.quote_id}
                onChange={() => {setSelected(o.quote_id); setConfirmed(false);}} />
              Dieses Angebot auswählen
            </label>}
          </article>)}
        </div>
        {canSelect && chosen && <div className="portal-panel buyer-confirm">
          <h3>Auswahl prüfen und freigeben</h3>
          <p>Sie wählen das Angebot von <strong>{chosen.company_name}</strong> mit
            einem Gesamtpreis von <strong>{formatEUR(chosen.gross_cents)}</strong>.
            Maßgeblich ist genau die angezeigte Angebotsversion.</p>
          <label className="buyer-choice">
            <input type="checkbox" checked={confirmed}
              onChange={e => setConfirmed(e.target.checked)} />
            Ich habe Preis, Leistungsumfang und Bedingungen geprüft und möchte dieses
            Angebot zur Buchung freigeben.
          </label>
          <button type="button" onClick={approve} disabled={!confirmed || submitting}>
            {submitting ? "Freigabe läuft…" : "Angebot zur Buchung freigeben"}
          </button>
          <p className="note">Pilot: Die Freigabe wird revisionsgebunden gespeichert.
            Die Anbieterbestätigung ist ein separater Schritt. Rechtliche Vertragsunterlagen
            und Verbraucherinformationen müssen vor öffentlichem Livebetrieb freigegeben werden.</p>
        </div>}
        {details.status !== "QUOTES_READY" && <p className="note">
          Für diesen Status ist derzeit keine neue Angebotsfreigabe möglich.
        </p>}
      </>}
      <p className="note">Dieser persönliche Link ermöglicht Zugriff auf den Vorgang.
        Geben Sie ihn nicht weiter.</p>
    </section>
  </main>;
}
