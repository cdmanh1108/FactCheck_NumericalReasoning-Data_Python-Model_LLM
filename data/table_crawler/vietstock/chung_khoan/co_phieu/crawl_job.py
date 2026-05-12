# =====================================================================
# CRAWL JOB CONFIG — Thành viên chỉ cần sửa file này
# =====================================================================

from vietstock.chung_khoan.co_phieu.Cms3GetTopStockChange import Cms3GetTopStockChange
from vietstock.chung_khoan.co_phieu.KQGDGiaoDichTuDoanhTopStockFilterForIframe import KQGDGiaoDichTuDoanhTopStockFilterForIframe
from vietstock.chung_khoan.co_phieu.KQGDGiaoDichTuDoanhChartByAllForIframe import KQGDGiaoDichTuDoanhChartByAllForIframe
from vietstock.chung_khoan.co_phieu.KQGDGiaoDichNDTNNTopStockFilterForIframe import KQGDGiaoDichNDTNNTopStockFilterForIframe
from vietstock.chung_khoan.co_phieu.KQGDGiaoDichNDTNNChartByAllForIframe import KQGDGiaoDichNDTNNChartByAllForIframe
from vietstock.chung_khoan.co_phieu.GetCPAnhHuongManh import GetCPAnhHuongManh

# 1. Cấu hình Exporter (thư mục lưu & metadata cho cột data)
EXPORTER_CONFIG = {
    "member_name": "Manh",
    "author":      "Vietstock",
    "topic":       "Chứng khoán",        # tiếng Việt → ghi vào cột Topic
    "topic_path":  "chung_khoan",        # dạng path  → tạo thư mục
    "sub_topic":      "Cổ phiếu",   # tiếng Việt (tuỳ chọn)
    "sub_topic_path": "co_phieu",   # dạng path  (tuỳ chọn)
}

# 2. Selector để lấy nội dung văn bản bài báo (mỗi website khác nhau)
ARTICLE_SELECTOR = ".article-content p"  # vietstock.vn: lấy hết p.pHead + p.pBody

# 3. Danh sách Parser — thêm/bớt tuỳ endpoint cần bắt
PARSERS = [
    Cms3GetTopStockChange(),
    KQGDGiaoDichTuDoanhTopStockFilterForIframe(),
    KQGDGiaoDichTuDoanhChartByAllForIframe(),
    KQGDGiaoDichNDTNNTopStockFilterForIframe(),
    KQGDGiaoDichNDTNNChartByAllForIframe(),
    GetCPAnhHuongManh(),
]

# 3. Danh sách URL đầu vào — cái nào có data thì dùng cái đó
try:
    from vietstock.chung_khoan.co_phieu.urls_input import URLS_STRING_FORMAT
except ImportError:
    URLS_STRING_FORMAT = []

try:
    from vietstock.chung_khoan.co_phieu.urls_input import URLS_OBJECT_FORMAT
except ImportError:
    URLS_OBJECT_FORMAT = []

if URLS_OBJECT_FORMAT:
    URLS = URLS_OBJECT_FORMAT               # dạng [{"url": ..., "mock_context": ...}]
elif URLS_STRING_FORMAT:
    URLS = [{"url": u} for u in URLS_STRING_FORMAT]
else:
    URLS = []
