class Cms3GetTopStockChange:
    endpoint = "Cms3GetTopStockChange"  # URL keyword để hệ thống Playwright tự động nhận diện định tuyến

    def parse(self, json_array):
        """
        Hàm nhận trực tiếp response.json() dạng List từ Crawler Engine chung
        và ép phẳng dữ liệu thành chuỗi tuyến tính (Linearized Text).
        """
        if not json_array or len(json_array) == 0: 
            return ""
        
        # Dữ liệu API trả về [[top_tang_stocks], [top_giam_stocks]]
        top_tang = json_array[0] if len(json_array) > 0 else []
        top_giam = json_array[1] if len(json_array) > 1 else []

        # ÉP PHẲNG JSON THÀNH TEXT (Linearization) THEO CHUẨN FEVEROUS
        linearized_text = "\n[BẢNG: BIẾN ĐỘNG CỔ PHIẾU HÀNG NGÀY]\n"
        
        linearized_text += "--- Nhóm Cổ phiếu Tăng ---\n"
        for stock in top_tang:
            # Dùng .get() để tránh lỗi nếu API thiếu field
            stock_code = stock.get("StockCode", "")
            stock_name = stock.get("StockName", "")
            last_price = stock.get("LastPrice", 0)
            avg_vol = stock.get("AvgVol", 0)
            per_change = stock.get("PerChange", 0)
            
            linearized_text += f"- Cổ phiếu {stock_code} ({stock_name}): Giá cuối {last_price} VNĐ, Khối lượng trung bình {avg_vol}, Biến động +{per_change}%\n"
        
        linearized_text += "--- Nhóm Cổ phiếu Giảm ---\n"
        for stock in top_giam:
            stock_code = stock.get("StockCode", "")
            stock_name = stock.get("StockName", "")
            last_price = stock.get("LastPrice", 0)
            avg_vol = stock.get("AvgVol", 0)
            per_change = stock.get("PerChange", 0)
            
            linearized_text += f"- Cổ phiếu {stock_code} ({stock_name}): Giá cuối {last_price} VNĐ, Khối lượng trung bình {avg_vol}, Biến động {per_change}%\n"
        
        return linearized_text