import React, { useEffect, useState } from "react";
import {
  Bell,
  CheckCircle2,
  Droplets,
  Leaf,
  LogOut,
  RefreshCw,
  Settings2,
  Sprout,
  Sun,
  Thermometer,
  Waves,
  Wifi,
  WifiOff,
} from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import api, { setToken } from "./api";
import Analytics from "./Analytics";
import Alerts from "./Alerts";

function Auth({ done }) {
  const [reg, setReg] = useState(false);
  const [name, setName] = useState("Vaidehi");
  const [email, setEmail] = useState("vaidehi@example.com");
  const [pass, setPass] = useState("PlantCare@123");
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    setErr("");
    try {
      const payload = reg
        ? { name, email, password: pass }
        : { email, password: pass };
      const r = await api.post(reg ? "/auth/register" : "/auth/login", payload);
      localStorage.setItem("plant_token", r.data.access_token);
      setToken(r.data.access_token);
      done();
    } catch (x) {
      setErr(x.response?.data?.detail || "Authentication failed");
    }
  }

  return (
    <div className="auth">
      <div className="authCard">
        <div className="brand"><Leaf /></div>
        <small>CLOUD-CONNECTED IOT</small>
        <h1>Smart Plant Care</h1>
        <p>Monitor plant health, automate watering and explore sensor history.</p>
        <form onSubmit={submit}>
          {reg && (
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
          )}
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input value={pass} onChange={(e) => setPass(e.target.value)} placeholder="Password" type="password" />
          {err && <div className="error">{err}</div>}
          <button className="primary">{reg ? "Create account" : "Sign in"}</button>
        </form>
        <button className="link" onClick={() => setReg(!reg)}>
          {reg ? "Sign in" : "Create demo account"}
        </button>
      </div>
    </div>
  );
}

function Stat({ icon, label, value, unit }) {
  return (
    <div className="stat">
      <div className="statIcon">{icon}</div>
      <div>
        <small>{label}</small>
        <strong>{value}<i>{unit}</i></strong>
      </div>
    </div>
  );
}

function Sidebar({ page, setPage, alerts, logout }) {
  return (
    <aside>
      <div className="logo">
        <span><Leaf /></span>
        PlantCare
      </div>
      <small className="sideTitle">MONITORING</small>

      <button className={`nav ${page === "overview" ? "active" : ""}`} onClick={() => setPage("overview")}>
        <Sprout /> Overview
      </button>
      <button className={`nav ${page === "analytics" ? "active" : ""}`} onClick={() => setPage("analytics")}>
        <Waves /> Analytics
      </button>
      <button className={`nav ${page === "alerts" ? "active" : ""}`} onClick={() => setPage("alerts")}>
        <Bell /> Alerts
        <b>{alerts.filter((x) => x.status === "ACTIVE").length}</b>
      </button>

      <div className="grow" />
      <button className="nav" type="button"><Settings2 /> Settings</button>
      <button className="nav logout" onClick={logout}><LogOut /> Sign out</button>
    </aside>
  );
}

function Overview({ d, latest, hist, events, alerts, threshold, setThreshold, saveThreshold, water, load, toast, setToast }) {
  const chart = hist.map((x) => ({
    time: new Date(x.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    moisture: x.soil_moisture,
    temp: x.temperature,
    hum: x.humidity,
  }));

  const health = !latest
    ? "Waiting"
    : latest.soil_moisture < threshold
      ? "Needs Water"
      : latest.temperature > 38
        ? "High Temperature"
        : "Healthy";

  return (
    <main>
      <header>
        <div>
          <small>SMART PLANT / OVERVIEW</small>
          <h1>Good evening, Vaidehi</h1>
        </div>
        <div className="actions">
          <span className={d?.status === "ONLINE" ? "online" : "offline"}>
            {d?.status === "ONLINE" ? <Wifi /> : <WifiOff />}
            {d?.status || "CONNECTING"}
          </span>
          <button onClick={load} title="Refresh"><RefreshCw /></button>
        </div>
      </header>

      {toast && <div className="toast" onClick={() => setToast("")}>{toast}</div>}

      <section className="hero">
        <div>
          <small>YOUR PLANT</small>
          <h2>{d?.plant_name || "My Smart Plant"}</h2>
          <p>{d?.plant_type || "Indoor Plant"} - {d?.location || "Home"} - {d?.device_id || "PLANT-001"}</p>
          <em className={health === "Healthy" ? "good" : health === "Needs Water" ? "warn" : "bad"}>
            {health}
          </em>
        </div>
        <div className="plant"><Sprout size={74} /></div>
        <div className="sync">
          <small>CLOUD SYNC</small>
          <strong>{d?.status === "ONLINE" ? "Live" : "Offline"}</strong>
          <span>{latest ? new Date(latest.timestamp).toLocaleTimeString() : "No reading"}</span>
        </div>
      </section>

      <section className="stats">
        <Stat icon={<Droplets />} label="Soil Moisture" value={latest ? latest.soil_moisture.toFixed(0) : "-"} unit="%" />
        <Stat icon={<Thermometer />} label="Temperature" value={latest ? latest.temperature.toFixed(1) : "-"} unit=" C" />
        <Stat icon={<Waves />} label="Humidity" value={latest ? latest.humidity.toFixed(0) : "-"} unit="%" />
        <Stat icon={<Sun />} label="Light Level" value={latest ? latest.light_level.toFixed(0) : "-"} unit="%" />
      </section>

      <section className="grid">
        <div className="panel wide">
          <div className="head">
            <div><h3>Soil moisture</h3><p>Live virtual sensor trend</p></div>
            <span>{latest ? `${latest.soil_moisture.toFixed(0)}% now` : "No data"}</span>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={chart}>
              <defs>
                <linearGradient id="moistureFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#67a875" stopOpacity=".35" />
                  <stop offset="100%" stopColor="#67a875" stopOpacity="0" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5ebe5" />
              <XAxis dataKey="time" tickLine={false} axisLine={false} />
              <YAxis domain={[0, 100]} tickLine={false} axisLine={false} />
              <Tooltip />
              <Area type="monotone" dataKey="moisture" stroke="#4d9560" fill="url(#moistureFill)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="head"><div><h3>Watering control</h3><p>Automation and actuator</p></div></div>
          <div className="pump">
            <Droplets />
            <div><small>PUMP STATUS</small><strong>{d?.pump_on ? "ON" : "OFF"}</strong></div>
          </div>
          <button className="primary full" onClick={water}><Droplets /> Water now</button>
          <div className="threshold">
            <label>Moisture threshold <strong>{threshold}%</strong></label>
            <input
              type="range"
              min="10"
              max="70"
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              onMouseUp={saveThreshold}
            />
          </div>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <div className="head"><div><h3>Environment</h3><p>Temperature and humidity</p></div></div>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={chart}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5ebe5" />
              <XAxis dataKey="time" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} />
              <Tooltip />
              <Line dataKey="temp" name="Temperature" stroke="#d48b54" strokeWidth={2.5} dot={false} />
              <Line dataKey="hum" name="Humidity" stroke="#6194c8" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="head"><div><h3>Watering history</h3><p>Recent events</p></div></div>
          {events.length ? events.slice(0, 6).map((e) => (
            <div className="event" key={e.event_id}>
              <Droplets />
              <div>
                <strong>{e.trigger_type === "AUTO_THRESHOLD" ? "Automatic watering" : "Manual watering"}</strong>
                <small>{new Date(e.timestamp).toLocaleString()}</small>
              </div>
              <span>{e.duration}s</span>
            </div>
          )) : <p className="empty">No watering events yet.</p>}
        </div>
      </section>

      <section className="metrics">
        <div><small>Average moisture</small><strong>{hist.length ? `${(hist.reduce((a, x) => a + x.soil_moisture, 0) / hist.length).toFixed(1)}%` : "-"}</strong></div>
        <div><small>Min moisture</small><strong>{hist.length ? `${Math.min(...hist.map((x) => x.soil_moisture)).toFixed(0)}%` : "-"}</strong></div>
        <div><small>Waterings</small><strong>{events.length}</strong></div>
        <div><small>Avg temperature</small><strong>{hist.length ? `${(hist.reduce((a, x) => a + x.temperature, 0) / hist.length).toFixed(1)} C` : "-"}</strong></div>
      </section>

      <footer>Cloud-Connected Smart Plant Care - Built by Vaidehi Deore</footer>
    </main>
  );
}

export default function App() {
  const [tokenState, setTokenState] = useState(Boolean(localStorage.getItem("plant_token")));
  const [page, setPage] = useState("overview");
  const [d, setD] = useState(null);
  const [latest, setLatest] = useState(null);
  const [hist, setHist] = useState([]);
  const [events, setEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [threshold, setThreshold] = useState(30);
  const [toast, setToast] = useState("");

  useEffect(() => {
    const t = localStorage.getItem("plant_token");
    if (t) setToken(t);
  }, []);

  async function load() {
    if (!tokenState) return;
    try {
      let ds = (await api.get("/devices")).data;
      if (!ds.length) {
        ds = [(await api.post("/devices", {
          device_id: "PLANT-001",
          plant_name: "My Smart Plant",
          plant_type: "Indoor Plant",
          location: "Home",
          moisture_threshold: 30,
          water_tank_level: 100,
        })).data];
      }
      const x = ds[0];
      setD(x);
      setThreshold(x.moisture_threshold);
      const [a, b, c, e] = await Promise.all([
        api.get(`/devices/${x.device_id}/latest`),
        api.get(`/devices/${x.device_id}/history?limit=100`),
        api.get(`/devices/${x.device_id}/watering-history`),
        api.get("/alerts"),
      ]);
      setLatest(a.data);
      setHist(b.data);
      setEvents(c.data);
      setAlerts(e.data);
    } catch (e) {
      if (e.response?.status === 401) logout();
      else setToast("Could not load backend data");
    }
  }

  useEffect(() => { load(); }, [tokenState]);
  useEffect(() => {
    if (!tokenState) return undefined;
    const i = setInterval(load, 5000);
    return () => clearInterval(i);
  }, [tokenState]);

  function logout() {
    localStorage.removeItem("plant_token");
    setToken(null);
    setTokenState(false);
  }

  async function water() {
    try {
      await api.post(`/devices/${d.device_id}/water`, { duration_seconds: 5 });
      setToast("Watering action completed");
      load();
    } catch {
      setToast("Watering failed");
    }
  }

  async function saveThreshold() {
    try {
      await api.put(`/devices/${d.device_id}/threshold`, { moisture_threshold: Number(threshold) });
      setToast("Threshold saved");
      load();
    } catch {
      setToast("Threshold update failed");
    }
  }

  async function ack(id) {
    try {
      await api.put(`/alerts/${id}/acknowledge`);
      setToast("Alert acknowledged");
      load();
    } catch {
      setToast("Could not acknowledge alert");
    }
  }

  if (!tokenState) return <Auth done={() => setTokenState(true)} />;

  const common = {
    alerts,
    onOverview: () => setPage("overview"),
    onAnalytics: () => setPage("analytics"),
    onAlerts: () => setPage("alerts"),
    onLogout: logout,
  };

  return (
    <div className="layout">
      <Sidebar page={page} setPage={setPage} alerts={alerts} logout={logout} />
      {page === "overview" && (
        <Overview
          d={d}
          latest={latest}
          hist={hist}
          events={events}
          alerts={alerts}
          threshold={threshold}
          setThreshold={setThreshold}
          saveThreshold={saveThreshold}
          water={water}
          load={load}
          toast={toast}
          setToast={setToast}
        />
      )}
      {page === "analytics" && (
        <Analytics
          hist={hist}
          events={events}
          latest={latest}
          d={d}
          onBack={() => setPage("overview")}
          onAlerts={() => setPage("alerts")}
          onOverview={() => setPage("overview")}
          onAnalytics={() => setPage("analytics")}
          onLogout={logout}
        />
      )}
      {page === "alerts" && (
        <Alerts
          alerts={alerts}
          onBack={() => setPage("overview")}
          onOverview={() => setPage("overview")}
          onAnalytics={() => setPage("analytics")}
          onLogout={logout}
          onAcknowledge={ack}
        />
      )}
    </div>
  );
}
