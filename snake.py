import tkinter as tk
import time 
import random

root = tk.Tk()
root.geometry("500x500")
root.resizable(False, False)
root.title("Snake")

snakeBody = []
snakeBodyPos = []

bonus = []
bonusPos = []

direction = "RIGHT"
dead = False
keyPressed = False

def main(dead):
    '''
        Fonction principale qui exécute tout le programme
        Args :
            dead : Etat de vie ou de mort du serpent
    '''
    initializeGame() #On initialise le jeu
    bindKeys() #On defini les touches pour jouer
    newBonus(1) #On met un bonus sur le jeu
    while dead == False: #Tant qu'on est vivant on joue
        dead = movements(direction)

def initializeGame():
    '''
        Initialisation du jeu :
            - Définition de la taille de la carte
            - Ajout d'un serpent de taille 4
    '''
    #On defini la taille des lignes et colonnes de la fenêtre
    for i in range(50):
        root.rowconfigure(i, weight=10, minsize=10)
        root.columnconfigure(i, weight=10, minsize=10)

    #On crée le serpent de départ avec 4 parties différentes 
    addBodyPartToSnake(4, row=25, column=25)

def movements(direction):
    '''
        Fait bouger le serpent selon la direction selectionnée et
        teste si on passe sur un bonus.
        Args :
            direction : Direction dans laquelle le serpent doit aller 
        
        Return :
            bool : L'état de vie ou de mort du serpent
    '''
    global keyPressed
    
    #On place la queue du serpent en tête ce qui n'actualise que un canva et non tout le serpent
    snakeBody.insert(0, snakeBody[-1])
    snakeBody.pop(-1)
    snakeBodyPos.insert(0, snakeBodyPos[-1])
    snakeBodyPos.pop(-1)

    headInfo = snakeBody[1].grid_info()
    #On dirige la tête selon la direction voulue
    if(direction == "RIGHT"):
        snakeBody[0].grid(row=headInfo["row"], column=headInfo["column"] + 1)
        snakeBodyPos[0] = (headInfo["column"] + 1, headInfo["row"])

    elif(direction == "LEFT"):
        if (headInfo["column"] - 1 == -1):
            return True
        else:
            snakeBody[0].grid(row=headInfo["row"], column=headInfo["column"] - 1)
            snakeBodyPos[0] = (headInfo["column"] - 1, headInfo["row"])

    elif(direction == "UP"):
        if (headInfo["row"] - 1 == -1):
            return True
        else:
            snakeBody[0].grid(row=headInfo["row"] - 1, column=headInfo["column"])
            snakeBodyPos[0] = (headInfo["column"], headInfo["row"] - 1)

    elif(direction == "DOWN"):
        snakeBody[0].grid(row=headInfo["row"] + 1, column=headInfo["column"])
        snakeBodyPos[0] = (headInfo["column"], headInfo["row"] + 1)
    
    #Si on est passé sur un bonus
    if (snakeBodyPos[0] in bonusPos):
        #On supprime le bonus mangé des listes
        indexBonus = bonusPos.index((snakeBodyPos[0]))
        bonus[indexBonus].grid_remove()
        bonus.pop(indexBonus)
        bonusPos.pop(indexBonus)

        #On ajoute 5 bouts au corps du serpents et 2 nouveaux bonus sur dans le jeu
        addBodyPartToSnake(5)
        newBonus(1)

    root.update()
    time.sleep(0.1) #10 FPS
    keyPressed = False
    return death()

def death():
    '''
        Défini l'état du serpent selon s'il est hors des limites ou s'il
        se touche lui même

        Return :
            bool : L'état de vie ou de mort
    '''

    headInfo = snakeBody[0].grid_info()

    if (headInfo["row"] == 50 or headInfo["column"] == 50): #Si on atteint les limites du jeu
        return True
    elif (snakeBodyPos.count((headInfo["column"], headInfo["row"])) > 1): #Si on repasse sur le serpent
        return True
    
    return False

def bindKeys():
    '''
        Associe un appuie sur une touche à la fonction whichKey()
    '''
    root.bind("<Key>", lambda e: whichKey(e.keysym)) #On recupère n'import quelle touche du clavier

def whichKey(key):
    '''
        Change la direction du serpent selon les touches appuyées
        Args :
            key : Touche appuyée
    '''

    global direction
    global keyPressed

    #Si une touche n'a pas encore été préssée, on lui indique la nouvelle direction à suivre
    if keyPressed == False:
        if (key == "Up"):
            if direction != "DOWN":
                direction = "UP"
        elif (key == "Down"):
            if direction != "UP":
                direction = "DOWN"
        elif (key == "Right"):
            if direction != "LEFT":
                direction = "RIGHT"
        elif (key == "Left"):
            if direction != "RIGHT":
                direction = "LEFT"
        keyPressed = True

def newBonus(number):
    '''
        Ajoute une nombre N de bonus sur la carte du jeu
        Args :
            number : Nombre de bonus à ajouter
    '''
    numberOfBonus = len(bonus)
    for i in range(number):
        #On choisi une position aléatoire dans le jeu 
        x = random.randint(0, 49)
        y = random.randint(0, 49)

        #Si on ne le place pas sur le serpent alors on le place dans le jeu
        if ((x, y) not in snakeBodyPos):
            bonus.append(tk.Canvas(root, width=10, height=10, bd=0, highlightthickness=0))
            bonus[i + numberOfBonus - 1].grid(row = y, column = x)
            bonus[i + numberOfBonus - 1].create_rectangle(0, 0, 10, 10, fill="red")
            bonusPos.append((x, y))
        else:
            newBonus(number)
            
def addBodyPartToSnake(number, row=None, column=None):
    '''
        Ajoute un nombre N de partie à la queue du serpent
        Args :
            number : Nombre de partie à rajouter
            row ?: Ligne à laquelle ajouter les parties
            column ?: Colonne à laquelle ajouter les parties
    '''
    lengthSnake = len(snakeBody)

    #On défini l'emplacement où ajouter les parties si non précisée
    if (row == None and column == None):
        lastPartSnake = snakeBody[lengthSnake-1].grid_info()
        row, column = lastPartSnake["row"], lastPartSnake["column"]

    #On rajoute les parties du corps
    for i in range(number):
        snakeBody.append(tk.Canvas(root, width=10, height=10, bd=0, highlightthickness=0))
        snakeBody[lengthSnake + i].grid(row=row, column=column)
        snakeBody[lengthSnake + i].create_rectangle(0, 0, 10, 10, fill="green")
        snakeBodyPos.append((column-i, row))

main(dead)
root.mainloop()
