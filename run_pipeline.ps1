# VN50 Clustering + Markowitz Pipeline Runner
# Chạy toàn bộ pipeline từ đầu đến cuối

Write-Host "=== VN50 Clustering + Markowitz Portfolio Optimization ===" -ForegroundColor Green
Write-Host "Starting pipeline execution..." -ForegroundColor Yellow

# Bước 1: Tải dữ liệu
Write-Host "`n[1/5] Fetching market data..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.fetch_data +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in data fetching!" -ForegroundColor Red
    exit 1 
}

# Bước 2: Xây dựng features
Write-Host "`n[2/5] Building features..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.build_features +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in feature building!" -ForegroundColor Red
    exit 1 
}

# Bước 3: Clustering
Write-Host "`n[3/5] Running clustering..." -ForegroundColor Cyan
uv run python -m src.vn50.cli.run_clustering +experiment=experiment_hclust
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in clustering!" -ForegroundColor Red
    exit 1 
}

# Bước 4: Tối ưu hóa danh mục
Write-Host "`n[4/5] Optimizing portfolio..." -ForegroundColor Cyan
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
Write-Host "`nTo view all charts, run: .\view_charts.ps1" -ForegroundColor Cyan
