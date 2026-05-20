// treeBuilder.js
export function buildTree(files) {
  const root = [];

  for (const file of files) {
    const parts = file.webkitRelativePath
      ? file.webkitRelativePath.split("/")
      : file.path.split("/");

    let currentLevel = root;

    parts.forEach((part, index) => {
      let existing = currentLevel.find((n) => n.name === part);

      if (!existing) {
        existing = {
          name: part,
          type: index === parts.length - 1 ? "file" : "directory",
          children: [],
          file: index === parts.length - 1 ? file : null,
          path: file.path || file.webkitRelativePath,
        };

        currentLevel.push(existing);
      }

      currentLevel = existing.children;
    });
  }

  return root;
}