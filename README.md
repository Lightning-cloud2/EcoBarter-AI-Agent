# 🌿 Eco-Barter AI Platform
**Hệ thống AI Agent tự chủ giải cứu thực phẩm cận date (Hackathon Prototype)**

### 🚀 Giới thiệu
Dự án được phát triển tại Hackathon AIDEV Summer 2026. Đây là giải pháp AI Agent giúp các siêu thị tự động hóa quy trình xử lý thực phẩm cận date, tối ưu doanh thu và giảm thiểu lãng phí thực phẩm.

### 🤖 Tính năng cốt lõi (Agentic Workflow)
- **Real-time Monitoring:** Tự động lấy thời gian hệ thống, quét kho POS và tính toán giờ đếm ngược đến hạn chót (0h00 ngày hôm sau).
- **Dynamic Pricing Tool:** Tự động áp dụng mức giảm giá linh hoạt (20% - 40% - 60%) theo thời gian thực.
- **Autonomous Re-planning:** Khi gặp sự cố API thông báo (Lỗi 503), Agent tự động thay đổi kế hoạch (Re-plan) để chuyển hướng hàng hóa sang luồng quyên góp từ thiện cho Hội Chữ Thập Đỏ.

### 🛠️ Công nghệ sử dụng
- **Ngôn ngữ:** Python
- **Framework:** Streamlit (Giao diện), Pandas (Xử lý dữ liệu)
- **Kiến trúc:** Single-Agent thực chiến kết hợp Tool-use.

### 📦 Hướng dẫn cài đặt & Chạy thử
1. Clone dự án: `git clone https://github.com/username/EcoBarter-AI-Agent.git`
2. Cài đặt thư viện: `pip install -r requirements.txt`
3. Chạy ứng dụng: `streamlit run app.py`

---
**Thực hiện bởi:** Lê Anh Quyền - Nhóm Infinity
