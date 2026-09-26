import React from "react";
import { AlertTriangle, BarChart3, Bell, CheckCircle2, Leaf, LogOut, Settings2, Sprout } from "lucide-react";

export default function Alerts({ alerts = [], onBack, onOverview, onAnalytics, onAlerts, onLogout, onAcknowledge }) {
  return (
    <main>
      <header>
        <div><small>SMART PLANT / ALERTS</small><h1>Plant Alerts</h1><p>Cloud-generated plant health events and acknowledgements.</p></div>
        <button className="primary" onClick={onBack}>Back to Overview</button>
      </header>

      <section className="panel alerts">
        <div className="head"><div><h3>Plant Health Alerts</h3><p>Recent sensor and automation events</p></div><Bell /></div>
        {alerts.length ? alerts.map((a) => (
          <div className="alert" key={a.alert_id}>
            <span><AlertTriangle size={16} /></span>
            <div><strong>{String(a.alert_type || "ALERT").replaceAll("_", " ")}</strong><p>{a.message}</p><small>{new Date(a.created_at).toLocaleString()}</small></div>
            {a.status === "ACTIVE" ? (
              <button className="primary alertAction" onClick={() => onAcknowledge(a.alert_id)}><CheckCircle2 size={15} /> Acknowledge</button>
            ) : (
              <i><CheckCircle2 size={16} /> {a.status === "ACKNOWLEDGED" ? "ACKNOWLEDGED" : "RESOLVED"}</i>
            )}
          </div>
        )) : <p className="empty">No plant alerts at the moment.</p>}
      </section>
      <footer>Cloud-Connected Smart Plant Care - Built by Vaidehi Deore</footer>
    </main>
  );
}
