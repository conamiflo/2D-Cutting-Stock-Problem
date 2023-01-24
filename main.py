import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from gui import *

class Pravougaonik:
    def __init__(self, sirina, visina, x=0, y=0):
        self.sirina = sirina
        self.visina = visina
        self.x = x
        self.y = y

    def povrsina(self):
        return self.sirina * self.visina


def provera_nula(matrica, i, j, nova_visina, nova_sirina):
    for m in range(i, nova_visina):
        for n in range(j, nova_sirina):
            if matrica[m][n] != 0:
                return False

    return True

sve_povrsine = {}
def fituj(pravougaonici, hromozom,vrati_matricu = False):

    if not vrati_matricu:
        if hromozom in sve_povrsine:
            return sve_povrsine[hromozom]

    materijal_matrica = np.zeros((materijal.visina, materijal.sirina))
    povrsina = materijal.povrsina()


    for i in range(len(pravougaonici)):

        if hromozom[i] == "1":
            j,k = 0, 0
            while j < materijal.visina and k < materijal.sirina:
                if materijal_matrica[j][k] == 0:
                    nova_visina = j + pravougaonici[i].visina
                    nova_sirina = k + pravougaonici[i].sirina
                    if nova_visina <= materijal.visina and nova_sirina <= materijal.sirina:
                        if provera_nula(materijal_matrica, j, k, nova_visina, nova_sirina):
                            povrsina -= pravougaonici[i].povrsina()
                            for m in range(j, nova_visina):
                                for n in range(k, nova_sirina):
                                    materijal_matrica[m][n] = i + 1

                            break


                    nova_visina = j + pravougaonici[i].sirina
                    nova_sirina = k + pravougaonici[i].visina
                    if nova_visina <= materijal.visina and nova_sirina <= materijal.sirina:
                        if provera_nula(materijal_matrica, j, k, nova_visina, nova_sirina):
                            povrsina -= pravougaonici[i].povrsina()
                            for m in range(j, nova_visina):
                                for n in range(k, nova_sirina):
                                    materijal_matrica[m][n] = i + 1

                            break


                k+=1
                if k == materijal.sirina:
                    k = 0
                    j+=1

    sve_povrsine[hromozom] = povrsina

    if vrati_matricu == True:
        return materijal_matrica
    else:
        return povrsina


def validan_hromozom(pravougaonici, hromozom):
    temp = 0
    for i in range(len(pravougaonici)):
        if hromozom[i] == "1":
            temp += pravougaonici[i].povrsina()

    pm = materijal.povrsina()
    if hromozom in sve_povrsine:
        if sve_povrsine[hromozom] == pm - temp:
            return True
    elif fituj(pravougaonici, hromozom) == pm - temp:
        return True

    return False


def inicijalizuj_populaciju(velicina_populacije, broj_jedinki, pravougaonici):
    populacija = []
    while len(populacija) < velicina_populacije:
        novi_string = "".join(random.choice("01") for _ in range(broj_jedinki))

        if validan_hromozom(pravougaonici, novi_string):
            populacija.append(novi_string)


    return populacija


def turnir_selekcija(populacija, broj_jedinki, pravougaonici):
    def func(x):
        return fituj(pravougaonici, x)

    roditelji = random.sample(populacija, broj_jedinki)

    return min(roditelji, key=func)


def prirodna_selekcija(jedinke,broj_jedinki):

    return jedinke[:broj_jedinki]

def sortiranje(jedinke,pravougaonici):

    jedinke = sorted(jedinke,key=lambda x: fituj(pravougaonici,x))
    return jedinke


def rulet_selekcija(roditelji):
    parovi = []
    i = 0

    for i in range(0, len(roditelji), 2):

        sanse = []
        for i in range(len(roditelji)):
            sanse.append((len(roditelji) - i) * random.random())
        if (sanse[0] >= sanse[1]):
            max1 = 0
            max2 = 1
        else:
            max1 = 1
            max2 = 0

        for i in range(2, len(roditelji)):
            if sanse[i] > sanse[max1]:
                max2 = max1
                max1 = i
            elif sanse[i] > sanse[max2]:
                max2 = 1
        parovi.append([roditelji[max1], roditelji[max2]])

    return parovi

def ukrstanje(parovi, pravougaonici):
    duzina = len(parovi[0][0])
    deca = []

    for (a,b) in parovi:
        while True:
            r1 = random.randrange(0, duzina)
            r2 = random.randrange(0, duzina)

            if r1 < r2:
                d1 = a[:r1] + b[r1:r2] + a[r2:]
                d2 = b[:r1] + a[r1:r2] + b[r2:]

                if validan_hromozom(pravougaonici, d1) and validan_hromozom(pravougaonici, d2):
                    deca.append(d1)
                    deca.append(d2)
                    break
            else:
                d1 = a[:r2] + b[r2:r1] + a[r1:]
                d2 = b[:r2] + a[r2:r1] + b[r1:]
                if validan_hromozom(pravougaonici, d1) and validan_hromozom(pravougaonici, d2):
                    deca.append(d1)
                    deca.append(d2)
                    break

    return deca

def inv_mutacija(jedinke, procenat, pravougaonici):

    mutirane_jedinke = []

    for jedinka in jedinke:
        while True:
            if random.random() < procenat and len(jedinka) > 1:
                r1 = random.randrange(0, len(jedinka) - 1)
                r2 = random.randrange(0, len(jedinka) - 1)

                if r1 < r2:
                    m = jedinka[:r1] + jedinka[r1:r2][::-1] + jedinka[r2:]
                    if validan_hromozom(pravougaonici, m):
                        mutirane_jedinke.append(m)
                        break
                else:
                    m = jedinka[:r2] + jedinka[r2:r1][::-1] + jedinka[r1:]
                    if validan_hromozom(pravougaonici, m):
                        mutirane_jedinke.append(m)
                        break

            else:
                mutirane_jedinke.append(jedinka)
                break

    return mutirane_jedinke

def elitis(stare_jedinke, mutirane_jedinke, elitis_rate, population_size):
    old_ind_size = int(np.round(population_size * elitis_rate))
    return stare_jedinke[:old_ind_size] + mutirane_jedinke[:(population_size - old_ind_size)]

def cost(pravougaonici, hromozom):
    return fituj(pravougaonici, hromozom) / materijal.povrsina()


def draw_rectangle(matrix):
    # Create a color map to map values to colors
    cmap = plt.get_cmap('jet')
    # Normalize the matrix values to the range [0, 1]
    norm = plt.Normalize(vmin=np.min(matrix), vmax=np.max(matrix))
    # Create a figure
    fig, ax = plt.subplots()
    # Plot the matrix as a rectangle with each element represented as a square
    ax.imshow(matrix, cmap=cmap, norm=norm)
    # Remove the axis labels
    ax.set_xticks([])
    ax.set_yticks([])
    # Create a custom legend
    unique_values = np.unique(matrix)
    patches = []
    for value in unique_values:
        color = cmap(norm(value))
        patches.append(mpatches.Patch(color=color, label=str(int(value))))
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # Display the figure
    plt.show()

def procenat_ostatka(pravougaonici, hromozom):

    if hromozom in sve_povrsine:
        return sve_povrsine[hromozom] / materijal.povrsina() * 100
    else:
        return fituj(pravougaonici, hromozom) / materijal.povrsina() * 100

if __name__ == '__main__':

    aplikacija = InputForm()
    aplikacija.mainloop()

    gui_pravougaonici = aplikacija.isecci
    materijal = Pravougaonik(eval(aplikacija.sirina_materijala), eval(aplikacija.visina_materijala))

    pravougaonici = []
    for p in gui_pravougaonici:
        pravougaonici.append(Pravougaonik(eval(p[0]), eval(p[1])))


    populacija = inicijalizuj_populaciju(10, len(pravougaonici), pravougaonici)

    a = []

    konvergencija = 0

    for i in range(100):
        jed = sortiranje(populacija, pravougaonici)
        jedinke = prirodna_selekcija(jed, 6)
        parovi = rulet_selekcija(jedinke)
        ukrsteni = ukrstanje(parovi, pravougaonici)
        populacija = inv_mutacija(ukrsteni, 0.9, pravougaonici)
        populacija = sortiranje(populacija, pravougaonici)
        populacija = elitis(jed, populacija, 0.1, len(populacija))
        a.append(populacija)
        if (cost(pravougaonici, populacija[0]) < 0.05):
            konvergencija += 1

        if konvergencija > 20:
            break


    print("Procenat preostale povrsine: ", procenat_ostatka(pravougaonici, populacija[0]))
    draw_rectangle(fituj(pravougaonici, populacija[0], True))
