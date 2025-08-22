import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="스터디 플래너", layout="wide")
st.title("📖 자동 스터디 플래너 ")

# 세션 초기화
if "plans" not in st.session_state:
    st.session_state.plans = []

# --- 입력 영역 ---
st.sidebar.header("✏️ 새로운 시험 계획 추가")
subject = st.sidebar.text_input("과목 / 시험 이름", placeholder="예: 수학 문제집")
unit_type = st.sidebar.selectbox("공부 단위", ["페이지", "문제", "단어"])
start_num = st.sidebar.number_input(f"시작 {unit_type} 번호", min_value=1, value=1)
end_num = st.sidebar.number_input(f"끝 {unit_type} 번호", min_value=1, value=100)
exam_date = st.sidebar.date_input("시험 날짜", value=date.today() + timedelta(days=7))

if st.sidebar.button("📌 계획 생성", use_container_width=True):
    if subject.strip():
        total_units = end_num - start_num + 1
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.sidebar.error("⚠️ 시험 날짜가 오늘보다 이전입니다!")
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
