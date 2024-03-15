# Python Blackjack
#
# For this project you will make a Blackjack game using Python. Click here to familiarize yourself with the rules of the game.
# You won't be implementing every rule "down to the letter" with the game, but we will be doing a simpler version of the game.
# This assignment will be given to further test your knowledge on object-oriented programming concepts.
# Rules:
#
# 1. The game will have two players: the Dealer and the Player. The game will start off with a deck of 52 cards.
# The 52 cards will consist of 4 different suits: Clubs, Diamonds, Hearts and Spades. For each suit, there will be cards numbered 1 through 13.
# Note: No wildcards will be used in the program
#
# 2. When the game begins, the dealer will shuffle the deck of cards, making them randomized.
# After the dealer shuffles, it will deal the player 2 cards and will deal itself 2 cards from.
# The Player should be able to see both of their own cards, but should only be able to see one of the Dealer's cards.
#
# 3. The objective of the game is for the Player to count their cards after they're dealt.
# If they're not satisfied with the number, they have the ability to 'Hit'.
# A hit allows the dealer to deal the Player one additional card. The Player can hit as many times as they'd like as long as they don't 'Bust'.
# A bust is when the Player is dealt cards that total more than 21.
#
# 4. If the dealer deals the Player cards equal to 21 on the first deal, the Player wins. This is referred to as Blackjack.
# Blackjack is NOT the same as getting cards that equal up to 21 after the first deal. Blackjack can only be attained on the first deal.
#
# 5. The Player will never see the Dealer's hand until the Player chooses to 'stand'.
# A Stand is when the player tells the dealer to not deal it anymore cards. Once the player chooses to Stand,
# the Player and the Dealer will compare their hands. Whoever has the higher number wins. Keep in mind that the Dealer can also bust.
import random
import time


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if self.value == 1:
            self.face = "Ace"
        elif self.value == 11:
            self.face = "Jack"
        elif self.value == 12:
            self.face = "Queen"
        elif self.value == 13:
            self.face = "King"
        else:
            self.face = None

    def __str__(self):
        if self.face:
            return f"{self.face} of {self.suit}"
        else:
            return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        # Create a deck of cards with four suits and values from 1 to 13
        for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)  # Shuffle the deck

    def deal(self):
        # Deal a card from the deck
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []  # Player's hand
        self.bet = 0  # Amount of bet placed by the player

    def add_card(self, card):
        # Add a card to the player's hand
        self.hand.append(card)

    def calculate_total(self):
        # Calculate the total value of the player's hand
        total = 0
        for card in self.hand:
            if card.value == 1:
                total += 11  # Ace can be 1 or 11, start with 11
            elif card.value > 10:
                total += 10  # Face cards are worth 10
            else:
                total += card.value
        num_aces = sum(1 for card in self.hand if card.value == 1)
        while total > 21 and num_aces > 0:
            total -= 10  # Adjust for Aces if total is over 21
            num_aces -= 1
        return total

    def place_bet(self, amount):
        # Place a bet
        if amount <= self.balance:  # Check if the player has enough balance to place the bet
            self.bet = amount
            self.balance -= amount  # Deduct the bet amount from the player's balance
            return True
        else:
            print(f"{self.name}, you don't have enough balance to place a bet of {amount}.")
            return False


class Game:
    def __init__(self):
        self.deck = Deck()  # Initialize the deck
        self.player = Player("Player", 100)  # Initialize the player with a balance of 100 credits
        self.dealer = Player("Dealer", float('inf'))  # Dealer has infinite credits

    def deal_initial_cards(self):
        # Deal initial cards to the player and the dealer
        self.player.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def player_turn(self):
        # Player's turn to play
        while True:
            print("\nPlayer's Hand:")
            for card in self.player.hand:
                print(card)
            total = self.player.calculate_total()
            print(f"Total: {total}")
            if total == 21:
                print("Blackjack!")
                break
            elif total > 21:
                print("Busted! You lose.")
                break
            else:
                choice = input("Do you want to hit? (y/n): ")
                if choice.lower() == 'y':
                    time.sleep(1)
                    self.player.add_card(self.deck.deal())
                else:
                    break

    def dealer_turn(self):
        # Dealer's turn to play
        while self.dealer.calculate_total() < 17:
            self.dealer.add_card(self.deck.deal())
        time.sleep(1)
        print("\nDealer's Hand:")
        for card in self.dealer.hand:
            print(card)
        total = self.dealer.calculate_total()
        print(f"Total: {total}")
        if total > 21:
            print("Dealer busted! You win!")
            self.player.balance += 2 * self.player.bet  # Player wins double their bet
        elif total >= self.player.calculate_total():
            print("Dealer wins!")
        else:
            print("You win!")
            self.player.balance += 2 * self.player.bet  # Player wins double their bet

    def place_bet(self):
        # Prompt the player to place a bet
        while True:
            try:
                amount = int(input(f"Place your bet (minimum 1 credit):\nYou currently have ${self.player.balance} available to bet. "))  # Get the bet amount from the player
                if amount >= 1:  # Check if the bet amount is valid
                    if self.player.place_bet(amount):  # Place the bet if the player has enough balance
                        break
                else:
                    print("Invalid bet amount. Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def play(self):
        print('Welcome to Python Blackjack!')
        while True:
            self.deal_initial_cards()  # Deal initial cards
            self.place_bet()  # Place a bet before starting the game
            self.player_turn()  # Player's turn
            if self.player.calculate_total() <= 21:  # Check if the player hasn't busted
                self.dealer_turn()  # Dealer's turn
            print(f"Your balance: {self.player.balance} credits")
            if self.player.balance == 0:  # Check if the player has run out of credits
                print("You have run out of credits. Game over.")
                break
            play_again = input("Do you want to play again? (y/n): ")
            if play_again.lower() != 'y':
                print("Thanks for playing!")
                break


game = Game()
game.play()
