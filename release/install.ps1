# Copies every Ultimate Anime theme into each Discord client mod found on this computer.
# Usage: double-click install.bat, or run .\install.ps1 [themes folder]
param([string]$Target)
$ErrorActionPreference = 'Stop'

$themes = Get-ChildItem -Path (Join-Path $PSScriptRoot 'themes') -Filter '*.theme.css'
$plugin = Join-Path $PSScriptRoot 'plugins\UltimateAnimeSwitcher.plugin.js'

function Copy-Themes($name, $folder) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    $themes | Copy-Item -Destination $folder -Force
    Write-Host "Installed $($themes.Count) themes for ${name}: $folder"
}

if ($Target) {
    Copy-Themes 'your folder' $Target
    exit 0
}

$clients = [ordered]@{
    'Vencord'       = Join-Path $env:APPDATA 'Vencord'
    'Vesktop'       = Join-Path $env:APPDATA 'vesktop'
    'BetterDiscord' = Join-Path $env:APPDATA 'BetterDiscord'
}
$found = $false
foreach ($name in $clients.Keys) {
    $dir = $clients[$name]
    if (-not (Test-Path $dir)) { continue }
    Copy-Themes $name (Join-Path $dir 'themes')
    if ($name -eq 'BetterDiscord') {
        $plugins = Join-Path $dir 'plugins'
        New-Item -ItemType Directory -Force -Path $plugins | Out-Null
        Copy-Item $plugin -Destination $plugins -Force
        Write-Host "Installed the UltimateAnimeSwitcher plugin: $plugins"
    }
    $found = $true
}

if (-not $found) {
    Write-Host "Couldn't find Vencord, Vesktop or BetterDiscord."
    Write-Host "Run .\install.ps1 <your themes folder>, or copy the files in themes\ there yourself."
    exit 1
}

Write-Host ''
Write-Host 'Done! Open Discord settings > Themes and turn on ONE character.'
