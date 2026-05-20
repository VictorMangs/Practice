-- CreateTable
CREATE TABLE "UploadSession" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "FileRecord" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "sessionId" TEXT NOT NULL,
    "originalName" TEXT NOT NULL,
    "relativePath" TEXT NOT NULL,
    "extension" TEXT NOT NULL,
    "storedPath" TEXT NOT NULL,
    "validationState" TEXT NOT NULL,
    "validationMessage" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "FileRecord_sessionId_fkey" FOREIGN KEY ("sessionId") REFERENCES "UploadSession" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
