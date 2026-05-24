@echo off
setlocal enabledelayedexpansion

echo ============================================
echo  SmartStudent Backend - Demarrage
echo ============================================
echo.

cd /d "%~dp0"

:: Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    pause
    exit /b 1
)

:: Arreter tout processus existant sur le port 8000
echo [INFO] Arret de tout processus sur le port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Port 8000 libere.
echo.

:: Afficher l'IP locale
echo [INFO] Adresse IP de ce PC sur le reseau local :
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4 Address"') do (
    set PCIP=%%a
    set PCIP=!PCIP: =!
    echo        http://!PCIP!:8000
)
echo.

:: Configurer le pare-feu Windows (port 8000 entrant)
echo [INFO] Configuration du pare-feu Windows...
netsh advfirewall firewall delete rule name="SmartStudent Port 8000" >nul 2>&1
netsh advfirewall firewall add rule name="SmartStudent Port 8000" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Pare-feu non configure. Relancez en tant qu'Administrateur si la connexion echoue.
) else (
    echo [OK] Pare-feu configure : port 8000 autorise.
)
echo.

:: Installer les dependances
echo [INFO] Verification des dependances...
pip install -r backend/requirements.txt -q
echo [OK] Dependances pres.
echo.

:: Demarrer le backend sur toutes les interfaces (0.0.0.0)
echo ============================================
echo  Backend demarre sur http://0.0.0.0:8000
echo  Le telephone Android se connecte via :
echo  http://!PCIP!:8000
echo ============================================
echo.
echo  Ctrl+C pour arreter
echo.

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause
