JALKAPALLON ARVOKISOJEN PISTEVEIKKAUS APP

Konsoliappsi jalkapallon arvokisojen pistelaskuun. Osallistujat veikkaavat turnauksen alkusarjan otteluiden tuloksia. Veikkausten perusteella jaetaan pisteitä ja
eniten pisteitä saanut voittaa kilpailun alkusarjan päätyttyä. Osallistujat voivat seurata miten pistetilanne kehittyy jokaisen pelipäivän jälkeen.

OHJEET:

Ohjelma käynnistetään suorittamalla futisveikkaus_konsoli.py, avautuvasta käyttöliittymästä voidaan luoda uusia osallistujia tai katsoa pistetilannetta.
Admin käyttöliittymässä voidaan lisätä ja päivittää otteluita sekä laskea osallistujien pisteitä. Admin.py tiedostoa ja admin_kirjautuminen() funktiota muokkaamalla
voi halutessaan luoda Admin-paneeliin kirjautumiseen salasanan. Appsiin on laitettu hieman täytedataa, mutta ne voi halutessaan poistaa ja luoda oman puhtaan tietokannan.

PISTEIDEN LASKUN KAAVA:

Ottelun lopputilanteen (kotijoukkueen voitto, tasapeli, vierasjoukkueen voitto) oikein arvaamisesta saa 1p ja mikäli lopputilanne oikein niin 1p per oikea maalimäärä. Max 3p / ottelu

Esimerkiksi Suomi – Belgia päättyy 3 – 2

Käyttäjä A arvasi 4 – 2, jolloin saa 2p arvauksesta (1p voittajan arvaamisesta ja 1p vierasjoukkueen maalimäärästä)
Käyttäjä B arvasi 3 – 3, jolloin saa 0p arvauksesta, koska voittaja/tasuri arvaus väärin niin ei tule maalimäärästä pisteitä
Käyttäjä C arvasi 1- 0, jolloin saa 1p arvauksesta, koska voittaja/tasuri oikein

TEKNIIKAT:

Python 3
SQLite