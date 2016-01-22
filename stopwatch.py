""" 
Mini project for Introduction to Interactive Programming in Python. Stopwatch: The Game.
Written on: 18/6/2015  
"""
import simplegui

# define global variables
counter = 0
n_success = 0
n_stop = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    C = (t//10) % 10
    B = (t//100) % 6
    A = t//600
    return str(A) + ":" + str(B) + str(C) + "." + str(D)   
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global timer
    timer.start()

def stop_timer():
    global timer, counter, n_stop, n_success
    if timer.is_running():
        n_stop += 1
        if counter % 10 == 0:
            n_success += 1
    timer.stop()    

def reset_timer():
    global timer, counter, n_stop, n_success
    timer.stop()
    counter = 0  
    n_stop = 0
    n_success = 0
        
# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1
    
# define draw handler
def draw(canvas):
    global counter, n_success, n_stop
    canvas.draw_text(format(counter), [80, 150], 60,"White")
    canvas.draw_text(str(n_success) + "/" + str(n_stop), \
                     [250, 40], 30,"Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start', start_timer, 100)
frame.add_button('Stop', stop_timer, 100)
frame.add_button('Reset', reset_timer, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
