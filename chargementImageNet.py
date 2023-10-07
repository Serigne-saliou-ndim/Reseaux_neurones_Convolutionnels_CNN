# -*- coding: utf-8 -*-

"""
Ce code est conçu pour télécharger des images à partir de liens URL spécifiques en utilisant la bibliothèque BeautifulSoup et les traiter pour les stocker localement. Voici ce que fait ce code en détail :

Il importe les bibliothèques nécessaires telles que BeautifulSoup, NumPy, OpenCV, requests, etc.

Il définit une fonction url_to_image(url) qui prend une URL d'image, la télécharge, la convertit en un tableau NumPy et la redimensionne à 224x224 pixels à l'aide de la bibliothèque OpenCV. Ensuite, elle renvoie l'image.

La fonction main() commence par initialiser quelques variables, comme la liste des identifiants WordNet (wnids) et le nombre d'images à télécharger par classe (n_of_training_images).

Elle parcourt les identifiants WordNet (wnids) et pour chaque classe :

Crée un dossier pour stocker les images de cette classe.
Télécharge la page web contenant les URL des images de cette classe à partir du site ImageNet.
Analyse le contenu de la page web avec BeautifulSoup pour extraire les URL.
Mélange aléatoirement la liste des URL.
Télécharge et traite les images jusqu'à atteindre le nombre souhaité (n_of_training_images) ou jusqu'à épuisement des URL.
Les images sont téléchargées à l'aide de la fonction url_to_image(), traitées pour s'assurer qu'elles sont valides et ne sont pas principalement blanches, puis enregistrées localement dans le dossier de la classe correspondante.

Le processus est répété pour chaque classe spécifiée dans la liste wnids.

Le code est exécuté lorsque le fichier est exécuté en tant que script, grâce à la condition if __name__ == '__main__':.

Notez que le code peut être ajusté pour télécharger des images à partir d'autres sources ou d'autres classes en modifiant les identifiants WordNet, les URL ou d'autres paramètres.

Ce code est principalement utilisé pour collecter des données d'entraînement pour des modèles d'apprentissage automatique, en particulier pour les réseaux de neurones convolutionnels (CNN).

"""


from bs4 import BeautifulSoup
import numpy as np
import requests
import cv2
import urllib
import matplotlib.pyplot as plt
import random
import os
import socket
#from urllib.request import urlopen

def url_to_image(url):
# download the image, convert it to a NumPy array, and then read
# it into OpenCV format
#    opener = urllib.request.build_opener()
#    opener.addheaders = [('User-agent','Mozilla/49.0.2')]
    try:
#        op1ener.open(url)
        resp = urllib.request.urlopen(url,timeout=1)        
    except urllib.error.HTTPError:
        print('find one HTTPError')
        return 0
    except urllib.errorURLError:
        print('find one URLError')
        return 0
    except socket.timeout:
        print('time out')
        return 0
            
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.resize(image,(224,224))
    # return the image
    return image

def main():       
    startp = 0
    # number of images per class
    n_of_training_images=10  
    # read in the wordnet id list
    infile = open("./wnids1000.txt","r")
    lines = infile.readlines()
    wnids = []
    for line in lines:
        wnids.append(line.strip('\n').split(' ')[0])
    wnids = wnids[startp:]
    # download images
    for i in range(len(wnids)):
        print("preparing class #%d"%(i+startp))
        # create sub folders
        root = "./images/"+str(i+startp)
        folder = os.path.exists(root)
        if not folder:
            os.makedirs(root)
        # start downloading (BeautifulSoup is an HTML parsing library)
        url = "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=" + wnids[i]
        page = requests.get(url)#ship synset
        soup = BeautifulSoup(page.content, 'html.parser')#puts the content of the website into the soup variable, each url on a different line
        str_soup=str(soup) #convert soup to string so it can be split
        type(str_soup)
        split_urls=str_soup.split('\r\n')#split so each url is a different possition on a list
        # shuffle
        random.shuffle(split_urls)
        print(len(split_urls))#print the length of the list so you know how many urls you have
        # store images
        nn = 0
        kk = 0
        while(nn<n_of_training_images and kk<len(split_urls)):
            if not split_urls[kk] == None:
                try:
                    I = url_to_image(split_urls[kk])
                    if I.any():
                        if (len(I.shape))==3: #check if the image has width, length and channels
#                            plt.imshow(I)
#                            plt.show()
                            if np.mean(I)<250: # remove failed images (almost all white)
                                save_path = root+'/img'+str(nn)+'.jpg'#create a name of each image                
                                cv2.imwrite(save_path,I)
                                nn=nn+1
                except:
                    None
            kk=kk+1
            if kk==len(split_urls):
                print("not enough valid images!")

if __name__ == '__main__':
    main()