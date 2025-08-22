import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📚 스터디 플래너 자동화 앱")

# --- 할 일 입력 ---
st.subheader("✏️ 공부할 일 추가")
task = st.text_input("과목 / 주제")
hours = st.number_input("예상 소요 시간 (시간)", min_value=1, max_value=24, step=1)
deadline = st.date_input("마감 기한")
priority = st.selectbox("우선순위", ["높음", "보통", "낮음"])

# --- 세션 상태 초기화 ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- 추가 버튼 ---
if st.button("추가"):
    if task.strip() != "":
        st.session_state.tasks.append({
            "과목": task,
            "시간": hours,
            "마감": str(deadline),
            "우선순위": priority,
            "완료": False
        })
        st.success(f"✅ '{task}' 추가됨!")
    else:
        st.warning("⚠️ 과목/주제를 입력하세요.")

# --- 할 일 리스트 표시 ---
st.subheader("📅 내 공부 계획")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)

    # ✅ 완료 버튼을 수정 가능하게 (data_editor 사용)
    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "완료": st.column_config.CheckboxColumn("완료"),
            "과목": st.column_config.TextColumn("과목"),
            "시간": st.column_config.NumberColumn("시간 (h)"),
            "마감": st.column_config.DateColumn("마감 기한"),
            "우선순위": st.column_config.SelectboxColumn(
                "우선순위", options=["높음", "보통", "낮음"]
            ),
        },
        use_container_width=True,
        num_rows="dynamic"  # 표에서 직접 행 추가/삭제 가능
    )

    # 세션 상태 업데이트
    st.session_state.tasks = edited_df.to_dict(orient="records")

    # 진행률 표시
    done_count = sum(1 for t in st.session_state.tasks if t["완료"])
    progress = done_count / len(st.session_state.tasks)
    st.progress(progress)
    st.write(f"진행률: {done_count}/{len(st.session_state.tasks)} 완료 ✅")

    # CSV 다운로드
    st.download_button(
        "📥 CSV 다운로드",
        pd.DataFrame(st.session_state.tasks).to_csv(index=False).encode("utf-8"),
        "study_plan.csv",
        "text/csv"
    )
else:
    st.info("아직 등록된 할 일이 없습니다.")
