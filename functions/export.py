import os
from datetime import datetime
import csv
from pathlib import Path

def export(datas):
    if datas:
        #file_number sera le numero du fichier créé
        file_number=datetime.now().strftime("%Y%m%d_%H%M%S")
        file_number=str(file_number)

        #le nom de dossier
        repository="Files_Scraping"

        #le nom des fichiers
        files="file N° "+file_number

        #assemblage du fichier et du dossier
        full_path=Path(repository)/files

        #indique le chemin
        print(f"The full path is : {full_path}")

        try:
            #verification de l'existence 
            Path(repository).mkdir(exist_ok=True)

            #ouverture et fermeture automatique
            with open(f"{full_path}.csv", 'w',newline='', encoding='utf-8') as f:

                #en-tete du ficher csv(colonne)
                fieldnames=['image','title','price','available','rating']

                #création des en-tete
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                writer.writeheader()

                #remplissage des ligne
                for data in datas:
                    writer.writerow(data)

            print("Success.")
        
        except Exception as e: 

            #message d'erreur
            print(f"Error during the process: {e} ")
