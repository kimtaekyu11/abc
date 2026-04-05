import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# 🔹 상태 초기화
# -----------------------------
if "coins" not in st.session_state:
    st.session_state.coins = 0

if "owned" not in st.session_state:
    st.session_state.owned = []

if "displayed" not in st.session_state:
    st.session_state.displayed = []

if "last_score" not in st.session_state:
    st.session_state.last_score = 0

# -----------------------------
# 🔹 이미지
# -----------------------------
def get_image(name):
    return f"https://ui-avatars.com/api/?name={name}&background=random&size=150"

# -----------------------------
# 🔹 제목
# -----------------------------
st.title("🌀 피하기 게임")

# -----------------------------
# 🔹 로비
# -----------------------------
st.subheader("🏛 로비")

if len(st.session_state.displayed) == 0:
    st.info("전시 없음")
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
# 🔹 게임 HTML
# -----------------------------
game_html = """
<!DOCTYPE html>
<html>
<body>
<div id="game" style="width:100%; height:400px; background:black; position:relative; cursor:none;">
<div id="player" style="width:10px; height:10px; background:cyan; border-radius:50%; position:absolute;"></div>
<div id="gameover" style="color:white; font-size:30px; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); display:none;">GAME OVER</div>
<button id="restart" style="display:none; position:absolute; top:60%; left:50%; transform:translate(-50%,-50%);">다시 시작</button>
</div>

<script>
let game = document.getElementById("game");
let player = document.getElementById("player");
let gameover = document.getElementById("gameover");
let restartBtn = document.getElementById("restart");

let obstacles = [];
let running = true;
let startTime = Date.now();

// 마우스
document.addEventListener("mousemove", (e) => {
    player.style.left = e.clientX + "px";
    player.style.top = e.clientY + "px";
});

// 장애물 생성
function createObstacle() {
    let o = document.createElement("div");
    o.innerText = Math.random() > 0.5 ? "문" : "베";
    o.style.position = "absolute";
    o.style.color = "red";

    let size = Math.random()*30 + 30;
    o.style.fontSize = size + "px";

    let x = Math.random()*window.innerWidth;
    let y = Math.random()*350;

    let vx = (Math.random()-0.5)*4;
    let vy = (Math.random()-0.5)*4;

    game.appendChild(o);

    obstacles.push({
        el:o,
        x:x,
        y:y,
        vx:vx,
        vy:vy,
        angle:0
    });
}

// 충돌
function hit(a,b){
    let r1=a.getBoundingClientRect();
    let r2=b.getBoundingClientRect();
    return !(r2.left>r1.right || r2.right<r1.left || r2.top>r1.bottom || r2.bottom<r1.top);
}

// 루프
function loop(){
    if(!running) return;

    obstacles.forEach(o=>{
        o.x += o.vx;
        o.y += o.vy;

        // 벽 반사
        if(o.x<0 || o.x>window.innerWidth) o.vx*=-1;
        if(o.y<0 || o.y>350) o.vy*=-1;

        o.angle += 1; // 회전 속도 ↓
        o.el.style.transform = "rotate("+o.angle+"deg)";
        o.el.style.left = o.x+"px";
        o.el.style.top = o.y+"px";

        if(hit(player,o.el)){
            running=false;
            gameover.style.display="block";
            restartBtn.style.display="block";

            let score = Math.floor((Date.now()-startTime)/1000);
            window.parent.postMessage({score:score},"*");
        }
    });

    requestAnimationFrame(loop);
}

// 재시작
restartBtn.onclick = ()=>{
    location.reload();
}

// 시작
setInterval(createObstacle,1000);
loop();
</script>
</body>
</html>
"""

# -----------------------------
# 🔹 게임 출력
# -----------------------------
components.html(game_html, height=420)

# -----------------------------
# 🔥 코인 지급 처리
# -----------------------------
score = components.html("""
<script>
window.addEventListener("message", (event) => {
    if(event.data.score !== undefined){
        const streamlitDoc = window.parent.document;
        const input = streamlitDoc.createElement("input");
        input.type = "hidden";
        input.name = "score";
        input.value = event.data.score;
        streamlitDoc.body.appendChild(input);
    }
});
</script>
""", height=0)

# 수동 반영 (Streamlit 구조상 필요)
if st.button("🎁 점수 반영 (코인 받기)"):
    import random
    earned = random.randint(5,15)  # 테스트용 (실제 점수 연결은 제한 있음)
    st.session_state.coins += earned
    st.success(f"{earned} 코인 획득!")

# -----------------------------
# 🔹 코인
# -----------------------------
st.write(f"💰 코인: {st.session_state.coins}")

# -----------------------------
# 🔹 상점
# -----------------------------
st.subheader("🛒 상점")

presidents = ["김대중","노무현","이명박","박근혜","문재인","윤석열","이재명"]

cols = st.columns(3)

for i,p in enumerate(presidents):
    with cols[i%3]:
        if p in st.session_state.owned:
            st.success(f"{p} 보유")

            if p not in st.session_state.displayed:
                if st.button(f"{p} 전시", key="d"+p):
                    st.session_state.displayed.append(p)
                    st.rerun()
            else:
                st.info("전시중")

        else:
            if st.button(f"{p} 구매(100)", key=p):
                if st.session_state.coins>=100:
                    st.session_state.coins-=100
                    st.session_state.owned.append(p)
                    st.rerun()
                else:
                    st.warning("코인 부족")
