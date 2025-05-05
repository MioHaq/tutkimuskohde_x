import pygame as pg


### NOTE: Peliprojektini vuoden 2025 Ohjelmoinnin jatkokurssia varten.
###       Pelissä pelaat musitinsa menettänyttä hahmoa, jonka täytyy löytää
###       kaikki kadonneet muistot paetakseen ulos. Lisäksi pelaajan on
###       voitettava robottivartijat, jotka yrittävät estää sinua keräämästä
###       muistoja.


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption('Tutkimuskohde X')

        self.load_images()
        self.clock = pg.time.Clock()
        self.grid_size = 50             # yhden ruudun leveys pikseleinä
        
        self.w_window = 1920
        self.h_window = 1080
        self.window = pg.display.set_mode((self.w_window, self.h_window))

        self.start_game()

    
    def start_game(self) -> None:
        # alustetaan huoneet
        # 0 = tyhjä ruutu
        # 1 = seinä
        # 2 = muisto
        # 3 = ovi
        # 4 = vihollinen
        room0 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1],
            [1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 1],
            [1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1]
        ]
        room1 = [...]
        room2 = [...]

        self.rooms = [room0, room1, room2]
        self.memory_counts = [4, 0, 0]
        self.current_room = 0

        self.player = {
            'x': 5,
            'y': 3,
            'health': 10
        }
        self.memories = 0

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
            
            # käsitellään näppäinkomennot ja liikutetaan hahmoa niiden mukaisesti
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.move_player(-1, 0)
                if event.key == pg.K_d:
                    self.move_player(1, 0)
                if event.key == pg.K_w:
                    self.move_player(0, -1)
                if event.key == pg.K_s:
                    self.move_player(0, 1)

            if event.type == pg.MOUSEBUTTONDOWN:
                ...


    def draw_room(self) -> None:
        """Piirtää huoneen."""
        # huomioi, että silmukoiden järjestyksen vuoksi 'i' kuvastaa y-akselia ja 'j' kuvastaa x-akselia!
        for i in range(len(self.rooms[self.current_room])):
            for j in range(len(self.rooms[self.current_room][i])):
                
                # jos ruudun koodi on 1, se on osa seinää (jolloin kohdalle piirretään koko ruudun täyttävä neliö)
                if self.rooms[self.current_room][i][j] == 1:
                    pg.draw.rect(self.window, (0,0,0), pg.rect.Rect(j*self.grid_size, i*self.grid_size, self.grid_size, self.grid_size))
                
                # jos ruudun koodi on 2, se on kolikko, joten kohdalle piirretään kolikkokuva
                elif self.rooms[self.current_room][i][j] == 2:
                    self.window.blit(self.coin_im, (j*self.grid_size, i*self.grid_size))

                # jos ruudun koodi on 3, se on ovi, joten kohdalle piirretään ovi
                elif self.rooms[self.current_room][i][j] == 3:
                    self.window.blit(self.door_im, (j*self.grid_size, i*self.grid_size))

                # jos ruudun koodi on 4, se on vihollinen, joten kohtaan piirretään robotti
                elif self.rooms[self.current_room][i][j] == 4:
                    self.window.blit(self.robo_im, (j*self.grid_size, i*self.grid_size))


    def draw_player(self) -> None:
        """Piirtää pelaajan näytölle."""
        self.window.blit(self.monster_im, (self.player['x'] * 50, self.player['y'] * 50))


    def move_player(self, dx: int, dy: int) -> None:
        """Siirtää pelaajan (mikäli haluttu ruutu ei ole seinää) ja suorittaa mahdollisen komennon (kolikon / oven kohdalla)"""

        new_x = self.player['x'] + dx
        new_y = self.player['y'] + dy

        # pelaaja siirtyy tyhjään ruutuun.
        if self.rooms[self.current_room][new_y][new_x] == 0:
            self.player['x'] = new_x
            self.player['y'] = new_y

        # pelaaja siirtyy ruutuun jossa on muisto. muisto katoaa ja pelaaja saa pisteen.
        elif self.rooms[self.current_room][new_y][new_x] == 2:
            self.player['x'] = new_x
            self.player['y'] = new_y
            self.rooms[self.current_room][new_y][new_x] = 0
            self.memories += 1
            print(self.memories)

        # pelaaja yrittää siirtyä oviruutuun, päästetään vain jos kaikki muistot on kerätty
        elif self.rooms[self.current_room][new_y][new_x] == 3:
            if self.memories == self.memory_counts[self.current_room]:
                print("jee")


    def main_loop(self) -> None:
        while True:
            self.handle_events()
            self.window.fill((100, 100, 100))
            self.draw_room()
            self.draw_player()
            pg.display.flip()

            self.dt = self.clock.tick(144)


def main() -> None:
    Game()

main()

