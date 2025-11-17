# 📌 Data – Chatbot Luật Đất Đai

Thư mục `data/` chứa các **tập dữ liệu luật và feedback** phục vụ cho backend chatbot Luật Đất Đai. Đây là nguồn dữ liệu để thực hiện:

* Tìm kiếm luật theo keyphrase
* Fuzzy search
* Semantic search
* Huấn luyện, cập nhật phản hồi người dùng

Frontend và backend **không lưu trữ dữ liệu trực tiếp** ở nơi khác, tất cả đều dùng dữ liệu từ thư mục này.

---

## 📁 Các file chính

```
data/
├── luat_dat_dai.json   # Dữ liệu luật gốc (tham khảo)
├── law_db.json         # Dữ liệu luật được backend sử dụng (có thể cập nhật từ feedback)
└── feedback.json       # Lưu phản hồi người dùng (tự tạo khi chạy backend)
```

---

## 📝 1. `luat_dat_dai.json`

* Là bản **dữ liệu luật gốc**, phục vụ tham khảo và reset cơ sở dữ liệu.
* Mỗi mục là một điều luật gồm:

  * `chuong` – tên chương
  * `ten_chuong` – mô tả chương
  * `dieu` – số điều
  * `noi_dung` – nội dung luật
  * `keyphrase` – các từ khóa chính dùng cho tìm kiếm

Ví dụ:

```json
{
  "chuong": "Chương I",
  "ten_chuong": "Những quy định chung",
  "dieu": 1,
  "noi_dung": "Phạm vi điều chỉnh và đối tượng áp dụng của Luật Đất đai.",
  "keyphrase": ["phạm vi điều chỉnh", "đối tượng áp dụng"]
}
```

---

## 📝 2. `law_db.json`

* Là **dữ liệu chính mà backend dùng để trả lời câu hỏi**.
* Có thể được cập nhật tự động từ **feedback người dùng** thông qua API `/feedback` và chức năng promote.
* Cấu trúc tương tự `luat_dat_dai.json`, nhưng có thể thêm keyphrase mới, confidence và nguồn:

```json
{
  "chuong": "Chương III",
  "ten_chuong": "Trách nhiệm sử dụng đất",
  "dieu": 10,
  "noi_dung": "Người sử dụng đất phải sử dụng đất đúng mục đích, bảo vệ đất và thực hiện nghĩa vụ tài chính.",
  "keyphrase": [
    "sử dụng đất đúng mục đích",
    "nghĩa vụ tài chính",
    "trách nhiệm",
    "nghĩa vụ"
  ]
}
```

* Backend load file này khi khởi động và **refresh embeddings** để thực hiện tìm kiếm semantic.

---

## 📝 3. `feedback.json`

* Lưu các phản hồi người dùng gửi qua frontend.
* Mỗi mục gồm:

```json
{
  "question": "Người sử dụng đất có thể cho thuê đất không?",
  "answer": "Người sử dụng đất có quyền cho thuê, chuyển nhượng, thừa kế quyền sử dụng đất.",
  "user": "user1"
}
```

* Backend có thể **promote feedback** để thêm vào `law_db.json` nếu phù hợp.

---

## 🔧 Cách dùng

1. **Reset dữ liệu luật**: chạy `backend/reset_db.py` sẽ tạo lại `law_db.json` từ `luat_dat_dai.json` và xóa `feedback.json`.
2. **Backend tự load dữ liệu** khi chạy `app.py`.
3. **Cập nhật dữ liệu**: khi nhận feedback từ người dùng, backend có thể thêm luật mới vào `law_db.json`.

---

