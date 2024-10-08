import React, { useState, useEffect } from 'react';

const SnakeGame = () => {
  const [snake, setSnake] = useState([{ x: 10, y: 10 }, { x: 9, y: 10 }, { x: 8, y: 10 }]);
  const [direction, setDirection] = useState('RIGHT');
  const [food, setFood] = useState({ x: 15, y: 15 });
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      moveSnake();
    }, 100);

    return () => clearInterval(intervalId);
  }, [snake, direction]);

  const moveSnake = () => {
    const head = { ...snake[0] };
    switch (direction) {
      case 'UP':
        head.y -= 1;
        break;
      case 'DOWN':
        head.y += 1;
        break;
      case 'LEFT':
        head.x -= 1;
        break;
      case 'RIGHT':
        head.x += 1;
        break;
      default:
        break;
    }

    if (head.x < 0 || head.x > 20 || head.y < 0 || head.y > 20 || snake.some((bodyPart) => bodyPart.x === head.x && bodyPart.y === head.y)) {
      setGameOver(true);
    } else {
      setSnake([head, ...snake.slice(0, -1)]);
      if (head.x === food.x && head.y === food.y) {
        setScore((prevScore) => prevScore + 1);
        setFood({ x: Math.floor(Math.random() * 20), y: Math.floor(Math.random() * 20) });
        setSnake((prevSnake) => [...prevSnake, { x: prevSnake[prevSnake.length - 1].x, y: prevSnake[prevSnake.length - 1].y }]);
      }
    }
  };

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowUp':
        setDirection('UP');
        break;
      case 'ArrowDown':
        setDirection('DOWN');
        break;
      case 'ArrowLeft':
        setDirection('LEFT');
        break;
      case 'ArrowRight':
        setDirection('RIGHT');
        break;
      default:
        break;
    }
  };

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div>
      <h1>Snake Game</h1>
      <div style={{ width: '400px', height: '400px', border: '1px solid black', display: 'flex', flexWrap: 'wrap' }}>
        {Array(20)
          .fill(null)
          .map((_, y) =>
            Array(20)
              .fill(null)
              .map((_, x) => (
                <div
                  key={`${x}-${y}`}
                  style={{
                    width: '20px',
                    height: '20px',
                    backgroundColor:
                      snake.some((bodyPart) => bodyPart.x === x && bodyPart.y === y) ||
                      (x === food.x && y === food.y)
                        ? 'green'
                        : 'white',
                  }}
                />
              )),
          )}
      </div>
      <p>Score: {score}</p>
      {gameOver && <p>Game Over!</p>}
    </div>
  );
};

export default SnakeGame;