function Initialize-VirtualEnvironment {
    [CmdletBinding()]
    param(
        [string]$Name = "venv",
        [string]$Location = $PWD
    )
    $locations = @("Scripts", "bin");
    $results = @{};
    foreach ($dir in Get-ChildItem $Location -Directory -Filter $Name) {
        $dirName = $dir.Name;
        foreach($location in $locations) {
            $activatePath = Join-Path -Path $dir -ChildPath $location -AdditionalChildPath "Activate.ps1"; 
            if (Test-Path -Path $activatePath) {
                Write-Verbose "Virtual environment detected at '$dirName'!";
                $results[$dirName] = $activatePath;
            }
        }
    }

    if ($results.Count -eq 0) {
        Write-Host "No virtual environment found";
        return;        
    } 
    . $results[$results.Keys[0]];        

    return;
}
