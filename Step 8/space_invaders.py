# My Space Invaders :D
# cleaning up this code took a long time -_-
import turtle
import random
import time
import pygame
import json

# Asking for player name for highscore saving
try:
    player_name = input("Enter your username: ")

    # Attempt to convert to int to check if it's a pure number
    if player_name.isdigit():
        raise ValueError("Username cannot be only numbers.")

    print("Username accepted.")

except ValueError as e:
    print(f"Invalid input: {e}")

# Initializers for pygame and sounds
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

# Charger les sons
pew_sound = pygame.mixer.Sound('laser.wav')
pew_sound.set_volume(0.3)
collision_sound = pygame.mixer.Sound('collision.wav')
collision_sound.set_volume(0.55)
game_over_sound = pygame.mixer.Sound('game_over.wav')

# Paramètres modifiable
CANNON_SPEED = 10
LASER_SPEED = 0.9
DETECTION_RADIUS = 15

ALIEN_SPEED = 0.5
ALIEN_SPAWN_INTERVAL = 1.2
ALIEN_FIRE_RATE = 2  # Alien fire rate in seconds

DIFFICULTY_LEVEL = 0
SCORE = 0
LIVES = 3
CANNON_FIRE_RATE = 0.5  # Player fire rate in seconds
last_cannon_shot_time = 0
alien_last_shot_time = 0

# Game logic handling
lasers = []
alien_lasers = []
aliens = []
game_on = True  # Variable booléenne pour signaler la fin du jeu
start_time = time.time()

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgpic("space_background.gif")
window.title("Space Invaders")
window.tracer(0) #

# Création de la partie inférieure du cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1.5, stretch_len=3)

# Création de la partie supérieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=0.75)
    part2.left(90)
    return part2
part2 = create_cannon_top()

# Affichage du temps et du score
score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.setposition(350, 250)
score_display.color("white")

# Health bar
health_bar = turtle.Turtle()
health_bar.hideturtle()
health_bar.penup()
health_bar.setposition(-350, 260)
health_bar.pendown()
health_bar.width(20)

# it's in the name lol
def update_health_bar():
    health_bar.clear()
    health_bar.penup()
    health_bar.setposition(-350, 260)
    health_bar.pendown()
    health_bar.color("green")
    health_bar.forward(100 * LIVES)

# Mettre à jour le score, le temps et les vies
def update_display():
    elapsed_time = time.time() - start_time
    score_display.clear()
    score_display.write(f"Temps : {elapsed_time:.1f}s\nScore : {SCORE}",
                        align="right", font=("Courier", 16, "normal"))
    update_health_bar()

# it's also in the name
def alien_spawn_location_randomizer():
         return random.randint(-150, 150)

window.addshape("alien_texture.gif") # registering the image as a shape
# !!REMINDER: to register all textures as shapes before assigning the shape, took me way too long to figure this out

# Création d’un extraterrestre
def create_alien():
    global alien
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("alien_texture.gif")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.right(90)
    alien.setposition(alien_spawn_location_randomizer(), 250)
    aliens.append(alien)
    return alien

# Déplacer l’extraterrestre
def move_aliens():
    global ALIEN_SPEED
    for alien in aliens:
        alien.setx(alien.xcor() + ALIEN_SPEED)
        # Inverts direction when aliens touch the borders of the screen
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            # Makes the aliens go down by 40 pixels
            for a in aliens:
                a.sety(a.ycor() - 40)
        # Checks if the alien reaches the bottom of the screen
        if alien.ycor() < -300:
            global game_on
            game_on = False
            game_over_sound.play()

# Créer un laser (player lasers)
def create_laser():
    global last_cannon_shot_time
    current_time = time.time()
    if current_time - last_cannon_shot_time >= CANNON_FIRE_RATE:
        laser = turtle.Turtle()
        laser.penup()
        laser.color("red")
        laser.shape("square")
        laser.shapesize(stretch_wid=0.5, stretch_len=2)
        laser.setheading(90)
        laser.setposition(cannon.xcor(), cannon.ycor() + 20)
        lasers.append(laser)  # Ajouter le laser à la liste des lasers
        last_cannon_shot_time = current_time
        pew_sound.play()
        return laser

# Creates an alien, laser, code was stolen from above with some tweaks
def create_alien_laser(alien):
    alien_laser = turtle.Turtle()
    alien_laser.penup()
    alien_laser.color("yellow")
    alien_laser.shape("square")
    alien_laser.shapesize(stretch_wid=0.25, stretch_len=1)
    alien_laser.setheading(270)
    alien_laser.setposition(alien.xcor(), alien.ycor() - 20)
    alien_lasers.append(alien_laser)
    pew_sound.play()

# Déplacer les lasers
def move_lasers():
    # move player lasers
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        # Retirer les lasers qui sortent de l’écran
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

def move_alien_lasers():
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

# Checks if a laser(player laser) and an alien touch, if so then both are removed and explosion is played
window.addshape("explosion.gif")

def check_collision():
    global SCORE
    for laser in lasers[:]:
        for alien in aliens[:]:
            distance = laser.distance(alien)
            if distance < DETECTION_RADIUS:
                laser.hideturtle()
                alien.hideturtle()
                SCORE += 10
                collision_sound.play()
                explosion = turtle.Turtle()
                explosion.shape("explosion.gif")
                explosion.penup()
                explosion.setposition(alien.xcor(), alien.ycor())
                explosion.showturtle()
                window.update()
                window.ontimer(lambda: explosion.hideturtle(), 200)  # Use a lambda instead of sleep to avoid freezing the game
                lasers.remove(laser)
                aliens.remove(alien)
                break

# Déplacer le canon vers la gauche
def move_left():
    new_x = cannon.xcor() - CANNON_SPEED
    if new_x >= - window.window_width() / 2 + 20:  # Garder le canon dans l’écran
        cannon.setx(new_x)
        part2.setx(new_x)  # Déplacer aussi la partie supérieure

# Déplacer le canon vers la droite
def move_right():
    new_x = cannon.xcor() + CANNON_SPEED
    if new_x <= window.window_width() / 2 - 20:
        cannon.setx(new_x)
        part2.setx(new_x)  # Déplacer aussi la partie supérieure

# Player inputs
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(lambda: None, "Left")
window.onkeyrelease(lambda: None, "Right")
window.onkeypress(create_laser, "space")

# SO MANY GLOBALS
def difficulty_menu():
    global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL, LASER_SPEED, DIFFICULTY_LEVEL, CANNON_FIRE_RATE, ALIEN_FIRE_RATE

    # Affichage du logo "Space Invaders"
    logo = turtle.Turtle()
    logo.hideturtle()
    logo.color("yellow")
    logo.penup()
    logo.setposition(0, 200)
    logo.write("SPACE INVADERS", align="center", font=("Courier", 30, "bold"))

    # Buttons for difficulty selection, quite shrimple really
    button1 = turtle.Turtle()
    button1.shape("square")
    button1.color("green")
    button1.shapesize(stretch_wid=2.5, stretch_len=5)
    button1.penup()
    button1.setposition(-150, 0)

    button2 = turtle.Turtle()
    button2.shape("square")
    button2.color("orange")
    button2.shapesize(stretch_wid=2.5, stretch_len=5)
    button2.penup()
    button2.setposition(0, 0)

    button3 = turtle.Turtle()
    button3.shape("square")
    button3.color("red")
    button3.shapesize(stretch_wid=2.5, stretch_len=5)
    button3.penup()
    button3.setposition(150, 0)

    text = turtle.Turtle()
    text.hideturtle()
    text.color("white")
    text.penup()
    text.setposition(0, -50)
    text.write("EASY      NORMAL      HARD", align="center", font=("Courier", 18, "normal")) # this spacing saves me so many line of code

# function nesting, rarely used this
    def set_difficulty(level):
        global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL, LASER_SPEED, DIFFICULTY_LEVEL, CANNON_FIRE_RATE, ALIEN_FIRE_RATE
        if level == 1:
            ALIEN_SPEED = 0.25
            ALIEN_SPAWN_INTERVAL = 3
            LASER_SPEED = 1.2
            CANNON_FIRE_RATE = 0.4
            ALIEN_FIRE_RATE = 2.25
        elif level == 2:
            ALIEN_SPEED = 0.75
            ALIEN_SPAWN_INTERVAL = 1
            LASER_SPEED = 1
            CANNON_FIRE_RATE = 0.5
            ALIEN_FIRE_RATE = 1.75
        elif level == 3:
            ALIEN_SPEED = 0.8
            ALIEN_SPAWN_INTERVAL = 1.75
            LASER_SPEED = 0.6
            CANNON_FIRE_RATE = 0.4
            ALIEN_FIRE_RATE = 2
        DIFFICULTY_LEVEL = level
        logo.clear()
        text.clear()
        button1.hideturtle()
        button2.hideturtle()
        button3.hideturtle()

    button1.onclick(lambda x, y: set_difficulty(1)) # I love lambdas
    button2.onclick(lambda x, y: set_difficulty(2))
    button3.onclick(lambda x, y: set_difficulty(3))

    while DIFFICULTY_LEVEL == 0:
        window.update()
        time.sleep(0.01)

difficulty_menu()

# Boucle du jeu
alien_timer = time.time()
while game_on == True:
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

    # Alien shooting logic
    current_time = time.time()
    if current_time - alien_last_shot_time > ALIEN_FIRE_RATE:
        if aliens:
            shooting_alien = random.choice(aliens)
            create_alien_laser(shooting_alien)
            alien_last_shot_time = current_time

    # Calling everything else
    move_alien_lasers()
    move_aliens()
    move_lasers()
    check_collision()
    update_display()
    window.update()

# Afficher "Game Over"
game_over = turtle.Turtle()
game_over.color("red")
game_over.hideturtle()
game_over.write("GAME OVER", align="center", font=("Courier", 40, "bold"))

# Afficher le score final
game_over.sety(game_over.ycor() - 50)
game_over.color("red")
game_over.hideturtle()
game_over.write(f"Score: {SCORE}", align="center", font=("Courier", 30, "bold"))

window.update()

# Saves score in a .json file
def save_score():
    with open("highscore.json", "w") as f:
        json.dump({"player_username": player_name}, f)
        json.dump({"highscore": SCORE}, f)
        json.dump({"difficulty_level": DIFFICULTY_LEVEL}, f)
save_score()

turtle.done()
