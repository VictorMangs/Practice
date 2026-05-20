const path = require("path");

function buildTreeFromFiles(files, tempRoot) {
  const root = {};

  for (const file of files) {
    const relPath = file.originalnamePath;
    const parts = relPath.split("/");

    let current = root;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const isFile = i === parts.length - 1;

      if (!current[part]) {
        current[part] = isFile
          ? {
              type: "file",
              name: part,
              path: path.join(tempRoot, file.filename),
            }
          : {
              type: "directory",
              name: part,
              children: {},
            };
      }

      if (!isFile) {
        current = current[part].children;
      }
    }
  }

  return convertToArray(root);
}

function convertToArray(obj) {
  return Object.values(obj).map((node) => {
    if (node.type === "directory") {
      return {
        ...node,
        children: convertToArray(node.children),
      };
    }
    return node;
  });
}

module.exports = { buildTreeFromFiles };