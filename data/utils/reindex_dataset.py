import pandas as pd
import uuid
import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

def reindex_dataset():
    # Load .env từ thư mục gốc dự án (cách utils 2 cấp: data/utils -> data -> root)
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    file_path = os.getenv("REINDEX_UTIL_DATASET_PATH")
    if not file_path:
        print("Lỗi: Không tìm thấy REINDEX_UTIL_DATASET_PATH trong file .env!")
        return
        
    # Chuyển đổi thành đường dẫn tuyệt đối từ thư mục gốc
    root_dir = Path(__file__).parent.parent.parent
    abs_file_path = root_dir / file_path
    
    print(f"Đang đọc file: {abs_file_path}")
    try:
        df = pd.read_excel(abs_file_path)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return
        
    print(f"Tổng số dòng hiện tại: {len(df)}")
    
    # 1. Đánh lại index tuần tự từ 1 đến N
    df['index'] = range(1, len(df) + 1)
    
    # 2. Sinh mới annotation_id cho tất cả các dòng (ID 64-bit ngẫu nhiên)
    df['annotation_id'] = [int(uuid.uuid4().int & (1<<63)-1) for _ in range(len(df))]
    
    # 3. Lưu lại (ghi đè lên file cũ)
    print("Đang lưu lại file...")
    df.to_excel(abs_file_path, index=False)
    
    print("✅ Đã đánh lại index và annotation_id thành công!")

if __name__ == "__main__":
    reindex_dataset()
