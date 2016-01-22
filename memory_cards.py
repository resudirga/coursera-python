"""
Mini-project #5 for Introduction to Interactive Programming in Python. Implementation of card game - Memory
Written on: 21/07/2015 
"""

import simplegui
import random

WIDTH = 800
HEIGHT = 150
CARD_WIDTH = 50

# helper function to initialize globals
def new_game():
    global deck, exposed, state, prev_index, nturns 

    nturns = 0
    
    # generate deck of cards and shuffle
    deck = [x for x in range(8)]
    deck += deck
    
    random.shuffle(deck)

    # initialize exposed
    exposed = [False] * len(deck)

    # initialize state of game and indices of previous 2 exposed cards
    state = 0
    prev_index = [len(deck)] * 2
    
# define event handlers
def mouseclick(pos):
    global deck, card_index, exposed, prev_index, state, nturns

    card_index = len(deck) #set default card index to 16; for cases when area outside card boundary is pressed
    
    # get the card index upon mouse click. Set index to 16 if outside card boundaries
    if 20 < pos[1] < HEIGHT - 20:
        card_index = pos[0]//CARD_WIDTH

    # game logic
    if card_index in range(len(deck)) and not exposed[card_index]:

        exposed[card_index] = True
        
        if state == 0:
            state = 1
            prev_index[0] = card_index
        elif state == 1:
            nturns += 1
            state = 2
            prev_index[1] = prev_index[0]
            prev_index[0] = card_index
        elif state == 2:
            if deck[prev_index[0]] != deck[prev_index[1]]:
                exposed[prev_index[0]] = False
                exposed[prev_index[1]] = False
            state = 1
            prev_index[0] = card_index 
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck, exposed, nturns

    label.set_text("Turns = " + str(nturns))

    for k in range(len(deck)):
        if exposed[k]:
            canvas.draw_polygon([(k*CARD_WIDTH,20), \
                                 ((k+1)*CARD_WIDTH,20), \
                                 ((k+1)*CARD_WIDTH,HEIGHT-20), \
                                 (k*CARD_WIDTH,HEIGHT -20)], \
                                5,"Red","Yellow")
            canvas.draw_text(str(deck[k]), [k*CARD_WIDTH+5, HEIGHT-45], \
                             80, "Black")
        else:
            canvas.draw_polygon([(k*CARD_WIDTH,20), \
                                 ((k+1)*CARD_WIDTH,20), \
                                 ((k+1)*CARD_WIDTH,HEIGHT-20), \
                                 (k*CARD_WIDTH,HEIGHT -20)], \
                                5,"Red","Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
