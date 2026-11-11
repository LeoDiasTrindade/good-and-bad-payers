[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$paperDirectory = $PSScriptRoot
$projectDirectory = Split-Path (Split-Path $paperDirectory -Parent) -Parent
$portableCompiler = Join-Path $projectDirectory '.qa-runtime\tectonic\tectonic.exe'
$buildDirectory = Join-Path $paperDirectory 'build'
$tectonicCommand = Get-Command tectonic -ErrorAction SilentlyContinue
$latexmkCommand = Get-Command latexmk -ErrorAction SilentlyContinue
$previousCache = $env:TECTONIC_CACHE_DIR

Push-Location $paperDirectory
try {
    New-Item -ItemType Directory -Force -Path $buildDirectory | Out-Null
    if ($tectonicCommand -or (Test-Path -LiteralPath $portableCompiler)) {
        $compiler = if ($tectonicCommand) { $tectonicCommand.Source } else { $portableCompiler }
        $env:TECTONIC_CACHE_DIR = Join-Path $projectDirectory '.qa-runtime\tectonic-cache'
        New-Item -ItemType Directory -Force -Path $env:TECTONIC_CACHE_DIR | Out-Null
        & $compiler --untrusted --keep-logs --outdir $buildDirectory main.tex
    } elseif ($latexmkCommand) {
        & $latexmkCommand.Source -pdf main.tex
    } else {
        throw 'Instale Tectonic ou uma distribuicao LaTeX com latexmk. Veja README.md.'
    }
    if ($LASTEXITCODE -ne 0) {
        throw "A compilacao LaTeX falhou (codigo $LASTEXITCODE). Consulte build/main.log."
    }
    Copy-Item -LiteralPath (Join-Path $buildDirectory 'main.pdf') -Destination (Join-Path $paperDirectory 'main.pdf') -Force
    Write-Output "PDF atualizado: $(Join-Path $paperDirectory 'main.pdf')"
} finally {
    $env:TECTONIC_CACHE_DIR = $previousCache
    Pop-Location
}
