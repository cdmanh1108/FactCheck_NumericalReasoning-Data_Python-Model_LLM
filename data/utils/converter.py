"""
Chuyển đổi định dạng file dữ liệu:
  - parquet_to_excel : .parquet → .xlsx  (để gán nhãn bằng Excel)
  - excel_to_parquet : .xlsx   → .parquet (sau khi gán nhãn xong)

Cấu hình trong .env:
    CONVERTER_MODE=to_excel          # to_excel | to_parquet
    CONVERTER_INPUT=data\members\...\draft_crawled_data.parquet
    CONVERTER_OUTPUT=                # để trống = cùng thư mục, đổi đuôi tự động

Chạy: python data/utils/converter.py
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")


def parquet_to_excel(input_path: str | Path, output_path: str | Path = None) -> Path:
    """Chuyển .parquet → .xlsx. output mặc định cùng thư mục, đổi đuôi .xlsx."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_path}")

    output_path = Path(output_path) if output_path else input_path.with_suffix(".xlsx")
    pd.read_parquet(input_path).to_excel(output_path, index=False, engine="openpyxl")
    print(f"✅ parquet → excel: {output_path}")
    return output_path


def excel_to_parquet(input_path: str | Path, output_path: str | Path = None) -> Path:
    """Chuyển .xlsx → .parquet. output mặc định cùng thư mục, đổi đuôi .parquet."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_path}")

    output_path = Path(output_path) if output_path else input_path.with_suffix(".parquet")
    pd.read_excel(input_path, engine="openpyxl").to_parquet(output_path, index=False)
    print(f"✅ excel → parquet: {output_path}")
    return output_path


if __name__ == "__main__":
    MODE   = os.getenv("CONVERTER_MODE", "to_excel")
    INPUT  = os.getenv("CONVERTER_INPUT")
    OUTPUT = os.getenv("CONVERTER_OUTPUT") or None

    if not INPUT:
        print("❌ Chưa có CONVERTER_INPUT trong .env")
    elif MODE == "to_excel":
        parquet_to_excel(INPUT, OUTPUT)
    elif MODE == "to_parquet":
        excel_to_parquet(INPUT, OUTPUT)
    else:
        print(f"❌ CONVERTER_MODE không hợp lệ: '{MODE}'. Dùng 'to_excel' hoặc 'to_parquet'")
