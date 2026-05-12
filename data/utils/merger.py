"""
Gộp tất cả file draft_crawled_data.parquet trong data/members/ thành 1 file duy nhất.
Reset cột index tuần tự sau khi gộp.

Cấu hình trong .env:
    MERGE_OUTPUT=data\members\merged_dataset.parquet   # để trống = dùng mặc định

Chạy: python data/utils/merger.py
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

DATA_DIR = Path(__file__).parent.parent  # trỏ vào /data


def merge_parquets(output_path: str | Path = None, source_dir: str | Path = None) -> Path:
    """
    Quét đệ quy source_dir để tìm tất cả draft_crawled_data.parquet, gộp lại thành 1 file.

    Args:
        output_path: File đầu ra. Mặc định: data/members/merged_dataset.parquet
        source_dir : Thư mục gốc để quét. Mặc định: data/members/
    """
    source_dir = Path(source_dir) if source_dir else DATA_DIR / "members"
    files = sorted(source_dir.rglob("draft_crawled_data.parquet"))

    if not files:
        print(f"⚠️ Không tìm thấy file .parquet nào trong {source_dir}")
        return None

    print(f"📂 Tìm thấy {len(files)} file:")
    dfs = []
    for f in files:
        df = pd.read_parquet(f)
        print(f"   - {f.relative_to(DATA_DIR)} ({len(df)} dòng)")
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)
    merged["index"] = range(1, len(merged) + 1)

    output_path = Path(output_path) if output_path else DATA_DIR / "members" / "merged_dataset.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(output_path, index=False)
    print(f"✅ Đã gộp {len(merged)} dòng → {output_path}")
    return output_path


# ================================================================
# Cấu hình trong .env:
#   MERGE_OUTPUT=data\members\merged_dataset.parquet  # tuỳ chọn
# Chạy: python data/utils/merger.py
# ================================================================
if __name__ == "__main__":
    OUTPUT = os.getenv("MERGE_OUTPUT") or None
    merge_parquets(output_path=OUTPUT)
