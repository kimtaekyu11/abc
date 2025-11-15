import streamlit as st
import time

# 게임 상태를 저장할 세션 상태 변수
if 'score' not in st.session_state:
    st.session_state.score = 0  # 초기 점수
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0  # 초기 클릭 횟수

# 게임 제목
st.title("클리커 게임")

# 점수 및 클릭 수 표시
st.write(f"점수: {st.session_state.score}")
st.write(f"클릭 횟수: {st.session_state.clicks}")

# 버튼 클릭 이벤트 처리
if st.button("클릭!"):
    st.session_state.score += 1  # 점수 증가
    st.session_state.clicks += 1  # 클릭 횟수 증가

# 자동으로 점수를 증가시키는 기능 (예: 5초마다 자동 점수 증가)
st.write("자동 점수 증가 중...")
auto_click_time = 5  # 5초마다 점수 증가
if time.time() % auto_click_time < 1:
    st.session_state.score += 1
    st.session_state.clicks += 1

# 게임 종료 기능 (조건에 맞추어 종료할 수 있습니다)
if st.button("게임 종료"):
    st.session_state.score = 0
    st.session_state.clicks = 0
    st.write("게임이 종료되었습니다. 새로 시작하려면 페이지를 새로 고침 하세요.")
