@echo off
setlocal

:: Get the path to the Python script
set "PYTHON_SCRIPT=C:\Users\noyda\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\RhinoScripts\scripts\create_separate_stls_and_full_videos_in_silver.py"

:: Iterate over each .3dm file in the current directory
for %%i in (*.3dm) do (
    echo Processing file: %%i
    start "" "C:\Program Files\Rhino 7\System\Rhino.exe" "%%~fi" /runscript="_-RunPythonScript ""%PYTHON_SCRIPT%"""
)

endlocal