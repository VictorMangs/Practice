// upload/fileIngestor.js

export function ingestFiles(fileList, onChunk) {
  let i = 0;
  const CHUNK_SIZE = 500;

  function process() {
    const chunk = [];

    for (let j = 0; j < CHUNK_SIZE && i < fileList.length; j++, i++) {
      const file = fileList[i];

      chunk.push({
        id: crypto.randomUUID(),
        file,
        name: file.name,

        // CRITICAL: preserves folder hierarchy
        relativePath: file.webkitRelativePath || file.name,

        size: file.size,
      });
    }

    onChunk(chunk);

    if (i < fileList.length) {
      requestIdleCallback(process);
    }
  }

  requestIdleCallback(process);
}