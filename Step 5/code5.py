# -*- coding: utf-8 -*-
import turtle
import random
import time
import math

# Paramètres
CANNON_STEP = 10
LASER_SPEED = 4
ALIEN_SPEED = 0.4
ALIEN_SPAWN_INTERVAL = 1.2
DETECTION_RADIUS = 20

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0) # Désactiver la mise à jour automatique de l’écran

# Création du canon (partie intermédiaire)
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("circle")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)

# Création de la partie supérieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("turtle")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)
    part2.left(90)
    return part2

part2 = create_cannon_top()

# Création d’un extraterrestre
def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("square")
    alien.color("green")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.setposition(0, 250)
    return alien

alien = create_alien()

# Déplacer l’extraterrestre
def move_alien():
    alien.setx(alien.xcor() + ALIEN_SPEED)
    if alien.xcor() > 390 or alien.xcor() < -390:
        alien.setx(-alien.xcor())

# Créer un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    return laser

# Créer une fonction pour détecter les collisions
# def check_collision(laser, alien):
    # distance = laser.distance(alien)
   # if distance < DETECTION_RADIUS:
       # laser.hideturtle()
       #alien.hideturtle()
       # lasers.remove(laser)
       # aliens.remove(alien)
       # return True
   # return False

def collision_checker(laser, alien):
    distance = math.sqrt(math.pow(laser.xcor() - alien.xcor(), 2) + math.pow(laser.ycor() - alien.ycor(), 2))
    return distance < DETECTION_RADIUS

# Déplacer les lasers
def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        # Retirer les lasers qui sortent de l’écran
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
        # Vérifier les collisions
        if collision_checker(laser, alien):
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
            alien.clear()
            alien.hideturtle()

# Lier les touches du clavier
def move_left():
    new_x = cannon.xcor() - CANNON_STEP
    if new_x >= - window.window_width() / 2 + 20:  # Garder le canon dans l ’é cran
        cannon.setx(new_x)
        part2.setx(new_x)  # D é placer aussi la partie sup é rieure
# D é placer le canon vers la droite

def move_right():
    new_x = cannon.xcor() + CANNON_STEP
    if new_x <= window . window_width() / 2 - 20:
        cannon.setx(new_x)
        part2.setx(new_x)  # D é placer aussi la partie sup é rieure

def move_alien():
    global ALIEN_SPEED
    alien.setx(alien.xcor() + ALIEN_SPEED)
    # Inverser la direction lorsque l'alien atteint les bords
    if alien.xcor() > 390 or alien.xcor() < -390:
        ALIEN_SPEED = -ALIEN_SPEED


# Créer un laser
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(lambda: lasers.append(create_laser()), "space")

# Boucle de jeu
lasers = []
aliens = []

while True:
    window.update()  # Mettre à jour l’écran
    move_lasers()  # Déplacer les lasers
    turtle.delay(10)  # Ajouter un léger délai pour la fluidité
    move_alien()
# Garder la fenêtre ouverte
turtle.done()

# 1. On utilise la méthode laser.distance(alien) pour calculer la distance de l'alien par rapport au laser
# 2. On peut ajuster la sensibilité en changeant la valeur de COLLISION_RADIUS
# 3. Pour montrer que l'alien c'est fait toucher par le laser
# 4. L'extraterrestre est déplacé en modifiant sa position sur l'axe des x, quand l'alien atteint le bord de l'écran il inverse son mouvement
# 5. 5 Une fois qu'un alien est touché, marquez-le comme détruit.