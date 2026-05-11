from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from table_parser import linearize_table
from model_inference import ai_model
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI(title="ViFactCheck Numerical API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FactCheckRequest(BaseModel):
    claim: str
    html_context: str

@app.post("/api/verify")
async def verify_claim(request: FactCheckRequest):
    # 1. Bóc tách bảng biểu thành văn bản (Theo hướng FEVEROUS)
    table_text = linearize_table(request.html_context)
    
    # 2. Bóc tách văn bản thường từ HTML
    soup = BeautifulSoup(request.html_context, 'html.parser')
    plain_text = soup.get_text(separator=' ', strip=True)
    
    # 3. Gộp toàn bộ thành Full Context
    full_context = plain_text + " " + table_text
    
    # 4. Đưa vào mô hình AI xử lý
    result = ai_model.predict(request.claim, full_context)
    
    return {
        "status": "success",
        "claim": request.claim,
        "prediction": result["prediction"],
        "evidence": result["evidence"],
        "parsed_context": full_context # Trả về để Frontend có thể debug xem bảng đã biến thành chữ đúng chưa
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)