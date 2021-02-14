# UNO von Niclas Berger
# README-file lesen!

import Uno_text as text # Text-Teil von Uno / Verarbeitung
import pygame, sys

from pygame.locals import * 
from Toolbox import *  # GUI-"Bausteine"

pygame.init()

# dict für alle rgb-Farben, die genutzt werden
farben = {
    # Farbe   ||  R , G , B  |
    "weiß"    : (255,255,255),
    "schwarz" : (  0,  0,  0),
    "rot"     : (204, 44, 22),
    "grün"    : (101,162, 38),
    "blau"    : ( 46, 98,253),
    "gelb"    : (242,230, 18),
    "grau"    : (128,128,128),
    "darkgrau": ( 38, 38, 38),
    "hellgrau": (179,179,179)
}

# dict für alle Sounds, die genutzt werden
sounds = {
    # Soundname   || pygame-Mixer(Sound)
    "button_click": pygame.mixer.Sound('Sounds/Button_Click.wav'),
    "correct"     : pygame.mixer.Sound('Sounds/Correct.wav'),
    "wrong"       : pygame.mixer.Sound('Sounds/Wrong.wav'),
    "gewonnen"    : pygame.mixer.Sound('Sounds/Game_Win.wav')
}

# Uhr/Clock, um die Framerate regulieren
Clock = pygame.time.Clock()
FPS = 60

# Klasse, um das Windows-Fenster zu verwalten
class Screen:
    # Fenster erstellen
    def __init__(self, width, caption='UNO'):
        """ (args)
        width = Fenster-Breite
        caption = Fenster-Überschrift
        """
        self.width = width
        self.height = round(width * 0.75)

        self.surface = pygame.display.set_mode((self.width, self.height)) # "width x height" großes Fenster erstellen
        
        self.caption = caption # Fenster-Überschrift festlegen
        pygame.display.set_icon(pygame.image.load('Images/Uno_icon.png'))

        self.color = farben["grau"] # Allg. Fensterfarbe festlegen

        self.surface.fill(self.color)
        pygame.display.flip()

    # Caption property
    # Eigenschaft mit der man die Fensterüberschrift ändern kann
    @property
    def caption(self):
        str_caption, _ = pygame.display.get_caption()
        return str_caption

    @caption.setter
    def caption(self, caption):
        pygame.display.set_caption(caption)  

    # Fenster schließen/Spiel beenden
    @staticmethod
    def terminate():
        # Daten abspeichern/sichern
        data = open('data.txt', 'w')
        data.write("-".join([str(screen.width), str(Optionen.Master_Volume), str(Optionen.Music_Volume), Spiel.deck]))
        data.close()

        # Fenster schließen/Programm beenden
        pygame.quit()
        sys.exit()

"""
Die folgenden Klassen sind verschiedene Szenen für das Programm
"""

# Haupmenü-Szene
class Hauptmenü:
    def __init__(self):
        screen.caption = 'UNO' # Fenster-Überschrift ändern
        # Hintergrundbild laden und auf die Fenstergröße anpassen
        self.bg = pygame.transform.scale(pygame.image.load('Images/Menu_Background.png'), (screen.width,screen.height))

        rect = pygame.Rect((0,0), (int(screen.width / 5), int(screen.height / 15))) # pygame.Rect-Objekt für einen Knopf(Button)
        # Buttons erstellen
        self.button_Spielen = Button(rect, round(screen.height / 37.5), 'Spielen', (242, 242, 242), farben['rot'], Spiel.run)
        self.button_Optionen = Button(rect, round(screen.height / 37.5), 'Optionen', (242, 242, 242), farben['rot'], Optionen.run)
        self.button_Beenden = Button(rect, round(screen.height / 37.5), 'Zum Desktop', (242, 242, 242), farben['rot'], None)

        # Position der Buttons ändern
        self.button_Spielen.center = (screen.width / 1.9, screen.height / 1.7)
        self.button_Optionen.center = (screen.width / 1.9, screen.height / 1.41)
        self.button_Beenden.center = (screen.width / 1.9, screen.height / 1.2)

    # Main-Funktion
    @classmethod
    def run(cls):
        surf = cls() # Klasse initialisieren

        surf.fadeIn() # Einblendung
        surf.update() # Fenster aktualisieren

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                elif event.type == MOUSEMOTION:
                    # Prüfen, ob Maus auf einem Button ist und diesen markieren
                    if surf.button_Spielen.rect.collidepoint(event.pos) and surf.button_Spielen.hover == False:
                        surf.button_Spielen.hover = True
                    elif surf.button_Optionen.rect.collidepoint(event.pos) and surf.button_Optionen.hover == False:
                        surf.button_Optionen.hover = True
                    elif surf.button_Beenden.rect.collidepoint(event.pos) and surf.button_Beenden.hover == False:
                        surf.button_Beenden.hover = True

                    # Prüfen, ob Maus vom Button herunter ist und markierung entfernen werden muss
                    if not surf.button_Spielen.rect.collidepoint(event.pos) and surf.button_Spielen.hover == True:
                        surf.button_Spielen.hover = False
                    elif not surf.button_Optionen.rect.collidepoint(event.pos) and surf.button_Optionen.hover == True:
                        surf.button_Optionen.hover = False
                    elif not surf.button_Beenden.rect.collidepoint(event.pos) and surf.button_Beenden.hover == True:
                        surf.button_Beenden.hover = False

                # Fallse "Maustaste gedrückt"
                elif event.type == MOUSEBUTTONDOWN:
                    # Prüfen, ob Klick auf einem der Buttons gemacht wurde
                    if surf.button_Spielen.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Spielen.Click(screen.surface)
                        running = False

                    elif surf.button_Optionen.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Optionen.Click(screen.surface)
                        surf = cls()

                    elif surf.button_Beenden.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Beenden.Click(screen.surface)
                        screen.terminate()

            if running: surf.update()
            Clock.tick(FPS) # Framerate begrenzen
    
    # Funktion, um das Fenster neu zu malen/zu aktualisieren
    def update(self):
        # Hintergrundbild
        screen.surface.blit(self.bg, (0,0))

        # Buttons
        screen.surface.blit(self.button_Spielen() , self.button_Spielen.pos)
        screen.surface.blit(self.button_Optionen() , self.button_Optionen.pos)
        screen.surface.blit(self.button_Beenden() , self.button_Beenden.pos)

        pygame.display.update()

    # Einblendung der Szene
    def fadeIn(self):
        # Surface erstellen
        surf = pygame.Surface((screen.width, screen.height))

        # Transparenz des Surface pro Durchgang erhöhen
        for i in range(70):
            surf.set_alpha(i) # Alpha-Wert für Surface einstellen

            # Surfaces auf das transparente Surface "malen"
            surf.blit(self.bg, (0,0))
            surf.blit(self.button_Spielen() , self.button_Spielen.pos)
            surf.blit(self.button_Optionen() , self.button_Optionen.pos)
            surf.blit(self.button_Beenden() , self.button_Beenden.pos)

            # Transparentes Surface auf das Fenster "malen"
            screen.surface.blit(surf, (0,0))
            pygame.display.update()

# Spieleinstellungen-Szene
class Spieleinstellungen:
    def __init__(self):
        screen.caption = 'UNO - Spielvorbereitung' # Fenster-Überschrift ändern

        self.color = farben['darkgrau'] # Szenen-Farbe festlegen

        # Überschrift "Spieleinstellungen"
        self.label_title = Label((0,0), int(screen.width/12.5), 'Spieleinstellungen', farben['hellgrau'], bold=True)
        self.label_title.center = (screen.width / 2, screen.height / 12.5)

        # Restliche Labels in der Szene
        self.label_Spieler = Label((int(screen.width/40), int(screen.height/3.75)), int(screen.height/15), 'Spieler:', farben['hellgrau'])
        self.label_Handkarten = Label((int(screen.width/40), int(screen.height/1.875)), int(screen.height/15), 'Handkarten:', farben['hellgrau'])
        self.label_title_Spielernamen = Label((int(screen.width/2.2), int(screen.height/3.75)), int(screen.height/15), 'Spielernamen', farben['darkgrau'], bold=True)

        # Größe der valueBars ausrechnen
        w = int(screen.width / 6.67)
        h = int(w/3)
        # valueBars für Spieler- und Handkartenanzahl erstellen
        self.valueBar_Spieler = valueBar(pygame.Rect(int(screen.width/3.846),int(screen.height/3.57),w,h), farben['weiß'], farben['rot'], range(1,5), 1)
        self.valueBar_Handkarten = valueBar(pygame.Rect(int(screen.width/3.846),int(screen.height/1.83),w,h), farben['weiß'], farben['rot'], range(3,11), 4)

        # pygame.Rect für den Bestätigen-Button
        rect = pygame.Rect((0,0), (int(screen.width/3), int(screen.height/10)))
        rect.center = (int(screen.width/2), screen.height - int(screen.height/10))
        # Bestätigen-Button "Spiel starten" erstellen
        self.button_Bestätigen = Button(rect, int(screen.height/18.75), 'Spiel starten', farben['hellgrau'], farben['schwarz'], None, font='Comic Sans MS')

        # Listen für textBoxen (für Spielernamen) und Labels (vor textBoxen) erstellen
        self.textBoxes_Spielernamen = []
        self.labels_Spielernamen = []
        # x,y Startwert ausrechnen und for-Loop für alle 4 Spieler
        x,y = (int(screen.width/2.083), int(screen.height/2.73))
        for spieler in range(1,5):
            # Label (Spieler x:) und textBox erstellen
            self.labels_Spielernamen.append(Label((x,y), int(screen.height/21.43), 'Spieler {}:'.format(spieler), farben['darkgrau']))
            self.textBoxes_Spielernamen.append(textBox(pygame.Rect(x+int(screen.width/6.67), y, int(screen.width/3.3), int(screen.height/18.75)), farben['weiß'], farben['schwarz'], 20))
            
            y += round(screen.height / 12.5) # y-Wert erhöhen

    # Main-Funktion
    @classmethod
    def run(cls):
        surf = cls() # Klasse initialisieren

        spielernamen = [] # Liste für Spielernamen
        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                elif event.type == MOUSEMOTION:
                    # Prüfen, ob Maus auf/oder nicht auf einer valueBar
                    for valueBar in [surf.valueBar_Spieler, surf.valueBar_Handkarten]:
                        if valueBar.button_left_rect.collidepoint(event.pos):
                            valueBar.button_left.hover = True
                        elif valueBar.button_right_rect.collidepoint(event.pos):
                            valueBar.button_right.hover = True

                        elif valueBar.button_left.hover: valueBar.button_left.hover = False
                        elif valueBar.button_right.hover: valueBar.button_right.hover = False

                    # Prüfen, ob Maus auf Bestätigen-Button
                    if surf.button_Bestätigen.rect.collidepoint(event.pos):
                        surf.button_Bestätigen.hover = True
                    elif surf.button_Bestätigen:
                        surf.button_Bestätigen.hover = False

                # Falls "Mausklick"
                elif event.type == MOUSEBUTTONDOWN:
                    # Prüfen, ob Mausklick auf einer valueBar
                    for valueBar in [surf.valueBar_Spieler, surf.valueBar_Handkarten]:
                        if valueBar.button_left_rect.collidepoint(event.pos):
                            pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                            valueBar.button_left.Click(valueBar, screen.surface)
                        elif valueBar.button_right_rect.collidepoint(event.pos):
                            pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                            valueBar.button_right.Click(valueBar, screen.surface)

                    # Prüfen, ob Mausklick auf einer textBox
                    for textBox in surf.textBoxes_Spielernamen:
                        if textBox.rect.collidepoint(event.pos):
                            textBox.run(screen.surface) # textBox starten

                    if surf.button_Bestätigen.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Bestätigen.Click(screen.surface)

                        valid = True # Gibt an, ob alle Eingaben gültig sind
                        spielernamen = [] # Liste mit Spielernamen leeren
                        # Spielernamen auslesen
                        for textBox in surf.textBoxes_Spielernamen[:surf.valueBar_Spieler.value]:
                            if textBox.label.text == '': valid = False # Falls textBox leer
                            spielernamen.append(textBox.label.text)

                        if valid: running = False # Falls Eingaben gültig Szene beenden
                        else: # Eingaben ungültig
                            pygame.mixer.Sound.play(sounds['wrong']) # Falsch-Sound abspielen
                            surf.button_Bestätigen.color = farben['rot'] # Button rot färben
                            screen.surface.blit(surf.button_Bestätigen(), surf.button_Bestätigen.pos)
                            pygame.display.update()

                            pygame.time.delay(1000) # Verzögerung, damit der rote Button zu sehen ist
                            surf.button_Bestätigen.color = farben['hellgrau'] # Farbe zurücksetzen

            surf.update() # Aktualisieren
            Clock.tick(FPS) # Framerate reduzieren

        # Spielernamen und Handkartenanzahl zurückgeben
        return spielernamen, surf.valueBar_Handkarten.value

    # Fenster aktualisieren/neu "malen"
    def update(self):
        screen.surface.fill(self.color) # Mit Szenen-Farbe füllen
        # Kasten für Spielernameneingabe malen
        rect = (int(screen.width/2.27), int(screen.height/3.95), int(screen.width/1.92), int(screen.height/1.875))
        pygame.draw.rect(screen.surface, farben['grau'], rect)
        pygame.draw.rect(screen.surface, farben['hellgrau'], rect, 2)

        # Labels auf Fenster malen
        screen.surface.blit(self.label_title(), self.label_title.pos)
        screen.surface.blit(self.label_Handkarten(), self.label_Handkarten.pos)
        screen.surface.blit(self.label_Spieler(), self.label_Spieler.pos)
        screen.surface.blit(self.label_title_Spielernamen(), self.label_title_Spielernamen.pos)

        # Button aufmalen
        screen.surface.blit(self.button_Bestätigen(), self.button_Bestätigen.pos)

        # valueBars aufmalen
        screen.surface.blit(self.valueBar_Spieler(), self.valueBar_Spieler.pos)
        screen.surface.blit(self.valueBar_Handkarten(), self.valueBar_Handkarten.pos)

        # Passende Anzahl Labels und textBoxen aufmalen
        for spieler in range(self.valueBar_Spieler.value):
            screen.surface.blit(self.labels_Spielernamen[spieler](), self.labels_Spielernamen[spieler].pos)
            screen.surface.blit(self.textBoxes_Spielernamen[spieler](), self.textBoxes_Spielernamen[spieler].pos)

        # Deaktivierte textBoxen leeren
        for disabled_textBox in self.textBoxes_Spielernamen[self.valueBar_Spieler.value:]:
            disabled_textBox.label.text = ''

        pygame.display.update()

# Haupspiel-Szene (UNO)
class Spiel:
    deck = 'Default' # Legt das Deck fest, mit dem gespielt wird (grafisch)

    def __init__(self):
        self.card_w = round(screen.width / 6.67) # Kartenbreite berechnen
        self.card_h = round(self.card_w * 1.56) # Kartenhöhe berechnen
        self.card_size = (round(self.card_w), round(self.card_h)) # Kartengröße

        screen.caption = "UNO - Im Spiel" # Fenster-Überschrift ändern
        self.images = self.get_images(self.card_size) # Bilder/Karten laden
        
        self.rects = []
        """
        self.rects[0] = Ablagestapel
        self.rects[1] = Ziehstapel
        self.rects[2:] = Spielerkarten
        """
        self.rects.append(pygame.Rect((round(screen.width / 2 - self.card_w / 2), round(screen.height / 10)), self.card_size))
        self.rects.append(pygame.Rect((round(screen.width - self.card_w - screen.height / 25), round(screen.height / 25)), self.card_size))
        self.handkarten_neu()

        self.labels = []
        """
        self.labels[0] = aktueller Spieler (text)
        self.labels[1] = Zwischentext
        self.labels[2:6] = Spieler
        """
        self.labels.append(Label((0,0), int(screen.height / 30), 'Aktueller Spieler:', farben['weiß'], bold=True))
        self.labels.append(Label((0,round(screen.height / 9)), int(screen.height / 55), 'Andere Spieler und deren übrige Karten', farben['weiß'], bold=True))
        self.labels.append(Label((0,0), int(screen.height / 30), None, farben['weiß']))
        self.labels.append(Label((0,0), int(screen.height / 37.5), None, farben['weiß']))
        self.labels.append(Label((0,0), int(screen.height / 37.5), None, farben['weiß']))
        self.labels.append(Label((0,0), int(screen.height / 37.5), None, farben['weiß']))

    # Main-Funktion
    @classmethod
    def run(cls):
        namen,karten = Spieleinstellungen.run() # Spieleinstellungen-Szene aufrufen, um Spielernamen und Handkartenanzahl zu bekommen
        text.start(namen,karten) # UNO starten

        surf = cls() # Klasse initialisieren
        surf.update()

        markierte_karte = None # Gibt an, welche Karte gerade markiert ist

        # Booleans definieren
        Abbruch = False
        spielEnde = False
        zug_Möglich = False
        zug_Versuch = False
        ziehen = False

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Wenn Maus über eine Spielerkarte/den Ziehstapel hovert, Karte markieren
                elif event.type == MOUSEMOTION:
                    for rect in surf.rects[1:]:
                        # Wenn Maus auf Karte
                        if rect.collidepoint(event.pos):
                            # Falls keine Karte markiert ist und Karte nicht unter der markierten Karte liegt
                            if markierte_karte != None and rect.left > markierte_karte.left:
                                # Karte ent-markieren
                                surf.markieren(markierte_karte, False)
                                markierte_karte = None

                            # Karte markieren, wenn noch keine markiert ist
                            if markierte_karte == None:
                                surf.markieren(rect)
                                markierte_karte = rect

                    # Auswahl entfernen
                    if markierte_karte != None and not markierte_karte.collidepoint(event.pos):
                        surf.markieren(markierte_karte, False)
                        markierte_karte = None

                # Falls "Mausklick" und eine Karte ist ausgewählt
                elif event.type == MOUSEBUTTONDOWN and markierte_karte != None:
                    karte = surf.rects.index(markierte_karte) - 2 # Index der Karte bekommen und Ablage- und Ziehstapel abziehen
                    zug_Möglich, spielEnde = text.zug(karte, markierte_karte.left) # Zug ausführen
                    # Wenn keine Karte gezogen wurde, zug_Versuch = True
                    zug_Versuch = True if karte != -1 else False

                # Falls "Tastendruck" und Taste ist Escape
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound
                    Abbruch = Optionen_Spiel.run() # Optionen/Pausen-Menü -Szene aufrufen
                    
                    surf = cls() # Klasse neu laden
                    screen.caption = "UNO - Im Spiel" # Fenster-Überschrift festlegen

                    # Falls Spielabbruch
                    if Abbruch:
                        running = False
                        surf.update()

            # Falls ein Spieler gewonnen hat
            if spielEnde:
                running = False

            # Fallse der Zug möglich war
            elif zug_Möglich:
                pygame.mixer.Sound.play(sounds['correct']) # Bestätigungs-Sound abpielen
                # Variablen zurücksetzen
                zug_Möglich = False
                zug_Versuch = False

                surf.markieren(markierte_karte, False)
                markierte_karte = None
                
                # Handkarten neu laden
                surf.handkarten_neu()
                pygame.time.delay(25) # kurze Verzögerung, um Fehlern vorzubeugen

            # Falls Zug versucht wurde, aber nicht möglich war
            elif zug_Versuch and not zug_Möglich:
                pygame.mixer.Sound.play(sounds['wrong']) # Falsch-Sound abspielen
                # Variablen zurücksetzen
                zug_Versuch = False

                surf.nicht_Möglich(markierte_karte) # Zeigt an, dass der Zug nicht möglich war
                surf.markieren(markierte_karte, False)
                markierte_karte = None
            
            if running:
                surf.update()
                Clock.tick(FPS)

        # Szene beenden
        surf.rect_refresh(surf.rects[0], text.ablagestapel[0]) # Ablagestapenkarte aktualisieren
        screen.surface.fill(screen.color, (0, round(screen.height / 2), screen.width, screen.height)) # Handkarten übermalen
        pygame.display.update()

        # Kein Spielabbruch (Spieler hat gewonnen)
        if not Abbruch:
            # Endmenü-Szene aufrufen
            Endmenü(text.spielerNamen[text.aktuellerSpieler])
        else: # Spielabbruch
            # Zurück zur Hauptmenü-Szene
            Hauptmenü.run()

    # Fenster aktualisieren/neu malen
    def update(self):
        screen.surface.fill(screen.color) # mit Fensterfarbe füllen
        # Infokasten Rechteck und Umrandung
        info = pygame.draw.rect(screen.surface, farben['darkgrau'], (0,0, round(screen.width / 4), round(screen.height / 3.5)))
        pygame.draw.line(screen.surface, farben['weiß'], info.topright, info.bottomright, 3)
        pygame.draw.line(screen.surface, farben['weiß'], info.bottomleft, info.bottomright, 3)
        pygame.draw.line(screen.surface, farben['weiß'], (0,round(screen.height / 10)), (info.right, round(screen.height / 10)), 1)

        # Handkarten
        i = 0
        for rect in self.rects[2:]:
            self.rect_refresh(rect, text.spielerHand[text.aktuellerSpieler][i])
            i += 1
        # Ablagestapel / Ziehstapel
        self.rect_refresh(self.rects[0], text.ablagestapel[0])
        self.rect_refresh(self.rects[1], 'Back')

        # Label
        screen.surface.blit(self.labels[0](), self.labels[0].pos)
        screen.surface.blit(self.labels[1](), self.labels[1].pos)

         # aktuellen Spielernamen zentrieren
        x,y = (round(screen.width / 8), screen.height / 16)
        self.labels[2].text = text.spielerNamen[text.aktuellerSpieler]
        self.labels[2].center = (x,y)
        screen.surface.blit(self.labels[2](), self.labels[2].pos)

        y += y * 1.5 # y-Wert erhöhen
        # Restliche Spielernamen
        for i in range(1, len(text.spielerNamen)):
            name = text.nextSpielername(i)
            # Spielernamen und übrige Handkarten anzeigen
            self.labels[i+2].text = text.spielerNamen[name] + ' ({})'.format(len(text.spielerHand[name]))
            self.labels[i+2].center = (x,y)
            
            screen.surface.blit(self.labels[i+2](), self.labels[i+2].pos)
            y += screen.height / 25  # y-Wert erhöhen

        pygame.display.flip()

    # Funktion, um die Handkarten neu zu laden
    def handkarten_neu(self):
        karten = len(text.spielerHand[text.aktuellerSpieler]) # Anzahl der Handkarten bekommen
        self.rects = self.rects[:2] # Liste leeren

        # Margin zum Bildschirmrand und Padding zwischen den Karten berechnen
        margin = round(screen.width / 15)
        padding = self.card_w - ((screen.width - (margin * 2)) / karten)

        # Falls padding kleiner als x: den Rest auf margin berechnen (Karten zentrieren)
        if padding < -(screen.width / 40):
            margin += round(((padding*-1 - screen.width / 40) * karten) / 2)
            padding = -(screen.width / 40)
        padding += padding / karten # Padding von letzten Karte (nicht gebraucht) auf andere Karten aufteilen

        # pygame.Rect's für Handkarten erstellen
        x = margin
        y = round(screen.height - self.card_h - screen.height / 50)
        for i in range(karten):
            self.rects.append(pygame.Rect((x,y), self.card_size))
            x += round(self.card_w - padding) # x-Wert erhöhen

    # Funktion, um Bild/Karte an der Stelle des rects zu malen
    def rect_refresh(self, rect, karte):
        """ (args)
        rect = pygame.Rect, auf dem die Karte gemalt werden soll
        karte = die Karte, die gemalt werden soll (Bsp.: ['grün', '2'])
        """
        img_str = " ".join(karte) if karte != 'Back' else karte # Karte zu einem string zsm.-fügen
        screen.surface.blit(self.images[img_str], rect) # Karte an der Stelle des Rects malen

    # Funktion, um eine Karte/ein Rect hervorzuheben
    def markieren(self, rect, markieren=True):
        """ (args)
        rect = pygame.Rect, das hervorgehoben werden soll
        markieren = Gibt an, ob Karte markiert oder ent-markiert werden soll
        """
        if markieren: # markieren
            rect.move_ip(0, int(screen.height / 45 * -1)) # Rect nach oben bewegen
        else: # ent-markieren
            rect.move_ip(0, int(screen.height / 45)) # Rect unten oben bewegen

    # Funktion, die anzeigt, dass ein Zug nicht möglich war
    def nicht_Möglich(self, karte):
        """ (args)
        karte = Karte, die nicht abgewlegt werden kann (pygame.Rect)
        """

        # Handkarten übermalen
        screen.surface.fill(screen.color, pygame.Rect(0, int(screen.height / 2), screen.width, int(screen.height / 2)))
        
        # Handkarten neu malen
        i = 0
        for rect in self.rects[2:]:
            # Bild aktualisieren
            self.rect_refresh(rect, text.spielerHand[text.aktuellerSpieler][i])
            
            # Falls Rect = nicht ablegbare Karte: rot markieren
            if rect == karte: pygame.draw.rect(screen.surface, farben['rot'], rect, 5)
            i += 1

        pygame.display.update()
        pygame.time.delay(500)

    # Funktion, um die Bilder/Karten zu laden/bekommen
    @staticmethod
    def get_images(size):
        """ (args)
        size = Kartengröße (x,y)
        """
        images = {} # Dict für Karten
        img_path = 'Images/{}/'.format(Spiel.deck) # Pfad zum ricgtigen Kartendeck

        # Jede Karte dem dict hinzufühen
         # Karten mit Standardfarben 
        for farbe in text.normale_farben:
            for nummer in text.normale_nummern + text.spezial_karten:
                img = pygame.transform.scale(pygame.image.load(img_path + " ".join([farbe, nummer]) + '.png'), size)
                images.update({" ".join([farbe,nummer]) : img})

         # Schwarze Karten
        for spezialkarte in text.spezial_karten:
            img = pygame.transform.scale(pygame.image.load(img_path + " ".join(['Schwarz', spezialkarte]) + '.png'), size)
            images.update({" ".join(["Schwarz", spezialkarte]) : img})

         # Kartenrückseite
        img = pygame.transform.scale(pygame.image.load(img_path + "Back.png"), size)
        images.update({"Back" : img})

        # Dict mit allen images zurückgeben
        # Beispiel für einen Dict-"Eintrag": {"Blau 7": Surface-obj}
        return images

# "Mini-Szene", falls Farbenwahl/+4 gelegt wurde,
# um sich eine Farbe zu wünschen
class Farbenwahl:
    def __init__(self, x, y, width):
        """ (args)
        x = x-Koordinate für das Surface
        y = y-Koordinate für das Surface
        width = Durchmesser des gesamten Surface
        """
        self.farben = ['rot', 'blau', 'grün', 'gelb']
        self.width = width # Gesamte Breite
        self.size = round(width / 2) # Breite für ein Quadrat
    
        # Liste mit einem pygame.Rect für jede Farbe
        self.rects = []
        self.rects.append(pygame.Rect((x            ,y            ), (self.size,self.size)))
        self.rects.append(pygame.Rect((x + self.size,y            ), (self.size,self.size)))
        self.rects.append(pygame.Rect((x            ,y + self.size), (self.size,self.size)))
        self.rects.append(pygame.Rect((x + self.size,y + self.size), (self.size,self.size)))

    # Main-Funktion
    @classmethod
    def run(cls, x, y, width):
        """ (args)
        x = x-Koordinate für das Surface
        y = y-Koordinate für das Surface
        width = Durchmesser des gesamten Surface
        """
        surf = cls(x, y, width) # Klasse initialisieren
        surf.animation(x, y, width) # Einblendung

        markiertes_rect = None
        while True:
            for event in pygame.event.get():
                #Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                if event.type == MOUSEMOTION:
                    # Bei jedem Rect prüfen, ob Maus auf Rect
                    for rect in surf.rects:
                        if rect.collidepoint(event.pos) and markiertes_rect == None:
                            index = surf.rects.index(rect) # Index des Rects bekommen
                            surf.markieren(index) # Rect markieren
                            markiertes_rect = index

                    # Falls Maus nichtmehr auf martkierter Karte
                    if markiertes_rect != None and not surf.rects[markiertes_rect].collidepoint(event.pos):
                        surf.markieren(markiertes_rect, False) # Markierung aufheben
                        markiertes_rect = None

                # Falls "Mausklick" und ein Rect ist markiert/ausgewählt
                if event.type == MOUSEBUTTONDOWN and markiertes_rect != None:
                    pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                    # Gesamtes Surface mit der Fenster-Farbe übermalen
                    pygame.draw.rect(screen.surface, screen.color, (x - screen.width / 60, y - screen.width / 60, width + 40, width + 40))
                    pygame.display.update()

                    return surf.farben[markiertes_rect].capitalize() # Ausgewählte Farbe zurückgeben

            Clock.tick(FPS) # Framerate reduzieren

    # Funktion für eine Einblendung des Surface
    def animation(self, x, y, width):
        """ (args)
        x = x-Koordinate für das Surface
        y = y-Koordinate für das Surface
        width = Durchmesser des gesamten Surface
        """
        surf = [] # Liste mit Surfaces
        rect = [] # Liste mit Rects für Animation

        # Surfaces/Rects erstellen
        for i in range(4):
            surf.append(pygame.Surface((width / 2, width / 2)))
            rect.append(pygame.Rect(0, 0, 1, 1))
            rect[i].center = surf[i].get_rect().center

        # For-Loop für Transparenz und Größe der Rects
        for alpha in range(int(width / 2)):
            # Alle Surfaces/Rects durchgehen
            for i in range(4):
                surf[i].set_alpha(alpha) # Transparenz des Surfaces festlegen
                surf[i].fill(farben['schwarz'])
                surf[i].fill(farben[self.farben[i]], rect[i].inflate(alpha, alpha)) # Rect vergrößern
                screen.surface.blit(surf[i], self.rects[i].topleft)
            pygame.display.update()
            pygame.time.delay(1)

        # End-Surfaces malen
        for i in range(4):
            pygame.draw.rect(screen.surface, farben[self.farben[i]], self.rects[i])
            pygame.draw.rect(screen.surface, farben['schwarz'], self.rects[i], 3)

        pygame.display.update(self.rects)

    # Funktion, die ein Rect/Surface hervorhebt
    def markieren(self, index, markieren=True):
        """ (args)
        index = Index des Rects in (self.rects)
        markieren = Markieren oder Ent-Markierung
        """
        rect = self.rects[index]
        i = round(self.width / 50) # Verschiebungsgröße

        x,y = (0,0) # Verschiebung
        size = (i*2,i*2) # Größe
        
        if markieren:
            if index == 0:   x,y = (-i, -i)
            elif index == 1: x,y = ( i, -i)
            elif index == 2: x,y = (-i,  i)
            elif index == 3: x,y = ( i,  i)
        else:
            if index == 0:   x,y = ( i,  i)
            elif index == 1: x,y = (-i,  i)
            elif index == 2: x,y = ( i, -i)
            elif index == 3: x,y = (-i, -i)
            size = (-(i*2),-(i*2)) # Größe zurücksetzen

        # Rect übermalen
        pygame.draw.rect(screen.surface, screen.color, rect)
        pygame.draw.rect(screen.surface, screen.color, rect, 3)
        pygame.display.update(rect)

        # Rect bewegen und vergrößern/verkleinern
        rect.move_ip(x,y)
        rect.inflate_ip(size)

        # Neues Rect malen
        pygame.draw.rect(screen.surface, farben[self.farben[index]], rect)
        pygame.draw.rect(screen.surface, farben['schwarz'], rect, 3)
        pygame.display.update(rect)

# Endmenü-Szene
class Endmenü:
    def __init__(self, gewinner):
        """ (args)
        gewinner = Name des Spiers, der gewonnen hat
        """
        screen.caption = 'UNO - Endmenü' #  Fenster-Überschrift festlegen
        # Panel für das Endmenü erstellen
        surf = Panel(pygame.Rect(screen.width, round(screen.height / 4), screen.width, round(screen.height / 2)), farben['grün'])
        
        # Labels und Button zu Panel hinzufügen
        surf.controls.append(Label((0,0), round(screen.height / 16.67), gewinner, farben['weiß']))
        surf.controls.append((Label((0,0), round(screen.height / 21.42), 'HAT GEWONNEN!', farben['weiß'], bold=True)))
        surf.controls.append(Button(pygame.Rect(0,0,int(screen.width/3),int(screen.height/8)), round(screen.height / 25), 'Back to Menu', farben['grau'], farben['schwarz'], None))

        # Labels und Buttons positionieren
        surf.controls[0].center = (surf.rect.centerx, surf.rect.height / 5.5)
        surf.controls[1].center = (surf.rect.centerx, surf.rect.centery - surf.rect.height / 10)
        surf.controls[2].center = (surf.rect.centerx, surf.rect.height - surf.rect.height / 4)

        # Umrandung zum Panel hinzufügen
        surf.controls.append(Line(surf.rect.topleft, surf.rect.topright, farben['schwarz'], 10))
        surf.controls.append(Line(surf.rect.bottomleft, surf.rect.bottomright, farben['schwarz'], 10))
        surf.controls.append(Line(surf.rect.topleft, surf.rect.bottomleft, farben['schwarz']))
        surf.controls.append(Line(surf.rect.topright, surf.rect.bottomright, farben['schwarz']))

        pygame.mixer.music.fadeout(2000) # Musik ausblenden
        self.animation(surf) # Einblendung

        # y-Koordinate des Buttons im gesamten Fenster
        rect = surf.controls[2].rect
        rect.y += surf.pos_y

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                elif event.type == MOUSEMOTION:
                    # Falls Maus auf Button: markieren
                    if rect.collidepoint(event.pos) and surf.controls[2].hover == False:
                        surf.controls[2].hover = True
                    # Falls Maus nichtmehr auf Button ent-markieren
                    elif not rect.collidepoint(event.pos) and surf.controls[2].hover == True:
                        surf.controls[2].hover = False

                # Falls "Mausklick" und Klick auf Button
                elif event.type == MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                    surf.controls[2].Click(surf, screen=screen.surface)
                    running = False
            
            # Aktualisieren
            screen.surface.blit(surf(), surf.pos)
            pygame.display.update()
            Clock.tick(FPS) # Framerate reduzieren

        # Programmende
        self.fadeOut() # Ausblendung
        pygame.mixer.music.play(-1,0.0) # Musik starten
        Hauptmenü.run() # Hauptmenü starten

    # Funktion zur Einblendung des Surface
    @staticmethod
    def animation(surface):
        """ (args)
        surface = zu animierende Surface
        """
        pygame.mixer.Sound.play(sounds['gewonnen']) # Win-Sound abspielen
        # Solange x-Koordinate des Surface > 0
        while surface.pos_x > 0:
            surface.pos_x -= 3 # x-Koordinate verkleinern
            screen.surface.blit(surface(), surface.pos)
            pygame.display.update()

        # x-Koordinate auf 0 setzen
        surface.pos_x = 0

    # Funktion zur Ausblendung der Szene (Schwarzblende)
    @staticmethod
    def fadeOut():
        # Surface mit Fenstergröße erstellen
        surf = pygame.Surface((screen.width, screen.height))

        # Bei jedem Durchgang transparenz verringern
        for i in range(90):
            surf.set_alpha(i) # Transparenz festlegen
            surf.fill(farben['schwarz'])
            
            screen.surface.blit(surf, (0,0))
            pygame.display.update()
            pygame.time.delay(5)


# Optionen-Szene
class Optionen:
    Master_Volume = 100 # Sound-Lautstärke
    Music_Volume = 100 # Musik-Lautstärke

    def __init__(self):
        screen.caption = 'UNO - Optionen' # Fenster-Überschrift festlegen
        self.color = screen.color # Szenen-Farbe festlegen

        # Label Überschrift "OPTIONEN"
        self.label_title = Label((int(screen.width/10),int(screen.width/100)), int(screen.height/15), 'OPTIONEN', farben['weiß'], bold=True)

        # Restliche Labels erstellen
        self.label_Auflösung = Label((int(screen.width/6.67),int(screen.height/7.5)), int(screen.width/25), 'Auflösung', farben['weiß'])
        self.label_Lautstärke = Label((int(screen.width/6.67),int(screen.height/3.75)), int(screen.width/25), 'Lautstärke', farben['weiß'])
        self.label_Musik = Label((int(screen.width/4.76),int(screen.height/2.78)), int(screen.height/21.73), '=> Musik', farben['weiß'])
        self.label_Kartendeck = Label((int(screen.width/6.67),int(screen.height/2.05)), int(screen.width/25), 'Kartendeck', farben['weiß'])

        # Liste mit Auflösungen und Lautstärke für die valueBars
        resolutions = ['200x150','400x300','600x450','800x600','1000x750','1200x900']
        volume = range(0, 101, 10)
        # valueBars erstellen
        self.valueBar_Auflösung = valueBar(pygame.Rect(int(screen.width/3.3),int(screen.height/7.5),int(screen.width/2),int(screen.height/15)), farben['schwarz'], farben['weiß'], resolutions, resolutions.index('{}x{}'.format(int(screen.width),int(screen.height))))
        self.valueBar_Lautstärke = valueBar(pygame.Rect(int(screen.width/3.3),int(screen.height/3.75),int(screen.width/2),int(screen.height/15)), farben['schwarz'], farben['weiß'], volume, volume.index(Optionen.Master_Volume))
        self.valueBar_Musik = valueBar(pygame.Rect(int(screen.width/3.03),int(screen.height/2.78),int(screen.width/2.13),int(screen.height/15)), farben['schwarz'], farben['weiß'], volume, volume.index(Optionen.Music_Volume))

        # Buttons erstellen
        self.button_Zurück = Button(pygame.Rect(int(screen.width) - int(screen.width/20) - int(screen.width/100), int(screen.width/100), int(screen.width/20), int(screen.width/20)), int(screen.height/25), 'X', farben['weiß'], farben['schwarz'], None)
        self.button_Anwenden = Button(pygame.Rect(0,0,int(screen.width/2.86),int(screen.height/12.5)), int(screen.height/25), '[A] Anwenden', farben['weiß'], farben['darkgrau'], self.anwenden_click)
        self.button_Anwenden.center = (int(screen.width - screen.width/5.26), int(screen.height * 0.95))

        # Kartendeckauswahl
         # Labels
        self.label_Default = Label((int(screen.width/2.38),int(screen.height/1.53)), int(screen.height/37.5), 'Default', farben['weiß'], bold=True)
        self.label_minimalista = Label((int(screen.width/1.49), int(screen.height/1.61)), int(screen.height/37.5), 'minimalista', farben['weiß'], bold=True)

         # Kartengröße ausrechnen
        card_w = round(screen.width / 7)
        card_h = round(card_w * 1.56)
         # Aktuelles Kartendeck bekommen
        self.deck = Spiel.deck

         # Bilder der Kartendecks 
        self.surf_Default = pygame.transform.scale(pygame.image.load('Images/Default/Back.png'), (card_w, card_h))
        self.surf_minimalista = pygame.transform.scale(pygame.image.load('Images/minimalista/Back.png'), (card_w, card_h))

         # Position der Surfaces festlegen
        self.Default_pos = (int(screen.width/3.64),int(screen.height/1.81))
        self.minimalista_pos = (int(screen.width/1.9),int(screen.height/1.81))

    # Main-Funktion
    @classmethod
    def run(cls):
        surf = cls() # Klasse initialisieren
        surf.fadeIn() # Einblendungen

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                elif event.type == MOUSEMOTION:
                    # Prüfen, ob Maus auf einem valueBar-Button
                    for valueBar in [surf.valueBar_Auflösung,surf.valueBar_Lautstärke,surf.valueBar_Musik]:
                        # Linker Button
                        if valueBar.button_left_rect.collidepoint(event.pos):
                            valueBar.button_left.hover = True
                        elif valueBar.button_left.hover: valueBar.button_left.hover = False

                        # Rechter Button
                        if valueBar.button_right_rect.collidepoint(event.pos):
                            valueBar.button_right.hover = True
                        elif valueBar.button_right.hover: valueBar.button_left.hover = False

                # Falls "Mausklick"
                elif event.type == MOUSEBUTTONDOWN:
                    # Falls Mausklick auf valueBar-Button
                    for valueBar in [surf.valueBar_Auflösung,surf.valueBar_Lautstärke,surf.valueBar_Musik]:
                        if valueBar.button_left_rect.collidepoint(event.pos):
                            pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                            valueBar.prev()
                        elif valueBar.button_right_rect.collidepoint(event.pos):
                            pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                            valueBar.next()

                    # Falls Mausklick auf Zurück-Button
                    if surf.button_Zurück.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Zurück.Click(screen.surface)
                        running = False

                    # Falls Mausklick auf Anwenden-Button
                    elif surf.button_Anwenden.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        change = surf.button_Anwenden.Click(screen.surface)
                        if change: 
                            surf = cls()

                    # Falls Mausklick auf Default-Deck
                    elif pygame.Rect(surf.Default_pos, surf.surf_Default.get_rect().size).collidepoint(event.pos):
                        surf.deck = 'Default' # Deck ändern
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen

                    # Falls Mausklick auf minimalista-Deck
                    elif pygame.Rect(surf.minimalista_pos, surf.surf_minimalista.get_rect().size).collidepoint(event.pos):
                        surf.deck = 'minimalista' # Deck ändern
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen

                # Falls "Tastendruck"
                elif event.type == KEYDOWN:
                    # Falls Taste = A
                    if event.key == K_a:
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        change = surf.button_Anwenden.Click(screen.surface) # Änderungen anwenden
                        # Falls Auflösung geändert wurde, neu laden
                        if change: 
                            surf = cls()

                    # Falls Taste = Escape
                    elif event.key == K_ESCAPE:
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        running = False

            surf.update()
            Clock.tick(FPS) # Framerate reduzieren

    # Fenster aktualisieren
    def update(self):
        screen.surface.fill(self.color) # Fenster übermalen

        # Hintergrund-Rects
        pygame.draw.rect(screen.surface, farben['schwarz'], (0,0,int(screen.width/12.5),screen.height))
        pygame.draw.rect(screen.surface, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/8.3),int(screen.width/1.49),int(screen.height/10.71)))
        pygame.draw.rect(screen.surface, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/3.95),int(screen.width/1.49),int(screen.width/7.14)))
        pygame.draw.rect(screen.surface, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/2.08),int(screen.width/1.49),int(screen.height/2.5)))

        # Labels
        screen.surface.blit(self.label_title(), self.label_title.pos)
        screen.surface.blit(self.label_Auflösung(), self.label_Auflösung.pos)
        screen.surface.blit(self.label_Lautstärke(), self.label_Lautstärke.pos)
        screen.surface.blit(self.label_Musik(), self.label_Musik.pos)
        screen.surface.blit(self.label_Kartendeck(), self.label_Kartendeck.pos)

        # valueBars
        screen.surface.blit(self.valueBar_Auflösung(), self.valueBar_Auflösung.pos)
        screen.surface.blit(self.valueBar_Lautstärke(), self.valueBar_Lautstärke.pos)
        screen.surface.blit(self.valueBar_Musik(), self.valueBar_Musik.pos)

        # Buttons
        screen.surface.blit(self.button_Anwenden(), self.button_Anwenden.pos)
        screen.surface.blit(self.button_Zurück(), self.button_Zurück.pos)

        # Kartendeck Labels (90-Grad gedreht)
        screen.surface.blit(pygame.transform.rotate(self.label_Default(), 90), self.label_Default.pos)
        screen.surface.blit(pygame.transform.rotate(self.label_minimalista(), 90), self.label_minimalista.pos)

        # Kartenbilder
        screen.surface.blit(self.surf_Default, self.Default_pos)
        screen.surface.blit(self.surf_minimalista, self.minimalista_pos)

        # Auwgewähltes Deck umranden
        if self.deck == 'Default':
            pygame.draw.rect(screen.surface, farben['rot'], (self.Default_pos, self.surf_Default.get_rect().size), 5)
        else:
            pygame.draw.rect(screen.surface, farben['rot'], (self.minimalista_pos, self.surf_minimalista.get_rect().size), 5)

        pygame.display.update()

    def fadeIn(self):
        # Surf erstellen und mit Fensterfarbe füllen
        surf = pygame.Surface((screen.width, screen.height))
        surf.fill(self.color)

        # Hintergrund-Rects
        pygame.draw.rect(surf, farben['schwarz'], (0,0,int(screen.width/12.5),screen.height))
        pygame.draw.rect(surf, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/8.3),int(screen.width/1.49),int(screen.height/10.71)))
        pygame.draw.rect(surf, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/3.95),int(screen.width/1.49),int(screen.width/7.14)))
        pygame.draw.rect(surf, farben['darkgrau'], (int(screen.width/7.14),int(screen.height/2.08),int(screen.width/1.49),int(screen.height/2.5)))

        # Labels
        surf.blit(self.label_title(), self.label_title.pos)
        surf.blit(self.label_Auflösung(), self.label_Auflösung.pos)
        surf.blit(self.label_Lautstärke(), self.label_Lautstärke.pos)
        surf.blit(self.label_Musik(), self.label_Musik.pos)
        surf.blit(self.label_Kartendeck(), self.label_Kartendeck.pos)

        # valueBars
        surf.blit(self.valueBar_Auflösung(), self.valueBar_Auflösung.pos)
        surf.blit(self.valueBar_Lautstärke(), self.valueBar_Lautstärke.pos)
        surf.blit(self.valueBar_Musik(), self.valueBar_Musik.pos)

        # Buttons
        surf.blit(self.button_Anwenden(), self.button_Anwenden.pos)
        surf.blit(self.button_Zurück(), self.button_Zurück.pos)

        # Kartendeck Labels (90-Grad gedreht)
        surf.blit(pygame.transform.rotate(self.label_Default(), 90), self.label_Default.pos)
        surf.blit(pygame.transform.rotate(self.label_minimalista(), 90), self.label_minimalista.pos)

        # Kartenbilder
        surf.blit(self.surf_Default, self.Default_pos)
        surf.blit(self.surf_minimalista, self.minimalista_pos)

        # Auwgewähltes Deck umranden
        if self.deck == 'Default':
            pygame.draw.rect(surf, farben['rot'], (self.Default_pos, self.surf_Default.get_rect().size), 5)
        else:
            pygame.draw.rect(surf, farben['rot'], (self.minimalista_pos, self.surf_minimalista.get_rect().size), 5)

        # Solange y-Koordinate > 0, nach oben verschieben
        y = screen.height
        while y > 0:
            screen.surface.blit(surf, (0,y))
            pygame.display.update()

            y -= 3 # y-Koordinate verkleinern

    # Button-Funktion für Anwenden-Button
    def anwenden_click(self):
        global screen
        changed_resolution = False

        # Auflösung aus valueBar bekommen
        resolution,_ = self.valueBar_Auflösung.value.split('x')
        # Falls Auflösung geändert
        if int(resolution) != screen.width:
            # Screen neu laden und Fenster-Überschrift festlegen
            screen = Screen(int(resolution), 'UNO - Optionen')
            changed_resolution = True

        # Lautstärken übernehmen
        Optionen.Master_Volume = self.valueBar_Lautstärke.value
        Optionen.Music_Volume = self.valueBar_Musik.value

        # Kartendeck übernehmen
        Spiel.deck = self.deck

        # Lautstärken einstellen
        for sound in sounds.values():
            sound.set_volume(Optionen.Master_Volume / 100)
        pygame.mixer.music.set_volume(Optionen.Music_Volume / 100)

        # Zurückgeben, ob Auflösung geändert wurde
        return changed_resolution

# Spiel- Pauseszene
class Optionen_Spiel:
    def __init__(self):
        screen.caption = 'UNO - Im Spiel (PAUSE)' # Fenster-Überschrift ändern

        # Halb-Transparenten Hintergrund erstellen
        self.background = pygame.Surface((screen.width, screen.height), pygame.SRCALPHA)
        self.background.fill((0,0,0, 230))
        screen.surface.blit(self.background, (0,0))

        # Rectz für das Menü
        self.menu_rect = pygame.Rect(0,0, int(screen.width/3), int(screen.height/3))
        self.menu_rect.center = (int(screen.width / 2), int(screen.height / 2))

        # Pause-Label
        self.label_pause = Label((0,0), int(screen.height / 15), 'P A U S E', farben['darkgrau'], bold=True)
        self.label_pause.center = (screen.width / 2, self.label_pause().get_rect().centery)

        # Buttons erstellen
        self.button_Fortfahren = Button(pygame.Rect(int(screen.width/2.82),int(screen.height/2.78), int(screen.width/3.41),int(screen.height/15)), int(screen.height/18.75), 'Fortfahren', farben['weiß'], farben['schwarz'], None)
        self.button_Optionen = Button(pygame.Rect(int(screen.width/2.82),int(screen.height/2.14), int(screen.width/3.41),int(screen.height/15)), int(screen.height/18.75), 'Optionen', farben['weiß'], farben['schwarz'], Optionen.run)
        self.button_Abbruch = Button(pygame.Rect(int(screen.width/2.82),int(screen.height/1.74), int(screen.width/3.41),int(screen.height/15)), int(screen.height/18.75), 'Spiel beenden', farben['weiß'], farben['schwarz'], None)

    # Main-Funktion
    @classmethod
    def run(cls):
        surf = cls() # Klasse initialisieren

        # Boolean erstellen
        spielAbbruch = False

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == QUIT:
                    screen.terminate()

                # Falls "Mausbewegung"
                elif event.type == MOUSEMOTION:
                    # Falls Maus auf Button
                    for button in [surf.button_Fortfahren, surf.button_Optionen, surf.button_Abbruch]:
                        if button.rect.collidepoint(event.pos):
                            button.hover = True
                        elif button.hover:
                            button.hover = False

                # Falls "Mausklick"
                elif event.type == MOUSEBUTTONDOWN:
                    # Falls Klick auf Fortfahren-Button
                    if surf.button_Fortfahren.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Fortfahren.Click(screen.surface)
                        running = False
                    
                    elif surf.button_Optionen.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        _ = surf.button_Optionen.Click(screen.surface) # Optionen-Szene aufrufen
                        running = False

                    elif surf.button_Abbruch.rect.collidepoint(event.pos):
                        pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                        surf.button_Abbruch.Click(screen.surface)
                        running = False
                        spielAbbruch = True # Spiel abbrechen

                # Falls Escape-Taste gedrückt
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.mixer.Sound.play(sounds['button_click']) # Klick-Sound abspielen
                    running = False

            if running:
                # Aktualiesieren
                surf.update()
                Clock.tick(FPS) # Framerate reduzieren

        # Zurückgeben, ob Spiel abgebrochen wird
        return spielAbbruch

    # Fenster aktualisieren
    def update(self):
        # Menü-Fenster neu malen
        pygame.draw.rect(screen.surface, farben['darkgrau'], self.menu_rect)

        # Pause-Label
        screen.surface.blit(self.label_pause(), self.label_pause.pos)

        # Buttons
        screen.surface.blit(self.button_Fortfahren(), self.button_Fortfahren.pos)
        screen.surface.blit(self.button_Optionen(), self.button_Optionen.pos)
        screen.surface.blit(self.button_Abbruch(), self.button_Abbruch.pos)

        pygame.display.update()


# --- PROGRAMM INITIALISIERUNG --- #

screen = Screen(1000) # Fenster erstellen
# Falls Datei, die ausgeführte Datei
if __name__ == '__main__':

    # Versuchen Daten zu laden und einzustellen
    try:
        # Datei öffnen und lesen
        datei = open('data.txt', 'r')
        data = datei.read().split("-")
        datei.close()
    
        # Einstellungen übernehmen
        screen = Screen(int(data[0]))
        Optionen.Master_Volume = int(data[1])
        Optionen.Music_Volume = int(data[2])
        Spiel.deck = data[3]

    # Falls Datei nicht vorhanden oder verändert/beschädigt:
    # Standarteinstellungen beibehalten
    except Exception: pass

    # Musik einrichten
    pygame.mixer.music.load('Sounds/UNO_Soundtrack.mp3')
    pygame.mixer.music.play(-1,0.0)

    # Hauptmenü starten/aufrufen
    Hauptmenü.run()