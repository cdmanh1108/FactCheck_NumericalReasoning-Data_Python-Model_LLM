import pandas as pd
import json
import time
import re
import os
import uuid
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

def generate_samples():
    print("Bắt đầu đọc file merged_dataset.xlsx...")
    input_path = r"D:\Study\Khai thác dữ liệu truyền thông xã hội\vifactcheck-numerical-project\data\members\merged_dataset.xlsx"
    
    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Lỗi khi đọc file Excel: {e}")
        return
    
    # Xác định cột chứa ngữ cảnh.
    context_col = 'Context' 
    if context_col not in df.columns:
        potential_cols = ['Full Context', 'Content', 'Text', 'Nội dung']
        for col in potential_cols:
            if col in df.columns:
                context_col = col
                break
        # Nếu vẫn không tìm thấy, lấy cột đầu tiên có vẻ chứa nhiều text
        if context_col not in df.columns:
            context_col = 'Context' # Ép về Context để in lỗi rõ ràng nếu không có
                
    print(f"Sử dụng cột '{context_col}' làm ngữ cảnh (Context).")
    
    # Chọn ngẫu nhiên bài báo để tạo ra ~200 mẫu
    # Nếu trung bình mỗi bài sinh 8 mẫu, ta cần khoảng 25 bài
    sample_size = min(30, len(df))
    sampled_df = df.sample(n=sample_size, random_state=42)
    
    # ==========================================
    # CẤU HÌNH API KEY TẠI ĐÂY
    # ==========================================
    load_dotenv() # Tải các biến môi trường từ file .env
    GENAI_API_KEY = os.getenv("GENAI_API_KEY")
    
    if not GENAI_API_KEY:
        print("Lỗi: Không tìm thấy GENAI_API_KEY trong file .env!")
        return
        
    client = genai.Client(api_key=GENAI_API_KEY)
    
    results = []
    current_index = 1
    
    prompt_template = """
    Bạn là một chuyên gia tạo dữ liệu Fact-checking về lĩnh vực tài chính, chứng khoán (dự án ViNumFCR).
    Dưới đây là một ngữ cảnh (Context) bao gồm văn bản (Text) và/hoặc bảng dữ liệu (Table).
    Nhiệm vụ của bạn là tạo ra 7 đến 10 mẫu kiểm chứng (Statement - Evidence) đánh mạnh vào KHẢ NĂNG SUY LUẬN SỐ HỌC, cố tình gài các "bẫy" để kiểm tra các AI khác.
    
    CÁC LOẠI BẪY CẦN ÁP DỤNG (Bắt buộc phải phân bổ đều các bẫy này):
    1. Bẫy Toán học đa bước (Reasoning_Type = Toan_hoc_da_buoc): Yêu cầu tính tổng/hiệu của 3-4 thực thể, làm tròn số thập phân, tính chênh lệch số âm (biến động giảm), tính tỷ trọng % hoặc số lần, tính toán ẩn (VD: Khối lượng x Giá).
    2. Bẫy So sánh chéo & Cực trị (Reasoning_Type = So_sanh_cheo): So sánh chéo số liệu giữa Text và Table hoặc giữa các cột/hàng cách xa nhau. Tìm Min/Max (VD: "mã tăng mạnh nhất", "giảm ít nhất") sau đó thực hiện phép tính.
    3. Bẫy Chuỗi thời gian (Reasoning_Type = Chuoi_thoi_gian): Cộng dồn hoặc tính hiệu số qua một chuỗi ngày liên tiếp (đảo chiều mua/bán ròng), tìm đỉnh/đáy thời gian.
    4. Bẫy Không đủ thông tin (Reasoning_Type = Khong_du_thong_tin): Tuyên bố có số liệu ĐÚNG nhưng cố tình chèn thêm nguyên nhân/chi tiết BỊA ĐẶT không hề có trong bài báo, bắt buộc nhãn phải là 2 (NEI).
    5. Bẫy Nhập nhằng ngữ nghĩa (Reasoning_Type = Nhap_nhang_ngu_nghia): Gài sự khác biệt giữa số làm tròn trong Text (VD: "hơn 37 điểm") và số chi tiết trong Table (VD: 37.16 điểm). Sử dụng từ ngữ mập mờ ("chính xác là", "khoảng", "gần gấp đôi").
    
    YÊU CẦU VỀ NHÃN (labels):
    - 0 (Supported): Tuyên bố hoàn toàn đúng so với ngữ cảnh.
    - 1 (Refuted): Tuyên bố sai về mặt con số thực tế hoặc sai do tính toán (rất dễ lừa nếu không tính toán kỹ).
    - 2 (NEI - Not Enough Information): Tuyên bố chứa thông tin/nguyên nhân bịa đặt không có trong ngữ cảnh.
    
    Ngữ cảnh:
    {context}
    
    Hãy trả về duy nhất một mảng JSON (không bọc trong markdown codeblock), mỗi phần tử có định dạng sau:
    [
      {{
        "Statement": "Nội dung tuyên bố (chứa các bẫy đã nêu)",
        "Evidence": "Trích dẫn bằng chứng từ ngữ cảnh và giải thích chi tiết phép tính (VD: 'Lợi nhuận Q1 là 115, Q2 là -20. Tổng = 115 + (-20) = 95')",
        "labels": 0,
        "Reasoning_Type": "Toan_hoc_da_buoc",
        "Evidence_Type": "Text", 
        "Reasoning_Steps": 2 
      }}
    ]
    Lưu ý: labels là số nguyên (0, 1 hoặc 2), Reasoning_Steps là số nguyên, Evidence_Type chọn 1 trong ["Text", "Table", "Both"].
    """
    
    print("Bắt đầu sinh dữ liệu với Gemini API...")
    for idx, row in sampled_df.iterrows():
        context_text = str(row[context_col])
        # Bỏ qua các bài báo quá ngắn
        if len(context_text) < 150:
            continue 
            
        prompt = prompt_template.format(context=context_text)
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            response_text = response.text
            
            # Trích xuất JSON từ chuỗi phản hồi (xử lý trường hợp LLM sinh ra markdown markdown)
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                pairs = json.loads(json_str)
                for pair in pairs:
                    # Chuẩn hóa keys để khớp với data_exporter
                    pair_normalized = {
                        "annotation_id": int(uuid.uuid4().int & (1<<63)-1), # ID duy nhất 64-bit
                        "index": current_index,
                        "Statement": pair.get("Statement", pair.get("statement", "")),
                        "Context": context_text,
                        "Evidence": pair.get("Evidence", pair.get("evidence", "")),
                        "labels": pair.get("labels", pair.get("label", -1)),
                        "Reasoning_Type": pair.get("Reasoning_Type", ""),
                        "Evidence_Type": pair.get("Evidence_Type", ""),
                        "Reasoning_Steps": pair.get("Reasoning_Steps", ""),
                        "Source_Row_Index": idx
                    }
                    results.append(pair_normalized)
                    current_index += 1
            
            print(f" Đã sinh thành công {len(pairs)} mẫu từ bài viết dòng {idx}. Tổng số mẫu hiện tại: {len(results)}")
            time.sleep(2) # Nghỉ ngắn để tránh Rate Limit của API miễn phí
            
            if len(results) >= 200:
                print(">>> Đã đạt mục tiêu 200 mẫu!")
                break
                
        except Exception as e:
            print(f" Lỗi ở dòng {idx}: {e}")
            time.sleep(5)
            
    # Lưu kết quả ra file mới
    output_df = pd.DataFrame(results)
    output_path = r"D:\Study\Khai thác dữ liệu truyền thông xã hội\vifactcheck-numerical-project\data\members\generated_vinumfcr_200_samples.xlsx"
    output_df.to_excel(output_path, index=False)
    print(f"\nHoàn thành! Đã lưu {len(output_df)} mẫu vào file: {output_path}")

if __name__ == "__main__":
    generate_samples()
