# My Space Invaders :D
# Cleaned up code with consistent structure, enhanced logic, and improved user interactions.

import turtle
import random
import time
import pygame
import json

###############################################################################
# Player Name Handling
###############################################################################
def get_player_name():
    """
    Prompt the user for a valid username.
    Ensures the username is not purely numeric.
    """
    while True:
        try:
            name = input("Enter your username: ").strip()
            if not name:
                raise ValueError("Username cannot be empty.")
            if name.isdigit():
                raise ValueError("Username cannot be only numbers.")
            print("Username accepted.")
            return name
        except ValueError as ve:
            print(f"Invalid username: {ve}")

player_name = get_player_name()

###############################################################################
# Pygame and Sounds Initialization
###############################################################################
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

pew_sound = pygame.mixer.Sound('laser.wav')
pew_sound.set_volume(0.3)
collision_sound = pygame.mixer.Sound('collision.wav')
collision_sound.set_volume(0.55)
game_over_sound = pygame.mixer.Sound('game_over.wav')
game_over_sound.set_volume(0.7)

###############################################################################
# Configurable Game Parameters
###############################################################################
CANNON_SPEED        = 10
LASER_SPEED         = 0.9
DETECTION_RADIUS    = 15
ALIEN_SPEED         = 0.5
ALIEN_SPAWN_INTERVAL= 1.2
ALIEN_FIRE_RATE     = 2.0    # seconds between alien shots
DIFFICULTY_LEVEL    = 0

SCORE               = 0
LIVES               = 3

CANNON_FIRE_RATE    = 0.5    # Player can shoot at intervals of 0.5s
last_cannon_shot_time  = 0
alien_last_shot_time   = 0

###############################################################################
# Game Data Structures
###############################################################################
lasers        = []
alien_lasers  = []
aliens        = []

game_on       = True
start_time    = time.time()

###############################################################################
# Turtle Window Setup
###############################################################################
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgpic("space_background.gif")  # Ensure this file is in your directory
window.title("Space Invaders")
window.tracer(0)

###############################################################################
# Cannon Setup
###############################################################################
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1.5, stretch_len=3)

def create_cannon_top():
    """
    Create the upper part of the cannon sprite.
    """
    cannon_top = turtle.Turtle()
    cannon_top.shape("square")
    cannon_top.color("white")
    cannon_top.penup()
    cannon_top.speed(0)
    cannon_top.setposition(0, -210)
    cannon_top.shapesize(stretch_wid=1, stretch_len=0.75)
    cannon_top.left(90)
    return cannon_top

cannon_top = create_cannon_top()

###############################################################################
# UI Display: Score, Time, Health Bar
###############################################################################
score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.setposition(350, 250)
score_display.color("white")

health_bar = turtle.Turtle()
health_bar.hideturtle()
health_bar.penup()
health_bar.setposition(-350, 260)
health_bar.pendown()
health_bar.width(20)

def update_health_bar():
    """
    Render the health bar based on the player's remaining lives.
    """
    health_bar.clear()
    health_bar.penup()
    health_bar.setposition(-350, 260)
    health_bar.pendown()
    health_bar.color("green")
    # 100 px per life (or choose your preferred scaling)
    health_bar.forward(100 * LIVES)

def update_display():
    """
    Update the top-right text showing elapsed time & score, plus refresh the health bar.
    """
    elapsed_time = time.time() - start_time
    score_display.clear()
    score_display.write(
        f"Time: {elapsed_time:.1f}s\nScore: {SCORE}",
        align="right",
        font=("Courier", 16, "normal")
    )
    update_health_bar()

###############################################################################
# Alien Setup
###############################################################################
window.addshape("alien_texture.gif")  # Provide an actual .gif file in the directory

def alien_spawn_location_randomizer():
    """
    Returns a random X position for an alien to spawn horizontally within -150..150
    """
    return random.randint(-150, 150)

def create_alien():
    """
    Create an alien turtle with the specified shape & initial position,
    then add it to the aliens list.
    """
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("alien_texture.gif")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.right(90)
    alien.setposition(alien_spawn_location_randomizer(), 250)
    aliens.append(alien)
    return alien

def move_aliens():
    """
    Move each alien horizontally. If hitting the screen boundary, reverse direction.
    Also, if an alien goes below a certain Y, game ends.
    """
    global ALIEN_SPEED, game_on
    for alien in aliens:
        alien.setx(alien.xcor() + ALIEN_SPEED)
        # Invert direction and move all aliens down when one hits the boundary
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            for a in aliens:
                a.sety(a.ycor() - 40)
        # If alien goes too low, game over
        if alien.ycor() < -300:
            game_on = False
            game_over_sound.play()

###############################################################################
# Laser Setup
###############################################################################
def create_laser():
    """
    Create a laser from the cannon if enough time has passed since last shot.
    The laser travels upward.
    """
    global last_cannon_shot_time
    now = time.time()
    if now - last_cannon_shot_time >= CANNON_FIRE_RATE:
        laser = turtle.Turtle()
        laser.penup()
        laser.color("red")
        laser.shape("square")
        laser.shapesize(stretch_wid=0.5, stretch_len=2)
        laser.setheading(90)
        laser.setposition(cannon.xcor(), cannon.ycor() + 20)
        lasers.append(laser)
        last_cannon_shot_time = now
        pew_sound.play()
        return laser

def create_alien_laser(alien):
    """
    Create a downward-traveling laser from a chosen alien.
    """
    alien_laser = turtle.Turtle()
    alien_laser.penup()
    alien_laser.color("yellow")
    alien_laser.shape("square")
    alien_laser.shapesize(stretch_wid=0.25, stretch_len=1)
    alien_laser.setheading(270)
    alien_laser.setposition(alien.xcor(), alien.ycor() - 20)
    alien_lasers.append(alien_laser)
    pew_sound.play()

def move_lasers():
    """
    Move player lasers upward; remove them if they go off-screen.
    """
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

def move_alien_lasers():
    """
    Move alien lasers downward; remove them if off-screen.
    If a laser hits the cannon, reduce life.
    """
    global LIVES, game_on
    for alien_laser in alien_lasers[:]:
        alien_laser.forward(LASER_SPEED)
        if alien_laser.ycor() < -300:
            alien_laser.hideturtle()
            alien_lasers.remove(alien_laser)
        elif alien_laser.distance(cannon) < DETECTION_RADIUS:
            alien_laser.hideturtle()
            alien_lasers.remove(alien_laser)
            LIVES -= 1
            update_display()
            if LIVES <= 0:
                game_on = False
                game_over_sound.play()

###############################################################################
# Collisions & Explosions
###############################################################################
window.addshape("explosion.gif")

def check_collision():
    """
    For each player laser, check collision with each alien.
    If collided, remove both from screen and increment score + show explosion.
    """
    global SCORE
    for laser in lasers[:]:
        for alien in aliens[:]:
            if laser.distance(alien) < DETECTION_RADIUS:
                laser.hideturtle()
                alien.hideturtle()
                SCORE += 10
                collision_sound.play()
                # Explosion effect
                explosion = turtle.Turtle()
                explosion.shape("explosion.gif")
                explosion.penup()
                explosion.setposition(alien.xcor(), alien.ycor())
                explosion.showturtle()
                window.update()
                # Hide explosion after a short delay
                window.ontimer(lambda: explosion.hideturtle(), 200)
                lasers.remove(laser)
                aliens.remove(alien)
                break

###############################################################################
# Cannon Movement
###############################################################################
def move_left():
    """
    Move cannon left, ensuring it doesn't go out of the screen.
    """
    new_x = cannon.xcor() - CANNON_SPEED
    if new_x >= - (window.window_width()/2) + 20:
        cannon.setx(new_x)
        cannon_top.setx(new_x)

def move_right():
    """
    Move cannon right, ensuring it doesn't go out of the screen.
    """
    new_x = cannon.xcor() + CANNON_SPEED
    if new_x <= (window.window_width()/2) - 20:
        cannon.setx(new_x)
        cannon_top.setx(new_x)

###############################################################################
# Key Bindings
###############################################################################
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(lambda: None, "Left")
window.onkeyrelease(lambda: None, "Right")
window.onkeypress(create_laser, "space")

###############################################################################
# Difficulty Menu
###############################################################################
def difficulty_menu():
    """
    Display a menu with 3 difficulty buttons: EASY, NORMAL, HARD.
    Each has different speeds & rates for alien/player behaviors.
    """
    global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL, LASER_SPEED
    global DIFFICULTY_LEVEL, CANNON_FIRE_RATE, ALIEN_FIRE_RATE

    logo = turtle.Turtle()
    logo.hideturtle()
    logo.color("yellow")
    logo.penup()
    logo.setposition(0, 200)
    logo.write("SPACE INVADERS", align="center", font=("Courier", 30, "bold"))

    def create_button(x, y, color):
        btn = turtle.Turtle()
        btn.shape("square")
        btn.color(color)
        btn.shapesize(stretch_wid=2.5, stretch_len=5)
        btn.penup()
        btn.setposition(x, y)
        return btn

    button1 = create_button(-150, 0, "green")
    button2 = create_button(0, 0, "orange")
    button3 = create_button(150, 0, "red")

    text = turtle.Turtle()
    text.hideturtle()
    text.color("white")
    text.penup()
    text.setposition(0, -50)
    text.write("EASY      NORMAL      HARD", align="center", font=("Courier", 18, "normal"))

    def set_difficulty(level):
        """
        Apply different parameters for each difficulty level.
        """
        nonlocal DIFFICULTY_LEVEL
        if level == 1:  # Easy
            ALIEN_SPEED         = 0.25
            ALIEN_SPAWN_INTERVAL= 3.0
            LASER_SPEED         = 1.2
            CANNON_FIRE_RATE    = 0.4
            ALIEN_FIRE_RATE     = 2.25
        elif level == 2:  # Normal
            ALIEN_SPEED         = 0.75
            ALIEN_SPAWN_INTERVAL= 1.0
            LASER_SPEED         = 1.0
            CANNON_FIRE_RATE    = 0.5
            ALIEN_FIRE_RATE     = 1.75
        else:  # Hard
            ALIEN_SPEED         = 0.8
            ALIEN_SPAWN_INTERVAL= 1.75
            LASER_SPEED         = 0.6
            CANNON_FIRE_RATE    = 0.4
            ALIEN_FIRE_RATE     = 2.0

        DIFFICULTY_LEVEL = level
        logo.clear()
        text.clear()
        button1.hideturtle()
        button2.hideturtle()
        button3.hideturtle()

    button1.onclick(lambda x, y: set_difficulty(1))
    button2.onclick(lambda x, y: set_difficulty(2))
    button3.onclick(lambda x, y: set_difficulty(3))

    # Wait until difficulty chosen
    while DIFFICULTY_LEVEL == 0:
        window.update()
        time.sleep(0.01)

# Show difficulty menu before starting
difficulty_menu()

###############################################################################
# Main Game Loop
###############################################################################
alien_timer = time.time()

while game_on:
    # Spawn aliens at intervals
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

    # Alien shooting at intervals
    current_time = time.time()
    if current_time - alien_last_shot_time > ALIEN_FIRE_RATE and aliens:
        shooting_alien = random.choice(aliens)
        create_alien_laser(shooting_alien)
        alien_last_shot_time = current_time

    # Move objects and check collisions
    move_aliens()
    move_lasers()
    move_alien_lasers()
    check_collision()

    # Update UI & refresh
    update_display()
    window.update()

###############################################################################
# Game Over Screen
###############################################################################
game_over_display = turtle.Turtle()
game_over_display.color("red")
game_over_display.hideturtle()
game_over_display.write("GAME OVER", align="center", font=("Courier", 40, "bold"))

game_over_display.sety(game_over_display.ycor() - 50)
game_over_display.color("red")
game_over_display.write(f"Score: {SCORE}", align="center", font=("Courier", 30, "bold"))

window.update()

###############################################################################
# Save Score to JSON
###############################################################################
def save_score():
    """
    Save the player's name, final score, and difficulty to a JSON file.
    Creates or overwrites 'highscore.json'.
    """
    data = {
        "player_username": player_name,
        "highscore": SCORE,
        "difficulty_level": DIFFICULTY_LEVEL
    }
    with open("highscore.json", "w") as f:
        json.dump(data, f, indent=2)

save_score()
turtle.done()
