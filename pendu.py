#!/usr/bin/env python3
import math
import random
import logging
import json
import requests as req
import urllib.request

logging.basicConfig(filename='logs.log',level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

logging.info("Verification overture de fichier mots. START")
if urllib.request.urlopen("http://www.mit.edu/~ecprice/wordlist.10000").getcode() != 200:
      f= open("./assets/mots.txt","r")
      backup_liste = f.read()
      reponse2 = backup_liste.split(',')
else:      
      resp = req.get("http://www.mit.edu/~ecprice/wordlist.10000")
      logging.info("Verification overture de fichier mots. FIN")
      #print(resp.text)
      mots = resp.content #type bytes avec "\n"
      #transformer le type byte de content en string
      reponse = mots.decode('utf-8')
      reponse2 = reponse.split("\n")


#print(reponse2)

life = 7

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

#print(HANGMANPICS[6])



chosen_word = random.choice(reponse2) 
print(chosen_word)
chaineDecouvrir=[]
for i in range(len(chosen_word)) :
      chaineDecouvrir.append('-')
      #print('-', end=' ')

print(chaineDecouvrir)

nroPendu=0
drapeu = True

while drapeu:
      guest = input("\nChoisir une lettre : ")
      print(guest)
      if guest in chosen_word:
            print('trouvé')
            for ki,x in enumerate(chosen_word):            
                  if guest == x :
                        chaineDecouvrir[ki]=guest                  
            
      else:
            life -=1
            print('il vous reste :',life,' vies')
            print(HANGMANPICS[nroPendu])
            nroPendu+=1
            
      print(chaineDecouvrir)

      if life == 0:
            print('pendu')
            drapeu=False #pour sortir du boucle


print('il est sortie')

#def reemplacer(mots, lettre):
#      print('entra a reemplacer')
#      position=0
#      for x in mots:            
#            if lettre == x :
#                  chaineDecouvrir[position]=lettre
#            position +=1

 #     print(chaineDecouvrir)           