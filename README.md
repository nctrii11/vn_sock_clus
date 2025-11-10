# VN50 Phân cụm + Markowitz

Pipeline hoàn chỉnh để tối ưu hóa danh mục đầu tư VN30/VN50 dựa trên phân cụm phân cấp và tối ưu hóa trung bình-phương sai Markowitz.

## Tổng quan Dự án

Dự án này triển khai một pipeline nghiên cứu định lượng hoàn chỉnh:

- **Thu thập Dữ liệu**: Dữ liệu cổ phiếu VN30/VN50 qua vnstock
- **Xây dựng Đặc trưng**: Lợi nhuận, chỉ số rủi ro, ma trận tương quan
- **Phân cụm**: Phân cụm phân cấp để nhóm tài sản
- **Tối ưu hóa**: Tối ưu hóa danh mục trung bình-phương sai Markowitz
- **Kiểm định lại**: Kiểm định với các chỉ số hiệu suất
- **Trực quan hóa**: Biểu đồ và bảng điều khiển chuyên nghiệp

## Công nghệ Sử dụng

- Python 3.11
- **uv** để quản lý môi trường và phụ thuộc
- Hydra/OmegaConf để cấu hình
- NumPy/SciPy/Pandas để xử lý dữ liệu
- CVXPY để tối ưu hóa lồi
- matplotlib/seaborn để trực quan hóa
- pytest để kiểm thử

## Bắt đầu Nhanh

### 1. Thiết lập Môi trường

```bash
# Cài đặt uv (nếu chưa có)
pipx install uv

# Tạo môi trường ảo
make venv

# Cài đặt các phụ thuộc
make install
```

Trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
make install
```

Trên Linux/Mac:

```bash
source .venv/bin/activate
make install
```

### 2. Chạy Pipeline Đầy đủ

**Tùy chọn A: Pipeline hoàn chỉnh với trực quan hóa**

```bash
make all         # Chạy tất cả các bước bao gồm trực quan hóa
```

**Tùy chọn B: Các bước riêng lẻ**

```bash
make data        # Thu thập dữ liệu thị trường
make features    # Xây dựng đặc trưng (lợi nhuận, tương quan, v.v.)
make cluster     # Chạy phân cụm phân cấp
make opt         # Tối ưu hóa danh mục
make backtest    # Chạy kiểm định lại
make visualize   # Tạo biểu đồ
```

**Tùy chọn C: Scripts PowerShell (Windows)**

```powershell
# Pipeline hoàn chỉnh với trực quan hóa
.\run_complete_pipeline.ps1

# Xem tất cả biểu đồ đã tạo
.\open_charts.ps1
```

### 3. Chạy Kiểm thử

```bash
make test
```

### 4. Kiểm tra Mã nguồn

```bash
make lint
```

## Cấu trúc Dự án

```
vn50-cluster-markowitz/
├── configs/           # Các file cấu hình Hydra
├── data/             # Dữ liệu thô, trung gian, đã xử lý, cache
├── reports/          # Biểu đồ và sản phẩm
├── src/vn50/         # Mã nguồn
│   ├── utils/        # Tiện ích (io, logging)
│   ├── data/         # Thu thập và tiền xử lý dữ liệu
│   ├── features/     # Lợi nhuận, rủi ro, tương quan
│   ├── clustering/   # Phân cụm phân cấp
│   ├── optimize/     # Tối ưu hóa Markowitz
│   ├── backtest/     # Công cụ kiểm định và chỉ số
│   ├── visualization/ # Biểu đồ và bảng điều khiển
│   └── cli/          # Điểm vào CLI
└── tests/            # Bộ kiểm thử
```

## Cấu hình

Tất cả tham số được quản lý qua cấu hình Hydra trong `configs/`:

- `base.yaml`: Giá trị mặc định toàn cục
- `data.yaml`: Nguồn dữ liệu và ký hiệu
- `features.yaml`: Tham số xây dựng đặc trưng
- `cluster_hclust.yaml`: Cấu hình phân cụm
- `optimizer_markowitz.yaml`: Cài đặt tối ưu hóa
- `experiment_hclust.yaml`: Cấu hình thí nghiệm hoàn chỉnh

## Phát triển

### Thêm Tính năng Mới

1. Đặt các hàm tính toán thuần túy vào các module phù hợp (`features/`, `clustering/`, `optimize/`)
2. Thêm logic I/O vào `utils/io.py` hoặc các module CLI
3. Viết kiểm thử trong `tests/`
4. Cập nhật cấu hình nếu cần tham số mới
5. Chạy `make test` và `make lint`

### Tiêu chuẩn Mã nguồn

- Sử dụng `uv run` cho tất cả lệnh Python
- Tất cả tham số từ cấu hình Hydra (`cfg`)
- I/O chỉ trong `utils/io.py` hoặc các module CLI
- Hàm thuần túy cho tính toán
- Ghi log qua `utils.logging.task()`
- Viết kiểm thử cho các hàm mới

## 📊 Trực quan hóa

Dự án bao gồm các trực quan hóa toàn diện:

### Biểu đồ Được tạo

- **Biến động Giá**: Biến động giá cổ phiếu chuẩn hóa
- **Ma trận Tương quan**: Ma trận tương quan cổ phiếu
- **Tỷ trọng Danh mục**: Phân bổ danh mục tối ưu
- **Đường cong Vốn**: Hiệu suất danh mục theo thời gian
- **Chỉ số Trượt**: Xu hướng chỉ số Sharpe và độ biến động
- **Phân tích Sụt giảm**: Phân tích rủi ro và giai đoạn sụt giảm
- **Tóm tắt Hiệu suất**: Bảng điều khiển hiệu suất toàn diện

### Sử dụng

```bash
# Tạo tất cả trực quan hóa
make visualize

# Xem biểu đồ (Windows)
.\open_charts.ps1
```

### Tùy chỉnh

- Chỉnh sửa `src/vn50/visualization/plots.py` để tạo biểu đồ tùy chỉnh
- Điều chỉnh màu sắc, kích thước và kiểu dáng
- Thêm các hàm trực quan hóa mới

Xem `VISUALIZATION_GUIDE.md` để biết tài liệu chi tiết.

## Giấy phép

MIT
