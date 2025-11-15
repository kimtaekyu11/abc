import streamlit as st
import time

# 게임 상태를 저장할 세션 상태 변수
if 'score' not in st.session_state:
    st.session_state.score = 0  # 초기 점수
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0  # 초기 클릭 횟수
if 'auto_clicker_level' not in st.session_state:
    st.session_state.auto_clicker_level = 0  # 자동 클릭기 레벨
if 'upgrade_cost' not in st.session_state:
    st.session_state.upgrade_cost = 10  # 업그레이드 비용
if 'upgrade_message' not in st.session_state:
    st.session_state.upgrade_message = ""  # 업그레이드 메시지

# 게임 제목
st.title("클리커 게임 - 업그레이드 버전")

# 점수 및 클릭 수 표시
st.write(f"점수: {st.session_state.score}")
st.write(f"클릭 횟수: {st.session_state.clicks}")

# 자동 클릭기 업그레이드
def upgrade_auto_clicker():
    if st.session_state.score >= st.session_state.upgrade_cost:
        st.session_state.score -= st.session_state.upgrade_cost
        st.session_state.auto_clicker_level += 1
        st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)  # 업그레이드 비용 증가
        st.session_state.upgrade_message = f"자동 클릭기가 {st.session_state.auto_clicker_level} 레벨로 업그레이드되었습니다!"
    else:
        st.session_state.upgrade_message = "점수가 부족합니다. 업그레이드를 위해 더 많은 점수가 필요합니다."

# 버튼 클릭 이벤트 처리
def click_button():
    st.session_state.score += 1  # 점수 증가
    st.session_state.clicks += 1  # 클릭 횟수 증가
    st.session_state.upgrade_message = ""  # 업그레이드 메시지 초기화

# 업그레이드 버튼
if st.button(f"자동 클릭기 업그레이드 (비용: {st.session_state.upgrade_cost} 점)"):
    upgrade_auto_clicker()

# 업그레이드 메시지 표시
if st.session_state.upgrade_message:
    st.success(st.session_state.upgrade_message)

# 클릭 버튼 (클릭 시 효과)
click_button_effect = st.empty()  # 클릭 효과를 위해 빈 공간 생성
if st.button("클릭!"):
    click_button()

    # 클릭 시 효과 (버튼 색상 변경)
    click_button_effect.markdown("""
        <style>
            .stButton>button {
                background-color: #FF5733;
                color: white;
                font-size: 20px;
                padding: 10px;
                border-radius: 10px;
            }
            .stButton>button:hover {
                background-color: #FF8552;
            }
        </style>
    """, unsafe_allow_html=True)

# 자동 클릭기 작동
def auto_clicker():
    if st.session_state.auto_clicker_level > 0:
        interval = 2  # 자동 클릭 주기 (초)
        st.session_state.score += st.session_state.auto_clicker_level  # 자동 클릭으로 점수 증가
        st.session_state.clicks += st.session_state.auto_clicker_level  # 클릭 횟수 증가
        st.write(f"자동 클릭기 {st.session_state.auto_clicker_level} 레벨이 작동 중...")

# 자동 클릭기 작동 실행
auto_clicker()

# 게임 종료 기능 (조건에 맞추어 종료할 수 있습니다)
if st.button("게임 종료"):
    st.session_state.score = 0
    st.session_state.clicks = 0
    st.session_state.auto_clicker_level = 0
    st.session_state.upgrade_cost = 10
    st.session_state.upgrade_message = ""
    st.write("게임이 종료되었습니다. 새로 시작하려면 페이지를 새로 고침 하세요.")
