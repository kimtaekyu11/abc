import streamlit as st
from streamlit.components.v1 import html

# HTML + JavaScript로 피하기 게임 만들기
game_code = """
<!DOCTYPE html>
<html>
<head>
  <title>피하기 게임</title>
  <style>
    body { margin: 0; overflow: hidden; }
    canvas { background-color: #f4f4f4; display: block; }
    #score { font-size: 20px; font-family: 'Arial', sans-serif; position: absolute; top: 10px; left: 10px; color: #333; }
  </style>
</head>
<body>
  <canvas id="gameCanvas"></canvas>
  <div id="score"></div>
  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const playerWidth = 50;
    const playerHeight = 50;
    let playerX = canvas.width / 2 - playerWidth / 2;
    let playerY = canvas.height - playerHeight - 10;
    let playerSpeed = 10;  // 플레이어 속도
    let gameInterval;
    let score = 0;

    let moveLeft = false;
    let moveRight = false;
    let moveUp = false;
    let moveDown = false;

    // 게임 환경 설정
    window.onload = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      startGame();
    };

    // 키 입력 감지
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        moveLeft = true;
      }
      if (e.key === 'ArrowRight') {
        moveRight = true;
      }
      if (e.key === 'ArrowUp') {
        moveUp = true;
      }
      if (e.key === 'ArrowDown') {
        moveDown = true;
      }
    });

    document.addEventListener('keyup', (e) => {
      if (e.key === 'ArrowLeft') {
        moveLeft = false;
      }
      if (e.key === 'ArrowRight') {
        moveRight = false;
      }
      if (e.key === 'ArrowUp') {
        moveUp = false;
      }
      if (e.key === 'ArrowDown') {
        moveDown = false;
      }
    });

    // 점수 업데이트
    function updateScore() {
      document.getElementById('score').innerText = '점수: ' + score;
    }

    // 캐릭터 그리기
    function drawPlayer() {
      ctx.fillStyle = '#3498db'; // 캐릭터 색상
      ctx.beginPath();
      ctx.arc(playerX + playerWidth / 2, playerY + playerHeight / 2, playerWidth / 2, 0, Math.PI * 2);
      ctx.fill();
    }

    // 장애물
    let obstacles = [];
    function createObstacle() {
      let size = Math.random() * 50 + 30;
      let x = Math.random() * (canvas.width - size);
      let y = -size;
      let speed = 5 + Math.random() * 3;
      let direction = Math.random() < 0.5 ? 1 : -1; // 장애물이 지그재그로 이동하도록 방향 설정
      obstacles.push({ x: x, y: y, size: size, speed: speed, direction: direction });
    }

    // 장애물 그리기
    function drawObstacles() {
      ctx.fillStyle = '#e74c3c'; // 장애물 색상
      obstacles.forEach(obstacle => {
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.size, obstacle.size);
        obstacle.y += obstacle.speed;
        obstacle.x += obstacle.direction * 2; // 지그재그 이동

        // 장애물이 화면 밖으로 나가면 제거
        if (obstacle.y > canvas.height) {
          obstacles = obstacles.filter(o => o !== obstacle);
        }

        // 충돌 감지
        if (
          playerX < obstacle.x + obstacle.size &&
          playerX + playerWidth > obstacle.x &&
          playerY < obstacle.y + obstacle.size &&
          playerY + playerHeight > obstacle.y
        ) {
          clearInterval(gameInterval);
          alert('게임 오버! 점수: ' + score);
          window.location.reload(); // 게임 재시작
        }
      });
    }

    // 게임 루프
    function updateGame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 플레이어 이동
      if (moveLeft && playerX > 0) {
        playerX -= playerSpeed;
      }
      if (moveRight && playerX < canvas.width - playerWidth) {
        playerX += playerSpeed;
      }
      if (moveUp && playerY > 0) {
        playerY -= playerSpeed;
      }
      if (moveDown && playerY < canvas.height - playerHeight) {
        playerY += playerSpeed;
      }

      // 점수 증가
      score += 1;
      updateScore();

      // 캐릭터 그리기
      drawPlayer();

      // 장애물 그리기
      drawObstacles();

      // 새 장애물 생성
      if (Math.random() < 0.02) {
        createObstacle();
      }
    }

    // 게임 시작
    function startGame() {
      gameInterval = setInterval(updateGame, 20);
    }
  </script>
</body>
</html>
"""

# Streamlit으로 HTML 코드 삽입
html(game_code, height=700)
