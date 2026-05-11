class gettradingresultdrawchart:
    endpoint = "gettradingresultdrawchart"  # URL keyword Playwright sẽ bắt

    def parse(self, json_data):
        """
        Hàm nhận trực tiếp response.json() từ Playwright và ép phẳng thành chữ
        """
        # Kiểm tra xem gói tin có chứa key Data không
        if not json_data or not json_data.get("Data"): 
            return ""
        
        # Mảng Data thường chứa 1 phần tử object, lấy phần tử đầu tiên
        data_list = json_data.get("Data", [])
        if not data_list or len(data_list) == 0:
            return ""
            
        data = data_list[0] if isinstance(data_list, list) else data_list
        
        # Ép phẳng dữ liệu bảng thành văn bản tuyến tính chuẩn FEVEROUS
        linearized_text = (
            f"\n[BẢNG GIAO DỊCH CỔ PHIẾU {data.get('StockCode', 'Không xác định')} - SÀN {data.get('Exchange', '')}]: "
            f"Giá đóng cửa: {data.get('ClosePrice', 0):,}đ | "
            f"Mức thay đổi: {data.get('Change', 0)}đ ({data.get('PerChange', 0)}%) | "
            f"Tổng lệnh mua: {data.get('TotalBuyTrade', 0)} lệnh | Tổng lệnh bán: {data.get('TotalSellTrade', 0)} lệnh | "
            f"Tổng KL mua: {data.get('TotalBuyVol', 0):,} | Tổng KL bán: {data.get('TotalSellVol', 0):,} | "
            f"Chênh lệch KL (Mua-Bán): {data.get('DiffBuySellVol', 0):,} | "
            f"Khối ngoại mua: {data.get('ForeignBuyVol', 0):,} | Khối ngoại bán: {data.get('ForeignSellVol', 0):,} | "
            f"Khối ngoại giao dịch ròng: {data.get('ForeignDiffBuySellVol', 0):,}."
        )
        return linearized_text