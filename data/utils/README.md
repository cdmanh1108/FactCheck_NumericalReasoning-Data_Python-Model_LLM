# 🔄 Data Converter

Tiện ích chuyển đổi dữ liệu giữa `.parquet` và `.xlsx`.

## Cách dùng

Mở file `.env` ở thư mục gốc dự án, chỉnh 2 dòng:

```env
CONVERTER_MODE=to_excel
CONVERTER_INPUT=data\members\Manh\Vietstock\chung_khoan\co_phieu\draft_crawled_data.parquet
```

Sau đó chạy:

```bash
python data/utils/converter.py
```

> File output tự động tạo **cùng thư mục** với input, chỉ đổi đuôi.  
> Muốn lưu nơi khác thì thêm `CONVERTER_OUTPUT=đường/dẫn/khác.xlsx` vào `.env`.

## Workflow gán nhãn

```
draft_crawled_data.parquet
        ↓  CONVERTER_MODE=to_excel
draft_crawled_data.xlsx       ← Team Data mở, điền Statement/Evidence/labels
        ↓  CONVERTER_MODE=to_parquet
draft_crawled_data.parquet    ← Dùng cho training model
```

## Yêu cầu

```bash
pip install openpyxl
```

