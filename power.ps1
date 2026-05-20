Write-Host "Pulling trivy zip file ..."
$release = Invoke-RestMethod `
  -Uri "https://api.github.com/repos/aquasecurity/trivy/releases/latest"

$asset = $release.assets |
  Where-Object { $_.name -match "windows-64bit.zip$" } |
  Select-Object -First 1

Invoke-WebRequest `
  -Uri $asset.browser_download_url `
  -OutFile "trivy.zip"

Write-Host "Unzipping trivy zip file ..."
Expand-Archive -Force .\trivy.zip -DestinationPath .\trivy

Write-Host "Downloading trivy database files ..."
.\trivy\trivy.exe image --download-db-only --cache-dir .\trivy-cache

Write-Host "Tarring trivy database files ..."
tar.exe -czf trivy-db.tar.gz -C "./trivy-cache/db" .

Write-Host "Cleaning up trivy download artifacts ..."
Remove-Item -Recurse -Force -Path ".\trivy-cache",".\trivy",".\trivy.zip"

Write-Host
# ================================================================================
Write-Host "Pulling grype zip file ..."
$release = Invoke-RestMethod `
  -Uri "https://api.github.com/repos/anchore/grype/releases/latest"

$asset = $release.assets |
  Where-Object { $_.name -match "windows_amd64.zip$" } |
  Select-Object -First 1

Invoke-WebRequest `
  -Uri $asset.browser_download_url `
  -OutFile "grype.zip"

Write-Host "Unzipping grype zip file ..."
Expand-Archive -Force .\grype.zip -DestinationPath .\grype

Write-Host "Downloading grype database files ..."
.\grype\grype.exe db update

$grype_db_path = (.\grype\grype.exe db status) -match '^(Location|Path):' -replace '^(Location|Path):\s*', ''

$grype_db_path = Split-Path (
    Split-Path $grype_db_path -Parent
) -Parent

Write-Host "Tarring grype database files ..."
tar.exe -czf grype-db.tar.gz -C "$grype_db_path" .

$grype_db_path = Split-Path (
    Split-Path $grype_db_path -Parent
) -Parent

Write-Host "Cleaning up grype download artifacts ..."
Remove-Item -Recurse -Force -Path ".\grype",".\grype.zip","$grype_db_path"

Write-Host
Write-Host "Grype database archive path: $PSScriptRoot\grype-db.tar.gz"
Write-Host "Trivy database archive path: $PSScriptRoot\trivy-db.tar.gz"
Write-Host "Script Complete!"