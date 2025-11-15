import streamlit as st
import time

# 게임 상태를 저장할 세션 상태 변수
if 'score' not in st.session_state:
    st.session_state.score = 0  # 초기 점수
if 'click_multiplier' not in st.session_state:
    st.session_state.click_multiplier = 1  # 초기 클릭 배수
if 'upgrade_cost' not in st.session_state:
    st.session_state.upgrade_cost = 20  # 첫 번째 업그레이드 비용
if 'auto_clicker_level' not in st.session_state:
    st.session_state.auto_clicker_level = 0  # 자동 클릭기 레벨
if 'auto_clicker_cost' not in st.session_state:
    st.session_state.auto_clicker_cost = 100  # 자동 클릭기 구매 비용
if 'upgrade_message' not in st.session_state:
    st.session_state.upgrade_message = ""  # 업그레이드 메시지

# 게임 제목
st.title("쿠키 클리커 - 업그레이드 및 자동 점수 증가")

# 점수 표시
st.write(f"점수: {st.session_state.score}")
st.write(f"현재 클릭 배수: x{st.session_state.click_multiplier}")
st.write(f"자동 클릭기 레벨: {st.session_state.auto_clicker_level}")

# 자동 클릭기 업그레이드 기능
def upgrade_auto_clicker():
    if st.session_state.score >= st.session_state.auto_clicker_cost:
        st.session_state.score -= st.session_state.auto_clicker_cost
        st.session_state.auto_clicker_level += 1  # 자동 클릭기 레벨 증가
        st.session_state.auto_clicker_cost = int(st.session_state.auto_clicker_cost * 1.5)  # 자동 클릭기 비용 증가
        st.session_state.upgrade_message = f"자동 클릭기가 {st.session_state.auto_clicker_level} 레벨로 업그레이드되었습니다!"
    else:
        st.session_state.upgrade_message = "점수가 부족합니다. 업그레이드를 위해 더 많은 점수가 필요합니다."

# 클릭 배수 업그레이드 기능
def upgrade_click_multiplier():
    if st.session_state.score >= st.session_state.upgrade_cost:
        st.session_state.score -= st.session_state.upgrade_cost
        st.session_state.click_multiplier += 1  # 클릭 배수 증가
        st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)  # 업그레이드 비용 증가
        st.session_state.upgrade_message = f"클릭 배수가 x{st.session_state.click_multiplier}로 업그레이드되었습니다!"
    else:
        st.session_state.upgrade_message = "점수가 부족합니다. 업그레이드를 위해 더 많은 점수가 필요합니다."

# 업그레이드 버튼
if st.button(f"자동 클릭기 업그레이드 (비용: {st.session_state.auto_clicker_cost} 점)"):
    upgrade_auto_clicker()

if st.button(f"클릭 배수 업그레이드 (비용: {st.session_state.upgrade_cost} 점)"):
    upgrade_click_multiplier()

# 업그레이드 메시지 표시
if st.session_state.upgrade_message:
    st.success(st.session_state.upgrade_message)

# 클릭 버튼 (클릭 시 효과)
click_button_effect = st.empty()  # 클릭 효과를 위해 빈 공간 생성
if st.button("클릭!"):
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
    
    # 점수 증가: 클릭 배수만큼 증가
    st.session_state.score += st.session_state.click_multiplier

# 자동 클릭기 작동
def auto_clicker():
    if st.session_state.auto_clicker_level > 0:
        interval = 2  # 자동 클릭 주기 (초)
        last_click_time = st.session_state.get("last_click_time", 0)
        current_time = time.time()
        
        # 일정 시간마다 자동으로 점수 증가
        if current_time - last_click_time > interval:
            st.session_state.score += st.session_state.auto_clicker_level  # 자동 클릭으로 점수 증가
            st.session_state.get("last_click_time", current_time)  # 마지막 자동 클릭 시간 갱신
            st.write(f"자동 클릭기 {st.session_state.auto_clicker_level} 레벨이 작동 중...")

# 자동 클릭기 작동 실행
auto_clicker()
