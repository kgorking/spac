import random


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def value(self):
        val = 0
        if self.face in ['J', 'Q', 'K']:
            val += 10
        elif self.face == 'A':
            val += 11
        else:
            val += self.face
        return val

    def is_ace(self):
        return self.face == 'A'

    def __repr__(self):
        return f"{self.suit} {self.face}"


class Deck:
    def __init__(self):
        suits = ['♥', '♦', '♣', '♠']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)
  
    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()
  
    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            has_ace = has_ace or card.is_ace()
            self.value += card.value()
      
        if has_ace and self.value > 21:
            self.value -= 10

  
    def calculate_dealer_value(self):
        value = 0
        has_ace = False

        for card in self.cards[1:]:
            has_ace = has_ace or card.is_ace()
            value += card.value()
      
        if has_ace and self.value > 21:
            value -= 10

        return value


class Player:
    def __init__(self):
        self.hand = Hand()
        self.done = False

    def __repr__(self):
        return f"{self.hand.value:2}  {self.hand.cards}"

    def value(self):
        return self.hand.value
  
    def take_card(self, deck: Deck, count = 1):
        for i in range(count):
            self.hand.add_card(deck.deal_card())
        self.done = self.bust()

    def bust(self):
        return self.value() > 21

    def hit_or_stand(self, deck: Deck):
        if self.done:
            return True

        choice = input("(h)it or (s)tand? ")
        while choice not in ['s', 'h']:
            choice = input("I said, (h)it or (s)tand? ")

        if choice == 'h':
            self.take_card(deck)
            self.done = (self.value() >= 21)
            print(f"Player: {self}")
        elif choice == 's':
            self.done = True


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hidden = True

    def __repr__(self):
        if self.hidden:
            return f"{self.hand.calculate_dealer_value():2}  {self.hand.cards[1:]}"
        else:
            return f"{self.hand.value:2}  {self.hand.cards}"

    def partial_value(self):
        return super().value() - self.hand.cards[0].value()

    def hit_or_stand(self, deck: Deck, player: Player):
        if self.value() < max(17, player.value()):
            self.take_card(deck)
            self.done = (self.value() >= 21)
            print(f"Dealer takes card: {self}")
        else:
            self.done = True
            print(f"Dealer stands with: {self}")

class Game:
    def run(self):
        deck = Deck()
        dealer = Dealer()
        player = Player()

        player.take_card(deck, 2)
        print(f"Player takes 2 cards: {player}")

        dealer.take_card(deck, 2)
        print(f"Dealer takes 2 cards: {dealer}")

        print()

        while not (player.done and dealer.done):
            if not player.done:
                player.hit_or_stand(deck)

            if not dealer.done:
                dealer.hit_or_stand(deck, player)

        dealer.hidden = False
        if player.value() == 21:
            print(f"Player has Blackjack! {player}")
        if dealer.value() == 21:
            print(f"Dealer has Blackjack! {dealer}")

        if player.bust():
            print(f"Player loses:  {player}")
        elif dealer.bust():
            print(f"Dealer loses:  {dealer}")
        else:
            print()
            print(f"Player: {player}")
            print(f"Dealer: {dealer}")
            if dealer.value() >= player.value():
                print("Dealer wins!")
            else:
                print("Player wins!")

game = Game()
game.run()
