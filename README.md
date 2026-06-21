# 🌿 Eco-Barter AI Platform
**An Autonomous Agentic Platform for Dynamic Food Rescuing & Zero-Waste Distribution**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Fast%20AI-f37626?style=for-the-badge)](https://groq.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

---

## 🌟 Vấn đề & Giải pháp (Problem Statement)

Tại các siêu thị và cửa hàng tiện lợi, hàng ngàn tấn thực phẩm hoàn toàn chất lượng bị tiêu hủy mỗi ngày chỉ vì "chạm mốc 24h cuối cùng", trong khi các tổ chức từ thiện thiếu hụt nguồn cung an toàn. 

**Eco-Barter** giải quyết bài toán này bằng một **AI Agent tự chủ** hoạt động theo thời gian thực:
1. **Dynamic Pricing (Định giá động):** Tự động suy luận mức chiết khấu tăng dần (20% -> 40% -> 60%) dựa trên gia tốc đếm ước lượng tính từ mốc thời gian thực hiện tại đến hạn chót của ngày hết hạn sản phẩm. Khi thời gian chạm mốc rủi ro cao (< 6 tiếng), Agent lập tức kích hoạt kịch bản xả kho với mức chiết khấu tối đa 60%.
2. **Zero-Waste Fallback (Kích hoạt từ thiện):** Khi sản phẩm chính thức hết giờ mở bán thương mại hoặc hệ thống kích hoạt trạng thái khẩn cấp, Agent tự động gỡ mác thương mại, chuyển dịch 100% hàng hóa sang mác **"Quyên góp Chữ Thập Đỏ (0đ)"** để giải quyết triệt để vấn đề rác thải thực phẩm.

---

## 🧠 Kiến trúc Luồng tư duy Agent (Autonomy Workflow)

Hệ thống tuân thủ nghiêm ngặt mô hình **ReAct (Reason + Act)** thông qua Groq LLaMA-3.3-70B:

```text
[POS Data / Kho hàng] ──> (Step 1: Observe) ──> LLaMA 70B Engine
                                                      │
[Cập nhật UI / Dataframe] <── (Step 3: Action) <── (Step 2: Reason/Map)
```

* **Deterministic Routing:** Lược đồ Prompt được phong ấn cấu trúc (JSON-Schema bọc thép), loại bỏ hoàn toàn hiện tượng *Hallucination* (bịa giá hoặc sinh ra key sai lệch) của LLM.

---

## 🛡️ Điểm nhấn Kỹ thuật: Hệ thống Chống sập & Tự phục hồi (Fail-Safe & Self-Healing)
*(Đáp ứng trực tiếp Tiêu chí số 9 của Hackathon)*

Hệ thống được thiết kế theo tư duy **Fail-Safe** của ngành An toàn Thông tin:

1. **Anti-Crash API Timeout:** Bọc giới hạn `timeout=5.0s`. Nếu LLM Server bị nghẽn tải, Agent không để ứng dụng bị treo mà lập tức trả về `API_TIMEOUT`.
2. **JSON Extractor Immune:** Tích hợp bộ bóc tách chuỗi thuần Python ở tầng Output. Kể cả khi LLM trả về chuỗi bọc rác markdown, hệ thống vẫn tự lọc sạch được tệp JSON gốc để nạp vào bộ nhớ.
3. **Chế độ xả kho khẩn cấp (Charity Fallback Engine):** 
   * Tại Sidebar có một công tắc **"🔥 Kích hoạt Giả lập Lỗi kết nối API"**. 
   * Khi bật công tắc (hoặc khi siêu thị thực sự bị đứt cáp/mất mạng internet), AI Agent lập tức bẻ lái luồng dữ liệu sang Local Engine: **Tự động gán toàn bộ sản phẩm cận hạn trong ngày về giá 0 VND và gán mác "Quyên góp Khẩn cấp"**. 
   * *Logic:* "Khi hệ thống AI thương mại gục ngã, an sinh xã hội và bảo vệ môi trường sẽ tiếp quản."

---

## ⚙️ Cài đặt & Chạy thử nghiệm (Local Setup)

1. **Clone repository về máy:**
```bash
git clone [https://github.com/Lightning-cloud2/EcoBarter-AI-Agent.git](https://github.com/Lightning-cloud2/EcoBarter-AI-Agent.git)
cd EcoBarter-AI-Agent
```

2. **Cài đặt các thư viện môi trường:**
```bash
pip install -r requirements.txt
```

3. **Cấu hình API Key bảo mật (Bắt buộc dưới máy local):**
* Tạo một file văn bản đặt tên chính xác là `.env` tại thư mục gốc của dự án dưới máy tính.
* Dán chuỗi Groq API Key của bạn vào file theo cú pháp:
```text
GROQ_API_KEY=gsk_your_api_key_here
```

4. **Khởi chạy ứng dụng:**
```bash
# Cách 1: Chạy trực tiếp
streamlit run app.py

# Cách 2: Nếu gặp lỗi "not recognized", sử dụng lệnh này:
python -m streamlit run app.py
```

-------------------------------------------------------------------------
