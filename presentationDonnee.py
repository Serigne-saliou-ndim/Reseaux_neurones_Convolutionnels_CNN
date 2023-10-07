# -*- coding: utf-8 -*-

import os
from PIL import Image
import matplotlib.pyplot as plt

# Répertoire racine contenant les classes
root_directory = "dataset_ImageNet"

# Liste des classes
classes = [
    {"nom": "humain", "wnid": "n00007846"},
    {"nom": "chat_domestique", "wnid": "n02123597"},
    {"nom": "Souris", "wnid": "n02352591"},
    {"nom": "maison", "wnid": "n03544360"},
    {"nom": "poule", "wnid": "n01514859"},
    {"nom": "coq", "wnid": "n01514668"}
]

# Fonction pour compter les images dans une classe donnée
def compter_images(classe):
    classe_directory = os.path.join(root_directory, classe["nom"])
    if not os.path.exists(classe_directory):
        print(f"Le répertoire de la classe '{classe['nom']}' n'existe pas.")
        return

    images = [f for f in os.listdir(classe_directory) if f.endswith(".JPEG") or f.endswith(".jpg")]
    return len(images)

# Répartition des données
train_ratio = 0.7
test_ratio = 0.15
val_ratio = 0.15

# Dictionnaire pour stocker les histogrammes par classe
histograms = {}

# Parcourir chaque classe
for classe in classes:
    total_images = compter_images(classe)
    train_count = int(total_images * train_ratio)
    test_count = int(total_images * test_ratio)
    val_count = int(total_images * val_ratio)

    # Créer un histogramme pour la classe
    histogram = [train_count, test_count, val_count]
    histograms[classe["nom"]] = histogram

# Tracer l'histogramme
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.2
index = range(len(classes))

train_histogram = [histograms[classe["nom"]][0] for classe in classes]
test_histogram = [histograms[classe["nom"]][1] for classe in classes]
val_histogram = [histograms[classe["nom"]][2] for classe in classes]

plt.bar(index, train_histogram, bar_width, label='Entraînement')
plt.bar([i + bar_width for i in index], test_histogram, bar_width, label='Test')
plt.bar([i + bar_width * 2 for i in index], val_histogram, bar_width, label='Validation')

plt.xlabel('Classes')
plt.ylabel('Nombre d\'images')
plt.title('Répartition des données par classe')
plt.xticks([i + bar_width for i in index], [classe["nom"] for classe in classes])
plt.legend()

plt.tight_layout()
plt.show()



# Fonction pour récupérer le chemin de la première image de chaque classe
def get_first_image_path(classe):
    classe_directory = os.path.join(root_directory, classe["nom"])
    if not os.path.exists(classe_directory):
        print(f"Le répertoire de la classe '{classe['nom']}' n'existe pas.")
        return None

    images = [f for f in os.listdir(classe_directory) if f.endswith(".JPEG") or f.endswith(".jpg")]
    if not images:
        print(f"Aucune image trouvée pour la classe '{classe['nom']}'")
        return None

    first_image = images[0]
    return os.path.join(classe_directory, first_image)

# Créer un graphique avec la première image de chaque classe
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle('Première image de chaque classe')

for i, classe in enumerate(classes):
    first_image_path = get_first_image_path(classe)
    if first_image_path:
        ax = axs[i // 3, i % 3]
        img = Image.open(first_image_path)
        ax.imshow(img)
        ax.set_title(classe["nom"])
        ax.axis('off')

plt.show()