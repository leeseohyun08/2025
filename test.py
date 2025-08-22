import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📚 자동 스터디 플래너")

# 세션 초기화
if "plan" not in st.session_state:
    st.session_state.plan = []

# --- 입력 영역 ---
st.subheader("✏️ 시험 정보 입력")
subject = st.text_input("과목 / 시험 이름")
unit_start = st.number_input("시작 단원(또는 번호)", min_value=1, value=1)
unit_end = st.number_input("끝 단원(또는 번호)", min_value=1, value=10)
exam_date = st.date_input("시험 날짜", value=date.today() + timedelta(days=7))

if st.button("📌 자동 계획 생성"):
    if subject.strip():
        total_units = unit_end - unit_start + 1
        days_left = (exam_date - date.today()).days
        
        if days_left <= 0:
            st.error("⚠️ 시험 날짜가 오늘보다 이전입니다!")
        else:
            units_per_day = total_units // days_left
            extra = total_units % days_left

            plan = []
            current_unit = unit_start

            for i in range(days_left):
                today = date.today() + timedelta(days=i)
                count = units_per_day + (1 if i < extra else 0)
                if count > 0:
                    plan.append({
                        "날짜": today,
                        "공부 범위": f"{subject} {current_unit} ~ {current_unit+count-1} 단원",
                        "완료": False
                    })
                    current_unit += count

            st.session_state.plan = plan
    else:
        st.warning("⚠️ 과목명을 입력하세요!")

# --- 계획 표시 ---
st.subheader("📅 자동 생성된 공부 계획")

if st.session_state.plan:
    df = pd.DataFrame(st.session_state.plan)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "완료": st.column_config.CheckboxColumn("완료"),
            "날짜": st.column_config.DateColumn("날짜"),
            "공부 범위": st.column_config.TextColumn("공부 범위"),
        },
        use_container_width=True,
    )

    st.session_state.plan = edited_df.to_dict(orient="records")

    # 진행률
    done = sum(1 for p in st.session_state.plan if p["완료"])
    total = len(st.session_state.plan)
    st.progress(done / total if total else 0)
    st.write(f"✅ 완료 {done}/{total}개")

    # 다운로드 버튼
    st.download_button(
        "📥 계획 다운로드 (CSV)",
        pd.DataFrame(st.session_state.plan).to_csv(index=False).encode("utf-8"),
        "study_plan.csv",
        "text/csv",
        use_container_width=True,
    )
else:
    st.info("아직 생성된 계획이 없습니다. 위에서 시험 정보를 입력하세요!")
