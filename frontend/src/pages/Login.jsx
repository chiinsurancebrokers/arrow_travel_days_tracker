import React from "react";

export default function Login() {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Sign In</h1>
      <input className="border p-2 mb-2" placeholder="Email" />
      <input className="border p-2 mb-2" placeholder="Password" type="password" />
      <button className="bg-indigo-600 text-white px-4 py-2 rounded">Login</button>
    </div>
  );
}
