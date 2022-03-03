param(
    [Switch]$LegacyBuild
)

. .\build\Initialize-VirtualEnvironment.ps1

if($LegacyBuild) {
    Initialize-VirtualEnvironment -Name "venv";    
} else {
    Initialize-VirtualEnvironment -Name "venv310";    
}
& pyinstaller --noconfirm `
    --log-level=WARN `
    --onefile `
    --noconsole `
    --strip `Y
    main.py