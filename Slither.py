import pygame
import random

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SNAKE_SPEED = 7
INITIAL_LENGTH = 3
MAX_FOOD_RATIO = 0.15  # 15% do mapa pode ter comida

# Cores
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Inicializar o pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Classe da cobra
class Snake:
    def __init__(self, color, name, is_bot=False):
        start_x, start_y = random.randint(5, WIDTH // GRID_SIZE - 5) * GRID_SIZE, random.randint(5, HEIGHT // GRID_SIZE - 5) * GRID_SIZE
        self.body = [(start_x - i * GRID_SIZE, start_y) for i in range(INITIAL_LENGTH)]
        self.direction = (GRID_SIZE, 0)
        self.growing = False
        self.color = color
        self.is_bot = is_bot
        self.dead = False
        self.name = name
    
    def move(self):
        if self.dead:
            return
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def check_collision(self, other_snakes):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        for snake in other_snakes:
            if self != snake and not snake.dead:
                if self.body[0] in snake.body:
                    return True
        return False
    
    def draw(self, is_leader):
        for i, segment in enumerate(self.body):
            color = GOLD if is_leader and i == 0 else self.color
            pygame.draw.rect(screen, color, (*segment, GRID_SIZE, GRID_SIZE))

    def auto_move(self, food_positions):
        if self.is_bot and not self.dead:
            if food_positions:
                target = min(food_positions, key=lambda pos: abs(pos[0] - self.body[0][0]) + abs(pos[1] - self.body[0][1]))
                dx = target[0] - self.body[0][0]
                dy = target[1] - self.body[0][1]
                if abs(dx) > abs(dy):
                    self.direction = (GRID_SIZE if dx > 0 else -GRID_SIZE, 0)
                else:
                    self.direction = (0, GRID_SIZE if dy > 0 else -GRID_SIZE)

# Classe da comida
class Food:
    def __init__(self, count=5):
        self.positions = [self.random_position() for _ in range(count)]
    
    def random_position(self):
        return (random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE,
                random.randint(0, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE)
    
    def regenerate(self):
        self.positions.append(self.random_position())
        self.limit_food()
    
    def limit_food(self):
        max_food = int((WIDTH // GRID_SIZE) * (HEIGHT // GRID_SIZE) * MAX_FOOD_RATIO)
        if len(self.positions) > max_food:
            self.positions = random.sample(self.positions, max_food)
    
    def draw(self):
        for pos in self.positions:
            pygame.draw.rect(screen, RED, (*pos, GRID_SIZE, GRID_SIZE))

# Função para desenhar o ranking
def draw_ranking(snakes):
    ranking = sorted(snakes, key=lambda s: len(s.body), reverse=True)
    y_offset = 50
    for i, snake in enumerate(ranking):
        text = font.render(f"{i+1}. {snake.name}: {len(snake.body)}", True, WHITE)
        screen.blit(text, (WIDTH + 20, y_offset))
        y_offset += 30
    return ranking[0] if ranking else None

# Função principal
def main():
    player = Snake(GREEN, "Player")
    bots = [Snake(BLUE, f"Bot {i+1}", is_bot=True) for i in range(2)]
    food = Food()
    snakes = [player] + bots
    running = True
    
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.direction != (0, GRID_SIZE):
                    player.direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and player.direction != (0, -GRID_SIZE):
                    player.direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and player.direction != (GRID_SIZE, 0):
                    player.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and player.direction != (-GRID_SIZE, 0):
                    player.direction = (GRID_SIZE, 0)
        
        for snake in snakes:
            if not snake.dead:
                snake.move()
                if snake.check_collision(snakes):
                    if snake == player:
                        running = False
                    else:
                        snake.dead = True
                        for i, seg in enumerate(snake.body):
                            if i % 2 == 0:
                                food.positions.append(seg)
                        bots.remove(snake)
                        bots.append(Snake(BLUE, f"Bot {len(bots) + 1}", is_bot=True))
                        snakes = [player] + bots
                if snake.body[0] in food.positions:
                    snake.grow()
                    food.positions.remove(snake.body[0])
                    food.regenerate()
        
        food.limit_food()
        
        for bot in bots:
            bot.auto_move(food.positions)
        
        leader = draw_ranking(snakes)
        
        for snake in snakes:
            snake.draw(snake == leader)
        food.draw()
        pygame.display.flip()
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()

if __name__ == "__main__":
    main()
