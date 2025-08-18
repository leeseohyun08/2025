# app.py
# -----------------------------------------------
# 🌟 MBTI 기반 진로 추천 웹앱 (화려한 이모지 & 커스텀 테마 포함)
# 실행: streamlit run app.py
# -----------------------------------------------
import streamlit as st
from datetime import datetime
import textwrap
import json

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
        min-height: 100vh;
      }}
      .glass {{
        background: var(--panel);
        backdrop-filter: blur(10px);
        border: 1px solid {primary}33;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px #00000022;
      }}
      .headline {{
        font-weight: 800;
        font-size: 2.1rem;
        line-height: 1.1;
        color: var(--text);
      }}
      .subline {{
        font-size: 0.98rem;
        color: {("#A6ADBB" if dark_bg else "#4B5563")};
      }}
      .pill {{
        display:inline-block;
        padding: 6px 12px;
        margin: 2px;
        border-radius: 999px;
        border: 1px solid {secondary}55;
        background: {secondary}1A;
        color: var(--text);
        font-size: 0.85rem;
      }}
      .job-card {{
        border: 1px solid var(--border);
        background: var(--card);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
      }}
      .job-title {{
        font-weight: 700; font-size: 1.05rem; color: var(--text);
      }}
      .badge {{
        display:inline-flex; align-items:center; gap:6px;
        border: 1px dashed {accent}88; padding: 4px 10px; border-radius: 10px;
        background: {accent}1A; font-size: 0.82rem; color: var(--text);
      }}
      .muted {{
        color: {("#9AA0AA" if dark_bg else "#6B7280")}; font-size: 0.88rem;
      }}
      .emoji-huge {{
        font-size: 2rem; line-height: 1;
      }}
      /* Streamlit native tweaks */
      header, .stDeployButton {{ visibility: hidden; height: 0; }}
      .block-container {{ padding-top: 1rem; }}
    </style>
    <div class="app-root"></div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Data — MBTI Career DB (16유형)
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

CAREERS = {
    "INTJ":[
        {"job":"데이터 사이언티스트 📈","why":"복잡한 문제를 구조화해 전략을 세우는 데 강점.","skills":["분석적 사고","Python","통계"],"learn":["Kaggle 프로젝트","논문 리딩"]},
        {"job":"전략기획가 🧭","why":"장기 비전 수립과 효율 극대화에 적합.","skills":["시장분석","재무"],"learn":["산업 리포트 작성","케이스 스터디"]}
    ],
    "INFP":[
        {"job":"작가/에디터 ✍️","why":"가치 중심 메시지 제작.","skills":["글쓰기","인터뷰"],"learn":["연재 프로젝트","출판 기획"]},
        {"job":"UX 라이터 ✒️","why":"사용자 공감 기반 카피 제작.","skills":["톤앤매너","마이크로카피"],"learn":["카피 테스트","인터뷰"]}
    ],
    # 나머지 MBTI도 필요하면 위 형식으로 추가...
}

SIMILAR = {
    "INTJ":["INTP","ENTJ","INFJ"],
    "INFP":["INFJ","ENFP","INTP"],
    # 나머지 MBTI도 위 형식으로 추가...
}

EMOJI_TYPE = {
    "I":"🧠", "E":"🌟", "N":"✨", "S":"🔎", "T":"⚙️", "F":"💞", "J":"🗂️", "P":"🌊"
}

# -----------------------------
# Helpers
# -----------------------------
def mbti_badges(mbti: str) -> str:
    return " ".join([f"<span class='pill'>{c} {EMOJI_TYPE.get(c,'')}</span>" for c in mbti])

def render_job_card(item):
    skills = " ".join([f"<span class='pill'>🔧 {s}</span>" for s in item["skills"]])
    learn = " ".join([f"<span class='pill'>📚 {s}</span>" for s in item["learn"]])
    return f"""
      <div class="job-card">
        <div class="job-title">{item['job']}</div>
        <div class="muted">💡 {item['why']}</div>
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
st.markdown(
    f"""
    <div class="glass" style="padding:12px;">
      <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <div class="emoji-huge">🌈</div>
        <div>
          <div class="headline">MBTI 진로 추천</div>
          <div class="subline">당신의 성향에 딱 맞는 직업 영감을 찾아보세요 — 선택하고, 읽고, 바로 실행! 🚀</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Selector — MBTI Grid + Selectbox
# -----------------------------
col1, col2 = st.columns([1,1])
with col1:
    st.markdown("#### 🔤 빠른 선택 (버튼)")
    rows = [
        ["INTJ","INTP","ENTJ","ENTP"],
        ["INFJ","INFP","ENFJ","ENFP"],
        ["ISTJ","ISFJ","ESTJ","ESFJ"],
        ["ISTP","ISFP","ESTP","ESFP"],
    ]
    if "selected" not in st.session_state:
        st.session_state.selected = "INTJ"
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
st.markdown(
    f"""
    <div class="glass" style="margin-top: 10px;">
      <div style="display:flex; align-items:flex-start; gap:18px; flex-wrap:wrap;">
        <div class="emoji-huge">🎯</div>
        <div style="flex:1">
          <div class="headline" style="font-size:1.5rem;">{user_mbti} — {MBTI_INTRO.get(user_mbti,"")}</div>
          <div class="subline" style="margin-top:6px;">{mbti_badges(user_mbti)}</div>
          <div style="margin-top:10px;">
            <span class="badge">✨ 추천 직업</span>
            <span class="badge">🧭 맞춤 역량 & 활동</span>
            <span class="badge">🔁 비슷한 유형</span>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Career Cards
# -----------------------------
left, right = st.columns([1.2, 1])
with left:
    st.markdown("### 🧩 추천 직업 카드")
    careers = CAREERS.get(user_mbti, [])
    if not careers:
        st.info("해당 MBTI에 대한 데이터가 아직 없어요. 다른 유형을 선택해보세요!")
    else:
        for c in careers:
            st.markdown(render_job_card(c), unsafe_allow_html=True)

with right:
    st.markdown("### 🧑‍🤝‍🧑 비슷한 유형")
    sim = SIMILAR.get(user_mbti, [])
    if sim:
        st.markdown(" ".join([f"<span class='pill'>{s}</span>" for s in sim]), unsafe_allow_html=True)

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
st.markdown(
    f"""
    <div class="glass" style="margin-top:10px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div class="emoji-huge">💡</div>
        <div class="subline">참고: MBTI는 **경향**을 보여줄 뿐, 직업 적합성을 결정하지 않아요. 실제 선택은 흥미/능력/환경을 종합해요.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
