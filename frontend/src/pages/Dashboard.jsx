import React, { useEffect, useState } from "react";
import EmployeeCard from "../components/EmployeeCard";
import axios from "axios";

export default function Dashboard() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    axios.get("/api/employees")
      .then(res => setEmployees(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Arrow Travel Tracker Dashboard</h1>
      {employees.map(emp => (
        <EmployeeCard key={emp.name} employee={emp} />
      ))}
    </div>
  );
}
