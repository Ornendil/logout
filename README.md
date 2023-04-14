# Logout-skript

Skript til publikums-PCer som kjører Linux Mint med gjestebruker. Det kan nok også brukes på andre lignende distribusjoner, men er ikke testet. Skriptet teller tiden låneren har brukt PCen og logger automatisk ut ved inaktivitet.

Det legger en liten widget sentrert øverst på skjermen, der den er i veien for minst mulig.

Widgeten viser tiden låneren har vært logget inn og en logg-ut-knapp. Hvis låneren ikke har rørt tastatur eller mus på et minutt blir widgeten rød og tidtakeren begynner å telle ned. Etter ytterligere fem minutter blir låneren automatisk logget ut.

![Tidtaker](https://github.com/Ornendil/logout/blob/main/Screenshot2.png?raw=true)

## Installere

1. Sørg for at ```python3``` og ```pyqt5``` er installert
2. Lagre ```logout.py``` i ```/opt/logout/``` eller lignende sted.
3. Legg til skriptet ```logout.py``` blant oppstartsprogrammer på gjestebrukeren.

## Innstillinger

```idleCountdownShow```: hvor mange sekunder med inaktivitet (i sekunder) som skal gå før widgeten viser nedtellingen.

```idleCountdownEnd```: hvor mange sekunder med inaktivitet (i sekunder) som skal gå før låneren blir automatisk logget ut.

Det er mulig å legge til støtte for flere språk ved å legge dem til i if-else-uttrykket på linje 20-27. Per nå støtter skriptet norsk og engelsk, basert på hvilket språk låneren har logget inn med.

## Ting å tenke på

Hvis dere bruker en nettleser som ikke har et tittelfelt øverst, og nettleser-fanene dermed blir liggende under widgeten, bør dere endre innstillingene for nettleseren. Ihvertfall Chrome har mulighet til å velge om man vil ha tittelfelt synlig. Firefox i Linux Mint har tittelfelt synlig som standard per nå (april 2023).
