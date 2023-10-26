@echo off
setlocal

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: MAIN COLOR

@echo off
:AskAgain
echo Main Color. Choose your option:
echo 1. Gold
echo 2. Silver
echo 3. Black
echo 4. Green
echo 5. Rose
echo 6. Blue
set /p MainColor=Enter your choice (1 or 2): 

if "%MainColor%"=="1" (
    echo You chose Gold.
) else if "%MainColor%"=="2" (
    echo You chose Silver.
) else if "%MainColor%"=="3" (
    echo You chose Black.
) else if "%MainColor%"=="4" (
    echo You chose Green.
) else if "%MainColor%"=="5" (
    echo You chose Rose.
) else if "%MainColor%"=="6" (
    echo You chose Blue.
)
else (
    echo Invalid choice. Please try again.
    goto AskAgain
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: DIAMOND COLOR

@echo off
:AskAgain
echo Stone Color: Choose your option:
echo 1. White
echo 2. Red
echo 3. Black
echo 4. Green
echo 5. Blue
set /p SecondaryColor=Enter your choice (1 or 2): 

if "%SecondaryColor%"=="1" (
    echo You chose White.
) else if "%SecondaryColor%"=="2" (
    echo You chose Red.
) else if "%SecondaryColor%"=="3" (
    echo You chose Black.
) else if "%SecondaryColor%"=="4" (
    echo You chose Green.
) else if "%SecondaryColor%"=="5" (
    echo You chose Blue.
)
else (
    echo Invalid choice. Please try again.
    goto AskAgain
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: CLOSE RHINO?




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
start "" "C:\Program Files\Rhino 7\System\Rhino.exe" "%FILEPATH%" /runscript="_-RunPythonScript C:\Users\noyda\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\create_video_silver.py"

endlocal