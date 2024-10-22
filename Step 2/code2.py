# -* - coding : utf -8 -* -
import turtle
# Création de la fenêtre
window = turtle.Screen()
window.setup(width =800 , height =600)
window.bgcolor("black")
window.title ("Space␣Invaders")
# Création du canon principal
cannon = turtle.Turtle()
cannon.shape("square")
cannon.color("white")
cannon.penup()
cannon.speed(0)  # D é placement instantan é
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)  # Intermédiaire ( taille moyenne )
# Création de la partie supérieure du canon

def create_cannon_top () :
    part2 = turtle.Turtle ()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)  # Petite partie supérieure
    return part2

# Création de la partie sup é rieure du canon

part2 = create_cannon_top()

# Déplacer le canon et la partie supérieure ensemble

def move_left():
    x = cannon.xcor()  # Position actuelle du canon
    x -= 40  # Déplacer de 20 pixels vers la gauche
    if x < -390:  # Limite de l’écran à gauche
        x = -390
    cannon.setx(x)
    part2.setx(x)  # Déplacer la partie supérieure
def move_right():
    x = cannon . xcor()  # Position actuelle du canon
    x += 40  # Déplacer de 20 pixels vers la droite
    if x > 390:  # Limite de l ’é cran à droite
        x = 390
    cannon.setx(x)
    part2.setx(x)  # D é placer la partie sup é rieure

# Associer les mouvements aux touches du clavier
window.listen()  # Attente des événements du clavier
window.onkeypress(move_left, "Left")  # Appel de la fonction move_left quand on appuie sur "Left"
window.onkeypress(move_right, "Right")  # Appel de la fonctionbmove_right quand on appuie sur "Right"

# Garder l’écran ouvert
turtle.done()

# 1. xcor() donne la position actuelle de l'objet
# 2. on utilise if parce qu'on veut que le cannon bouge seulement quand on appui sur 'left' ou 'right'
# 3. le cannon ne bouge pas si on supprime window.listen()
# 4. onkeypress() actionne un evenement quand on appui et onkey() actionne un evenement quand on relache
# 5. on peut changer la vitesse du deplacement par changer x-= 20 et x += 20 à une valeur plus élevée dans les fonctions move left et move right
