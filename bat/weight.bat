@echo off
setlocal

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

:: Extract just the file name without the extension from FILEPATH
for %%i in ("%FILEPATH%") do set "FILENAME_ONLY=%%~ni"

set "WEIGHT_PY=%USER_PATH%\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\calculate_weight.py"

:: Use FILENAME_ONLY instead of FILEPATH for the Python script argument
start /B cmd /c ""%PYTHON_PATH%" "%WEIGHT_PY%" "%GRANDPARENT_DIR%" "%FILENAME_ONLY%""

:EndScript
endlocal
