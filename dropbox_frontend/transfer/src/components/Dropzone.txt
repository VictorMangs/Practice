import { useDropzone } from 'react-dropzone'

import { useUploadStore } from '../store/uploadStore'

import type { UploadFile } from '../types/upload'

import { validateFile } from '../utils/mockValidation'

declare module 'react' {
  interface InputHTMLAttributes<T> extends HTMLAttributes<T> {
    directory?: string;
    webkitdirectory?: string;
  }
}

function randomId() {
  return crypto.randomUUID()
}

export function Dropzone() {
  const setFiles = useUploadStore(
    (state) => state.setFiles,
  )

  const onDrop = (acceptedFiles: File[]) => {
    const mapped: UploadFile[] =
      acceptedFiles.map((file) => ({
        id: randomId(),
        file,
        relativePath:
          file.webkitRelativePath || file.name,
        validation: validateFile(file.name),
      }))

    setFiles(mapped)
  }

  const {
    getRootProps,
    getInputProps,
    isDragActive,
  } = useDropzone({
    onDrop,
  })

  return (
    <div
      {...getRootProps()}
      className="cursor-pointer rounded-lg border-2 border-dashed border-slate-600 p-12 text-center transition hover:border-blue-400"
    >
      <input
        {...getInputProps()}
        webkitdirectory="true"
        directory=""
        multiple
      />

      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <div>
          <p className="text-lg font-semibold">
            Drag and drop folders here
          </p>

          <p className="mt-2 text-sm text-slate-400">
            Or click to browse
          </p>
        </div>
      )}
    </div>
  )
}