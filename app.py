<head>
  <title>피하기 게임</title>
  <style>
    body { margin: 0; overflow: hidden; }
    canvas { background-color: #f4f4f4; display: block; }
    #score { font-size: 20px; font-family: 'Arial', sans-serif; position: absolute; top: 10px; left: 10px; color: #333; }
    #message { font-size: 24px; font-family: 'Arial', sans-serif; position: absolute; top: 100px; right: 20px; color: #e74c3c; font-weight: bold; }
  </style>
</head>
<body>
  <canvas id="gameCanvas"></canvas>
  <div id="score"></div>
  <div id="message"></div>
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

    let messages = [
      "넌 이제 끝이야!", 
      "한 번 더 도전해봐!", 
      "움직여, 피할 수 있어!", 
      "지금이 기회야!"
    ];

    let currentMessage = 0;

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

    // 대사 업데이트
    function updateMessage() {
      document.getElementById('message').innerText = messages[currentMessage];
      currentMessage = (currentMessage + 1) % messages.length;
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
      let shape = Math.random() < 0.33 ? 'square' : (Math.random() < 0.5 ? 'circle' : 'triangle');
      let x, y, speedX = 0, speedY = 0;

      // 장애물 위치 랜덤으로 설정 (사방에서 나오게)
      const direction = Math.floor(Math.random() * 4); // 0: 위, 1: 아래, 2: 왼쪽, 3: 오른쪽

      if (direction === 0) {  // 위에서 나오는 장애물
        x = Math.random() * canvas.width;
        y = -size;
        speedY = 5 + Math.random() * 3;
      } else if (direction === 1) {  // 아래에서 나오는 장애물
        x = Math.random() * canvas.width;
        y = canvas.height + size;
        speedY = -(5 + Math.random() * 3);
      } else if (direction === 2) {  // 왼쪽에서 나오는 장애물
        x = -size;
        y = Math.random() * canvas.height;
        speedX = 5 + Math.random() * 3;
      } else {  // 오른쪽에서 나오는 장애물
        x = canvas.width + size;
        y = Math.random() * canvas.height;
        speedX = -(5 + Math.random() * 3);
      }

      obstacles.push({ x: x, y: y, size: size, shape: shape, speedX: speedX, speedY: speedY, angle: 0 });
    }

    // 장애물 그리기
    function drawObstacles() {
      obstacles.forEach(obstacle => {
        // 장애물 모양에 따라 다르게 그리기
        ctx.fillStyle = '#e74c3c'; // 기본 장애물 색상

        ctx.save();
        ctx.translate(obstacle.x + obstacle.size / 2, obstacle.y + obstacle.size / 2); // 회전의 중심점 설정
        ctx.rotate(obstacle.angle);  // 회전 각도 적용
        ctx.translate(-obstacle.size / 2, -obstacle.size / 2); // 회전 후 원래 위치로 복원

        if (obstacle.shape === 'square') {
          ctx.fillRect(0, 0, obstacle.size, obstacle.size);
        } else if (obstacle.shape === 'circle') {
          ctx.beginPath();
          ctx.arc(obstacle.size / 2, obstacle.size / 2, obstacle.size / 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (obstacle.shape === 'triangle') {
          ctx.beginPath();
          ctx.moveTo(0, obstacle.size);
          ctx.lineTo(obstacle.size / 2, 0);
          ctx.lineTo(obstacle.size, obstacle.size);
          ctx.closePath();
          ctx.fill();
        }

        ctx.restore(); // 회전 복원

        // 장애물 이동
        obstacle.x += obstacle.speedX;
        obstacle.y += obstacle.speedY;
        obstacle.angle += 0.05;  // 장애물 회전 속도

        // 장애물이 화면 밖으로 나가면 제거
        if (
          obstacle.x < -obstacle.size || obstacle.x > canvas.width || 
          obstacle.y < -obstacle.size || obstacle.y > canvas.height
        ) {
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

      // 대사 업데이트
      updateMessage();

      // 캐릭터 그리기
      drawPlayer();

      // 장애물 그리기
      drawObstacles();

      // 새 장애물 생성 (빠르게 생성)
      if (Math.random() < 0.05) { // 장애물 빈도 증가
        createObstacle();
      }
    }

    // 게임 시작
    function startGame() {
      gameInterval = setInterval(updateGame, 16); // 게임 속도
