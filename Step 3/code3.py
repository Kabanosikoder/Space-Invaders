import turtle
# Param è tres
CANNON_STEP = 10
LASER_SPEED = 15
# Configuration de la fen ê tre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space␣Invaders")
window.tracer(0)  # D é sactiver la mise à jour automatique de l ’é cran
# Cr é ation du canon ( partie interm é diaire )
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)  # Taille moyenne
# Cr é ation de la partie sup é rieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)  # Petite partie sup é rieure
    return part2
part2 = create_cannon_top()

# D é placer le canon vers la gauche
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
# Cr é er un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    return laser
# Déplacer le laser vers le haut

def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
    # Retirer les lasers qui sortent de l’écran

# Lier les touches du clavier
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(lambda: lasers.append(create_laser()), "space")

# Boucle de jeu
lasers = []

while True:
    window.update()  # Mettre àjour l’écran
    move_lasers()  # Déplacer les lasers
    turtle.delay(10)  # Ajouter un léger délai pour la fluidité

# Garder la fenêtre ouvertes
turtle.done()

# 1. append() enléve le laser qui est créer
# 2. penup() arrete de dessiner quand le laser bouge
# 3. create_laser() créer un laser et move_lasers() bouge les lasers
# 4. si on enléve 'if laser.ycor() > window.window_height() / 2' les lasers ne sont pas supprimés
# 5. on peut changer la valeur de LASER_SPEED à la ligne 4
