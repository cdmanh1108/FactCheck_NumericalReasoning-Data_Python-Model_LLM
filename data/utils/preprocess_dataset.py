import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split

def preprocess_and_split():
    print("🚀 Bắt đầu tiền xử lý dữ liệu...")
    
    # Định vị đường dẫn thư mục
    project_root = Path(__file__).parent.parent.parent
    raw_data_path = project_root / "data" / "members" / "generated_vinumfcr_200_samples.xlsx"
    processed_dir = project_root / "data" / "processed"
    
    # Đảm bảo thư mục processed tồn tại
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Đọc dữ liệu thô
    if not raw_data_path.exists():
        print(f"❌ Lỗi: Không tìm thấy file {raw_data_path}")
        return
        
    df = pd.read_excel(raw_data_path)
    print(f"Đã đọc {len(df)} dòng từ file gốc.")
    
    # 2. Xoá các dòng thiếu Statement hoặc Evidence
    df = df.dropna(subset=['Statement', 'Evidence'])
    
    # 3. Lọc chỉ lấy những dòng ĐÃ GÁN NHÃN chuẩn (0, 1 hoặc 2)
    df = df[df['labels'].isin([0, 1, 2])].copy()
    df['labels'] = df['labels'].astype(int)
    print(f"Sau khi lọc các nhãn không hợp lệ, còn lại: {len(df)} dòng.")
    
    if len(df) == 0:
        print("⚠️ Cảnh báo: Không có dòng nào được gán nhãn! Vui lòng gán nhãn file Excel trước khi chạy script.")
        return
        
    # 4. Làm sạch text (Xoá khoảng trắng thừa, ký tự ẩn)
    def clean_text(text):
        if pd.isna(text): return ""
        text = str(text).strip()
        text = " ".join(text.split()) # Xoá khoảng trắng kép, tab, dấu xuống dòng
        return text
        
    df['Statement'] = df['Statement'].apply(clean_text)
    df['Evidence'] = df['Evidence'].apply(clean_text)
    df['Context'] = df['Context'].apply(clean_text)
    
    # 5. Đánh lại index sau khi lọc
    df.reset_index(drop=True, inplace=True)
    
    # 6. Chia tập Train, Validation, Test (Tỉ lệ 80-10-10)
    # Stratify theo 'labels' để đảm bảo phân bổ đều các nhãn 0, 1, 2 vào 3 tập
    try:
        # Đầu tiên tách 80% Train, 20% Temp
        train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['labels'])
        # Tiếp tục chia Temp thành 50% Val, 50% Test (Tức là mỗi tập 10% so với ban đầu)
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['labels'])
        
        # 7. Lưu kết quả ra file Parquet (chuẩn công nghiệp, nhẹ và nhanh hơn CSV/Excel)
        train_df.to_parquet(processed_dir / "train_data.parquet", index=False)
        val_df.to_parquet(processed_dir / "val_data.parquet", index=False)
        test_df.to_parquet(processed_dir / "test_data.parquet", index=False)
        
        # Lưu riêng 1 file CSV cho tập test_data để con người dễ xem
        test_df.to_csv(processed_dir / "test_data.csv", index=False, encoding='utf-8-sig')
        
        print("\n✅ Hoàn thành tiền xử lý!")
        print(f"📁 Dữ liệu Train: {len(train_df)} mẫu")
        print(f"📁 Dữ liệu Val  : {len(val_df)} mẫu")
        print(f"📁 Dữ liệu Test : {len(test_df)} mẫu")
        print(f"Tất cả file đã được lưu tại: {processed_dir}")
        
    except ValueError as e:
        print(f"\n⚠️ Lỗi khi chia tập: {e}")
        print("Có thể do số lượng nhãn của bạn quá ít (phải có ít nhất 2 mẫu cho mỗi loại nhãn 0, 1, 2 thì mới dùng stratify được).")
        print("Hãy gán nhãn thêm trong Excel rồi chạy lại script nhé!")

if __name__ == "__main__":
    preprocess_and_split()
