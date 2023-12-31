@echo off
setlocal

:: Read key-value pairs from config.txt
for /f "tokens=1* delims==" %%a in (%BAT_CONFIG_PATH%) do (
    set %%a=%%b
)

:: Get the path to the Python script
set "PYTHON_SCRIPT=%USER_PATH%\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\create_separate_stl.py"

:: Set the countdown duration in seconds (e.g., 5 seconds)
set "COUNTDOWN_DURATION=30"

:: Iterate over each .3dm file in the current directory
for %%i in (%OTHER_BAT_RELATIVE_DIRECTORY%) do (
    echo Processing file: %%i

    :: Display the countdown
    for /l %%s in (%COUNTDOWN_DURATION%,-1,1) do (
        echo Starting processing in %%s seconds...
        timeout /t 1 > nul
    )

    :: Start Rhino and run the Python script
    start "" "%RHINO_PATH%" "%%~fi" /runscript="_-RunPythonScript ""%PYTHON_SCRIPT%"""
)

endlocal