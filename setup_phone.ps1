# SmartStudent - Setup Script
# Run this in PowerShell each time you connect the phone via USB

Write-Host "`n=== SmartStudent Phone Setup ===" -ForegroundColor Cyan

# 1. Check device
$devices = adb devices 2>&1 | Select-String "device$"
if (-not $devices) {
    Write-Host "[ERR] Phone not connected. Connect via USB and enable USB Debugging." -ForegroundColor Red
    exit 1
}
Write-Host "[OK]  Phone detected: $devices" -ForegroundColor Green

# 2. ADB reverse tunnel
adb reverse tcp:8000 tcp:8000 | Out-Null
Write-Host "[OK]  ADB reverse tunnel active (phone localhost:8000 -> PC port 8000)" -ForegroundColor Green

# 3. Enable WiFi ADB (so you can disconnect USB later)
adb tcpip 5555 | Out-Null
$phoneIp = adb shell "ip route | grep wlan | awk '{print $9}' | head -1" 2>&1
Write-Host "[OK]  WiFi ADB enabled. Phone IP: $phoneIp" -ForegroundColor Green

# 4. Check backend
try {
    $r = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 3
    Write-Host "[OK]  Backend running: $($r.service)" -ForegroundColor Green
} catch {
    Write-Host "[!]   Backend not running. Starting it..." -ForegroundColor Yellow
    Start-Process -FilePath "$PSScriptRoot\.venv\Scripts\python.exe" `
        -ArgumentList "-m uvicorn backend.main:app --host 0.0.0.0 --port 8000" `
        -WorkingDirectory $PSScriptRoot -WindowStyle Minimized
    Start-Sleep -Seconds 4
    Write-Host "[OK]  Backend started" -ForegroundColor Green
}

# 5. Install latest APK if it exists
$apk = "$PSScriptRoot\flutter\build\app\outputs\flutter-apk\app-release.apk"
if (Test-Path $apk) {
    Write-Host "[...]  Installing APK..." -ForegroundColor Yellow
    $result = adb install -r $apk 2>&1
    if ($result -match "Success") {
        Write-Host "[OK]  APK installed successfully" -ForegroundColor Green
    } else {
        Write-Host "[!]   APK install issue: $result" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Ready! Open SmartStudent on your phone ===" -ForegroundColor Cyan
