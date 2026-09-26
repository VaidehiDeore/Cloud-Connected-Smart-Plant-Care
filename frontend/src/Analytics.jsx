import React from "react";
import { Activity, BarChart3, Bell, CheckCircle2, Droplets, Leaf, LogOut, Settings2, Sprout, Thermometer, Waves } from "lucide-react";
import { Area, AreaChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function Analytics({ hist = [], events = [], latest, d, onBack, onAlerts, onOverview, onAnalytics, onLogout, alerts = [] }) {
  const chart = hist.map((x) => ({
    time: new Date(x.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    moisture: x.soil_moisture,
    temperature: x.temperature,
    humidity: x.humidity,
  }));

  const avgMoisture = hist.length ? (hist.reduce((a, x) => a + x.soil_moisture, 0) / hist.length).toFixed(1) : "-";
  const minMoisture = hist.length ? Math.min(...hist.map((x) => x.soil_moisture)).toFixed(1) : "-";
  const maxMoisture = hist.length ? Math.max(...hist.map((x) => x.soil_moisture)).toFixed(1) : "-";
  const avgTemperature = hist.length ? (hist.reduce((a, x) => a + x.temperature, 0) / hist.length).toFixed(1) : "-";

  return (
    <main>
      <header>
        <div><small>SMART PLANT / ANALYTICS</small><h1>Plant Analytics</h1></div>
        <button className="primary" onClick={onBack}>Back to Overview</button>
      </header>

      <section className="hero">
        <div><small>ANALYZING PLANT</small><h2>{d?.plant_name || "My Smart Plant"}</h2><p>{d?.plant_type || "Indoor Plant"} - {d?.location || "Home"} - {d?.device_id || "PLANT-001"}</p></div>
        <div className="plant"><Sprout size={74} /></div>
        <div className="sync"><small>DATA POINTS</small><strong>{hist.length}</strong><span>sensor readings</span></div>
      </section>

      <section className="stats">
        <div className="stat"><div className="statIcon"><Activity /></div><div><small>Average Moisture</small><strong>{avgMoisture}<i>%</i></strong></div></div>
        <div className="stat"><div className="statIcon"><Droplets /></div><div><small>Minimum Moisture</small><strong>{minMoisture}<i>%</i></strong></div></div>
        <div className="stat"><div className="statIcon"><Thermometer /></div><div><small>Average Temperature</small><strong>{avgTemperature}<i> C</i></strong></div></div>
        <div className="stat"><div className="statIcon"><Droplets /></div><div><small>Total Waterings</small><strong>{events.length}</strong></div></div>
      </section>

      <section className="grid">
        <div className="panel wide">
          <div className="head"><div><h3>Soil Moisture Analysis</h3><p>Historical moisture readings</p></div><span>{latest ? `${latest.soil_moisture.toFixed(0)}% now` : "No data"}</span></div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chart}>
              <defs><linearGradient id="analyticsMoisture" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#67a875" stopOpacity=".35" /><stop offset="100%" stopColor="#67a875" stopOpacity="0" /></linearGradient></defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5ebe5" />
              <XAxis dataKey="time" tickLine={false} axisLine={false} /><YAxis domain={[0, 100]} tickLine={false} axisLine={false} /><Tooltip />
              <Area type="monotone" dataKey="moisture" stroke="#4d9560" fill="url(#analyticsMoisture)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <div className="head"><div><h3>Moisture Range</h3><p>Recorded sensor range</p></div></div>
          <div className="metrics"><div><small>Minimum</small><strong>{minMoisture}%</strong></div><div><small>Average</small><strong>{avgMoisture}%</strong></div><div><small>Maximum</small><strong>{maxMoisture}%</strong></div></div>
        </div>
      </section>

      <section className="grid">
        <div className="panel wide">
          <div className="head"><div><h3>Environment Analysis</h3><p>Temperature and humidity over time</p></div></div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chart}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5ebe5" /><XAxis dataKey="time" tickLine={false} axisLine={false} /><YAxis tickLine={false} axisLine={false} /><Tooltip />
              <Line dataKey="temperature" name="Temperature" stroke="#d48b54" strokeWidth={2.5} dot={false} /><Line dataKey="humidity" name="Humidity" stroke="#6194c8" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <div className="head"><div><h3>Watering Summary</h3><p>Recent watering events</p></div><Droplets /></div>
          {events.length ? events.slice(0, 8).map((e) => (
            <div className="event" key={e.event_id}><Droplets /><div><strong>{e.trigger_type === "AUTO_THRESHOLD" ? "Automatic watering" : "Manual watering"}</strong><small>{new Date(e.timestamp).toLocaleString()}</small></div><span>{e.duration}s</span></div>
          )) : <p className="empty">No watering events yet.</p>}
        </div>
      </section>

      <section className="panel">
        <div className="head"><div><h3>Sensor Data Overview</h3><p>Latest available readings</p></div><Waves /></div>
        <div className="metrics"><div><small>Soil Moisture</small><strong>{latest ? `${latest.soil_moisture.toFixed(1)}%` : "-"}</strong></div><div><small>Temperature</small><strong>{latest ? `${latest.temperature.toFixed(1)} C` : "-"}</strong></div><div><small>Humidity</small><strong>{latest ? `${latest.humidity.toFixed(1)}%` : "-"}</strong></div><div><small>Light Level</small><strong>{latest ? `${latest.light_level.toFixed(1)}%` : "-"}</strong></div></div>
      </section>
      <footer>Cloud-Connected Smart Plant Care - Built by Vaidehi Deore</footer>
    </main>
  );
}
