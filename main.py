# app.py
# 실행: streamlit run app.py
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="MBTI 진로 추천 🌈",
    page_icon="🌈",
    layout="wide"
)

# -----------------------------
# Sidebar — Theme & Intro
# -----------------------------
with st.sidebar:
    st.markdown("## 🎨 테마 커스터마이즈")
    primary = st.color_picker("Primary", "#7C3AED")      # 보라
    secondary = st.color_picker("Secondary", "#06B6D4")  # 청록
    accent = st.color_picker("Accent", "#F59E0B")        # 주황
    dark_bg = st.toggle("어두운 배경", value=True)
    st.markdown("---")
    st.markdown("### ℹ️ 안내")
    st.write("컬러를 바꾸면 배경/카드/포인트 색감이 즉시 바뀝니다!")

# -----------------------------
# Dynamic Styles
# -----------------------------
bg_gradient = (
    f"linear-gradient(135deg, {primary}22 0%, {secondary}22 50%, {accent}22 100%)"
    if dark_bg else
    f"linear-gradient(135deg, #ffffff 0%, #fafafa 50%, #ffffff 100%)"
)

text_color = "#EAEAEA" if dark_bg else "#111827"
panel_bg = "#0B0F19CC" if dark_bg else "#ffffff"
card_bg = "#0F172ACC" if dark_bg else "#ffffff"
border_color = primary

st.markdown(
    f"""
    <style>
      body {{
        background: {bg_gradient};
      }}
      .glass {{
        background: {panel_bg};
        backdrop-filter: blur(10px);
        border: 1px solid {primary}55;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        color: {text_color};
      }}
      .job-card {{
        border: 2px solid {border_color};
        background: {card_bg};
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        color: {text_color};
        font-size: 1.1rem;
      }}
      .pill {{
        display:inline-block;
        padding: 6px 12px;
        margin: 2px;
        border-radius: 999px;
        border: 1px solid {secondary}55;
        background: {secondary}1A;
        color: {text_color};
        font-size: 0.85rem;
      }}
      .badge {{
        display:inline-block;
        border: 1px dashed {accent}88;
        background: {accent}1A;
        color: {text_color};
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 0.85rem;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# MBTI 데이터 (16유형 전부)
# -----------------------------
career_dict = {
    "INTJ": ["데이터 사이언티스트 📊", "전략기획가 🧭", "리서처 🔬"],
    "INTP": ["연구원 🧪", "백엔드 개발자 💻", "데브옵스 엔지니어 ⚙️"],
    "ENTJ": ["프로덕트 매니저 🧑‍✈️", "전략 컨설턴트 🧠", "사업 개발자 🤝"],
    "ENTP": ["스타트업 창업가 🚀", "마케팅 전략가 📣", "변호사 ⚖️"],
    "INFJ": ["상담사 🧑‍⚕️", "작가 ✍️", "교육 기획자 🎓"],
    "INFP": ["작가/에디터 ✒️", "NGO 활동가 🌍", "UX 라이터 ✍️"],
    "ENFJ": ["교육자 🎤", "커뮤니티 매니저 👥", "HR 전문가 👔"],
    "ENFP": ["크리에이티브 디렉터 🎨", "프로덕트 마케터 🧲", "프리랜서 🌈"],
    "ISTJ": ["회계사 📊", "프로젝트 매니저 📅", "품질 관리 전문가 ✅"],
    "ISFJ": ["간호사 🏥", "행정 직원 🗂️", "초중등 교사 🍎"],
    "ESTJ": ["운영 매니저 🏢", "영업 리더 💼", "공공 행정가 🏛️"],
    "ESFJ": ["채용 담당자 👔", "서비스 기획자 💬", "이벤트 플래너 🎉"],
    "ISTP": ["보안 엔지니어 🔐", "필드 엔지니어 🔧", "하드웨어 엔지니어 🔩"],
    "ISFP": ["디자이너 🎨", "사진작가 📷", "공예가 🧵"],
    "ESTP": ["세일즈 전문가 ⚡", "프로듀서 🎬", "트레이더 💱"],
    "ESFP": ["연예인 🎤", "이벤트 기획자 🎈", "브랜드 스페셜리스트 🛍️"],
}

# -----------------------------
# UI
# -----------------------------
st.markdown(
    "<div class='glass'><h1>🌟 MBTI 기반 진로 추천</h1>"
    "<p>MBTI를 선택하면 적합한 직업을 추천해드려요!</p></div>",
    unsafe_allow_html=True
)

mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(career_dict.keys()))

if mbti:
    st.markdown(
        f"<div class='glass'><h2>✅ {mbti} 추천 직업</h2></div>",
        unsafe_allow_html=True
    )
    for job in career_dict[mbti]:
        st.markdown(f"<div class='job-card'>💼 {job}</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='glass'>"
        "💡 참고: MBTI는 성향을 보여주는 지표일 뿐, 직업 적합성을 결정하지는 않아요."
        "</div>",
        unsafe_allow_html=True
    )
