@echo off
setlocal
echo 🍎 Mapple v0.2.0 Installer
echo -----------------------

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python 3 not found. 
    echo [!] Opening the download page...
    start https://www.python.org/downloads/
    pause
    exit
)

:: 2. Version Check logic
set "NEW_VER=0.2.0"
for /f "tokens=3" %%i in ('mppl --version 2^>nul') do set "INSTALLED_VER=%%i"

if defined INSTALLED_VER (
    echo [*] Detected existing Mapple v%INSTALLED_VER%
    if "%INSTALLED_VER%"=="v%NEW_VER%" (
        echo [!] You already have the latest version.
        set /p choice="Reinstall anyway? (y/n): "
        if /I "%choice%"=="n" exit
    )
)

:: 3. Set PATH
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

echo [*] Adding Mapple to User PATH...
:: setx adds to the user path permanently
setx PATH "%PATH%;%CURRENT_DIR%" >nul

echo [OK] Mapple path set to: %CURRENT_DIR%
echo -----------------------
echo 🚀 Installation Complete! 
echo Please RESTART your terminal/VS Code to apply changes.
echo Then type 'mppl --doctor' to verify.
pause