import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📚 스터디 플래너")

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- 입력 영역 ---
with st.container():
    st.subheader("✏️ 공부할 일 추가")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        task = st.text_input("과목 / 주제")
    with col2:
        hours = st.number_input("시간(h)", min_value=1, max_value=24, step=1, value=1)
    with col3:
        deadline = st.date_input("마감 기한", value=date.today())
    with col4:
        priority = st.selectbox("우선순위", ["높음", "보통", "낮음"])

    if st.button("➕ 추가", use_container_width=True):
        if task.strip():
            st.session_state.tasks.append({
                "과목": task,
                "시간": hours,
                "마감": str(deadline),
                "우선순위": priority,
                "완료": False
            })
        else:
            st.warning("⚠️ 과목/주제를 입력하세요!")

# --- 계획 표시 ---
st.subheader("📅 내 공부 계획")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)

    # ✅ 체크박스 포함된 표
    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "완료": st.column_config.CheckboxColumn("완료"),
            "과목": st.column_config.TextColumn("과목"),
            "시간": st.column_config.NumberColumn("시간(h)"),
            "마감": st.column_config.DateColumn("마감"),
            "우선순위": st.column_config.SelectboxColumn(
                "우선순위", options=["높음", "보통", "낮음"]
            ),
        },
        use_container_width=True,
    )

    # 업데이트
    st.session_state.tasks = edited_df.to_dict(orient="records")

    # 진행률
    done = sum(1 for t in st.session_state.tasks if t["완료"])
    total = len(st.session_state.tasks)
    st.progress(done / total if total else 0)
    st.write(f"✅ 완료 {done}/{total}개")

    # 다운로드 버튼
    st.download_button(
        "📥 CSV 다운로드",
        pd.DataFrame(st.session_state.tasks).to_csv(index=False).encode("utf-8"),
        "study_plan.csv",
        "text/csv",
        use_container_width=True,
    )
else:
    st.info("아직 등록된 할 일이 없습니다.")
