const fs = require("fs-extra");
const path = require("path");
const { createObjectCsvWriter } = require("csv-writer");

class TransferService {
  constructor(config) {
    this.uploadRoot = config.uploadRoot;
    this.cyberRoot = config.cyberRoot;
    this.logPath = config.logPath;
    this.logFile = config.logFile;
  }

  async writeFileDirect({ buffer, relativePath, user, mode }) {
    const basePath =
        mode === "Cyber" ? this.cyberRoot : this.uploadRoot;

    const timestamp = this.getTimestamp();

    const rootFolder = `${user}_${timestamp}`;

    const fullPath = path.join(basePath, rootFolder, relativePath);

    await fs.ensureDir(path.dirname(fullPath));

    await fs.writeFile(fullPath, buffer);

    return fullPath;
    }

  // NEW: log from real filesystem (not tree)
  async writeLogFromPath(rootPath) {
    const files = await fs.readdir(rootPath, { recursive: true });

    const fileInfoList = [];

    for (const file of files) {
      const fullPath = path.join(rootPath, file);

      const stats = await fs.stat(fullPath);

      if (!stats.isFile()) continue;

      fileInfoList.push({
        FullPath: fullPath,
        FileName: path.basename(fullPath),
        FileSize_KB: Math.round((stats.size / 1024) * 100) / 100,
        FileTransferTime: 0, // optional enhancement later
      });
    }

    await this.writeLog(fileInfoList);
  }

  async writeLog(fileInfoList) {
    const rows = fileInfoList.map((entry) => {
      return {
        username: "SYSTEM",
        Lastname: "SYSTEM",
        Firstname: "SYSTEM",
        FileName: entry.FileName,
        FileSize_KB: entry.FileSize_KB,
        FileDate: "UNKNOWN",
        FileTime: "UNKNOWN",
        Timezone: this.getTimezone(),
        TransferTime_seconds: entry.FileTransferTime,
      };
    });

    const csvPath = path.join(this.logPath, this.logFile);

    const writer = createObjectCsvWriter({
      path: csvPath,
      header: [
        { id: "username", title: "username" },
        { id: "Lastname", title: "Lastname" },
        { id: "Firstname", title: "Firstname" },
        { id: "FileName", title: "FileName" },
        { id: "FileSize_KB", title: "FileSize_KB" },
        { id: "FileDate", title: "FileDate" },
        { id: "FileTime", title: "FileTime" },
        { id: "Timezone", title: "Timezone" },
        { id: "TransferTime_seconds", title: "TransferTime_seconds" },
      ],
      append: await fs.pathExists(csvPath),
    });

    await writer.writeRecords(rows);
  }

  getTimezone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  }
}

module.exports = TransferService;