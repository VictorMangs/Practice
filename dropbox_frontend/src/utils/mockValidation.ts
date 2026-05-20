import type { ValidationMessage } from '../types/upload'

const blockedExtensions = [
  '.exe',
  '.bat',
  '.cmd',
  '.ps1',
]

const cyberExtensions = [
  '.zip',
  '.7z',
]

export function validateFile(
  filename: string,
): ValidationMessage[] {
  const lower = filename.toLowerCase()

  const extension =
    lower.slice(lower.lastIndexOf('.'))

  if (blockedExtensions.includes(extension)) {
    return [
      {
        type: 'blocked',
        message:
          'This file type is not approved for transfer.',
      },
    ]
  }

  if (cyberExtensions.includes(extension)) {
    return [
      {
        type: 'cyber',
        message:
          'This file requires cyber routing.',
      },
    ]
  }

  return [
    {
      type: 'allowed',
      message: 'File is approved.',
    },
  ]
}