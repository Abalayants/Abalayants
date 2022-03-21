from dataclasses import dataclass, field
import random
from typing import List
from itertools import permutations, product
from art import logo
import os

RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()
SUITS = "♣ ♢ ♡ ♠".split()


@dataclass
class Card:
    """
    Card Class for single card identification
    Allows for str representation
    """

    rank: str
    suit: str

    def __str__(self):
        return f"{self.rank}{self.suit}"


@dataclass()
class Deck:
    """
    Deck will create a deck with all normal deck ranks/suits in a list.
    Shuffle deck.
    Deal one card.
    Allows for returned str representation
    """

    """Using itertools to define a function to create a deck out of global variables RANKS & SUITS"""
    init_deck = lambda: [Card(r, s) for r, s in product(RANKS, SUITS)]
    all_cards: List[Card] = field(default_factory=init_deck)

    def shuffle_deck(self):
        """Shuffle the deck"""
        random.shuffle(self.all_cards)

    def deal_cards(self, num_cards: int) -> List[Card]:
        """
        Returns cards: Card that is pulled from all_cards list
        """
        return [self.all_cards.pop() for _ in range(num_cards)]

    def __repr__(self):
        """Return string representation of hand/s"""
        return ", ".join(map(str, self.all_cards))


@dataclass()
class Hand:
    """Class for individual hand. Player can have more than one for split function.

    Attributes:
        cards: List of all cards in hand
        values: List of all potential values
        bet: Integer value of the bet
        is_bust: Boolean returning bust or not
        is_blackjack: Boolean specifying if hand is blackjack
        show_one_card: For Dealer, whether to show only card when printing the hand

    """

    cards: List[Card] = field(default_factory=list)
    values: List[int] = field(default_factory=list)
    max_non_bust_value: int = 0
    is_blackjack: bool = False
    is_bust: bool = False
    bet: int = 0
    show_one_card: bool = False

    def __post_init__(self):
        """
        Post initialization of the data class
        This will process the hand that is dealt since it is not done in original deal of 2 cards
        """

        self.process_hand()

    def add_bet(self, value: int):
        """adding value of bet to bet attribute"""

        self.bet += value

    def add_cards(self, cards: List[Card]):
        self.cards.extend(cards)
        self.process_hand()

    def process_hand(self):
        """
        Get all possible hand values, check for bust or blackjack
        """
        self.compute_card_values()
        self.is_bust = all(map(lambda v: v > 21, self.values)) # boolean
        if len(self.cards) == 2: 
            self.is_blackjack = any(map(lambda v: v == 21, self.values))

    def compute_card_values(self):
        """
        Gets individual values for ace and non-ace cards
        Provides all possible permutations of values with any/all aces in the hand
        Provides the highest value without bust out of a list of all possible values
        """
        cards = list(map(lambda c: c.rank, self.cards))
        non_ace_cards = list(filter(lambda c: c != "A", cards))
        ace_cards = list(filter(lambda c: c == "A", cards))
        non_ace_value = sum(int(i) if i.isnumeric() else 10 for i in non_ace_cards)

        if ace_cards:
            num_aces = len(ace_cards)
            list_of_ace_values = permutations([1, 11] * num_aces, num_aces)
            list_of_ace_values = set(map(sum, list_of_ace_values))
        else:
            list_of_ace_values = {0}

        values = map(lambda v: v + non_ace_value, list_of_ace_values)
        self.values = sorted(list(values))
        self.max_non_bust_value = list(filter(lambda c: c <= 21, self.values))
        self.max_non_bust_value = 0 if self.max_non_bust_value == [] else max(self.max_non_bust_value)

    def pop_card(self):
        return self.cards.pop()

    def __str__(self) -> str:
        if self.show_one_card:
            cards_str = "-".join(map(str, ["*", self.cards[-1]]))
            value_str = "*"
        else:
            cards_str = "-".join(map(str, self.cards))
            value_str = "/".join(map(str, self.values))
        return f"cards: {cards_str} | values: {value_str}"


@dataclass()
class Player:
    """
    Class for creating any # of players, give them a name/hand/bank
    
    """

    name: str
    bank: int = 0
    # Assigns a hand object to a list belonging to a player
    hands: List[Hand] = field(default_factory=lambda: [Hand()])

    def reset_hand(self):
        self.hands = [Hand()]

    def has_enough_money(self, bet: int) -> bool:
        return self.bank >= bet

    def __str__(self):
        return "\n".join(map(str, [self.name] + self.hands))


class Game:
    """
    The Game itself.
    1. Initialize Deck
    2. Shuffle Deck
    3. Dealer is only showing one card
    4. Ask users for # of players, their names, and to choose a buy in amount.
    5. Add all players to player list
    """
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.dealers_hand = Hand(show_one_card=True)
        self.players = []
        print(logo)
        num_players = int(input("How many players are at the table? "))

        for player_idx in range(num_players):
            player_name = input(f"\nPlayer {player_idx + 1}, what is your name? ")
            player_bank = int(input(f"\n{player_name}, how much do you want to buy in for? "))
            self.players.append(Player(player_name, player_bank))

    def reset_table(self):
        """
        Resets deck/hands/bets/dealer
        """
        self.dealers_hand = Hand(show_one_card=True)
        for player in self.players:
            player.reset_hand()
        self.deck = Deck()
        self.deck.shuffle_deck()

    @staticmethod
    def ask_to_stop():
        want_to_stop = input("\nWould you like to play again? (Y or N): ")
        return want_to_stop == "N".lower()

    def print_table(self):
        """Visual representation of table"""
        for player in self.players:
            print("\n" + str(player))
        print(f"\nDealer: \n{self.dealers_hand}")

    def __call__(self):
        """
        Function calls for the game class:
            Gets bets and creates a hand for players
            Checks for dealer blackjack
            Asks to play again after the initial hand is played
            Resets output screen
        """
        stop_game = False

        while not stop_game:
            self.init_bets()
            self.init_hands()
            if not self.dealers_hand.is_blackjack:
                self.play_round()
                self.dealer_turn()
            self.check_and_payout()
            stop_game = self.ask_to_stop()
            self.reset_table()
            os.system("cls")
            print(logo)

    def init_bets(self):
        """Initialize the original pre-deal bet, check against player bank, remove bet from bank"""
        for player in self.players:
            # really high number
            bet = int(1e10)
            while not player.has_enough_money(bet):
                bet = int(input(f"\n{player.name}, You have {player.bank}. How much do you want to bet? "))
            player.hands[0].add_bet(bet)
            player.bank -= bet

    def init_hands(self):
        """first hand for players and dealer, using list of hand objects. Each object gets 2 cards cumulatively"""
        all_hands = [player.hands[0] for player in self.players] + [self.dealers_hand]
        for hand in all_hands * 2:
            hand.add_cards(self.deck.deal_cards(1))

    def play_round(self):
        """Action to play all hands for all players"""
        for player in self.players:
            for hand in player.hands:
                is_hand_done = hand.is_blackjack

                while not is_hand_done:

                    """Player decision which uses ask_player_decision method from below"""
                    decision = self.ask_player_decision(player, hand)
                    if decision == "stand":
                        is_hand_done = True
                    elif decision == "hit":
                        hand.add_cards(self.deck.deal_cards(1))
                    elif decision == "double":
                        player.bank -= hand.bet
                        hand.bet *= 2
                        hand.add_cards(self.deck.deal_cards(1))
                        self.print_table()
                        is_hand_done = True
                    else:
                        print("You have chosen to split. ", "\r")
                        # pop card from hand into a variable
                        split_card = hand.pop_card()
                        # create new hand with the same bet as original hand and the popped card.
                        new_hand = Hand([split_card, *self.deck.deal_cards(1)], bet=hand.bet)
                        hand.add_cards(self.deck.deal_cards(1))
                        # retrieve bet from bank
                        player.bank -= hand.bet
                        player.hands.append(new_hand)

                    """Check for finished action on hand, or bust, or blackjack"""
                    is_hand_done = bool(is_hand_done or hand.is_bust or hand.is_blackjack)

    def ask_player_decision(self, current_player, current_hand):
        """
        All possible actions a user can take to play each hand limited to rules of the game
        """
        possible_decisions = ["hit", "stand"]
        if current_player.has_enough_money(current_hand.bet) and len(current_hand.cards) == 2:
            possible_decisions.append("double")
            if current_hand.cards[0].rank == current_hand.cards[1].rank:
                possible_decisions.append("split")
                # A concise way to check if original two cards = one another by using set
                # if len(set(map(lambda card: card.rank, current_hand.cards))) == 1:
        self.print_table()
        decision = ""
        while decision not in possible_decisions:
            decision = input(f"\n{current_player.name} your options are: {', '.join(possible_decisions)}\n"
                             f"\nWhat would you like to do? ")
        return decision

    def dealer_turn(self):
        """Max value that isn't over 21 id'ed and played out"""
        print("\nDealer Turn!\n")
        self.dealers_hand.show_one_card = False
        while 0 < self.dealers_hand.max_non_bust_value < 17:
            self.dealers_hand.add_cards(self.deck.deal_cards(1))
        self.print_table()

    def check_and_payout(self):

        for player in self.players:
            for hand in player.hands:
                if not hand.is_bust:

                    # Case 1: Both Tie
                    if self.dealers_hand.max_non_bust_value == hand.max_non_bust_value:
                        print(f"\n{player.name} you tied the house. ", "\r")
                        player.bank += hand.bet

                    # Case 2: Dealer Bust
                    if self.dealers_hand.is_bust:
                        print(f"\nDealer busts! {player.name} you win. ")
                        player.bank += (hand.bet * 2)

                    # Case 3: Player Win
                    if self.dealers_hand.max_non_bust_value < hand.max_non_bust_value:
                        print(f"\n{player.name} your hand beats the house. ", "\r")
                        player.bank += (hand.bet * 2)

                    # Case 4: Player is BJack
                    if hand.is_blackjack:
                        print(f"\n{player.name} you have 21. You win")
                        player.bank += (hand.bet * 2.5)

                    # Printing Dealer Win for reference
                    if self.dealers_hand.max_non_bust_value > hand.max_non_bust_value:
                        print(f"\nDealer had {self.dealers_hand}")


new_game = Game()

new_game()
