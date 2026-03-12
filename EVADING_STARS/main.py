import pygame
from random import randint
from sys import exit


class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)) # Create the visual surface
        self.image.fill((255, 255, 255)) # Color it white

        self.rect = self.image.get_rect(topleft=(x, y))

    def key_move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and self.rect.left - PLAYER_SPEED > 0 :  # left
            self.rect.left -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT] and self.rect.right + PLAYER_SPEED < WIDTH:  # right
            self.rect.left += PLAYER_SPEED
        if keys_pressed[pygame.K_UP] and self.rect.top - PLAYER_SPEED > 0:  # up
            self.rect.top -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom + PLAYER_SPEED < HEIGHT:  # down
            self.rect.top += PLAYER_SPEED

    # get mouse position and set player center to mouse position
    def mouse_move(self):                                       # IMPROVE THIS LATER
        if pygame.mouse.get_pressed()[0] :  # left mouse button              
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # self.rect.center = (mouse_x, mouse_y)

            mouse_x, mouse_y = pygame.mouse.get_pos()

        # 2. Set "Smoothness" (0.1 = 10% of the distance covered per frame)
        # Lower is smoother/slower, higher is snappier.
            lerp_factor = 0.15 

        # 3. Calculate the new center using the LERP formula
            new_x = self.rect.centerx + (mouse_x - self.rect.centerx) * lerp_factor
            new_y = self.rect.centery + (mouse_y - self.rect.centery) * lerp_factor

        # 4. Apply the position
            self.rect.center = (new_x, new_y)

        # 5. Boundary Checking (keeps player on screen)
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > WIDTH: self.rect.right = WIDTH
            if self.rect.top < 0: self.rect.top = 0
            if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

    def update(self):
        self.key_move()
        self.mouse_move()

class Star(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.width = STAR_WIDTH
        self.height = STAR_HEIGHT

        self.image = pygame.Surface((STAR_WIDTH, STAR_HEIGHT))
        self.image.fill((255, 255, 0)) # Color it yellow

        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        global STAR_SPEED
        self.rect.y += STAR_SPEED  # move downwards

    def update(self):
        self.move()

pygame.init()

# welcome and game music flags
game_playing : bool = False
welcome_playing : bool = False

font = pygame.font.Font("font/Pixeltype.ttf", 36)

# window dimensions and setup
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR EVADER")

# background image
BG = pygame.transform.scale(pygame.image.load("graphics/space.jpg"), WIN.get_size())

# intro screen
intro_main_rect_width = 400
intro_main_rect_height = 300

intro_main_rect = pygame.Rect(WIDTH//2-intro_main_rect_width//2, HEIGHT//2-intro_main_rect_height//2, intro_main_rect_width, intro_main_rect_height)

intro_header_surf = font.render("Welcome to Star Evader!", True, (255, 255, 255))   
intro_header_rect = intro_header_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

intro_text = font.render("Press SPACE to Start", True, (255, 255, 255))
intro_rect = intro_text.get_rect(center=(intro_main_rect.x + intro_main_rect.width // 2, intro_main_rect.y + intro_main_rect.height - 30))

#  player 
PLAYER_SPEED = 5
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

player = pygame.sprite.GroupSingle()
player.add(Player(randint(0, WIDTH-PLAYER_WIDTH), HEIGHT-PLAYER_HEIGHT))

# obstacle
STAR_SPEED = 5
STAR_WIDTH, STAR_HEIGHT = 10, 10
stars = pygame.sprite.Group()

spawn_star_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_star_event, difficulty:= 1000)  # spawn  stars 

difficulty_increase_event = pygame.USEREVENT + 2
pygame.time.set_timer(difficulty_increase_event, 5000)  # increase difficulty every

difficulty_index = 0
difficulty_levels = [1000, 800, 600, 400, 200]

clock = pygame.time.Clock()

def main():
    global game_playing, welcome_playing
    
    game_active = False

    pygame.mouse.set_visible(False)

    start_time = 0
    
    score = 0
    high_score = 0

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if game_active:

                if event.type == spawn_star_event:
                    for _ in range(3):  # spawn 3 stars at a time
                        stars.add(Star(randint(0, WIDTH-STAR_WIDTH), -STAR_HEIGHT))  # spawn above the screen

                if event.type == difficulty_increase_event:  update_difficulty()
            else:
                

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    reset()
                    game_active = True
                    start_time = pygame.time.get_ticks() // 1000  # get current time in seconds
                    
        
        if game_active:

            if not game_playing:
                # switch tracks
                pygame.mixer.music.load("audio/game.mp3")
                pygame.mixer.music.play(loops=-1)
                game_playing    = True
                welcome_playing = False

                pygame.mouse.set_visible(False)

            draw()

            game_active = collision_check()

            score = display_score(start_time)
            if score > high_score : high_score = score

        else:
            if not welcome_playing:
                pygame.mixer.music.load("audio/welcome.mp3")
                pygame.mixer.music.play(loops=-1)
                welcome_playing = True
                game_playing    = False

                pygame.mouse.set_visible(True)

            draw_intro()  
            draw_welcome_scores(score, high_score)
            
        pygame.display.update()

def draw():
    WIN.blit(BG, (0, 0))

    player.update()
    player.draw(WIN)

    stars.update()
    stars.draw(WIN)

def draw_intro():
        
        pygame.draw.rect(WIN, (173, 216, 230), intro_main_rect)  # black background for intro

        WIN.blit(intro_header_surf, intro_header_rect)
        WIN.blit(intro_text, intro_rect)


def collision_check():
    if pygame.sprite.spritecollide(player.sprite, stars, False):
        return False
    return True
    

def reset():

    player.sprite.rect.bottomleft = (WIDTH//2  - PLAYER_WIDTH//2, HEIGHT)
    stars.empty()
    reset_difficulty() 

def update_difficulty():

    global difficulty_index, difficulty

    if difficulty_index < len(difficulty_levels) - 1:
        difficulty_index += 1
        difficulty = difficulty_levels[difficulty_index]
        pygame.time.set_timer(spawn_star_event, difficulty)


def reset_difficulty():

    global difficulty_index, difficulty

    difficulty_index = 0
    difficulty = difficulty_levels[difficulty_index]
    pygame.time.set_timer(spawn_star_event, difficulty)

def display_score(start_time):
    current_time = pygame.time.get_ticks() // 1000  # get current time in seconds
    score = current_time - start_time

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surf.get_rect(topleft=(10, 10))
    WIN.blit(score_surf, score_rect)

    return score

def draw_welcome_scores(score, high_score):
    # pre score
    pre_score_surf = font.render(f"Score: {score}",  False, (100, 100, 100))
    pre_score_rect = pre_score_surf.get_rect(center = (WIDTH // 2,  HEIGHT // 2 + 20))
    
    # high score 
    high_score_surf = font.render(f"High Score: {high_score}", False, (100, 100, 100))
    high_score_rect = high_score_surf.get_rect(center = (WIDTH // 2,  HEIGHT // 2 + 40))
    
    
    WIN.blit(pre_score_surf, pre_score_rect)
    WIN.blit(high_score_surf, high_score_rect)

if __name__ == "__main__":
    main()