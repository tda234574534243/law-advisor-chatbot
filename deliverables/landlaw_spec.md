# Tóm tắt đặc tả - Luật Đất đai (Luật Đất đai 2013)

## 1) Văn bản chọn
- Luật Đất đai 2013 (Luật số 45/2013/QH13) và văn bản hướng dẫn (Nghị định, Thông tư)

## 2) Keyphrases theo chủ đề (ví dụ)
- Quyền và chủ thể: `quyền sử dụng đất`, `chủ sử dụng`, `người sử dụng đất`
- Giao đất / thuê: `giao đất`, `cho thuê đất`, `nhận chuyển nhượng`
- Giấy tờ: `giấy chứng nhận quyền sử dụng đất`, `đăng ký đất đai`, `sổ đỏ`
- Mục đích/loại: `đất ở`, `đất nông nghiệp`, `chuyển mục đích sử dụng đất`
- Thu hồi / bồi thường: `thu hồi đất`, `bồi thường`, `tái định cư`
- Tranh chấp: `tranh chấp đất đai`, `khiếu nại`, `khởi kiện`
- Quy hoạch: `quy hoạch sử dụng đất`, `bản đồ địa chính`

## 3) Data model (đề xuất)
- document: {
  - `chuong`, `ten_chuong`, `dieu` (số điều),
  - `noi_dung` (text),
  - `keyphrase` (list),
  - `source` (Luật Đất đai 2013 / nghị định / feedback),
  - optional: `confidence`, `tags`
}

## 4) Tìm kiếm & Trả lời (kiến trúc)
- Preprocessing: tách thành doc trên từng điều/khoản, gắn `keyphrase` rule-based
- Indexing options:
  - TF-IDF (scikit-learn) cho prototype nhẹ
  - Embeddings (sentence-transformers) cho tìm ngữ nghĩa
- Search pipeline:
  1. Fuzzy search (rapidfuzz) cho khớp cụm từ
  2. Keyphrase rule match
  3. Semantic search (embeddings) lấy top-k, boost nếu keyphrase trùng
- Answer generation: template tóm tắt + liệt kê block điều/khoản có trích dẫn (ví dụ "Điều X")
- Confidence threshold và fallback (nếu score thấp -> hỏi rõ hơn hoặc khuyến nghị liên hệ chuyên gia)

## 5) API / Giao diện
- Backend: `POST /ask` trả JSON { answer: [blocks], related_questions: [] }
- Frontend: hiển thị các block (title, content, source) và cho phép gửi feedback

## 6) Triển khai nhanh (gợi ý)
- Sử dụng module hiện có `backend/search.py` (đã dùng sentence-transformers).
- Nếu muốn TF-IDF: thêm script `backend/build_tfidf.py`, lưu vectorizer và ma trận.
- Thu thập feedback: `data/feedback.json` (hiện có) và chức năng promote (đã có trong `database.py`).

## 7) File bổ sung trong repo
- `data/faq_landlaw.json` : bộ câu hỏi phổ biến (đã thêm)
- `deliverables/landlaw_spec.md` : file này (tóm tắt đặc tả + hướng triển khai)

## 8) Bước tiếp theo đề xuất
- Chạy server test: `python backend/app.py` (hoặc `python app.py` từ thư mục `backend`)
- Kiểm tra dependency: `pip install -r requirements.txt` (thêm `sentence-transformers`, `rapidfuzz` nếu cần)
- Nếu muốn, tôi có thể: a) Thêm endpoint tìm kiếm TF-IDF, b) Cài đặt embeddings + build index offline, c) Mở rộng `faq_landlaw.json` với thêm câu hỏi chuyên sâu.

---
Cần tôi tiếp tục thực hiện bước kỹ thuật nào trong phần "Bước tiếp theo" (a/b/c) không?