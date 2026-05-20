// upload/uploadStore.js

export function createUploadStore() {
  return {
    transferId: null,
    files: new Map(),     // id → file
    queue: [],            // {id, path}
    progress: new Map(),  // id → %
  };
}