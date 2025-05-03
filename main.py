import pygame as pg

class Player:
    """Käsittelee pelaajan informaatiota, kuten sijaintia ja elämäpisteiden määrää."""
    def __init__(self) -> None:
        self.x: int = 5
        self.y: int = 3
        self.health: int = 100

    def hit(self) -> None:
        self.health -= 15

    def move(self, x: int, y: int) -> None:
        self.x += x
        self.y += y

    def draw(self, window: pg.surface.Surface, image: pg.surface.Surface) -> None:
        window.blit(image, (self.x * 50, self.y * 50))


class Game:
    def __init__(self) -> None:
        pg.display.set_caption('Tutkimuskohde X')

        self.load_images()
        self.clock = pg.time.Clock()
        self.grid_size = 50
        
        self.w_window = 1920
        self.h_window = 1080
        self.window = pg.display.set_mode((self.w_window, self.h_window))
        
        self.player = Player()

        self.start_game()

    
    def start_game(self) -> None:
        room1 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        room2 = [...]
        room3 = [...]

        self.rooms = [room1, room2, room3]

        self.main_loop()

    def load_images(self) -> None:
        """Ladataan pelin käyttämät kuvat valmiiksi."""
        self.robo_im = pg.image.load('robo.png')
        self.door_im = pg.image.load('ovi.png')
        self.coin_im = pg.image.load('kolikko.png')
        self.monster_im = pg.image.load('hirvio.png')


    def handle_events(self) -> None:
        """Käsitellään mahdollsiesti saatu tapahtuma, kuten näppäimen painallus tai hiiren liikututs"""
        for event in pg.event.get():
            # käyttäjä haluaa poistua pelistä. koodin suoritus päättyy tähän
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.player.move(-1, 0)
                if event.key == pg.K_d:
                    self.player.move(1, 0)
                if event.key == pg.K_w:
                    self.player.move(0, -1)
                if event.key == pg.K_s:
                    self.player.move(0, 1)

            if event.type == pg.MOUSEBUTTONDOWN:
                ...


    def draw_room(self) -> None:
        for i in range(len(self.rooms[0])):
            for j in range(len(self.rooms[0][i])):
                if self.rooms[0][i][j] == 1:
                    pg.draw.rect(self.window, (0,0,0), pg.rect.Rect(j*50, i*50, 50, 50))


    def main_loop(self) -> None:
        while True:
            self.handle_events()
            self.window.fill((100, 100, 100))
            self.draw_room()
            self.player.draw(self.window, self.monster_im)
            pg.display.flip()

            self.clock.tick(144)


def main() -> None:
    pg.init()
    Game()

main()

