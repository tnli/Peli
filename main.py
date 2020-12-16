# code copyright Taneli Pirinen (tnli@iki.fi) 2020, Free for non-commercial use,
# but do buy me a beer if you enjoy it

import pygame
import random

class Kohde:
    def __init__(self, nimi: str, x: int, y: int, x_koko: int, y_koko: int):
        self.nimi = nimi
        self.x = x
        self.y = y
        self.x_koko = x_koko
        self.y_koko = y_koko

    def sijainti(self):
        return(self.x, self.y)
    
    def koko(self):
        return(self.x_koko, self.y_koko)

class Kolikko(Kohde):
    def __init__(self, nimi: str, x: int, y: int, x_koko: int, y_koko: int, laudalla: bool, keratyt: int):
        Kohde.__init__(self, nimi, x, y, x_koko, y_koko)
        self.laudalla = laudalla
        self.keratyt = keratyt
    
    def kerattiin_kolikko(self):
        self.keratyt += 1

    def keratty_kymmenen(self):
        if self.keratyt >= 10:
            return True
        else:
            return False
    
    def pois(self):
        self.x = -100
        self.y = -100
        self.laudalla = False
    
    def takaisin(self, x: int, y: int):
        self.laudalla = True
        self.x = x
        self.y = y

class Ovi(Kohde):
    def __init__(self, nimi: str, x: int, y: int, x_koko: int, y_koko: int):
        Kohde.__init__(self, nimi, x, y, x_koko, y_koko)
        self.laudalla = False
        self.keratty = False

    def laudalle(self, x: int, y: int):
        self.laudalla = True
        self.x = x
        self.y = y
    
    def pois(self):
        self.x = -100
        self.y = -100
        self.laudalla = False

class Pelattava(Kohde):
    def __init__(self, nimi: str, x: int, y: int, nopeus: int, x_koko: int, y_koko: int):
        Kohde.__init__(self, nimi, x, y, x_koko, y_koko)
        self.nopeus = nopeus
        self.kolikot = 0
        self.ovet = 0

        self.pisteet = 0

        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False

        self.ei_ole_liikkunut = True
    
    def liiku_x(self, suunta: int):
        # suunta 1 oikealle, -1 vasemmalle
        self.x += suunta
    
    def liiku_y(self, suunta: int):
        # suunta 1 alas, -1 ylös
        self.y += suunta

    def liikkuu(self):
        return self.oikealle or self.vasemmalle or self.ylos or self.alas

    # def aloita_alusta(self):

class Peli:
    def __init__(self):

        self.kolikon_arvo = 10
        self.oven_arvo = 50

        self.pelin_leveys = 640
        self.pelin_korkeus = 480

        pygame.init()

        self.lataa_kuvat()
        self.uusi_peli()

        self.naytto = pygame.display.set_mode((self.pelin_leveys, self.pelin_korkeus))

        self.fontti = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Peli")

        self.silmukka()

    def lataa_kuvat(self):
        self.robo_kuva = pygame.image.load("images/robo.png")
        self.hirvio_kuva = pygame.image.load("images/hirvio.png")
        self.kolikko_kuva = pygame.image.load("images/kolikko.png")
        self.ovi_kuva = pygame.image.load("images/ovi.png")

    def uusi_peli(self):
        self.voittaja = ""

        # robon aloitus
        x = 0
        y = self.pelin_korkeus - self.robo_kuva.get_height()
        nopeus = 2
        x_koko = self.robo_kuva.get_width()
        y_koko = self.robo_kuva.get_height()

        self.robo = Pelattava("robo", x, y, nopeus, x_koko, y_koko)
        
        # hirvion aloitus
        # kyllä, hirvio on nopeampi mutta pienempi
        x = self.pelin_leveys - self.hirvio_kuva.get_width()
        y = 0
        nopeus = 3
        x_koko = self.hirvio_kuva.get_width()
        y_koko = self.hirvio_kuva.get_height()

        self.hirvio = Pelattava("hirvio", x, y, nopeus, x_koko, y_koko)

        self.pelattavat = (self.robo, self.hirvio)
        self.yhteentormays = False

        self.robo_sai_kolikon = False
        self.hirvio_sai_kolikon = False

        self.robo_sai_oven = False
        self.hirvio_sai_oven = False

        # kolikon aloitus
        x = random.randint(0, self.pelin_leveys - self.kolikko_kuva.get_width())
        y = random.randint(0, self.pelin_korkeus - self.kolikko_kuva.get_height())

        keratyt = 0
        laudalla = True
        x_koko = self.kolikko_kuva.get_width()
        y_koko = self.kolikko_kuva.get_height()

        self.kolikko = Kolikko("kolikko", x, y, x_koko, y_koko, laudalla, keratyt)

        # oven aloitus, ovi on piilossa
        x = -1000
        y = -1000

        x_koko = self.ovi_kuva.get_width()
        y_koko = self.ovi_kuva.get_height()

        self.ovi = Ovi("ovi", x, y, x_koko, y_koko)

        # kello
        self.kello = pygame.time.Clock()

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.liikkumiset()
            self.tormaykset()
            self.paivitykset()
            self.piirra_naytto()
            self.kello.tick(60)
        
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:

                # robo
                if tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.robo.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.robo.alas = True

                # hirvio
                if tapahtuma.key == pygame.K_a:
                    self.hirvio.vasemmalle = True
                if tapahtuma.key == pygame.K_d:
                    self.hirvio.oikealle = True
                if tapahtuma.key == pygame.K_w:
                    self.hirvio.ylos = True
                if tapahtuma.key == pygame.K_s:
                    self.hirvio.alas = True
                
                # peli
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:

                # robo
                if tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.robo.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.robo.alas = False

                # hirvio
                if tapahtuma.key == pygame.K_a:
                    self.hirvio.vasemmalle = False
                if tapahtuma.key == pygame.K_d:
                    self.hirvio.oikealle = False
                if tapahtuma.key == pygame.K_w:
                    self.hirvio.ylos = False
                if tapahtuma.key == pygame.K_s:
                    self.hirvio.alas = False

            if tapahtuma.type == pygame.QUIT:
                exit()

    def tormaa_reunaan(self, liikkuja: Pelattava, suunta: int, akseli: str):
        # return False jos EI törmää
        # retrun True jos TÖRMÄÄ
        # suunta 1, jos kasvaa, -1 jos pienenee

        if akseli == "x":
            maksimi = self.pelin_leveys
            if liikkuja.x + 1 * suunta >= 0 and liikkuja.x + 1 * suunta + liikkuja.x_koko <= maksimi:
                return False
            else:
                return True

        elif akseli == "y":
            maksimi = self.pelin_korkeus
            if liikkuja.y + 1 * suunta >= 0 and liikkuja.y + 1 * suunta + liikkuja.y_koko <= maksimi:
                return False
            else:
                return True
    
    def liikkumiset(self):
        if self.peli_lapi() or self.game_over():
            pass

        else: 
            for pelattava in self.pelattavat:
                if pelattava.liikkuu:
                    self.liikuta(pelattava)

    def liikuta(self, liikkuja: Pelattava):
        for _ in range (liikkuja.nopeus):
            if liikkuja.oikealle and not self.tormaa_reunaan(liikkuja, 1, "x"):
                liikkuja.liiku_x(1)
                liikkuja.ei_ole_liikkunut = False
            if liikkuja.vasemmalle and not self.tormaa_reunaan(liikkuja, -1, "x"):
                liikkuja.liiku_x(-1)
                liikkuja.ei_ole_liikkunut = False
            if liikkuja.ylos and not self.tormaa_reunaan(liikkuja, -1, "y"):
                liikkuja.liiku_y(-1)
                liikkuja.ei_ole_liikkunut = False
            if liikkuja.alas and not self.tormaa_reunaan(liikkuja, 1, "y"):
                liikkuja.liiku_y(1)
                liikkuja.ei_ole_liikkunut = False

    def tormaykset(self):
        self.tarkista_yhteentormays()

        if self.kolikko.laudalla:
            self.robo_sai_kolikon = self.tormays_pelattava_kohde(self.robo, self.kolikko)
            self.hirvio_sai_kolikon = self.tormays_pelattava_kohde(self.hirvio, self.kolikko)

        if self.ovi.laudalla:
            self.robo_sai_oven = self.tormays_pelattava_kohde(self.robo, self.ovi)
            self.hirvio_sai_oven = self.tormays_pelattava_kohde(self.hirvio, self.ovi)
    
    def tarkista_yhteentormays(self):
        if self.robo.x + self.robo.x_koko >= self.hirvio.x and self.robo.x <= self.hirvio.x + self.hirvio.x_koko and self.robo.y + self.robo.y_koko >= self.hirvio.y and self.robo.y <= self.hirvio.y + self.hirvio.y_koko:
            self.yhteentormays = True
        else:
            self.yhteentormays = False

    def tormays_pelattava_kohde(self, pelattava: Pelattava, kohde: Kohde):
        if pelattava.x + pelattava.x_koko >= kohde.x and pelattava.x <= kohde.x + kohde.x_koko and pelattava.y + pelattava.y_koko >= kohde.y and pelattava.y <= kohde.y + kohde.y_koko:
            return True
        else:
            return False

    def arvo_x(self, kuvan_leveys: int):
        return random.randint(0, self.pelin_leveys - kuvan_leveys)
    
    def arvo_y(self, kuvan_korkeus: int):
        return random.randint(0, self.pelin_korkeus - kuvan_korkeus)

    def paivitykset(self):
        if self.robo_sai_kolikon:
            self.robo.nopeus += 1
            self.robo.kolikot += 1

        if self.hirvio_sai_kolikon:
            self.hirvio.nopeus += 1
            self.hirvio.kolikot += 1

        if self.robo_sai_oven and not self.peli_lapi():
            self.robo.ovet += 1

        if self.hirvio_sai_oven and not self.peli_lapi():
            self.hirvio.ovet += 1

        if self.robo_sai_kolikon or self.hirvio_sai_kolikon:
            self.kolikko.keratyt += 1
            self.kolikko.pois()
            self.robo_sai_kolikon = False
            self.hirvio_sai_kolikon = False

        if self.robo_sai_oven or self.hirvio_sai_oven:
            self.ovi.pois()
            self.ovi.keratty = True
            self.robo_sai_oven = False
            self.hirvio_sai_oven = False

        if not self.kolikko.laudalla and not self.kolikko.keratty_kymmenen():
            self.kolikko.takaisin(self.arvo_x(self.kolikko_kuva.get_width()), self.arvo_y(self.kolikko_kuva.get_height()))
        
        if self.kolikko.keratty_kymmenen() is True and self.ovi.laudalla is False and self.ovi.keratty is False:
            self.kolikko.pois()
            self.ovi.laudalle(self.arvo_x(self.kolikko_kuva.get_width()), self.arvo_y(self.kolikko_kuva.get_height()))
        
        for pelattava in self.pelattavat:
            pelattava.pisteet = pelattava.ovet * self.oven_arvo + pelattava.kolikot * self.kolikon_arvo

    def piirra_naytto(self):
        self.naytto.fill((255, 255, 255))

        # robo
        self.naytto.blit(self.robo_kuva, (self.robo.x, self.robo.y))

        # hirvio
        self.naytto.blit(self.hirvio_kuva, (self.hirvio.x, self.hirvio.y))

        if self.kolikko.laudalla:
            self.naytto.blit(self.kolikko_kuva, (self.kolikko.x, self.kolikko.y))

        if self.ovi.laudalla:
            self.naytto.blit(self.ovi_kuva, (self.ovi.x, self.ovi.y))

        if self.yhteentormays:
            teksti = self.fontti.render("Game Over! Press F2 for a new game!", True, (255, 0, 0))
            self.naytto.blit(teksti, (self.pelin_leveys/2 - teksti.get_width()/2, self.pelin_korkeus/2 - teksti.get_height()/2))

        teksti = self.fontti.render("Robo liikkuu nuolinäppäimillä! Robon pisteet: " + str(self.robo.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (self.pelin_leveys/2 - teksti.get_width()/2, self.pelin_korkeus - 50))
        
        teksti = self.fontti.render("Hirviö liikkuu wasd-näppäimillä! Hirviön pisteet: " + str(self.hirvio.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (self.pelin_leveys/2 - teksti.get_width()/2, 10))

        if not self.peli_lapi():
            if self.hirvio.ei_ole_liikkunut or self.robo.ei_ole_liikkunut:
                teksti = self.fontti.render("Kerää kolikoita! Älä törmää! Ovi on kultasieppi!", True, (255, 0, 0))
                self.naytto.blit(teksti, (self.pelin_leveys/2 - teksti.get_width()/2, self.pelin_korkeus/2 - teksti.get_height()/2))

        if self.peli_lapi():
            teksti = self.fontti.render(self.voittaja + " voitti! Press F2 for a new game", True, (255, 0, 0))
            self.naytto.blit(teksti, (self.pelin_leveys/2 - teksti.get_width()/2, self.pelin_korkeus/2 - teksti.get_height()/2))

        pygame.display.flip()
    
    def peli_lapi(self):
        if self.kolikko.keratty_kymmenen() and self.ovi.keratty is True:
            for pelattava in self.pelattavat:
                pelattava.pisteet = pelattava.ovet * self.oven_arvo + pelattava.kolikot * self.kolikon_arvo
            
            if self.robo.pisteet > self.hirvio.pisteet:
                self.voittaja = "Robo"
            else:
                self.voittaja = "Hirviö"

            return True
    
    def game_over(self):
        if self.yhteentormays:
            return True

if __name__ == "__main__":
    Peli()