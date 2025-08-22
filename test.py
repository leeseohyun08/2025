import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("📚 스터디 플래너 자동화 앱")

# --- 할 일 입력 ---
st.subheader("✏️ 공부할 일 추가")
task = st.text_input("과목 / 주제")
hours = st.number_input("예상 소요 시간 (시간)", min_value=1, max_value=24)
deadline = st.date_input("마감 기한")
priority = st.selectbox("우선순위", ["높음", "보통", "낮음"])

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.button("추가"):
    st.session_state.tasks.append({
        "과목": task,
        "시간": hours,
        "마감": deadline,
        "우선순위": priority,
        "완료": False
    })

# --- 할 일 리스트 ---
st.subheader("📅 내 공부 계획")
df = pd.DataFrame(st.session_state.tasks)
if not df.empty:
    st.dataframe(df)

    # 진행률
    progress = sum(df["완료"]) / len(df)
    st.progress(progress)

    # CSV 다운로드
    st.download_button(
        "📥 CSV 다운로드",
        df.to_csv(index=False).encode("utf-8"),
        "study_plan.csv",
        "text/csv"
    )
else:
    st.info("아직 등록된 할 일이 없습니다.")

