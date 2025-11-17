# file: pdf_to_json.py
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

    # Tên chương
    lines = chap_content.splitlines()
    ten_chuong = lines[0].strip() if lines else ""
    chap_content = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

    # ===== Tách Điều =====
    article_pattern = re.compile(
        r"(Điều\s+(\d+)\.\s*([\s\S]*?))(?=Điều\s+\d+\.|$)",
        re.IGNORECASE
    )
    articles = article_pattern.findall(chap_content)

    for full_match, art_num, art_body in articles:
        art_body = re.sub(r"^Điều\s+\d+\.\s*", "", art_body).strip()

        khoan_list = []
        split_khoans = re.split(r"^(\d+)\.\s", art_body, flags=re.MULTILINE)

        # ===== Có khoản =====
        if len(split_khoans) > 1:

            if split_khoans[0].strip():
                khoan_list.append({
                    "so": None,
                    "muc": [{
                        "ky_hieu": None,
                        "noi_dung": re.sub(r"\s+", " ", split_khoans[0].strip())
                    }]
                })

            for j in range(1, len(split_khoans), 2):
                so_khoan = int(split_khoans[j])
                text_khoan = split_khoans[j + 1].strip()

                # ===== Tách ĐIỂM: a), b), c), d), đ), e), g)... =====
                muc_pattern = r"([a-zA-Zđ])\)\s*(.*?)(?=([a-zA-Zđ])\)|$)"
                muc_matches = re.findall(
                    muc_pattern,
                    text_khoan,
                    flags=re.DOTALL | re.IGNORECASE
                )

                muc_list = []

                if muc_matches:
                    for m in muc_matches:
                        ky_hieu = m[0].strip().lower()
                        noi_dung = re.sub(r"\s+", " ", m[1].strip())
                        muc_list.append({
                            "ky_hieu": ky_hieu,
                            "noi_dung": noi_dung
                        })
                else:
                    muc_list.append({
                        "ky_hieu": None,
                        "noi_dung": re.sub(r"\s+", " ", text_khoan)
                    })

                khoan_list.append({"so": so_khoan, "muc": muc_list})

        else:
            # ===== Điều không có khoản =====
            khoan_list = [{
                "so": None,
                "muc": [{
                    "ky_hieu": None,
                    "noi_dung": re.sub(r"\s+", " ", art_body)
                }]
            }]

        keyphrase = generate_keyphrase(art_body, n=15)

        law_items.append({
            "chuong": chap_title_line,
            "ten_chuong": ten_chuong,
            "dieu": int(art_num),
            "khoan": khoan_list,
            "keyphrase": keyphrase
        })

# ===== 3. Ghi JSON =====
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(law_items, f, ensure_ascii=False, indent=2)

print(f"Hoàn thành! Đã tạo {OUTPUT_JSON} với {len(law_items)} điều luật.")
