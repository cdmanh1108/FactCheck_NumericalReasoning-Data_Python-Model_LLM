class KQGDGiaoDichNDTNNTopStockFilterForIframe:
    endpoint = "KQGDGiaoDichNDTNNTopStockFilterForIframe"  # Keyword định tuyến cho Playwright

    def parse(self, json_array):
        """
        Hàm ép phẳng JSON (Linearization) cho dữ liệu Giao dịch Nhà đầu tư nước ngoài (Khối ngoại)
        """
        if not json_array or len(json_array) == 0: 
            return ""
        
        # Dữ liệu API trả về [[Top_Mua_Rong], [Top_Ban_Rong]]
        top_mua = json_array[0] if len(json_array) > 0 else []
        top_ban = json_array[1] if len(json_array) > 1 else []

        # ÉP PHẲNG JSON THÀNH TEXT CHUẨN FEVEROUS
        linearized_text = "\n[BẢNG: GIAO DỊCH NHÀ ĐẦU TƯ NƯỚC NGOÀI - TOP MUA BÁN RÒNG]\n"
        
        linearized_text += "--- Nhóm Top Mua Ròng ---\n"
        for stock in top_mua:
            stock_code = stock.get("StockCode", "")
            kl_buy = stock.get("KLBuyRong_Total", 0)
            gt_buy = stock.get("GTBuyRong_Total", 0)
            
            linearized_text += f"- Cổ phiếu {stock_code}: Khối lượng mua ròng {kl_buy}, Giá trị mua ròng {gt_buy} tỷ đồng\n"
        
        linearized_text += "--- Nhóm Top Bán Ròng ---\n"
        for stock in top_ban:
            stock_code = stock.get("StockCode", "")
            kl_sell = stock.get("KLSellRong_Total", 0)
            gt_sell = stock.get("GTSellRong_Total", 0)
            
            linearized_text += f"- Cổ phiếu {stock_code}: Khối lượng bán ròng {kl_sell}, Giá trị bán ròng {gt_sell} tỷ đồng\n"
        
        return linearized_text