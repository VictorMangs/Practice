import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Define the obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image = pygame.Surface((random.randint(20, 50), random.randint(20, 50)))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.speed = speed

    def reset_position(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-height, -self.rect.height)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.reset_position()

    def draw(self, screen):
        screen.blit(self.image, self.rect)



def new_game():
    # Create player object
    player = Player()

    # Create obstacles group
    obstacles = pygame.sprite.Group()
    initial_speed = 3
    obstacle_speed = initial_speed
    for _ in range(10):
        obstacle = Obstacle(obstacle_speed)
        obstacles.add(obstacle)

    # Set up the game clock
    clock = pygame.time.Clock()

    # Game over flag and message
    game_over = False
    font = pygame.font.Font(None, 36)

    # Scoring variables
    score = 0
    score_font = pygame.font.Font(None, 24)

    # Level variables
    level = 1
    level_font = pygame.font.Font(None, 24)

    # Speed increment variables
    speed_increment = 0.5
    speed_increment_interval = 5000  # milliseconds
    last_speed_increment_time = pygame.time.get_ticks()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key == pygame.K_SPACE:
                    # Restart the game
                    game_over = False
                    score = 0
                    level = 1

        if not game_over:
            screen.fill(BLACK)

            player.update()
            player.draw(screen)

            obstacles.update()
            obstacles.draw(screen)

            # Check for collisions
            if pygame.sprite.spritecollide(player, obstacles, False):
                game_over = True

            # Increase score based on time
            score += 1

            # Increase obstacle speed at regular intervals
            current_time = pygame.time.get_ticks()
            if current_time - last_speed_increment_time > speed_increment_interval:
                obstacle_speed += speed_increment
                last_speed_increment_time = current_time
                level += 1

            # Update obstacle speeds
            for obstacle in obstacles:
                obstacle.speed = obstacle_speed

            # Display score
            score_text = score_font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (10, 10))

            # Display level
            level_text = level_font.render("Level: " + str(level), True, WHITE)
            screen.blit(level_text, (10, 40))

            pygame.display.flip()
            clock.tick(60)
        else:
            # pygame.time.wait()

            player.rect.center = (width // 2, height // 2)
            obstacles.empty()
            
            obstacle_speed = initial_speed
            for _ in range(10):
                obstacle = Obstacle(obstacle_speed)
                while pygame.sprite.spritecollide(obstacle, obstacles, False) or pygame.sprite.collide_rect(player, obstacle):
                    obstacle.reset_position()
                obstacles.add(obstacle)

            # Display game over message and final score
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (width // 2 - 80, height // 2 - 18))
            score_text = font.render("Final Score: " + str(score), True, WHITE)
            screen.blit(score_text, (width // 2 - 100, height // 2 + 18))
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(restart_text, (width // 2 - 130, height // 2 + 54))
            pygame.display.flip()
            

    # Quit the game
    pygame.quit()

new_game()