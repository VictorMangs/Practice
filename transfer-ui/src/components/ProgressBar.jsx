// ProgressBar.jsx
export default function ProgressBar({ percent }) {
  return (
    <div style={{ border: "1px solid #ccc", width: "100%" }}>
      <div
        style={{
          width: `${percent}%`,
          background: "green",
          color: "white",
        }}
      >
        {percent}%
      </div>
    </div>
  );
}