# TeamOntspoord
Project RailNL voor Programmeer Theorie

TODO: Plaatjes toevoegen

## RailNL

Voordat een treinnetwerk in gebruik genomen kan worden, is het de bedoeling dat zo efficiënt mogelijk treintrajecten worden uitgestippeld. Het is niet de bedoeling dat er heel veel korte trajecten zijn, waardoor passagiers veel over zouden moeten stappen en er veel treinen in gebruik zijn. Het is ook niet de bedoeling dat de trajecten te lang zijn of dat teveel spoor onbereden blijft. Om de kwaliteit van de collectie treintrajecten, ook wel de lijnvoering genoemd, te toetsen is gebruik gemaakt van deze formule:

Kwaliteit = (Aantal bereden connecties / Totaal aantal connecties) * 10.000 - (Aantal trajecten * 100 + tijdsduur in minuten)

Des te hoger de kwaliteit, des te beter de lijnvoering. Het doel van dit project is om de beste lijnvoering te vinden. Met dit doel hebben wij meerdere algoritmes geschreven. Al deze algoritmes zijn aan te roepen in de commandline via main.py. 

# Gebruikshandleiding

UITLEG COMMANDLINE MAIN.PY

## De algoritmes

Het treinnetwerk waar de algoritmes gebruik van maken is opgebouwd uit vier klasses die allemaal staan in het mapje 'classes'. Zo zijn de stations en de connecties tussen de stations aparte klassen, beide staan in stations.py. De treintrajecten zijn ook een aparte klas, onder de naam 'Train' in train.py. Deze drie klasses zijn ondergebracht in de Railnet, in structure.py. Elk algoritme maakt gebruik van Railnet om bij de stations, connecties en treintrajecten te komen.

Het eerste algoritme is het random algoritme. Hierin wordt een willekeurige hoeveelheid treintrajecten aangemaakt, van 1 tot het maximaal aantal toegestane treintrajecten. Elk treintraject is compleet willekeurig gekozen, met als enige limiet dat het traject niet langer mag zijn dan de maximale tijdsduur. 

Random iteration (random_iteration.py) maakt gebruik van het random algoritme maar vervangt de treintrajecten door betere treintrajecten. Het maximaal aantal toegestane treintrajecten wordt aangemaakt - de treintrajecten zelf zijn wel nog steeds willekeurig gekozen. Vervolgens wordt voor elk treintraject 1000 nieuwe trajecten aangemaakt die het huidige treintraject mogelijk zouden kunnen vervangen. Van al deze treintrajecten wordt de kwaliteit vergeleken en de beste wordt gekozen. Als het verwijderen van het originele traject de hoogste kwaliteitsscore oplevert, wordt het traject verwijderd. 

Biased iteration (biased_iteration.py) volgt hetzelfde principe als random iteration - meerdere treintrajecten worden getoetst en de beste wordt gekozen - maar de trajecten worden niet meer willekeurig bepaald. Elke connectie in het spoornetwerk mag maar één keer gebruikt worden en het traject begint altijd bij een station waar nog één of meer ongebruikte connecties beschikbaar zijn. Een ander verschil is dat er minder nieuwe trajecten worden aangemaakt - voor elk treintraject zijn dat er hier 200. Er is geen betekenisvol verschil zichtbaar bij het eindresultaat voor hogere getallen na 200.

Het greedy algoritme (bad_algorithm.py) maakt gebruik van dezelfde vooringenomen trajecten als biased iteration. Connecties worden ook hier maar één keer gebruikt. Het verschil is dat het greedy algoritme doorgaat totdat alle connecties bereden zijn en niet de trajecten op kwaliteit toetst.

TODO DEPTH FIRST

Het hillclimber algoritme (simulated_annealing.py) maakt steeds kleine stapjes op zoek naar het beste resultaat. Eerst wordt een lijnvoering gemaakt met het random algoritme, wat vervolgens wordt verbeterd. De trajecten kunnen met één connectie verlengd of verkort worden, in tweeën gesplit worden en er kunnen ook geheel nieuwe trajecten aangemaakt worden - zolang het maar de kwaliteit van de lijnvoering ten goede komt.

De simulated annealing en reheating algoritmes zijn extensies van het hillclimber algoritme en staan in hetzelfde bestand (simulated_annealing.py). Een groot probleem met een hillclimber algoritme is dat het makkelijk vast komt te zitten in lokale maxima. Dit zijn in dit geval zijn dat kwaliteitsscores die niet met één stap van het hillclimber algoritme verbeterd kunnen worden - ook al is de lijnvoering dan niet het meest efficiënt. Met simulated annealing worden stappen van het hillclimber algoritme die de kwaliteit verslechteren tot op zekere hoogte toegelaten. Hoe hoog deze zekere hoogte is hangt af van de temperatuur.

TODO leg reheating en simulated annealing uit
