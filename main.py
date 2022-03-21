from dataclasses import dataclass, field
import random
from typing import List
import itertools
# from art import logo

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()


@dataclass
class Card:
    """Card Class for single card identification and for determining Ace value"""

    rank: str
    suit: str

    def __str__(self):
        return f"{self.rank} of {self.suit}"


@dataclass()
class Player:
    """ Player class for creating any # of players, give them a name/hand/bank """

    name: str

    # hand is a list of cards with an initial DEFAULT value of none or an empty list
    # DEFAULT VALUES MUST BE STATED
    bank: int = 0
    bet: int = 0
    values: int = 0
    hand: List[None] = field(default_factory=list)

    def compute_card_value(self, card):
        # J, Q, K needs to be a rank of 10 check a specified list of all possible card ranks
        if card.rank in ["J", "Q", "K"]:
            value = 10
        elif card.rank == "A":
            value = 1 if self.values > 10 else 11
        else:
            # numerical value for individual card which is passed as an argument/input
            value = int(card.rank)
        self.adjust_for_ace()
        return value

    def adjust_for_ace(self):
        if "A" in self.hand and self.values > 10:
            self.values -= 10
            return self.values

    def add_card_to_hand(self, card):
        self.hand.append(card)
        self.values += self.compute_card_value(card)


@dataclass()
class Dealer(Player):
    """Dealer will need to be able to have their own hand, and display only the second card after initial deal"""

    dealer_hand = []

    def show_dealer_hand(self):
        return f"Dealer is showing {self.dealer_hand[0]}"

    def add_card_to_hand(self, card):
        self.dealer_hand.append(card)
        self.values += self.compute_card_value(card)
        self.adjust_for_ace()


def new_deck():
    """ Using itertools to define a function to create a deck out of existing global variables RANKS & SUITS"""
    return [Card(r, s) for r, s in itertools.product(RANKS, SUITS)]


@dataclass()
class Deck:
    """Deck will create a deck with all normal deck ranks/suits in a list. Shuffle deck. Deal one card.
    Also return str """

    all_cards: List[Card] = field(default_factory=new_deck)

    def shuffle_deck(self):
        random.shuffle(self.all_cards)

    def deal_card(self):
        return self.all_cards.pop(0)

    def __repr__(self):
        return ", ".join([str(card) for card in self.all_cards])


def win_check(player_total, dealer_total):
    """ In order: tie, player blackjack, dealer blackjack, dealer wins, player wins, player bust, dealer bust"""
    # Determine the winner and adjust the Player's chips accordingly
    if (
        dealer_total == player_total
        and player.values <= 21
        and dealer.values <= 21
    ):
        return "tie"
    elif player_total == 21:
        return "win"
    elif dealer_total == 21:
        return "loss"
    elif player_total > 21:
        return "loss"
    elif dealer_total > 21:
        return "win"
    elif player_total < dealer_total:
        return "loss"
    elif dealer_total < player_total:
        return "win"


def black_jack_check(person, dealer_hand, players):
    for player in players:
        # Checks current player in loop against dealer for immediate blackjack
        if dealer_hand.values == 21 and person.values == 21:
            player.bank += player.bet
            print("Push. ")

        elif dealer.values == 21:
            print("Dealer has Blackjack. ")
            continue
        elif person.values == 21:
            player.bank += (player.bet * 2.5)
            print(f"{player.name}, you have blackjack!")
            continue


def get_players(num_players) -> list:
    players = []
    for _ in range(num_players):
        name = input("Please enter the new player's name: ")
        bank = input("How many chips are you buying in for? Please enter a numerical value: ")
        players.append(Player(name, int(bank)))
        print(f"{name} sat down at the table with {bank} chips. ")
    return players


def place_bet(players):
    for player in players:
        player.bet = 0
        place_bet = int(input(f"{player.name}, you have {player.bank} "
                              f"current chips. Please place your bet: "))
        while place_bet > player.bank:
            print("Bet exceeds current bank! ")
            break
        player.bet += place_bet
        player.bank -= place_bet


def deal_new_hand(players, dealer, deck):
    deck.shuffle_deck()
    for _ in players:
        player.hand.clear()
        dealer.dealer_hand.clear()
        player.values = 0
        dealer.values = 0
        player.add_card_to_hand(deck.deal_cards())
        player.add_card_to_hand(deck.deal_cards())
    for i in range(2):
        dealer.add_card_to_hand(deck.deal_cards())


def double_down(current_player: Player, hand):
    # print(f"{current_player.name}, you are showing {hand}")
    dbl = input("\nWould you like to double down (y or n)? ")
    if dbl != "y".lower():
        return "You did not double down\n"
    current_player.bank -= current_player.bet
    current_player.bet += current_player.bet
    hand.append(blackjack_deck.deal_card())
    return "done"


def hit_or_stay(player):
    player.add_card_to_hand(blackjack_deck.deal_card())
    print(f"{player.name} you got a {player.hand[-1]}")


def dealer_hit():
    print("All players have gone. Dealer turn... ")
    while dealer.values < 17:
        dealer.add_card_to_hand(blackjack_deck.deal_card())
    if dealer.values > 21:
        print("Dealer Busts...")

    print(dealer.dealer_hand)


dealer = Dealer("Dealer")
game_on = True

if __name__ == "__main__":
    number_of_players = int(input("Enter the amount of players: "))
    player_list = get_players(number_of_players)
    while game_on:
        blackjack_deck = Deck()
        place_bet(player_list)
        deal_new_hand(player_list, dealer, blackjack_deck)
        for player in player_list:
            # Checks current player in loop against dealer for immediate blackjack
            if dealer.values == 21 and player.values == 21:
                print("Push. ")
            elif dealer.values == 21:
                print("Dealer has Blackjack. ")
                continue
            elif player.values == 21:
                player.bank += (player.bet * 2.5)
                print(f"{player.name}, you have blackjack!")
                continue
            else:
                # Ask players if they want to double down
                double_down(player, player.hand)
                # players choice to hit and checks for busts
                while not player.values >= 21:
                    player_choice = input(f"{dealer.show_dealer_hand()},\n"
                                          f"{player.name} you have {player.hand} would you like to hit, y or n? ")
                    if player_choice == "y":
                        hit_or_stay(player)
                    else:
                        break
        # Dealer goes after all the players are satisfied with their choices
        dealer_hit()
        for player in player_list:

            if win_check(player.values, dealer.values) == "tie":
                player.bank += player.bet
                print(f"You tied. Dealer had {dealer.dealer_hand} and\n{player.name} had {player.hand}. ")
            elif win_check(player.values, dealer.values) == "win" and not player.values > 21:
                player.bank += (player.bet * 2)
                print(f"{player.name} wins. \nDealer had {dealer.dealer_hand}\n"
                      f"{player.name} had {player.hand}.")
            elif win_check(player.values, dealer.values) == "loss" and not dealer.values > 21:
                print(f"Dealer wins. \nDealer had {dealer.dealer_hand} and\n{player.name.title()} had {player.hand}. ")

        play_again = input("Would you like to play again, y or n? ")
        if play_again == "y" or "":
            game_on = True
        else:
            game_on = False
