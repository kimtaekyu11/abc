import streamlit as st

# 게임 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'auto_clicker' not in st.session_state:
    st.session_state.auto_clicker = 0
if 'click_boost' not in st.session_state:
    st.session_state.click_boost = 1
if 'next_upgrade_cost' not in st.session_state:
    st.session_state.next_upgrade_cost = 50

# 게임 타이틀
st.title("업그레이드 기능이 있는 간단한 클리커 게임")

# 점수 출력
st.write(f"현재 점수: {st.session_state.score}")
st.write(f"자동 클릭기 보유: {st.session_state.auto_clicker}개")
st.write(f"클릭 당 점수 보너스: {st.session_state.click_boost}배")

# 자동 클릭기 효과
st.session_state.score += st.session_state.auto_clicker

# 클릭 버튼
if st.button("클릭!"):
    st.session_state.score += st.session_state.click_boost

# 업그레이드 버튼
if st.session_state.score >= st.session_state.next_upgrade_cost:
    if st.button(f"자동 클릭기 업그레이드 (가격: {st.session_state.next_upgrade_cost} 점수)"):
        st.session_state.auto_clicker += 1
        st.session_state.score -= st.session_state.next_upgrade_cost
        st.session_state.next_upgrade_cost *= 2  # 업그레이드 가격 증가
else:
    st.write("자동 클릭기를 구매하려면 더 많은 점수가 필요합니다!")

# 클릭 보너스 업그레이드
if st.session_state.score >= st.session_state.next_upgrade_cost:
    if st.button(f"클릭 보너스 업그레이드 (가격: {st.session_state.next_upgrade_cost} 점수)"):
        st.session_state.click_boost += 1
        st.session_state.score -= st.session_state.next_upgrade_cost
        st.session_state.next_upgrade_cost *= 2  # 업그레이드 가격 증가

# 게임 설명
st.write("""
### 업그레이드 설명:
- **자동 클릭기**: 자동으로 점수를 추가합니다.
- **클릭 보너스**: 클릭할 때마다 점수 상승량이 증가합니다.
""")
