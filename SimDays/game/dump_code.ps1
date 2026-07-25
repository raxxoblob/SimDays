$out = "C:\Users\oskar.bazydlo\Documents\LivingTheDream\all_code.rpy"
$game = $PSScriptRoot

$files = Get-ChildItem $game -Filter "*.rpy" | Where-Object { $_.Name -ne "dump_code.ps1" } | Sort-Object Name

$lines = foreach ($f in $files) {
    "# " + ("=" * 72)
    "# $($f.Name)"
    "# " + ("=" * 72)
    ""
    Get-Content $f.FullName -Encoding UTF8
    ""
}

$lines | Set-Content $out -Encoding UTF8
Write-Host "Written $($files.Count) files -> $out"
