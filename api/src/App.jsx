// src/App.jsx
import React, { useEffect, useState } from "react";
import { Plane, Calendar, Award, TrendingUp } from "lucide-react";
import "./styles.css"; // add your tailwind or css

const PROXY_URL = "https://<your-vercel-app>.vercel.app/api/proxy"; // <-- replace this

const MAX_DAYS = 250;
const POLICY_START = "30/09/2025";

function sumTrips(trips) {
  return trips.reduce((s, t) => s + (Number(t.days) || 0), 0);
}

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(PROXY_URL)
      .then((r) => r.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-8">Loading...</div>;
  if (!data) return <div className="p-8">No data available.</div>;

  // data format produced by backend.compute_summary()
  // data.trips_by_employee is { name: [ {days,start,end,...}, ... ], ... }
  const employees = Object.entries(data.trips_by_employee).map(([name, trips]) => ({
    name,
    trips,
    totalDays: sumTrips(trips),
    email: trips.find(t => t.email)?.email || ""
  }));

  const totalDays = employees.reduce((s, e) => s + e.totalDays, 0);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3">
            <Plane className="w-10 h-10 text-indigo-600" />
            <h1 className="text-4xl font-bold">Arrow Travel Tracker</h1>
            <Plane className="w-10 h-10 text-indigo-600 transform scale-x-[-1]" />
          </div>
          <p className="text-sm text-gray-600 mt-2">Policy start: {POLICY_START} • Annual limit: {MAX_DAYS} days</p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <p className="text-sm text-gray-500">Total Employees</p>
            <h2 className="text-2xl font-bold">{employees.length}</h2>
          </div>
          <div className="card">
            <p className="text-sm text-gray-500">Total Days Traveled</p>
            <h2 className="text-2xl font-bold">{totalDays}</h2>
          </div>
          <div className="card">
            <p className="text-sm text-gray-500">Days Remaining (global)</p>
            <h2 className="text-2xl font-bold">{MAX_DAYS - totalDays}</h2>
          </div>
        </section>

        <section className="space-y-4">
          {employees.map((emp) => {
            const remaining = MAX_DAYS - emp.totalDays;
            const pct = (emp.totalDays / MAX_DAYS) * 100;
            return (
              <div key={emp.name} className="bg-white rounded-lg p-4 shadow">
                <div className="flex justify-between items-center mb-3">
                  <div>
                    <h3 className="text-lg font-semibold">{emp.name}</h3>
                    {emp.email && <p className="text-sm text-gray-500">📧 {emp.email}</p>}
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{emp.totalDays}</div>
                    <div className="text-sm text-gray-500">days traveled</div>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-indigo-600 h-3 rounded-full" style={{ width: `${Math.min(pct, 100)}%` }} />
                  </div>
                  <div className="text-xs text-gray-500 mt-1 text-right">{pct.toFixed(1)}% of limit used — {remaining} days left</div>
                </div>

                <div className="grid gap-2">
                  {emp.trips.map((t, i) => (
                    <div key={i} className="p-2 border rounded-sm bg-indigo-50">
                      <div className="flex justify-between">
                        <div>
                          <div className="font-medium">{t.route}</div>
                          <div className="text-sm text-gray-600">📅 {t.start} → {t.end}</div>
                        </div>
                        <div className="text-sm font-semibold bg-indigo-600 text-white px-2 py-1 rounded">{t.days} days</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </section>
      </div>
    </div>
  );
}
