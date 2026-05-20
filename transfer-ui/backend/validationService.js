// validationService.js
const fs = require("fs");
const path = require("path");
const { parse } = require("csv-parse/sync");

class ValidationService {
  constructor(basePath) {
    this.basePath = basePath;

    this.allowedFileTypes = [];
    this.messages = [];
    this.cyberAllowed = new Set();
  }

  // -------------------------------
  // Load all CSV data once
  // -------------------------------
  init() {
    this.allowedFileTypes = this.loadCSV("AllowedFileTypes.csv");
    this.messages = this.loadCSV("Messages.csv");
    this.loadCyberWhitelist("file extention whitelist reference 2022.csv");
  }

  loadCSV(fileName) {
    const filePath = path.join(this.basePath, fileName);
    if (!fs.existsSync(filePath)) {
      throw new Error(`Missing file: ${filePath}`);
    }

    const content = fs.readFileSync(filePath);
    return parse(content, {
      columns: true,
      skip_empty_lines: true,
      trim: true,
    });
  }

  loadCyberWhitelist(fileName) {
    const rows = this.loadCSV(fileName);

    rows.forEach((row) => {
      let ext = row["File Extention"]?.trim();
      if (!ext) return;

      if (!ext.startsWith(".")) ext = "." + ext;
      this.cyberAllowed.add(ext.toLowerCase());
    });
  }

  // -------------------------------
  // Classification logic
  // -------------------------------
  getExtensionClassification(ext) {
    const extension = ext.toLowerCase();

    const isRegular = this.allowedFileTypes.some((row) =>
      row.Extension.split(";").includes(extension)
    );

    if (isRegular) return "Regular";
    if (this.cyberAllowed.has(extension)) return "Cyber";

    return "Unknown";
  }

  // -------------------------------
  // Core function (PORTED)
  // -------------------------------
  getFileValidationMessages(fileName) {
    const extension = path.extname(fileName).toLowerCase();
    const classification = this.getExtensionClassification(extension);

    let validationMessages = [];

    if (classification === "Regular") {
      const match = this.allowedFileTypes.find((row) =>
        row.Extension.split(";").includes(extension)
      );

      if (match) {
        const ids = match.Message.split(";");

        validationMessages = this.messages
          .filter((msg) => ids.includes(msg.ID))
          .map((msg) => ({
            ID: msg.ID,
            Type: msg.Type,
            Action: msg.Action,
            Message: msg.Message,
          }));
      }
    }

    if (classification === "Cyber") {
      validationMessages = this.messages
        .filter((msg) => msg.ID === "70")
        .map((msg) => ({
          ID: msg.ID,
          Type: msg.Type,
          Action: msg.Action,
          Message: msg.Message,
        }));
    }

    if (classification === "Unknown") {
      validationMessages = this.messages
        .filter((msg) => msg.ID === "10")
        .map((msg) => ({
          ID: msg.ID,
          Type: msg.Type,
          Action: msg.Action,
          Message: msg.Message,
        }));
    }

    // -------------------------------
    // Special cases (pptx/docx)
    // -------------------------------
    const special = this.getSpecialCaseMessages(fileName, extension);
    if (special.length > 0) {
      validationMessages = validationMessages.concat(special);
    }

    return {
      FileName: fileName,
      ValidationMessages: validationMessages,
    };
  }

  // -------------------------------
  // Special Case Handler (simplified)
  // -------------------------------
  getSpecialCaseMessages(fileName, extension) {
    // Placeholder for now (see note below)
    if (![".pptx", ".docx"].includes(extension)) return [];

    // You can later plug in ZIP extraction like PowerShell
    return [];
  }
}

module.exports = ValidationService;