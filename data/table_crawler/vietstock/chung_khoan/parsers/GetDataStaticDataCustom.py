class GetDataStaticDataCustom:
    endpoint = "GetDataStaticDataCustom"  # URL keyword Playwright sẽ bắt

    def parse(self, json_array):
        """
        Hàm nhận trực tiếp response.json() từ Playwright (dạng List) và ép phẳng thành chữ
        """
        # Kiểm tra xem mảng có rỗng hay không
        if not json_array or len(json_array) == 0: 
            return ""
        
        # Vì json_array là một List, ta cần lấy Name và Unit từ phần tử đầu tiên
        first_item = json_array[0] if isinstance(json_array, list) else json_array
        chart_name = first_item.get("Name", "Lợi nhuận")
        unit = first_item.get("Unit", "")
        
        # Bắt đầu chuỗi văn bản tuyến tính (Linearized Text)
        linearized_text = f"\n[BẢNG SỐ LIỆU TÀI CHÍNH - {chart_name} (Đơn vị: {unit})]: "
        
        for item in json_array:
            period = item.get("Period", "")
            value = item.get("Value", 0)
            linearized_text += f"(Năm {period}) Giá trị: {value} | "
            
        return linearized_text