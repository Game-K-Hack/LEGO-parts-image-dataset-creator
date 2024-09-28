import os
import subprocess
from threading import Thread

# Chemin vers le dossier des pièces de LEGO (ex: C:/LDView/LDRAW/parts/)
PARTS_PATH = "<PATH-OF-LEGO-PART>/"
# Chemin vers le logiciel LDView (website: https://www.ldraw.org) (ex: C:/LDView/LDView64.exe)
LDVIEW_PATH = "<PATH-OF-SOFTWARE>"
# Chemin vers le dossier des images exporté
IMAGE_DEST = "<PATH-OF-IMAGES-EXPORTED>/"
# Le "step" est la différence d'angle entre 2 images. Par exemple,
# si la variable "step" est égal à 30 alors la longitude commencera
# par 0 puis 30, 60, etc. Et quand la longitude sera égal à 360 alors
# on ajoute la valeur de la variable "step" à la longitude. Donc si la
# variable "step" est égal à 30 alors il y aura 144 images de la même
# pièce de LEGO sous tous les angles différents.
STEP = 30 # entre 1 et 360
# Si vous comptez arrêter le traitement sans reprendre à 0, vous pouvez
# paramétrer cette variable pour reprendre à une pièce de LEGO précise.
START_INDEX = 0
# La variable "max_thread" permet de définir le nombre de
# taches similaire simultané maximal.
max_thread = 10
# déclare la fonction command, qui prend en paramètre la commande à exécuter.
def command(cmd):
    # utilisation de la variable globale max_thread pour limiter le nombre de tâches simultanées.
    global max_thread
    # declare la fonction à lancer en parallèle avec la commande à exécuter
    def __run__(parm):
        # max_thread est également utilisée ici pour gérer les threads.
        global max_thread
        # exécute la commande donnée en utilisant subprocess.run, qui lance un processus externe.
        subprocess.run(parm)
        # incrémente max_thread après l'exécution de la commande, signalant qu'un thread est terminé.
        max_thread += 1
    # boucle tant que max_thread est inférieur à 1. Attente qu'il y ait un thread disponible avant de continuer.
    while max_thread < 1: pass
    # décrémente max_thread pour indiquer qu'un nouveau thread va être utilisé pour cette tâche.
    max_thread -= 1
    # crée et démarre un nouveau thread pour exécuter la fonction __run__, permettant ainsi d'exécuter la commande en parallèle.
    Thread(target=__run__, args=(cmd,)).start()
# récupérer la liste des fichiers des pièces de LEGO
part_list = os.listdir(PARTS_PATH)
# pour toutes les pièces de LEGO de la liste des fichiers
for index, part in enumerate(part_list[START_INDEX:]):
    # si le fichier à l'extension "dat"
    if part.endswith(".dat"):
        # alors on signale à l'utilisateur à quelle pièce le traitement est rendu
        print((100*(index+START_INDEX))//len(part_list), f"% | Part: {part} | Index:", index+START_INDEX)
        # on récupère le nom du fichier
        filename = part.split(".")[0]
        # si le dossier de la pièce n'existe pas
        if not os.path.exists(IMAGE_DEST + filename):
            # alors on créer le dossier
            os.makedirs(IMAGE_DEST + filename)
        # pour toutes les latitudes, de 0 à 360 avec un écart défini par la variable "STEP"
        for lat in range(0, 360, STEP):
            # pour toutes les longitude, de 0 à 360 avec un écart défini par la variable "STEP"
            for lon in range(0, 360, STEP):
                # exécuter la commande pour extraire les images d'un fichier dat
                command(f"\"{LDVIEW_PATH}\" \"{PARTS_PATH + part}\" -DefaultLatitude={lat} -DefaultLongitude={lon} -SaveSnapshot={IMAGE_DEST}{filename}/part_{filename}_lat{lat}lon{lon}.png")
        # attendre que toutes les exècution parallèle soit terminer avant de passer à une autre pièce
        while max_thread != 10: pass
