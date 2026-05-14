# =====================================================================
# CRAWL JOB CONFIG — Thành viên chỉ cần sửa file này
# =====================================================================
import importlib

# Import TẤT CẢ các parser từ thư mục parsers dùng chung
from vietstock.chung_khoan.parsers.Cms3GetTopStockChange import Cms3GetTopStockChange
from vietstock.chung_khoan.parsers.KQGDGiaoDichTuDoanhTopStockFilterForIframe import KQGDGiaoDichTuDoanhTopStockFilterForIframe
from vietstock.chung_khoan.parsers.KQGDGiaoDichTuDoanhChartByAllForIframe import KQGDGiaoDichTuDoanhChartByAllForIframe
from vietstock.chung_khoan.parsers.KQGDGiaoDichNDTNNTopStockFilterForIframe import KQGDGiaoDichNDTNNTopStockFilterForIframe
from vietstock.chung_khoan.parsers.KQGDGiaoDichNDTNNChartByAllForIframe import KQGDGiaoDichNDTNNChartByAllForIframe
from vietstock.chung_khoan.parsers.GetCPAnhHuongManh import GetCPAnhHuongManh
from vietstock.chung_khoan.parsers.gettradingresultdrawchart import gettradingresultdrawchart
from vietstock.chung_khoan.parsers.FinanceStaticChartData import FinanceStaticChartData
from vietstock.chung_khoan.parsers.GetDataStaticDataCustom import GetDataStaticDataCustom
from vietstock.chung_khoan.parsers.FinanceInfoChart import FinanceInfoChart

# 1. Cấu hình Exporter (thư mục lưu & metadata cho cột data)
# ĐỔI THÔNG TIN Ở ĐÂY ĐỂ CRAWL CÁC SUB-TOPIC KHÁC NHAU
EXPORTER_CONFIG = {
    "member_name": "Manh",
    "author":      "Vietstock",
    "topic":       "Chứng khoán",        # tiếng Việt → ghi vào cột Topic
    "topic_path":  "chung_khoan",        # dạng path  → tạo thư mục
    "sub_topic":      "Cổ phiếu",        # tiếng Việt (tuỳ chọn) -> VD: "Cổ phiếu", "Niêm yết", "Giao dịch nội bộ"
    "sub_topic_path": "co_phieu",        # dạng path  (tuỳ chọn) -> VD: "co_phieu", "niem_yet", "giao_dich_noi_bo"
}

# 2. Selector để lấy nội dung văn bản bài báo (mỗi website khác nhau)
ARTICLE_SELECTOR = ".article-content p"  # vietstock.vn: lấy hết p.pHead + p.pBody

# 3. Danh sách Parser — Dùng TẤT CẢ các parser hiện có
PARSERS = [
    Cms3GetTopStockChange(),
    KQGDGiaoDichTuDoanhTopStockFilterForIframe(),
    KQGDGiaoDichTuDoanhChartByAllForIframe(),
    KQGDGiaoDichNDTNNTopStockFilterForIframe(),
    KQGDGiaoDichNDTNNChartByAllForIframe(),
    GetCPAnhHuongManh(),
    gettradingresultdrawchart(),
    FinanceStaticChartData(),
    GetDataStaticDataCustom(),
    FinanceInfoChart(),
]

# 4. Tự động load URL từ urls_input.py của sub_topic tương ứng ---- đổi
sub_topic_path = EXPORTER_CONFIG.get("sub_topic_path", "")
urls_module_name = f"vietstock.chung_khoan.{sub_topic_path}.urls_input"

URLS_STRING_FORMAT = []
URLS_OBJECT_FORMAT = []

try:
    urls_module = importlib.import_module(urls_module_name)
    URLS_STRING_FORMAT = getattr(urls_module, "URLS_STRING_FORMAT", [])
    URLS_OBJECT_FORMAT = getattr(urls_module, "URLS_OBJECT_FORMAT", [])
except ImportError as e:
    print(f"Warning: Không thể load được urls từ {urls_module_name}.py (Lỗi: {e})")

if URLS_OBJECT_FORMAT:
    URLS = URLS_OBJECT_FORMAT               # dạng [{"url": ..., "mock_context": ...}]
elif URLS_STRING_FORMAT:
    URLS = [{"url": u} for u in URLS_STRING_FORMAT]
else:
    URLS = []
