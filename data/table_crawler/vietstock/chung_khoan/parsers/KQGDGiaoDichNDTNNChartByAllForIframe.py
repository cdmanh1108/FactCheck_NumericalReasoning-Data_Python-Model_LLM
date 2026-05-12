import re
from datetime import datetime

class KQGDGiaoDichNDTNNChartByAllForIframe:
    endpoint = "KQGDGiaoDichNDTNNChartByAllForIframe"  # Keyword định tuyến cho Playwright

    def parse(self, json_array):
        """
        Hàm ép phẳng JSON (Linearization) cho dữ liệu Giao dịch Khối ngoại theo chuỗi thời gian
        """
        # API trả về mảng 2 phần tử, mảng thứ 2 (index 1) mới chứa danh sách record
        if not json_array or len(json_array) < 2: 
            return ""
        
        records = json_array[1]  # Index 1: danh sách record theo thời gian

        # ÉP PHẲNG JSON THÀNH TEXT CHUẨN FEVEROUS
        linearized_text = "\n[BẢNG: THỐNG KÊ GIAO DỊCH NHÀ ĐẦU TƯ NƯỚC NGOÀI THEO THỜI GIAN]\n"
        
        for record in records:
            # 1. Giải mã chuỗi thời gian Unix (Ví dụ: \/Date(1777827600000)\/ -> dd/mm/yyyy)
            raw_date = record.get("TradingDate", "")
            date_str = "N/A"
            match = re.search(r'\d+', raw_date)
            if match:
                timestamp = int(match.group()) / 1000.0 
                date_str = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
            
            # 2. Lấy các chỉ số Khối lượng (Vol) và Giá trị (Val)
            buy_vol = record.get("BuyVol", 0)
            buy_val = record.get("BuyVal", 0)
            sell_vol = record.get("SellVol", 0)
            sell_val = record.get("SellVal", 0)
            
            # 3. Format chuỗi văn bản tuyến tính
            linearized_text += f"- Ngày {date_str}: Khối ngoại Mua (Khối lượng: {buy_vol}, Giá trị: {buy_val} tỷ) | Bán (Khối lượng: {sell_vol}, Giá trị: {sell_val} tỷ)\n"
        
        return linearized_text