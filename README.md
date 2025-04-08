# 📸 AI Screen Translator

- ✨ Một ứng dụng Windows giúp bạn **chụp ảnh màn hình, và hỏi AI để dịch hoặc giải thích nội dung ngay lập tức** – không cần mở trình duyệt, không cần gõ tay từng chữ!

---

## 🚀 Tính năng nổi bật

- 📷 Chụp nhanh ảnh màn hình với phím tắt
- 🌐 Tự động gửi ảnh đến AI (Gemini API)
- 💬 Hiển thị câu trả lời trực tiếp trên màn hình
- 🪶 Giao diện đơn giản, nhẹ, dễ sử dụng

---

## 🧑‍💻 Cách hoạt động

1. Nhấn phím tắt để kích hoạt ứng dụng.
2. Dùng công cụ mặc định của Windows (Snipping Tool) để chọn vùng ảnh.
3. Hình ảnh được gửi đến AI để dịch hoặc giải thích nội dung
4. Kết quả hiển thị ngay trên màn hình.

---

## 🛠 Cài đặt

1. Clone repo:
- git clone https://github.com/pham-van-man/AIScreenTranslator.git
2. Cấu hình API key trong .env:
- Vào trong chủ của Google Studio, sau đó đăng kí lấy cho mình một api_key của gemini-2.0-flash
- Dán nó vào file config.env với cú pháp sau: gemini_api_key=your_key_here
3. Cấu hình rules:
- Mở file rules.txt
- Gõ yêu cầu của bạn vào file sau đó lưu lại
- Các request gửi đến AI sẽ gửi kèm theo các yêu cầu bên trong file rules.txt
3. Chạy ứng dụng:
- Chạy trực tiếp bằng file app.exe hoặc python app.py (cần có môi trường python)
4. Sử dụng ứng dụng:
- Mở ứng dụng bằng phím tắt Ctrl + Alt + X
- Kéo thả chuột tạo vùng chọn
- Đợi AI đưa ra câu trả lời

---

## 🧩 Công nghệ sử dụng

- Python
- Gemini API (gemini-2.0-flash)
- Windows Snipping Tool (cho trải nghiệm cắt ảnh mượt mà)

---

## 💡 Động lực

- Mình tạo ra ứng dụng này vì bản thân từng cảm thấy việc dịch văn bản trên màn hình rất bất tiện, đặc biệt là khi phải tra cứu kỹ thuật hoặc đọc tài liệu nước ngoài. Không có công cụ nào thực sự làm điều này nhanh gọn, nên mình tự tay viết ra giải pháp mà mình luôn cần.

---

## 📬 Góp ý & Liên hệ

- Nếu bạn thấy ứng dụng hữu ích, hãy ⭐ repo này nhé!
- Mọi góp ý, ý tưởng hay báo lỗi, vui lòng tạo issue hoặc liên hệ mình qua email: phamvanmancomvn@gmail.com

---

## Made with 💻 and ☕ by Mẫn