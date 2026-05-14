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
│   ├── members/                # Dữ liệu thô + file Excel gán nhãn theo từng thành viên
│   │   └── generated_vinumfcr_200_samples.xlsx   # Dataset gốc 200 mẫu đã gán nhãn
│   ├── processed/              # Dữ liệu đã xử lý sẵn sàng cho model
│   │   ├── train_data.parquet
│   │   ├── val_data.parquet
│   │   ├── test_data.parquet
│   │   ├── finetuned_results.csv   # Output: kết quả dự đoán của mô hình
│   │   └── error_analysis.csv      # Output: các câu AI dự đoán sai
│   └── utils/
│       └── preprocess_dataset.py   # Chuyển Excel → parquet, chia train/val/test
├── models/
│   ├── plms/
│   │   └── finetune_phobert.py     # Fine-tuning PhoBERT (chạy local)
│   └── prompts/
│       └── zero_shot.json          # System prompt & user prompt cho LLM
├── notebooks/
│   ├── EDA_Dataset.py              # Phân tích khám phá dữ liệu (vẽ biểu đồ)
│   ├── Evaluate.py                 # Đánh giá mô hình: Accuracy, F1, Confusion Matrix
│   ├── Error_Analysis.py           # Phân tích lỗi: AI sai ở dạng toán nào
│   ├── zero_shot.json              # Prompt dùng trong Google Colab
│   └── *.ipynb                     # Notebook tương ứng (chạy trên Google Colab)
├── backend/                        # Dự phòng triển khai Demo cuối kỳ
├── frontend/                       # Dự phòng triển khai Demo cuối kỳ
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

**Bước 4 — Chạy Crawler --- tự viết hàm parsers** 

```bash
# Chạy job mặc định
python data/table_crawler/main.py

# Hoặc chỉ định job cụ thể
python data/table_crawler/main.py vietstock.chung_khoan.giao_dich_noi_bo.crawl_job
```

> **Thêm URL mới:** chỉ cần append vào `URLS_STRING_FORMAT` trong `crawl_job.py` hoặc `urls_input.py` rồi chạy lại — URL cũ tự động được bỏ qua.

---

## 🗺️ Lộ trình Dự án (Roadmap)

### ✅ Giai đoạn 1 — Thu thập & Xử lý Dữ liệu
- [x] Xây dựng hệ thống Crawler bằng Playwright đánh chặn API mạng
- [x] Ép phẳng biểu đồ tài chính thành văn bản tuyến tính (Full Context)
- [x] Thiết lập cấu trúc trường dữ liệu (Statement, Evidence, labels, Reasoning_Type…)
- [x] Kiến trúc `crawl_job.py` — mỗi thành viên tự cấu hình độc lập

### 🔜 Giai đoạn 2 — Tạo Tuyên bố & Gán nhãn thủ công
- [x] Viết câu bẫy số liệu (`Statement`) từ bài báo tài chính
- [x] Trích xuất `Evidence` từ Context
- [x] Điền nhãn: `labels` (0 = Support, 1 = Refute, 2 = NEI)
- [x] Phân loại: `Reasoning_Type`, `Evidence_Type`, `Reasoning_Steps`

### 🔜 Giai đoạn 3 — Tiền xử lý & Chuẩn bị dữ liệu
- [ ] Chuyển Excel → `.parquet` bằng `data/utils/preprocess_dataset.py`
- [ ] Chia tập Train / Val / Test (stratified theo nhãn)
- [ ] Tự động cắt ngắn Evidence > 4000 ký tự để tránh tràn bộ nhớ mô hình

### 🔜 Giai đoạn 4 — Thực nghiệm Mô hình
- [ ] Fine-tuning **Gemma-2B** (LoRA rank 16) với Unsloth trên Google Colab
- [ ] Chuyển từ `model.generate` sang **Direct Logit Scoring** để tránh hallucination
- [ ] Đánh giá hiệu suất: Accuracy 25%, Macro F1 13.33% (baseline với 200 mẫu)
- [ ] Fine-tuning **PhoBERT** (chạy local với `models/plms/finetune_phobert.py`)

### 🔜 Giai đoạn 5 — Phân tích lỗi & Viết báo cáo *(Cuối kỳ)*
- [ ] Chạy `notebooks/Error_Analysis.py` để phân tích hallucination và lỗi tính toán
- [ ] Đóng gói Demo + viết báo cáo theo template 2 cột ACL

---

## 📋 Cấu trúc Dataset

| Trường | Mô tả |
|---|---|
| `Statement` | Câu tuyên bố cần kiểm chứng (Team Data viết tay) |
| `Context` | Nội dung bài báo + bảng số liệu đã ép phẳng |
| `Evidence` | Đoạn trích dẫn hỗ trợ/bác bỏ Statement |
| `labels` | `0` Support · `1` Refute · `2` NEI |
| `annotation_id` | ID duy nhất tự sinh |
| `Reasoning_Type` | Loại suy luận (5 loại): `Toan_hoc_da_buoc` · `So_sanh_cheo` · `Chuoi_thoi_gian` · `Khong_du_thong_tin` · `Nhap_nhang_ngu_nghia` |
| `Evidence_Type` | `Text` · `Table` · `Both` |
| `Reasoning_Steps` | Số bước suy luận trung gian cần thiết (1, 2, 3…) |

---

## 🔬 Quy trình Thực nghiệm Mô hình

```
data/processed/
├── train_data.parquet  ──►  Google Colab (Fine-tune Gemma-2B)  ──►  lora_model/
├── val_data.parquet    ──►  Validation trong quá trình train
└── test_data.parquet   ──►  Inference (Direct Logit Scoring)   ──►  finetuned_results.csv
                                                                          │
                                              ┌───────────────────────────┤
                                              ▼                           ▼
                                       Evaluate.py                Error_Analysis.py
                               (Accuracy, F1, Confusion Matrix)  (Phân tích câu sai)
```