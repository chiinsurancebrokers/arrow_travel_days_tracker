import React from "react";

export default function EmployeeCard({ employee }) {
  const totalDays = employee.trips.reduce((sum, t) => sum + t.days, 0);
  const MAX_DAYS = 250;
  const remaining = MAX_DAYS - totalDays;

  return (
    <div className="bg-white rounded-xl shadow p-4 mb-4">
      <h3 className="text-lg font-bold">{employee.name}</h3>
      {employee.email && <p className="text-sm text-gray-500">📧 {employee.email}</p>}
      <p>Total Days Traveled: {totalDays}</p>
      <p>Days Remaining: {remaining}</p>
      <div className="mt-2">
        {employee.trips.map((trip, idx) => (
          <div key={idx} className="border p-2 rounded mb-1">
            <p>{trip.route} | {trip.dates} | {trip.days} days</p>
          </div>
        ))}
      </div>
    </div>
  );
}
