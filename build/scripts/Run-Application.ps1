param(
    [Switch]$Legacy
)
. .\build\Initialize-VirtualEnvironment.ps1
if ($Legacy) {
    Initialize-VirtualEnvironment "venv";
} else {
    Initialize-VirtualEnvironment "venv310";
}
& python.exe main.py;