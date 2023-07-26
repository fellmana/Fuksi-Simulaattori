# Fuksi-Simulaattori

Leikkimielinen fuksisimulataattori jossa fuksit yrittävät suunnistaa kumpulan käytävillä luennoille. 
Fuksi on keltainen pallero joka yrittää suunnistaa tavoitteeseensa. Kun simulaattorin eri hahmot törmäävät toisiin voivat he kysellä toisiltaan neuvoa kuinka päästä tavoitteeseensa. Mutta kaikkien neuvot eivät aina ole yhtä hyviä.

## Hahmot

### Fuksi
Fuksi on keltainen pallero joka ei tiedä mihin on menossa. Kun fuksi tormää toiseen henkilöön antaa hän suuntaneuvon joka on lähtökohtaisesti väärään suuntaan. Fuksi liikkuu suoraviivaisesti kunnes törmaa seinään tai toiseen henkilöön joka neuvoo hänelle uuden suunnan.

### Opiskelja (1-5)
Opiskelija (1-5) toimii lähes identtisesti kuin fuksi mutta opiskelija antamat suuntaneuvot ovat lähtökohtaisesti oikeaan suuntaan. Sitä suurempi akateeminenikä sitä parempia neuvoja opiskelija antaa. Opiskelijan tunnistaan sinisesta ulkoasustaan.

### Opiskelija (n>5)
Opiskelja(n) liikkuu painotetun (kohti tavoitettaan) kaksi-uloitteisen satunnaiskulun mukaisesti. Heidät voi tunnistaa hapuleivista ja tärisevistä liikkeistä (Luulin että tällainen sekoilu... ja jne.). Jos heiltä kysyy neuvoja antavat he täysin satunnaisen suunnan. 

### Proffa
Proffat liikkuvat hitaasti käytävillä ilman varsinaista tavoitetta. He käyskentelevät käytävillä miettien ja auttavat opiskelijoita löytäämään oikeaan paikkaan. Jos proffalta kysyy neuvoa osoittavat he suoraan kohti paikkaa johon kyselijä on menossa. Proffa on harmaa ja hieman muita suurempi.

## Käyttöohjeet

### Riippuvuudet (Dependencies)

* pygame 
* numpy 

### Ohjelmant ajaminen (Running program)

```bash 
python fuksi-simulaattori.py
```

## Brief English description


## todos
- Commandline argument parser
- GUI elements(?)
