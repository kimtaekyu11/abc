import streamlit as st

# 클릭 기록을 저장할 공간 만들기
if "count" not in st.session_state:
    st.session_state.count = 0

# 빨간색 버튼을 위한 CSS
st.markdown("""
    <style>
    div.stButton > button {
        background-color: red;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 안내 문구
st.write("클릭해주세요")

# 버튼
if st.button("버튼"):
    st.session_state.count += 1

# 버튼을 누른 횟수만큼 "하꼬" 출력
for _ in range(st.session_state.count):
    st.write("하꼬")
