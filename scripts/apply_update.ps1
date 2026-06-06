Param(
    [switch]$Commit,
    [string]$Tag = ""
)

# Basit güncelleme yardımcı betiği — dikkatli kullanın.
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git bulunamadı; betik commit/tag adımlarını atlayacak." -ForegroundColor Yellow
}

Write-Host "Markdown lint (varsa) çalıştırılıyor..." -ForegroundColor Cyan
if (Get-Command markdownlint -ErrorAction SilentlyContinue) {
    markdownlint "**/*.md"
} else {
    Write-Host "markdownlint yüklü değil; atlanıyor." -ForegroundColor Yellow
}

Write-Host "Değişiklikleri gözden geçirin. -Commit parametresi verilirse commit yapılır." -ForegroundColor Cyan
if ($Commit -and (Get-Command git -ErrorAction SilentlyContinue)) {
    git add -A
    git commit -m "chore(update): 2026-06-06 — doküman ve UI placeholder'ları eklendi"
    if ($Tag -ne "") { git tag -a $Tag -m "Update package $Tag" }
    Write-Host "Commit/tag işlemi tamamlandı." -ForegroundColor Green
} else {
    Write-Host "Commit yapılmadı. Eğer yapmak istiyorsanız betiği -Commit ile çalıştırın." -ForegroundColor Yellow
}
