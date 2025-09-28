import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def requestUrl():

    library=[]
    max_page=51
    for page in range(1,max_page):

        url=f"http://books.toscrape.com/catalogue/page-{page}.html"

        try:
    
            #envoie de la requete
            response=requests.get(url,timeout=10)

            #vérification du statut de la requete
            if response.status_code==200:

                #changement de l'encodage
                response.encoding="utf-8"

                #recuperation du texte
                html_doc=response.text

                #tranformation en objet facile à traiter
                soup=BeautifulSoup(html_doc,'lxml')

                treatResponse(soup,library)
            else:
                 print(f"la requete de la page {page} à échoué\n Code d'erreur : {response.status_code}")
                 
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion pour la page {page}: {e}")
    
    return library





def treatResponse(soup,All_books):
    #filtre de la varibale soup et recupération des livres
    books=soup.find_all('article',{'class':"product_pod"})

    for book in books:
            
            #data sera comme un objet livre qui contiendra les propriétés de chaque livre
            full_book={}

            base_url="http://books.toscrape.com/"
            #recherche du lien de l'image,récupération et ajout de la partie http grace à urljoin
            book_cover=book.find('img',{'class':"thumbnail"})
            book_img_without_http=book_cover['src']
            book_img=urljoin(base_url,book_img_without_http)

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
            full_book['image']=book_img
            full_book['title']=book_title
            full_book['price']=book_price
            full_book['available']=book_availability
            full_book['rating']=book_rating

            #Ajout de chaque full_book(livre) à All_books(disons bibliotheque)
            All_books.append(full_book)

    return All_books
