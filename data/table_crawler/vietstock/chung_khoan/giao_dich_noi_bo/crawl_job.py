# =====================================================================
# CRAWL JOB CONFIG — Thành viên chỉ cần sửa file này
# =====================================================================

from vietstock.chung_khoan.giao_dich_noi_bo.gettradingresultdrawchart import gettradingresultdrawchart
from vietstock.chung_khoan.giao_dich_noi_bo.FinanceStaticChartData import FinanceStaticChartData
from vietstock.chung_khoan.giao_dich_noi_bo.GetDataStaticDataCustom import GetDataStaticDataCustom
from vietstock.chung_khoan.giao_dich_noi_bo.FinanceInfoChart import FinanceInfoChart

# 1. Cấu hình Exporter (thư mục lưu & metadata cho cột data)
EXPORTER_CONFIG = {
    "member_name": "Manh",
    "author":      "Vietstock",
    "topic":       "Chứng khoán",        # tiếng Việt → ghi vào cột Topic
    "topic_path":  "chung_khoan",        # dạng path  → tạo thư mục
    "sub_topic":      "Giao dịch nội bộ",   # tiếng Việt (tuỳ chọn)
    "sub_topic_path": "giao_dich_noi_bo",   # dạng path  (tuỳ chọn)
}

# 2. Danh sách Parser — thêm/bớt tuỳ endpoint cần bắt
PARSERS = [
    gettradingresultdrawchart(),
    FinanceStaticChartData(),
    GetDataStaticDataCustom(),
    FinanceInfoChart(),
]

# 3. Danh sách URL đầu vào — cái nào có data thì dùng cái đó
try:
    from vietstock.chung_khoan.giao_dich_noi_bo.urls_input import URLS_STRING_FORMAT
except ImportError:
    URLS_STRING_FORMAT = []

try:
    from vietstock.chung_khoan.giao_dich_noi_bo.urls_input import URLS_OBJECT_FORMAT
except ImportError:
    URLS_OBJECT_FORMAT = []

if URLS_OBJECT_FORMAT:
    URLS = URLS_OBJECT_FORMAT               # dạng [{"url": ..., "mock_context": ...}]
elif URLS_STRING_FORMAT:
    URLS = [{"url": u} for u in URLS_STRING_FORMAT]
else:
    URLS = []
