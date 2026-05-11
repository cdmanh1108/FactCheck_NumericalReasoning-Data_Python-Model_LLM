from playwright.sync_api import sync_playwright

class BasePlaywrightCrawler:
    def __init__(self, headless=True):
        self.headless = headless

    def fetch_with_interception(self, url, api_endpoints, parsers_dict):
        """
        Hàm dùng chung để vào 1 URL và bắt nhiều API cùng lúc.
        - api_endpoints: List các từ khóa URL API cần bắt.
        - parsers_dict: Dictionary chứa các hàm parse tương ứng.
        """
        collected_texts = []

        def handle_response(response):
            # Lặp qua các endpoint để kiểm tra xem gói tin có khớp không
            for endpoint, parser_func in parsers_dict.items():
                if endpoint in response.url and response.status == 200:
                    try:
                        json_data = response.json()
                        text_result = parser_func(json_data)
                        if text_result:
                            collected_texts.append(text_result)
                    except Exception as e:
                        print(f"Lỗi parse {endpoint}: {e}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            # Bật chế độ lắng nghe mạng
            page.on("response", handle_response)
            
            print(f"🌐 Đang truy cập và lắng nghe: {url}")
            page.goto(url, wait_until="networkidle")
            
            browser.close()
            
        return " ".join(collected_texts)