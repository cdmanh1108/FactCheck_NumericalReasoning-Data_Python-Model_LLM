from bs4 import BeautifulSoup

def linearize_table(html_content: str) -> str:
    """
    Chuyển đổi bảng HTML thành chuỗi văn bản tuyến tính để đưa vào Context.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        return ""
    
    linearized_text = "\n[DỮ LIỆU TỪ BẢNG]: "
    
    for table in tables:
        rows = table.find_all('tr')
        for row_idx, row in enumerate(rows):
            cols = row.find_all(['th', 'td'])
            col_texts = [col.get_text(strip=True) for col in cols]
            if col_texts:
                linearized_text += f"(Hàng {row_idx + 1}) " + " | ".join(col_texts) + ". "
                
    return linearized_text