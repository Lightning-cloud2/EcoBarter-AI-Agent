import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import time
import os
import json
from groq import Groq 
from dotenv import load_dotenv

# 1. TẢI BIẾN MÔI TRƯỜNG TỪ FILE .env CỤC BỘ TRÊN MÁY
load_dotenv()

# CẤU HÌNH TRANG STREAMLIT
st.set_page_config(page_title="Eco-Barter AI Platform", page_icon="🌿", layout="wide")

st.title("🌿 Eco-Barter AI Platform")
st.subheader("Hệ thống AI Agent tự chủ giải cứu thực phẩm cận date")
st.markdown("---")

# CẤU HÌNH THANH ĐIỀU KHIỂN SIDEBAR
st.sidebar.header("⚙️ CẤU HÌNH HỆ THỐNG")

GROQ_API_KEY = st.sidebar.text_input(
    "🔑 Nhập Groq API Key:", 
    type="password", 
    value=os.environ.get("GROQ_API_KEY", "")
)

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ Vui lòng cấu hình file .env hoặc nhập Groq API Key để kích hoạt AI Agent!")

st.sidebar.markdown("---")
st.sidebar.header("🚨 CÔNG CỤ DEMO PHẢN XẠ SỰ CỐ")

simulate_network_error = st.sidebar.toggle(
    "🔥 Kích hoạt Giả lập Lỗi kết nối API", 
    value=False,
    help="Bật nút này để mô phỏng tình huống hệ thống mất mạng diện rộng hoặc API sập đột ngột nhằm demo tính năng Fail-Safe."
)

if simulate_network_error:
    st.sidebar.error("🔴 Trạng thái: Hệ thống đang ngắt kết nối với LLM Server.")
else:
    st.sidebar.success("🟢 Trạng thái: Kết nối LLM API sẵn sàng.")

# Ghim cố định ngày mốc chạy Demo của hệ thống
demo_target_date = date(2026, 6, 21)
demo_prev_date = demo_target_date - timedelta(days=1)

# 2. BẢNG ĐA NĂNG HỆ THỐNG
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"Mã SP": "SP001", "Tên sản phẩm": "Bánh mì gối tươi", "Danh mục": "Bánh ngọt/Mì", "Giá bán (VND)": 30000, "Hạn sử dụng": demo_target_date, "Trạng thái": "Chờ quét"},
        {"Mã SP": "SP002", "Tên sản phẩm": "Sữa tươi TH True Milk 1L", "Danh mục": "Sữa & Sản phẩm từ sữa", "Giá bán (VND)": 42000, "Hạn sử dụng": demo_target_date, "Trạng thái": "Chờ quét"},
        {"Mã SP": "SP003", "Tên sản phẩm": "Salad ức gà trộn sẵn", "Danh mục": "Đồ ăn chế biến sẵn", "Giá bán (VND)": 45000, "Hạn sử dụng": demo_target_date, "Trạng thái": "Chờ quét"},
        {"Mã SP": "SP004", "Tên sản phẩm": "Bánh Pudding đóng hộp", "Danh mục": "Đồ ăn chế biến sẵn", "Giá bán (VND)": 35000, "Hạn sử dụng": date(2026, 6, 22), "Trạng thái": "Chờ quét"},
        {"Mã SP": "SP005", "Tên sản phẩm": "Sữa chua nếp cẩm", "Danh mục": "Sữa & Sản phẩm từ sữa", "Giá bán (VND)": 15000, "Hạn sử dụng": date(2026, 6, 23), "Trạng thái": "Chờ quét"}
    ])

st.markdown("### 📦 Dữ liệu kho hàng POS")
edited_df = st.data_editor(
    st.session_state.inventory,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Mã SP": st.column_config.TextColumn("Mã SP", required=True),
        "Tên sản phẩm": st.column_config.TextColumn("Tên sản phẩm", required=True),
        "Danh mục": st.column_config.SelectboxColumn("Danh mục", options=["Bánh ngọt/Mì", "Sữa & Sản phẩm từ sữa", "Đồ ăn chế biến sẵn"], required=True),
        "Giá bán (VND)": st.column_config.NumberColumn("Giá bán (VND)", min_value=0, step=1000, required=True),
        "Hạn sử dụng": st.column_config.DateColumn("Hạn sử dụng", min_value=date(2026, 6, 20), format="DD-MM-YYYY", required=True),
        "Trạng thái": st.column_config.TextColumn("Trạng thái", disabled=True)
    }
)

if st.button("🔄 Đồng bộ dữ liệu cập nhật", type="secondary"):
    st.session_state.inventory = edited_df
    st.success("✅ Đã đồng bộ cấu trúc kho hàng!")
    time.sleep(0.5)
    st.rerun()

st.markdown("---")

# 3. KHU VỰC THỜI GIAN THEO 4 MỐC SỰ KIỆN CỐ ĐỊNH
st.markdown("### ⏰ Bối cảnh hệ thống (Time-Shift Simulation)")
milestones = [
    {"label": "🔴 21:00 (Hôm trước) - Khởi tạo Bong bóng Cận Date", "datetime": datetime(demo_prev_date.year, demo_prev_date.month, demo_prev_date.day, 21, 0, 0)},
    {"label": "🟡 09:00 (Hôm sau) - Khung giờ Sáng", "datetime": datetime(demo_target_date.year, demo_target_date.month, demo_target_date.day, 9, 0, 0)},
    {"label": "🟠 13:00 (Hôm sau) - Khung giờ Chiều", "datetime": datetime(demo_target_date.year, demo_target_date.month, demo_target_date.day, 13, 0, 0)},
    {"label": "🟢 21:00 (Hôm sau) - Hạn chót Quyên góp & Đóng kho", "datetime": datetime(demo_target_date.year, demo_target_date.month, demo_target_date.day, 21, 0, 0)}
]

if 'current_milestone_idx' not in st.session_state:
    st.session_state.current_milestone_idx = 0

with st.container(border=True):
    col_metric1, col_metric2 = st.columns(2)
    active_milestone = milestones[st.session_state.current_milestone_idx]
    active_datetime = active_milestone["datetime"]
    
    with col_metric1:
        st.metric(label="📅 Ngày hệ thống giả lập", value=active_datetime.strftime("%d-%m-%Y"))
    with col_metric2:
        st.metric(label="🕒 Thời gian giả lập", value=active_datetime.strftime("%H:%M"))

    selected_label = st.select_slider(
        "Kéo để chuyển đổi qua các mốc thời gian cốt lõi:",
        options=[m["label"] for m in milestones],
        value=active_milestone["label"],
        label_visibility="collapsed"
    )
    
    for idx, m in enumerate(milestones):
        if m["label"] == selected_label:
            if idx != st.session_state.current_milestone_idx:
                st.session_state.current_milestone_idx = idx
                st.rerun()

st.markdown("---")

# 4. THUẬT TOÁN ĐỔI THẲNG SANG TỪ THIỆN KHI API LỖI
def local_fallback_charity_pricing(inventory_df):
    fallback_df = inventory_df.copy()
    for idx, row in fallback_df.iterrows():
        if pd.isna(row.get("Hạn sử dụng")) or row.get("Hạn sử dụng") is None:
            fallback_df.at[idx, "Trạng thái"] = "Lỗi dữ liệu"
            continue
            
        hsd = row["Hạn sử dụng"]
        if isinstance(hsd, str):
            try:
                hsd = datetime.strptime(hsd, "%Y-%m-%d").date()
            except:
                fallback_df.at[idx, "Trạng thái"] = "Lỗi ngày"
                continue
            
        diff_with_demo_day = (hsd - demo_target_date).days
        
        if diff_with_demo_day < 0:
            fallback_df.at[idx, "Trạng thái"] = "Đã quá hạn - Hủy hàng"
            fallback_df.at[idx, "Giá bán (VND)"] = 0
        elif diff_with_demo_day == 0:
            fallback_df.at[idx, "Trạng thái"] = "Quyên góp (Khẩn cấp - API Fail)"
            fallback_df.at[idx, "Giá bán (VND)"] = 0
        elif diff_with_demo_day == 1:
            fallback_df.at[idx, "Trạng thái"] = "Còn hàng (Chờ API kết nối)"
        else:
            fallback_df.at[idx, "Trạng thái"] = "Còn hàng"
            
    return fallback_df

# 5. HÀM CORE KẾT NỐI LLM API (DÙNG DETERMINISTIC MAPPING ĐỂ KHÓA CHẾT LOGIC)
def dynamic_pricing_agent_core(inventory_json, current_milestone_str, target_date_str):
    if simulate_network_error:
        return None, "SIMULATED_NETWORK_DISCONNECT"
        
    if not GROQ_API_KEY:
        return None, "API_KEY_MISSING"
        
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        system_prompt = f"""
        Bạn là Eco-Rescue AI Agent đóng vai trò Bộ định giá tự chủ (Dynamic Pricing Router) cho siêu thị.
        Ngày mục tiêu giải cứu cốt lõi (Target Date) là: {target_date_str}.

        Hệ thống đang đứng tại mốc sự kiện: "{current_milestone_str}"

        Hãy đọc danh sách sản phẩm POS và định giá CHÍNH XÁC TUYỆT ĐỐI theo logic sau:

        1. Nếu mốc là [🔴 21:00 (Hôm trước)]:
           - Các SP có Hạn sử dụng == {target_date_str}: Trạng thái = "Giảm giá (20%)", Giá mới = int(Giá gốc * 0.8)
           - Các SP hạn xa hơn: Trạng thái = "Còn hàng", Giá mới = Giá gốc

        2. Nếu mốc là [🟡 09:00 (Hôm sau)]:
           - Các SP có Hạn sử dụng == {target_date_str}: Trạng thái = "Giảm giá (40%)", Giá mới = int(Giá gốc * 0.6)
           - Các SP hạn xa hơn: Trạng thái = "Còn hàng", Giá mới = Giá gốc

        3. Nếu mốc là [🟠 13:00 (Hôm sau)]:
           - Các SP có Hạn sử dụng == {target_date_str}: Trạng thái = "Giảm giá (60%)", Giá mới = int(Giá gốc * 0.4)
           - Các SP hạn xa hơn: Trạng thái = "Còn hàng", Giá mới = Giá gốc

        4. Nếu mốc là [🟢 21:00 (Hôm sau)]:
           - Các SP có Hạn sử dụng == {target_date_str}: Trạng thái = "Quyên góp (Chữ Thập Đỏ)", Giá mới = 0
           - Các SP có Hạn sử dụng đúng ngày hôm sau nữa (ví dụ 2026-06-22): Trạng thái = "Giảm giá (20%)", Giá mới = int(Giá gốc * 0.8)
           - Các SP hạn xa hơn nữa: Trạng thái = "Còn hàng", Giá mới = Giá gốc

        5. Các SP đã hết hạn từ trước {target_date_str}: Trạng thái = "Đã quá hạn - Hủy hàng", Giá mới = 0

        BẮT BUỘC trả về JSON hợp lệ duy nhất có key "danh_sach", bên trong là mảng các object chứa: "Mã SP", "Giá mới (VND)", "Trạng thái".
        """
        
        user_prompt = f"Dữ liệu POS đầu vào:\n{inventory_json}"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
            timeout=5.0 
        )
        return completion.choices[0].message.content, None
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return None, "API_TIMEOUT"
        return None, f"{error_msg}"

# 6. TIẾN TRÌNH TƯ DUY TỰ CHỦ CỦA AI AGENT (ĐÃ SỬA LỖI KEYERROR TẠI ĐÂY)
if st.button("🤖 Kích hoạt Eco-Rescue Agent quét kho", type="primary"):
    st.session_state.inventory = edited_df
    
    if st.session_state.inventory.empty:
        st.error("🚨 [Input Error]: Kho hàng rỗng!")
    else:
        st.markdown("### 🧠 Tiến trình tư duy tự chủ của Agent (Autonomy Chain)")
        
        updated_inv = st.session_state.inventory.copy()
        inventory_json = updated_inv.to_json(orient="records", date_format="iso")
        
        target_date_str = demo_target_date.strftime("%Y-%m-%d")

        with st.status("🔍 Agent phân tích kho POS và định tuyến logic...", expanded=True) as status_agent:
            st.write("🛰️ [Observe]: Đọc cấu trúc dữ liệu POS kho hàng...")
            time.sleep(0.3)
            st.write("🤖 [Action]: Truyền tin bối cảnh sang LLM Router và đợi xử lý...")
            
            agent_output, error_code = dynamic_pricing_agent_core(inventory_json, active_milestone["label"], target_date_str)
            
            if error_code is not None:
                if error_code == "SIMULATED_NETWORK_DISCONNECT":
                    st.error("🚨 [Simulated Failure]: Công tắc giả lập sự cố đang BẬT!")
                else:
                    st.error(f"🚨 [System Failure Detected]: Ngoại vi trục trặc ({error_code}).")
                    
                st.warning("🔥 [Fail-Safe Activated]: Kích hoạt xả kho khẩn cấp - Chuyển thẳng hàng cận date sang diện TỪ THIỆN!")
                time.sleep(0.8)
                
                updated_inv = local_fallback_charity_pricing(st.session_state.inventory)
                status_agent.update(label="⚠️ Đã chuyển giao khẩn cấp hàng hóa sang luồng an sinh xã hội!", state="error")
                
                st.markdown("### 📊 Kết quả POS sau xử lý (Chế độ Cứu trợ khẩn cấp)")
                st.dataframe(updated_inv, use_container_width=True)
            else:
                # BỘ LỌC DỮ LIỆU AN TOÀN TUYỆT ĐỐI (SAFE GETTER)
                try:
                    clean_output = agent_output.strip()
                    if clean_output.startswith("```json"):
                        clean_output = clean_output[7:]
                    elif clean_output.startswith("```"):
                        clean_output = clean_output[3:]
                    if clean_output.endswith("```"):
                        clean_output = clean_output[:-3]
                    clean_output = clean_output.strip()
                    
                    data_dict = json.loads(clean_output)
                    
                    items = []
                    if isinstance(data_dict, dict):
                        items = data_dict.get("danh_sach", data_dict.get("products", []))
                    elif isinstance(data_dict, list):
                        items = data_dict
                        
                    for item in items:
                        sp_code = item.get("Mã SP")
                        if not sp_code:
                            continue
                            
                        match_idx = updated_inv[updated_inv["Mã SP"] == sp_code].index
                        if len(match_idx) > 0:
                            t_idx = match_idx[0]
                            
                            # LẤY GIÁ TRỊ AN TOÀN: Nếu LLaMA quên không trả về giá mới thì giữ nguyên giá bán cũ
                            suggested_price = item.get("Giá mới (VND)")
                            if suggested_price is not None:
                                updated_inv.at[t_idx, "Giá bán (VND)"] = int(suggested_price)
                                
                            suggested_status = item.get("Trạng thái")
                            if suggested_status:
                                updated_inv.at[t_idx, "Trạng thái"] = str(suggested_status)
                                
                    status_agent.update(label="🤖 Xử lý luồng định giá thông qua LLM Agent hoàn tất!", state="complete")
                    
                    st.markdown("### 📊 Kết quả sau khi Agent vận hành thực tế")
                    st.dataframe(updated_inv, use_container_width=True)
                    
                except Exception as parse_err:
                    st.warning(f"⚠️ [Data Error]: Cú pháp LLM bị lệch ({parse_err}). Bẻ lái sang xả kho từ thiện...")
                    updated_inv = local_fallback_charity_pricing(st.session_state.inventory)
                    status_agent.update(label="⚠️ Đã chuyển giao hàng hóa sang luồng an sinh xã hội!", state="error")
                    
                    st.markdown("### 📊 Kết quả POS sau xử lý (Chế độ Cứu trợ khẩn cấp)")
                    st.dataframe(updated_inv, use_container_width=True)

st.markdown("---")
st.caption("⚡ Thực hiện bởi Nhóm Infinity - ĐH FPT Quy Nhơn")