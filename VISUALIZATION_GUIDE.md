# 📊 VN50 Portfolio Visualization Guide

## 🎨 Biểu đồ đã tạo

Sau khi chạy pipeline, bạn sẽ có **7 biểu đồ trực quan** trong thư mục `reports/figures/`:

### 1. 📈 **Price Evolution** (`price_evolution.png`)

- **Mô tả**: Biểu đồ giá cổ phiếu chuẩn hóa (base = 100)
- **Thông tin**: Hiển thị sự biến động giá của tất cả 14 cổ phiếu VN30 từ 2020-2025
- **Màu sắc**: Mỗi cổ phiếu có màu riêng để dễ phân biệt

### 2. 🔥 **Correlation Heatmap** (`correlation_heatmap.png`)

- **Mô tả**: Ma trận tương quan giữa các cổ phiếu
- **Thông tin**:
  - Màu đỏ: Tương quan dương cao
  - Màu xanh: Tương quan âm
  - Giá trị từ -1 đến +1
- **Ứng dụng**: Giúp hiểu mối quan hệ giữa các cổ phiếu

### 3. 🎯 **Portfolio Weights** (`portfolio_weights.png`)

- **Mô tả**: Trọng số danh mục đầu tư được tối ưu
- **Thông tin**:
  - Chỉ hiển thị cổ phiếu có trọng số > 0.1%
  - Màu sắc theo độ lớn trọng số
  - Giá trị phần trăm trên mỗi thanh
- **Kết quả**: 8 cổ phiếu được chọn với trọng số tối đa 15%

### 4. 📊 **Equity Curve** (`equity_curve.png`)

- **Mô tả**: Đường cong tăng trưởng danh mục theo thời gian
- **Thông tin**:
  - Trục Y: Lợi nhuận tích lũy (%)
  - Trục X: Thời gian (2020-2025)
  - Đường cong mượt mà thể hiện hiệu suất
- **Kết quả**: Tăng trưởng 47.26% trong 5 năm

### 5. 📉 **Rolling Metrics** (`rolling_metrics.png`)

- **Mô tả**: Chỉ số Sharpe và Volatility theo cửa sổ trượt 252 ngày
- **Thông tin**:
  - **Sharpe Ratio**: Đường màu cam, ngưỡng = 1
  - **Volatility**: Đường màu đỏ, đơn vị %
- **Ứng dụng**: Theo dõi chất lượng danh mục theo thời gian

### 6. 📉 **Drawdown Analysis** (`drawdown.png`)

- **Mô tả**: Phân tích drawdown của danh mục
- **Thông tin**:
  - **Biểu đồ trên**: Đường cong equity
  - **Biểu đồ dưới**: Vùng drawdown (màu đỏ)
- **Kết quả**: Max drawdown = -11.38%

### 7. 🎯 **Performance Summary** (`performance_summary.png`)

- **Mô tả**: Dashboard tổng hợp các chỉ số hiệu suất
- **Thông tin**:
  - **Key Metrics**: Total Return, Annualized Return, Volatility, Sharpe Ratio
  - **Risk Metrics**: Max Drawdown, Sortino Ratio, Calmar Ratio
  - **Hit Ratio**: Pie chart tỷ lệ ngày thắng/thua
  - **Performance Scores**: So sánh các chỉ số

## 🚀 Cách sử dụng

### **Chạy tạo biểu đồ:**

```bash
# Chỉ tạo biểu đồ (sau khi đã chạy pipeline)
uv run python -m src.vn50.cli.create_visualizations +experiment=experiment_hclust

# Hoặc dùng Makefile
make visualize
```

### **Xem tất cả biểu đồ:**

```bash
# Mở tất cả biểu đồ cùng lúc
.\view_charts.ps1
```

### **Chạy toàn bộ pipeline + biểu đồ:**

```bash
# Chạy từ đầu đến cuối bao gồm tạo biểu đồ
.\run_pipeline.ps1
```

## 🎨 Tùy chỉnh biểu đồ

### **Thay đổi màu sắc:**

Chỉnh sửa file `src/vn50/visualization/plots.py`:

```python
# Thay đổi palette màu
sns.set_palette("viridis")  # hoặc "Set2", "husl", "coolwarm"

# Thay đổi màu cụ thể
colors = ['#2E86AB', '#F18F01', '#C73E1D', '#A23B72']
```

### **Thay đổi kích thước:**

```python
# Tăng kích thước biểu đồ
fig, ax = plt.subplots(figsize=(20, 12))  # thay vì (15, 8)
```

### **Thêm biểu đồ mới:**

```python
def plot_custom_chart(data):
    fig, ax = plt.subplots(figsize=(12, 8))
    # Code tạo biểu đồ
    return fig
```

## 📁 Cấu trúc thư mục

```
reports/
├── artifacts/          # Dữ liệu kết quả
│   ├── equity_curve.csv
│   ├── initial_weights.csv
│   └── metrics.csv
└── figures/            # Biểu đồ trực quan
    ├── price_evolution.png
    ├── correlation_heatmap.png
    ├── portfolio_weights.png
    ├── equity_curve.png
    ├── rolling_metrics.png
    ├── drawdown.png
    └── performance_summary.png
```

## 🔧 Troubleshooting

### **Lỗi matplotlib:**

```bash
# Cài đặt lại matplotlib
uv add matplotlib seaborn
```

### **Lỗi font:**

```python
# Thêm vào đầu file plots.py
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
```

### **Biểu đồ không hiển thị:**

```bash
# Kiểm tra backend
python -c "import matplotlib; print(matplotlib.get_backend())"
```

## 📈 Kết quả mong đợi

Sau khi chạy thành công, bạn sẽ có:

- ✅ **7 biểu đồ chất lượng cao** (300 DPI)
- ✅ **Màu sắc chuyên nghiệp** và dễ đọc
- ✅ **Thông tin chi tiết** về hiệu suất danh mục
- ✅ **Dashboard tổng hợp** các chỉ số quan trọng

---

**💡 Tip**: Chạy `.\view_charts.ps1` để mở tất cả biểu đồ cùng lúc và so sánh kết quả!
