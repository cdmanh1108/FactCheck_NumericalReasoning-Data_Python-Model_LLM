# =====================================================================
# DẠNG 1: MẢNG STRING (Chỉ chứa URL thuần)
# =====================================================================
# Đặc điểm: Dễ copy-paste hàng loạt từ trình duyệt.

URLS_STRING_FORMAT = [
    "https://vietstock.vn/2026/05/co-dong-mot-doanh-nghiep-thuy-san-sang-tay-noi-bo-truoc-mua-co-tuc-739-1440868.htm",
    "https://vietstock.vn/2026/05/cong-ty-cua-shark-lien-muon-ban-toan-bo-gan-23-trieu-cp-pws-sau-dot-co-tuc-ky-luc-739-1439862.htm",
    "https://vietstock.vn/2026/05/hang-da-xay-dung-hoa-an-don-co-dong-lon-dai-loan-739-1439814.htm",
    "https://vietstock.vn/2026/05/vo-ong-to-hai-da-thoai-het-co-phan-tai-vci-739-1439654.htm",
    "https://vietstock.vn/2026/05/dong-thai-moi-cua-dragon-capital-tai-mwg-739-1439153.htm",
    "https://vietstock.vn/2026/05/pho-tong-dvm-mua-65-luong-co-phieu-dang-ky-nang-so-huu-len-gan-20-739-1438498.htm",
    "https://vietstock.vn/2026/05/nhom-hipt-tro-thanh-co-dong-lon-cua-pjt-739-1438391.htm",
    "https://vietstock.vn/2026/05/me-ruot-thanh-vien-hdqt-va-pho-tong-kbc-muon-gom-8-trieu-cp-739-1438357.htm"
]

# =====================================================================
# DẠNG 2: MẢNG OBJECT (List các Dictionary)
# =====================================================================
# Đặc điểm: Đây là cấu trúc dữ liệu khuyên dùng nhất cho hệ thống của bạn!

# URLS_OBJECT_FORMAT = [
#     {
#         "url": "https://finance.vietstock.vn/ACB-chi-tiet.htm",
#         "stock_code": "ACB",
#         "mock_context": "Đóng cửa phiên giao dịch, mã cổ phiếu ACB ghi nhận nhiều biến động. "
#     },
#     {
#         "url": "https://finance.vietstock.vn/FPT-chi-tiet.htm",
#         "stock_code": "FPT",
#         "mock_context": "Cổ phiếu công nghệ FPT tiếp tục thu hút dòng tiền khối ngoại. "
#     },
#     {
#         "url": "https://finance.vietstock.vn/HPG-chi-tiet.htm",
#         "stock_code": "HPG",
#         "mock_context": "Báo cáo giao dịch thép Hòa Phát hôm nay cho thấy lực bán áp đảo. "
#     },
#     {
#         "url": "https://finance.vietstock.vn/VNM-chi-tiet.htm",
#         "stock_code": "VNM",
#         "mock_context": "Thống kê từ Vietstock cho thấy tình hình tài chính của Vinamilk. "
#     }
# ]