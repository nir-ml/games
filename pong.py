import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 12

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNING_SCORE = 10

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            if self.y > 0: #this limit stops the paddle from moving out of the window
                self.y -= self.VEL
        else:
            if self.y + self.height < HEIGHT: #this limit stops the paddle from moving out of the window
                self.y += self.VEL

    def move_left_left_paddle(self):
        if self.x - self.VEL >= 0:  # Check if the paddle is within the distance limit on the left
            self.x -= self.VEL

    def move_right_left_paddle(self):
        if self.x + self.width + self.VEL <= WIDTH // 2:  # Check if the paddle is within the distance limit on the right
            self.x += self.VEL

    def move_left_right_paddle(self):
        if self.x - self.VEL >= WIDTH // 2 + 1:  # Check if the paddle is within the distance limit on the left
            self.x -= self.VEL

    def move_right_right_paddle(self):
        if self.x + self.width + self.VEL <= WIDTH:  # Check if the paddle is within the distance limit on the right
            self.x += self.VEL


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__ (self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width()//2, 20))
    window.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(window)

    # dotted line separation in the middle of the window
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(window)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                #create angles of ball motion
                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                #create angles of ball motion
                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    elif keys[pygame.K_s]:
        left_paddle.move(up=False)
    elif keys[pygame.K_a]:  # Move the left paddle to the left
        left_paddle.move_left_left_paddle()
    elif keys[pygame.K_d]:  # Move the left paddle to the right
        left_paddle.move_right_left_paddle()

    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    elif keys[pygame.K_DOWN]:
        right_paddle.move(up=False)
    elif keys[pygame.K_LEFT]:  # Move the right paddle to the left
        right_paddle.move_left_right_paddle()
    elif keys[pygame.K_RIGHT]:  # Move the right paddle to the right
        right_paddle.move_right_right_paddle()
        

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width() // 2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()

