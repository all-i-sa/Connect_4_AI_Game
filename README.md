# Connect 4 AI Game
---
This is a Connect 4 game that uses AI for the computer gameplay.  
It uses minimax with alpha–beta pruning and a Pygame UI.  
The player can choose between three difficulty levels: easy, medium, and hard.  
The game runs locally.
---
## Tech details
- Python
- Libraries:  
  - `pygame` for the UI  
  - Standard Python libraries like `math`, `random`
- AI: Minimax with alpha–beta pruning and a heuristic
---

## Files

- `main.py` – Launches the Pygame UI
- `ui.py` – Handles all UI builds, input, buttons, and main game loop
- `ai.py` – Minimax and alpha–beta pruning and the AI move selection
- `board.py` – Board representation and game logic like drop piece, check winner, etc.
- `constants.py` – Game settings such as rows, columns, piece IDs, difficulty depths
- `game.py` – Original text-based game loop used for testing and reference
- `main_menu.py` - Main menu interface
---

## How the AI Works

1. **Board Representation**  
   The board is a 6×7 grid stored as a 2D list  
   - `0` = empty  
   - `1` = human player  
   - `2` = AI

2. **Heuristic Evaluation**  
   The AI scores the board using windows of 4 cells (horizontal, vertical, diagonal).  
   scoring:

   ```python
   if piece_count == 4:
       score += 100
   elif piece_count == 3 and empty_count == 1:
       score += 5
   elif piece_count == 2 and empty_count == 2:
       score += 2

   if opponent_count == 3 and empty_count == 1:
       score -= 4
---
The AI rewards:  
- 4 in a row (high score)
- 3 in a row with an empty slot
- 2 in a row with two empties
The AI penalizes:
- situations where the opponent has 3 in a row and one empty
---
Center Preference for AI moves:
- counts how many AI pieces are in the center column and each center piece adds extra points to the score.
- AI prefers playing toward the middle of the board, since it is usually better because it allows more  
opportunities to get 4 in a row.
---
Minimax + Alpha–Beta Pruning:
-The AI assumes tries to maximize the score, and the human tries to minimize it.
- At each node, it simulates placing a piece, goes deeper until it hits a win/loss/draw state, or  
the depth limit.
- When the depth limit is reached, it uses score_position to evaluate the board.

Alpha–beta pruning is used to:
- Keep track of the best scores seen so far AND cut off branches that cannot improve the final decision.
---
Difficulty Levels (Search Depth):
- Easy: depth 1
- Medium: depth 3
- Hard: depth 5

The higher the depth means AI can see more moves into the future.

## How to Run

1. Clone the repository
2. Create and activate a virtual environment (optional but recommended)
3. Install dependencies
pip install pygame
4. Run the game
python main.py

### Game Controls
- Mousev/ pointer: move mouse left/right to select a column and the 
hover shows where your piece will drop)
- Click to drop your piece in that column
- Buttons: click Easy, Medium, or Hard at the top to change difficulty
- Keyboard: Key in 1 for easy, 2 for medium, 3 for hard

## Gameplay Summary from intial tests
- Increasing search depth made the AI much harder to beat.
- Response time stayed low and consistent for all three levels: Easy/Medium/Hard.
- The AI did favor the center, block most 3-in-a-row threats, and won more often than  
the human, especially on higher difficulty levels.

## Team

Bryan Alarcon, Allisa Warren, Minh Duc Ngo