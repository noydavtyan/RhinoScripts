@echo off
setlocal

:: Count the number of .3dm files in the current directory
for /f %%A in ('dir /b *.3dm 2^>nul ^| find /c /v ""') do set count=%%A

:: If there's exactly one .3dm file, set FILEPATH to its name
if "%count%"=="1" for %%i in (*.3dm) do set "FILEPATH=%%~fi"

:: If there's none or more than one .3dm file, prompt the user to pick a file
if not defined FILEPATH (
    for /f "delims=" %%i in ('powershell -command "[System.Reflection.Assembly]::LoadWithPartialName('System.windows.forms') | Out-Null; $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog; $OpenFileDialog.InitialDirectory = Get-Location; $OpenFileDialog.ShowDialog() | Out-Null; $OpenFileDialog.FileName"') do set "FILEPATH=%%i"
)

:: Check if a file was selected
if "%FILEPATH%"=="False" (
    echo No file selected.
    exit /b
)

:: Run Rhino with the selected file and execute the Python script
start "" "C:\Program Files\Rhino 7\System\Rhino.exe" "%FILEPATH%" /runscript="_-RunPythonScript C:\Users\noyda\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\create_video_gold.py"

endlocal