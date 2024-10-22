# -*- coding: utf-8 -*-
import turtle
import random
import time

# Paramètres modifiable
CANNON_STEP = 10
LASER_SPEED = 0.9
ALIEN_SPEED = 0.8
ALIEN_SPAWN_INTERVAL = 1.2
DETECTION_RADIUS = 20
SCORE = 0

# Listes pour lasers et aliens
lasers = []
aliens = []
game_on = True  # Variable booléenne pour signaler la fin du jeu
start_time = time.time()

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
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
    part2.shapesize(stretch_wid=1, stretch_len=2.2)
    part2.left(90)
    return part2
part2 = create_cannon_top()

# Affichage du temps et du score
score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.setposition(350, 250)
score_display.color("white")

# Mettre à jour le score et le temps
def update_display():
    elapsed_time = time.time() - start_time
    score_display.clear()
    score_display.write(f"Temps : {elapsed_time:.1f}s\nScore : {SCORE}",
                        align="right", font=("Courier", 14, "normal"))

# Création d’un extraterrestre
def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("turtle")
    alien.color("green")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.right(90)
    alien.setposition(0, 250)
    aliens.append(alien)  # Ajouter l'alien à la liste des aliens
    return alien

# Déplacer l’extraterrestre
def move_aliens():
    global ALIEN_SPEED
    for alien in aliens:
        alien.setx(alien.xcor() + ALIEN_SPEED)
        # Inverser la direction lorsque l'alien atteint les bords
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            # Faire descendre les aliens
            for a in aliens:
                a.sety(a.ycor() - 40)  # Descendre de 40 pixels
        # Vérifier si l'alien touche le bas de l'écran
        if alien.ycor() < -300:
            global game_on
            game_on = False

# Créer un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    lasers.append(laser)  # Ajouter le laser à la liste des lasers
    return laser

# Déplacer les lasers
def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        # Retirer les lasers qui sortent de l’écran
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

def check_collision():
    global SCORE
    for laser in lasers[:]:
        for alien in aliens[:]:
            distance = laser.distance(alien)
            if distance < DETECTION_RADIUS:
                laser.hideturtle()
                alien.hideturtle()
                SCORE += 10
                lasers.remove(laser)
                aliens.remove(alien)
                break

# Déplacer le canon vers la gauche
def move_left():
    new_x = cannon.xcor() - CANNON_STEP
    if new_x >= - window.window_width() / 2 + 20:  # Garder le canon dans l’écran
        cannon.setx(new_x)
        part2.setx(new_x)  # D é placer aussi la partie supérieure

# Déplacer le canon vers la droite
def move_right():
    new_x = cannon.xcor() + CANNON_STEP
    if new_x <= window . window_width() / 2 - 20:
        cannon.setx(new_x)
        part2.setx(new_x)  # Déplacer aussi la partie supérieure

# Player inputs
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(lambda: lasers.append(create_laser()), "space")

# Boucle du jeu
alien_timer = time.time()
while game_on == True:
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

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
game_over.color("white")
game_over.write(f"Score: {SCORE}", align="center", font=("Courier", 30, "bold"))

window.update()

turtle.done()

# 1. time.time creer le chronometre
# 2. Le score est mis a jour en increment de 10 dans la fonction check_collision apres une collision entre laser et alien
# 3. update_display sert a afficher le score et le temps
# 4. les nombres se superposent donc les nombres sont illisibles
# 5. On pourrait afficher le score final joueur en dessous de "GAME OVER"