class FinanceStaticChartData:
    endpoint = "FinanceStaticChartData"  # URL keyword Playwright sẽ bắt

    # Không cần __init__ hay url, vs_headers nữa vì Playwright đã lo việc bắt mạng
    
    def parse(self, json_data):
        """
        Hàm này nhận trực tiếp response.json() từ Playwright
        """
        data_list = json_data.get("data", [])
        
        # Nếu mảng rỗng thì bỏ qua
        if not data_list or len(data_list) == 0: 
            return ""

        # Lấy Tên biểu đồ và Đơn vị từ phần tử đầu tiên của mảng
        first_item = data_list[0] if isinstance(data_list, list) else data_list
        report_name = first_item.get("ReportNormName", "Chỉ tiêu tài chính")
        unit = first_item.get("Unit", "")

        # Khởi tạo chuỗi văn bản tuyến tính (chuẩn FEVEROUS)
        linearized_text = f"\n[BẢNG SỐ LIỆU TÀI CHÍNH - {report_name} (Đơn vị: {unit})]: "
        
        for item in data_list:
            # Xử lý chuỗi năm (Ví dụ: "N/2017" -> "2017")
            year = item.get("NormTerm", "").replace("N/", "")
            value = item.get("Value", 0)
            linearized_text += f"(Năm {year}) Giá trị: {value} | "
            
        return linearized_text