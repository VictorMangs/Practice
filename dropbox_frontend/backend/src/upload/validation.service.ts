import { Injectable } from '@nestjs/common'

@Injectable()
export class ValidationService {
  validateExtension(ext: string) {
    const blocked = ['.exe', '.bat']
    const cyber = ['.zip']

    if (blocked.includes(ext)) {
      return {
        state: 'blocked',
        message: 'Blocked extension',
      }
    }

    if (cyber.includes(ext)) {
      return {
        state: 'cyber',
        message: 'Cyber routing required',
      }
    }

    return {
      state: 'allowed',
      message: 'Approved',
    }
  }
}