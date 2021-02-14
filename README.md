# Python-Pygame UNO
Von Niclas Berger                                                   
                                                                     

!!! Das Uno-Programm benutzt die Python-Library "pygame" !!!

Um das Programm zu starten, main.py ausführen.


Das Programm besteht aus drei Datein:
 - main.py
 	=> Beinhalten das GUI des Programms und stellt
 	   den Hauptteil des Programms dar

 - Toolbox.py
 	=> Beinhaltet selbst erstellte Bausteine für
 	   pygame nach den Steuerelementen von Windows-Forms

 - Uno_text.py
 	=> Für die Verarbeitung der Züge und das erstellen des Spiels 
 	   "zuständig" (repräsentiert UserStory 1-9 [ohne Textausgaben])

Außerdem gibt es 2 Ordner:
 - Images
 	=> 2 Weitere Ordner und 2 Bilder für Hauptmenü-Hintergrund und icon
 		- Default: Standart Uno-Kartendeck
 		- minimalista: Spezielles Uno-Kartendeck (nach https://buyminimalisticcards.com/de)
 		! Alle Kartendecks wurden selbst (von mir) erstellt (Gimp-Vorlagen in den Ordnern)

 - Sounds
    => Alle Sounds/Musik, die im Programm verwendet wird


*** FUNKTIONEN DES SPIELS/PROGRAMMS ***

- Sounds und Musik im GUI
- Automatische speicherung/auslesung der eingestellten Optionen in/aus der Datei "data.txt" (erst nach erster Benutzung vorhanden)

1. Uno-Spiel:
	(Spieleinstellungen)
	- Angabe der Spielerzahl
	- Spielernameneingabe
	- Angabe der Handkartenanzahl
	- Eingabenvalidierung

	(Spiel)
	- Darstellung der Handkarten
	- Darstellung des Ablagestapels
	- Datstellung des Ziehstapels
	- Anzeige des aktuellen Spielernamens
	- Anzeige der anderen Spielernamen inkl. Handkartenanzahl
	- Darstellung der aktuell Ausgewählten Karte
	- Ablegen einer Karte / Spielen von Uno (inkl. Sonderkarten)

	(Pause-Menü)
	- Aufrufbar durch Tastendruck auf "Escape" (ESC)
	- Verlassen des Menüs (Fortfahren-Button)
	- Optionen-Szene aufrufen und Änderungen anwenden (Optionen-Button)
	- Spiel abbrechen bzw. zum Hauptmenü (Spiel beenden-Button)

	(Endmenü)
	- Einblendung / Ausblendung
	- Anzeige des Gewinners
	- Button, um zum Hauptmenü zurückzukehren

2. Hauptmenü:
	- Einblendung
	- Spiel starten Button (Uno starten)
	- Optionen Button (Optionen-Szene)
	- Button, um Spiel zu beenden

3. Optionen:
	- Einblendung
	- Auflösung ändern
	- Sound-Lautstärke ändern
	- Musik-Lautstärke ändern
	- Kartendeck ändern
	- Zurück Button, um Optionen zu verlassen
	- Anwenden Button, um Änderungen anzuwenden
