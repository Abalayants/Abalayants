<h1>About the Project</h1>

A Blackjack game for multiple users to simulate a casino table. The rules reflect <a href="https://www.officialgamerules.org/blackjack">official blackjack rules</a>.

<h2>Process</h2>

For the visual plan: <a href="https://github.com/Abalayants/PersonalProjects/blob/main/blackjack%20diagram.png">please see diagram</a>. The main goal was to be able to have multiple players, for whom multiple hands had to be a possibility. Hence, Hand and Player class are written separate, which will also allow for a dealer as well. 

Note that a Game class was added later to organize the gameplay into appropriate parts. The Game class not only runs the game per the rules, but also uses function __call__ method for all the steps necessary to play a round. It also gives a way to show visual representation of the game "table," payouts of bets, and resetting of the table.

<h2>Libraries</h2>

<b>Dataclass</b>: Utilizing dataclass library to organize and initialize attributes in a clean manner.

<b>Random</b>: Strictly to shuffle the cards.

<b>Typing</b>: Used for type-hinting.

<b>Itertools</b>: Used for permutations for all possible values for the "A" card for calculating hand values. Product to create full deck from possible combinations.
