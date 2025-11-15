import streamlit as st

# 게임 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0

# 게임 타이틀
st.title("간단한 클리커 게임")

# 점수 출력
st.write(f"점수: {st.session_state.score}")

# 클릭 버튼
if st.button("클릭!"):
    st.session_state.score += 1

# 게임 설명
st.write("""
클릭 버튼을 클릭하면 점수가 증가합니다.
""")

