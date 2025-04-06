import pygame
import random
import os
import sys
from time import time
import mysql.connector
from Block import Block
from Player import Player
# Příprava DBS
# !!! UPRAV ŘÁDEK POD KOMENTÁŘEM PRO GLOBAL HIGH SCORE !!!
mydb = mysql.connector.connect(host="HOST", user="USERNAME", password="PASSWORD", database="DBNAME")
mycursor = mydb.cursor()
# Kontrola a vytvoření tabulky
mycursor.execute("CREATE TABLE IF NOT EXISTS FlappyBirdScores (id INT PRIMARY KEY AUTO_INCREMENT, unixtime INT, score INT)")
# Pygame init
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Věci pro generování a přípravu
WIDTH, HEIGHT = 400, 600
FPS = 60
GAP_SIZE = 150
PIPE_FREQUENCY = 2500  # v ms
GRAVITY = 0.5 
JUMP_STRENGTH = 10
PIPE_SPEED = 2

# Definice barev
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
GOLD = (255, 215, 0)

# Více příprav pro Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Definice fontů
font_small = pygame.font.SysFont('Arial', 24)
font_medium = pygame.font.SysFont('Arial', 36)
font_large = pygame.font.SysFont('Arial', 64)

# Fallback pro logo
def create_logo():
    logo = pygame.Surface((300, 100), pygame.SRCALPHA)
    pygame.draw.rect(logo, GOLD, (0, 0, 300, 100), border_radius=15)
    text = font_large.render("Flappy Bird", True, BLACK)
    logo.blit(text, (150 - text.get_width()//2, 50 - text.get_height()//2))
    return logo

# Obrázky + fallback
try:
    bg_image = pygame.image.load("background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = pygame.Surface((WIDTH, HEIGHT))
    bg_image.fill((135, 206, 235))  # Sky blue

try:
    logo_image = pygame.image.load("logo.png").convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (300, 100))
except:
    logo_image = create_logo()

# Audio + fallback
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
except:
    jump_sound = None

try:
    score_sound = pygame.mixer.Sound("score.wav")
except:
    score_sound = None

try:
    hit_sound = pygame.mixer.Sound("hit.wav")
except:
    hit_sound = None

# Renderování textu
def draw_text(text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

# Načtení lokálního highscore
def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0
def load_globalhighscore():
    globalhighscore = "0"
    mycursor.execute("SELECT MAX(score) FROM FlappyBirdScores")
    hs_result = mycursor.fetchall()
    for hs in hs_result:
        if hs == (None,):
            globalhighscore = "0"
        else:
            globalhighscore = str(hs[0])
    return globalhighscore
# Načtení globálního highscore
globalhighscore = load_globalhighscore()

# Uložení lokálního highscore
def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Uložení globálního highscore do DBS
def save_global(score):
    if score > int(globalhighscore):
        timenow = round(time())
        mycursor.execute("INSERT INTO FlappyBirdScores (unixtime, score) VALUES (%s, %s)", (timenow, score,))
        mydb.commit()

def game():
    player = Player(HEIGHT)
    all_sprites = pygame.sprite.Group(player)
    pipes = []
    # Proměnné pro hru
    score = 0
    highscore = load_highscore()
    globalhighscore = load_globalhighscore()
    game_over = False
    scroll_speed = PIPE_SPEED
    
    # Časovač pro generování trubek
    last_pipe = pygame.time.get_ticks()
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Reakce na klávesy a křížek
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                    if jump_sound: jump_sound.play()
                if event.key == pygame.K_SPACE and game_over:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                player.jump()
                if jump_sound: jump_sound.play()
        
        # Hlavní smyčka hry
        if not game_over:
            # Generování trubek
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipe_height = random.randint(100, HEIGHT - 100 - GAP_SIZE)
                new_pipe = Block(HEIGHT, WIDTH, pipe_height, GAP_SIZE, scroll_speed)
                pipes.append(new_pipe)
                last_pipe = time_now
            
            # Pohyb a gravitace hráče
            player.update()
            player.proc_grav(HEIGHT)
            
            # Pohyb trubek
            for pipe in pipes[:]:
                pipe.update()
                
                # Připsání bodů
                if pipe.score_point(player.rect):
                    score += pipe.points
                    if score_sound: score_sound.play()
                
                # Kolize s trubkami
                top_collision = player.rect.colliderect(pipe.rect_top)
                bottom_collision = player.rect.colliderect(pipe.rect_bottom)
                if (top_collision or bottom_collision) and not player.invincible:
                    if hit_sound: hit_sound.play()
                    game_over = True
                
                # Vymazání trubek mimo obrazovku
                if pipe.is_off_screen():
                    pipes.remove(pipe)
            
            # Ukončení hry při nárazu do země nebo stropu
            if player.rect.bottom >= HEIGHT or player.rect.top <= 0:
                if hit_sound: hit_sound.play()
                game_over = True
            
            # Zvýšení rychlosti v závislosti na skóre
            scroll_speed = PIPE_SPEED + score * 0.02
        else:
            # Uložení highscore lokálně
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            # Nahrání highscore na DBS
            if score > int(globalhighscore):
                
                globalhighscore = score
                save_global(globalhighscore)
        
        # Renderování obrazovky
        screen.blit(bg_image, (0, 0))
        
        for pipe in pipes:
            pipe.draw(screen)
        
        player.draw(screen)
        
        # Skórovací texty
        draw_text(f"Score: {score}", font_small, WHITE, WIDTH // 2, 50)
        draw_text(f"High Score: {highscore}", font_small, WHITE, WIDTH // 2, 100)
        draw_text(f"Global High Score: {globalhighscore}", font_small, WHITE, WIDTH // 2, 150)
        
        if game_over:
            # Konec hry
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            screen.blit(s, (0, 0))
            
            draw_text("GAME OVER", font_large, RED, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Final Score: {score}", font_medium, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text("Press SPACE to restart", font_small, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        
        pygame.display.flip()

def main_menu():
    highscore = load_highscore()
    
    while True:
        screen.blit(bg_image, (0, 0))
        
        # Renderování loga
        screen.blit(logo_image, (WIDTH // 2 - 150, 50))
        
        # Renderování textu
        draw_text(f"High Score: {highscore}", font_medium, WHITE, WIDTH // 2, 200)
        draw_text(f"Global High Score: {load_globalhighscore()}", font_medium, WHITE, WIDTH // 2, 250)
        
        # Renderování tlačítek
        start_rect = draw_text("START", font_medium, GREEN, WIDTH // 2, 350)
        quit_rect = draw_text("QUIT", font_medium, RED, WIDTH // 2, 400)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    game()
                    highscore = load_highscore()
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
                    highscore = load_highscore()
        
        clock.tick(FPS)

# Kontrola spouštění hry a ne modulu
if __name__ == "__main__":
    main_menu()