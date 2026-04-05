import streamlit as st

# -----------------------------
# 🔹 상태 초기화
# -----------------------------
if "coins" not in st.session_state:
    st.session_state.coins = 0

if "owned" not in st.session_state:
    st.session_state.owned = []

if "displayed" not in st.session_state:
    st.session_state.displayed = []

# -----------------------------
# 🔹 이미지 생성 함수
# -----------------------------
def get_image(name):
    return f"https://ui-avatars.com/api/?name={name}&background=random&size=150"

# -----------------------------
# 🔹 제목
# -----------------------------
st.title("🌀 피하기 게임")

# -----------------------------
# 🔹 로비 (전시)
# -----------------------------
st.subheader("🏛 로비 (전시된 초상화)")

if len(st.session_state.displayed) == 0:
    st.info("전시된 초상화가 없습니다.")
else:
    cols = st.columns(4)
    for i, p in enumerate(st.session_state.displayed):
        with cols[i % 4]:
            st.image(get_image(p))
            if st.button(f"{p} 내리기", key=f"remove_{p}_{i}"):
                st.session_state.displayed.remove(p)
                st.rerun()

st.divider()

# -----------------------------
# 🔹 게임 영역 (HTML + JS)
# -----------------------------
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; overflow:hidden; }
#game {
  position: relative;
  width: 100%;
  height: 400px;
  background: black;
  cursor: none;
}
.obstacle {
  position: absolute;
  font-size: 40px;
  color: red;
  user-select: none;
}
#player {
  position: absolute;
  width: 10px;
  height: 10px;
  background: cyan;
  border-radius: 50%;
}
#gameover {
  position: absolute;
  color: white;
  font-size: 30px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: none;
}
</style>
</head>
<body>
<div id="game">
  <div id="player"></div>
  <div id="gameover">GAME OVER</div>
</div>

<script>
let game = document.getElementById("game");
let player = document.getElementById("player");
let gameover = document.getElementById("gameover");

let obstacles = [];
let startTime = Date.now();
let running = true;

// 마우스 따라가기
document.addEventListener("mousemove", (e) => {
    player.style.left = e.clientX + "px";
    player.style.top = e.clientY + "px";
});

// 장애물 생성
function createObstacle() {
    let o = document.createElement("div");
    o.className = "obstacle";
    o.innerText = Math.random() > 0.5 ? "문" : "베";

    let size = Math.random() * 30 + 30;
    let speed = Math.random() * 3 + 1;

    o.style.left = Math.random() * window.innerWidth + "px";
    o.style.top = Math.random() * 400 + "px";
    o.style.fontSize = size + "px";

    game.appendChild(o);

    obstacles.push({el:o, angle:0, speed:speed});
}

// 충돌 체크
function checkCollision(a, b) {
    let r1 = a.getBoundingClientRect();
    let r2 = b.getBoundingClientRect();
    return !(r2.left > r1.right || 
             r2.right < r1.left || 
             r2.top > r1.bottom ||
             r2.bottom < r1.top);
}

// 게임 루프
function loop() {
    if (!running) return;

    obstacles.forEach(o => {
        o.angle += o.speed * 5;
        o.el.style.transform = "rotate(" + o.angle + "deg)";

        if (checkCollision(player, o.el)) {
            running = false;
            gameover.style.display = "block";

            let time = Math.floor((Date.now() - startTime)/1000);

            // Streamlit으로 점수 보내기
            window.parent.postMessage({score: time}, "*");
        }
    });

    requestAnimationFrame(loop);
}

// 시작
setInterval(createObstacle, 800);
loop();
</script>
</body>
</html>
"""

st.components.v1.html(game_html, height=420)

# -----------------------------
# 🔹 코인 표시
# -----------------------------
st.write(f"💰 현재 코인: {st.session_state.coins}")
st.write("⏱ 살아남은 시간 = 코인")

# -----------------------------
# 🔹 상점
# -----------------------------
st.subheader("🛒 상점 (각 100코인)")

presidents = ["김대중", "노무현", "이명박", "박근혜", "문재인", "윤석열", "이재명"]

cols = st.columns(3)

for i, p in enumerate(presidents):
    with cols[i % 3]:
        if p in st.session_state.owned:
            st.success(f"{p} (보유)")

            if p not in st.session_state.displayed:
                if st.button(f"{p} 전시하기", key=f"display_{p}"):
                    st.session_state.displayed.append(p)
                    st.rerun()
            else:
                st.info("전시 중")

        else:
            if st.button(f"{p} 구매 (100코인)", key=p):
                if st.session_state.coins >= 100:
                    st.session_state.coins -= 100
                    st.session_state.owned.append(p)
                    st.rerun()
                else:
                    st.warning("코인이 부족합니다!")
