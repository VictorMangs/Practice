// components/FileTree.jsx
function Node({ node }) {
  return (
    <li>
      {node.type === "directory" ? "📁" : "📄"} {node.name}

      {node.children?.length > 0 && (
        <ul style={{ paddingLeft: 20 }}>
          {node.children.map((child, i) => (
            <Node key={i} node={child} />
          ))}
        </ul>
      )}
    </li>
  );
}

export default function FileTree({ tree }) {
  return (
    <ul>
      {tree.map((node, i) => (
        <Node key={i} node={node} />
      ))}
    </ul>
  );
}