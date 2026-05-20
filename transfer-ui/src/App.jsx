// App.jsx
import { useRef, useState } from "react";
import FileDrop from "./components/FileDrop";
import FileList from "./components/FileList";

import { createUploadStore } from "./upload/uploadStore";
import { ingestFiles } from "./upload/fileIngestor";
import { uploadQueue } from "./upload/uploader";
import { uploadFile } from "./upload/api";

function App() {
  const storeRef = useRef(createUploadStore());
  const [, forceRender] = useState(0);

  const handleFiles = (files) => {
    ingestFiles(files, (chunk) => {
      for (const item of chunk) {
        storeRef.current.files.set(item.id, item.file);
        storeRef.current.queue.push(item.id);
      }

      forceRender((x) => x + 1);
    });
  };

  const startTransfer = async () => {
    await uploadQueue({
      store: storeRef.current,
      concurrency: 5,

      uploadFn: (fileItem, onProgress) =>
        uploadFile(fileItem, onProgress, {
          user: "victor",
          mode: "Normal",
        }),

      onProgressUpdate: () => {
        forceRender((x) => x + 1);
      },
    });
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Transfer Tool</h2>

      <FileDrop onFiles={handleFiles} />

      <button onClick={startTransfer}>
        Start Transfer
      </button>

      <FileList store={storeRef.current} />
    </div>
  );
}

export default App;