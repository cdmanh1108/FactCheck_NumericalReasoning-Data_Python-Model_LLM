class FinanceInfoChart:
    endpoint = "FinanceInfoChart"  # URL keyword để Playwright tự động nhận diện

    def parse(self, json_array):
        """
        Hàm nhận response.json() dạng List, kiểm tra Type để gọi từ điển động 
        và ép phẳng dữ liệu thành chuỗi tuyến tính.
        """
        if not json_array or len(json_array) == 0: 
            return ""
        
        # 1. Bắt lấy Type từ phần tử đầu tiên để xác định loại biểu đồ
        first_item = json_array[0] if isinstance(json_array, list) else json_array
        chart_type = first_item.get("Type", 1)
        
        # 2. KHAI BÁO TỪ ĐIỂN ĐỘNG (DYNAMIC DICTIONARY)
        if chart_type == 1:
            chart_title = "KẾT QUẢ KINH DOANH THEO QUÝ"
            mapping = {
                "Value1": "Doanh thu thuần",
                "Value2": "Lợi nhuận gộp",
                "Value3": "Lợi nhuận thuần từ HĐKD",
                "Value4": "Biên lợi nhuận gộp (%)",
                "Value5": "Biên lợi nhuận ròng (%)",
                "Value6": "Tài sản ngắn hạn", 
                "Value7": "Tổng tài sản"
                # (Bạn có thể bổ sung thêm khi đối chiếu trên web)
            }
        elif chart_type == 2:
            chart_title = "CÂN ĐỐI KẾ TOÁN THEO QUÝ"
            mapping = {
                "Value1": "Tổng tài sản",
                "Value2": "Vốn chủ sở hữu",
                "Value3": "Nợ phải trả"
                # (Lưu ý: Thông tin mapping của Type 2 này là ví dụ giả định bên ngoài tài liệu, bạn cần tự đối chiếu lại trên trang Vietstock để điền cho chính xác).
            }
        else:
            chart_title = f"CHỈ TIÊU TÀI CHÍNH KHÁC (Loại {chart_type})"
            mapping = {}

        # 3. Ép phẳng dữ liệu (Linearization)
        linearized_text = f"\n[BẢNG {chart_title}]: "
        
        for item in json_array:
            # Ghép Quý và Năm (Ví dụ: Q1/2026)
            term = f"{item.get('TermCode', '')}/{item.get('YearPeriod', '')}"
            linearized_text += f"({term}) "
            
            # Quét qua từ điển, nếu JSON trả về có Value đó và khác null thì lấy
            for key, label in mapping.items():
                val = item.get(key)
                if val is not None:  # Xử lý trường hợp Value8, Value9 bị null
                    linearized_text += f"{label}: {val} | "
            
            linearized_text += " *** " # Ký tự phân cách giữa các quý
            
        return linearized_text