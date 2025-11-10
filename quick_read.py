"""
Quick Examples - Đọc dữ liệu nhanh
Chạy: uv run python quick_read.py
"""

import pandas as pd

# ============================================================================
# CÁCH 1: ĐỌC 1 CỔ PHIẾU CỤ THỂ
# ============================================================================
print("=== ĐỌC DỮ LIỆU 1 CỔ PHIẾU: VIC.VN ===\n")

prices = pd.read_parquet('data/processed/prices.parquet')
vic_price = prices['VIC.VN']

print(f"Giá VIC.VN:")
print(f"  Hiện tại: {vic_price.iloc[-1]:,.0f} VND")
print(f"  Cao nhất: {vic_price.max():,.0f} VND")
print(f"  Thấp nhất: {vic_price.min():,.0f} VND")
print(f"  Trung bình: {vic_price.mean():,.0f} VND")

# ============================================================================
# CÁCH 2: ĐỌC NHIỀU CỔ PHIẾU
# ============================================================================
print("\n=== ĐỌC DỮ LIỆU NHIỀU CỔ PHIẾU ===\n")

# Chỉ đọc 3 cổ phiếu
selected_stocks = ['VIC.VN', 'FPT.VN', 'TCB.VN']
prices_selected = pd.read_parquet(
    'data/processed/prices.parquet',
    columns=selected_stocks
)

print("Giá 5 ngày gần nhất của 3 cổ phiếu:")
print(prices_selected.tail())

# ============================================================================
# CÁCH 3: LỌC THEO THỜI GIAN
# ============================================================================
print("\n=== LỌC DỮ LIỆU THEO THỜI GIAN ===\n")

# Chỉ lấy dữ liệu 2024-2025
prices_2024 = prices.loc['2024-01-01':]

print(f"Dữ liệu từ 2024:")
print(f"  Số ngày: {len(prices_2024)}")
print(f"  Từ: {prices_2024.index.min().date()}")
print(f"  Đến: {prices_2024.index.max().date()}")

# ============================================================================
# CÁCH 4: TÍNH TOÁN NHANH
# ============================================================================
print("\n=== TÍNH TOÁN NHANH ===\n")

# Tính tăng trưởng từ đầu năm 2024
ytd_returns = (prices_2024.iloc[-1] / prices_2024.iloc[0] - 1) * 100

print("Tăng trưởng từ đầu 2024 (%):")
for ticker, ret in ytd_returns.sort_values(ascending=False).items():
    print(f"  {ticker:10s}: {ret:>6.2f}%")

# ============================================================================
# CÁCH 5: SO SÁNH 2 CỔ PHIẾU
# ============================================================================
print("\n=== SO SÁNH 2 CỔ PHIẾU: VIC vs FPT ===\n")

vic = prices['VIC.VN']
fpt = prices['FPT.VN']

vic_return = (vic.iloc[-1] / vic.iloc[0] - 1) * 100
fpt_return = (fpt.iloc[-1] / fpt.iloc[0] - 1) * 100

print(f"VIC.VN:")
print(f"  Giá đầu: {vic.iloc[0]:,.0f}")
print(f"  Giá cuối: {vic.iloc[-1]:,.0f}")
print(f"  Tăng trưởng: {vic_return:.2f}%")

print(f"\nFPT.VN:")
print(f"  Giá đầu: {fpt.iloc[0]:,.0f}")
print(f"  Giá cuối: {fpt.iloc[-1]:,.0f}")
print(f"  Tăng trưởng: {fpt_return:.2f}%")

# ============================================================================
# CÁCH 6: TÌM CỔ PHIẾU TỐT NHẤT
# ============================================================================
print("\n=== TOP 5 CỔ PHIẾU TĂNG TRƯỞNG TỐT NHẤT ===\n")

total_returns = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
top5 = total_returns.sort_values(ascending=False).head(5)

for rank, (ticker, ret) in enumerate(top5.items(), 1):
    print(f"  {rank}. {ticker:10s}: {ret:>7.2f}%")

# ============================================================================
# CÁCH 7: ĐỌC PORTFOLIO WEIGHTS
# ============================================================================
print("\n=== DANH MỤC ĐẦU TƯ CỦA BẠN ===\n")

weights = pd.read_csv('reports/artifacts/initial_weights.csv', index_col=0)
weights.columns = ['weight']

# Chỉ lấy cổ phiếu được chọn
portfolio = weights[weights['weight'] > 0.001].sort_values('weight', ascending=False)

print("Cổ phiếu trong danh mục:")
for ticker, row in portfolio.iterrows():
    weight = row['weight'] * 100
    current_price = prices.loc[prices.index[-1], ticker]
    print(f"  {ticker:10s}: {weight:>5.2f}% - Giá: {current_price:>10,.0f} VND")

# Tính giá trị danh mục nếu đầu tư 100 triệu
capital = 100_000_000  # 100 triệu VND
print(f"\nNếu đầu tư {capital:,} VND:")
for ticker, row in portfolio.iterrows():
    amount = capital * row['weight']
    current_price = prices.loc[prices.index[-1], ticker]
    shares = int(amount / current_price / 100) * 100  # Làm tròn lô 100
    print(f"  {ticker:10s}: {amount:>15,.0f} VND ≈ {shares:>6,} cp")

print("\n✅ Hoàn thành!")
