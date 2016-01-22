"""
Mini project for Introduction to Interactive Programming in Python. Implementation of classic arcade game Pong.
Written on: 07/2015  
"""

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0] # number of pixels per update (1/60 sec)
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

def spawn_ball(direction):
    """ Spawn ball from the middle of table. Direction is randomized. """
    # initialize ball_pos and ball_vel for new ball in middle of table
    # if direction is RIGHT, the ball's velocity is upper right, else upper left
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(120, 240) / 60, \
                random.randrange(60, 180) / 60]
    
    if direction == LEFT:
        ball_vel[0] *= -1
    
def new_game():
    """ Start a new game """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # reset score
    score1 = 0
    score2 = 0
    
    # determine randomly the direction of ball
    if random.randrange(2):
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def draw(canvas):
    """ Update canvas """
    global score1, score2, paddle1_pos, paddle2_pos, \
            paddle1_vel, paddle2_vel, ball_pos, ball_vel 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ---- bounce ball if it hits sides (gutter or top)
    # left/right sides
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS - 1: # ball bounces off left gutter
        ball_vel[0] *= -1
        
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS: # ball bounces off right gutter
        ball_vel[0] *= -1
        
    # top    
    if ball_pos[1] <= BALL_RADIUS - 1 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1
    
    # -- draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # --- update paddles' vertical positions, keep paddle on the screen
    # left paddle
    if paddle1_pos >= HALF_PAD_HEIGHT and paddle1_pos <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    elif paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    # right paddle
    if paddle2_pos >= HALF_PAD_HEIGHT and paddle2_pos <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    elif paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
            
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), \
                         (PAD_WIDTH-1, paddle1_pos - HALF_PAD_HEIGHT - 1), \
                         (PAD_WIDTH-1, paddle1_pos + HALF_PAD_HEIGHT -1), \
                         (0, paddle1_pos + HALF_PAD_HEIGHT -1)], .5, \
                        'Yellow', 'Green')
    
    canvas.draw_polygon([(WIDTH-PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), \
                         (WIDTH-1, paddle2_pos - HALF_PAD_HEIGHT - 1), \
                         (WIDTH-1, paddle2_pos + HALF_PAD_HEIGHT -1), \
                         (WIDTH-PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT -1)], .5, \
                        'Yellow', 'Green')
    
    # determine whether paddle and ball collide 
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS - 1: # Ball hits left gutter
        # if paddle fails to strike ball, increase opponent's score and re-spawn ball towards \
        # the opponent's side (to the right)
        if ball_pos[1] < paddle1_pos - HALF_PAD_HEIGHT or ball_pos[1] > paddle1_pos + HALF_PAD_HEIGHT - 1:
            score2 += 1
            spawn_ball(RIGHT)
        else: # paddle strikes ball
            ball_vel[0] += (0.1 * ball_vel[0])
            ball_vel[1] += (0.1 * ball_vel[1])
            
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS: # Ball hits right gutter
        # same as above, but to the left
        if ball_pos[1] < paddle2_pos - HALF_PAD_HEIGHT or ball_pos[1] > paddle2_pos + HALF_PAD_HEIGHT - 1:
            score1 += 1
            spawn_ball(LEFT)
        else: # paddle strikes ball
            ball_vel[0] += (0.1 * ball_vel[0])
            ball_vel[1] += (0.1 * ball_vel[1])
            
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2 - 40, 40], 30,"White")
    canvas.draw_text(str(score2), [WIDTH/2 + 30, 40], 30,"White")  

def keydown(key):
    """ Move up/down paddles if the up/down/w/s keys is pressed """
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
    
def keyup(key):
    """ Set paddle velocity to a stop when the up/down/w/s key is pressed. """
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button('RESTART GAME', new_game, 150)

# start frame
new_game()
frame.start()
