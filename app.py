<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>클리커 게임</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }

        h1 {
            margin-top: 50px;
            color: #333;
        }

        #score {
            font-size: 2em;
            color: #27ae60;
            margin-top: 20px;
        }

        #clickButton {
            padding: 20px 40px;
            font-size: 1.5em;
            margin-top: 30px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }

        #clickButton:hover {
            background-color: #2980b9;
        }

        #upgrades {
            margin-top: 40px;
        }

        .upgrade {
            margin: 10px;
            padding: 10px;
            font-size: 1.2em;
            background-color: #f39c12;
            color: white;
            cursor: pointer;
            border-radius: 5px;
            width: 200px;
            margin: 10px auto;
        }

        .upgrade:hover {
            background-color: #e67e22;
        }

        .upgrade.disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }

        #message {
            font-size: 1.5em;
            color: #e74c3c;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <h1>클리커 게임</h1>
    <div id="score">점수: 0</div>
    <button id="clickButton">클릭해서 점수 얻기</button>

    <div id="upgrades">
        <div class="upgrade" id="upgrade1">
            클릭 당 점수 +1 추가 (가격: 10점)
        </div>
        <div class="upgrade" id="upgrade2">
            클릭 당 점수 +5 추가 (가격: 50점)
        </div>
        <div class="upgrade" id="upgrade3">
            클릭 당 점수 +10 추가 (가격: 100점)
        </div>
    </div>

    <div id="message"></div>

    <script>
        let score = 0;
        let scorePerClick = 1;

        const upgradePrices = [10, 50, 100];
        const upgradeBonuses = [1, 5, 10];
        let upgradesBought = [false, false, false];

        const scoreElement = document.getElementById("score");
        const clickButton = document.getElementById("clickButton");
        const messageElement = document.getElementById("message");

        const upgradeElements = [
            document.getElementById("upgrade1"),
            document.getElementById("upgrade2"),
            document.getElementById("upgrade3")
        ];

        clickButton.addEventListener("click", function() {
            score += scorePerClick;
            updateScore();
            checkUpgrades();
        });

        upgradeElements.forEach((upgrade, index) => {
            upgrade.addEventListener("click", () => {
                if (score >= upgradePrices[index] && !upgradesBought[index]) {
                    score -= upgradePrices[index];
                    scorePerClick += upgradeBonuses[index];
                    upgradesBought[index] = true;
                    upgrade.classList.add("disabled");
                    messageElement.textContent = `${upgradeBonuses[index]} 추가! 업그레이드 완료!`;
                    updateScore();
                    checkUpgrades();
                } else if (upgradesBought[index]) {
                    messageElement.textContent = "이미 이 업그레이드를 구매했습니다!";
                } else {
                    messageElement.textContent = "점수가 부족합니다!";
                }
            });
        });

        function updateScore() {
            scoreElement.textContent = `점수: ${score}`;
        }

        function checkUpgrades() {
            upgradeElements.forEach((upgrade, index) => {
                if (score >= upgradePrices[index] && !upgradesBought[index]) {
                    upgrade.classList.remove("disabled");
                }
            });
        }

        checkUpgrades();
    </script>
</body>
</html>
