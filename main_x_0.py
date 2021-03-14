import statistics
import time

import pygame
import sys

ADANCIME_MAX = 6


def elem_identice(lista):
    if len(set(lista)) == 1:
        castigator = lista[0]
        if castigator != Joc.GOL:
            return castigator
    return False


def deseneaza_grid(display, tabla, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]
    w_gr = h_gr = 100  # width-ul si height-ul unei celule din grid

    x_img = pygame.image.load('ics.png')
    x_img = pygame.transform.scale(x_img, (w_gr, h_gr))
    zero_img = pygame.image.load('zero.png')
    zero_img = pygame.transform.scale(zero_img, (w_gr, h_gr))
    drt = []  # este lista cu patratelele din grid
    for ind in range(len(tabla)):
        linie = ind // Joc.NR_COLOANE  # // inseamna div
        coloana = ind % Joc.NR_COLOANE
        patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
        # print(str(coloana*(w_gr+1)), str(linie*(h_gr+1)))
        drt.append(patr)
        if marcaj == ind:
            # daca am o patratica selectata, o desenez cu rosu
            culoare = (255, 0, 0)
        else:
            # altfel o desenez cu alb
            culoare = (255, 255, 255)
        pygame.draw.rect(display, culoare, patr)  # alb = (255,255,255)
        if tabla[ind] == 'x':
            display.blit(x_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
        elif tabla[ind] == '0':
            display.blit(zero_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
    pygame.display.flip()
    return drt


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = None
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.matr = tabla or [self.__class__.GOL] * self.NR_COLOANE ** 2

    def final(self):
        ics = 0
        zero = 0
        for r in range(0, len(self.matr)):
            if self.matr[r] == "x":
                ics += 1
            elif self.matr[r] == "0":
                zero += 1
            else:
                return False
        if ics > zero:
            return "x"
        elif ics == zero:
            return "remiza"
        else:
            return "0"

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            # self.matr.verificare_simbol()
            if self.matr[i] == self.__class__.GOL:
                matr_tabla_noua = list(self.matr)
                matr_tabla_noua[i] = jucator_opus
                l_mutari.append(Joc(matr_tabla_noua))
        return l_mutari

    def patratica_libera(self, patrat, jucator):
        if patrat == jucator:
            # inseamna ca o patratica din jurul celei candidat este asemanatoare cu simbolul
            return 2  # ne intereseaza sa formam cat mai multe grupuri de patratele, astfel incat sa nu pierdem piesele
        elif patrat == self.__class__.GOL:
            # inseamna ca o patratica din jurul celei candidat este goala => nu prezinta interes
            return 0
        else:
            # inseamna ca o patratica din jurul celei candidat este ocupata de un simbol diferit => este valid (ne intereseaza mai ales pentru ca vrem sa incercuim adversarul)
            return 1

    def patratica_libera_gol(self, patrat, jucator):
        if patrat == jucator:
            # inseamna ca o patratica din jurul celei candidat este asemanatoare cu simbolul
            return 1  # in cazul de fata, nu conteaza asa mult ca patratica inconjurata sa fie libera, intrucat nu poate fi capturata decat prin asezarea simbolului in ea
        elif patrat == self.__class__.GOL:
            # inseamna ca o patratica din jurul celei candidat este goala => prezinta interes, deoarece poate fi ocupata fara probleme
            return 2
        else:
            # inseamna ca o patratica din jurul celei candidat este ocupata de un simbol diferit => ne ferim, deoarece se poate ca adversarul sa ne incercuiasca
            return 0

    def verificare_simbol(self):

        for index in range(self.NR_COLOANE ** 2):
            if self.matr[index] == self.__class__.GOL:
                continue
            l = {"x": 0,
                 "0": 0,
                 "#": 0}
            if index >= self.NR_COLOANE:
                l[self.matr[index - self.NR_COLOANE]] += 1
                if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                    l[self.matr[index - self.NR_COLOANE + 1]] += 1
                if index % self.NR_COLOANE != 0:
                    l[self.matr[index - self.NR_COLOANE - 1]] += 1
            if index < self.NR_COLOANE ** 2 - self.NR_COLOANE:
                l[self.matr[index + self.NR_COLOANE]] += 1
                if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                    l[self.matr[index + self.NR_COLOANE + 1]] += 1
                if index % self.NR_COLOANE != 0:
                    l[self.matr[index + self.NR_COLOANE - 1]] += 1
            if index % self.NR_COLOANE != 0:
                l[self.matr[index - 1]] += 1
            if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                l[self.matr[index + 1]] += 1
            if l["x"] > l["0"] and l["x"] >= 4:
                self.matr[index] = "x"
            elif l["x"] < l["0"] and l["0"] >= 4:
                self.matr[index] = "0"
            else:
                continue

    def patratele_libere(self, jucator):
        suma = 0
        for index in range(0, self.NR_COLOANE ** 2):
            if self.matr[index] != self.__class__.GOL:
                if index >= self.NR_COLOANE:
                    suma += self.patratica_libera(self.matr[index - self.NR_COLOANE], jucator)
                    if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                        suma += self.patratica_libera(self.matr[index - self.NR_COLOANE + 1], jucator)
                    if index % self.NR_COLOANE != 0:
                        suma += self.patratica_libera(self.matr[index - self.NR_COLOANE - 1], jucator)
                if index < self.NR_COLOANE ** 2 - self.NR_COLOANE:
                    suma += self.patratica_libera(self.matr[index + self.NR_COLOANE], jucator)
                    if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                        suma += self.patratica_libera(self.matr[index + self.NR_COLOANE + 1], jucator)
                    if index % self.NR_COLOANE != 0:
                        suma += self.patratica_libera(self.matr[index + self.NR_COLOANE - 1], jucator)
                if index % self.NR_COLOANE != 0:
                    suma += self.patratica_libera(self.matr[index - 1], jucator)
                if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                    suma += self.patratica_libera(self.matr[index + 1], jucator)
            else:
                if index >= self.NR_COLOANE:
                    suma += self.patratica_libera_gol(self.matr[index - self.NR_COLOANE], jucator)
                    if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                        suma += self.patratica_libera_gol(self.matr[index - self.NR_COLOANE + 1], jucator)
                    if index % self.NR_COLOANE != 0:
                        suma += self.patratica_libera_gol(self.matr[index - self.NR_COLOANE - 1], jucator)
                if index < self.NR_COLOANE ** 2 - self.NR_COLOANE:
                    suma += self.patratica_libera_gol(self.matr[index + self.NR_COLOANE], jucator)
                    if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                        suma += self.patratica_libera_gol(self.matr[index + self.NR_COLOANE + 1], jucator)
                    if index % self.NR_COLOANE != 0:
                        suma += self.patratica_libera_gol(self.matr[index + self.NR_COLOANE - 1], jucator)
                if index % self.NR_COLOANE != 0:
                    suma += self.patratica_libera_gol(self.matr[index - 1], jucator)
                if index % self.NR_COLOANE != self.NR_COLOANE - 1:
                    suma += self.patratica_libera_gol(self.matr[index + 1], jucator)
        return suma

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 1000 + adancime
        elif t_final == self.__class__.JMIN:
            return -1000 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            return self.patratele_libere(self.__class__.JMAX) - self.patratele_libere(self.__class__.JMIN)
            # calculez mutarile cele mai bune ale calculatorului si din ele le scad pe cele mai bune ale jucatorului

    def estimeaza_scor_2(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 1000 + adancime
        elif t_final == self.__class__.JMIN:
            return -1000 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            x = 0
            zero = 0
            for i in range(self.NR_COLOANE**2):
                if self.matr[i] == "x":
                    x += 1
                elif self.matr[i] == "0":
                    zero += 1
                else:
                    continue
            return self.patratele_libere(self.__class__.JMAX) + x - (self.patratele_libere(self.__class__.JMIN) + zero)\
                   / max((x + zero), 1)
        # aici calculam ce suma de oportunitati are calculatorul, adunat cu simbolurile deja existente din care scadem acelasi lucru pentru jucator. totul se imparte la numarul
        # de simboluri deja existente pe masa (pentru a avea valori mari la inceput si mici la final

    def calculeaza_scor(self):
        scor_jucatori = {"x": 0,
                         "0": 0,
                         "#": 0}
        for index in range(self.NR_COLOANE ** 2):
            scor_jucatori[self.matr[index]] += 1
        print("Jucatorul x a obtinut scorul " + str(scor_jucatori["x"]) + "\n")
        print("Jucatorul 0 a obtinut scorul " + str(scor_jucatori["0"]) + "\n")
        print("Spatiile goale sunt in numar de: " + str(scor_jucatori["#"]) + "\n")

    def __str__(self):
        sir = "  |"
        for i in range(self.NR_COLOANE):
            sir += str(i) + " "
        sir += "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for index in range(0, self.NR_COLOANE):
            sir += str(index) + " |" + " ".join([str(x) for x in self.matr[index * self.NR_COLOANE:(index + 1) * self.NR_COLOANE]]) + "\n"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        self.noduri = []
        # adancimea in arborele de stari
        self.adancime = adancime

        self.nr_noduri = 0
        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        self.tabla_joc.verificare_simbol()
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        # stare.estimare = stare.tabla_joc.estimeaza_scor_2(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    stare.nr_noduri = len(stare.mutari_posibile)
    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]
    for index in mutariCuEstimare:
        stare.nr_noduri += index.nr_noduri

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.nr_noduri = 0
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        # stare.estimare = stare.tabla_joc.estimeaza_scor_2(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    stare.nr_noduri = len(stare.mutari_posibile)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)
            for index in stare_noua.mutari_posibile:
                stare.nr_noduri += index.nr_noduri
            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)
            for index in stare_noua.mutari_posibile:
                stare.nr_noduri += index.nr_noduri
            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.noduri.append(stare.nr_noduri)
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    t_program = int(round(time.time() * 1000))
    interfata_grafica = True
    if len(sys.argv) == 1:
        interfata_grafica = False
    if len(sys.argv) == 2 and sys.argv[1] != "-gui":
        interfata_grafica = False
    # initializare algoritm
    raspuns_valid = False
    tip_algoritm = ""
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0?\n ").lower()
        if Joc.JMIN in ['x', '0']:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

    # initializare dimensiune tabla
    raspuns_valid = False
    while not raspuns_valid:
        sir = input("Ce dimensiune va doriti sa aiba tabla? (NxN, 4 < N < 11): ")
        if sir in ["5", "6", "7", "8", "9", "10"]:
            raspuns_valid = True
            Joc.NR_COLOANE = int(sir)
        else:
            print("Raspunsul trebuie sa fie un numar intreg intre 5 si 10 inclusiv.\n")

    # initializare complexitate calculator
    raspuns_valid = False
    dificultate = ""
    while not raspuns_valid:
        dificultate = input("Alegeti dificultatea: ").lower()
        if dificultate in ["incepator", "mediu", "avansat"]:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie unul dintre cuvintele: \"incepator\", \"mediu\", \"avansat\".\n")

    if dificultate == "incepator":
        ADANCIME_MAX = 3
    elif dificultate == "mediu":
        ADANCIME_MAX = 4
    else:
        ADANCIME_MAX = 5

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    timp_calculator = []
    while not interfata_grafica:
        while True:
            if stare_curenta.j_curent == Joc.JMIN:
                t_inainte = int(round(time.time() * 1000))
                # muta jucatorul
                print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
                raspuns_valid = False
                while not raspuns_valid:
                    try:
                        print("Pentru iesire, linia sau coloana trebuie sa fie -1! \n")
                        linie = int(input("linie="))
                        if linie == -1:
                            break
                        coloana = int(input("coloana="))
                        if coloana == -1:
                            break

                        elif linie in range(Joc.NR_COLOANE) and coloana in range(Joc.NR_COLOANE):
                            if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.GOL:
                                raspuns_valid = True
                            else:
                                print("Exista deja un simbol in pozitia ceruta.")
                        else:
                            print("Linie sau coloana invalida.")

                    except ValueError:
                        print("Linia si coloana trebuie sa fie numere intregi")

                if linie == -1 or coloana == -1:
                    stare_curenta.tabla_joc.calculeaza_scor()
                    break
                # dupa iesirea din while sigur am valide atat linia cat si coloana
                # deci pot plasa simbolul pe "tabla de joc"
                stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] = Joc.JMIN
                stare_curenta.tabla_joc.verificare_simbol()

                # afisarea starii jocului in urma mutarii utilizatorului
                print("\nTabla dupa mutarea jucatorului")
                print(str(stare_curenta))
                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                t_dupa = int(round(time.time() * 1000))
                print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                stare_curenta.tabla_joc.calculeaza_scor()

                if afis_daca_final(stare_curenta):
                    stare_curenta.tabla_joc.calculeaza_scor()
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()

            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator

                print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))

                # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
                stare_curenta.tabla_joc.verificare_simbol()
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                timp_calculator.append(t_dupa - t_inainte)
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                stare_curenta.noduri.append(stare_curenta.nr_noduri)
                print("Numarul de noduri calculate: " + str(stare_curenta.nr_noduri) + ".\n")
                stare_curenta.tabla_joc.calculeaza_scor()
                if afis_daca_final(stare_curenta):
                    stare_curenta.tabla_joc.calculeaza_scor()
                    break

                # S-a realizat o mutare.  jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()
        if linie != -1 and coloana != -1:
            print("Calculatorul a \"gandit\" in medie, timp de " + str(statistics.mean(timp_calculator)) + " milisecunde.")
            print("Mediana timpului de gandire al calculatorului: " + str(statistics.median(timp_calculator)) + " milisecunde. \n")
            print("Timp minim de gandire: " + str(min(timp_calculator)) + " milisecunde \n")
            print("Timp maxim de gandire: " + str(max(timp_calculator)) + " milisecunde \n")
            print("Numarul minim de noduri calculate: " + str(min(stare_curenta.noduri)) + ".\n")
            print("Numarul maxim de noduri calculate: " + str(max(stare_curenta.noduri)) + ".\n")
            print("Numarul mediu de noduri calculate: " + str(statistics.mean(stare_curenta.noduri)) + ".\n")
            print("Mediana nodurilor calculate: " + str(statistics.median(stare_curenta.noduri)) + ".\n")
        print("Programul a rulat timp de: " + str(int(round(time.time() * 1000)) - t_program) + " milisecunde.")
        quit()
        sys.exit()

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('x si 0')
    # dimensiunea ferestrei in pixeli
    ecran = pygame.display.set_mode(size=(Joc.NR_COLOANE * 100 + Joc.NR_COLOANE - 1, Joc.NR_COLOANE * 100 + Joc.NR_COLOANE - 1))  # N * 100+ N-1

    de_mutat = False
    patratele = deseneaza_grid(ecran, tabla_curenta.matr)
    timp_calculator = []
    while interfata_grafica:
        if stare_curenta.j_curent == Joc.JMIN:
            # muta jucatorul
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stare_curenta.tabla_joc.calculeaza_scor()
                    print("Programul a rulat timp de: " + str(int(round(time.time() * 1000)) - t_program) + " milisecunde.")
                    pygame.quit()
                    sys.exit()
                t_inainte = int(round(time.time() * 1000))
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for np in range(len(patratele)):

                        if patratele[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE
                            ###############################
                            if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.JMIN:
                                if de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]:
                                    # daca am facut click chiar pe patratica selectata, o deselectez
                                    de_mutat = False
                                    deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)
                                else:
                                    de_mutat = (linie, coloana)
                                    # desenez gridul cu patratelul marcat
                                    deseneaza_grid(ecran, stare_curenta.tabla_joc.matr, np)
                            if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.GOL:
                                if de_mutat:
                                    #  eventuale teste legate de mutarea simbolului
                                    stare_curenta.tabla_joc.matr[de_mutat[0] * Joc.NR_COLOANE + de_mutat[1]] = Joc.GOL
                                    de_mutat = False
                                # dupa iesirea din while sigur am valide atat linia cat si coloana
                                # deci pot plasa simbolul pe "tabla de joc"
                                stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] = Joc.JMIN
                                stare_curenta.tabla_joc.verificare_simbol()

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                t_dupa = int(round(time.time() * 1000))
                                print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                                stare_curenta.tabla_joc.calculeaza_scor()
                                patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)

                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if afis_daca_final(stare_curenta):
                                    stare_curenta.tabla_joc.verificare_simbol()
                                    print("Calculatorul a \"gandit\" in medie, timp de " + str(statistics.mean(timp_calculator)) + " milisecunde. \n")
                                    print("Mediana timpului de gandire al calculatorului: " + str(statistics.median(timp_calculator)) + " milisecunde. \n")
                                    print("Timp minim de gandire: " + str(min(timp_calculator)) + " milisecunde \n")
                                    print("Timp maxim de gandire: " + str(max(timp_calculator)) + " milisecunde \n")
                                    print("Numarul minim de noduri calculate: " + str(min(stare_curenta.noduri)) + ".\n")
                                    print("Numarul maxim de noduri calculate: " + str(max(stare_curenta.noduri)) + ".\n")
                                    print("Numarul mediu de noduri calculate: " + str(statistics.mean(stare_curenta.noduri)) + ".\n")
                                    print("Mediana nodurilor calculate: " + str(statistics.median(stare_curenta.noduri)) + ".\n")
                                    # stare_curenta.tabla_joc.calculeaza_scor()
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = stare_curenta.jucator_opus()
        #  --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            stare_actualizata.tabla_joc.verificare_simbol()
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timp_calculator.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.noduri.append(stare_curenta.nr_noduri)
            print("Numarul de noduri calculate: " + str(stare_curenta.noduri[-1]) + ".\n")
            stare_curenta.tabla_joc.calculeaza_scor()

            if afis_daca_final(stare_curenta):
                stare_curenta.tabla_joc.verificare_simbol()
                print("Calculatorul a \"gandit\" in medie, timp de " + str(statistics.mean(timp_calculator)) + " milisecunde. \n")
                print("Mediana timpului de gandire al calculatorului: " + str(statistics.median(timp_calculator)) + " milisecunde. \n")
                print("Timp minim de gandire: " + str(min(timp_calculator)) + " milisecunde \n")
                print("Timp maxim de gandire: " + str(max(timp_calculator)) + " milisecunde \n")
                print("Numarul minim de noduri calculate: " + str(min(stare_curenta.noduri)) + ".\n")
                print("Numarul maxim de noduri calculate: " + str(max(stare_curenta.noduri)) + ".\n")
                print("Numarul mediu de noduri calculate: " + str(statistics.mean(stare_curenta.noduri)) + ".\n")
                print("Mediana nodurilor calculate: " + str(statistics.median(stare_curenta.noduri)) + ".\n")
                # stare_curenta.tabla_joc.calculeaza_scor()
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()
    stare_curenta.tabla_joc.calculeaza_scor()  # Calculam scorul final
    print("Programul a rulat timp de: " + str(int(round(time.time() * 1000)) - t_program) + " milisecunde.")


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
