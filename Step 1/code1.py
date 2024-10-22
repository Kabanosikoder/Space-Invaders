# -* - coding : utf -8 -* -
import turtle
# Création de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)  # Taille de la fenêtre
window.bgcolor("black")  # Couleur de fond
window.title("Space␣Invaders")
# Création du canon
cannon = turtle.Turtle()
cannon.shape("circle")
cannon.color("white")
cannon.penup()  # Évite de dessiner des lignes pendant les déplacements
cannon.setposition(0, -250)  # Position en bas de l’écran
# Garder l’écran ouvert
turtle.done()

# 1. turtle.done() sert a garder l'écran ouvert
# 2. la methode penup() evite de dessiner les lignes pendant que le cannon se deplace
# 3. window.bgcolor() permet de changer la couleur de fond
# 4. setposition() permet de changer la positon de l'objet et setheading() permet de changer l'angle
# 5. il faut changer le code a ligne 10: cannon.shape("circle")