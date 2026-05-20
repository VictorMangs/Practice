// fileIngestor.js

export function ingestFiles(files, onChunkReady) {
  let i = 0;
  const CHUNK_SIZE = 500; // tune for performance

  function processChunk() {
    const chunk = [];

    for (let j = 0; j < CHUNK_SIZE && i < files.length; j++, i++) {
      const file = files[i];

      chunk.push({
        id: crypto.randomUUID(),
        file,
        path: file.webkitRelativePath || file.name,
        size: file.size,
        name: file.name,
      });
    }

    onChunkReady(chunk);

    if (i < files.length) {
      requestIdleCallback(processChunk);
    }
  }

  requestIdleCallback(processChunk);
}