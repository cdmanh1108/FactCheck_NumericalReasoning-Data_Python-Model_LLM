# 📊 ViNumFCR — Vietnamese Numerical Fact-Checking & Reasoning

> **Hệ thống xác thực tin tức Tiếng Việt tập trung vào Suy luận Số liệu (Numerical Reasoning)**  
> Đồ án môn học **IE403 — Khai thác dữ liệu truyền thông xã hội** | UIT — Nhóm 9

---

## 👥 Nhóm Thực Hiện

| Họ tên | MSSV | Vai trò |
|---|---|---|
| Châu Đức Mạnh | 22520846 | **Nhóm trưởng** |
| Thái Minh Đạt | 23520268 | Thành viên |
| Nguyễn Mạnh Tuấn | 21522755 | Thành viên |
| Nguyễn Ánh Dương | 23520351 | Thành viên |

---

## 🎯 Giới thiệu Dự án

Dự án mở rộng từ bộ dữ liệu chuẩn **ViFactCheck** (AAAI-25) theo hướng đặc thù cho bài toán **ViNumFCR** — kiểm chứng các câu tuyên bố có chứa số liệu tài chính, kết hợp chuẩn đọc bảng biểu **FEVEROUS**.

Hệ thống dùng **Python + Playwright** để:
- Thu thập và ép phẳng biểu đồ tài chính thành văn bản tuyến tính (Full Context)
- Tinh chỉnh (**Fine-tuning**) các LLM như Gemma, PhoBERT nhằm giải quyết lỗi **Chuỗi suy luận phức tạp (Complex Inferential Chain)** — nguyên nhân lớn nhất khiến AI dự đoán sai trên dữ liệu số

---

## 📂 Cấu trúc Thư mục

```
vifactcheck-numerical-project/
├── data/
│   ├── table_crawler/          # Hệ thống Crawler (Playwright) + Parser bắt API
│   │   ├── main.py             # Engine chạy chung — không cần sửa
│   │   └── vietstock/...       # crawl_job.py + urls_input.py của từng thành viên
│   ├── members/                # Dữ liệu thô .parquet đã crawl (theo từng thành viên)
│   └── data_exporter.py        # Module xuất & quản lý file parquet
├── models/                     # Model weights sau huấn luyện (Giai đoạn 4)
├── notebooks/                  # File .ipynb: chuyển đổi dữ liệu & Fine-tuning LLMs
├── backend/                    # Dự phòng triển khai Demo cuối kỳ
├── frontend/                   # Dự phòng triển khai Demo cuối kỳ
└── requirements.txt
```

---

## 🚀 Hướng dẫn Cài đặt (Dành cho Team)

Sau khi `git clone` về máy, thực hiện lần lượt:

**Bước 1 — Tạo môi trường ảo**

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**Bước 2 — Cài đặt thư viện**

```bash
pip install -r requirements.txt
```

**Bước 3 — Cài Chromium cho Playwright** *(chỉ cần 1 lần)*

```bash
python -m playwright install chromium
```

**Bước 4 — Chạy Crawler**

```bash
# Chạy job mặc định
python data/table_crawler/main.py

# Hoặc chỉ định job cụ thể
python data/table_crawler/main.py vietstock.chung_khoan.giao_dich_noi_bo.crawl_job
```

> **Thêm URL mới:** chỉ cần append vào `URLS_STRING_FORMAT` trong `crawl_job.py` hoặc `urls_input.py` rồi chạy lại — URL cũ tự động được bỏ qua.

---

## 🗺️ Lộ trình Dự án (Roadmap)

### ✅ Giai đoạn 1 — Thu thập & Xử lý Dữ liệu *(Đang thực hiện)*
- [x] Xây dựng hệ thống Crawler bằng Playwright đánh chặn API mạng
- [x] Ép phẳng biểu đồ tài chính thành văn bản tuyến tính (Full Context)
- [x] Thiết lập cấu trúc 12 trường dữ liệu (9 trường chuẩn ViFactCheck + 3 trường phân loại số liệu)
- [x] Kiến trúc `crawl_job.py` — mỗi thành viên tự cấu hình độc lập

### ⏳ Giai đoạn 2 — Tạo Tuyên bố & Gán nhãn thủ công *(Sắp tới)*
- [ ] Mở file Excel, đọc Context và sáng tạo câu bẫy số liệu (`Statement`)
- [ ] Trích xuất `Evidence` từ Context
- [ ] Điền nhãn: `labels` (0 = Support, 1 = Refute, 2 = NEI)
- [ ] Phân loại: `Reasoning_Type`, `Evidence_Type`, `Reasoning_Steps`

### 🔜 Giai đoạn 3 — Thẩm định chéo
- [ ] Đổi chéo file Excel giữa các thành viên để cross-check lỗi logic, đạt hệ số đồng thuận cao

### 🔜 Giai đoạn 4 — Thực nghiệm Mô hình
- [ ] Chuyển Excel → `.parquet`
- [ ] Fine-tuning ≥ 4 mô hình (Gemma, PhoBERT, Llama…) với Unsloth/Transformers
- [ ] Đánh giá hiệu suất trên các bẫy suy luận toán học

### 🔜 Giai đoạn 5 — Phân tích lỗi & Viết báo cáo *(Cuối kỳ)*
- [ ] Phân tích hallucination và lỗi tính toán của LLM
- [ ] Đóng gói Demo + viết báo cáo theo template 2 cột ACL

---

## 📋 Cấu trúc Dataset

| Trường | Mô tả |
|---|---|
| `Statement` | Câu tuyên bố cần kiểm chứng (Team Data viết tay) |
| `Context` | Nội dung bài báo + bảng số liệu đã ép phẳng |
| `Evidence` | Đoạn trích dẫn hỗ trợ/bác bỏ Statement |
| `Topic` | Chủ đề (VD: Chứng khoán) |
| `Author` | Nguồn dữ liệu (VD: Vietstock) |
| `Url` | URL bài báo gốc |
| `labels` | `0` Support · `1` Refute · `2` NEI · `-1` Chưa gán nhãn |
| `annotation_id` | ID duy nhất tự sinh |
| `Reasoning_Type` | Loại suy luận: `So_sanh`, `Phan_tram_vs_Tuyet_doi`, `Khuynh_huong_thoi_gian` |
| `Evidence_Type` | `Text` · `Table` · `Both` |
| `Reasoning_Steps` | Số bước suy luận trung gian cần thiết |