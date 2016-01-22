"""
Mini-project #6 for Introduction to Interactive Programming in Python. Blackjack.
Written on: 24/07/2015 
"""
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

dealer_hand_pos = [20, 150]
player_hand_pos = [20, 450]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        x = ""
        for card in self.cards:
            x = x + str(card) + " "
        return x

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = sum([VALUES[card.get_rank()] for card in self.cards])
        if 'A' in [card.get_rank() for card in self.cards]:
            if value + 10 <= 21:
                value += 10
        return value
   
    def draw(self, canvas, pos):
        for k in range(len(self.cards)):
            card_pos = [0,0]
            card_pos[0] = pos[0] + k * CARD_SIZE[0] + 50
            card_pos[1] = pos[1]

            self.cards[k].draw(canvas, card_pos)
 
        
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)   

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop(0)
    
    def __str__(self):
        # return a string representing the deck
        x = ""
        for card in self.cards:
            x = x + str(card) + " "
        return x 

def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, in_play, score

    if in_play:
        outcome = "You lost. Press 'Deal' again for a new game."
        score -= 1 
        in_play = False
    else: 
        # shuffle cards and create new p's and d's hands
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()

        # add 2 cards to each hand
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())

        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

        # for debugging: print to console
        #print("Player hand: " + str(player_hand))
        #print(player_hand.get_value())
        #print("Dealer hand: " + str(dealer_hand))
        #print(dealer_hand.get_value())

        outcome = "Hit or stand?"
    
        in_play = True

def hit():
    global outcome, in_play, deck, player_hand, dealer_hand, in_play, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted. New deal?"
            score -= 1
            in_play = False
        else:
            outcome = "Hit or stand?"
       
        #print("Player hand: " + str(player_hand))
        #print(player_hand.get_value())

    
def stand():
    global outcome, in_play, deck, player_hand, dealer_hand, in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        #print("Dealer hand: " + str(dealer_hand))
        #print(dealer_hand.get_value())
        
        if dealer_hand.get_value() > 21:
              outcome = "Dealer has busted. New deal?"
              score += 1
        else:
              if dealer_hand.get_value() >= player_hand.get_value():
                  outcome = "Dealer won. New deal?"
                  score -= 1
              else:
                  outcome = "You won. New deal?"
                  score += 1
    else:
        outcome = "You have busted. New deal?"
  
                 
    # assign a message to outcome, update in_play and score
    in_play = False
    
def draw(canvas):
    global score, outcome, in_play
    
    canvas.draw_text("BLACKJACK", [200,50], 40, 'Black')
    canvas.draw_text("Dealer:", [10, 100], 40,'Black')
    canvas.draw_text("Player:", [10, 400], 40, 'Black')
    canvas.draw_text("Score: " + str(score), [400, 350], 40, 'Blue')
    canvas.draw_text(outcome, [10, 300], 30, 'Magenta')
    
    dealer_hand.draw(canvas, dealer_hand_pos)
    player_hand.draw(canvas, player_hand_pos)

    # draw the back of card over dealer's hole if in_play
    if in_play:
        card_loc = CARD_BACK_CENTER
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, \
                          [dealer_hand_pos[0] + CARD_BACK_CENTER[0] + 50, dealer_hand_pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)        
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
