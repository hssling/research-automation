param(
    [string]$ProjectPath,
    [string]$ScriptName,
    [switch]$Silent
)

# PowerShell helper function to run R scripts with automatic path and quoting handling
function Run-RScript {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ProjectDir,

        [Parameter(Mandatory=$true)]
        [string]$ScriptName,

        [switch]$Silent
    )

    # Navigate to project directory
    Push-Location $ProjectDir

    try {
        # Get full path to R executable (R 4.5.1)
        $rExePath = "C:\Program Files\R\R-4.5.1\bin\x64\R.exe"

        if (-not (Test-Path $rExePath)) {
            throw "R executable not found at: $rExePath"
        }

        $scriptPath = Join-Path $ProjectDir $ScriptName

        if (-not (Test-Path $scriptPath)) {
            throw "R script not found: $scriptPath"
        }

        # Run the R script using CMD BATCH for consistent output
        $cmdArgs = "CMD BATCH --vanilla `"$scriptPath`""

        if (-not $Silent) {
            Write-Host "Running R script in: $ProjectDir" -ForegroundColor Green
            Write-Host "Script: $ScriptName" -ForegroundColor Green
            Write-Host "Command: & `"$rExePath`" $cmdArgs" -ForegroundColor Yellow
        }

        # Execute R with proper path handling
        & $rExePath CMD BATCH --vanilla $scriptPath

        # Check if output file was created
        $routFile = [System.IO.Path]::ChangeExtension($scriptPath, "Rout")
        if (Test-Path $routFile) {
            if (-not $Silent) {
                Write-Host "R output file created: $routFile" -ForegroundColor Green
                Write-Host "Last 10 lines of output:" -ForegroundColor Cyan
                Get-Content $routFile -Tail 10 | ForEach-Object { Write-Host "  $_" }
            }
        } else {
            Write-Host "Warning: No Rout file generated" -ForegroundColor Yellow
        }

    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        # Always return to original location
        Pop-Location
    }
}

# Call the function with provided parameters
Run-RScript -ProjectDir $ProjectPath -ScriptName $ScriptName -Silent:$Silent
