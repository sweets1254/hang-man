import tkinter
import random

# Define the tile size
TILE_SIZE = 35

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Initialize global variables
two_player = False
game_started = False
game_over = False

snake1 = None
snake2 = None
food = None
velocityX1, velocityY1 = 0, 0
velocityX2, velocityY2 = 0, 0
snake_body1 = []
snake_body2 = []
score1 = 0
score2 = 0

def init_game():
    global snake1, snake2, food, velocityX1, velocityY1, velocityX2, velocityY2, snake_body1, snake_body2, game_over, score1, score2
    snake1 = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    if two_player:
        snake2 = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    else:
        snake2 = None
    food = Tile(TILE_SIZE * 15, TILE_SIZE * 15)
    velocityX1 = 0
    velocityY1 = 0
    velocityX2 = 0
    velocityY2 = 0
    snake_body1 = []
    snake_body2 = []
    game_over = False
    score1 = 0
    score2 = 0

def start_game(event):
    global two_player, game_started, game_over
    if not game_started:
        if event.char == '1':
            two_player = False
            game_started = True
            init_game()
        elif event.char == '2':
            two_player = True
            game_started = True
            init_game()
    elif game_over and event.keysym == 'Return':
        game_started = False
        game_over = False
        init_game()

def change_direction(e):
    global velocityX1, velocityY1, velocityX2, velocityY2, game_over

    if game_over:
        return

    if e.keysym == "w" and velocityY1 != 1:
        velocityX1 = 0
        velocityY1 = -1
    elif e.keysym == "s" and velocityY1 != -1:
        velocityX1 = 0
        velocityY1 = 1
    elif e.keysym == "a" and velocityX1 != 1:
        velocityX1 = -1
        velocityY1 = 0
    elif e.keysym == "d" and velocityX1 != -1:
        velocityX1 = 1
        velocityY1 = 0

    if two_player:
        if e.keysym == "Up" and velocityY2 != 1:
            velocityX2 = 0
            velocityY2 = -1
        elif e.keysym == "Down" and velocityY2 != -1:
            velocityX2 = 0
            velocityY2 = 1
        elif e.keysym == "Left" and velocityX2 != 1:
            velocityX2 = -1
            velocityY2 = 0
        elif e.keysym == "Right" and velocityX2 != -1:
            velocityX2 = 1
            velocityY2 = 0

def move():
    global snake1, snake2, food, snake_body1, snake_body2, game_over, score1, score2
    if game_over:
        return
    
    def move_snake(snake, velocityX, velocityY, snake_body, score):
        new_head = Tile(snake.x + velocityX * TILE_SIZE, snake.y + velocityY * TILE_SIZE)
        
        # Check for collisions with walls
        if new_head.x < 0 or new_head.x >= WINDOW_WIDTH or new_head.y < 0 or new_head.y >= WINDOW_HEIGHT:
            return True, score, snake_body
        
        # Check for collisions with itself
        for tile in snake_body:
            if new_head.x == tile.x and new_head.y == tile.y:
                return True, score, snake_body
        
        # Update the snake's body
        if len(snake_body) > 0:
            snake_body = [Tile(snake.x, snake.y)] + snake_body[:-1]



        # Check for collisions with food
        if new_head.x == food.x and new_head.y == food.y:
            snake_body.append(Tile(snake.x, snake.y))
            score += 1
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        
        snake.x = new_head.x
        snake.y = new_head.y

        return False, score, snake_body

    game_over1, score1, snake_body1 = move_snake(snake1, velocityX1, velocityY1, snake_body1, score1)
    
    if two_player:
        game_over2, score2, snake_body2 = move_snake(snake2, velocityX2, velocityY2, snake_body2, score2)
        game_over = game_over1 or game_over2
    else:
        game_over = game_over1

def draw_checkerboard():
    cols = (WINDOW_WIDTH // TILE_SIZE) + 1
    rows = (WINDOW_HEIGHT // TILE_SIZE) + 1

    for row in range(rows):
        for col in range(cols):
            color = 'white' if (row + col) % 2 == 0 else 'light gray'
            x1 = col * TILE_SIZE
            y1 = row * TILE_SIZE
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

def draw():
    global snake1, snake2, food, snake_body1, snake_body2, game_over, score1, score2, game_started
    if game_started and not game_over:
        move()

    canvas.delete("all")
    draw_checkerboard()

    if game_started:
        # Draw food
        canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='gold')

        # Draw snakes
        canvas.create_oval(snake1.x, snake1.y, snake1.x + TILE_SIZE, snake1.y + TILE_SIZE, fill='red')
        if two_player:
            canvas.create_oval(snake2.x, snake2.y, snake2.x + TILE_SIZE, snake2.y + TILE_SIZE, fill='blue')

        for tile in snake_body1:
            canvas.create_oval(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='red')

        if two_player:
            for tile in snake_body2:
                canvas.create_oval(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='blue')

        if game_over:
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text="Game Over", fill="red")
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, font="Arial 15", text=f"Player 1 Score: {score1}", fill="red")
            if two_player:
                canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60, font="Arial 15", text=f"Player 2 Score: {score2}", fill="blue")
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 90, font="Arial 15", text="Press Enter to Restart", fill="black")
    else:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, font="Arial 20", text="Choose Mode:", fill="black")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 10, font="Arial 15", text="Press 1 for Single Player", fill="black")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40, font="Arial 15", text="Press 2 for Two Players", fill="black")
    
    window.after(100, draw)

# Game window
window = tkinter.Tk()
window.title("Snake")
window.attributes('-fullscreen', True)
window.resizable(False, False)

# Calculate the rows and columns based on the fullscreen size
window.update_idletasks()
WINDOW_WIDTH = window.winfo_width()
WINDOW_HEIGHT = window.winfo_height()
COLS = WINDOW_WIDTH // TILE_SIZE
ROWS = WINDOW_HEIGHT // TILE_SIZE

canvas = tkinter.Canvas(window, bg="light blue", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()

window.bind("<KeyRelease>", change_direction)
window.bind("<KeyPress>", start_game)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))  # Exit fullscreen on 'Escape'
draw()
window.mainloop()
