# VN50 Clustering + Markowitz Portfolio Optimization - Complete Pipeline
# Chạy toàn bộ pipeline từ đầu đến cuối bao gồm tạo biểu đồ

Write-Host "=== VN50 Clustering + Markowitz Portfolio Optimization ===" -ForegroundColor Green
Write-Host "Complete Pipeline with Visualizations" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

# Bước 1: Tải dữ liệu
Write-Host "`n[1/6] Fetching market data..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.fetch_data +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in data fetching!" -ForegroundColor Red
    exit 1 
}

# Bước 2: Xây dựng features
Write-Host "`n[2/6] Building features..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.build_features +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in feature building!" -ForegroundColor Red
    exit 1 
}

# Bước 3: Clustering
Write-Host "`n[3/6] Running clustering..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.run_clustering +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in clustering!" -ForegroundColor Red
    exit 1 
}

# Bước 4: Tối ưu hóa danh mục
Write-Host "`n[4/6] Optimizing portfolio..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.optimize_portfolio +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in portfolio optimization!" -ForegroundColor Red
    exit 1 
}

# Bước 5: Backtest
Write-Host "`n[5/6] Running backtest..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.backtest +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in backtesting!" -ForegroundColor Red
    exit 1 
}

# Bước 6: Tạo biểu đồ
Write-Host "`n[6/6] Creating visualizations..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.create_visualizations +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in visualization!" -ForegroundColor Red
    exit 1 
}

Write-Host "`n=== Pipeline completed successfully! ===" -ForegroundColor Green
Write-Host "Results saved in:" -ForegroundColor Yellow
Write-Host "  - Data: data/processed/" -ForegroundColor White
Write-Host "  - Results: reports/artifacts/" -ForegroundColor White
Write-Host "  - Charts: reports/figures/" -ForegroundColor White

Write-Host "`n=== Performance Summary ===" -ForegroundColor Green
if (Test-Path "reports\artifacts\metrics.csv") {
    $metrics = Import-Csv "reports\artifacts\metrics.csv"
    $row = $metrics[0]
    Write-Host "Total Return: $([math]::Round($row.total_return * 100, 2))%" -ForegroundColor Cyan
    Write-Host "Annualized Return: $([math]::Round($row.annualized_return * 100, 2))%" -ForegroundColor Cyan
    Write-Host "Sharpe Ratio: $([math]::Round($row.sharpe_ratio, 2))" -ForegroundColor Cyan
    Write-Host "Max Drawdown: $([math]::Round($row.max_drawdown * 100, 2))%" -ForegroundColor Cyan
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. View all charts: .\open_charts.ps1" -ForegroundColor White
Write-Host "2. Check portfolio weights: reports\artifacts\initial_weights.csv" -ForegroundColor White
Write-Host "3. View equity curve: reports\artifacts\equity_curve.csv" -ForegroundColor White
Write-Host "4. Read visualization guide: VISUALIZATION_GUIDE.md" -ForegroundColor White

Write-Host "`nPipeline execution completed!" -ForegroundColor Green
