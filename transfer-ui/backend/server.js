const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs-extra");

const TransferService = require("./transferService");

const app = express();

/**
 * ---------------------------
 * CORS FIX (your earlier error)
 * ---------------------------
 */
app.use(
  cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST", "OPTIONS"],
  })
);

app.use(express.json());

/**
 * ---------------------------
 * MULTER CONFIG (CRITICAL FIX)
 * ---------------------------
 */
const upload = multer({
  storage: multer.memoryStorage(),
});

/**
 * ---------------------------
 * TRANSFER SERVICE
 * ---------------------------
 */
const transferService = new TransferService({
  uploadRoot: "C:\\Users\\Victor2021\\Documents\\testing",
  cyberRoot: "C:\\Users\\Victor2021\\Documents\\testing\\cyber",
  logPath: "C:\\Users\\Victor2021\\Documents\\testing\\log",
  logFile: "TransferLog.csv",
});

/**
 * ---------------------------
 * UPLOAD ENDPOINT (FIXED)
 * ---------------------------
 */
app.post("/api/upload", upload.single("file"), async (req, res) => {
  try {
    const file = req.file; // <-- THIS was undefined before

    if (!file) {
      return res.status(400).json({
        error: "No file received (check FormData field name = 'file')",
      });
    }

    const relativePath = req.body.path || file.originalname;

    const targetPath = path.join(
      "C:\\Users\\Victor2021\\Documents\\testing\\uploads",
      relativePath
    );

    await fs.ensureDir(path.dirname(targetPath));

    await fs.writeFile(targetPath, file.buffer);

    return res.json({
      success: true,
      path: targetPath,
    });
  } catch (err) {
    console.error("UPLOAD ERROR:", err);
    return res.status(500).json({ error: "Upload failed" });
  }
});

/**
 * ---------------------------
 * TRANSFER ENDPOINT
 * ---------------------------
 */
app.post("/api/transfer", async (req, res) => {
  const { tree, user, mode } = req.body;

  try {
    const result = await transferService.transfer(tree, user, mode);

    res.json({ started: true, result });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Transfer failed" });
  }
});

app.listen(3000, () =>
  console.log("Server running on http://localhost:3000")
);