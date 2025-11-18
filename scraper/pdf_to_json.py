import pdfplumber
import re
import json

PDF_PATH = "VanBanGoc_31-2024-qh15_1.pdf"
OUTPUT_JSON = "law_db.json"

# ===== 1. Đọc PDF =====
all_text = ""
with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            all_text += page_text + "\n"

# ===== 2. Chia Chương =====
chapters = re.split(r"(Chương\s+[IVXLC]+)", all_text, flags=re.IGNORECASE)
law_items = []

# ===== Hàm tạo keyphrase =====
def generate_keyphrase(text, n=15):
    clean_text = re.sub(r"[^\w\s]", " ", text)
    clean_text = re.sub(r"\d+", "", clean_text)
    words = [w.lower() for w in clean_text.split() if w.strip()]
    return words[:n]

# ===== Xử lý từng chương =====
for i in range(1, len(chapters), 2):
    chap_title_line = chapters[i].strip()
    chap_content = chapters[i+1].strip()

    # Lấy tên chương (dòng đầu tiên)
    lines = chap_content.splitlines()
    ten_chuong = lines[0].strip() if lines else ""
    chap_body = "\n".join(lines[1:]).strip()

    # ===== Tách Điều =====
    article_pattern = re.compile(
        r"(Điều\s+(\d+)\.\s*([\s\S]*?))(?=Điều\s+\d+\.|$)",
        re.IGNORECASE
    )
    articles = article_pattern.findall(chap_body)

    for full_match, art_num, art_body in articles:
        art_body = re.sub(r"^Điều\s+\d+\.\s*", "", art_body).strip()

        # ===== Tạo item đơn giản =====
        law_items.append({
            "chuong": chap_title_line,
            "ten_chuong": ten_chuong,
            "dieu": int(art_num),
            "noi_dung": re.sub(r"\s+", " ", art_body),
            "keyphrase": generate_keyphrase(art_body, n=15)
        })

# ===== 3. Ghi JSON =====
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(law_items, f, ensure_ascii=False, indent=2)

print(f"Đã tạo {OUTPUT_JSON} với {len(law_items)} điều.")
