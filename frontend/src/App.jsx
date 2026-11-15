import { useEffect, useState } from "react";
import TamilNaduMap from "./components/TamilNaduMap.jsx";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";

const navItems = [
  { id: "overview", icon: "◫", label: "Overview" },
  { id: "map", icon: "⌖", label: "Climate Map" },
  { id: "districts", icon: "▦", label: "District Analysis" },
  { id: "comparison", icon: "⇄", label: "Compare Districts" },
  { id: "trends", icon: "⌁", label: "Temperature Trends" },
];

const monthNames = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

function App() {
  const [active, setActive] = useState("overview");
  const [districts, setDistricts] = useState([]);
  const [coverage, setCoverage] = useState(null);
  const [selected, setSelected] = useState("Coimbatore");
  const [compare, setCompare] = useState("Chennai");
  const [apiStatus, setApiStatus] = useState("Connecting");

  const [annualData, setAnnualData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [compareData, setCompareData] = useState([]);
  const [trendLoading, setTrendLoading] = useState(false);
  const [trendError, setTrendError] = useState("");

  // Load district list and dataset coverage.
  useEffect(() => {
    async function loadData() {
      try {
        const [districtResponse, coverageResponse] = await Promise.all([
          fetch(`${API}/api/districts/`),
          fetch(`${API}/api/coverage/`),
        ]);

        if (!districtResponse.ok || !coverageResponse.ok) {
          throw new Error("API request failed");
        }

        const districtData = await districtResponse.json();
        const coverageData = await coverageResponse.json();
        const districtList = districtData.districts || [];

        setDistricts(districtList);
        setCoverage(coverageData);
        setApiStatus("Connected");

        if (districtList.length > 0) {
          setSelected((current) =>
            districtList.includes(current) ? current : districtList[0]
          );

          setCompare((current) =>
            districtList.includes(current)
              ? current
              : districtList[Math.min(1, districtList.length - 1)]
          );
        }
      } catch (error) {
        console.error("Dashboard loading error:", error);
        setApiStatus("Offline");
      }
    }

    loadData();
  }, []);

  // Load annual and monthly trends for the selected district.
  useEffect(() => {
    if (!selected) return;

    let cancelled = false;

    async function loadTrends() {
      setTrendLoading(true);
      setTrendError("");

      try {
        const [annualResponse, monthlyResponse] = await Promise.all([
          fetch(`${API}/api/trends/${encodeURIComponent(selected)}/annual`),
          fetch(`${API}/api/trends/${encodeURIComponent(selected)}/monthly`),
        ]);

        if (!annualResponse.ok || !monthlyResponse.ok) {
          throw new Error("Could not load climate trends for this district.");
        }

        const annual = await annualResponse.json();
        const monthly = await monthlyResponse.json();

        if (!cancelled) {
          setAnnualData(annual.records || []);
          setMonthlyData(monthly.records || []);
        }
      } catch (error) {
        if (!cancelled) {
          setAnnualData([]);
          setMonthlyData([]);
          setTrendError(error.message);
        }
      } finally {
        if (!cancelled) setTrendLoading(false);
      }
    }

    loadTrends();

    return () => {
      cancelled = true;
    };
  }, [selected]);

  // Load annual data for the second district in the comparison.
  useEffect(() => {
    if (!selected || !compare || selected === compare) {
      setCompareData([]);
      return;
    }

    let cancelled = false;

    async function loadComparison() {
      try {
        const [firstResponse, secondResponse] = await Promise.all([
          fetch(`${API}/api/trends/${encodeURIComponent(selected)}/annual`),
          fetch(`${API}/api/trends/${encodeURIComponent(compare)}/annual`),
        ]);

        if (!firstResponse.ok || !secondResponse.ok) {
          throw new Error("Comparison data unavailable");
        }

        const [first, second] = await Promise.all([
          firstResponse.json(),
          secondResponse.json(),
        ]);

        if (cancelled) return;

        const secondByYear = new Map(
          (second.records || []).map((item) => [item.year, item.annual_temperature_c])
        );

        const combined = (first.records || []).map((item) => ({
          year: item.year,
          [selected]: item.annual_temperature_c,
          [compare]: secondByYear.get(item.year) ?? null,
        }));

        setCompareData(combined);
      } catch (error) {
        console.error("Comparison loading error:", error);
        if (!cancelled) setCompareData([]);
      }
    }

    loadComparison();

    return () => {
      cancelled = true;
    };
  }, [selected, compare]);

  const scrollTo = (id) => {
    setActive(id);
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">T</div>
          <div>
            <h2>TerraTrend</h2>
            <span>CLIMATE INTELLIGENCE</span>
          </div>
        </div>

        <div className="nav-heading">WORKSPACE</div>

        <nav>
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-link ${active === item.id ? "active" : ""}`}
              onClick={() => scrollTo(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-card">
            <span className="status-dot" />
            <div>
              <strong>NASA Data Platform</strong>
              <p>TerraTrend Analytics</p>
            </div>
          </div>
          <div className="sidebar-footer">NASA SPACE APPS CHALLENGE 2026</div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="breadcrumb">Workspace / Climate Analytics</div>
            <h3>Tamil Nadu Climate Dashboard</h3>
          </div>

          <div className="topbar-right">
            <span className={`connection ${apiStatus === "Connected" ? "online" : ""}`}>
              <span className="status-dot" />
              {apiStatus === "Connected" ? "API Connected" : apiStatus}
            </span>
            <div className="profile">TT</div>
          </div>
        </header>

        <div className="dashboard">
          {/* OVERVIEW */}
          <section id="overview" className="section">
            <div className="welcome-row">
              <div>
                <span className="eyebrow">CLIMATE OVERVIEW</span>
                <h1>Understanding Tamil Nadu's Climate</h1>
                <p className="subtitle">
                  Explore temperature patterns, district-level changes and
                  long-term climate trends.
                </p>
              </div>
              <div className="period-pill">2001 — 2020 ANALYSIS</div>
            </div>

            <div className="stats-grid">
              <article className="stat-card">
                <div className="stat-top">
                  <span>STATE</span>
                  <span className="stat-icon">⌖</span>
                </div>
                <h2>Tamil Nadu</h2>
                <p>Study region</p>
              </article>

              <article className="stat-card">
                <div className="stat-top">
                  <span>DISTRICTS</span>
                  <span className="stat-icon">▦</span>
                </div>
                <h2>{districts.length || "—"} <small>/ 38</small></h2>
                <p>Districts in current analysis</p>
              </article>

              <article className="stat-card">
                <div className="stat-top">
                  <span>TIME PERIOD</span>
                  <span className="stat-icon">◷</span>
                </div>
                <h2>20 Years</h2>
                <p>2001 to 2020</p>
              </article>

              <article className="stat-card">
                <div className="stat-top">
                  <span>DATA SOURCE</span>
                  <span className="stat-icon">✧</span>
                </div>
                <h2>MERRA-2</h2>
                <p>NASA atmospheric data</p>
              </article>
            </div>
          </section>

          {/* CLIMATE MAP */}
<section id="map" className="section">
  <div className="section-heading">
    <div>
      <span className="eyebrow">GEOGRAPHICAL EXPLORER</span>
      <h2>Explore Climate by Location</h2>
      <p>Select a district to explore its climate information.</p>
    </div>
    <span className="coming-tag">INTERACTIVE MAP</span>
  </div>

  <div className="map-layout">
    <div className="map-placeholder">
     <TamilNaduMap
  selectedDistrict={selected}
  onDistrictSelect={setSelected}
/>
    </div>

    <div className="map-details">
      <span className="eyebrow">DISTRICT EXPLORER</span>
      <h3>Select a District</h3>

      <select
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
      >
        {districts.map((district) => (
          <option key={district} value={district}>
            {district}
          </option>
        ))}
      </select>

      <div className="detail-divider" />

      <p className="muted-label">SELECTED LOCATION</p>
      <h2>{selected}</h2>

      <p className="detail-note">
        Select a district to update the annual and monthly
        temperature charts.
      </p>

      <button
        className="primary-button"
        onClick={() => scrollTo("trends")}
      >
        View Temperature Trends →
      </button>
    </div>
  </div>
</section>

          {/* DISTRICT ANALYSIS */}
          <section id="districts" className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">DISTRICT INTELLIGENCE</span>
                <h2>District-wise Climate Analysis</h2>
                <p>Explore the districts currently included in the analysis.</p>
              </div>
            </div>

            <div className="district-grid">
              {districts.map((district, index) => (
                <button
                  key={district}
                  className={`district-card ${selected === district ? "selected" : ""}`}
                  onClick={() => {
                    setSelected(district);
                    scrollTo("trends");
                  }}
                >
                  <span className="district-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <strong>{district}</strong>
                  <span className="district-arrow">↗</span>
                </button>
              ))}

              {districts.length === 0 && (
                <p className="empty-message">
                  {apiStatus === "Offline"
                    ? "Backend unavailable. Start the FastAPI server to load districts."
                    : "Loading district information..."}
                </p>
              )}
            </div>
          </section>

          {/* DISTRICT COMPARISON */}
          <section id="comparison" className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">SIDE-BY-SIDE ANALYSIS</span>
                <h2>Compare Districts</h2>
                <p>Compare annual average temperatures between two districts.</p>
              </div>
            </div>

            <div className="compare-panel">
              <div className="compare-select">
                <label>FIRST DISTRICT</label>
                <select
                  value={selected}
                  onChange={(e) => setSelected(e.target.value)}
                >
                  {districts.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>

              <div className="versus">VS</div>

              <div className="compare-select">
                <label>SECOND DISTRICT</label>
                <select
                  value={compare}
                  onChange={(e) => setCompare(e.target.value)}
                >
                  {districts.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>

              <div className="compare-result">
                {selected === compare
                  ? "Choose two different districts to compare."
                  : `${selected}  ↔  ${compare}`}
              </div>

              {selected !== compare && compareData.length > 0 && (
                <div className="real-chart">
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={compareData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#263849" />
                      <XAxis dataKey="year" stroke="#9aabba" />
                      <YAxis
                        stroke="#9aabba"
                        domain={["auto", "auto"]}
                        tickFormatter={(value) => `${value.toFixed(1)}°`}
                      />
                      <Tooltip
                        contentStyle={{
                          background: "#142333",
                          border: "1px solid #34495b",
                          borderRadius: "8px",
                        }}
                        formatter={(value) =>
                          value == null ? "No data" : `${Number(value).toFixed(2)} °C`
                        }
                      />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey={selected}
                        name={selected}
                        stroke="#27c5b8"
                        strokeWidth={2.5}
                        dot={false}
                        connectNulls
                      />
                      <Line
                        type="monotone"
                        dataKey={compare}
                        name={compare}
                        stroke="#f2a65a"
                        strokeWidth={2.5}
                        dot={false}
                        connectNulls
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              {selected !== compare && compareData.length === 0 && (
                <p className="detail-note">
                  Loading comparison data or data is unavailable.
                </p>
              )}
            </div>
          </section>

          {/* TEMPERATURE TRENDS */}
          <section id="trends" className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">HISTORICAL CLIMATE</span>
                <h2>Temperature Trends</h2>
                <p>
                  Historical temperature analysis for {selected}, from 2001
                  to 2020.
                </p>
              </div>
              <span className="period-pill">2001 — 2020</span>
            </div>

            <div className="map-details trend-district-select">
              <label htmlFor="trend-district">SELECT DISTRICT</label>
              <select
                id="trend-district"
                value={selected}
                onChange={(e) => setSelected(e.target.value)}
              >
                {districts.map((district) => (
                  <option key={district} value={district}>{district}</option>
                ))}
              </select>
            </div>

            {trendLoading && (
              <p className="detail-note">Loading temperature data...</p>
            )}

            {trendError && (
              <p className="empty-message">{trendError}</p>
            )}

            <div className="chart-grid">
              <div className="chart-card">
                <h3>Annual Temperature — {selected}</h3>
                <p>Yearly average temperature (°C)</p>

                {annualData.length > 0 ? (
                  <div className="real-chart">
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={annualData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#263849" />
                        <XAxis dataKey="year" stroke="#9aabba" />
                        <YAxis
                          stroke="#9aabba"
                          domain={["auto", "auto"]}
                          tickFormatter={(value) => `${value.toFixed(1)}°`}
                        />
                        <Tooltip
                          contentStyle={{
                            background: "#142333",
                            border: "1px solid #34495b",
                            borderRadius: "8px",
                          }}
                          formatter={(value) => `${Number(value).toFixed(2)} °C`}
                        />
                        <Line
                          type="monotone"
                          dataKey="annual_temperature_c"
                          name="Annual temperature"
                          stroke="#27c5b8"
                          strokeWidth={3}
                          dot={{ r: 3 }}
                          activeDot={{ r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <div className="chart-empty">
                    <span>⌁</span>
                    <strong>Annual chart awaiting data</strong>
                    <small>
                      {trendLoading ? "Loading..." : "No annual records available."}
                    </small>
                  </div>
                )}
              </div>

              <div className="chart-card">
                <h3>Monthly Climate Pattern — {selected}</h3>
                <p>Average temperature by month (°C)</p>

                {monthlyData.length > 0 ? (
                  <div className="real-chart">
                   <ResponsiveContainer width="100%" height={300}>
  <BarChart
    data={monthlyData.map((item) => ({
      ...item,
      monthName: monthNames[item.month - 1],
    }))}
  >
    <CartesianGrid strokeDasharray="3 3" stroke="#263849" />

    <XAxis dataKey="monthName" stroke="#9aabba" />

    <YAxis
      stroke="#9aabba"
      domain={["auto", "auto"]}
      tickFormatter={(value) => `${value.toFixed(1)}°`}
    />

    <Tooltip
      contentStyle={{
        background: "#142333",
        border: "1px solid #34495b",
        borderRadius: "8px",
      }}
      formatter={(value) => `${Number(value).toFixed(2)} °C`}
    />

    <Bar
      dataKey="mean_temperature_c"
      name="Monthly temperature"
      fill="#27c5b8"
      radius={[5, 5, 0, 0]}
    />
  </BarChart>
</ResponsiveContainer>
                    
                  </div>
                ) : (
                  <div className="chart-empty">
                    <span>⌁</span>
                    <strong>Annual chart awaiting data</strong>
                    <small>
                      {trendLoading ? "Loading..." : "No annual records available."}
                    </small>
                  </div>
                )}
</div>

              <div className="chart-card">
                <h3>Monthly Climate Pattern — {selected}</h3>
                <p>Average temperature by month (°C)</p>

                {monthlyData.length > 0 ? (
                  <div className="real-chart">
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart
                        data={monthlyData.map((item) => ({
                          ...item,
                          monthName: monthNames[item.month - 1],
                        }))}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="#263849" />
                        <XAxis dataKey="monthName" stroke="#9aabba" />
                        <YAxis
                          stroke="#9aabba"
                          domain={["auto", "auto"]}
                          tickFormatter={(value) => `${value.toFixed(1)}°`}
                        />
                        <Tooltip
                          contentStyle={{
                            background: "#142333",
                            border: "1px solid #34495b",
                            borderRadius: "8px",
                          }}
                          formatter={(value) => `${Number(value).toFixed(2)} °C`}
                        />
                        <Bar
                          dataKey="mean_temperature_c"
                          name="Mean temperature"
                          fill="#27c5b8"
                          radius={[5, 5, 0, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
<div className="chart-empty">
                    <span>▥</span>
                    <strong>Monthly chart awaiting data</strong>
                    <small>
                      {trendLoading ? "Loading..." : "No monthly records available."}
                    </small>
                  </div>
                )}
              </div>
            </div>

            <p className="coverage-note">
              Source: NASA MERRA-2. Values represent processed climate data,
              not direct weather-station measurements.
            </p>
          </section>

          {/* DATASET COVERAGE */}
          <section className="sectioncoverage-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">DATA TRANSPARENCY</span>
                <h2>Dataset Coverage</h2>
                <p>Current verification status from the backend.</p>
              </div>
            </div>

            <div className="coverage-card">
              <div>
                <span className="muted-label">TEMPERATURE</span>
                <h3>NASA MERRA-2</h3>
              </div>
              <span className="coverage-status">
                {coverage?.datasets?.find((d) => d.variable === "temperature")
                  ?.status || "Checking"}</span>

              <div>
                <span className="muted-label">PRECIPITATION</span>
                <h3>NASA GPM IMERG</h3>
              </div>
              <span className="coverage-status">
                {coverage?.datasets?.find((d) => d.variable === "precipitation")
                  ?.status || "Checking"}
              </span>

              <p className="coverage-note">
                {coverage?.message || "Waiting for backend coverage information."}
              </p>
            </div>
          </section>

          <footer>
            <span>TerraTrend © 2026</span>  <span>NASA Space Apps Challenge 2026 · Tamil Nadu</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;