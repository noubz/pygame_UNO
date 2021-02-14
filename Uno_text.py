# Uno-Textverarbeitung von Niclas Berger
import random

# Tuples und Funktion, um UNO-Deck zu erstellen
normale_nummern = ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "Seitenwechsel", "+2", "Aussetzen")
normale_farben = ("Blau", "Rot", "Grün", "Gelb")
spezial_karten = ("Farbenwahl", "+4")
def generiereNeuesDeck():
    deck = []

    # For-Schleifen um alle Karten zum Deck hinzuzufügen
    for _ in range(2):
        for farbe in normale_farben:
            for nummer in normale_nummern:
                deck.append((farbe, nummer))

    for _ in range(4):
        for karte in spezial_karten:
            deck.append(("Schwarz", karte))

    random.shuffle(deck) # Die generierten Karten werden gemischt
    return deck

# Für jeden Spieler eine Hand mit x Karten erstellen
def erstelleHand(spieler, karten):
    alleHaende = []

    for _ in range(spieler): # Schleife für jede Hand
        hand = []

        for i in range(karten): # Schleife Spielerkarten
            karte = random.randint(0, len(ziehstapel) - 1)
            hand.append(ziehstapel[karte])
            ziehstapel.pop(karte)

        alleHaende.append(hand) # Hinzufügen der Hand zu spielerHaende

    return alleHaende

# Eine Karte vom Ziehstapel auf einen Stapel ziehen
def ziehen(stapel, anzahl=1):
    for i in range(anzahl):
        stapel.append(ziehstapel[0])
        ziehstapel.pop(0)

# Nächsten Spieler einstellen
def naechsterSpieler():
    global aktuellerSpieler
    aktuellerSpieler += 1 if not seitenwechsel else -1

    if aktuellerSpieler == -1:
        aktuellerSpieler = len(spielerNamen) - 1
    elif aktuellerSpieler == len(spielerNamen):
        aktuellerSpieler = 0

# Nächsten Spielernamen zurückgeben
def nextSpielername(züge=1):
    global aktuellerSpieler
    nextSpieler = aktuellerSpieler

    for i in range(züge):
        nextSpieler += 1 if not seitenwechsel else -1

        if nextSpieler == -1:
            nextSpieler = len(spielerNamen) - 1
        elif nextSpieler == len(spielerNamen):
            nextSpieler = 0

    return nextSpieler

# Prüfen, ob Karte abgelegt werden kann und Karte ablegen
def karteAblegenZiehen(Hand, abzulegende_Karte):
    zug_Möglich = False
    newCard = True

    # Karte ziehen
    if abzulegende_Karte == -1:
        ziehen(Hand)
        zug_Möglich = True
        newCard = False

    
    else: # Versuch Karte abzulegen
        kartenFarbe,kartenNummer = Hand[abzulegende_Karte] # Farbe und Nummer trennen
        ablageFarbe,ablageNummer = ablagestapel[0] # Farbe und Nummer trennen

        if kartenFarbe == ablageFarbe or kartenNummer == ablageNummer or kartenFarbe == "Schwarz":
            zug_Möglich = True
            if kartenNummer == "+4":
                for karte in Hand:
                    if ablageFarbe == karte[0] or ablageNummer == karte[1]: 
                        zug_Möglich = False

            if zug_Möglich:
                ablagestapel.insert(0, Hand[abzulegende_Karte])
                Hand.pop(abzulegende_Karte)

    return zug_Möglich, newCard

# Prüfen, ob Karte eine Spezialkarte ist
def istSpezialkarte(karte):
    if karte[0] == "Schwarz" or karte[1] in ["Aussetzen", "+2", "Seitenwechsel", "Farbenwahl", "+4"]:
        return True
    return False

# Spezialkarte verarbeiten
def Spezialkarte(Hand, x, first=False):
    from main import Farbenwahl, screen
    global seitenwechsel

    kartenFarbe,kartenNummer = ablagestapel[0]

    if kartenFarbe == "Schwarz":
        farbe = Farbenwahl.run(x, screen.height / 2.3, screen.width / 6.67) if not first else random.choice(normale_farben)
        ablagestapel[0] = (farbe, kartenNummer)

        if kartenNummer == "+4":
            if not first: naechsterSpieler()
            ziehen(Hand[aktuellerSpieler], 4)
            if first: naechsterSpieler()

    elif kartenNummer == "Seitenwechsel": seitenwechsel = not seitenwechsel
    elif kartenNummer == "Aussetzen": naechsterSpieler()
    elif kartenNummer == "+2":
        if not first: naechsterSpieler()
        ziehen(Hand[aktuellerSpieler], 2)
        if first: naechsterSpieler()


# Start-Funktion für UNO
# Initialisiert Variablen für Uno
def start(spieler, karten):
    """ (args)
    spieler = Spielernamen
    karten = Kartenanzahl
    """
    global ziehstapel
    global ablagestapel
    global spielerHand
    global aktuellerSpieler
    global spielerNamen
    global seitenwechsel

    ziehstapel = generiereNeuesDeck()
    ablagestapel = []

    aktuellerSpieler = 0
    seitenwechsel = False

    spielerNamen = spieler
    spielerHand = erstelleHand(len(spielerNamen), karten)
    
    # Anfangskarte aufdecken
    ziehen(ablagestapel)

    # Anfangskarte auf Spezialkarte Testen und Verarbeiten
    if istSpezialkarte(ablagestapel[0]):
        Spezialkarte(spielerHand, None, True)

    spielerHand[aktuellerSpieler].sort()

# Zug-Funktion für UNO
def zug(karte, x):
    """ (args)
    karte = index der Karte in Spielerhand
    x = x-Koordinate der Karte (für Farbenwahl)
    """
    global ablagestapel
    global ziehstapel

    gewonnen = False
    zug_Möglich, newCard = karteAblegenZiehen(spielerHand[aktuellerSpieler], karte)

    # Prüfen, ob Spieler gewonnen hat
    if len(spielerHand[aktuellerSpieler]) == 0:
        gewonnen = True

    # Falls Zug möglich
    elif zug_Möglich:
        # Auf Spezialkarte prüfen und verarbeiten
        if istSpezialkarte(ablagestapel[0]) and newCard:
            Spezialkarte(spielerHand, x)

        # ggf. Ziehstapel nachfüllen
        if len(ziehstapel) == 0:
            ziehstapel = ablagestapel[1:]
            ablagestapel = [ablagestapel[0]]

            random.shuffle(ziehstapel)

        naechsterSpieler()
        spielerHand[aktuellerSpieler].sort()

    return zug_Möglich, gewonnen