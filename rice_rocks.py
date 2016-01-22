"""
Mini-project #7 for Introduction to Interactive Programming in Python. Rice Rocks (inspired by the arcade game Asteroids)
Written on: 12/08/2015 
"""
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

class Ship:
   
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def thruster_on(self):
        self.thrust = True
        # set image_center of to thruster-on tiled image
        self.image_center[0] += self.image_size[0]
        # play thruster sound
        ship_thrust_sound.play()
    
    def thruster_off(self):
        self.thrust = False
        # set image_center of to thruster-off tiled image
        self.image_center[0] -= self.image_size[0]
        #rewind thruster sound
        ship_thrust_sound.rewind()
        
    def shoot(self):
        global missile_group
        
        mis_pos = [self.pos[0] + self.image_size[0]/2 * angle_to_vector(self.angle)[0], \
                  self.pos[1] + self.image_size[0]/2 * angle_to_vector(self.angle)[1]]
        mis_vel = [self.vel[0] + 6 * angle_to_vector(self.angle)[0], \
                  self.vel[1] + 6 * angle_to_vector(self.angle)[1]]
        
        new_missile = Sprite(mis_pos, mis_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.append(new_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    
    def update(self):
        if self.thrust:
            # add acceleration
            self.vel[0] += .3 * angle_to_vector(self.angle)[0]
            self.vel[1] += .3 * angle_to_vector(self.angle)[1]
        
        self.vel[0] = 0.98 * self.vel[0]
        self.vel[1] = 0.98 * self.vel[1]
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel       
    
    
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        
        if self.animated:
            image_center = [self.image_center[0] + self.age * self.image_size[0], \
                            self.image_center[1]]
        else:
            image_center = self.image_center
            
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size,self.angle)
        
    
    def update(self):
        # update position, vel, angle
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        # increment age
        self.age += 1
        if self.age < self.lifespan: # keep the object
            return False
        else: # remove the object
            return True
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self,other_object):
        other_object_pos = other_object.get_position()
        other_object_radius = other_object.get_radius()
        
        # determine if there is collision
        if min((self.pos[0]+self.radius)%WIDTH, (other_object_pos[0] + other_object_radius)%WIDTH) > \
        max((self.pos[0]-self.radius)%WIDTH, (other_object_pos[0]-other_object_radius)%WIDTH):
            if min((self.pos[1]+self.radius)%HEIGHT, (other_object_pos[1] + other_object_radius)%HEIGHT) > \
            max((self.pos[1]-self.radius)%HEIGHT, (other_object_pos[1]-other_object_radius)%HEIGHT):
                return True
           
        return False        
           
def draw(canvas):
    global time, score, lives, rock_group, my_ship, started
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship
    my_ship.update()
    
    if group_collide(rock_group,my_ship):
        lives -= 1
        # if lives is 0, splash screen, destroy all rocks, \
        # and set started = False
    
    if lives <= 0:
        started = False
        rock_group = []
            
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())    
        
    score += group_group_collide(missile_group, rock_group)

    # draw score and lives textboxes
    canvas.draw_text("Score: " + str(score), [40, 20], 20,"White")
    canvas.draw_text("Lives: " + str(lives), [40, 40], 20,"White")
    
# timer handler that spawns a rock    
def rock_spawner():
    """ Spawn a rock at a random position """
    global rock_group, timer, started
    
    if started: # if the game is started
        if len(rock_group) < 4:
            #determine random pos, vel, angle_vel
            pos = [random.randint(0,WIDTH), random.randint(0,HEIGHT)]
            vel = [0.35 * random.choice([-1,1]) * random.randint(1,5), \
                    0.35 * random.choice([-1,1]) * random.randint(1,5)]
            angle_vel = 0.05 * random.choice([-1,1]) * random.randint(3,6)
    
            # create a new rock
            new_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
            if not new_rock.collide(my_ship):
                rock_group.append(new_rock)
        
# Call the update and draw methods for a sprite group
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        if sprite.update():
            sprite_group.remove(sprite)
        sprite.draw(canvas)
        
# Check for collisions between a sprite group and an object
def group_collide(sprite_group, other_object):
    global explosion_group
    for sprite in set(sprite_group):
        if sprite.collide(other_object):
            # remove the sprite
            sprite_group.remove(sprite)
            # create a new explosion
            new_explosion = Sprite(sprite.pos, [0,0], 0, 0, explosion_image, explosion_info)
            explosion_group.append(new_explosion)
            # play explosion sound
            explosion_sound.play()
            # return boolean indicating an explosion
            return True
    
    return False

# Check for collisions between two groups
def group_group_collide(group1, group2):
    n = 0
    for sprite1 in set(group1): # rock
        if group_collide(group2, sprite1):
            group1.remove(sprite1)
            n += 1
                  
    return n
    
# handlers for keyup and keydown, mouseclick
def keydown(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_on()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -0.1
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0.1
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_off()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
        
def mouse_handler(position):
    if (0 <= position[0] <= WIDTH) and (0 <= position[1] <= HEIGHT):
        restart_game()

def restart_game():
    global started, my_ship, rock_group, missile_group, explosion_group, \
    score, lives, time, timer
        
    started = True
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group[:] = []
    missile_group[:] = []
    score = 0
    lives = 3
    time = 0
                 
    soundtrack.rewind()
    soundtrack.play()
    
    timer.start()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# globals for the game
started = False
rock_group = []
missile_group = []
explosion_group = []
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
