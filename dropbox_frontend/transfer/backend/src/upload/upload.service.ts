import { Injectable } from '@nestjs/common'

import * as path from 'path'

import { PrismaService } from '../prisma/prisma.service'
import { StorageService } from '../storage/storage.service'

import { ValidationService } from './validation.service'

@Injectable()
export class UploadService {
  constructor(
    private prisma: PrismaService,
    private storageService: StorageService,
    private validationService: ValidationService,
  ) {}

  async createSession() {
    return this.prisma.uploadSession.create({
      data: {},
    })
  }

  async uploadFile(
    sessionId: string,
    file: Express.Multer.File,
    relativePath: string,
  ) {
    const extension = path.extname(
      file.originalname,
    )

    const validation =
      this.validationService.validateExtension(
        extension,
      )

    const storedPath =
      await this.storageService.saveFile(
        sessionId,
        relativePath,
        file.buffer,
      )

    const saved =
      await this.prisma.fileRecord.create({
        data: {
          sessionId,

          originalName:
            file.originalname,

          relativePath,

          extension,

          storedPath,

          validationState:
            validation.state,

          validationMessage:
            validation.message,
        },
      })

    return saved
  }
}