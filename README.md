# RaspberryPiProject

3 codes:

- Scherm-client
- Game engine
- Controller



Communication MQTT:
Controller en gameserver:
- Authenticatie:

 de controller stuurt een ? met een nummer erachter. de controller zelf kiest dit nummer
wanneer de game server een vraagteken ziet met een nummer erachter zal die hierop reageren met ? en nummer en dan een id van 1 of 0
de controller zal blijven kijken totdat hij een antwoordt krijgt met op zijn request en zal de id eruit pakken en dit zal hij dan altijd gebruiken tijdens het spel

- Controller commando's naar gameserver:

de controller zal commando's sturen door de volgende  bericht te sturen "ID=x UP=y SP=z"
De x zal het id zijn van de controller dus 0 of 1
de y zal een string of bool zijn om aan te geven dat het naar boven is of naar beneden
de z zal de snelheid zijn/ hoeveel dat die moet bewegen

- Gameserver en schermclients:

de gameserver zal heletijd het volgende bericht sturen naar de verschillende clients
L=a R=b B=c,d
De a is de hoogte van de linkse speler
de b is de hoogte  van de rechtste speler
c en d zijn de X en Y coördinaten van de bal
