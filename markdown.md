You’re not “porting a GUI,” you’re **re-architecting a stateful desktop workflow into a client/server web system**. If you try to translate this line-for-line, you’ll end up with a brittle mess. The correct approach is to **separate concerns** and rebuild around a web-native model.

Below is a **practical blueprint + starter implementation** that preserves functionality while modernizing the design.

---

# 🧠 Target Architecture (What This Should Become)

```text
[ React (Vite) Frontend ]
        ↓ (HTTP / JSON)
[ Backend API (Node.js / Express or Python/FastAPI) ]
        ↓
[ File System + Network Shares ]
        ↓
[ CSV Logging / Validation Engine ]
```

---

# 🔄 Mapping: PowerShell → Web

| PowerShell Concept          | React Equivalent                 |
| --------------------------- | -------------------------------- |
| TreeView                    | Recursive component (`FileTree`) |
| Drag & Drop                 | `react-dropzone`                 |
| Icons (Error/Warning/Cyber) | UI badges/icons                  |
| Validation                  | Backend API                      |
| Copy-Item                   | Backend file service             |
| MessageBox                  | Modal / Toast                    |
| Global `$script:` vars      | React state / context            |

---

# ⚠️ Critical Design Decision

👉 **Do NOT validate or copy files in React**

Why:

* Browser cannot access network shares like `\\DropBox\...`
* Security model prevents it
* You’d leak business logic

✔️ React = UI only
✔️ Backend = validation + transfer + logging

---

# 🧩 Core Features We Must Preserve

* Drag/drop files & folders
* Tree visualization
* File validation (Regular / Cyber / Unknown)
* Blocking rules:

  * Unknown → hard block
  * Cyber-only → requires Cyber mode
* Transfer routing:

  * Uploads vs Cyber
* Backup creation
* Logging (CSV)
* User identity (auto + manual override)

---

# 🚀 Frontend (React + Vite)

## 1. Project Setup

```bash
npm create vite@latest transfer-ui
cd transfer-ui
npm install
npm install react-dropzone axios
```

---

## 2. App Structure

```text
src/
 ├── components/
 │    ├── FileDrop.jsx
 │    ├── FileTree.jsx
 │    ├── Controls.jsx
 │    └── UserForm.jsx
 ├── services/api.js
 ├── App.jsx
 └── main.jsx
```

---

## 3. API Service

```javascript
// src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:3000/api",
});

export const validateFiles = (files) =>
  api.post("/validate", files);

export const transferFiles = (payload) =>
  api.post("/transfer", payload);

export default api;
```

---

## 4. Drag & Drop

```javascript
// FileDrop.jsx
import { useDropzone } from "react-dropzone";

export default function FileDrop({ onFiles }) {
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      onFiles(acceptedFiles);
    },
  });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      <p>Drag & drop files or folders here</p>
    </div>
  );
}
```

---

## 5. File Tree (Core Replacement for TreeView)

```javascript
// FileTree.jsx
function FileNode({ node }) {
  const getIcon = () => {
    switch (node.type) {
      case "error": return "❌";
      case "warning": return "⚠️";
      case "cyber": return "🛡";
      default: return "📄";
    }
  };

  return (
    <li>
      {getIcon()} {node.name}
      {node.children && (
        <ul>
          {node.children.map((child, i) => (
            <FileNode key={i} node={child} />
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
        <FileNode key={i} node={node} />
      ))}
    </ul>
  );
}
```

---

## 6. Main App Logic

```javascript
// App.jsx
import { useState } from "react";
import FileDrop from "./components/FileDrop";
import FileTree from "./components/FileTree";
import { validateFiles, transferFiles } from "./services/api";

function App() {
  const [tree, setTree] = useState([]);
  const [validation, setValidation] = useState([]);
  const [transferMode, setTransferMode] = useState("Normal");

  const handleFiles = async (files) => {
    const res = await validateFiles(files);
    setTree(res.data.tree);
    setValidation(res.data.summary);
  };

  const handleTransfer = async () => {
    const hasUnknown = validation.some(f => f.type === "Unknown");
    if (hasUnknown) {
      alert("Unknown files detected. Remove them.");
      return;
    }

    const hasCyber = validation.some(f => f.type === "Cyber");
    if (hasCyber && transferMode !== "Cyber") {
      alert("Cyber-only files present. Enable Cyber mode.");
      return;
    }

    await transferFiles({ tree, transferMode });
    alert("Transfer initiated");
  };

  return (
    <div>
      <h1>File Transfer Tool</h1>

      <FileDrop onFiles={handleFiles} />

      <FileTree tree={tree} />

      <label>
        <input
          type="checkbox"
          onChange={(e) =>
            setTransferMode(e.target.checked ? "Cyber" : "Normal")
          }
        />
        Cyber Transfer
      </label>

      <button onClick={handleTransfer}>Transfer</button>
    </div>
  );
}

export default App;
```

---

# 🔧 Backend (Node.js Example)

## Why Node?

* Matches JS stack
* Easy file system access
* Good for rapid migration

---

## 1. Setup

```bash
mkdir backend
cd backend
npm init -y
npm install express multer fs-extra
```

---

## 2. Validation Endpoint

```javascript
// server.js
const express = require("express");
const app = express();

app.use(express.json());

app.post("/api/validate", (req, res) => {
  const files = req.body;

  // TODO: replicate:
  // Get-ExtensionClassification
  // Get-FileValidationMessages

  const tree = files.map(f => ({
    name: f.name,
    type: "regular", // or cyber / error
  }));

  res.json({
    tree,
    summary: tree
  });
});
```

---

## 3. Transfer Endpoint

```javascript
const fs = require("fs-extra");
const path = require("path");

app.post("/api/transfer", async (req, res) => {
  const { tree, transferMode } = req.body;

  const basePath =
    transferMode === "Cyber"
      ? "\\\\Cybersecurity\\Public\\File Transfer"
      : "\\\\DropBox\\Public\\Uploads";

  const timestamp = new Date().toISOString();

  const targetFolder = path.join(basePath, timestamp);

  await fs.ensureDir(targetFolder);

  // TODO: replicate Copy-TreeViewData logic

  res.json({ success: true });
});
```

---

# 🔥 Key Improvements Over PowerShell

### ✅ Separation of concerns

* UI vs logic vs filesystem

### ✅ Testability

* Backend logic can be unit tested

### ✅ Performance

* No repeated CSV reads per file

### ✅ Extensibility

* Add auth, progress bars, retries

---

# ⚠️ Gaps You MUST Address

These are non-trivial:

### 1. Network Share Access

* Backend must run in environment with access to:

  * `\\DropBox`
  * `\\Cybersecurity`

### 2. Folder Drag & Drop

* Browser support is limited
* You may need:

  ```javascript
  webkitdirectory
  ```

### 3. Active Directory Integration

Replace:

```powershell
[adsisearcher]
```

With:

* LDAP (Node: `ldapjs`)
* Or SSO (preferred)

---

# 🧭 Recommended Next Step

Don’t try to build everything at once.

### Phase 1 (MVP)

* Drag/drop files
* Show tree
* Mock validation
* Mock transfer

### Phase 2

* Real validation engine (port PowerShell logic)

### Phase 3

* Real file transfer + logging

---

# If You Want Next Level Help

I can:

* Port **Get-FileValidationMessages** fully to Node
* Design **API contract (OpenAPI spec)**
* Add **progress tracking + retry logic**
* Implement **real AD/SSO integration**
* Add **bulk performance optimizations**

---

Ask your next question—this is a non-trivial migration, and the hard parts are just ahead.
