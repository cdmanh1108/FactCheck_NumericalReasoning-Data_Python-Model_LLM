import re
from datetime import datetime

class KQGDGiaoDichTuDoanhChartByAllForIframe:
    endpoint = "KQGDGiaoDichTuDoanhChartByAllForIframe"  # Keyword định tuyến cho Playwright

    def parse(self, json_array):
        """
        Hàm ép phẳng JSON (Linearization) cho dữ liệu Giao dịch tự doanh theo chuỗi thời gian (Time-series)
        """
        # API này trả về mảng có 2 phần tử, mảng thứ 2 (index 1) chứa danh sách các ngày giao dịch
        if not json_array or len(json_array) < 2: 
            return ""
        
        records = json_array[1]  # Index 1: danh sách record theo thời gian

        # ÉP PHẲNG JSON THÀNH TEXT CHUẨN FEVEROUS
        linearized_text = "\n[BẢNG: THỐNG KÊ GIAO DỊCH TỰ DOANH THEO THỜI GIAN]\n"
        
        for record in records:
            # 1. Xử lý chuyển đổi chuỗi thời gian Unix (Ví dụ: \/Date(1777827600000)\/ -> dd/mm/yyyy)
            raw_date = record.get("TradingDate", "")
            date_str = "N/A"
            match = re.search(r'\d+', raw_date)
            if match:
                # Chia 1000 để đổi từ millisecond sang second
                timestamp = int(match.group()) / 1000.0 
                date_str = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
            
            # 2. Lấy các chỉ số Khối lượng (Vol) và Giá trị (Val)
            buy_vol = record.get("BuyVol", 0)
            buy_val = record.get("BuyVal", 0)
            sell_vol = record.get("SellVol", 0)
            sell_val = record.get("SellVal", 0)
            
            # 3. Nối thành chuỗi văn bản tuyến tính
            linearized_text += f"- Ngày {date_str}: Mua (Khối lượng: {buy_vol}, Giá trị: {buy_val} tỷ) | Bán (Khối lượng: {sell_vol}, Giá trị: {sell_val} tỷ)\n"
        
        return linearized_text