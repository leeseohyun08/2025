import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📖 자동 스터디 플래너")

# 세션 초기화
if "plans" not in st.session_state:
    st.session_state.plans = []

# --- 입력 영역 ---
st.subheader("✏️ 새로운 시험 계획 추가")
subject = st.text_input("과목 / 시험 이름", placeholder="예: 수학 문제집")
unit_type = st.selectbox("공부 단위", ["페이지", "문제", "단어"])
start_num = st.number_input(f"시작 {unit_type} 번호", min_value=1, value=1)
end_num = st.number_input(f"끝 {unit_type} 번호", min_value=1, value=100)
exam_date = st.date_input("시험 날짜", value=date.today() + timedelta(days=7))

if st.button("📌 계획 생성", use_container_width=True):
    if subject.strip():
        total_units = end_num - start_num + 1
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("⚠️ 시험 날짜가 오늘보다 이전입니다!")
        else:
            units_per_day = total_units // days_left
            extra = total_units % days_left

            plan = []
            current = start_num

            for i in range(days_left):
                today = date.today() + timedelta(days=i)
                count = units_per_day + (1 if i < extra else 0)
                if count > 0:
                    plan.append({
                        "날짜": today,
                        "공부 범위": f"{subject} {current} ~ {current+count-1} {unit_type}",
                        "완료": False
                    })
                    current += count

            st.session_state.plans.append({
                "과목": subject,
                "시험일": exam_date,
                "단위": unit_type,
                "계획": plan
            })
            st.success(f"✅ '{subject}' 계획이 생성되었습니다!")
    else:
        st.warning("⚠️ 과목명을 입력하세요!")

# --- 계획 표시 ---
st.subheader("📅 나의 공부 계획")

if st.session_state.plans:
    for idx, plan_obj in enumerate(st.session_state.plans):
        subject = plan_obj["과목"]
        exam_date = plan_obj["시험일"]
        unit_type = plan_obj["단위"]

        with st.expander(f"📘 {subject} (시험일: {exam_date})", expanded=True):
            df = pd.DataFrame(plan_obj["계획"])

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

            # 업데이트 반영
            st.session_state.plans[idx]["계획"] = edited_df.to_dict(orient="records")

            # 진행률
            done = sum(1 for p in edited_df.to_dict(orient="records") if p["완료"])
            total = len(edited_df)
            st.progress(done / total if total else 0)
            st.write(f"✅ {done}/{total} 완료 ({round(done/total*100,1) if total else 0}%)")

            # CSV 다운로드
            st.download_button(
                f"📥 {subject} 계획 다운로드 (CSV)",
                edited_df.to_csv(index=False).encode("utf-8"),
                f"{subject}_study_plan.csv",
                "text/csv",
                use_container_width=True,
            )
else:
    st.info("아직 생성된 계획이 없습니다. 위에서 시험 정보를 입력하세요!")
