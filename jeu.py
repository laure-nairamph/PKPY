import os
import pygame
import re
import math

# Initialisation Pygame
pygame.init()

# CONSTANTES DE TRAVAIL
TAILLE_TUILE = 32
LARGEUR_NIVEAU = 10
HAUTEUR_NIVEAU = 10
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 800
# 25 cases de chaque côté de l'écran

def charger_niveau(numero_niveau):
    
    chemin_niveau = "./ressources/niveaux/" + str(numero_niveau) +".txt"

    try:
        with open(chemin_niveau, 'r') as f:
            infos_niveau = {}
            infos_niveau['numero'] = int(f.readline())
            infos_niveau['nom'] = f.readline().strip()
            infos_niveau['tileset'] = f.readline().strip()
            infos_niveau['hauteur'], infos_niveau['largeur'] = f.readline().strip().split('*')
            infos_niveau['hauteur'] = int(infos_niveau['hauteur'])
            infos_niveau['largeur'] = int(infos_niveau['largeur'])
            infos_niveau['encodage'] = f.readline().strip()
            infos_niveau['cases'] = [[0 for _ in range(infos_niveau['largeur'])] for _ in range(infos_niveau['hauteur'])]
            infos_niveau['cases_teleportation'] = {}
            infos_niveau['encodage_teleportation'] = f.readline().strip().split('#')

    except FileNotFoundError:
        print("Fichier niveau ", chemin_niveau, " non trouvé")
    except Exception as e:
        print("Erreur :", str(e))


    #On initialise le tableau des cases, puis on charge les valeurs correspondantes   
    niveau = [[0 for _ in range(infos_niveau['hauteur'])] for _ in range(infos_niveau['largeur'])]
    
    #Enregistrement des cases du niveau
    for i in range(infos_niveau['hauteur']):
        for j in range(infos_niveau['largeur']):
            infos_niveau['cases'][i][j] = infos_niveau['encodage'].split(';')[i*infos_niveau['largeur']+j]

    #Enregistrement des téléporteurs du niveau
    for element in infos_niveau['encodage_teleportation']:
        if element:
            tp_x, tp_y, tp_direction_necessaire, tp_niveau_destination, tp_x_destination, tp_y_destination, tp_orientation_destination = element.split(';')
            
            tp_x = int(tp_x)
            tp_y = int(tp_y)
          
            infos_niveau['cases_teleportation'][(tp_x,tp_y)] = {
            'est_teleporteur' : "oui",
            'direction_necessaire': str(tp_direction_necessaire),
            'niveau_destination': int(tp_niveau_destination),
            'ligne_destination': int(tp_x_destination),
            'colonne_destination': int(tp_y_destination),
            'orientation_destination': tp_orientation_destination
            }

    return infos_niveau

def charger_joueur(base_position, base_orientation):

    joueur = {}
    joueur['position'] = base_position 
    joueur['orientation'] = base_orientation
    joueur['ancienne_orientation'] = "bas"
    joueur['animation'] = 0
    joueur['teleportation'] = 0
    joueur['en_mouvement'] = "non"

    joueur['bas'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/bas.png"))
    joueur['bas'] = pygame.transform.scale(joueur['bas'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['bas1'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/bas1.png"))
    joueur['bas1'] = pygame.transform.scale(joueur['bas1'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['bas2'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/bas2.png"))
    joueur['bas2'] = pygame.transform.scale(joueur['bas2'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['droite1'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/droite1.png"))
    joueur['droite1'] = pygame.transform.scale(joueur['droite1'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['droite2'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/droite2.png"))
    joueur['droite2'] = pygame.transform.scale(joueur['droite2'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))
    joueur['gauche1'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/gauche1.png"))
    joueur['gauche1'] = pygame.transform.scale(joueur['gauche1'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))
    joueur['gauche2'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/gauche2.png"))
    joueur['gauche2'] = pygame.transform.scale(joueur['gauche2'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))
    joueur['haut'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/haut.png"))
    joueur['haut'] = pygame.transform.scale(joueur['haut'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['haut1'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/haut1.png"))
    joueur['haut1'] = pygame.transform.scale(joueur['haut1'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))    
    joueur['haut2'] = pygame.image.load(os.path.join("./ressources/sfx/joueur/haut2.png"))
    joueur['haut2'] = pygame.transform.scale(joueur['haut2'], (TAILLE_TUILE *2, TAILLE_TUILE * 2))        

    if joueur['orientation'] == "gauche": 
        joueur['apparence'] = joueur['gauche1']
    elif joueur['orientation'] == "droite": 
        joueur['apparence'] = joueur['droite1']
    elif joueur['orientation'] == "haut": 
        joueur['apparence'] = joueur['haut']
    elif joueur['orientation'] == "bas": 
        joueur['apparence'] = joueur['bas']




    return joueur

def charger_tileset(niveau):
    
    tuiles = []
    chemin_tileset = ("./ressources/sfx/tilesets/" + str(niveau['tileset']))

    # On liste tous les fichiers et on les trie par ordre numérique
    filenames = [f for f in os.listdir(chemin_tileset) if f.endswith(".png")]
    filenames.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    # On charge les fichiers un par un
    for filename in filenames:
        tuile = pygame.image.load(os.path.join(chemin_tileset, filename))
        tuile = pygame.transform.scale(tuile, (TAILLE_TUILE,TAILLE_TUILE))
        tuiles.append(tuile)

    return tuiles

def charger_terrain(niveau, tuiles):

    chemin_terrain = ("./ressources/sfx/tilesets/" + str(niveau['tileset'] + "/terrain.txt"))
    encodage_terrain = ""
    niveau['terrain'] = [0 for _ in range(len(tuiles))]

    try:
        with open(chemin_terrain, 'r') as f:
            encodage_terrain = f.readline().strip()
            terrain_decode = encodage_terrain.split(';')

            for i in range(len(tuiles)):
                niveau['terrain'][i] = terrain_decode[i]
                
        
    except FileNotFoundError:
        print("Fichier niveau ", chemin_terrain, " non trouvé")
    except Exception as e:
        print("Erreur :", str(e))

    return(niveau, tuiles)

def affichage_ecran(ecran, niveau, tuiles, joueur, affichage_bonus):
    # I c'est la ligne, et J c'est la colonne
    
    case_grise = pygame.Surface((32,32))
    gris = (50,50,50)
    case_grise.fill(gris)
    ajustement_i = 0
    ajustement_j = 0


    ecran.fill(gris)

    #Le joueur est toujours au milieu de l'écran (case 12;12)
    #On vérifie si les 12 cases au dessus de lui, à sa gauche, en dessous de lui et à sa droite existent
    #Si oui on les affiche, si non on affiche du gris
    for i in range(25): 

        if i < 12:
            ajustement_i = joueur['position'][1] - (12-i)
        elif i == 12:
            ajustement_i = joueur['position'][1]
        elif i > 12:
            ajustement_i = joueur['position'][1] + (i-12)

        for j in range(25): #On affiche les colonnes

            if j < 12:
                ajustement_j = joueur['position'][0] - (12-j)
            elif j == 12:
                ajustement_j = joueur['position'][0]
            elif j > 12:
                ajustement_j = joueur['position'][0] + (j-12)
            
            if ajustement_i >= 0 and ajustement_i < niveau['hauteur']:
                if ajustement_j >= 0 and ajustement_j < niveau['largeur']:
                    case_a_afficher = niveau['cases'][ajustement_i][ajustement_j]
                    ecran.blit(tuiles[int(case_a_afficher)],(j * TAILLE_TUILE, i * TAILLE_TUILE))

                    if affichage_bonus != "RIEN":
                        affichage_ecran_debug(ecran, niveau, affichage_bonus, ajustement_i,ajustement_j, i, j)
            else:
                ecran.blit(case_grise,(j * TAILLE_TUILE, i * TAILLE_TUILE))



    #On affiche le joueur
    ecran.blit(joueur['apparence'], (12*TAILLE_TUILE, 12*TAILLE_TUILE))

    #On met à jour l'écran
    pygame.display.flip()

def affichage_ecran_debug(ecran, niveau, affichage_bonus,ajustement_i, ajustement_j, i,j):

    case_rouge = pygame.Surface((TAILLE_TUILE,TAILLE_TUILE), pygame.SRCALPHA)
    case_verte = pygame.Surface((TAILLE_TUILE,TAILLE_TUILE), pygame.SRCALPHA)
    case_bleue = pygame.Surface((TAILLE_TUILE,TAILLE_TUILE), pygame.SRCALPHA)
    police = pygame.font.SysFont("Arial", 10)
    vert = (0,255,0, 128)
    rouge = (255,0,0, 128)
    bleu = (0,0,255,128)
    noir = (0,0,0)

    case_verte.fill(vert)
    case_rouge.fill(rouge)
    case_bleue.fill(bleu)

    case_a_afficher = niveau['cases'][ajustement_i][ajustement_j]

    if affichage_bonus == "TERRAIN":
        if niveau['terrain'][int(case_a_afficher)] == "S":
            ecran.blit(case_verte,(j * TAILLE_TUILE, i * TAILLE_TUILE))
            surface_texte = police.render(case_a_afficher, True, noir)
            ecran.blit(surface_texte,(j * TAILLE_TUILE, i * TAILLE_TUILE))
        elif niveau['terrain'][int(case_a_afficher)] == "M":
            ecran.blit(case_rouge, (j * TAILLE_TUILE, i * TAILLE_TUILE))
            surface_texte = police.render(case_a_afficher, True, noir)
            ecran.blit(surface_texte,(j * TAILLE_TUILE, i * TAILLE_TUILE))
        elif niveau['terrain'][int(case_a_afficher)] == "E":
            ecran.blit(case_bleue, (j * TAILLE_TUILE, i * TAILLE_TUILE))
            surface_texte = police.render(case_a_afficher, True, noir)
            ecran.blit(surface_texte,(j * TAILLE_TUILE, i * TAILLE_TUILE))

    if affichage_bonus =="CASES":
        texte_cases = f"i{ajustement_i}-j{ajustement_j}"
        surface_texte = police.render(texte_cases, True, noir)
        ecran.blit(surface_texte,(j * TAILLE_TUILE, i * TAILLE_TUILE))

    if affichage_bonus =="TP":
        if (ajustement_i, ajustement_j) in niveau['cases_teleportation']:
            ecran.blit(case_bleue, (j * TAILLE_TUILE, i * TAILLE_TUILE))

def deplacement_joueur(niveau, tuiles, joueur, direction):
      
    #La position du joueur correspond à quatre cases du terrain
    #Position[0] c'est gauche / droite - Position[1] c'est haut / bas
    #La tête du joueur est sur la ligne Position[1]
    #Les pieds du joueur sont sur la ligne Position[1]+1
    #Le pied gauche du joueur est sur la colonne Position[0]
    #Le pied droit du joueur est sur la colonne Position[0]+1

    #Direction par direction, on vérifie si le joueur ne sort pas du terrain ou ne rencontre pas un mur.
    #Si ce n'est pas le cas, on avance

    declenchement_teleportation = 0

    niveau, tuiles, joueur, declenchement_teleportation = verifier_teleportation(niveau, tuiles, joueur, direction, declenchement_teleportation)
    if declenchement_teleportation == 1:
        return niveau, tuiles, joueur 
    
    match direction:   
        case "haut":
            if joueur['position'][1] > 0:
                if niveau['terrain'][int(niveau['cases'][joueur['position'][1]][joueur['position'][0]])] != "M" and niveau['terrain'][int(niveau['cases'][joueur['position'][1]][joueur['position'][0]+1])] != "M" :
                    joueur['position'][1] -= 1
                else:
                    print("on rencontre un mur")
            
        case "bas":
            if joueur['position'][1] < niveau['hauteur'] - 2:
                if niveau['terrain'][int(niveau['cases'][joueur['position'][1]+2][joueur['position'][0]])] != "M" and niveau['terrain'][int(niveau['cases'][joueur['position'][1]+2][joueur['position'][0]+1])] != "M" :
                    joueur['position'][1] += 1
                else:
                    print("on rencontre un mur")
                
        case "gauche":
            if joueur['position'][0] > 0:
                if niveau['terrain'][int(niveau['cases'][joueur['position'][1]+1][joueur['position'][0]-1])] != "M":
                    joueur['position'][0] -= 1
                else:
                    print("on rencontre un mur")

        case "droite":
            if joueur['position'][0] < niveau['largeur'] - 2 :
                if niveau['terrain'][int(niveau['cases'][joueur['position'][1]+1][joueur['position'][0]+2])] != "M":
                    joueur['position'][0] += 1
                else:
                    print("on rencontre un mur")

    joueur['en_mouvement'] = "oui"

    return niveau, tuiles, joueur

def verifier_teleportation(niveau, tuiles, joueur, direction, declenchement_teleportation):
   
    #On ajuste la position du joueur : +1 s'il marchait vers le bas ou la droite
    ajustement_joueur_x = joueur['position'][0]
    ajustement_joueur_y = joueur['position'][1]

    match direction:
            case "bas":
                ajustement_joueur_y += 1
            case "droite":
                ajustement_joueur_x += 1
    
    #On vérifie la présence d'un téléporteur sur la case de destination
    #Si oui on vérifie si le joueur est tourné dans le bon sens, et on téléporte le cas échéant
    if (ajustement_joueur_y, ajustement_joueur_x) in niveau['cases_teleportation']:
        if joueur['orientation'] == niveau['cases_teleportation'][(ajustement_joueur_y, ajustement_joueur_x)]['direction_necessaire']:
    
            position_x_arrivee = niveau['cases_teleportation'][(ajustement_joueur_y, ajustement_joueur_x)]['ligne_destination']
            position_y_arrivee = niveau['cases_teleportation'][(ajustement_joueur_y, ajustement_joueur_x)]['colonne_destination']
            base_orientation = niveau['cases_teleportation'][(ajustement_joueur_y, ajustement_joueur_x)]['orientation_destination']
            niveau_destination = niveau['cases_teleportation'][(ajustement_joueur_y, ajustement_joueur_x)]['niveau_destination']
            
            niveau = charger_niveau(niveau_destination)
            tuiles = charger_tileset(niveau)
            charger_terrain(niveau, tuiles)
            joueur = charger_joueur([position_x_arrivee,position_y_arrivee], base_orientation)
            declenchement_teleportation = 1
    
    return niveau, tuiles, joueur, declenchement_teleportation

def mise_a_jour_apparence_joueur(joueur):

    #Si le joueur est en mouvement, on détermine son apparence selon son orientation et l'étape de son mouvement (quel pied bouge)
    if joueur['en_mouvement'] == "oui":
        
        if joueur['ancienne_orientation'] == joueur['orientation'] and joueur['animation'] == 0:
            joueur['animation'] = 1
        else:
            joueur['animation'] = 0


        match joueur['orientation']:
            case "haut":    
                    if joueur['animation'] == 0:
                        joueur['apparence'] = joueur['haut1']
                    else : 
                        joueur['apparence'] = joueur['haut2']
                        
            case "bas": 
                    if joueur['animation'] == 0:
                        joueur['apparence'] = joueur['bas1']
                    else : 
                        joueur['apparence'] = joueur['bas2']
                        
            case "gauche": 
                    if joueur['animation'] == 0:
                        joueur['apparence'] = joueur['gauche1']
                    else:
                        joueur['apparence'] = joueur['gauche2']

            case "droite":
                    if joueur['animation'] == 0:
                        joueur['apparence'] = joueur['droite1']
                    else:
                        joueur['apparence'] = joueur['droite2']

                        
    #S'il n'est pas en mouvement , on l'affiche en position de repos selon son orientation
    else:
        match joueur['orientation']:
            case "haut": #Si on va vers le haut
                joueur['apparence'] = joueur['haut']
                joueur['animation'] = 1
                        
            case "bas": 
                joueur['apparence'] = joueur['bas']
                joueur['animation'] = 1
                        
            case "gauche": 
                joueur['apparence'] = joueur['gauche1']
                joueur['animation'] = 1

            case "droite":
                joueur['apparence'] = joueur['droite1']
                joueur['animation'] = 1

    joueur['ancienne_orientation'] = joueur['orientation']
                        





def main():

    pygame.init()
    
    joueur = charger_joueur([4,4],"bas")
    niveau = charger_niveau(3)
    tuiles = charger_tileset(niveau)
    charger_terrain(niveau, tuiles)
    clock = pygame.time.Clock()

    affichage_bonus = "RIEN"

    pygame.display.set_caption('PKPY')
    pygame.display.set_icon(joueur['bas'])

    # On crée l'écran de jeu
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    
     
    # Boucle principale
    boucle_principale = True
    while boucle_principale:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boucle_principale = False


        # On récupère les évènements clavier
        touche_pressee = pygame.key.get_pressed()

        # On vérifie si il y a eu pression sur des touches
        if touche_pressee[pygame.K_UP]:
            joueur['orientation'] = "haut"
            niveau, tuiles, joueur = deplacement_joueur(niveau, tuiles, joueur, joueur['orientation'])
        
        elif touche_pressee[pygame.K_DOWN]:
            joueur['orientation'] = "bas"
            niveau, tuiles, joueur = deplacement_joueur(niveau, tuiles, joueur, joueur['orientation'])

        elif touche_pressee[pygame.K_LEFT]:
            joueur['orientation'] = "gauche"
            niveau, tuiles, joueur = deplacement_joueur(niveau, tuiles, joueur, joueur['orientation'])
            
        elif touche_pressee[pygame.K_RIGHT]:
            joueur['orientation'] = "droite"
            niveau, tuiles, joueur = deplacement_joueur(niveau, tuiles, joueur, joueur['orientation'])

        #CES BLOCS LA C'EST DU BONUS POUR LE DEBUT
        elif touche_pressee[pygame.K_m]:
            if affichage_bonus != "TERRAIN":
                affichage_bonus = "TERRAIN"
            else:
                affichage_bonus = "RIEN"
        elif touche_pressee[pygame.K_n]:
            if affichage_bonus != "CASES":
                affichage_bonus = "CASES"
            else:
                affichage_bonus = "RIEN"  
        elif touche_pressee[pygame.K_t]:
            if affichage_bonus != "TP":
                affichage_bonus = "TP"
            else:
                affichage_bonus = "RIEN"  

        else:   
            joueur['en_mouvement'] = "non"
        
        mise_a_jour_apparence_joueur(joueur)
        
        # Temps de pause, pour éviter de trop rafraîchir l'écran
        clock.tick(5) 
        affichage_ecran(ecran, niveau, tuiles, joueur, affichage_bonus)

        



    # Fin de la boucle principale, on quitte la partie
    pygame.quit()


if __name__ == "__main__":
    main()