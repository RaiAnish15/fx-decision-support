type RateRow = {
  pair: string;
  date: string;
  rate: number;
};

export default async function Home() {
  const healthRes = await fetch("http://127.0.0.1:8000/api/health/", {
    cache: "no-store",
  });
  const health = await healthRes.json();

  const ratesRes = await fetch("http://127.0.0.1:8000/api/rates/", {
    cache: "no-store",
  });
  const rates: RateRow[] = await ratesRes.json();

  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700 }}>FX Decision Support</h1>

      <p style={{ marginTop: 12, fontSize: 16 }}>
        Backend status: <b>{health.status}</b>
      </p>

      <h2 style={{ marginTop: 24, fontSize: 20, fontWeight: 700 }}>
        Latest stored FX rates
      </h2>

      <table
        style={{
          marginTop: 12,
          borderCollapse: "collapse",
          width: "100%",
          maxWidth: 720,
        }}
      >
        <thead>
          <tr>
            <th style={thStyle}>Pair</th>
            <th style={thStyle}>Date</th>
            <th style={thStyle}>Rate</th>
          </tr>
        </thead>
        <tbody>
          {rates.slice(0, 20).map((r, i) => (
            <tr key={`${r.pair}-${r.date}-${i}`}>
              <td style={tdStyle}>{r.pair}</td>
              <td style={tdStyle}>{r.date}</td>
              <td style={tdStyle}>{r.rate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

const thStyle: React.CSSProperties = {
  textAlign: "left",
  borderBottom: "1px solid #ddd",
  padding: "8px 10px",
};

const tdStyle: React.CSSProperties = {
  borderBottom: "1px solid #eee",
  padding: "8px 10px",
};
