import streamlit as st

# 게임 상태를 저장할 세션 상태 변수
if 'score' not in st.session_state:
    st.session_state.score = 0  # 초기 점수
if 'click_multiplier' not in st.session_state:
    st.session_state.click_multiplier = 1  # 초기 클릭 배수
if 'upgrade_cost' not in st.session_state:
    st.session_state.upgrade_cost = 20  # 첫 번째 업그레이드 비용
if 'upgrade_message' not in st.session_state:
    st.session_state.upgrade_message = ""  # 업그레이드 메시지

# 게임 제목
st.title("클리커 게임 - 클릭 배수 업그레이드")

# 점수 표시
st.write(f"점수: {st.session_state.score}")
st.write(f"현재 클릭 배수: x{st.session_state.click_multiplier}")

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

# 게임 종료 기능 (조건에 맞추어 종료할 수 있습니다)
if st.button("게임 종료"):
    st.session_state.score = 0
    st.session_state.click_multiplier = 1
    st.session_state.upgrade_cost = 20
    st.session_state.upgrade_message = ""
    st.write("게임이 종료되었습니다. 새로 시작하려면 페이지를 새로 고침 하세요.")

