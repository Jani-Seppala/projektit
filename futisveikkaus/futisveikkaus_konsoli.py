import sqlite3
import pandas as pd
import bcrypt
import getpass
import admin


def luo_yhteys():
    """Luodaan tietokanta sekä yhteys siihen. Tämän jälkeen tietokantaan lisätään hieman täytedataa"""
    global CONN
    CONN = sqlite3.connect(':memory:')

    global CUR
    CUR = CONN.cursor()
    CUR.executescript("""CREATE TABLE IF NOT EXISTS tulokset(
                            tulos_id INTEGER PRIMARY KEY,
                            ottelupari text,
                            tulos text DEFAULT NULL,
                            pelattu text DEFAULT NULL                        
                );

                CREATE TABLE IF NOT EXISTS osallistujat(
                            osallistuja_id INTEGER PRIMARY KEY,
                            osallistuja text UNIQUE,
                            pisteet integer DEFAULT 0

                );
                CREATE TABLE IF NOT EXISTS veikkaukset(
                            veikkaus_id INTEGER PRIMARY KEY,
                            osallistuja_id integer,
                            tulos_id integer,
                            veikkaus text,
                            FOREIGN KEY (osallistuja_id) REFERENCES osallistujat (osallistuja_id),
                            FOREIGN KEY (tulos_id) REFERENCES tulokset (tulos_id)
                );
                """)

    Ottelu_lista = [('Rus-Sau', '5-0'), ('Egt-Uru', '0-1'), ('Mor-Ira', '0-1'), ('Por-Spa', '3-3'), ('Fra-Aus', None),
                    ('Arg-Ice', None), ('Per-Den', None), ('Cro-Nig', None), ('Cos-Ser', None), ('Ger-Mex', None)]

    Osallistujat_lista = [('Kingis',), ('Matti',), ('Jussi',)]
    Veikkaukset_lista = [(1, 1, '2-0'), (1, 2, '1-2'), (1, 3, '1-1'), (1, 4, '1-2'), (1, 5, '1-1'), (1, 6, '3-1'),
                         (1, 7, '1-2'),
                         (2, 1, '2-0'), (2, 2, '1-3'), (2, 3, '1-1'), (2, 4, '2-1'), (2, 5, '2-0'), (2, 6, '3-0'),
                         (2, 7, '1-2'),
                         (3, 1, '1-1'), (3, 2, '1-2'), (3, 3, '2-1'), (3, 4, '2-2'), (3, 5, '3-0'), (3, 6, '3-1'),
                         (3, 7, '1-1'), ]

    CUR.executemany("INSERT INTO tulokset(ottelupari, tulos) VALUES (?, ?)", Ottelu_lista)
    CUR.executemany("INSERT INTO osallistujat(osallistuja) VALUES (?)", Osallistujat_lista)
    CUR.executemany("INSERT INTO veikkaukset(osallistuja_id, tulos_id, veikkaus) VALUES (?, ?, ?)", Veikkaukset_lista)
    CONN.commit()


def laske_ottelu_pisteet(tulos, veikkaus):
    """ Parametreinä tulos ja veikkaus merkkijonot Esim. "1-2", "0-9", "8-5".
    Laskee ottelun yksiristikaksi tuloksen ja jakaa pisteet sen mukaisesti.
    10-0
    2-10
    """

    pisteet = 0

    tulos_kotimaalit, tulos_vierasmaalit = tulos.split("-")
    veikkaus_kotimaalit, veikkaus_vierasmaalit = veikkaus.split("-")

    if tulos_kotimaalit < tulos_vierasmaalit:
        tulos_yksiristikaksi = "2"
    elif tulos_kotimaalit > tulos_vierasmaalit:
        tulos_yksiristikaksi = "1"
    else:
        tulos_yksiristikaksi = "x"

    if veikkaus_kotimaalit < veikkaus_vierasmaalit:
        veikkaus_yksiristikaksi = "2"
    elif veikkaus_kotimaalit > veikkaus_vierasmaalit:
        veikkaus_yksiristikaksi = "1"
    else:
        veikkaus_yksiristikaksi = "x"

    if veikkaus_yksiristikaksi == tulos_yksiristikaksi:
        pisteet += 1

        if veikkaus_kotimaalit == tulos_kotimaalit:
            pisteet += 1
        if veikkaus_vierasmaalit == tulos_vierasmaalit:
            pisteet += 1

    return pisteet


def paivita_tulos():
    tulos_id = "."
    while tulos_id:
        CUR.execute("SELECT * FROM tulokset")
        data = CUR.fetchall()

        id_lista = []
        for rivi in data:
            print(rivi)
            if rivi[0] not in id_lista:
                id_lista.append(str(rivi[0]))

        print("Anna sen ottelun id numero, minkä haluat päivittää")
        print("Palaa alkuvalikkoon painamalla enteriä")
        tulos_id = input('Ottelun id numero:').strip()

        if tulos_id in id_lista:
            paivita_tulos_lista = tarkista_syote()

            sql_update_tulos_query = "UPDATE tulokset SET tulos = ? WHERE tulos_id = ?"
            tulos_data = (paivita_tulos_lista, tulos_id)
            CUR.execute(sql_update_tulos_query, tulos_data)
            CONN.commit()

            print(f"Ottelu id {tulos_id} päivitetty tuloksella {paivita_tulos_lista}")

        elif tulos_id == "":
            return

        else:
            print("Ottelun id:tä ei löydy")


def lisaa_ottelu():
    ottelu_lista = []

    while True:
        koti = input("Kotijoukkue: ")
        vieras = input("Vierasjoukkue: ")
        if not koti:
            break
        elif 0 < len(koti) < 50 and 0 < len(vieras) < 50:
            ottelu_lista.append((f'{koti}-{vieras}',))
            print(f"Lisätty ottelu: {koti}-{vieras}")
        else:
            print("Joukkueiden nimien pituus täytyy olla 1-50 merkin väliltä!")

    sql_lisaa_ottelu_query = "INSERT INTO tulokset(ottelupari) VALUES (?)"
    data = ottelu_lista
    CUR.executemany(sql_lisaa_ottelu_query, data)


def tarkista_syote():
    print("Anna ensiksi kotijoukkueen maalimäärä, paina enteriä ja tämän jälkeen vierasjoukkueen maalimäärä")
    print("Maalimäärien täytyy olla positiivisia kokonaislukuja väliltä 0-99")

    while True:
        kotimaalit = input('Kotijoukkueen maalit:').strip()
        vierasmaalit = input('Vierasjoukkueen maalit:').strip()

        if kotimaalit.isdigit() and vierasmaalit.isdigit():
            if 0 <= int(kotimaalit) <= 99 and 0 <= int(vierasmaalit) <= 99:
                tulos_str = f"{kotimaalit}-{vierasmaalit}"
                return tulos_str
            else:
                print('Maalimäärät virheellisiä')
        else:
            print('virheellinen syöte')


def laske_yhteispisteet():
    """Laskee yhteispisteet kaavalla, joka selviää readme:stä. Lisää pelattuihin otteluihin <pelattu> booleanin
     jolla tarkistetaan että peli on pelattu ja näin ollen siitä tulevia pisteitä ei lasketa enää uudestaan kahteen
     kertaan"""
    tulokset = CUR.execute("SELECT * FROM tulokset")
    tulokset = tulokset.fetchall()

    veikkaukset = CUR.execute("SELECT * FROM veikkaukset")
    veikkaukset = veikkaukset.fetchall()

    for tulosrivi in tulokset:
        pelattu_switch = tulosrivi[3]
        tulos = tulosrivi[2]
        tulokset_tulos_id = tulosrivi[0]

        if not tulos:
            continue

        elif not pelattu_switch:
            sql_update_pelattu_query = "UPDATE tulokset SET pelattu = ? WHERE tulos_id = ?"
            pelattu_data = (True, tulokset_tulos_id)
            CUR.execute(sql_update_pelattu_query, pelattu_data)
            CONN.commit()

        else:
            continue

        for veikkausrivi in veikkaukset:
            veikkaajan_id = veikkausrivi[1]
            veikkaukset_tulos_id = veikkausrivi[2]
            veikkaus = veikkausrivi[3]
            if tulokset_tulos_id == veikkaukset_tulos_id:
                print("------------")

                sql_osallistuja_nimi_query = "SELECT osallistuja FROM osallistujat WHERE osallistuja_id = ?"
                data = (veikkaajan_id,)
                sql_exe = CUR.execute(sql_osallistuja_nimi_query, data)
                sql_exe = sql_exe.fetchone()

                print(f"{sql_exe} veikkaus {veikkaus} otteluun {tulosrivi[1]}, tulos {tulos}")

                pisteet = laske_ottelu_pisteet(tulos, veikkaus)

                if pisteet > 0:

                    print(f"lisätään {pisteet} pistettä osallistuja id:lle {sql_exe}")

                    # HAE tämän hetkisen osallistujan pistetiedot ja päivitä ne
                    sql_paivita_pisteet_query = "UPDATE osallistujat SET pisteet = pisteet + ? WHERE osallistuja_id = ?"
                    paivita_pisteet_data = (pisteet, veikkaajan_id)
                    CUR.execute(sql_paivita_pisteet_query, paivita_pisteet_data)
                    CONN.commit()

                else:
                    print("Ei pisteitä...")

    CUR.execute("SELECT * FROM osallistujat")
    print(CUR.fetchall())

    CUR.execute("SELECT * FROM tulokset")
    print(CUR.fetchall())


def tulosta_tiedot(syote):
    if syote == 'p':
        print(pd.read_sql_query("SELECT osallistuja, pisteet FROM osallistujat ORDER BY pisteet DESC", CONN,
                                index_col="osallistuja"))
    elif syote == 't':
        print(pd.read_sql_query("SELECT ottelupari FROM tulokset", CONN))


def luo_osallistuja():
    while True:
        luotu_nimi = input("Anna nimi/nick jolla osallistut kisaan: ")

        if len(luotu_nimi) < 20 and luotu_nimi:

            try:
                sql_luo_osallistuja_query = "INSERT INTO osallistujat(osallistuja) VALUES (?)"
                osallistuja_data = (luotu_nimi,)
                CUR.execute(sql_luo_osallistuja_query, osallistuja_data)
                CONN.commit()
                break

            except sqlite3.Error:
                print("Nimi on jo käytössä")

        else:
            print("Nimi ei saa olla tyhjä ja sen maksimipituus on 20 merkkiä")

    sql_valitse_osallistuja_query = "SELECT osallistuja_id FROM osallistujat WHERE osallistuja = ?"
    CUR.execute(sql_valitse_osallistuja_query, osallistuja_data)
    uusi_osallistuja_id = CUR.fetchone()
    luo_veikkaus(uusi_osallistuja_id[0])


def luo_veikkaus(uusi_osallistuja_id):
    sql_hae_tulokset_query = "SELECT tulos_id, ottelupari FROM tulokset"
    CUR.execute(sql_hae_tulokset_query)
    data = CUR.fetchall()

    print(pd.read_sql_query(sql_hae_tulokset_query, CONN, index_col="tulos_id"))

    osallistujan_veikkaukset = []
    for ottelu in data:
        ottelupari = ottelu[1]
        otteluid = ottelu[0]
        print(f"Anna veikkaus ottelulle {ottelupari}: ")
        osallistujan_veikkaus = tarkista_syote()

        osallistujan_veikkaukset.append((uusi_osallistuja_id, otteluid, osallistujan_veikkaus))

    sql_tallenna_veikkaukset_query = "INSERT INTO veikkaukset(osallistuja_id, tulos_id, veikkaus) VALUES (?, ?, ?)"
    CUR.executemany(sql_tallenna_veikkaukset_query, osallistujan_veikkaukset)


def admin_kirjautuminen():
    """Kommentoitu pois salasana kirjautuminen, jos sitä halutaan käyttää, löytyy salasana admin.py filusta"""
    # while True:
    #     print('----------------------------')
    #     text_pwd = input("Anna salasana tai palaa alkuvalikkoon painamalla enteriä")
    #     text_pwd = bytes(text_pwd, encoding='utf8')
    #
    #     if bcrypt.checkpw(text_pwd, admin.hash_salasana):
    #         print('match')
    while True:
        print('--------ADMIN-PANEELI----------')
        print('Voit joko lisätä uusia otteluita, päivittää tuloksia tai tulostaa ottelulistan')
        print('Palaa alkuvalikkoon painamalla enteriä')
        print('(L)isää uusi ottelu')
        print('(P)äivitä ottelun tulos')
        print('(T)ulosta ottelulista')
        print('Laske (Y)hteispisteet')
        muokkaus_syote = input('Tee valintasi').lower()
        if muokkaus_syote == 'p':
            paivita_tulos()
        if muokkaus_syote == 'y':
            laske_yhteispisteet()
        elif muokkaus_syote == 'l':
            lisaa_ottelu()
        elif muokkaus_syote == 't':
            tulosta_tiedot(muokkaus_syote)
        elif muokkaus_syote == '':
            return
        else:
            print("Laiton valinta")


# elif not text_pwd:
#     break
#
# else:
#     print('no match')


def main():
    """Tässä demotyön versiossa luomme tietokannan joka kerta muistiin ja se nollautuu kun ohjelma suljetaan
    Lopullisessa versiossa tietokanta tallennetaan kovalevylle/pilveen."""
    luo_yhteys()
    while True:
        print('----------------------------')
        print('Tervetuloa Futisveikkaukseen.')
        print('(O)sallistu veikkaukseen')
        print('(P)istetilanne')
        print('(Q)uit')
        print('(A)dmin kirjautuminen')
        syote = input('Tee Valintasi.').lower()

        if syote == 'o':
            luo_osallistuja()
        elif syote == 'p':
            tulosta_tiedot(syote)
        elif syote == 'q':
            break
        elif syote == 'a':
            admin_kirjautuminen()

        else:
            print('Laiton valinta')


if __name__ == '__main__':
    main()
