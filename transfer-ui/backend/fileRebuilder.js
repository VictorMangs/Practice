const path = require("path");
const fs = require("fs-extra");

/**
 * Rebuild uploaded folder structure directly on disk
 *
 * files: multer file list
 * tempRoot: where multer stored raw uploads
 * outputRoot: final destination root
 */
async function rebuildFolderStructure(files, tempRoot, outputRoot) {
  for (const file of files) {
    const relativePath = file.originalnamePath;

    if (!relativePath) continue;

    // Normalize for Windows/Linux compatibility
    const normalizedPath = relativePath.replace(/\//g, path.sep);

    const finalPath = path.join(outputRoot, normalizedPath);

    // Ensure directory exists
    await fs.ensureDir(path.dirname(finalPath));

    // Move file from temp → final structure
    await fs.move(
      path.join(tempRoot, file.filename),
      finalPath,
      { overwrite: true }
    );
  }
}

module.exports = { rebuildFolderStructure };