"use client";

import { useState } from "react";

export default function Home() {
  const [zip, setZip] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchRisk = async () => {
    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/analyze/${zip}`);
      const result = await res.json();
      setData(result);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case "Low Risk":
        return "text-green-600";
      case "Moderate Risk":
        return "text-yellow-500";
      case "Elevated Risk":
        return "text-orange-500";
      case "High Risk":
        return "text-red-600";
      default:
        return "";
    }
  };

  return (
    <main className="min-h-screen bg-linear-to-b from-slate-50 to-slate-100 p-8">
      <div className="bg-white/70 border border-slate-200 rounded-xl p-8 shadow-sm">

        <h1 className="text-3xl font-bold mb-6">
          Dashboard
        </h1>

        <div className="flex gap-3 mb-8">
          <input
            type="text"
            placeholder="Enter ZIP Code"
            value={zip}
            onChange={(e) => setZip(e.target.value)}
            className="border rounded px-4 py-2 bg-white"
          />

          <button
            onClick={fetchRisk}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Analyze
          </button>
        </div>

        {loading && (
          <p className="text-lg">Loading...</p>
        )}

        {data && (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">

              <div className="bg-white p-5 rounded shadow">
                <h2 className="text-gray-500 text-sm">
                  Risk Score
                </h2>
                <p className="text-3xl font-bold">
                  {data.overall_risk_assessment.risk_score}
                </p>
              </div>

              <div className="bg-white p-5 rounded shadow">
                <h2 className="text-gray-500 text-sm">
                  Risk Level
                </h2>
                <p
                  className={`text-2xl font-bold ${getRiskColor(
                    data.overall_risk_assessment.risk_level
                  )}`}
                >
                  {data.overall_risk_assessment.risk_level}
                </p>
              </div>

              <div className="bg-white p-5 rounded shadow">
                <h2 className="text-gray-500 text-sm">
                  Recommendation
                </h2>
                <p className="font-medium">
                  {data.overall_risk_assessment.recommendation}
                </p>
              </div>

            </div>

            {/* Raw Data */}
            <div className="bg-white p-6 rounded shadow mb-8">

              <h2 className="text-2xl font-bold mb-4">
                Location Data
              </h2>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

                <div>
                  <p className="text-gray-500">Crime Count</p>
                  <p className="font-bold">
                    {data.raw_data.crime_count}
                  </p>
                </div>

                <div>
                  <p className="text-gray-500">Storm Count</p>
                  <p className="font-bold">
                    {data.raw_data.storm_count}
                  </p>
                </div>

                <div>
                  <p className="text-gray-500">Disaster Count</p>
                  <p className="font-bold">
                    {data.raw_data.disaster_count}
                  </p>
                </div>

                <div>
                  <p className="text-gray-500">Population</p>
                  <p className="font-bold">
                    {data.raw_data.population}
                  </p>
                </div>

              </div>

            </div>

            {/* Risk Factors */}
            <div className="bg-white p-6 rounded shadow">

              <h2 className="text-2xl font-bold mb-4">
                Risk Factors
              </h2>

              <pre className="overflow-auto text-sm leading-relaxed">
                {JSON.stringify(data.risk_factors, null, 2)}
              </pre>

            </div>
          </>
        )}
      </div>
    </main>
  );
}