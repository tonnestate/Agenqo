import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";
import "./style.css";
import ProviderPortal from "./ProviderPortal.jsx";
import BuyerPortal from "./BuyerPortal.jsx";

// Link format: /quote#<opaque token>; fragments are not sent as part of HTTP URL.
// The provider key is sent only in X-Invitation-Key to the Agenqo API.
// Do NOT persist tokens in localStorage, analytics, telemetry or query params.
function QuoteForm() {
  const [token] = useState(() => decodeURIComponent(location.hash.slice(1)));
  const [context, setContext] = useState(null);
  const [schema, setSchema] = useState(null);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!token) { setError("Angebotslink fehlt."); return; }
    Promise.all([
      fetch("/v1/provider/invitation", { headers: {"X-Invitation-Key": token}, cache: "no-store" }),
      fetch("/v1/quote-form-schema", { cache: "no-store" }),
    ]).then(async ([inv, form]) => {
      if (!inv.ok || !form.ok) throw Error("Der Angebotslink ist ungültig oder abgelaufen.");
      setContext(await inv.json());
      setSchema(await form.json());
    }).catch(e => setError(e.message));
  }, [token]);

  async function submit({formData}) {
    setBusy(true); setError("");
    try {
      const validDays = formData.valid_days;
      const expires_at = new Date(Date.now() + validDays*86400000).toISOString();
      const {valid_days, ...rest} = formData;
      const res = await fetch("/v1/provider/quotes", {
        method: "POST",
        headers: {"Content-Type":"application/json", "X-Invitation-Key":token},
        body: JSON.stringify({...rest, expires_at}),
      });
      if (!res.ok) {
        const reply = await res.json().catch(() => ({}));
        throw Error(reply.detail || reply.error || "Angebot konnte nicht abgegeben werden.");
      }
      setSent(true);
      history.replaceState(null, "", "/quote");
    } catch(e) { setError(String(e.message)); }
    finally { setBusy(false); }
  }

  return <main>
    <header><div className="brand">agenqo</div><p>Strukturiertes Dienstleistungsangebot</p></header>
    {error && <div className="error" role="alert">{error}</div>}
    {sent && <section className="success"><h2>Angebot eingegangen</h2><p>Die Anfrage wird manuell geprüft. Eine Buchung ist noch nicht erfolgt.</p></section>}
    {!sent && context && schema && <section>
      <h1>Anfrage beantworten</h1>
      <p><strong>Leistung:</strong> {context.category} · <strong>PLZ:</strong> {context.postal_code}</p>
      <p className="req">{context.requirements}</p>
      {context.structured_requirements && Object.keys(context.structured_requirements).length > 0 &&
        <details><summary>Strukturierte Leistungsdaten</summary><pre>{JSON.stringify(context.structured_requirements,null,2)}</pre></details>}
      <Form schema={schema} validator={validator} disabled={busy} onSubmit={submit}>
        <button disabled={busy} type="submit">{busy ? "Übermittle…" : "Angebot verbindlich einreichen"}</button>
      </Form>
      <p className="note">Der Anbieter bestätigt hier ausschließlich seine Angebotskonditionen. Ein Auftrag entsteht erst nach dem vorgesehenen Freigabe- und Bestätigungsprozess. Dieses Formular ist ein Pilotprototyp.</p>
    </section>}
    {!sent && !error && (!context || !schema) && <p>Anfrage wird geladen…</p>}
  </main>;
}

const isProviderPortal = window.location.pathname.startsWith("/provider");
const isBuyerPortal = window.location.pathname.startsWith("/request/");
createRoot(document.getElementById("root")).render(
  isProviderPortal ? <ProviderPortal/> : (isBuyerPortal ? <BuyerPortal/> : <QuoteForm/>)
);
