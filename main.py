import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Deszcz z kroplami i rozpryskiem')

# Kolory
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Parametry kropli
drop_radius = 5
gravity = 0.3
splash_particles = []

# Klasa reprezentująca kroplę deszczu
class Drop:
    def __init__(self):
        self.x = random.randint(0, screen_width)  # Losowa pozycja X
        self.y = random.randint(-100, screen_height)  # Losowa pozycja Y (na początku poza ekranem)
        self.velocity = random.randint(3, 5)  # Prędkość spadania

    def fall(self):
        self.y += self.velocity  # Kropla spada
        self.velocity += gravity  # Zwiększenie prędkości spadania

        # Jeżeli kropla dotknie podłogi, generujemy rozprysk
        if self.y > screen_height - drop_radius:
            self.y = random.randint(-100, -10)
            self.velocity = random.randint(3, 5)
            self.create_splash()

    def create_splash(self):
        # Tworzymy kilka cząsteczek rozprysku
        for _ in range(10):  # 10 cząsteczek rozprysku
            splash_particles.append(Splash(self.x, screen_height - drop_radius))

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), drop_radius)

# Klasa reprezentująca pojedynczą cząsteczkę rozprysku
class Splash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.velocity_x = random.uniform(-1, 1) * 3  # Losowy kierunek rozprysku w poziomie
        self.velocity_y = random.uniform(-1, 1) * 3  # Losowy kierunek rozprysku w pionie
        self.life = random.randint(10, 20)  # Żywotność cząsteczki (ilość klatek)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += gravity * 0.1  # Cząsteczki również podlegają lekkiej grawitacji
        self.life -= 1  # Zmniejszamy żywotność cząsteczki

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

# Inicjalizacja kropli
drops = [Drop() for _ in range(100)]  # Tworzymy 100 kropli deszczu

# Zegar do kontrolowania liczby klatek na sekundę
clock = pygame.time.Clock()

# Główna pętla gry
running = True
while running:
    screen.fill(BLACK)  # Wypełniamy tło kolorem czarnym (jak noc)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rysowanie i animacja kropli
    for drop in drops:
        drop.fall()  # Kropla spada
        drop.draw()  # Kropla jest rysowana

    # Rysowanie i animacja cząsteczek rozprysku
    for splash in splash_particles[:]:
        splash.move()  # Cząsteczka porusza się
        splash.draw()  # Cząsteczka jest rysowana
        if splash.life <= 0:  # Usuwamy cząsteczki, które wygasły
            splash_particles.remove(splash)

    pygame.display.update()  # Odświeżenie ekranu

    # Ustawienie liczby klatek na sekundę
    clock.tick(60)

# Zakończenie Pygame
pygame.quit()
