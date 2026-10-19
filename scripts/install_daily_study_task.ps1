#Requires -Version 5.1
<#
.SYNOPSIS
  매일 12:30에 전날 공부 요약을 자동 생성하는 Windows 작업 등록/갱신.
  Cursor Agent 기동 불필요. PC가 절전에서 깨어나면 놓친 실행도 재시도.
#>
$ErrorActionPreference = "Stop"

$TaskName = "261015python-DailyStudyNote"
$Repo = "C:\Users\LT-013\261015python"
$Cmd = Join-Path $Repo "scripts\run_daily_study.cmd"

if (-not (Test-Path $Cmd)) {
    throw "실행 파일 없음: $Cmd"
}

$Action = New-ScheduledTaskAction -Execute $Cmd -WorkingDirectory $Repo
$Trigger = New-ScheduledTaskTrigger -Daily -At "12:30"
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Force | Out-Null

Write-Host "등록 완료: $TaskName"
Write-Host "  실행: $Cmd"
Write-Host "  시각: 매일 12:30 (놓치면 PC 깨어난 뒤 StartWhenAvailable)"
Write-Host ""
Write-Host "지금 한 번 실행하려면:"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  또는: $Cmd --dry-run"
