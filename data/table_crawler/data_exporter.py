import pandas as pd
import uuid
from pathlib import Path

class ViFactCheckExporter:
    def __init__(self, member_name, author, topic, topic_path, sub_topic="", sub_topic_path=""):
        """
        Args:
            topic      : Tên tiếng Việt, ghi vào cột Topic trong data. VD: "Chứng khoán"
            topic_path : Tên dạng path an toàn, dùng tạo thư mục.    VD: "chung_khoan"
            sub_topic      : Tên tiếng Việt của chủ đề con (tuỳ chọn). VD: "Giao dịch nội bộ"
            sub_topic_path : Tên dạng path của chủ đề con (tuỳ chọn). VD: "giao_dich_noi_bo"
        """
        # 1. Tự động sinh đường dẫn theo cấu trúc thư mục nhóm
        # Dùng __file__ lùi lại 2 cấp (từ table_crawler ra data) để đảm bảo luôn tìm đúng thư mục data/members
        _data_dir = Path(__file__).parent.parent
        out_dir = _data_dir / "members" / member_name / author / topic_path
        if sub_topic_path:
            out_dir = out_dir / sub_topic_path

        # Tạo thư mục nếu chưa tồn tại
        out_dir.mkdir(parents=True, exist_ok=True)
        self.output_path = out_dir / "draft_crawled_data.parquet"

        # 2. Lưu lại Topic và Author để dùng chung cho mọi record
        self.topic = topic      # tiếng Việt → ghi vào cột data
        self.author = author

        # 9 trường dữ liệu chuẩn theo cấu trúc ViFactCheck trên Hugging Face
        self.columns = ["Statement", "Context", "Evidence", "Topic", "Author", "Url", 
                "labels", "annotation_id", "index", 
                "Reasoning_Type", "Evidence_Type", "Reasoning_Steps"]
        self.data_buffer = []

    def get_crawled_urls(self) -> set:
        """Trả về tập hợp các URL đã có trong file parquet (nếu file chưa tồn tại thì trả về set rỗng)."""
        if not self.output_path.exists():
            return set()
        df = pd.read_parquet(self.output_path, columns=["Url"])
        return set(df["Url"].dropna().tolist())

    # Bỏ tham số topic và author ở đây đi cho gọn, vì đã khai báo ở __init__
    def add_record(self, context, url):
        """Thêm một dòng dữ liệu thô (Team Data sẽ điền Statement, Evidence, labels sau)"""
        record = {
            "Statement": "", # Team Data tự viết bẫy
            "Context": context, # Chứa text bài báo + Bảng đã ép phẳng
            "Evidence": "",  # Team Data tự trích xuất
            "Topic": self.topic, # Gán tự động theo cấu hình
            "Author": self.author, # Gán tự động theo cấu hình
            "Url": url,
            "labels": -1, # -1 là chưa gán nhãn. ViFactCheck quy định: 0 (Support), 1 (Refute), 2 (NEI)
            "annotation_id": int(uuid.uuid4().int & (1<<63)-1), # Tạo ID ngẫu nhiên
            "index": len(self.data_buffer) + 1,
            # 3 CỘT MỚI ĐỂ TRỐNG CHO TEAM DATA NHẬP TAY KHI GÁN NHÃN:
            "Reasoning_Type": "",  # Gợi ý điền: "So_sanh" (so sánh bảng/số), "Phan_tram_vs_Tuyet_doi" (số liệu % và tuyệt đối), "Khuynh_huong_thoi_gian" (đánh giá thời gian tăng/giảm)
            "Evidence_Type": "",   # Gợi ý điền: "Text" (chỉ chữ), "Table" (chỉ bảng số liệu), "Both" (kết hợp chữ + bảng)
            "Reasoning_Steps": ""  # Gợi ý điền: 1, 2, 3... (số bước suy luận/tính toán trung gian cần thiết để xác minh)
        }
        self.data_buffer.append(record)
        print(f"[Exporter] Đã thêm bản ghi từ: {url}")

    def save_to_parquet(self):
        if not self.data_buffer:
            return
        
        df = pd.DataFrame(self.data_buffer, columns=self.columns)
        
        # Nếu file đã tồn tại, đọc lên và gộp vào
        if self.output_path.exists():
            existing_df = pd.read_parquet(self.output_path)
            df = pd.concat([existing_df, df], ignore_index=True)
            
        # Tính lại index tuần tự sau khi gộp (tránh trùng index=1 giữa các lần chạy)
        df["index"] = range(1, len(df) + 1)
        df.to_parquet(self.output_path)
        print(f"[Exporter] Đã lưu thành công {len(self.data_buffer)} mẫu vào {self.output_path}")
        self.data_buffer = [] # Clear buffer
