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
# Dynamic Styles
# -----------------------------
bg_gradient = (
    f"linear-gradient(135deg, {primary}22 0%, {secondary}22 50%, {accent}22 100%)"
    if dark_bg else
    "linear-gradient(135deg, #ffffff 0%, #fafafa 50%, #ffffff 100%)"
)
text_color = "#EAEAEA" if dark_bg else "#111827"
panel_bg = "#0B0F19CC" if dark_bg else "#ffffff"
card_bg = "#0F172ACC" if dark_bg else "#ffffff"
border_color = primary

# ✅ 배경 높이 줄임
st.markdown(
    f"""
    <style>
      :root {{
        --primary: {primary};
        --secondary: {secondary};
        --accent: {accent};
        --text: {text_color};
        --panel: {panel_bg};
        --card: {card_bg};
        --border: {border_color};
      }}
      .app-root {{
        background: {bg_gradient};
        height: 10vh; /* ✅ 배경 줄임 */
      }}
      .glass {{
        background: var(--panel);
        backdrop-filter: blur(10px);
        border: 1px solid {primary}33;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px #00000022;
        margin-bottom: 20px;
        color: var(--text);
      }}
      .job-card {{
        border: 2px solid var(--border);
        background: var(--card);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        color: var(--text);
        font-size: 1.05rem;
      }}
      .job-title {{
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 6px;
      }}
      .badge {{
        display:inline-block;
        border: 1px solid {secondary}88;
        background: {secondary}1A;
        color: var(--text);
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        margin-right: 6px;
      }}
    </style>
    <div class="app-root"></div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# MBTI 직업 데이터 (예시)
# -----------------------------
career_dict = {
    "INTJ": [
        {
            "job": "데이터 사이언티스트 📊",
            "desc": "복잡한 데이터를 분석해 전략적 의사결정을 돕는 역할",
            "skills": ["통계 분석", "프로그래밍(Python, R)", "논리적 사고"],
            "activities": ["머신러닝 프로젝트 참여", "데이터 해커톤"]
        },
        {
            "job": "전략기획가 🧭",
            "desc": "기업의 장기적 비전과 전략을 수립",
            "skills": ["분석력", "문제 해결", "기획력"],
            "activities": ["시장 조사", "비즈니스 케이스 작성"]
        }
    ],
    "ENFP": [
        {
            "job": "크리에이티브 디렉터 🎨",
            "desc": "광고, 디자인, 브랜딩 프로젝트를 총괄하며 창의성 발휘",
            "skills": ["스토리텔링", "브랜드 전략", "리더십"],
            "activities": ["콘텐츠 제작", "팀 크리에이티브 워크숍"]
        },
        {
            "job": "프로덕트 마케터 🧲",
            "desc": "제품의 매력을 고객에게 전달하는 전략가",
            "skills": ["마케팅 분석", "소통 능력", "창의적 기획"],
            "activities": ["SNS 캠페인 운영", "사용자 인터뷰"]
        }
    ],
}

# -----------------------------
# UI
# -----------------------------
st.markdown(
    "<div class='glass'><h1>🌟 MBTI 기반 진로 추천</h1>"
    "<p>버튼을 눌러 MBTI를 선택하세요!</p></div>",
    unsafe_allow_html=True
)

# 👉 MBTI 버튼 배열 (4x4)
mbti_types = list(career_dict.keys())
selected_mbti = None
cols = st.columns(4)

for i, t in enumerate(mbti_types):
    if cols[i % 4].button(t):
        selected_mbti = t

if selected_mbti:
    st.markdown(
        f"<div class='glass'><h2>✅ {selected_mbti} 추천 직업</h2></div>",
        unsafe_allow_html=True
    )
    for job_info in career_dict[selected_mbti]:
        st.markdown(
            f"""
            <div class='job-card'>
              <div class='job-title'>💼 {job_info['job']}</div>
              <p>{job_info['desc']}</p>
              <p><b>필요 역량:</b> {" ".join([f"<span class='badge'>{s}</span>" for s in job_info['skills']])}</p>
              <p><b>추천 활동:</b> {" ".join([f"<span class='badge'>{a}</span>" for a in job_info['activities']])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='glass'>💡 참고: MBTI는 성향을 보여주는 지표일 뿐, 직업 적합성을 결정하지는 않아요.</div>",
        unsafe_allow_html=True
    )
