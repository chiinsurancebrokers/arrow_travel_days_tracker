import React, { useState } from "react";
import axios from "axios";

export default function AddTrip() {
  const [employee, setEmployee] = useState("");
  const [trip, setTrip] = useState({ days: "", dates: "", route: "" });

  const handleSubmit = () => {
    if(!employee || !trip.days || !trip.dates || !trip.route) return;

    axios.post("/api/add-trip", { employee, trip })
      .then(res => alert("Trip added successfully"))
      .catch(err => alert("Error adding trip"));
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Add New Trip</h1>
      <input placeholder="Employee Name" className="border p-2 mb-2" 
             value={employee} onChange={e => setEmployee(e.target.value)} />
      <input placeholder="Days" className="border p-2 mb-2"
             value={trip.days} onChange={e => setTrip({...trip, days: e.target.value})} />
      <input placeholder="Dates" className="border p-2 mb-2"
             value={trip.dates} onChange={e => setTrip({...trip, dates: e.target.value})} />
      <input placeholder="Route" className="border p-2 mb-2"
             value={trip.route} onChange={e => setTrip({...trip, route: e.target.value})} />
      <button className="bg-green-600 text-white px-4 py-2 rounded" onClick={handleSubmit}>Add Trip</button>
    </div>
  );
}
