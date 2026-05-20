// components/FileDrop.jsx
import { useDropzone } from "react-dropzone";

export default function FileDrop({ onFiles }) {
  const { getRootProps, getInputProps } = useDropzone({
    multiple: true,
    useFsAccessApi: false,
    onDrop: (files) => onFiles(files),
  });

  return (
    <div
      {...getRootProps()}
      style={{
        border: "2px dashed #888",
        padding: 30,
        marginBottom: 20,
        cursor: "pointer",
      }}
    >
      <input {...getInputProps()} webkitdirectory="true" />
      <p>Drag & drop files/folders or click to select</p>
    </div>
  );
}