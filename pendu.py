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

logging.info("Verification overture de fichier mots. START")
#on verifie si le site envoie bien les mots
if urllib.request.urlopen("http://www.mit.edu/~ecprice/wordlist.10000").getcode() != 200:
      #s'il y a en erreur on affiche un fichier en local
      f= open("./assets/mots.txt","r")
      backup_liste = f.read()
      reponse2 = backup_liste.split(',') #on cree un liste des mots
else:      
      resp = req.get("http://www.mit.edu/~ecprice/wordlist.10000")
      logging.info("Verification overture de fichier mots. FIN")
      #print(resp.text) il retourne un string avec des retourn à la ligne
      mots = resp.content #il retourne une chaine de type bytes avec "\n"

      #transformer le type byte de content en string
      reponse = mots.decode('utf-8')

      #on cree un liste des mots
      reponse2 = reponse.split("\n")

#print(reponse2)

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

#on choisi un mot al hazar
chosen_word = random.choice(reponse2) 

print(chosen_word) #pour verifier

chaineDecouvrir=[] #variable de type liste avec les lettres que on aura decouverte

#boucle pour asigner les tires qui correspondant au mots choisie
for i in range(len(chosen_word)) :
      chaineDecouvrir.append('-')
      #print('-', end=' ')

print(chaineDecouvrir)

nroPendu=0 #variable qui affichera la partie du pendu
finJeux = False #variable pour sortir de la boucle
listeLettresChoisi=set() #variable pour afficher les lettres dejà choisie

while finJeux == False:
      if len(listeLettresChoisi) != 0:
            print("Lettres deja choisi : ", ' '.join(listeLettresChoisi))

      guest = input("\nChoisir une lettre : ")
      print(guest) #on affiche la letre

      listeLettresChoisi.add(guest) #ajoute la lettre dans le set

      if guest in chosen_word: #on demande si la lettre est partie du mot choisie
            #lprint('trouvé')
            for ki,x in enumerate(chosen_word):#on ajoute la lettre dans la liste avec le mot a decouvrir
                  if guest == x :
                        chaineDecouvrir[ki]=guest                  
            
      else: #le lettre n'est pas partie du mot à decouvrir
            life -=1
            print('il vous reste :',life,' vies')
            print(HANGMANPICS[nroPendu])
            nroPendu+=1 #variable pour savoir quel parti de l'ascii on affiche la prochaine fois
            
      print(chaineDecouvrir) #liste de lettre de mots à decouvrir
      motsDecouvrir = ''.join(chaineDecouvrir) #transforme la liste en string, pour la comparer avec le mots choisie
     #print('mot decouverte :', motsDecouvrir )

      if motsDecouvrir == chosen_word : #on verifie si le mots decouverte est egal à la mots choisie
            print('Vous avez Gangné!!!')
            finJeux=True #pour sortir du boucle
      elif life == 0: # verifie si il n y a pas de vie
            print('pendu')
            finJeux=True #pour sortir du boucle
      else:#demande si on veut essayer de diviner le mot
            print("Vous voulez essaie le mot à diviner [Oui] / [Non]?")
            res = input()
            if res == 'o':
                  print("Tapez le mot : ")
                  respuesta = input()
                  if respuesta == chosen_word:
                        print('Vous avez Gangné!!!')
                        finJeux=True #pour sortir du boucle
                        


print("c est fini")
          