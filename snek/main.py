import pygame
import random
from api import RecipeAPI  # Import the RecipeAPI class

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Set colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        self.yellow = (255, 255, 0)

        # Set display dimensions
        self.width = 600
        self.height = 400
        self.dis = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        # Game settings
        self.snake_block = 10
        self.snake_speed = 8

        # Set clock
        self.clock = pygame.time.Clock()

        # Font styles
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.recipe_font = pygame.font.SysFont("arial", 16)

        # Initialize Recipe API
        self.recipe_api = RecipeAPI()  # Create an instance of RecipeAPI

    def show_recipe(self, title, full_content):
        self.dis.fill(self.blue)
        title_text = self.recipe_font.render(title, True, self.white)
        self.dis.blit(title_text, [50, 50])  # Display the title at the top

        lines = full_content.strip().split('\n')
        y_offset = 80  # Adjust y_offset to avoid overlap with title
        for line in lines:
            text = self.recipe_font.render(line, True, self.white)
            self.dis.blit(text, [50, y_offset])
            y_offset += 20

        # Add continue instruction
        continue_text = self.font_style.render("Press SPACE to continue", True, self.yellow)
        self.dis.blit(continue_text, [self.width / 4, self.height - 50])
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False


    def your_score(self, score):
        value = self.score_font.render("Score: " + str(score), True, self.white)
        self.dis.blit(value, [0, 0])

    def our_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], self.snake_block, self.snake_block])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.width / 6, self.height / 3])

    def spawn_food(self, snake_list):
        while True:
            foodx = round(random.randrange(self.snake_block, self.width - self.snake_block*2) / 10.0) * 10.0
            foody = round(random.randrange(self.snake_block, self.height - self.snake_block*2) / 10.0) * 10.0
            if [foodx, foody] not in snake_list:
                return foodx, foody

    def teleport_snake(self, snake_list):
        """Teleport the snake to a random position within the game area."""
        x = round(random.randrange(self.snake_block, self.width - self.snake_block*2) / 10.0) * 10.0
        y = round(random.randrange(self.snake_block, self.height - self.snake_block*2) / 10.0) * 10.0
        snake_list[0] = [x, y]  # Teleport the snake's head
        return x, y

    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = self.width // 2
        y1 = self.height // 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1
        foods_eaten = 0  # Track foods eaten

        foodx, foody = self.spawn_food(snake_list)

        teleport_timer = pygame.time.get_ticks()  # Timer for teleportation

        while not game_over:
            while game_close:
                self.dis.fill(self.blue)
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.your_score(length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()
                            return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change != self.snake_block:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change != -self.snake_block:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change != self.snake_block:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change != self.snake_block:
                        y1_change = self.snake_block
                        x1_change = 0

            # Update snake position
            x1 += x1_change
            y1 += y1_change

            # Teleport snake every 3 seconds
            current_time = pygame.time.get_ticks()
            if current_time - teleport_timer > 3000:
                x1, y1 = self.teleport_snake(snake_list)
                teleport_timer = current_time  # Reset the timer

            # Check boundaries
            if x1 >= self.width - self.snake_block or x1 < 0 or y1 >= self.height - self.snake_block or y1 < 0:
                game_close = True

            self.dis.fill(self.blue)

            # Draw food
            pygame.draw.rect(self.dis, self.green, [foodx, foody, self.snake_block, self.snake_block])

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            self.our_snake(snake_list)
            self.your_score(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx, foody = self.spawn_food(snake_list)
                length_of_snake += 1
                foods_eaten += 1
                
                # Fetch and show a random recipe after each food piece is eaten
                title, full_content = self.recipe_api.get_random_recipe()  # Get a random recipe
                self.show_recipe(title, full_content)  # Show the recipe

                if (length_of_snake - 1) % 5 == 0 and self.snake_speed < 15:
                    self.snake_speed += 1

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()

# Create and start the game
if __name__ == "__main__":
    game = SnakeGame()
    game.gameLoop()
