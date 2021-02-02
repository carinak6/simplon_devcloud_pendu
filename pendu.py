#!/usr/bin/env python3
import math
import random
import logging
import json
import requests as req
import urllib.request

#bloque de configuration du fichier log
logging.basicConfig(filename='logs.log',level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

logging.info("Declaration des variables qu on utlisera pour charger les mots à utiliser")
#declaration des variables 
reponse2='' #

logging.info("Verification overture de fichier mots. START")

# On verifie si le site envoie bien les mots avec try  
try:
      resp = req.get("http://www.mit.edu/~ecprice/wordlist.10000")
      logging.info("Le Site functionne correcterment. Verification overture de fichier mots. FIN")

      #print(resp.text) il retourne un string avec des retourn à la ligne, alors j'utilise content
      mots = resp.content #il retourne une chaine de type bytes avec "\n"      
      
      #transformer le type byte de content en string
      reponse = mots.decode('utf-8')

      #on cree un liste des mots
      reponse2 = reponse.split("\n")

except urllib.error.URLError as e:
      print('Erreur trouve  ==> ',e.reason)
      logging.error('Error %s: %s', '01234', 'Le site source est indisponible :  '+e.reason)
      

#on verifie si la variable que recupere les mots est vide, s'il l'est alors ça veut dire qu il y a eu un probleme de ressource
#et on passe à la lecture du fichier des mots en local
if len(reponse2) == 0 :
      logging.info("Error le site est indisponible. Overture du fichier mots en local. START")
      f= open("assets/mots.txt","r")
      backup_liste = f.read()
      reponse2 = backup_liste.split(',') #on cree un liste des mots
      logging.info("Error le site est indisponible. Verification overture de fichier mots. FIN")

#print(reponse2)

logging.info("Declaration des variables à utiliser")
life = 7

#liste avec le code ascii du pendu
HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

HANGMANPICS.reverse() # j ai enversé la liste de l'ascii pour utiliser la variable life comme index de l'affichage du pendu

#on choisi un mot al hazar
chosen_word = random.choice(reponse2) 
logging.info("On chosie al hazar un mot : "+ chosen_word)

logging.info("declaration des variables à utiliser dans la boucle. START")
#declaration des variables à utiliser dans la boucle

print(chosen_word) #pour verifier
chaineDecouvrir=[] #variable de type liste avec les lettres que on aura decouverte
finJeux = False #variable pour sortir de la boucle
listeLettresChoisi=set() #variable pour afficher les lettres dejà choisie, on utlise cet parce qu il repet pas les valeurs
motsDecouvrir = ''
guest='' # lettre tappée pour l utilisateur

logging.info("Declaration des variables . FIN")

logging.info("Generation d'une liste qui represente les mots choisi. START")
#boucle pour asigner les tires qui correspondant au mots choisie
for i in range(len(chosen_word)) :
      chaineDecouvrir.append('-')
      #print('-', end=' ')

print(chaineDecouvrir)
logging.info("Generation d'une liste qui represente les mots choisi. FIN ==> mot à diviner :"+chosen_word +" representation : "+str(chaineDecouvrir ))

logging.info("Debut du boucle while pour diviner le mot caché. START ")
while finJeux == False:
      #verifie si on a deja tapé des lettre
      if len(listeLettresChoisi) != 0:
            print('Vous avez ',life,' vies')
            print("Lettres deja choisi : ", ' '.join(listeLettresChoisi))

      #demande d'entrer un lettre, on la transforme en minuscule
      guest = input("\nTapez une lettre : ").lower()  
      while len(guest) < 1:
            logging.warning('Warning %s: %s', '1111', 'L\'utilisateur n\'a pas tapez une lettre, demandede reessayer')
            print('\nVous \'avez pas tapez une lettre reessaye ')
            guest=input("\nTapez une lettre : ").lower()  

      print(guest) #on affiche la letre
      logging.info("L'utilisateur à tappé : "+guest)

      listeLettresChoisi.add(guest) #ajoute la lettre dans le set, pour afficher apres les lettres deja tapée

      logging.info("Verification si la lettre fait partir du mot à diviner ")
      #TODO verifier quand le mot est un valor vide, alors faire un loop
      #on demande si la lettre est partie du mot choisie
      if guest in chosen_word:            
            print('Lettre trouvée!!!', guest.upper())
            for ki,x in enumerate(chosen_word):#on ajoute la lettre dans la liste avec le mot a decouvrir
                  if guest == x :
                        chaineDecouvrir[ki]=guest # on reemplace  le tiré pour la lettre trouvé
            
            motsDecouvrir = ''.join(chaineDecouvrir) #transforme la liste en string, pour la comparer avec le mots choisie
            #print('mot decouverte :', motsDecouvrir ) 
            logging.info("La lettre : "+guest + "fait partie du mot, alors chaine decouverte pour le moment "+ motsDecouvrir)
            
      else: #le lettre ne fait pas partie du mot à decouvrir
            life -=1  # on enleve un vie
            print('Lettre introuvable !!!', HANGMANPICS[life]) #on affiche le dessin ascii qui prends life comme index
            logging.info("La lettre : "+guest + " ne fait pas partie du mot, alors on enleve une vie, il reste "+ str(life)+" vies")
            
      print(chaineDecouvrir) #On affiche la liste de lettre du mots à decouvrir ex: ['-', 'a', 'r', '-', '-', '-', '-', '-']
      logging.info("Affichage du mot decouverte jusqu'au moment "+ str(chaineDecouvrir) + "  liste des lettres tappé : "+str(listeLettresChoisi))

      #Bloque du code pour verifier si on a decouvert le mot, utilisé toutes les vies et pour essayer de deviner le mot
      logging.info("Initiation de verifaction si on a decouvert le mot . START")
      if motsDecouvrir == chosen_word : #on verifie si le mots decouverte est egal à la mots choisie

            print(f'Vous avez Gangné!!! Vous avez trouvé : {chosen_word} ')
            finJeux=True #pour sortir du boucle
            logging.info(f"Mot deviné, L'utilisateur a tappée correctement le mot : {chosen_word}. FIN")

      elif life == 0: # verifie si il n y a pas de vie
            print('Pendu !!!, vous avez perdu ....')
            finJeux=True #pour sortir du boucle
            logging.info("Il n'y plus de vie, l'utilisateur a perdu. FIN")

      else: # demande si on veut essayer de diviner le mot

            logging.info("Demande à l'utilisateur s'il veut taper le mot à diviner : [Oui] o / [Non]?. START")
            print("Vous voulez essaie le mot à diviner [Oui] o / [Non] ?")
            res = input().lower() # l utilisateur doit repondre s'il veut essayer de diviner le mot [Oui] o / [Non], le oui = o, et non c est n'import quel lettre, pour pas devoir redemander au cas où 
            
            if res == 'o' or res =='oui': # l'utilisateur veut diviner le mots
                  print("Tapez le mot : ")
                  respuesta = input().lower() # reponse de l'utilisateur                  
                  logging.info("L'utilisateur à tapé Oui, mot tapé : "+respuesta+" . START")

                  if respuesta == chosen_word: # verification si la reponse est egal au mot choisi
                        print('Vous avez Deviné Bravo Gangné!!!')
                        finJeux=True #pour sortir du boucle
                        logging.info("Mot correcte GAGNE, L'utilisateur à tapé Oui. FIN ")
                  else :
                        print('Mots Incorrecte')
                        life -=1  # on enleve un vie
                        print(HANGMANPICS[life]) # on affiche le dessin ascii qui prends life comme index
                        logging.info("Mots Incorrecte, alors on enleve une vie, il reste "+ str(life)+" vies.")
                        logging.info( "L'utilisateur à tapé Oui. FIN")
            else:
                  logging.info("L'utilisateur à tapé n'import quel lettre pour dire NON, on continue le boucle")

print("c est fini !! :-)")

#TODO passer le code sur des functions et apres sur une class
          