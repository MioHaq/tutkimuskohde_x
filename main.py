### NOTE: Peliprojektini vuoden 2025 Ohjelmoinnin jatkokurssia varten.
###       Pelissä pelaat musitinsa menettänyttä hahmoa, jonka täytyy löytää
###       kaikki kadonneet muistot paetakseen ulos. Lisäksi pelaajan on
###       voitettava robottivartijat, jotka yrittävät estää sinua keräämästä
###       muistoja.

import pygame as pg

### Tässä ovat tärkeimmät asetukset, määriteltynä vakioina, jotta niiden muuttaminen olisi helpompaa

SCREEN_WIDTH: int       = 1920  # näytön leveys pikseleinä
SCREEN_HEIGHT: int      = 1080  # näytön korkeus pikseleinä
GRID_SIZE: int          = 50    # yhden ruudun koko pikseleinä
BULLET_SPEED: float     = 4.0   # luodin nopeuden kerroin, pienempi luku hidastaa luotia ja suurempi nopeutta§a
ENEMY_RELOAD_TIME: int  = 1500  # kuinka nopeasti viholliset ampuvat, pienempi numero johtaa nopeampaan tuleen
FIRST_ROOM: int         = 0     # mistä huoneesta peli aloittaa (voit asettaa arvon 1 tai 2 hypätäksesi suoraan kyseiseen huoneeseen)


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption('Tutkimuskohde X')

        self.load_images()
        self.clock = pg.time.Clock()
        self.grid_size = GRID_SIZE
        
        self.w_window = SCREEN_WIDTH
        self.h_window = SCREEN_HEIGHT
        self.window = pg.display.set_mode((self.w_window, self.h_window))

        game_win_w = 22 * self.grid_size
        game_win_h = 15 * self.grid_size
        space_w = (self.w_window - game_win_w) // 2
        space_h = (self.h_window - game_win_h) // 2
        self.game_window = self.window.subsurface((space_w, space_h), (game_win_w, game_win_h))
        self.game_window.set_alpha(1)

        ui_window_w = space_w - 50
        ui_window_h = self.h_window - (space_h * 2)
        self.ui_window = self.window.subsurface((space_w + game_win_w + 25, space_h), (ui_window_w, ui_window_h))

        self.font_memories = pg.font.SysFont('Iosevka', 48)
        self.font_health = pg.font.SysFont('Iosevka', 48)

        self.dt = 0    # asetetaan jokin arvo muuttujalle, jotta alustusfunktiot toimivat
        self.transition = False

        self.start_game()

    
    def start_game(self) -> None:
        self.init_data()
        self.init_rooms()
        self.init_enemies()

        self.main_loop()


    def init_rooms(self) -> None:
        # alustetaan huoneet
        # 0 = tyhjä ruutu
        # 1 = seinä
        # 2 = muisto
        # 3 = ovi
        # 4 = vihollinen
        room0: list[list[int]] = [
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
        room1: list[list[int]] = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 4, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 2, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        room2: list[list[int]] = [
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

        self.rooms = [room0, room1, room2]


    def init_enemies(self) -> None:
        """Alustetaan uuden huoneen viholliset"""
        self.enemies: list[dict[str, int|bool]] = []
        
        # etsitään vihollisten sijainnit dynaamisesti huoneen määrittelystä, jotta ei tarvitse erikseen kovakoodata arvoja (jotka voivat sitten muuttua jos huonetta muokataan)
        for i in range(len(self.rooms[self.current_room])):
            for j in range(len(self.rooms[self.current_room][i])):
                if self.rooms[self.current_room][i][j] == 4:
                    self.enemies.append({
                        'x': j,
                        'y': i,
                        'alive': True,
                        'last_shot': 0
                    })


    def init_data(self) -> None:
        """Alustetaan uuden huoneen datat"""
        self.memory_counts = [4, 0, 0]      # muistojen määrä jokaisessa huoneessa. yritin ensin tehdä luokan mutta koodista tuli liian monimutkaista, joten tämä on nyt kompromissi.
        self.current_room = FIRST_ROOM
        self.memories = 0
        self.bullets: list[dict[str, pg.Vector2|float|str]] = []

        self.player = {
            'x': 5,
            'y': 3,
            'health': 10
        }


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
                self.player_shoot((event.pos[0], event.pos[1]))


    def draw_room(self) -> None:
        """Piirtää huoneen."""
        # huomioi, että silmukoiden järjestyksen vuoksi 'i' kuvastaa y-akselia ja 'j' kuvastaa x-akselia!
        for i in range(len(self.rooms[self.current_room])):
            for j in range(len(self.rooms[self.current_room][i])):
                
                # jos ruudun koodi on 1, se on osa seinää (jolloin kohdalle piirretään koko ruudun täyttävä neliö)
                if self.rooms[self.current_room][i][j] == 1:
                    pg.draw.rect(self.game_window, (106, 120, 136), pg.rect.Rect(j*self.grid_size, i*self.grid_size, self.grid_size, self.grid_size))
                
                # jos ruudun koodi on 2, se on kolikko, joten kohdalle piirretään kolikkokuva
                elif self.rooms[self.current_room][i][j] == 2:
                    self.game_window.blit(self.coin_im, (j*self.grid_size, i*self.grid_size))

                # jos ruudun koodi on 3, se on ovi, joten kohdalle piirretään ovi
                elif self.rooms[self.current_room][i][j] == 3:
                    self.game_window.blit(self.door_im, (j*self.grid_size, i*self.grid_size))


    def draw_player(self) -> None:
        """Piirtää pelaajan näytölle."""
        self.game_window.blit(self.monster_im, (self.player['x'] * 50, self.player['y'] * 50))


    def move_player(self, dx: int, dy: int) -> None:
        """Siirtää pelaajan (mikäli haluttu ruutu ei ole seinää) ja suorittaa mahdollisen komennon (kolikon / oven kohdalla)"""

        new_x = self.player['x'] + dx
        new_y = self.player['y'] + dy

        # pelaaja siirtyy tyhjään ruutuun tai vihollisen päälle.
        # tämä on vähän kompromissi, vihollinen ei pysty ampumaan jos sen päällä seisoo mutta pelaaja pystyy ampumaan "sisäänsä",
        # joten näin voi tuhota vihollisen joutumatta sen tuleen (koska vihollinen ei pysty samaan)
        if self.rooms[self.current_room][new_y][new_x] == 0 or self.rooms[self.current_room][new_y][new_x] == 4:
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
                self.switch_room()


    def shoot(self, start: tuple[int, int], direction: pg.Vector2, shooter: str) -> None:
        """Ampuu uuden luodin"""
        print(start, direction)
        self.bullets.append({
            'x': start[0],
            'y': start[1],
            'direction': direction,
            'shooter': shooter      # voi olla joko 'player' eli pelaajan ampuma, tai 'enemy' eli vihulaisen ampuma
        })


    def draw_enemies(self) -> None:
        """Piirtää viholliset näytölle"""
        for enemy in [e for e in self.enemies if e['alive']]:
            self.game_window.blit(self.robo_im, (enemy['x'] * 50, enemy['y'] * 50))


    def check_enemy_shooting(self) -> None:
        """Tarkistaa, onko vihollisten aika ampua"""

        # haetaan ensin kaikki elossa olevat viholliset
        for enemy in [e for e in self.enemies if e['alive']]:
            # jos edellisestä ampumakerrasta on mennyt yli 2000 iskua, voi vihollinen ampua uudelleen
            if pg.time.get_ticks() - enemy['last_shot'] > ENEMY_RELOAD_TIME:
                # luodaan vektori vihollisesta kohti pelaajaa, ja varmistetaan, ettei vektori ole nollavektori
                vec_to_player = pg.Vector2(self.player['x'] - enemy['x'], self.player['y'] - enemy['y'])
                
                if vec_to_player.length() != 0:
                    vec_to_player.normalize_ip()
                else:
                    return

                self.shoot((enemy['x'] * self.grid_size + self.grid_size // 2, enemy['y'] * self.grid_size + self.grid_size // 2), vec_to_player, 'enemy')

                enemy['last_shot'] = pg.time.get_ticks()


    def player_shoot(self, goal_raw: tuple[int, int]) -> None:
        """Ampuu luodin pelaajan sijainnista annettua maalia kohti"""

        # koska peli-ikkuna toimii koko näytön ali-ikkunana, muutetaan maalin koordinaatit vastaamaan samaa järjestelmää
        # ts. vähenntetään annetusta sijainnista peli-ikkunan sijaintiero (offset)
        offset_x, offset_y = self.game_window.get_abs_offset()
        goal = (goal_raw[0] - offset_x, goal_raw[1] - offset_y)

        vec_to_enemy = pg.Vector2(goal[0] - self.player['x'] * self.grid_size, goal[1] - self.player['y'] * self.grid_size)
        
        if vec_to_enemy.length() != 0:
            vec_to_enemy.normalize_ip()
        else:
            return

        self.shoot((self.player['x'] * self.grid_size + self.grid_size // 2, self.player['y'] * self.grid_size + self.grid_size // 2), vec_to_enemy, 'player')


    def check_hits(self) -> None:
        """Tarkistetaan, onko pelaajaan tai yhteenkään viholliseen osunut luotia. Tapetaan vihollinen, jos siihen on osunut luoti. Pelaajalta otetaan elämäpiste pois, jos häneen osuu. Jos elämäpisteet loppuvat, loppuu myös peli."""
        
        for i in range(len(self.bullets) - 1, -1, -1):
            bullet = self.bullets[i]
            has_hit = ''

            # siirretään luotia
            self.bullets[i]['x'] += self.bullets[i]['direction'].x * BULLET_SPEED
            self.bullets[i]['y'] += self.bullets[i]['direction'].y * BULLET_SPEED

            # lasketaan ruutu, jossa luoti sillä hetkellä on
            grid_x = int(bullet['x'] // self.grid_size)
            grid_y = int(bullet['y'] // self.grid_size)

            # selvitetään osuuko luoti seinään
            if self.rooms[self.current_room][grid_y][grid_x] == 1 or self.rooms[self.current_room][grid_y][grid_x] == 3:
                has_hit = 'wall'

            # selvitetään, ottiko pelaaja osumaa
            if grid_x == self.player['x'] and grid_y == self.player['y'] and bullet['shooter'] == 'enemy':
                self.player['health'] -= 1
                has_hit = 'player'
                print(self.player['health'])
            
            # selvitetään sitten, osuiko johonkin viholliseen
            for enemy in [e for e in self.enemies if e['alive']]:
                if grid_x == enemy['x'] and grid_y == enemy['y'] and bullet['shooter'] == 'player':
                    self.rooms[self.current_room][grid_y][grid_x] = 0
                    enemy['alive'] = False
                    has_hit = 'enemy'
                    break

            if has_hit != '':
                self.bullets.pop(i)
                print(f"osui {has_hit}")
                break


    def draw_bullets(self) -> None:
        for bullet in self.bullets:
            if bullet['shooter'] == 'player':
                pg.draw.circle(self.game_window, 'orange', (int(bullet['x']), int(bullet['y'])), 6)
            if bullet['shooter'] == 'enemy':
                pg.draw.circle(self.game_window, 'red', (int(bullet['x']), int(bullet['y'])), 6)


    def update_ui(self) -> None:
        # näytetään pelaajalle kerättyjen muistojen määrä
        pg.draw.rect(self.ui_window, (143, 114, 90), pg.Rect(0,0, self.ui_window.get_width(), 100))
        memory_str = f"MUISTOT    {self.memories} / {self.memory_counts[self.current_room]}"
        memory_txt = self.font_memories.render(memory_str, True, 'green')
        self.ui_window.blit(memory_txt, (10,30))

        pg.draw.rect(self.ui_window, (143, 114, 90), pg.Rect(0,150, self.ui_window.get_width(), 150))
        health_str = f"ELÄMÄPISTEET: {self.player['health']} / 10"
        health_txt = self.font_health.render(health_str, True, 'red')
        self.ui_window.blit(health_txt, (10, 180))


    def switch_room(self) -> None:
        if not self.transition:
            self.transition = True
            if self.current_room == 2:
                pg.quit()
                exit()
            else:
                self.current_room += 1

        current_alpha = self.game_window.get_alpha()

        if current_alpha == 0:
            self.transition = False
            return
        else:
            self.game_window.set_alpha(current_alpha - 0.01)



    def main_loop(self) -> None:
        """Aloittaa pääsilmukan."""
        while True:
            self.handle_events()

            self.game_window.fill((142, 145, 103))
           
            if not self.transition:
                self.draw_room()
                self.draw_player()
                self.draw_enemies()
                self.draw_bullets()
            
                self.check_enemy_shooting()
                self.check_hits()
                self.update_ui()
            else:
                self.switch_room()

            pg.display.flip()

            self.dt = self.clock.tick(60)


    def jee(self) -> None:
        self.main_loop()


def main() -> None:
    Game()

main()

