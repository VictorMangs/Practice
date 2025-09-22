package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func downloadHandler(w http.ResponseWriter, r *http.Request) {
    // Assuming you've received the file name from the client
    fileName := r.FormValue("filename")

    // Open the file for reading (you'll need to adjust the path)
    file, err := os.Open("path/to/your/files/" + fileName)
    if err != nil {
        http.Error(w, "File not found", http.StatusNotFound)
        return
    }
    defer file.Close()

    // Set appropriate headers for download
    w.Header().Set("Content-Disposition", fmt.Sprintf("attachment; filename=\"%s\"", fileName))
    w.Header().Set("Content-Type", "application/octet-stream")

    // Copy the file content to the response writer
    _, err = io.Copy(w, file)
    if err != nil {
        http.Error(w, "Error while copying file", http.StatusInternalServerError)
        return
    }
}

func main() {
    http.HandleFunc("/api", downloadHandler)
    http.ListenAndServe(":8080", nil)
}
