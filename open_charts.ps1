Write-Host "=== VN50 Portfolio Analysis Visualizations ===" -ForegroundColor Green
Write-Host "Opening all generated charts..." -ForegroundColor Yellow

$figuresDir = "reports\figures"

if (Test-Path $figuresDir) {
    $figures = Get-ChildItem $figuresDir -Filter "*.png"
    
    Write-Host "Found $($figures.Count) visualization files:" -ForegroundColor Cyan
    foreach ($fig in $figures) {
        Write-Host "  - $($fig.Name)" -ForegroundColor White
    }
    
    Write-Host "Opening visualizations..." -ForegroundColor Green
    
    foreach ($fig in $figures) {
        Start-Process $fig.FullName
        Start-Sleep -Seconds 1
    }
    
    Write-Host "All visualizations opened!" -ForegroundColor Green
    
} else {
    Write-Host "Figures directory not found. Run visualization first!" -ForegroundColor Red
}
