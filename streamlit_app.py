import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 1. Cấu hình trang (Page Configuration)
st.set_page_config(page_title="Calculator", layout="wide")

# 2. Tiêu đề (Header)
st.header("steel-pipe-calculator TEST")
st.caption("Complementary thesis GUI for FE database interrogation, RWS geometry screening, backbone response, and column-face demand.")
st.markdown("---")

# 3. Phân chia bố cục thành 3 cột chính
col1, col2, col3 = st.columns([1, 1.5, 1])

# ================= CỘT 1: INPUTS =================
with col1:
    st.subheader("INPUTS")
    
    # Thanh trượt cài đặt thông số
    profile = st.select_slider("Profile (IPE)", options=["IPE270", "IPE300", "IPE400", "IPE500", "IPE600"])
    steel_grade = st.select_slider("Steel grade", options=["S235", "S275", "S355"])
    span_ratio = st.slider("Span-to-depth ratio", min_value=6, max_value=14, value=6)
    web_opening = st.slider("Web opening, do/h (%)", min_value=0, max_value=75, value=30)
    opening_spacing = st.slider("Opening spacing, S/h (%)", min_value=0, max_value=240, value=60)
    
    # Thông tin mô hình
    st.markdown("**Model:** `<span style='float:right'>6.270.S235.C00</span>`", unsafe_allow_html=True)
    st.caption("Section geometry (from dataset): h=270.0 mm, b=135.0 mm, tw=6.6 mm, tf=10.2 mm")
    st.caption("Steel grade detail (from dataset): Fy=301.0 MPa")
    
    st.markdown("---")
    st.subheader("CASE GUIDE AND SPECIMEN CLASSIFICATION")
    st.caption("Table 1.5 Parametric combinations of (S/h) and (do/h) in each batch of analysis")
    
    # Tạo bảng ma trận phân loại (Table)
    df_matrix = pd.DataFrame(
        [["C00", "C10", "C28", "C30", "C48", "C50"],
         ["C01", "C11", "C21", "C31", "C41", "C51"],
         ["C02", "C12", "C22", "C32", "C42", "C52"],
         ["C03", "C13", "C23", "C33", "C43", "C53"]],
        columns=["30", "35", "40", "45", "50", "55"],
        index=["60", "80", "100", "120"]
    )
    st.dataframe(df_matrix, use_container_width=True)
    st.caption("C00 to C99 are reduced web section opening cases as shown in Table 1.5. C100 is the full section (no opening).")

# ================= CỘT 2: BACKBONE CURVE =================
with col2:
    st.subheader("Backbone curve")
    
    # Hàng nút bấm chức năng
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)
    btn_col1.button("Plot (replace)", type="primary")
    btn_col2.button("Add curve")
    btn_col3.button("Clear")
    btn_col4.button("Key points: off")
    btn_col5.button("Export SVG")
    
    # Dữ liệu giả lập cho biểu đồ đường cong
    x = np.linspace(-0.06, 0.06, 100)
    y = 150 * np.tanh(100 * x) 
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='6.270.S235.C00', line=dict(color='#4c78a8', width=2)))
    
    # Cấu hình giao diện biểu đồ Plotly
    fig.update_layout(
        xaxis_title="Rotation (rad)",
        yaxis_title="Moment (kN·m)",
        margin=dict(l=0, r=0, t=20, b=0),
        height=450,
        plot_bgcolor='white',
        xaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='lightgrey', gridcolor='#f0f0f0'),
        yaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='lightgrey', gridcolor='#f0f0f0'),
        legend=dict(yanchor="top", y=-0.1, xanchor="left", x=0, orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= CỘT 3: OUTPUTS =================
with col3:
    st.subheader("OUTPUTS")
    
    # Từ điển chứa các kết quả đầu ra
    outputs = {
        "My (kN m)": "148.7",
        "Mc (kN m)": "156.3",
        "M0.04 (kN m)": "156.3",
        "M0.06 (kN m)": "138.6",
        "Mp (kN m)": "113.7",
        "Mp,rws (kN m)": "111.2",
        "θy (rad)": "0.00720",
        "θc (rad)": "0.04000",
        "von Mises at column face (normalised)": "0.91",
        "PEEQ at column face (normalised)": "0.44",
    }
    
    # In dữ liệu: Tên căn trái, số liệu in đậm căn phải
    for key, value in outputs.items():
        st.markdown(f"<div style='display: flex; justify-content: space-between;'><span>{key}</span><span><b>{value}</b></span></div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.3em 0px; border-top: 1px solid #f0f0f0;' />", unsafe_allow_html=True)
        
    # Làm nổi bật thông số cảnh báo (màu đỏ)
    st.markdown("<div style='display: flex; justify-content: space-between;'><span>Stress@CF/Fy (normalised)</span><span style='color:#d62728;'><b>1.23</b></span></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.3em 0px; border-top: 1px solid #f0f0f0;' />", unsafe_allow_html=True)
    
    st.markdown("<div style='display: flex; justify-content: space-between;'><span>M/Mp,rws</span><span><b>1.406</b></span></div>", unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Tiêu chuẩn AISC 341
    st.subheader("AISC 341 Prequalification criteria")
    st.markdown("<div style='display: flex; justify-content: space-between;'><span>Check vs 0.8Mp</span><span style='color:#2ca02c; border: 1px solid #2ca02c; padding: 0px 5px; border-radius: 3px;'><b>OK</b></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 0.5em;'>Check vs 0.8Mp,rws</div>", unsafe_allow_html=True)
    st.caption("Margins: M0.04/(0.8Mp) = 1.718, M0.04/(0.8Mp,rws) = 1.757.")
    st.caption("M0.04 ≥ 0.8Mp and M0.04 ≥ 0.8Mp,rws")

# ================= HÀNG DƯỚI CÙNG: CONTOUR PLOTS =================
st.markdown("---")
st.subheader("CONTOUR PLOTS")

plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    st.markdown("<div style='display: flex; justify-content: space-between; align-items: center;'><b>von Mises</b> <button style='border: 1px solid #ccc; background: white; border-radius: 5px; padding: 2px 10px;'>Open</button></div>", unsafe_allow_html=True)
    # Gợi ý chèn ảnh thực tế
    st.info("Chèn đường dẫn file ảnh của bạn vào đây bằng lệnh: st.image('duong_dan_anh_von_mises.jpg')")

with plot_col2:
    st.markdown("<div style='display: flex; justify-content: space-between; align-items: center;'><b>PEEQ</b> <button style='border: 1px solid #ccc; background: white; border-radius: 5px; padding: 2px 10px;'>Open</button></div>", unsafe_allow_html=True)
    # Gợi ý chèn ảnh thực tế
    st.info("Chèn đường dẫn file ảnh của bạn vào đây bằng lệnh: st.image('duong_dan_anh_peeq.jpg')")
