# app.py
import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천 🌈",
    page_icon="🌈",
    layout="wide"
)

# -----------------------------
# Sidebar Theme
# -----------------------------
with st.sidebar:
    st.markdown("## 🎨 테마 커스터마이즈")
    primary = st.color_picker("Primary", "#7C3AED")
    secondary = st.color_picker("Secondary", "#06B6D4")
    accent = st.color_picker("Accent", "#F59E0B")
    dark_bg = st.toggle("어두운 배경", value=True)

# -----------------------------
# Dynamic Styles (배경만 수정)
# -----------------------------
if dark_bg:
    bg_css = f"""
    background: linear-gradient(-45deg, {primary}, {secondary}, {accent}, #000000);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    """
else:
    bg_css = f"""
    background: linear-gradient(-45deg, {primary}33, {secondary}33, {accent}33, #ffffff);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    """

st.markdown(
    f"""
    <style>
      body {{
        {bg_css}
      }}
      @keyframes gradientMove {{
        0% {{background-position: 0% 50%;}}
        50% {{background-position: 100% 50%;}}
        100% {{background-position: 0% 50%;}}
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# (나머지 UI / MBTI 추천 로직은 그대로)
# -----------------------------
st.markdown("<h1 style='color:white;'>🌟 MBTI 기반 진로 추천</h1>", unsafe_allow_html=True)
