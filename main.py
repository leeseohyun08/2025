# app.py
import streamlit as st
from datetime import datetime
import json
import textwrap

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
    primary = st.color_picker("Primary", "#7C3AED")      
    secondary = st.color_picker("Secondary", "#06B6D4")  
    accent = st.color_picker("Accent", "#F59E0B")        
    dark_bg = st.toggle("어두운 배경", value=True)
    st.markdown("---")
    st.markdown("### ℹ️ 안내")
    st.write("MBTI를 선택하면 유형에 맞는 **추천 직업**과 **핵심 역량**, **추천 활동**을 보여줍니다.")
    st.caption("💡 컬러를 바꾸면 카드/버튼 색감이 즉시 반영돼요!")

# -----------------------------
# Global Styles (CSS)
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
        height: 10vh;
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
# MBTI 데이터
# -----------------------------
MBTI_INTRO = {
    "INTJ": "전략적이고 독립적인 사색가 🧠",
    "INTP": "논리적 탐구자 🔍",
    "ENTJ": "비전 있는 리더 🚀",
    "ENTP": "아이디어 스파크 창업가 💡",
    "INFJ": "통찰력 있는 상담자 🌿",
    "INFP": "가치 중심의 스토리텔러 ✍️",
    "ENFJ": "사람을 이끄는 조력자 🤝",
    "ENFP": "영감 주는 탐험가 🌈",
    "ISTJ": "신뢰받는 관리자 📘",
    "ISFJ": "세심한 돌봄 제공자 🧺",
    "ESTJ": "체계적인 운영가 🧭",
    "ESFJ": "따뜻한 커뮤니티 빌더 🫶",
    "ISTP": "문제 해결 장인 🛠️",
    "ISFP": "감성적인 크리에이터 🎨",
    "ESTP": "액션 중심의 실행가 ⚡",
    "ESFP": "무대 위의 엔터테이너 🎤",
}

# 간단 직업 데이터 예시
CAREERS = {mbti:[{"job":"예시 직업 🏆","why":"이 MBTI에 적합한 직업","skills":["분석","협업"],"learn":["활동1","활동2"]} for _ in range(3)] for mbti in MBTI_INTRO}

SIMILAR = {
    "INTJ":["INTP","ENTJ","INFJ"],
    "INTP":["INTJ","ENTP","INFP"],
    "ENTJ":["INTJ","ESTJ","ENTP"],
    "ENTP":["INTP","ENFP","ENTJ"],
    "INFJ":["INFP","INTJ","ENFJ"],
    "INFP":["INFJ","ENFP","INTP"],
    "ENFJ":["INFJ","ESFJ","ENFP"],
    "ENFP":["INFP","ENTP","ENFJ"],
    "ISTJ":["ESTJ","ISFJ","INTJ"],
    "ISFJ":["ESFJ","ISTJ","INFJ"],
    "ESTJ":["ISTJ","ENTJ","ESFJ"],
    "ESFJ":["ISFJ","ENFJ","ESTJ"],
    "ISTP":["ESTP","INTP","ISFP"],
    "ISFP":["ESFP","INFP","ISTP"],
    "ESTP":["ISTP","ENTP","ESFP"],
    "ESFP":["ISFP","ENFP","ESTP"],
}

EMOJI_TYPE = {"I":"🧠","E":"🌟","N":"✨","S":"🔎","T":"⚙️","F":"💞","J":"🗂️","P":"🌊"}

def mbti_badges(mbti: str) -> str:
    return " ".join([f"<span class='badge'>{c} {EMOJI_TYPE.get(c,'')}</span>" for c in mbti])

def render_job_card(item):
    skills = " ".join([f"<span class='badge'>🔧 {s}</span>" for s in item["skills"]])
    learn = " ".join([f"<span class='badge'>📚 {s}</span>" for s in item["learn"]])
    return f"""
      <div class="job-card">
        <div class="job-title">{item['job']}</div>
        <div>💡 {item['why']}</div>
        <div style="margin-top:10px">{skills}</div>
        <div style="margin-top:6px">{learn}</div>
      </div>
    """

def make_download_payload(user_mbti: str):
    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mbti": user_mbti,
        "intro": MBTI_INTRO.get(user_mbti, ""),
        "careers": CAREERS.get(user_mbti, []),
        "similar_types": SIMILAR.get(user_mbti, [])
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div class="glass">
  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <div style="font-size:2rem;">🌈</div>
    <div>
      <div style="font-weight:800; font-size:2rem;">MBTI 진로 추천</div>
      <div>당신의 성향에 딱 맞는 직업 영감을 찾아보세요 🚀</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Selector — MBTI Grid + Selectbox
# -----------------------------
col1, col2 = st.columns([1,1])

rows = [["INTJ","INTP","ENTJ","ENTP"],["INFJ","INFP","ENFJ","ENFP"],["ISTJ","ISFJ","ESTJ","ESFJ"],["ISTP","ISFP","ESTP","ESFP"]]

if "selected" not in st.session_state:
    st.session_state.selected = "INTJ"

with col1:
    st.markdown("#### 🔤 빠른 선택 (버튼)")
    for row in rows:
        cols = st.columns(4)
        for i, t in enumerate(row):
            with cols[i]:
                if st.button(t, use_container_width=True):
                    st.session_state.selected = t

with col2:
    st.markdown("#### 📋 드롭다운 선택")
    picked = st.selectbox("MBTI를 선택하세요:", list(MBTI_INTRO.keys()), index=list(MBTI_INTRO.keys()).index(st.session_state.selected))
    st.session_state.selected = picked

user_mbti = st.session_state.selected

# -----------------------------
# Summary Panel
# -----------------------------
st.markdown(f"""
<div class="glass">
  <div style="display:flex; align-items:flex-start; gap:18px; flex-wrap:wrap;">
    <div style="font-size:2rem;">🎯</div>
    <div style="flex:1">
      <div style="font-weight:700; font-size:1.5rem;">{user_mbti} — {MBTI_INTRO.get(user_mbti,"")}</div>
      <div style="margin-top:6px;">{mbti_badges(user_mbti)}</div>
      <div style="margin-top:10px;">
        <span class='badge'>✨ 추천 직업 3선</span>
        <span class='badge'>🧭 맞춤 역량 & 활동</span>
        <span class='badge'>🔁 비슷한 유형 제안</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Career Cards
# -----------------------------
left, right = st.columns([1.2, 1])
with left:
    st.markdown("### 🧩 추천 직업 카드")
    careers = CAREERS.get(user_mbti, [])
    for c in careers:
        st.markdown(render_job_card(c), unsafe_allow_html=True)

    with st.expander("📘 유형 요약 & 추천 활동", expanded=True):
        st.markdown(textwrap.dedent(f"""
        **{user_mbti} 핵심 성향**
        - {MBTI_INTRO.get(user_mbti, '')}
        - 강점: 집중력, 몰입, 전략적 사고
        - 주의: 완벽주의 경향 → 작게 시작/짧게 반복 권장

        **추천 루틴**
        - 🎯 월간: 목표 1~2개 설정
        - 🔁 주간: 가설 → 실행 → 회고
        - 🧰 도구: 캘린더, 메모, 실험 기록
        """))

with right:
    st.markdown("### 🔗 빠른 리소스")
    st.markdown("""
    - 🇰🇷 워크넷: 직업정보/직무역량
    - 🌐 Coursera/edX: 온라인 전문과정
    - 🧪 Kaggle: 데이터 실전
    """)

    st.markdown("### 🧑‍🤝‍🧑 비슷한 유형")
    sim = SIMILAR.get(user_mbti, [])
    if sim:
        st.markdown(" ".join([f"<span class='badge'>{s}</span>" for s in sim]), unsafe_allow_html=True)

    st.markdown("### 💾 결과 저장")
    payload = make_download_payload(user_mbti)
    st.download_button(
        label="📥 JSON으로 저장",
        file_name=f"mbti_{user_mbti}_careers.json",
        mime="application/json",
        data=payload,
        use_container_width=True
    )

    st.markdown("### 🙌 피드백")
    c1, c2 = st.columns(2)
    if "feedback" not in st.session_state:
        st.session_state.feedback = {"up":0, "down":0}
    if c1.button("👍 유용했어요", use_container_width=True):
        st.session_state.feedback["up"] += 1
    if c2.button("👎 별로에요", use_container_width=True):
        st.session_state.feedback["down"] += 1
    st.caption(f"현재 피드백 — 👍 {st.session_state.feedback['up']} | 👎 {st.session_state.feedback['down']}")

# -----------------------------
# Footer
# -----------------------------
st.markdown(f"""
<div class="glass">
  <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
    <div style="font-size:2rem;">💡</div>
    <div>참고: MBTI는 경향을 보여줄 뿐, 직업 적합성을 결정하지 않아요. 실제 선택은 흥미/능력/환경을 종합하세요.</div>
  </div>
</div>
""", unsafe_allow_html=True)
