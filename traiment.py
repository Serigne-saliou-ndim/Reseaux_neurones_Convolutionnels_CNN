# -*- coding: utf-8 -*-
"""
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
import shutil

# Définir les classes d'objets et leurs numéros wnid correspondants
classes = {
    "humain": "n00007846",
    "chat_tigre": "n02123159",
    "chat_domestique": "n02123597",
    "uneSouris": "n02352591" ,
    "maison" : "n03544360",
    "poule": "n01514859"
}


# Fonction pour obtenir le chemin du répertoire d'une classe donnée
get_class_path = lambda name: os.path.join("dataset_ImageNet", classes[name], "{}_urlimages".format(classes[name]))

# Fonction pour tracer la distribution des pixels d'une image
def plot_pixel_distribution(img_file):
    # Charger l'image
    img = Image.open(img_file)

    # Créer une figure
    fig = plt.figure(figsize=(16, 8))

    # Tracer l'image
    fig.add_subplot(1, 2, 1)
    plt.title("Image")
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])

    # Tracer l'histogramme
    fig.add_subplot(1, 2, 2)
    plt.title("Histogramme")
    plt.hist(img.convert("L").ravel(), bins=256, range=(0, 256))
    
    plt.show()

# Exemple d'une bonne image
g_image = "dataset_ImageNet/humain/n00007846_383.JPEG"
plot_pixel_distribution(os.path.join(get_class_path("humain"), g_image))

# Exemple d'une mauvaise image
b_image = "1824736_a744fd42ee.jpg"
plot_pixel_distribution(os.path.join(get_class_path("chien"), b_image))

# Fonction pour filtrer les images
def filtered_images(images):
    good_images = []
    bad_images = []
    for filename in images:
        try:
            img = Image.open(filename)
            # Distribution des pixels
            v = img.histogram()
            h, w = img.size
            pourcentage_monochrome = max(v) / float(h * w)

            # Filtrer les images de mauvaise qualité et de petite taille
            if pourcentage_monochrome > 0.8 or h < 300 or w < 300:
                bad_images.append(filename)
            else:
                good_images.append(filename)
        except:
            pass

    print("Nombre de bonnes images : {}".format(len(good_images)))
    print("Nombre de mauvaises images : {}".format(len(bad_images)))
    return good_images, bad_images

# Répertoire de classe pour les images de chien
class_dir = get_class_path("chien")
dog_images = list(map(lambda f: os.path.join(class_dir, f), os.listdir(class_dir)))

# Filtrer les images de chien
g_images, b_images = filtered_images(dog_images)

# Fonction pour afficher une grille d'images
def plot_image_grid(image_files):
    # Taille de la figure
    fig = plt.figure(figsize=(8, 8))

    # Charger les images
    images = [Image.open(img) for img in image_files]

    # Tracer la grille d'images
    for x in range(4):
        for y in range(4):
            ax = fig.add_subplot(4, 4, 4 * y + x + 1)
            plt.imshow(images[4 * y + x])
            plt.xticks([])
            plt.yticks([])

    plt.show()

# Tracer des mauvaises images
plot_image_grid(b_images[:16])

# Dictionnaire pour stocker les images de chaque classe
data_dic = {}
for class_name, wind_number in classes.items():
    print("Nom de la classe : {}".format(class_name))
    class_dir = get_class_path(class_name)
    class_images = list(map(lambda f: os.path.join(class_dir, f), os.listdir(class_dir)))

    g_images, b_images = filtered_images(class_images)

    random.shuffle(g_images)
    data_dic[class_name] = g_images

    plot_image_grid(g_images[:16])

# Fonction pour copier des fichiers vers un répertoire
def copy_files_to_directory(files, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Répertoire créé : {}".format(directory))

    for f in files:
        shutil.copy(f, directory)
    print("Copié {} fichiers.\n".format(len(files)))

# Fonction pour diviser les données en ensembles d'entraînement et de validation
def train_validation_split(base_dir, data_dic, split_ratio=0.2):
    IMAGENET_DATASET = os.path.join(base_dir, "imageNet_dataset")

    if not os.path.exists(IMAGENET_DATASET):
        os.makedirs(IMAGENET_DATASET)

    for class_name, imgs in data_dic.items():
        idx_split = int(len(imgs) * split_ratio)
        random.shuffle(imgs)
        validation = imgs[:idx_split]
        train = imgs[idx_split:]
        copy_files_to_directory(train, os.path.join(IMAGENET_DATASET, "train", class_name))
        copy_files_to_directory(validation, os.path.join(IMAGENET_DATASET, "validation", class_name))

# Diviser les données en ensembles d'entraînement et de validation
#train_validation_split(BASE_DIR, data_dic, split_ratio=0.2)

"""
