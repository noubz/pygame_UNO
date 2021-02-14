# Toolbox für pygame von Niclas Berger

import pygame
from main import farben
pygame.mixer.init()

# Bautstein Label (text)
class Label:
    def __init__(self, pos, pt, text, color, font='Arial', bold=False):
        """ (args)
        pos = Potione des Labels
        pt = Schriftgröße
        text = Text des Labels
        color = Frabe des Textes
        font = Schriftart
        bold = Fettschrift
        """
        self.text = text
        self.text_color = color
        self._pos = pos
        self.font = pygame.font.SysFont(font, pt, bold)

    # Eingenschaft pos (position)
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, position):
        self._pos = position

    # Eingenschaft x-pos (x-Position)
    @property
    def pos_x(self):
        x,_ = self.pos
        return x

    @pos_x.setter
    def pos_x(self, x):
        y = self.pos_y
        self.pos = (x,y)

    # Eingenschaft y-pos (y-Position)
    @property
    def pos_y(self):
        _,y = self.pos
        return y

    @pos_y.setter
    def pos_y(self, y):
        x = self.pos_x
        self.pos = (x,y)

    # Eingenschaft center (Mitte des Labels/Surface)
    @property
    def center(self):
        rect = self().get_rect()
        return (self.pos_x + rect.w / 2, self.pos_y + rect.h / 2)

    @center.setter
    def center(self, position):
        x,y = position
        rect = self().get_rect()

        self.pos_x = round(x - rect.w / 2)
        self.pos_y = round(y - rect.h / 2)

    # Dunder-String gibt Art der Instanz zurück
    def __str__(self):
        return 'Label'

    # Dunder-Call gibt Surface mit dem Label zurück
    def __call__(self):
        return self.font.render(self.text, True, self.text_color)

# Baustein Button (Knopf)
class Button(Label):
    def __init__(self, rect, pt, text, bg_color, text_color, funktion, font='Arial'):
        """ (args)
        rect = pygame.Rect für den Button
        pt = Schriftgröße im Button
        text = Text im Button
        bg_color = Hintergrundfarbe des Buttons
        text_color = Schriftfarbe
        funktion = Funktion, die beim Klick ausgeführt wird
        font = Schriftart
        """
        # Text/Label im Button initialisieren
        super().__init__(rect.topleft, pt, text, text_color, font, True)
        # Variablen definieren
        self.color = bg_color
        self._rect = rect
        self.hover = False
        self.Funktion = funktion

    # Eigenschaft, die Rect des Buttons angibt
    @property
    def rect(self):
        return pygame.Rect(self.pos, self._rect.size)
    
    # Eigenschaft, die helle Version, der Hintergrundfarbe angibt
    @property
    def color_light(self):
        r,g,b = self.color

        r = round(r * 1.1) if round(r * 1.1) < 255 else 255
        g = round(g * 1.1) if round(g * 1.1) < 255 else 255
        b = round(b * 1.1) if round(b * 1.1) < 255 else 255

        return (r,g,b)
    
    # Funktion, die ausgeführt wird, wenn der Button gedrückt wird
    def Click(self, surf, screen=None):
        surface = surf if screen == None else surf() # Falls Button auf Panel
        pygame.draw.rect(surface, farben['grau'], ((self.pos), (self.rect.w-1, self.rect.h-1)), 2) # Button grau umranden
        if screen != None: screen.blit(surface, surf.pos)
        pygame.display.update()

        pygame.time.delay(150)

        # Button wieder schwarz umranden
        pygame.draw.rect(surface, farben['schwarz'], ((self.pos), (self.rect.w-1, self.rect.h-1)), 2)
        if screen != None: screen.blit(surface, surf.pos)
        pygame.display.update()

        # Funktion ausführen und ggf. Werte zurückgeben
        if self.Funktion != None:
            return self.Funktion()
        return None


    # Dunder-String gibt dir Art der Instanz zurück
    def __str__(self):
        return 'Button'

    # Dunder-Call gibt Surface mit dem Button zurück
    def __call__(self):
        text = super().__call__()
        text_rect = text.get_rect()
        surf = pygame.Surface(self.rect.size)

        text_rect.center = (self.rect.w/2, self.rect.h/2)
        surf.fill(self.color if not self.hover else self.color_light)
        pygame.draw.rect(surf, farben['schwarz'], (0,0, self.rect.w-1, self.rect.h-1), 2)
        surf.blit(text, text_rect)

        return surf

# Baustein Panel ("Tafel")
class Panel(Label):
    def __init__(self, rect, color, controls=None):
        """ (args)
        rect = pygame.Rect gibt das Panel an
        color = Hintergrundfarbe des Panels
        conrtrols = Dinge auf dem Panel
        """
        x,y, w,h = rect # Koordinaten entnehmen

        self.surface = pygame.Surface((w,h))
        self.pos = (x,y)
        self.color = color

        # Falls keine Dinge auf dem Panel: leere Liste
        if controls == None:
            self.controls = []
        else:
            self.controls = controls

    # Eigenschaft rect gibt das Rect des Panels an
    @property
    def rect(self):
        return self().get_rect()

    # Dunder-Call gibt Surface des Panels zurück
    def __call__(self):
        self.surface.fill(self.color)

        # Alle Objekte auf das Panel malen
        for obj in self.controls:
            # Falls Objekt Label oder Button
            if str(obj) == 'Label' or str(obj) == 'Button':
                self.surface.blit(obj(), obj.pos)
            # Falls Objekt Rect
            elif str(obj) == 'Rect':
                pygame.draw.rect(self.surface, obj.color, obj.rect, obj.width)
            # Falls Objekt Line 
            elif str(obj) == 'Line':
                pygame.draw.line(self.surface, obj.color, obj.start, obj.end, obj.width)

        return self.surface

# Baustein valueBar (Liste)
class valueBar(Label):
    def __init__(self, rect, color, text_color, items=[''], index=0):
        """ (args)
        rect = pygame.Rect der valueBar
        color = Hintergrundfarbe
        text_color = Textfarbe
        items = Liste der valueBar
        index = Start-item der valueBar
        """
        # Knöpfe erstellen
        self.button_left = Button(pygame.Rect(0,0,rect.h,rect.h), rect.h, '<', farben['grau'], farben['weiß'], self.prev)
        self.button_right = Button(pygame.Rect(rect.w - rect.h,0, rect.h,rect.h), rect.h, '>', farben['grau'], farben['weiß'], self.next)
        # Label für Listen-item erstellen
        self.label = Label((0,0), rect.h, '', text_color)

        # Variablen definieren
        self.items = items
        self.index = index

        self.color = color
        self.rect = rect
        self.pos = rect.topleft

    # Eigenschaft value gibt aktuelles item der valueBar an
    @property
    def value(self):
        return self.items[self.index]

    # Eigenschaft gibt Rect des linken Buttons an
    @property
    def button_left_rect(self):
        return pygame.Rect(self.rect.topleft, (self.rect.h, self.rect.h))

    # Eigenschaft gibt Rect des rechten Buttons an
    @property
    def button_right_rect(self):
        return pygame.Rect((self.rect.right - self.rect.h, self.rect.top), (self.rect.h, self.rect.h))

    # Funktion, um ein item weiter zu gehen
    def next(self):
        self.index += 1

        if self.index == len(self.items):
            self.index = 0

    # Funktion, um ein item zurück zu gehen
    def prev(self):
        self.index -= 1

        if self.index == -1:
            self.index = len(self.items) - 1

    # Dunder-String gibt dir Art der Instanz zurück
    def __str__(self):
        return 'valueBar'

    # Dunder-Call gibt Surface mit der valueBar zurück
    def __call__(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(self.color)

        surf.blit(self.button_left(), self.button_left.pos)
        surf.blit(self.button_right(), self.button_right.pos)

        self.label.text = str(self.items[self.index])
        self.label.center = (self.rect.w/2, self.rect.h/2)
        surf.blit(self.label(), self.label.pos)

        pygame.draw.rect(surf, farben['schwarz'], (0,0, self.rect.w-1, self.rect.h-1), 2)
        return surf

# Baustein textBox (Texteingabe)
class textBox(Label):
    def __init__(self, rect, color, text_color, max=100):
        """ (args)
        rect = pygame.Rect der textBox
        color = Hintergrundfarbe
        text_color = Textfarbe
        max = Maximale Chars/Buchstaben in der textBox
        """
        self.surf = pygame.Surface(rect.size)
        self.label = Label((0,0), int(rect.height * 0.8), '', text_color) # Text in der textBox
        
        self.pos = rect.topleft
        self.rect = rect
        self.padding = round(4 + self.rect.w / 120) # Zwischen Rand und Textanfang
        self.max = max
        
        self.color = color
        self.text_color = text_color
        self.text = self.label.text

        # Typing/Schreiben Sound speichern
        self.sound = pygame.mixer.Sound('Sounds/typing.wav')

    # Funktion, um die textBox zu "betreten"/Eingaben zu tätigen
    def run(self, screen):
        """ (args)
        screen = Surface auf dem die Textbox liegt
        """
        Clock = pygame.time.Clock()
        tick = 0 # aktueller Frame

        running = True
        while running:
            for event in pygame.event.get():
                # Falls "Fenster schließen"
                if event.type == pygame.QUIT:
                    screen.terminate()

                # Falls "Tastendruck"
                elif event.type == pygame.KEYDOWN:
                    # Falls Taste = Backspace
                    if event.key == pygame.K_BACKSPACE:
                        self.label.text = self.label.text[:-1] # Letzten Buchstabe des Textes entfernen
                    # Falls Taste = Enter
                    elif event.key == pygame.K_RETURN:
                        running = False # Eingabe beenden
                    
                    # Falls Länge des Textes unter Maximallänge
                    elif len(self.label.text) < self.max:
                        pygame.mixer.Sound.play(self.sound) # Typing-Sound abspielen
                        self.label.text += event.unicode # Gedrückte Taste hinzufügen
                    tick = 0 # Frame/Tick zurücksetzen

                # Falls "Mausklick" außerhalb der textBox
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.rect.collidepoint(event.pos):
                    running = False

            self.update(screen, tick)

            # Framerate reduzieren und nächsten Tick erhöhen
            Clock.tick(30)
            tick += 1 if tick < 30 else -30

        # Text entnehmen und abspeichern
        self.text = self.label.text

    # textBox aktualisieren
    def update(self, screen, tick):
        """ (args)
        screen = Surface auf dem die textBox liegt
        tick = Aktueller Tick/Frame
        """
        self.surf.fill(self.color)

        label = self.label()
        # Label positionieren
         # Falls Label größer als textBox
        if label.get_rect().w >= self.rect.w - self.padding * 2:
            x = self.rect.width - self.padding - 8 - label.get_rect().w
            self.label.pos = (x,0)
         # Falls Labelgröße in textBox
        else:
            self.label.pos = (self.padding, 0)
        self.surf.blit(label, self.label.pos)
        
        # Falls tick zwischen 0-15: Linie malen
        if tick <= 15:
            x = self.label.pos_x + label.get_rect().w + 4
            y = self.rect.h * 0.15
            pygame.draw.line(self.surf, self.text_color, (x,y), (x,self.rect.h - y), 4)

        # Umrandung der textBox malen
        pygame.draw.rect(self.surf, farben['schwarz'], (0,0, self.rect.w-1, self.rect.h-1), 4)
        screen.blit(self.surf, self.pos)

        pygame.display.update()

    # Dunder-String gibt Art der Instanz an
    def __str__(self):
        return 'textBox'

    # Dunder-Call gibt Surface der textBox zurück
    def __call__(self):
        self.surf.fill(self.color)

        label = self.label()
        # Label positionieren
         # Falls Label größer als textBox
        if label.get_rect().w >= self.rect.w - self.padding * 2:
            x = self.rect.width - self.padding - 8 - label.get_rect().w
            self.label.pos = (x,0)
         # Falls Labelgröße in textBox
        else:
            self.label.pos = (self.padding, 0)
        
        self.surf.blit(label, self.label.pos)
        # Umrandung der textBox malen
        pygame.draw.rect(self.surf, farben['schwarz'], (0,0, self.rect.w-1, self.rect.h-1), 4)
        
        return self.surf


# Folgende Klassen sind speziell für Panels gemacht

class Rect(Label):
    def __init__(self, rect, color, width=0):
        x,y,w,h = rect

        self.rect = pygame.Rect((x,y), (w,h))
        self._pos = (x,y)
        self.color = color
        self.line_w = width

    # Dunder-String gibt dir Art der Instanz zurück
    def __str__(self):
        return 'Rect'

class Line(Label):
    def __init__(self, start, end, color, width=5):
        self.start = start
        self.end = end
        self.color = color
        self.width = width

    # Dunder-String gibt dir Art der Instanz zurück
    def __str__(self):
        return 'Line'