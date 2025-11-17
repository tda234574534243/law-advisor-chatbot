<a id="readme-top"></a>
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green)](https://flask.palletsprojects.com/)
[![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-2.2-orange)](https://www.sbert.net/)
[![Unlicense License](https://img.shields.io/badge/License-Unlicense-lightgrey)](https://unlicense.org/)

  <h2 align="center">Chatbot Luật Đất Đai - Semantic Search Q&A</h2>

  <p align="center">
    Ứng dụng tra cứu kiến thức pháp luật chuyên sâu về Luật Đất Đai bằng Semantic Search và Feedback Loop.
  </p>
</div>

<details>
  <summary>Mục lục</summary>
  <ol>
    <li>
      <a href="#about-the-project">Về Dự án</a>
      <ul>
        <li><a href="#built-with">Công nghệ sử dụng</a></li>
        <li><a href="#features">Tính năng cốt lõi</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Bắt đầu</a>
      <ul>
        <li><a href="#prerequisites">Yêu cầu</a></li>
        <li><a href="#installation">Cài đặt</a></li>
      </ul>
    </li>
    <li><a href="#usage">Hướng dẫn sử dụng</a></li>
    <li><a href="#project-structure">Cấu trúc Dự án</a></li>
    <li><a href="#data-and-feedback">Dữ liệu & Cơ chế Feedback</a></li>
    <li><a href="#license">Bản quyền</a></li>
    <li><a href="#contact">Liên hệ</a></li>
    <li><a href="#acknowledgments">Lời cảm ơn</a></li>
  </ol>
</details>


## Về Dự án ⚖️

**Chatbot Luật Đất Đai** là một ứng dụng Hỏi & Đáp (Q&A) được xây dựng để hỗ trợ tra cứu các vấn đề liên quan đến Luật Đất Đai. Thay vì chỉ sử dụng tìm kiếm từ khóa truyền thống, hệ thống này khai thác sức mạnh của **Semantic Search** (Tìm kiếm ngữ nghĩa) để hiểu ý định thực sự của câu hỏi, ngay cả khi người dùng sử dụng từ ngữ khác nhau.

Đây là một giải pháp hiệu quả để:
* **Tăng độ chính xác** trong việc tìm kiếm các điều khoản luật liên quan.
* Hỗ trợ **tra cứu nhanh** cho các chuyên viên tư vấn hoặc người dân.
* Cung cấp khả năng **học hỏi liên tục** từ phản hồi của người dùng để cải thiện chất lượng trả lời.

<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>

### Tính năng cốt lõi ✨
* **Tra cứu Ngữ nghĩa (Semantic Search)**: Sử dụng mô hình Sentence Transformers để tìm kiếm câu trả lời dựa trên ý nghĩa của câu hỏi, không chỉ là từ khóa.
* **Đề xuất Câu hỏi Liên quan**: Gợi ý các câu hỏi khác có ý nghĩa tương tự câu hỏi hiện tại.
* **Highlight Keyphrase**: Tự động làm nổi bật các từ/cụm từ quan trọng trong câu trả lời.
* **Cơ chế Feedback**: Cho phép người dùng đánh dấu và gửi các cặp "Câu hỏi - Câu trả lời đúng" để thêm vào cơ sở dữ liệu.
* **Hỗ trợ Hội thoại (Multi-turn)**: Lưu lại lịch sử hội thoại để cung cấp ngữ cảnh tốt hơn cho các câu hỏi tiếp theo.

<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>

---

## Bắt đầu 🚀

### Yêu cầu (Prerequisites)

Bạn cần cài đặt các yêu cầu sau trên hệ thống của mình:

* **Python 3.10+**
* **pip** (Công cụ quản lý gói của Python)

### Cài đặt (Installation)

1.  **Clone Repository:**
    ```sh
    git clone [https://github.com/tên_người_dùng_github_của_bạn/chatbot-luat-dat-dai.git](https://github.com/tên_người_dùng_github_của_bạn/chatbot-luat-dat-dai.git)
    cd chatbot-luat-dat-dai
    ```
2.  **Cài đặt các gói Python:**
    ```sh
    pip install -r requirements.txt
    ```
    *Hoặc cài đặt thủ công:*
    ```sh
    pip install flask tinydb torch sentence-transformers
    ```
3.  **Tải mô hình Embedding** (Sentence Transformers sẽ tự động tải khi chạy lần đầu, nhưng yêu cầu kết nối mạng).

<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>

---

## Hướng dẫn sử dụng

Làm theo các bước sau để chạy và sử dụng chatbot:

1.  **Chạy Backend (Flask Server):**
    ```sh
    cd backend
    python app.py
    ```
    *Server sẽ khởi động tại cổng 5000.*

2.  **Mở Giao diện Người dùng:**
    Mở trình duyệt web của bạn và truy cập vào địa chỉ:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```
3.  **Sử dụng Chatbot:**
    * Nhập câu hỏi của bạn về Luật Đất Đai.
    * Nhấn "Gửi" để nhận câu trả lời.
    * Sử dụng nút **"👍 Feedback"** nếu bạn thấy câu trả lời không chính xác hoặc muốn bổ sung kiến thức mới. Dữ liệu này sẽ được lưu vào `law_db.json`.

<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>

---

## Cấu trúc Dự án 📂

Dưới đây là cấu trúc thư mục chính của dự án:

```bash
.
├── .gitignore
├── README.md
├── requirements.txt
|
├── 📁 backend
│   ├── app.py # Flask app, định tuyến API
│   ├── bot.py # Logic Chatbot (Semantic Search, Gợi ý, Multi-turn)
│   ├── database.py # Xử lý TinyDB (lưu/truy vấn dữ liệu)
│   └── search.py # Logic Sentence Transformer (tính embedding, similarity)
|
├── 📁 data
│   ├── law_db.json # Cơ sở dữ liệu chính (TinyDB, lưu trữ Q&A sau khi feedback)
│   └── luat_dat_dai.json # Nguồn dữ liệu luật ban đầu (Initial seed data)
|
└── 📁 frontend
    ├── index.html # Giao diện Chatbot
    ├── main.js # Xử lý Frontend logic & API call
    └── style.css # CSS styling
```
## Dữ liệu & Cơ chế Feedback 🔄
--- Cơ chế Hoạt động (Feedback Loop)
- Hệ thống được thiết kế để học hỏi và cải thiện liên tục dựa trên tương tác của người dùng.
- Khởi tạo Dữ liệu: Khi chạy lần đầu và file law_db.json trống, hệ thống sẽ tự động nạp dữ liệu ban đầu từ file luat_dat_dai.json vào cơ sở dữ liệu TinyDB.
- Học hỏi Liên tục: Mọi feedback từ người dùng (các cặp câu hỏi/trả lời mới được xác nhận qua nút "👍 Feedback") sẽ được lưu trữ tệp feedback.

Cập nhật Embedding: Dữ liệu Q&A mới sẽ được xử lý để tạo embedding vector mới. Quá trình này đảm bảo Semantic Search có thể trả lời các câu hỏi tương tự trong tương lai với độ chính xác cao hơn.
<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>
## Link Dự án:
[https://github.com/tda234574534243/law-advisor-chatbot]
<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>

## Lời cảm ơn 🙏
Xin chân thành cảm ơn các dự án mã nguồn mở sau đã giúp dự án này được thực hiện:

[Flask] - Web micro-framework mạnh mẽ cho backend Python.

[Sentence-Transformers] - Thư viện thiết yếu để tạo các embedding ngữ nghĩa (Semantic embeddings) chất lượng cao.

[TinyDB] - Cơ sở dữ liệu NoSQL nhẹ, đơn giản, lý tưởng cho môi trường phát triển.

<p align="right">(<a href="#readme-top">trở về đầu</a>)</p>
