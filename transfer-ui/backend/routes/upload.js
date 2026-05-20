const express = require("express");
const multer = require("multer");
const TransferService = require("../transferService");

const router = express.Router();

// Memory storage = stream directly into final destination
const upload = multer({ storage: multer.memoryStorage() });

const transferService = new TransferService({
  uploadRoot: "C:\\Users\\Victor2021\\Documents\\testing",
  cyberRoot: "C:\\Users\\Victor2021\\Documents\\testing\\cyber",
  logPath: "C:\\Users\\Victor2021\\Documents\\testing\\log",
  logFile: "TransferLog.csv",
});

/**
 * POST /api/upload
 * Streams file directly into final destination
 */
router.post("/upload", upload.single("file"), async (req, res) => {
    console.log("BODY:", req.body);
    console.log("FILE:", req.file);
    
    try {
    const file = req.file;

    const {
      relativePath,
      user = "UNKNOWN",
      mode = "Normal",
    } = req.body;

    if (!file || !relativePath) {
      return res.status(400).json({
        error: "Missing file or relativePath",
      });
    }

    // SECURITY: prevent path traversal
    if (relativePath.includes("..")) {
      return res.status(400).json({
        error: "Invalid path",
      });
    }

    const result = await transferService.writeFileDirect({
      buffer: file.buffer,
      relativePath,
      user,
      mode,
    });

    res.json({
      success: true,
      path: result,
    });
  } catch (err) {
    console.error("Upload failed:", err);
    res.status(500).json({
      error: "Upload failed",
    });
  }
});

module.exports = router;