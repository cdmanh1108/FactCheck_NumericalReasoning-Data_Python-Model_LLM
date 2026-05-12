class GetCPAnhHuongManh:
    endpoint = "GetCPAnhHuongManh"  # URL keyword để Playwright định tuyến

    def parse(self, json_array):
        """
        API trả về flat list các cổ phiếu ảnh hưởng mạnh đến chỉ số.
        OrderType=1: ảnh hưởng dương (kéo index tăng)
        OrderType=2: ảnh hưởng âm (kéo index giảm)
        """
        if not json_array or len(json_array) == 0:
            return ""

        tang = [s for s in json_array if s.get("OrderType") == 1]
        giam = [s for s in json_array if s.get("OrderType") == 2]

        linearized_text = "\n[BẢNG: CỔ PHIẾU ẢNH HƯỞNG MẠNH ĐẾN CHỈ SỐ]\n"

        linearized_text += "--- Nhóm kéo chỉ số Tăng ---\n"
        for s in tang:
            linearized_text += (
                f"- {s.get('StockCode', '')}: "
                f"Đóng góp chỉ số +{s.get('IndexChange', 0):.4f} điểm\n"
            )

        linearized_text += "--- Nhóm kéo chỉ số Giảm ---\n"
        for s in giam:
            linearized_text += (
                f"- {s.get('StockCode', '')}: "
                f"Đóng góp chỉ số {s.get('IndexChange', 0):.4f} điểm\n"
            )

        return linearized_text
