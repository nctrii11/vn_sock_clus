"""
Ví dụ đọc dữ liệu từ project VN50 Clustering + Markowitz
Chạy: uv run python read_data_examples.py
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("📊 VÍ DỤ ĐỌC DỮ LIỆU - VN50 CLUSTERING + MARKOWITZ")
print("=" * 70)

# ============================================================================
# 1. ĐỌC GIÁ CỔ PHIẾU
# ============================================================================
print("\n" + "=" * 70)
print("1️⃣  GIÁ CỔ PHIẾU (PRICES)")
print("=" * 70)

prices = pd.read_parquet('data/processed/prices.parquet')
print(f"📁 File: data/processed/prices.parquet")
print(f"📐 Kích thước: {prices.shape[0]} ngày x {prices.shape[1]} cổ phiếu")
print(f"📅 Từ {prices.index.min().date()} đến {prices.index.max().date()}")
print(f"\n📋 Danh sách cổ phiếu: {', '.join(prices.columns.tolist())}")

print("\n📊 5 ngày gần nhất:")
print(prices.tail())

print("\n💰 Giá hiện tại (ngày cuối):")
current_prices = prices.iloc[-1].sort_values(ascending=False)
for ticker, price in current_prices.items():
    print(f"  {ticker:10s}: {price:>10,.0f} VND")

# ============================================================================
# 2. ĐỌC TỶ SUẤT SINH LỜI
# ============================================================================
print("\n" + "=" * 70)
print("2️⃣  TỶ SUẤT SINH LỜI (RETURNS)")
print("=" * 70)

returns = pd.read_parquet('data/processed/returns.parquet')
print(f"📁 File: data/processed/returns.parquet")
print(f"📐 Kích thước: {returns.shape}")

print("\n📈 Return trung bình hàng ngày (%):")
daily_returns = (returns.mean() * 100).sort_values(ascending=False)
for ticker, ret in daily_returns.items():
    print(f"  {ticker:10s}: {ret:>6.3f}%")

print("\n📈 Return trung bình hàng năm - Annualized (%):")
annual_returns = (returns.mean() * 252 * 100).sort_values(ascending=False)
for ticker, ret in annual_returns.items():
    print(f"  {ticker:10s}: {ret:>6.2f}%")

print("\n📊 Độ biến động (Volatility) hàng năm (%):")
volatility = (returns.std() * np.sqrt(252) * 100).sort_values()
for ticker, vol in volatility.items():
    print(f"  {ticker:10s}: {vol:>6.2f}%")

# ============================================================================
# 3. ĐỌC MA TRẬN TƯƠNG QUAN
# ============================================================================
print("\n" + "=" * 70)
print("3️⃣  MA TRẬN TƯƠNG QUAN (CORRELATION)")
print("=" * 70)

corr = pd.read_parquet('data/processed/correlation.parquet')
print(f"📁 File: data/processed/correlation.parquet")
print(f"📐 Kích thước: {corr.shape}")

print("\n🔗 Các cặp cổ phiếu có tương quan cao nhất:")
# Tìm top 5 cặp tương quan cao (không tính với chính nó)
corr_pairs = []
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        corr_pairs.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))

corr_pairs.sort(key=lambda x: x[2], reverse=True)
for stock1, stock2, corr_val in corr_pairs[:5]:
    print(f"  {stock1:10s} - {stock2:10s}: {corr_val:>6.3f}")

print("\n🔗 Các cặp cổ phiếu có tương quan thấp nhất:")
for stock1, stock2, corr_val in corr_pairs[-5:]:
    print(f"  {stock1:10s} - {stock2:10s}: {corr_val:>6.3f}")

# ============================================================================
# 4. ĐỌC KẾT QUẢ CLUSTERING
# ============================================================================
print("\n" + "=" * 70)
print("4️⃣  PHÂN NHÓM CỔ PHIẾU (CLUSTERING)")
print("=" * 70)

clusters = pd.read_parquet('data/processed/cluster_labels.parquet')
print(f"📁 File: data/processed/cluster_labels.parquet")
print(f"📐 Số cổ phiếu: {len(clusters)}")
print(f"📐 Số nhóm: {clusters['cluster'].nunique()}")

print("\n📊 Phân bổ theo nhóm:")
for cluster_id in sorted(clusters['cluster'].unique()):
    stocks = clusters[clusters['cluster'] == cluster_id].index.tolist()
    print(f"\n  🔸 Nhóm {cluster_id} ({len(stocks)} cổ phiếu):")
    print(f"     {', '.join(stocks)}")

# ============================================================================
# 5. ĐỌC TRỌNG SỐ DANH MỤC
# ============================================================================
print("\n" + "=" * 70)
print("5️⃣  TRỌNG SỐ DANH MỤC TỐI ƯU (PORTFOLIO WEIGHTS)")
print("=" * 70)

weights = pd.read_csv('reports/artifacts/initial_weights.csv', index_col=0)
weights.columns = ['weight']
weights_filtered = weights[weights['weight'] > 0.001].sort_values('weight', ascending=False)

print(f"📁 File: reports/artifacts/initial_weights.csv")
print(f"📐 Tổng số cổ phiếu trong danh mục: {len(weights_filtered)}")
print(f"📐 Tổng trọng số: {weights_filtered['weight'].sum():.4f}")

print("\n💼 Phân bổ danh mục:")
for ticker, row in weights_filtered.iterrows():
    weight_pct = row['weight'] * 100
    bar_length = int(weight_pct)
    bar = "█" * bar_length
    print(f"  {ticker:10s}: {weight_pct:>5.2f}% {bar}")

# ============================================================================
# 6. ĐỌC KẾT QUẢ BACKTEST
# ============================================================================
print("\n" + "=" * 70)
print("6️⃣  KẾT QUẢ BACKTEST")
print("=" * 70)

metrics = pd.read_csv('reports/artifacts/metrics.csv', index_col=0)
print(f"📁 File: reports/artifacts/metrics.csv")

print("\n📊 Chỉ số hiệu suất:")
metric_names = {
    'total_return': 'Tổng lợi nhuận',
    'annualized_return': 'Lợi nhuận hàng năm',
    'volatility': 'Độ biến động',
    'sharpe_ratio': 'Sharpe Ratio',
    'sortino_ratio': 'Sortino Ratio',
    'calmar_ratio': 'Calmar Ratio',
    'max_drawdown': 'Max Drawdown',
    'hit_ratio': 'Tỷ lệ thắng'
}

for metric_key, metric_label in metric_names.items():
    if metric_key in metrics.columns:
        value = metrics[metric_key].iloc[0]
        if metric_key in ['total_return', 'annualized_return', 'volatility', 'max_drawdown', 'hit_ratio']:
            print(f"  {metric_label:25s}: {value*100:>8.2f}%")
        else:
            print(f"  {metric_label:25s}: {value:>8.2f}")

# ============================================================================
# 7. ĐỌC EQUITY CURVE
# ============================================================================
print("\n" + "=" * 70)
print("7️⃣  ĐƯỜNG VỐN (EQUITY CURVE)")
print("=" * 70)

equity = pd.read_csv('reports/artifacts/equity_curve.csv', index_col=0, parse_dates=True)
print(f"📁 File: reports/artifacts/equity_curve.csv")
print(f"📐 Số ngày: {len(equity)}")

print("\n📈 Thống kê equity curve:")
print(f"  Vốn ban đầu:        {equity['equity'].iloc[0]:>12.2f}")
print(f"  Vốn cuối kỳ:        {equity['equity'].iloc[-1]:>12.2f}")
print(f"  Tăng trưởng:        {(equity['equity'].iloc[-1] / equity['equity'].iloc[0] - 1) * 100:>11.2f}%")
print(f"  Vốn cao nhất:       {equity['equity'].max():>12.2f}")
print(f"  Vốn thấp nhất:      {equity['equity'].min():>12.2f}")

print("\n📊 10 ngày gần nhất:")
print(equity.tail(10))

print("\n" + "=" * 70)
print("✅ HOÀN THÀNH! Đã đọc tất cả dữ liệu thành công!")
print("=" * 70)
