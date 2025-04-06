import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, winsize, winsizex, gap_y, gap_size, speed):
        # Příprava a proměnné
        super().__init__()
        self.width = 80
        self.gap_size = gap_size
        self.speed = speed
        self.passed = False
        
        # 10% šance na zlatou trubku za 3 body
        self.is_special = random.random() < 0.1  # 10% šance
        
        if self.is_special:
            # Zlatá trubka
            self.image_top = pygame.image.load("pipe2.png").convert_alpha()
            self.points = 3  # 3 body za zlatou trubku
            self.gap_size = gap_size - 20  # Větší obtížnost pro zlatou trubku
        else:
            # Klasická trubka
            self.image_top = pygame.image.load("pipe.png").convert_alpha()
            self.points = 1
            self.gap_size = gap_size
            
        # Trubka nahoře
        self.image_top = pygame.transform.scale(self.image_top, (self.width, gap_y))
        self.image_top = pygame.transform.flip(self.image_top, False, True)
        
        # Trubka dole
        self.image_bottom = pygame.image.load("pipe2.png").convert_alpha() if self.is_special else pygame.image.load("pipe.png").convert_alpha()
        bottom_height = winsize - gap_y - self.gap_size
        self.image_bottom = pygame.transform.scale(self.image_bottom, (self.width, bottom_height))
        
        # Souřadnice pro trubky
        self.rect_top = self.image_top.get_rect()
        self.rect_top.x = winsizex
        self.rect_top.y = 0
        
        self.rect_bottom = self.image_bottom.get_rect()
        self.rect_bottom.x = winsizex
        self.rect_bottom.y = gap_y + self.gap_size
        
        # Definice pro kontrolu kolizí
        self.rect = pygame.Rect(winsizex, 0, self.width, winsize)

    # Funkce pro pohyb trubek
    def update(self):
        self.rect_top.x -= self.speed
        self.rect_bottom.x -= self.speed
        self.rect.x -= self.speed
        
    def draw(self, screen):
        screen.blit(self.image_top, self.rect_top)
        screen.blit(self.image_bottom, self.rect_bottom)
        
        # Efekt pro zlatou trubku
        if self.is_special:
            s = pygame.Surface((self.width, 10), pygame.SRCALPHA)
            s.fill((255, 255, 0, 128))
            screen.blit(s, (self.rect_top.x, self.rect_top.bottom - 5))
            screen.blit(s, (self.rect_bottom.x, self.rect_bottom.top))
        # Kontrola, jestli je trubka na obrazovce
    def is_off_screen(self):
        return self.rect_top.right < 0
        # Nahrání bodů
    def score_point(self, player_rect):
        if not self.passed and self.rect_top.right < player_rect.left:
            self.passed = True
            return True
        return False