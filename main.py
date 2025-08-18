import streamlit as st

# MBTI별 추천 직업 데이터
career_dict = {
    "INTJ": ["전략기획가", "연구원", "데이터 분석가"],
    "ENTP": ["기업가", "마케팅 기획자", "변호사"],
    "INFJ": ["상담가", "작가", "교사"],
    "ESFP": ["연예인", "이벤트 기획자", "영업직"],
    # ... 16가지 MBTI 다 넣기
}

# 웹앱 제목
st.title("🌟 MBTI 기반 진로 추천 사이트")
st.write("MBTI를 선택하면 적합한 직업을 추천해드려요!")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(career_dict.keys()))

# 추천 직업 출력
if mbti:
    st.subheader(f"✅ {mbti} 유형을 위한 추천 직업")
    for job in career_dict[mbti]:
        st.write(f"- {job}")
