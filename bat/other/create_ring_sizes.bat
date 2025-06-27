@echo off
setlocal

:: Ask user for diameter
echo Enter current inner diameter of the ring in mm (e.g. 16.5):
set /p DIAMETER=

:: Convert to circumference using PowerShell for float math
for /f %%a in ('powershell "3.1416 * %DIAMETER%"') do set Circumference=%%a

:: Navigate two folders up from the batch file location to find the grandparent directory
pushd "%~dp0" >nul || exit /b
cd ..\.. >nul || exit /b
for %%i in (.) do set "GRANDPARENT_DIR=%%~fi"
popd

:: Read key-value pairs from config.txt
for /f "tokens=1* delims==" %%a in (%BAT_CONFIG_PATH%) do (
    set %%a=%%b
)

:: Count the number of .stl files in the grandparent directory
for /f %%A in ('dir /b "%GRANDPARENT_DIR%\*.stl" 2^>nul ^| find /c /v ""') do set count=%%A

:: Initialize FILEPATH
set "FILEPATH="

:: If there's exactly one .stl file in the grandparent directory, set FILEPATH to its name
if "%count%"=="1" (
    for /f "delims=" %%i in ('dir /b "%GRANDPARENT_DIR%\*.stl"') do set "FILEPATH=%%i"
)

:: If there's none or more than one .stl file, prompt the user to pick a file
if not defined FILEPATH (
    for /f "delims=" %%i in ('powershell -command "[System.Reflection.Assembly]::LoadWithPartialName('System.windows.forms') | Out-Null; $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog; $OpenFileDialog.InitialDirectory = "%GRANDPARENT_DIR%"; $OpenFileDialog.Filter = 'STL Files (*.stl)|*.stl'; $OpenFileDialog.ShowDialog() | Out-Null; $OpenFileDialog.FileName"') do set "FILEPATH=%%i"
)

:: Check if a file was selected
if "%FILEPATH%"=="False" (
    echo No file selected.
    exit /b
)

:: Write values to temp file
echo %Circumference%>%TEMP%\RingSize.txt
echo %FILEPATH%>>%TEMP%\RingSize.txt

:: Start Rhino (replace path to match your Rhino.exe)
start "" "%RHINO_PATH%" "%FILEPATH%" /runscript="_-RunPythonScript ""%USERPROFILE%\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\create_ring_sizes.py"""

endlocal