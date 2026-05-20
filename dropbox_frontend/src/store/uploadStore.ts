import { create } from 'zustand'

import type {
  TreeNode,
  UploadFile,
} from '../types/upload'

interface UploadStore {
  files: UploadFile[]
  tree: TreeNode[]

  setFiles: (files: UploadFile[]) => void

  clearFiles: () => void
}

export const useUploadStore =
  create<UploadStore>((set) => ({
    files: [],
    tree: [],

    setFiles: (files) =>
      set(() => ({
        files,
      })),

    clearFiles: () =>
      set(() => ({
        files: [],
        tree: [],
      })),
  }))