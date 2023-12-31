@echo off
setlocal

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Ring size

@echo off
:AskAgain
echo Ring Current Circumference in mm (Example: 50)?
set /p RingSize=Enter the Circumference: 



:: Count the number of .3dm files in the parent directory
for /f %%A in ('dir /b ..\*.3dm 2^>nul ^| find /c /v ""') do set count=%%A

:: If there's exactly one .3dm file in the parent directory, set FILEPATH to its name
if "%count%"=="1" for %%i in (..\*.3dm) do set "FILEPATH=%%~fi"

:: If there's none or more than one .3dm file, prompt the user to pick a file
if not defined FILEPATH (
    for /f "delims=" %%i in ('powershell -command "[System.Reflection.Assembly]::LoadWithPartialName('System.windows.forms') | Out-Null; $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog; $OpenFileDialog.InitialDirectory = Split-Path (Get-Location) -Parent; $OpenFileDialog.ShowDialog() | Out-Null; $OpenFileDialog.FileName"') do set "FILEPATH=%%i"
)

:: Check if a file was selected
if "%FILEPATH%"=="False" (
    echo No file selected.
    exit /b
)

:: Write the ring size and file path to a temporary file
echo %RingSize%>%TEMP%\RingSize.txt
echo %FILEPATH%>>%TEMP%\RingSize.txt

:: Start Rhino and run the script
start "" "%RHINO_PATH%" "%FILEPATH%" /runscript="_-RunPythonScript ""%USER_PATH%\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\create_eu_sizes.py"""

endlocal