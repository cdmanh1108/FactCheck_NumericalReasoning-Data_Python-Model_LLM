# Lưu ý: Khi team AI train xong, họ sẽ mở comment các dòng import dưới đây
# from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

class FactCheckModel:
    def __init__(self):
        print("Sẵn sàng load mô hình AI...")
        self.labels_map = {0: "Support", 1: "Refute", 2: "NEI"}
        
        # TODO DÀNH CHO TEAM AI: Load model thật vào đây
        # Ví dụ nếu dùng PhoBERT:
        # self.tokenizer = AutoTokenizer.from_pretrained("./models/phobert-vifactcheck")
        # self.model = AutoModelForSequenceClassification.from_pretrained("./models/phobert-vifactcheck")

    def predict(self, claim: str, full_context: str):
        """
        Thực hiện dự đoán nhãn dựa trên Tuyên bố và Ngữ cảnh (đã bao gồm text từ bảng)
        """
        # --- CODE DỰ ĐOÁN THẬT (Team AI sẽ viết đè vào đây) ---
        # inputs = self.tokenizer(claim, full_context, return_tensors="pt", truncation=True)
        # outputs = self.model(**inputs)
        # predicted_class_id = outputs.logits.argmax().item()
        # label = self.labels_map[predicted_class_id]
        
        # Code tạm thời để test luồng API
        label = "Support" # Giả lập kết quả
        evidence = "Đây là đoạn bằng chứng trích xuất từ văn bản/bảng..."
        
        return {
            "prediction": label,
            "evidence": evidence
        }

ai_model = FactCheckModel()