import os
import sys
import importlib
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Đảm bảo Python luôn tìm thấy data_exporter.py (nằm ở thư mục data/)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env từ thư mục gốc dự án (2 cấp trên main.py)
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

from playwright.sync_api import sync_playwright
from data_exporter import ViFactCheckExporter

# =====================================================================
# LOAD CRAWL JOB
# Chạy: python main.py <module_path>
# VD:   python main.py vietstock.chung_khoan.giao_dich_noi_bo.crawl_job
# Mặc định đọc từ .env → DEFAULT_JOB
# =====================================================================
DEFAULT_JOB = os.getenv("DEFAULT_JOB")

job_module_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB

try:
    job = importlib.import_module(job_module_path)
except ModuleNotFoundError as e:
    print(f"❌ Không tìm thấy job module: {job_module_path}\n   ({e})")
    sys.exit(1)

EXPORTER_CONFIG = job.EXPORTER_CONFIG
PARSERS         = job.PARSERS
URLS            = job.URLS
ARTICLE_SELECTOR = getattr(job, "ARTICLE_SELECTOR", "p")  # fallback nếu job chưa khai báo

if not URLS:
    print("⚠️  Không tìm thấy URL nào để crawl. Kiểm tra lại crawl_job.py")
    sys.exit(0)

# =====================================================================
# ENGINE — Không cần sửa phần này
# =====================================================================
def run_crawlers():
    print(f"🚀 KHỞI ĐỘNG HỆ THỐNG CRAWLER [{job_module_path}] 🚀")
    print(f"   Member: {EXPORTER_CONFIG['member_name']} | "
          f"Topic: {EXPORTER_CONFIG['topic']} | "
          f"Parsers: {[p.__class__.__name__ for p in PARSERS]}")

    exporter = ViFactCheckExporter(**EXPORTER_CONFIG)

    # Load tập hợp URL đã crawl từ file hiện tại (nếu có) để bỏ qua khi gặp lại
    crawled_urls = exporter.get_crawled_urls()
    print(f"[Đã có sẵn] {len(crawled_urls)} URL trong data, sẽ bỏ qua.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Đổi False để debug
        page = browser.new_page()

        print(f"\n--- Đang xử lý {len(URLS)} URLs từ file input ---")

        for item in URLS:
            url = item["url"]

            # Bỏ qua nếu URL đã có trong data
            if url in crawled_urls:
                print(f"⏭️  Đã crawl rồi, bỏ qua: {url}")
                continue

            # mock_context = item.get("mock_context", "")
            collected_texts = []

            # HÀM LẮNG NGHE MẠNG (INTERCEPTION): Bắt cục JSON ngay khi biểu đồ tải xong
            def handle_response(response):
                if response.status == 200:
                    # DEBUG: in tất cả request đến vietstock để tìm endpoint đúng
                    if "vietstock.vn" in response.url and response.request.method in ("GET", "POST"):
                        print(f"  [DEBUG {response.request.method}] {response.url[:120]}")
                    if response.request.method == "POST":
                        for parser in PARSERS:
                            if parser.endpoint in response.url:
                                try:
                                    result = parser.parse(response.json())
                                    if result:
                                        collected_texts.append(result)
                                        print(f"  ✅ Bắt được bảng [{parser.__class__.__name__}]")
                                except Exception as e:
                                    print(f"  [PARSE ERROR] {parser.__class__.__name__}: {e}")
                                break  # Mỗi response chỉ khớp 1 parser

            page.on("response", handle_response)

            print(f"🌐 Đang truy cập: {url}")
            try:
                page.goto(url, wait_until="load", timeout=60_000)
                # Chờ thêm để chart iframe có thời gian khởi tạo và gọi API
                page.wait_for_timeout(5_000)
            except Exception as e:
                print(f"⚠️ Timeout/lỗi khi tải trang, bỏ qua: {url}\n   ({e})")
                page.remove_listener("response", handle_response)
                continue

            page.remove_listener("response", handle_response)

            # Scrape nội dung văn bản bài báo (pTitle + pHead + pBody + pAuthor + pSource)
            # .article-content p đã bao gồm tiêu đề ở index 0 — không cần page.title() riêng
            try:
                paragraphs = page.locator(ARTICLE_SELECTOR).all_inner_texts()
                article_text = " ".join(p.strip() for p in paragraphs if p.strip())
            except Exception:
                article_text = ""

            if collected_texts:
                # Full Context = [Văn bản bài báo] + [Bảng số liệu tài chính đã ép phẳng]
                table_text = " ".join(filter(None, collected_texts))
                full_context = " ".join(filter(None, [article_text, table_text]))
                exporter.add_record(context=full_context, url=url)
            else:
                print(f"⚠️ Không tìm thấy bảng API nào, bỏ qua lưu: {url}")

        browser.close()

    print("\n💾 Đang xuất dữ liệu ra file Parquet...")
    exporter.save_to_parquet()


if __name__ == "__main__":
    run_crawlers()