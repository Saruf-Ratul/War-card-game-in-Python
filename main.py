import random
import pickle

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self):
        return self.hand.pop(0)

def save_game(players):
    with open('savegame.pkl', 'wb') as file:
        pickle.dump(players, file)

def load_game():
    try:
        with open('savegame.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

def war_game():
    print("Welcome to the War card game!")

    # Check for saved game
    players = load_game()

    if not players:
        # Set up a new game
        player1 = Player("Player 1")
        player2 = Player("Player 2")

        deck = Deck()
        for _ in range(len(deck.cards) // 2):
            player1.add_card(deck.deal())
            player2.add_card(deck.deal())

        players = [player1, player2]

    while True:
        for player in players:
            print(f"{player.name}'s turn.")
            input("Press Enter to play a card...")

            card = player.play_card()
            print(f"{player.name} played: {card}")

        # Check the winner
        if player1.hand[-1].rank > player2.hand[-1].rank:
            print("Player 1 wins the round!")
            player1.add_card(player2.play_card())
        elif player1.hand[-1].rank < player2.hand[-1].rank:
            print("Player 2 wins the round!")
            player2.add_card(player1.play_card())
        else:
            print("It's a tie! WAR!")

            # In a tie, play 3 additional cards
            for _ in range(3):
                for player in players:
                    print(f"{player.name}'s turn.")
                    input("Press Enter to play a card...")
                    player.play_card()

            # Check the winner again after the tiebreaker
            if player1.hand[-1].rank > player2.hand[-1].rank:
                print("Player 1 wins the round!")
                player1.add_card(player2.play_card())
            elif player1.hand[-1].rank < player2.hand[-1].rank:
                print("Player 2 wins the round!")
                player2.add_card(player1.play_card())
            else:
                print("It's a tie again! The war continues...")

        # Check for a winner
        if not player1.hand:
            print("Player 2 wins the game!")
            break
        elif not player2.hand:
            print("Player 1 wins the game!")
            break

        # Save the game state
        save_game(players)

if __name__ == "__main__":
    war_game()
