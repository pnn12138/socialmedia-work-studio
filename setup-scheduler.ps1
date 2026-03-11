# 设置定时备份任务（每 30 分钟自动备份）
# 需要管理员权限运行

$taskName = "Obsidian-AutoBackup"
$scriptPath = "C:\Users\pnn\Desktop\socialmedia-work-studio\backup.ps1"
$triggerTime = (Get-Date).AddMinutes(2)  # 2 分钟后开始

# 检查是否已存在
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "⚠️  任务已存在，先删除..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# 创建定时任务
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger -Once -At $triggerTime `
    -RepetitionInterval (New-TimeSpan -Minutes 30) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "每 30 分钟自动备份 Obsidian 仓库到 GitHub"

Write-Host "✅ 定时任务已创建！" -ForegroundColor Green
Write-Host "📅 任务名称：$taskName"
Write-Host "⏰ 首次运行：$triggerTime"
Write-Host "🔁 重复间隔：每 30 分钟"
Write-Host ""
Write-Host "查看任务状态：" -NoNewline
Write-Host "Get-ScheduledTask -TaskName $taskName" -ForegroundColor Cyan
Write-Host "手动运行测试：" -NoNewline
Write-Host "Start-ScheduledTask -TaskName $taskName" -ForegroundColor Cyan
