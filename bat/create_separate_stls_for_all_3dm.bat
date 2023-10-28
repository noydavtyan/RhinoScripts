@echo off
setlocal

:: Get the path to the Python script
set "PYTHON_SCRIPT=C:\Users\noyda\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\create_separate_stl.py"

:: Set the countdown duration in seconds (e.g., 5 seconds)
set "COUNTDOWN_DURATION=30"

:: Iterate over each .3dm file in the current directory
for %%i in (*.3dm) do (
    echo Processing file: %%i

    :: Display the countdown
    for /l %%s in (%COUNTDOWN_DURATION%,-1,1) do (
        echo Starting processing in %%s seconds...
        timeout /t 1 > nul
    )

    :: Start Rhino and run the Python script
    start "" "C:\Program Files\Rhino 7\System\Rhino.exe" "%%~fi" /runscript="_-RunPythonScript ""%PYTHON_SCRIPT%"""
)

endlocal