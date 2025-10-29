# Script để mở tất cả biểu đồ đã tạo
Write-Host "=== VN50 Portfolio Analysis Visualizations ===" -ForegroundColor Green
Write-Host "Opening all generated charts..." -ForegroundColor Yellow

$figuresDir = "reports\figures"

if (Test-Path $figuresDir) {
    $figures = Get-ChildItem $figuresDir -Filter "*.png"
    
    Write-Host "`nFound $($figures.Count) visualization files:" -ForegroundColor Cyan
    foreach ($fig in $figures) {
        Write-Host "  - $($fig.Name)" -ForegroundColor White
    }
    
    Write-Host "`nOpening visualizations..." -ForegroundColor Green
    
    # Mở từng biểu đồ
    foreach ($fig in $figures) {
        Start-Process $fig.FullName
        Start-Sleep -Seconds 1  # Delay để tránh mở quá nhanh
    }
    
    Write-Host "`nAll visualizations opened!" -ForegroundColor Green
    Write-Host "`nChart descriptions:" -ForegroundColor Yellow
    Write-Host "  1. price_evolution.png - Biểu đồ giá cổ phiếu chuẩn hóa" -ForegroundColor White
    Write-Host "  2. correlation_heatmap.png - Ma trận tương quan giữa các cổ phiếu" -ForegroundColor White
    Write-Host "  3. portfolio_weights.png - Trọng số danh mục đầu tư" -ForegroundColor White
    Write-Host "  4. equity_curve.png - Đường cong tăng trưởng danh mục" -ForegroundColor White
    Write-Host "  5. rolling_metrics.png - Chỉ số Sharpe và Volatility theo thời gian" -ForegroundColor White
    Write-Host "  6. drawdown.png - Phân tích drawdown của danh mục" -ForegroundColor White
    Write-Host "  7. performance_summary.png - Tổng hợp các chỉ số hiệu suất" -ForegroundColor White
    
} else {
    Write-Host "Figures directory not found. Run visualization first!" -ForegroundColor Red
    Write-Host "Command: uv run python -m src.vn50.cli.create_visualizations +experiment=experiment_hclust" -ForegroundColor Yellow
}