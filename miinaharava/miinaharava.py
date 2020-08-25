from random import randint
import time
import haravasto
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITET_DIR = os.path.join(BASE_DIR, 'spritet')

Hiiri = {
    haravasto.HIIRI_VASEN: 'vasen',
    haravasto.HIIRI_KESKI: 'keski',
    haravasto.HIIRI_OIKEA: 'oikea'
}

tila = {
    'pvm': 0,
    'kello': 0,
    'minuutit': 0,
    'sekunnit': 0,
    'miina': 0,
    'vuorot': 0,
    'tulos': None,
    'piilokentta': None,
    'nakyvakentta': None,
    'jaljella': None,
    'aika': 0
}


def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin. kutsuu käyttäjän painalluksesta riippuen joko
    hiiri_vasen tai hiiri_oikea funktiota ja laskee pelin lopetus-ehdon.
    """
    # Tarkastetaan onko tilasanakirjan tulos arvo muuttunut, jos on, kysytään haluaako käyttäjä aloittaa uuden pelin.
    if tila['tulos'] != None:
        tila['tulos'] = None
        tila['vuorot'] = 0
        haravasto.lopeta()

        while True:
            valinta = input('Uusi peli? K/E.').lower()
            if valinta == 'k':
                aloita_peli()
            elif valinta == 'e':
                exit()
            else:
                print('laiton valinta')
    # Muuntaa hiiren sijainnin kentälle sopiviksi koordinaateiksi
    x = int(x / 40)
    y = int(y / 40)
    if Hiiri[nappi] == 'vasen':
        hiiri_vasen(x, y)
    elif Hiiri[nappi] == 'oikea':
        hiiri_oikea(x, y)
    # Käydään läpi for loopilla tyhjat_ruudut lista, joka sisältää piiloitetun kentän tyhjät ruudut.
    # silmukkamuuttuja tyhja sisältää koordinaattiparin joka sijoitetaan näkyvään kenttään ja tarkastellaan
    # onko näkyvässä kentässä sillä kohtaa jotain muuta kuin avaamaton ruutu. Jos on, tarkastellaan vielä onko samassa
    # kohtaa jotain muuta kuin lippu, jos on, lisätään count muuttujan arvoa yhdellä. Näin saadaan tietoon ovatko
    # näkyvän kentän avaamattomat tai liputetut ruudut samoissa koordinaateissa kuin piiloitetun kentän miinat
    count = 0
    for tyhja in aseta_numerot():
        if tila['nakyvakentta'][tyhja[0]][tyhja[1]] != ' ':
            if tila['nakyvakentta'][tyhja[0]][tyhja[1]] != 'f':
                count += 1
    # Jos count muuttuja on yhtäsuuri kuin kentän dimensiot vähennettynä miinojen määrä (eli pelaaja voittaa pelin jos
    # näkyvällä kentällä on jäljellä avaamattomia tai liputettuja ruutuja yhtä monta kuin piiloitetulla kentällä on
    # miinoja ja ne sijaitsevat samoilla koordinaateilla) pelaaja voittaa pelin.
    if count == (len(tila['nakyvakentta']) * len(tila['nakyvakentta'][0]) - tila['miina']):
        print('Voitit!')
        print('Klikkaa peli-ikkunaa jatkaaksesi')
        tila['tulos'] = 'Voitto'
        tallenna_tilastot('tilastot.csv')


def hiiri_vasen(x, y):
    """
    Hiiren vasemmasta napista tapahtuvat asiat
    """
    if tila['nakyvakentta'][y][x] != ' ':
        print('Ruutu on valittu jo')
    elif tila['piilokentta'][y][x] == 'x':
        tila['nakyvakentta'][y][x] = tila['piilokentta'][y][x]
        print('Ruudussa oli miina. Hävisit!')
        print('Klikkaa peli-ikkunaa jatkaaksesi')
        tila['vuorot'] += 1
        tila['tulos'] = 'Häviö'
        tallenna_tilastot('tilastot.csv')
    elif tila['piilokentta'][y][x] == '0':
        tulvataytto(y, x)
        tila['vuorot'] += 1
    else:
        tila['nakyvakentta'][y][x] = tila['piilokentta'][y][x]
        tila['vuorot'] += 1


def hiiri_oikea(x, y):
    """
    Hiiren oikeasta napista tapahtuvat asiat
    """
    if tila['nakyvakentta'][y][x] == ' ':
        tila['nakyvakentta'][y][x] = 'f'
    elif tila['nakyvakentta'][y][x] == 'f':
        tila['nakyvakentta'][y][x] = ' '
    else:
        print('Valittuun ruutuun ei voi laittaa lippua.')


def tallenna_tilastot(tiedosto):
    """
    Ensiksi funktio lopettaa ajanoton ja laskee minuutit ja sekunnit tila-sanakirjaan. Tila-sanakirjasta poistetaan
    aika' ja 'jaljella' avain. Tämän jälkeen tila-sanakirjaa käydään läpi for loopilla ja sen avain-arvo parit
    tallennetaan 'tilastot.csv' tiedostoon.
    """
    tila['minuutit'], tila['sekunnit'] = divmod(int(time.time() - tila['aika']), 60)
    del tila['aika']
    del tila['jaljella']
    with open(tiedosto, "a+") as kohde:
        for tilasto in tila:
            print(tilasto, tila[tilasto])
            kohde.write("{}: {}\n".format(tilasto, tila[tilasto]))


def lataa_tilasto(tiedosto):
    """
    Lataa 'tilastot.csv' tiedoston ja avaa sen pelaajalle ihasteltavaksi.
    """
    try:
        with open(tiedosto) as lahde:
            for i in lahde.readlines():
                i = i.strip()
                print(i)
    except FileNotFoundError:
        print('Tiedostoa ei ole olemassa tai sitä ei voitu avata.')


def aika():
    """
    Mittaa pelissä kuluneen ajan
    """
    tila['aika'] = time.time()
    tila['pvm'] = time.strftime('%d.%m.%Y', time.localtime())
    tila['kello'] = time.strftime('%H:%M:%S', time.localtime())


def tulvataytto(y, x):
    """
    Vertailee piilokentän ja näkyvankentän arvoja keskenään ja sijoittaa piilokentän arvoja näkyvään kenttään, mikäli
    arvo on tyhjä tai numeroitu ruutu. Pelaajan klikatessa tyhjää ruutua, tapahtuu ketjureaktio mikä avaa näkyvän
    kentän viereiset ruudut joka suuntaan niin pitkälle kunnes törmätään piilokentän numeroituihin ruutuihin.
    """
    newlist = [(y, x)]
    while newlist != []:
        pop1, pop2 = newlist.pop()
        if tila['piilokentta'][pop1][pop2] == '0':
            for r, c in tutki_naapurit(pop1, pop2):
                if tila['nakyvakentta'][r][c] == ' ':
                    tila['nakyvakentta'][r][c] = tila['piilokentta'][r][c]
                    newlist.append((r, c))


def miinoita():
    """
    Asettaa kentälle käyttäjän valitseman määrän miinoja satunnaisiin paikkoihin.
    """
    for i in range(tila['miina']):
        i = tila['jaljella'][randint(0, len(tila['jaljella']) - 1)]
        tila['piilokentta'][i[0]][i[1]] = 'x'
        tila['jaljella'].remove(i)


def aseta_numerot():
    """
    numeroi piilokentän miinojen viereiset alueet ruudun ympäröivän miinojen määrällä
    """
    tyhjat = []
    for rivinro, rivi in enumerate(tila['piilokentta']):
        for sarakenro, solu in enumerate(rivi):
            if solu != 'x':
                tyhjat.append((rivinro, sarakenro))     # lisää piilokentän tyhjät ruudut listaan
    for r, c in tyhjat:
        val = [tutki_naapurit(r, c)]    # palauttaa koordinaatit eikä solua
        count = 0
        for i, j in val[0]:     # käydään saadut koordinaatit läpi ja lasketaan niissä olevat miinat
            if tila['piilokentta'][i][j] == 'x':
                count += 1
            tila['piilokentta'][r][c] = str(count)
    return tyhjat


def tutki_naapurit(y, x):
    """
    Funktio laskee kentän dimensiot ja tämän jälkeen hakee valitun koordinaatin ympäriltä 9 kpl koordinaatteja
    itsensä mukaan lukien, tämän jälkeen tehdään tarkistus että koordinaatit sijaitsevat kentän sisällä ja palautetaan
    kyseiset koordinaatit.
    """
    # Otettu mallia https://gist.github.com/mohd-akram/3057736.
    rivit = len(tila['nakyvakentta'])
    sarake = len(tila['nakyvakentta'][0])
    naapurit = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if -1 < (y + i) < rivit and -1 < (x + j) < sarake:
                naapurit.append((y + i, x + j))
    return naapurit


def piirra_peli():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(tila['nakyvakentta']):
        for x, merkki in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(merkki, x * 40, y * 40)
            haravasto.piirra_ruudut()


def aloita_peli():
    """
    Kutsuu haravaston funktioita lataamalla kuvat, piirtämällä pelin ja käsittelemällä hiiren painalluksia. Viimeiseksi
    kutsutaan aika-funktiota ja aloitetaan peli.
    """
    luo_kentta()
    haravasto.lataa_kuvat(SPRITET_DIR)
    haravasto.luo_ikkuna(len(tila['nakyvakentta'][0]) * 40, len(tila['nakyvakentta'] * 40))
    haravasto.aseta_piirto_kasittelija(piirra_peli)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    aika()
    haravasto.aloita()


def luo_kentta():
    """
    Kysyy kentän dimensiot, miinojen määrän ja luo kentät.
    """
    # Ohjelma ei hyväksy kentän dimensioiksi negatiivisia lukuja, liukulukuja tai nollaa. Negatiiviset luvut muutetaan
    # positiiviseksi abs metodilla. Lisäksi miinojen määräksi ei hyväksytä nollaa tai suurempaa määrää kuin kentän
    # koko -1.
    while True:
        try:
            korkeus = abs(int(input('Anna kentän korkeus: ')))
            leveys = abs(int(input('Anna kentän leveys: ')))
            if korkeus == 0 or leveys == 0:
                print('Kenttä pitää olla vähintään 1x1 kokoinen')
                continue
            miina = abs(int(input('Anna miinojen määrä: ')))
            if miina >= (korkeus * leveys) or miina == 0:
                print('Miinoja pitää olla minimissään yksi tai maksimissaan kentän koko -1')
                continue
            else:
                break
        except ValueError:
            print('Anna positiivinen kokonaisluku')

    # Luodaan piilossa oleva kenttä joka on miinoitettu ja numeroitu sekä käyttäjälle nakyvissä oleva kenttä joka on
    # tällä hetkellä tyhjä mutta tulee myöhemmin hakemaan arvoja piiloitetusta kentästä sen perusteella mitä käyttäjä
    # valitsee.
    piilokentta = []
    for rivi in range(korkeus):
        piilokentta.append([])
        for sarake in range(leveys):
            piilokentta[-1].append(" ")

    nakyvakentta = []
    for rivi in range(korkeus):
        nakyvakentta.append([])
        for sarake in range(leveys):
            nakyvakentta[-1].append(" ")


    # Luodaan jaljella -niminen lista, jota käytetään apuna piiloitetun kentän miinoitukseen, jotta samoja
    # koordinaatteja ei valittaisi uudelleen
    jaljella = []
    for x in range(korkeus):
        for y in range(leveys):
            jaljella.append((x, y))

    # Sijoitetaan piilokentta, nakyvakentta, jaljella, ja miina arvot tilasanakirjaan
    tila['piilokentta'] = piilokentta
    tila['nakyvakentta'] = nakyvakentta
    tila['jaljella'] = jaljella
    tila['miina'] = miina
    miinoita()
    aseta_numerot()


if __name__ == "__main__":
    # Ohjelma aloitetaan kysymällä käyttäjältä mitä tämä haluaa tehdä, '(U)usi peli' aloittaa uuden pelin,
    # '(T)ilastot' avaa pelattujen pelien tilastoja. '(L)opeta.' lopettaa ohjelman suorituksen.
    print('Tervetuloa pelaamaan miinaharavaa.')
    print('(U)usi peli')
    print('(T)ilastot')
    print('(L)opeta')
    while True:
        syote = input('Tee Valintasi.').lower()
        if syote == 'u':
            aloita_peli()
        elif syote == 't':
            lataa_tilasto('tilastot.csv')
        elif syote == 'l':
            exit()
        else:
            print('Laiton valinta')
