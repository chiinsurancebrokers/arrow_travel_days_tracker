import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <nav className="bg-indigo-600 text-white px-6 py-3 flex gap-6">
      <Link to="/dashboard" className="hover:underline">Dashboard</Link>
      <Link to="/add-trip" className="hover:underline">Add Trip</Link>
      <Link to="/login" className="hover:underline ml-auto">Logout</Link>
    </nav>
  );
}
