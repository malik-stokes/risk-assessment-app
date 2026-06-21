"use client";

import { useEffect, useState } from "react";

type Assessment = {
  id: number;
  zip_code: string;
  crime_count: number;
  storm_count: number;
  disaster_count: number;
  population: number;
  risk_score: number;
  risk_level: string;
  recommendation: string;
  created_at: string;
};

export default function HistoryPage() {
  const [history, setHistory] = useState<Assessment[]>([]);
  const [zipFilter, setZipFilter] = useState("");
  const [riskFilter, setRiskFilter] = useState("");
  const [loading, setLoading] = useState(true);

  // Get all history
  const fetchHistory = async () => {
    try {
      setLoading(true);

      const res = await fetch("http://127.0.0.1:8000/history");
      const data = await res.json();

      setHistory(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Delete one item
  const deleteItem = async (id: number) => {
    await fetch(`http://127.0.0.1:8000/history/${id}`, {
      method: "DELETE",
    });

    fetchHistory();
  };

  // Delete all items
  const deleteAll = async () => {
    const confirmDelete = confirm("Are you sure you want to delete all history?");

    if (!confirmDelete) return;

    await fetch("http://127.0.0.1:8000/history", {
      method: "DELETE",
    });

    fetchHistory();
  };

  // Refresh after delete
  useEffect(() => {
    fetchHistory();
  }, []);

  // Color helper for risk levels
  const getRiskColor = (level: string) => {
    if (level.includes("Low")) return "text-green-600 bg-green-100";
    if (level.includes("Moderate")) return "text-yellow-600 bg-yellow-100";
    if (level.includes("Elevated")) return "text-orange-600 bg-orange-100";
    return "text-red-600 bg-red-100";
  };

  // Search history
  const filteredHistory = history.filter((item) => {
  const matchesZip =
    item.zip_code.includes(zipFilter);

  const matchesRisk =
    riskFilter === "" ||
    item.risk_level === riskFilter;

  return matchesZip && matchesRisk;
  });

  return (
    <main className="min-h-screen bg-linear-to-b from-slate-50 to-slate-100 p-8">

      <div className="bg-white/60 backdrop-blur border border-slate-200 rounded-xl p-8 space-y-6">

      {/* Header */}
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">History</h1>
        </div>

        {/* Control Bar */}
        <div className="flex gap-4 flex-wrap pb-2">
          
          {/* ZIP filter */}
          <input
            type="text"
            placeholder="Filter by ZIP Code"
            value={zipFilter}
            onChange={(e) => setZipFilter(e.target.value)}
            className="border px-3 py-2 rounded"
          />

          {/* Risk filter */}
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="border px-3 py-2 rounded"
          >
            <option value="">All Risk Levels</option>
            <option value="Low Risk">Low Risk</option>
            <option value="Moderate Risk">Moderate Risk</option>
            <option value="Elevated Risk">Elevated Risk</option>
            <option value="High Risk">High Risk</option>
          </select>

          {/* Reset button */}
          <button
            onClick={() => {
              setZipFilter("");
              setRiskFilter("");
            }}
            className="bg-gray-200 px-3 py-2 rounded hover:bg-gray-300"
          >
            Reset
          </button>

          {/* Delete all button*/}
          <button
            onClick={deleteAll}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-800 transition"
          >
            Delete All
          </button>

        </div>

        {/* Cards */}
        <div className="grid gap-4 pt-2">
          {filteredHistory.map((item) => (
            <div
              key={item.id}
              className="bg-white/80 backdrop-blur border border-gray-100 shadow-md rounded-xl p-5 hover:shadow-xl transition"
            >
              {/* Top row */}
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-xl font-bold">ZIP: {item.zip_code}</h2>
                  <p className="text-sm text-gray-500">
                    {new Date(item.created_at).toLocaleString()}
                  </p>
                </div>

                {/* Risk badge */}
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(
                    item.risk_level
                  )}`}
                >
                  {item.risk_level}
                </span>
              </div>

              {/* Risk score */}
              <div className="mt-3">
                <p className="text-lg">
                  Risk Score:{" "}
                  <span className="font-bold">{item.risk_score}</span>
                </p>
              </div>

              {/* Details */}
              <div className="mt-2 text-sm text-gray-600 grid grid-cols-2 gap-2">
                <p>Crime: {item.crime_count}</p>
                <p>Storm: {item.storm_count}</p>
                <p>Disaster: {item.disaster_count}</p>
                <p>Population: {item.population}</p>
              </div>

              {/* Recommendation */}
              <div className="mt-3 text-sm italic text-gray-700">
                {item.recommendation}
              </div>
              {/* Delete button */}
              <div className="mt-4 flex justify-end">
                <button
                  onClick={() => deleteItem(item.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-400 transition"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}