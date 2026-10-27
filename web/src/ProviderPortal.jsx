import React, {useEffect, useState} from "react";
import {UserManager, WebStorageStateStore, InMemoryWebStorage} from "oidc-client-ts";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";

export default function ProviderPortal() {
  const [manager, setManager] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [companies, setCompanies] = useState([]);
  const [claims, setClaims] = useState([]);
  const [query, setQuery] = useState("");
  const [candidates, setCandidates] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [profile, setProfile] = useState(null);
  const [invitations, setInvitations] = useState([]);
  const [formSchema, setFormSchema] = useState(null);
  const [busy, setBusy] = useState(false);

  const [claimEmail,setClaimEmail] = useState("");
  const [claimProof,setClaimProof] = useState("");
  const [proposedField,setProposedField] = useState("legal_name");
  const [proposedValue,setProposedValue] = useState("");
  const [publicConsent,setPublicConsent] = useState(false);

  useEffect(() => {
    let active = true;
    async function init() {
      try {
        const response = await fetch("/v1/public/auth-config", {cache:"no-store"});
        if (!response.ok) throw Error("Identitätskonfiguration konnte nicht gelesen werden.");
        const cfg = await response.json();
        if (!cfg.enabled) {
          if (active) setError("Anbieter-Login noch nicht eingerichtet. Bitte OIDC-Provider und SPA-Client konfigurieren.");
          return;
        }
        const mgr = new UserManager({
          authority: cfg.authority, client_id: cfg.client_id, scope: cfg.scope,
          response_type: "code",
          redirect_uri: window.location.origin + "/provider/callback",
          post_logout_redirect_uri: window.location.origin + "/provider",
          automaticSilentRenew: false, monitorSession: false,
          userStore: new WebStorageStateStore({store: new InMemoryWebStorage()}),
          stateStore: new WebStorageStateStore({store: window.sessionStorage}),
        });
        if (!active) return;
        setManager(mgr);
        const isCallback = window.location.pathname === "/provider/callback";
        const signedIn = isCallback ? await mgr.signinRedirectCallback() : await mgr.getUser();
        if (isCallback) history.replaceState({}, "", "/provider");
        if (active && signedIn && !signedIn.expired) setUser(signedIn);
      } catch (err) {
        if (active) setError(String(err.message || err));
      } finally {
        if (active) setLoading(false);
      }
    }
    init();
    return () => {active=false;};
  }, []);

  async function request(path, options = {}) {
    if (!user || user.expired) throw Error("Anmeldung abgelaufen – bitte erneut anmelden.");
    const response = await fetch(path, {
      ...options, cache:"no-store",
      headers: {...(options.body ? {"Content-Type":"application/json"} : {}),
        "Authorization":"Bearer " + user.access_token, ...(options.headers||{})},
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw Error(typeof payload.detail === "string" ? payload.detail :
                  payload.error || ("Serverantwort: " + response.status));
    }
    return response.json();
  }

  async function refresh() {
    if (!user) return;
    try {
      const [a,b,c] = await Promise.all([
        request("/v1/provider/companies"),
        request("/v1/provider/claims"),
        fetch("/v1/quote-form-schema", {cache:"no-store"}).then(r => r.json()),
      ]);
      setCompanies(a.companies || []);
      setClaims(b.claims || []);
      setFormSchema(c);
      setError("");
    } catch (e) {setError(String(e.message));}
  }
  useEffect(() => {if (user) refresh();}, [user]);

  async function loadCompany(id) {
    setCompanyId(id); setError(""); setMessage("");
    if (!id) {setProfile(null);setInvitations([]);return;}
    try {
      const [a,b] = await Promise.all([
        request("/v1/provider/companies/" + encodeURIComponent(id) + "/profile"),
        request("/v1/provider/companies/" + encodeURIComponent(id) + "/invitations"),
      ]);
      setProfile(a);setInvitations(b.invitations||[]);
    } catch(e) {setError(String(e.message));}
  }

  async function searchCompanies() {
    setBusy(true);setError("");
    try {
      const r = await fetch("/v1/public/companies?q=" + encodeURIComponent(query), {cache:"no-store"});
      if (!r.ok) throw Error("Mindestens drei Zeichen für die Suche eingeben.");
      setCandidates((await r.json()).companies || []);
    } catch(e){setError(String(e.message));} finally {setBusy(false);}
  }

  async function claim(id) {
    setBusy(true);setError("");setMessage("");
    try {
      await request("/v1/provider/companies/"+encodeURIComponent(id)+"/claim",
        {method:"POST",body:JSON.stringify({claimant_email:claimEmail,proof_reference:claimProof})});
      setMessage("Übernahmeantrag eingegangen. Eine Freigabe erfolgt erst nach manueller Vertretungsprüfung.");
      await refresh();
    } catch(e){setError(String(e.message));} finally {setBusy(false);}
  }

  async function propose(e) {
    e.preventDefault();setBusy(true);setError("");setMessage("");
    try {
      await request("/v1/provider/companies/"+encodeURIComponent(companyId)+"/proposed-updates",
        {method:"POST",body:JSON.stringify({
          field_name: proposedField,value: proposedValue,
          public_reuse_consent: publicConsent
        })});
      setMessage("Änderungsvorschlag eingereicht; noch nicht öffentlich veröffentlicht.");
      setProposedValue("");
      await loadCompany(companyId);
    } catch(e){setError(String(e.message));} finally {setBusy(false);}
  }

  async function offer(invitationId, {formData}) {
    setBusy(true);setError("");setMessage("");
    try {
      const {valid_days,...fields} = formData;
      const expires_at = new Date(Date.now()+valid_days*86400000).toISOString();
      await request("/v1/provider/companies/"+encodeURIComponent(companyId)+
        "/invitations/"+encodeURIComponent(invitationId)+"/quotes",
        {method:"POST",body:JSON.stringify({...fields,expires_at})});
      setMessage("Angebot eingegangen; interne Angebotsprüfung steht noch aus.");
      await loadCompany(companyId);
    } catch(e){setError(String(e.message));} finally {setBusy(false);}
  }

  async function confirm(bookingId) {
    setBusy(true);setError("");setMessage("");
    try {
      await request("/v1/provider/companies/"+encodeURIComponent(companyId)+
        "/bookings/"+encodeURIComponent(bookingId)+"/confirm",
        {method:"POST",body:"{}"});
      setMessage("Buchung bestätigt. Der Auftrag muss noch dokumentiert durchgeführt werden.");
      await loadCompany(companyId);
    } catch(e){setError(String(e.message));} finally {setBusy(false);}
  }

  return <main className="provider-portal">
    <header>
      <div className="brand">agenqo</div>
      <p>Anbieterportal · Concierge-Pilot</p>
    </header>
    <section>
      <h1>Mein Unternehmen und meine Anfragen</h1>
      {loading && <p>Identitätsdienst wird geprüft …</p>}
      {error && <div className="error" role="alert">{error}</div>}
      {message && <div className="success" role="status">{message}</div>}
      {!loading && manager && !user && <div>
        <p>Für Ihr Unternehmensprofil ist eine Anmeldung über den konfigurierten Identitätsdienst erforderlich.</p>
        <button onClick={() => manager.signinRedirect().catch(e=>setError(String(e.message)))}>Sicher anmelden</button>
        <p className="note">OAuth2 Authorization Code mit PKCE. Keine Passwörter bei Agenqo.</p>
      </div>}
      {user && <div>
        <div className="portal-toolbar">
          <strong>Authentifiziert</strong>
          <button className="secondary" onClick={()=>refresh()}>Aktualisieren</button>
          <button className="secondary" onClick={async()=>{await manager.removeUser();setUser(null);setProfile(null);setCompanies([]);}}>
            Lokal abmelden
          </button>
        </div>
        <h2>Meine Unternehmen</h2>
        {companies.length===0 && <p>Noch kein Unternehmen freigegeben. Nutzen Sie die Suche für einen Übernahmeantrag.</p>}
        {companies.length>0 && <select aria-label="Unternehmen auswählen" value={companyId}
          onChange={e=>loadCompany(e.target.value)}>
          <option value="">Unternehmen auswählen</option>
          {companies.map(c=><option key={c.company_id} value={c.company_id}>{c.legal_name} · {c.role}</option>)}
        </select>}
        {profile && <div className="portal-panel">
          <h3>{profile.legal_name}</h3>
          <p>{profile.postal_code} · {profile.service_category} · Status {profile.company_status}</p>
          <details><summary>Veröffentlichte Daten und offene Änderungen</summary>
            <pre>{JSON.stringify(profile.published_fields,null,2)}</pre>
            {profile.proposed_fields.map((p,i)=><p key={i}>{p.field}: {p.value} ({p.review_state})</p>)}
          </details>
          <form onSubmit={propose} className="portal-form">
            <h3>Profiländerung vorschlagen</h3>
            <label>Feld
              <select value={proposedField} onChange={e=>setProposedField(e.target.value)}>
                <option value="legal_name">Firmenname</option>
                <option value="postal_code">Postleitzahl</option>
                <option value="contact_email">Kontakt-E-Mail</option>
                <option value="service_category">Leistungskategorie</option>
              </select>
            </label>
            <label>Neuer Wert
              <input required maxLength={255} value={proposedValue}
                onChange={e=>setProposedValue(e.target.value)}/>
            </label>
            <label className="inline-check">
              <input type="checkbox" checked={publicConsent} onChange={e=>setPublicConsent(e.target.checked)}/>
              Ich stimme der öffentlichen Verwendung dieses Firmenfelds zu
            </label>
            <button type="submit" disabled={busy}>Prüfpflichtige Änderung einreichen</button>
          </form>
          <h3>Anfragen und Angebote</h3>
          {invitations.length===0 && <p>Derzeit keine Anfragen für dieses Unternehmen.</p>}
          {invitations.map(inv=><article className="portal-panel" key={inv.invitation_id}>
            <h4>{inv.request_category} · {inv.request_postal_code}</h4>
            <p className="req">{inv.request_description}</p>
            <p>Einladung: {inv.invitation_status} · gültig bis {new Date(inv.invitation_expires_at).toLocaleString("de-DE")}</p>
            {inv.quote && <p>Angebot: {inv.quote.status} · {(inv.quote.gross_cents/100).toLocaleString("de-DE",{style:"currency",currency:"EUR"})}</p>}
            {inv.booking && <p>Buchung: {inv.booking.status}</p>}
            {inv.booking?.status==="CUSTOMER_APPROVED" &&
              <button disabled={busy} onClick={()=>confirm(inv.booking.booking_id)}>Buchung bestätigen</button>}
            {inv.invitation_status==="READY" && new Date(inv.invitation_expires_at)>new Date() &&
              formSchema && <details>
                <summary>Verbindliches Angebot abgeben</summary>
                <Form schema={formSchema} validator={validator} disabled={busy}
                  onSubmit={data=>offer(inv.invitation_id,data)}>
                  <button disabled={busy} type="submit">Angebot einreichen</button>
                </Form>
              </details>}
          </article>)}
        </div>}
        <div className="portal-panel">
          <h2>Unternehmen finden und übernehmen</h2>
          <div className="portal-toolbar">
            <input aria-label="Firma suchen" placeholder="Firmenname (mind. 3 Zeichen)"
              value={query} maxLength={80} onChange={e=>setQuery(e.target.value)}/>
            <button onClick={searchCompanies} disabled={busy||query.trim().length<3}>Suchen</button>
          </div>
          <label>Kontakt-E-Mail
            <input value={claimEmail} type="email" onChange={e=>setClaimEmail(e.target.value)}/>
          </label>
          <label>Nachweisreferenz (z. B. Handelsregister / manuell überprüfbarer Beleg)
            <input value={claimProof} onChange={e=>setClaimProof(e.target.value)} maxLength={1024}/>
          </label>
          {candidates.map(c=><div className="portal-toolbar" key={c.company_id}>
            <span>{c.legal_name} · {c.postal_code}</span>
            <button disabled={busy||!claimProof||!claimEmail} onClick={()=>claim(c.company_id)}>Übernahme beantragen</button>
          </div>)}
          {claims.length>0 && <details><summary>Meine Übernahmeanträge</summary>
            {claims.map(c=><p key={c.claim_id}>Unternehmen {c.company_id}: {c.review_state}</p>)}
          </details>}
        </div>
      </div>}
      <p className="note">Pilotbetrieb: Es werden keine automatischen Anbieter-E-Mails versendet oder Zahlungen abgewickelt. Angegebene Unternehmensdaten werden vor Veröffentlichung geprüft.</p>
    </section>
  </main>;
}
