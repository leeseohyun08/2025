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
# Data — MBTI Career DB (간단 예시 16유형 * 3직업)
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
    "INTJ": [
        {"job":"데이터 사이언티스트 📈","why":"복잡한 문제를 구조화해 전략을 세우는 데 강점.","skills":["분석적 사고","Python/R","통계","머신러닝"],"learn":["Kaggle 대회","논문 리딩","A/B 테스트 실습"]},
        {"job":"전략기획가 🧭","why":"장기 비전 수립과 효율 극대화에 적합.","skills":["문제정의","재무/시장분석","OKR"],"learn":["케이스 스터디","산업 리포트 요약"]},
        {"job":"리서처(UX/산업) 🔬","why":"가설-검증 루프를 즐김.","skills":["리서치 설계","정성/정량 분석"],"learn":["인터뷰 기법","서베이 설계"]}
    ],
    "INTP": [
        {"job":"백엔드 개발자 🧩","why":"시스템 설계와 최적화에 매력.","skills":["알고리즘","DB/캐시","분산처리"],"learn":["오픈소스 기여","성능 튜닝"]},
        {"job":"연구원(컴공/수학) 🧮","why":"개념 탐구와 이론화에 강점.","skills":["수리적 모델링","논증"],"learn":["arXiv 리딩","세미나 발표"]},
        {"job":"데브옵스/플랫폼 엔지니어 🏗️","why":"도구화/자동화 애정.","skills":["CI/CD","Infra as Code"],"learn":["쿠버네티스 실습","GitHub Actions"]}
    ],
    "ENTJ": [
        {"job":"프로덕트 매니저 🧑‍✈️","why":"목표 설정→실행→성과관리에 탁월.","skills":["우선순위화","조직조율","데이터 리딩"],"learn":["PRD 작성","KPI 설계"]},
        {"job":"전략컨설턴트 🧠","why":"복잡 문제를 빠르게 구조화.","skills":["피라미드 사고","시장모형"],"learn":["케이스 인터뷰","MECE 연습"]},
        {"job":"사업개발(BD) 🤝","why":"네트워킹과 협상력 강점.","skills":["협상","계약","파트너십"],"learn":["딜 파이프라인 관리"]}
    ],
    "ENTP": [
        {"job":"스타트업 창업가 🚀","why":"실험과 피보팅 즐김.","skills":["가설검증","그로스","피치"],"learn":["린캔버스","MVP 빌드"]},
        {"job":"마케팅 전략가 📣","why":"창의 아이디어+데이터 밸런스.","skills":["퍼널","크리에이티브","리텐션"],"learn":["광고 실험","퍼포먼스 분석"]},
        {"job":"변호사/정책기획 ⚖️","why":"논쟁/설득 능력 우수.","skills":["논증","리서치","글쓰기"],"learn":["모의 재판","정책 제안서"]}
    ],
    "INFJ": [
        {"job":"상담사/코치 🧑‍⚕️","why":"공감과 통찰의 조합.","skills":["경청","질문","윤리"],"learn":["상담이론","수퍼비전"]},
        {"job":"콘텐츠 전략가 🧭","why":"메시지와 의미 설계.","skills":["내러티브","브랜드"],"learn":["스토리텔링 워크숍"]},
        {"job":"교육기획자 🎓","why":"학습 경험 설계에 적합.","skills":["커리큘럼","러닝디자인"],"learn":["MOOC 기획"]}
    ],
    "INFP": [
        {"job":"작가/에디터 ✍️","why":"가치 중심 메시지 제작.","skills":["글쓰기","인터뷰"],"learn":["연재 프로젝트","출판 기획"]},
        {"job":"UX 라이터 ✒️","why":"사용자 공감 기반 카피.","skills":["톤앤매너","마이크로카피"],"learn":["카피 테스팅"]},
        {"job":"사회혁신/NGO 🌍","why":"가치 실현 지향.","skills":["캠페인","리서치"],"learn":["임팩트 측정"]}
    ],
    "ENFJ": [
        {"job":"HR/조직문화 🧑‍💼","why":"사람과 변화관리 강점.","skills":["코칭","퍼실리테이션"],"learn":["워크숍 디자인"]},
        {"job":"교육/강의 🎤","why":"동기부여와 안내.","skills":["커뮤니케이션","콘텐츠"],"learn":["티칭 실습"]},
        {"job":"커뮤니티 매니저 👥","why":"관계 구축 탁월.","skills":["행사기획","운영"],"learn":["온/오프라인 운영"]}
    ],
    "ENFP": [
        {"job":"크리에이티브 디렉터 🎨","why":"아이디어 폭발+연결.","skills":["컨셉팅","캠페인"],"learn":["포트폴리오 제작"]},
        {"job":"프로덕트 마케터 🧲","why":"사용자 공감 기반 메시지.","skills":["세그먼트","포지셔닝"],"learn":["인터뷰/서베이"]},
        {"job":"창업/프리랜서 🧑‍🎤","why":"자유/탐험 선호.","skills":["셀프브랜딩","세일즈"],"learn":["랜딩페이지 제작"]}
    ],
    "ISTJ": [
        {"job":"재무/회계 📊","why":"정확/규정 준수 강점.","skills":["분개/결산","분석"],"learn":["자격증 학습"]},
        {"job":"프로젝트 매니저 🗂️","why":"계획/리스크 관리.","skills":["스케줄링","리스크"],"learn":["거버넌스 수립"]},
        {"job":"품질관리(QA) ✅","why":"체크리스트/표준화.","skills":["테스트","문서화"],"learn":["테스트케이스 작성"]}
    ],
    "ISFJ": [
        {"job":"간호/의료보조 🏥","why":"세심/헌신적 케어.","skills":["기록","커뮤니케이션"],"learn":["임상 지식"]},
        {"job":"행정/운영 🗃️","why":"지원/안정 추구.","skills":["문서/정리","고객응대"],"learn":["업무자동화"]},
        {"job":"초중등 교사 🍎","why":"돌봄과 교육 균형.","skills":["수업설계","평가"],"learn":["수업 시연"]}
    ],
    "ESTJ": [
        {"job":"운영/총괄 COO 🏢","why":"규모화/프로세스화.","skills":["KPI","표준화"],"learn":["프로세스 맵"]},
        {"job":"영업 리더 💼","why":"목표관리/관리.","skills":["영업전략","코칭"],"learn":["파이프라인 관리"]},
        {"job":"공공행정/관리 🏛️","why":"규정/정책 집행.","skills":["규정해석","감사"],"learn":["정책 리서치"]}
    ],
    "ESFJ": [
        {"job":"HRBP/채용 👔","why":"관계/조율 우수.","skills":["인터뷰","온보딩"],"learn":["채용 브랜딩"]},
        {"job":"서비스 기획/CS 💬","why":"고객만족 지향.","skills":["VOC","프로세스"],"learn":["CS 매뉴얼"]},
        {"job":"행사/이벤트 기획 🎉","why":"디테일/케어.","skills":["스케줄","예산"],"learn":["스크립트 작성"]}
    ],
    "ISTP": [
        {"job":"하드웨어 엔지니어 🔩","why":"손으로 해결/최적화.","skills":["회로","CAD"],"learn":["프로토타입 제작"]},
        {"job":"보안/리버싱 🕵️","why":"해킹/퍼즐 선호.","skills":["리버스","침투"],"learn":["CTF 참가"]},
        {"job":"필드 엔지니어 🧰","why":"현장 트러블슈팅.","skills":["진단","수리"],"learn":["케이스 라이브러리"]}
    ],
    "ISFP": [
        {"job":"디자이너(UX/UI) 🖌️","why":"감각/사용자 공감.","skills":["리서치","프로토타입"],"learn":["피그마 포트폴리오"]},
        {"job":"사진/영상 크리에이터 📷","why":"감성표현 탁월.","skills":["촬영","편집"],"learn":["시네마틱 연습"]},
        {"job":"공예/제품디자인 🧵","why":"손끝 디테일.","skills":["재료","제작"],"learn":["전시 참여"]}
    ],
    "ESTP": [
        {"job":"세일즈/BD ⚡","why":"현장감/스피드.","skills":["니즈파악","협상"],"learn":["콜드콜 스크립트"]},
        {"job":"프로듀서/PD 🎬","why":"즉각 실행/조율.","skills":["섭외","타임라인"],"learn":["파일럿 제작"]},
        {"job":"트레이딩/브로커 💱","why":"민첩한 판단.","skills":["리스크","데이터"],"learn":["백테스트"]}
    ],
    "ESFP": [
        {"job":"연예/퍼포머 🎤","why":"표현/관객 교감.","skills":["보컬/댄스","무대"],"learn":["무대 연습"]},
        {"job":"이벤트/프로모션 🎈","why":"현장 에너지.","skills":["프로모","MC"],"learn":["행사 운영"]},
        {"job":"리테일/브랜드 스페셜리스트 🛍️","why":"고객경험.","skills":["VMD","스토리"],"learn":["매장 개선"]}
    ],
}

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
    <div class="glass">
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
st.write("")

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
                label = f"{t}"
                if st.button(f"{label}", use_container_width=True):
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
            <span class="badge">✨ 추천 직업 3선</span>
            <span class="badge">🧭 맞춤 역량 & 활동</span>
            <span class="badge">🔁 비슷한 유형 제안</span>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

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

    with st.expander("📘 유형 요약 & 추천 활동", expanded=True):
        st.markdown(
            textwrap.dedent(f"""
            **{user_mbti} 핵심 성향**
            - {MBTI_INTRO.get(user_mbti, '')}
            - 강점: 집중력, 고도 사고력, 몰입(개인차)
            - 주의: 과도한 완벽주의/아이디어 과잉 → **작게 시작/짧게 반복** 권장

            **추천 루틴**
            - 🎯 월간: 목표 1~2개, 측정 가능한 지표(KPI) 설정
            - 🔁 주간: 가설 설정 → 실험 → 회고(15분)
            - 🧰 도구: 캘린더 블록, 이슈 트래커, 메모/리서치 아카이브
            """)
        )
with right:
    st.markdown("### 🔗 빠른 리소스")
    st.markdown(
        """
        - 🇰🇷 **워크넷**: 직업정보/직무역량
        - 🇰🇷 **잡코리아/사람인**: 채용공고/직무요건
        - 🌐 **Coursera/edX**: 온라인 전문과정
        - 🧪 **Kaggle**: 데이터 실전
        """
    )
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
st.write("")
st.markdown(
    f"""
    <div class="glass">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div class="emoji-huge">💡</div>
        <div class="subline">참고: MBTI는 **경향**을 보여줄 뿐, 직업 적합성을 결정하지 않아요. 실제 선택은 흥미/능력/환경을 종합해요.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
