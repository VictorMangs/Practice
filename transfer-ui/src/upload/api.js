export function uploadFile(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "http://localhost:3000/api/upload");

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr.response);
      } else {
        reject(xhr.response);
      }
    };

    xhr.onerror = reject;

    const formData = new FormData();

    // IMPORTANT: must be exactly "file"
    formData.append("file", file);

    // optional but useful for folder structure
    formData.append("path", file.webkitRelativePath || file.name);

    xhr.send(formData);
  });
}