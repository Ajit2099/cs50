import pygame
from sys import exit
from random import randint, choices

class Player(pygame.sprite.Sprite):

    gravity : int = 1
    velocity : int = 0

    def __init__(self):
        super().__init__()

        self.walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        self.walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()

        self.walk = [self.walk_1, self.walk_2]
        self.index = 0

        self.jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom = (300, GROUND_y))

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.7)
    
    def apply_gravity(self):
        self.velocity += self.gravity
        self.rect.bottom += self.velocity
        
        if self.rect.bottom >= GROUND_y: 
            self.rect.bottom = GROUND_y
            self.velocity = 0

    def animation(self):
        if self.rect.bottom < GROUND_y:
            self.image = self.jump

        else:
            self.index += 0.1
            if self.index >= len(self.walk):   self.index = 0
            self.image: pygame.Surface = self.walk[int(self.index)]

    def update(self):
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()

        if type == "snail":
            self.frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            self.frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

            self.frames = [self.frame_1, self.frame_2]

            y_pos = GROUND_y

            

        else:
            self.frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            self.frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()

            self.frames = [self.frame_1, self.frame_2]

            y_pos = 400

        self.index = 0
        self.image: pygame.Surface = self.frames[self.index]
        self.rect = self.image.get_rect(bottomleft = (randint(WIN_WIDTH + 300,WIN_WIDTH + 400 ), y_pos))

        self.speed = OBSTACLE_SPEED

    def movement(self):
        self.rect.left -= self.speed
        if self.rect.right < 0:    self.kill()

    def update_speed(self, n):
        self.speed += n

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.frames):   self.index = 0
        self.image: pygame.Surface = self.frames[int(self.index)]

    def update(self):
        self.movement()
        self.animation()

pygame.init()

# welcome and game music flags
game_playing : bool = False
welcome_playing : bool = False




# clock
clock = pygame.time.Clock()

WIN_WIDTH : int = 1000
WIN_HEIGHT : int =  600

#font 
font = pygame.font.Font("font/Pixeltype.ttf", 50)

# setting display
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# setting game titlt 
pygame.display.set_caption("DINO GAME")

# welcome screen heading
welcome_header_surf = font.render("DINO GAME", False, (90, 90, 90))
welcome_header_rect = welcome_header_surf.get_rect(center = (WIN_WIDTH//2, 50))

# welcome intruction 
welcome_instruc_surf = font.render("Press Space Bar to Play", False, (70,70,70))
welcome_instruc_rect = welcome_instruc_surf.get_rect(center = (WIN_WIDTH//2, 500)) 

# setting sky background
SKY = pygame.image.load("graphics/background_img.jpg").convert()
SKY = pygame.transform.scale(SKY, WIN.get_size())

# setting ground image
GROUND_y : int = 500

GROUND = pygame.image.load("graphics/ground_img.png").convert()
GROUND = pygame.transform.scale(GROUND, (WIN_WIDTH, WIN_HEIGHT - GROUND_y))

# welcome image
WELCOME = pygame.image.load("graphics/welcome_img.webp").convert()
WELCOME = pygame.transform.scale(WELCOME, WIN.get_size())

#   GROUPS

    # player
player = pygame.sprite.GroupSingle()
player.add(Player())

    # obstacles
obstacle_group = pygame.sprite.Group()

# # welcome scren player 
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 3)
player_stand_rect = player_stand.get_rect(center = (WIN_WIDTH//2, WIN_HEIGHT//2))


# creating spawn event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT,  difficulty := 2000)

# difficulty levels in milliseconds
difficulties = [2000, 1500, 1000, 500]
difficulty_index: int = 0

# speed and increment for obstacles
OBSTACLE_SPEED : int = 6
SPEED_INCREMENT = 3

# creating snail animation event
SNAIL_ANIM_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SNAIL_ANIM_EVENT, 500)

# creating fly animation event
FLY_ANIM_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(FLY_ANIM_EVENT, 300)

#  creating difficulty increase event
DIFFICULTY_INCREASE_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(DIFFICULTY_INCREASE_EVENT, 10000)  # Increase difficulty every 10 seconds

def main():
    global welcome_playing, game_playing, difficulty, difficulty_index, difficulties
    
    start_time = 0
    
    score = 0
    high_score = 0
    
    game_active : bool = False
    run : bool = True 

     
    
    while run:
        clock.tick(60)
        
        #  EVENTS
        for event in pygame.event.get():
            
            # quit 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if game_active:

                # Handle jumps on key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if player.sprite.rect.bottom >= GROUND_y : 
                            player.sprite.velocity = - 20
                            player.sprite.jump_sound.play()

                # Handle mouse click (left button) on press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and player.sprite.rect.collidepoint(event.pos) and player.sprite.rect.bottom >= GROUND_y:
                        player.sprite.velocity = -20
                        player.sprite.jump_sound.play()

                if event.type == SPAWN_EVENT:
                    obstacle_group.add(Obstacle(choices(["snail", "fly"], weights = [70, 30], k= 1)[0]))

                if event.type == DIFFICULTY_INCREASE_EVENT:
                    set_difficulty()   
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True  
                    start_time = pygame.time.get_ticks() // 1000
                
        
        if game_active:

            if not game_playing:
                # switch tracks
                pygame.mixer.music.load("audio/game.mp3")
                pygame.mixer.music.play(loops=-1)
                game_playing    = True
                welcome_playing = False
           
            

            draw()

            player.draw(WIN)
            player.update()

            obstacle_group.draw(WIN)
            obstacle_group.update()
            
            
            
            game_active =  collision_sprite()

            # assigning score and updating high score 
            score = display_score(start_time)
            if score > high_score : high_score = score 
 
        
        else:

            if not welcome_playing:
                pygame.mixer.music.load("audio/welcome.mp3")
                pygame.mixer.music.play(loops=-1)
                welcome_playing = True
                game_playing    = False
           
            
            reset_game()
            
            
            draw_welcome()
            
            draw_welcome_scores(score, high_score)
            
            
        pygame.display.update()
            
            
        
def draw():
    # sky
    WIN.blit(SKY, (0, 0))
    # ground
    WIN.blit(GROUND, (0, GROUND_y))
    # # player
    # WIN.blit(player_surf, player_rect) 
    
    
def draw_welcome():
    # background
    WIN.blit(WELCOME, (0, 0))
    
    # header 
    WIN.blit(welcome_header_surf, welcome_header_rect)
    
    # player
    WIN.blit(player_stand, player_stand_rect)
    
    # instruction 
    WIN.blit(welcome_instruc_surf, welcome_instruc_rect)
    

def display_score(start_time):
    current_time = pygame.time.get_ticks() // 1000    - start_time
    
    score_surf = font.render(f"Score: {current_time}", False,  (64 ,64 ,64))
    score_rect = score_surf.get_rect(center = (WIN_WIDTH // 2, 20))
    
    WIN.blit(score_surf, score_rect)
    
    return current_time
    
    
    
def draw_welcome_scores(score, high_score):
    # pre score
    pre_score_surf = font.render(f"Score: {score}",  False, (100, 100, 100))
    pre_score_rect = pre_score_surf.get_rect(center = (WIN_WIDTH - 150,  30))
    
    # high score 
    high_score_surf = font.render(f"High Score: {high_score}", False, (100, 100, 100))
    high_score_rect = high_score_surf.get_rect(center = (WIN_WIDTH - 150, 65))
    
    
    WIN.blit(pre_score_surf, pre_score_rect)
    WIN.blit(high_score_surf, high_score_rect)


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True  


def set_difficulty():
    global difficulty, difficulty_index, SPEED_INCREMENT, OBSTACLE_SPEED

    if difficulty_index < len(difficulties)-1:
        difficulty_index += 1
        difficulty = difficulties[difficulty_index]

        pygame.time.set_timer(SPAWN_EVENT, difficulty)

        OBSTACLE_SPEED += SPEED_INCREMENT

        for ob in obstacle_group:
            ob.speed = OBSTACLE_SPEED

def reset_game():
    global difficulty_index, difficulty

    difficulty_index = 0
    difficulty = difficulties[0]

    pygame.time.set_timer(SPAWN_EVENT, difficulty)

    player.sprite.rect.midbottom = (300, GROUND_y)
    player.sprite.velocity = 0

if __name__ == "__main__":
    main()