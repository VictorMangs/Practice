// components/FileList.jsx

export default function FileList({ store }) {
  const entries = Array.from(store.files.entries());

  return (
    <div>
      <h3>Files</h3>

      <ul>
        {entries.map(([id, file]) => (
          <li key={id}>
            📄 {file.name} — {store.progress.get(id) || 0}%
          </li>
        ))}
      </ul>
    </div>
  );
}