import pygame
import random

class SnakeGame:
    def __init__(self, screenWidth = 300, screenHeight = 300):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.scoreFont = pygame.font.SysFont('Arial', 20)
        self.startingMessageFont = pygame.font.SysFont('Arial', 20)
        self.gameOverMessageFont = pygame.font.SysFont('Arial', 40)
        self.tileWidth = screenWidth // 20
        self.tileHeight = screenHeight // 20
        self.snake = pygame.Rect(screenWidth // 2 - (self.tileWidth * 3), screenHeight // 2, self.tileWidth, self.tileHeight)
        self.apple = pygame.Rect(screenWidth // 2 + (self.tileWidth * 3), screenHeight // 2, self.tileWidth, self.tileHeight)
        self.score = 0
        self.highScore = 0
        self.snakeLength = 3
        self.positions = []
        self.direction = 'east'
        self.gameRunning = True
        self.gameStarted = False
        self.gameEnded = False
        self.cooldowns = {}

        for x in range(self.snakeLength - 1, -1, -1):
            self.positions.append((self.snake.topleft[0] - (x * self.tileWidth), self.snake.topleft[1]))

    def newGame(self):
        self.gameEnded = False
        self.gameStarted = False
        self.snakeLength = 3
        self.snake = pygame.Rect(self.screenWidth // 2 - (self.tileWidth * 3), self.screenHeight // 2, self.tileWidth, self.tileHeight)
        self.apple = pygame.Rect(self.screenWidth // 2 + (self.tileWidth * 3), self.screenHeight // 2, self.tileWidth, self.tileHeight)
        self.positions = []
        for x in range(self.snakeLength - 1, -1, -1):
            self.positions.append((self.snake.topleft[0] - (x * self.tileWidth), self.snake.topleft[1]))
        if self.score > self.highScore:
            self.highScore = self.score
        self.score = 0
        self.direction = 'east'
    
    def getOppositeDirection(self, direction):
        dict = {'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east'}
        return dict[direction]

    def getAppleRandomLocation(self):
        location = ()
        while not location and location not in self.positions:
            location = (random.randint(0, (self.screenWidth - self.tileWidth) // self.tileWidth) * self.tileWidth, random.randint(0, (self.screenHeight - self.tileHeight) // self.tileHeight) * self.tileHeight)
        return location

    def drawInnerBorder(self, rect, colour):
        thickness = 2
        innerRect = pygame.Rect(rect.x + thickness, rect.y + thickness, rect.width - thickness, rect.height - thickness)
        pygame.draw.rect(self.screen, colour, innerRect)

    def execute(self):
        while self.gameRunning:
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            self.screen.fill((0, 0, 0))
            scoreText = self.scoreFont.render('{:02}'.format(self.score), False, (255, 255, 255))
            highScoreText = self.scoreFont.render('{:02}'.format(self.highScore), False, (255, 255, 255))
            startingMessageText = self.startingMessageFont.render('Press any key to begin!', False, (255, 255, 255))
            gameOverText = self.gameOverMessageFont.render('Game Over!', False, (255, 255, 255))
            scoreRect = scoreText.get_rect(topleft=(5, 5))
            highScoreRect = highScoreText.get_rect(topleft=(40, 5))
            startingMessageRect = startingMessageText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            gameOverTextRect = gameOverText.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
            self.screen.blit(scoreText, scoreRect)
            self.screen.blit(highScoreText, highScoreRect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.snake)
            pygame.draw.rect(self.screen, (0, 0, 0), self.apple)
            self.drawInnerBorder(self.snake, (100, 200, 75))
            self.drawInnerBorder(self.apple, (250, 25, 25))
            
            for x in range(1, self.snakeLength):
                lastIndex = len(self.positions) - 1
                rect = pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.positions[lastIndex - x][0], self.positions[lastIndex - x][1], self.tileWidth, self.tileHeight))
                self.drawInnerBorder(rect, (100, 200, 75))

            for cooldownName in self.cooldowns:
                if self.cooldowns[cooldownName] > 0:
                    self.cooldowns[cooldownName] -= 1
            
            if event.type == pygame.QUIT:
                self.gameRunning = False
            if not self.gameStarted:
                self.screen.blit(startingMessageText, startingMessageRect)
                if True in keys:
                    self.gameStarted = True
            elif self.gameEnded:
                self.screen.blit(gameOverText, gameOverTextRect)
                if self.cooldowns['gameEnded'] <= 0:
                    self.newGame()
            else:
                if event.type == pygame.QUIT:
                    self.gameRunning = False
                if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.getOppositeDirection(self.direction) != 'north':
                    self.direction = 'north'
                elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.getOppositeDirection(self.direction) != 'west':
                    self.direction = 'west'
                elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.getOppositeDirection(self.direction) != 'south':
                    self.direction = 'south'
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.getOppositeDirection(self.direction) != 'east':
                    self.direction = 'east'

                if not self.cooldowns.get('movement') or self.cooldowns['movement'] <= 0:
                    seconds = 0.1
                    self.cooldowns['movement'] = self.fps * seconds
                    if self.direction == 'north':
                        if self.snake.top > 0:
                            self.snake.move_ip(0, -self.tileHeight)
                    elif self.direction == 'east':
                        if self.snake.right < self.screenWidth:
                            self.snake.move_ip(self.tileWidth, 0)
                    elif self.direction == 'south':
                        if self.snake.bottom < self.screenHeight:
                            self.snake.move_ip(0, self.tileHeight)
                    elif self.direction == 'west':
                        if self.snake.left > 0:
                            self.snake.move_ip(-self.tileWidth, 0)

                    if self.snake.topleft == self.apple.topleft:
                        self.snakeLength += 1
                        self.score += 1
                        self.apple.topleft = self.getAppleRandomLocation()
                        # self.fps += 1
                    if self.snake.topleft in self.positions[-self.snakeLength:] or self.snake.top < 0 or self.snake.right > self.screenWidth or self.snake.bottom > self.screenHeight or self.snake.left < 0:
                        self.gameEnded = True
                        seconds = 5
                        self.cooldowns['gameEnded'] = self.fps * seconds
                    else:
                        self.positions.append((self.snake.x, self.snake.y))
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

if __name__ == '__main__':
    game = SnakeGame()
    game.execute()