import type { UploadFile } from '../types/upload'

interface Props {
  files: UploadFile[]
}

export function ValidationSummary({
  files,
}: Props) {
  const summary = {
    allowed: 0,
    cyber: 0,
    blocked: 0,
  }

  for (const file of files) {
    const state = file.validation[0].type
    summary[state] += 1
  }

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="rounded bg-green-600 p-4">
        <div className="text-sm">Allowed</div>
        <div className="text-2xl font-bold">
          {summary.allowed}
        </div>
      </div>

      <div className="rounded bg-yellow-600 p-4">
        <div className="text-sm">Cyber</div>
        <div className="text-2xl font-bold">
          {summary.cyber}
        </div>
      </div>

      <div className="rounded bg-red-600 p-4">
        <div className="text-sm">Blocked</div>
        <div className="text-2xl font-bold">
          {summary.blocked}
        </div>
      </div>
    </div>
  )
}