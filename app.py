import streamlit as st
import time
from streamlit.components.v1 import html

# HTML + JavaScript로 피하기 게임 만들기
game_code = """
<!DOCTYPE html>
<html>
<head>
  <title>피하기 게임</title>
  <style>
    body { margin: 0; overflow: hidden; }
    canvas { background-color: #eee; display: block; }
  </style>
</head>
<body>
  <canvas id="gameCanvas"></canvas>
  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const playerWidth = 50;
    const playerHeight = 20;
    let playerX = canvas.width / 2 - playerWidth / 2;
    let playerY = canvas.height - playerHeight - 10;
    let playerSpeed = 5;
    let gameInterval;
    let score = 0;

    // 게임 환경 설정
    window.onload = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      startGame();
    };

    // 키 입력 감지
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft' && playerX > 0) {
        playerX -= playerSpeed;
      }
      if (e.key === 'ArrowRight' && playerX < canvas.width - playerWidth) {
        playerX += playerSpeed;
      }
    });

    // 장애물
    let obstacles = [];
    function createObstacle() {
      let size = Math.random() * 50 + 30;
      let x = Math.random() * (canvas.width - size);
      obstacles.push({ x: x, y: -size, size: size });
    }

    // 게임 루프
    function updateGame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // 플레이어 그리기
      ctx.fillStyle = '#00f';
      ctx.fillRect(playerX, playerY, playerWidth, playerHeight);
      
      // 장애물 그리기
      ctx.fillStyle = '#f00';
      obstacles.forEach(obstacle => {
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.size, obstacle.size);
        obstacle.y += 5;
        
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

      // 장애물 제거
      obstacles = obstacles.filter(obstacle => obstacle.y < canvas.height);

      // 점수 증가
      score += 1;

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


