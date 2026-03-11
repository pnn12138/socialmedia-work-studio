# Obsidian 仓库自动备份脚本
# 用法：.\backup.ps1

$repoPath = "C:\Users\pnn\Desktop\socialmedia-work-studio"
cd $repoPath

Write-Host "🔄 开始备份 Obsidian 仓库..." -ForegroundColor Cyan

# 添加所有更改
git add -A

# 检查是否有更改
$status = git status --porcelain
if ($status) {
    # 提交更改
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "auto backup: $timestamp"
    
    # 推送到 GitHub
    Write-Host "⬆️  推送到 GitHub..." -ForegroundColor Green
    git push origin main
    
    Write-Host "✅ 备份完成！$timestamp" -ForegroundColor Green
} else {
    Write-Host "✨ 没有更改，跳过备份" -ForegroundColor Yellow
}
