import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📖 자동 스터디 플래너")

# 세션 초기화
if "plans" not in st.session_state:
    st.session_state.plans = []

# 좌우 컬럼 나누기
col1, col2 = st.columns([1, 3])  # 왼쪽 좁게, 오른쪽 넓게

# ------------------------ #
# 📌 왼쪽: 계획 추가 & 선택
# ------------------------ #
with col1:
    st.header("📝 계획 추가")
    subject = st.text_input("과목명", placeholder="예: 수학 문제집")
    unit_type = st.selectbox("단위", ["페이지", "문제", "단어"])
    start = st.number_input(f"시작 {unit_type}", min_value=1, value=1, step=1)
    end = st.number_input(f"끝 {unit_type}", min_value=1, value=100, step=1)
    exam_date = st.date_input("시험 날짜", value=date.today() + timedelta(days=7))

    if st.button("➕ 계획 생성", use_container_width=True):
        if subject.strip():
            total_units = end - start + 1
            days_left = (exam_date - date.today()).days

            if days_left <= 0:
                st.error("⚠️ 시험 날짜가 오늘보다 이전입니다!")
            else:
                units_per_day = total_units // days_left
                extra = total_units % days_left
                current = start

                plan = []
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

                # ✅ 괄호 닫기 주의
                st.session_state.plans.append({
                    "과목": subject,
                    "시험일": exam_date,
                    "단위": unit_type,
                    "계획": plan
                })
                st.success(f"✅ '{subject}' 계획이 생성되었습니다!")

    st.divider()
    st.header("📂 계획 목록")

    plan_names = [f"{p['과목']} ({p['시험일']})" for p in st.session_state.plans]
    selected_index = (
        st.selectbox(
            "📌 확인할 계획 선택",
            range(len(plan_names)),
            format_func=lambda i: plan_names[i]
        )
        if plan_names else None
    )

# ---------------------------- #
# 📋 오른쪽: 선택된 계획 보여주기
# ---------------------------- #
with col2:
    st.header("📅 선택한 공부 계획")

    if plan_names:
        selected_plan = st.session_state.plans[selected_index]
        df = pd.DataFrame(selected_plan["계획"])

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

        # 상태 업데이트
        st.session_state.plans[selected_index]["계획"] = edited_df.to_dict(orient="records")

        # 진행률 표시
        done = sum(1 for p in edited_df.to_dict(orient="records") if p["완료"])
        total = len(edited_df)
        st.progress(done / total if total else 0)
        st.write(f"✅ {done}/{total} 완료 ({round(done/total*100,1) if total else 0}%)")

        # 다운로드 버튼
        st.download_button(
            f"📥 계획 다운로드 (CSV)",
            edited_df.to_csv(index=False).encode("utf-8"),
            f"{selected_plan['과목']}_plan.csv",
            "text/csv",
            use_container_width=True,
        )
    else:
        st.info("왼쪽에서 새 계획을 먼저 추가하세요!")
