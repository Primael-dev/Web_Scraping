#importation des bibliotheque nécessaire
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

#déclaration de la liste qui contiendra les objets
datas=[]

#file_number sera le numero du fichier créé
file_number=datetime.now().microsecond
file_number=str(file_number)

#page allant de 1 à 50
for page in range(1,51):

    #url du site à scrapper
    url=f"http://books.toscrape.com/catalogue/page-{page}.html"

    #envoie de la requete
    response=requests.get(url)
    print(f"Processing of the page N° {page}")

    #vérification du statut de la requete
    if response.status_code==200:

        #changement de l'encodage
        response.encoding="utf-8"

        #recuperation du texte
        html_doc=response.text

        #tranformation en objet facile à traiter
        soup=BeautifulSoup(html_doc,'lxml')

        #filtre de la varibale soup et recupération des livres
        books=soup.find_all('article',{'class':"product_pod"})

        #books est une liste de livre, on la parcours pour recupérer chaque livre
        for book in books:
            
            #data sera comme un objet livre qui contiendra les propriétés de chaque livre
            data={}

            #recherche du lien de l'image,récupération et ajout de la partie http en remplacant ".." par "http"
            book_cover=book.find('img',{'class':"thumbnail"})
            book_img_without_http=book_cover['src']
            book_img=book_img_without_http.replace("..","http://books.toscrape.com")

            #répurécation du titre de chaque livre
            book_title=book_cover['alt']

            #récupération du prix du livre et de la disponibilité après reduction de la zone de recherche
            book_other=book.find('div',{'class':"product_price"})
            book_price=book_other.find('p',{'class':"price_color"}).text
            book_availability=book_other.find('p',{'class':"instock"}).text.strip()

            #récupération de la note qui est une classe de "p"
            rating_tag=book.find('p',{'class':"star-rating"})
            rating_class=rating_tag['class']
            book_rating=f"{rating_class[1]} stars"
            
            #création de l'objet livre 
            data['image']=book_img
            data['title']=book_title
            data['price']=book_price
            data['available']=book_availability
            data['rating']=book_rating

            #Ajout de chaque data(livre) à la datas(disons bibliotheque)
            datas.append(data)
    
    else:

        #message d'erreur meme si c'est pas sur
        print("scraping failed...")

if datas:

    #le nom de dossier
    repository="Files_Scraping"

    #le nom des fichiers
    files="file N° "+file_number

    #assemblage du fichier et du dossier
    full_path=os.path.join(repository,files)

    #indique le chemin
    print(f"The full path is : {full_path}")

    try:
        #verification de l'existence 
        os.makedirs(repository,exist_ok=True)

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
    
    except: 

        #message d'erreur
        print("Error during the process ")

