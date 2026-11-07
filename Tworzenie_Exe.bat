@echo off
rem ==========================================================
rem  LabiryntOL - kompilacja do .exe (PyInstaller, tryb katalogu)
rem  Wynik: dist\LabiryntOL\LabiryntOL.exe
rem ==========================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set NAZWA=LabiryntOL
set SKRYPT=labiryntol.py
set IKONA=GitHub\ikona.ico
set WERSJA=GitHub\Wersja.txt

echo.
echo === Kompilacja %NAZWA% ===
echo.

rem --- Sprawdzenie plikow ---------------------------------
for %%F in ("%SKRYPT%" "%IKONA%" "%WERSJA%") do (
    if not exist %%F (
        echo [BLAD] Brak pliku %%~F
        goto :blad
    )
)

rem --- Sprawdzenie Pythona i PyInstallera ----------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Nie znaleziono Pythona w PATH.
    goto :blad
)

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nie jest zainstalowany - instaluje...
    python -m pip install pyinstaller
    if errorlevel 1 goto :blad
)

rem --- Czyszczenie poprzedniej kompilacji ----------------
if exist "build\%NAZWA%" rmdir /s /q "build\%NAZWA%"
if exist "dist\%NAZWA%"  rmdir /s /q "dist\%NAZWA%"
if exist "%NAZWA%.spec"  del /q "%NAZWA%.spec"

rem --- Kompilacja -----------------------------------------
python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onedir ^
    --windowed ^
    --name "%NAZWA%" ^
    --icon "%IKONA%" ^
    --version-file "%WERSJA%" ^
    --add-data "%IKONA%;." ^
    "%SKRYPT%"
if errorlevel 1 goto :blad

rem --- Dolaczenie dokumentacji ----------------------------
for %%F in (LICENCJA.txt README.md CHANGELOG.md) do (
    if exist "%%F" copy /y "%%F" "dist\%NAZWA%\" >nul
)

echo.
echo === Gotowe: dist\%NAZWA%\%NAZWA%.exe ===
echo.
pause
exit /b 0

:blad
echo.
echo === Kompilacja NIEUDANA ===
echo.
pause
exit /b 1