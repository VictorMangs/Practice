export type ValidationState =
  | 'allowed'
  | 'cyber'
  | 'blocked'

export interface ValidationMessage {
  type: ValidationState
  message: string
}

export interface UploadFile {
  id: string
  file: File
  relativePath: string
  validation: ValidationMessage[]
}

export interface TreeNode {
  name: string
  path: string
  type: 'file' | 'folder'
  validation?: ValidationState
  children?: TreeNode[]
}