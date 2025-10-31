let boxes = document.querySelectorAll(".box");
let resetBtn = document.querySelector("#reset-btn");
let newGameBtn = document.querySelector("#new-btn");
let msgContainer = document.querySelector(".msg-container");
let msg = document.querySelector("#msg");
let currentPlayerDisplay = document.querySelector("#turn-display");
let scoreXDisplay = document.querySelector("#score-x");
let scoreODisplay = document.querySelector("#score-o");

let playerX = prompt("Enter name for Player X:") || "Player X";
let playerO = prompt("Enter name for Player O:") || "Player O";

let turnO = true;
let count = 0;
let scoreX = 0;
let scoreO = 0;

const winPatterns = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
];

const resetGame = () => {
  turnO = true;
  count = 0;
  enableBoxes();
  msgContainer.classList.add("hide");
  currentPlayerDisplay.innerText = `${playerO}'s Turn (O)`;
};

const enableBoxes = () => {
  boxes.forEach(box => {
    box.disabled = false;
    box.innerText = "";
    box.classList.remove("win", "x-player", "o-player");
  });
};

const disableBoxes = () => {
  boxes.forEach(box => (box.disabled = true));
};

const updateScoreboard = () => {
  scoreXDisplay.innerText = scoreX;
  scoreODisplay.innerText = scoreO;
};

const showWinner = winner => {
  if (winner === "X") scoreX++;
  else scoreO++;

  updateScoreboard();

  msg.innerText = ` Congratulations, ${
    winner === "X" ? playerX : playerO
  } Wins!`;
  msgContainer.classList.remove("hide");
  disableBoxes();
};

const gameDraw = () => {
  msg.innerText = " It's a Draw!";
  msgContainer.classList.remove("hide");
  disableBoxes();
};

boxes.forEach(box => {
  box.addEventListener("click", () => {
    if (turnO) {
      box.innerText = "O";
      box.classList.add("o-player");
    } else {
      box.innerText = "X";
      box.classList.add("x-player");
    }
    box.disabled = true;
    count++;

    if (checkWinner()) return;

    if (count === 9) {
      gameDraw();
    } else {
      turnO = !turnO;
      currentPlayerDisplay.innerText = turnO
        ? `${playerO}'s Turn (O)`
        : `${playerX}'s Turn (X)`;
    }
  });
});

const checkWinner = () => {
  for (let pattern of winPatterns) {
    let [a, b, c] = pattern;
    if (
      boxes[a].innerText &&
      boxes[a].innerText === boxes[b].innerText &&
      boxes[a].innerText === boxes[c].innerText
    ) {
      let winnerClass =
        boxes[a].innerText === "X" ? "x-player" : "o-player";
      boxes[a].classList.add("win", winnerClass);
      boxes[b].classList.add("win", winnerClass);
      boxes[c].classList.add("win", winnerClass);

      showWinner(boxes[a].innerText);
      return true;
    }
  }
  return false;
};

newGameBtn.addEventListener("click", resetGame);
resetBtn.addEventListener("click", resetGame);

currentPlayerDisplay.innerText = `${playerO}'s Turn (O)`;
updateScoreboard();
