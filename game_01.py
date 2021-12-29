import pygame
import os  #  i am using this to join path name
pygame.font.init()
pygame.mixer.init()

# pygame.init()
#  never name you game file pygame
WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # creates window
pygame.display.set_caption("Space Invaders")

VELOCITY = 5
FPS = 60

BULLET_VEL = 7
MAX_BULLETS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)

SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT+1 #there are total 32 events in pygame... 24-32 are free for us to use pygame.USEREVENT assigns 24 number to us... by adding respective number we can get the desired event for use
RED_HIT = pygame.USEREVENT+2  #if error comes edit this add +2 instead here and +1 in upper

BORDER = pygame.Rect((WIDTH // 2 - 5), 0, 10, HEIGHT)  # arguments(x, y, width, height) and also the arguments of rect can only take integers in it so we use double slash to divide as it will give integer as output instead of the float 

HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)  # transforms the width of the spaceship that we are using
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))#yha pe we are telling the that the event that just happend right now is RED_HIT, ie we have successfully hit the red spaceship
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.pop()
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.pop()
    
    
def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and yellow.x + VELOCITY < BORDER.x - (
        yellow.width - 15
    ):  # RIGHT
        yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and yellow.y + VELOCITY > 15:  # UP
        yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + VELOCITY + 60 < HEIGHT:  # DOWN
        yellow.y += VELOCITY


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - (VELOCITY + 10) > BORDER.x:  # LEFT
        red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and red.x < WIDTH - (red.width - 10):  # RIGHT
        red.x += VELOCITY
    if key_pressed[pygame.K_UP] and red.y + VELOCITY > 15:  # UP
        red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and red.y + VELOCITY + 60 < HEIGHT:  # DOWN
        red.y += VELOCITY


def draw_window(red, yellow,red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    
    pygame.draw.rect(WIN, BLACK, BORDER)  # arguments(window, color, position)
    
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health),0,WHITE) 
            #edit antialias is turned to 0, what antialias does is
             # makes your lines which are diagonal look smooth
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health),0,WHITE )

    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))
    #red_health_text.getwidth() gets width of the text
    WIN.blit(
        YELLOW_SPACESHIP, (yellow.x, yellow.y)
    )  # we put the coordinates where we want our
    # spaceship to be
    # blit is use to pin stuff on screen like text or images, origin start from top left corner of the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)    
    
    pygame.display.update()  # updates the display

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()  #edit
    pygame.time.delay(5000) #5000 milliseconds or 5 seconds


def main():
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10
    
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # controls for the red spaceship
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()  # creates object to track time
    run = True
    while run:
        clock.tick(FPS)  # makes sure your code runs FPS times per second
        for event in pygame.event.get():  # all of the different events in game
            if event.type == pygame.QUIT:
                run = False    
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5) #-2 is to subtract height of bullet
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_l and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5) #-2 is to subtract height of bullet
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_text = " "
        if yellow_health <=0:
            winner_text = "RED WINS!"
                
        if red_health <=0:
            winner_text = "YELLOW WINS!"

        if winner_text != " ":
            draw_winner(winner_text)
            break

        # red.x += 1 #changes the x position of the red spaceship at 60 pixel per second as FPS = 60
        # print(yellow_bullets, red_bullets) 
        key_pressed = pygame.key.get_pressed()
        draw_window(red, yellow,red_bullets,yellow_bullets, red_health, yellow_health)
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
    main()


if __name__ == "__main__":
    main()