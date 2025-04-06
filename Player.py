import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, winsize):
        # Příprava a proměnné
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (100, winsize//2)
        self.velocity = 0
        self.gravity = 0.4
        self.jump_strength = -7
        self.visible = True
        self.invincible = False
        self.animation_frames = []
        self.current_frame = 0
        self.animation_speed = 0.15
    # Funkce pro skok
    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        # Gravitace a pohyb
        self.velocity += self.gravity
        self.rect.y += self.velocity
        
        # Rotace ptáka
        self.image = pygame.transform.rotate(
            pygame.image.load("player.png").convert_alpha(), 
            min(max(-self.velocity * 5, -30), 30)
        )
        self.image = pygame.transform.scale(self.image, (40, 40))

    def proc_grav(self, winsize):
        # Aby pták nesjel z obrazovky
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > winsize:
            self.rect.bottom = winsize
            self.velocity = 0

    def draw(self, screen):
        if self.visible:
            # Animace?
            screen.blit(self.image, self.rect)
            
            # Nezničitelnost
            if self.invincible:
                s = pygame.Surface((40, 40), pygame.SRCALPHA)
                s.fill((255, 255, 255, 128))
                screen.blit(s, self.rect)