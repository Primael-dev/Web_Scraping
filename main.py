#importation des bibliotheque nécessaire
from functions.scraper import requestUrl
from functions.export import export

#déclaration de la liste qui contiendra les objets
datas=[]

#fonction pricipal main
def main():
    requestAnswer=requestUrl()
    export(requestAnswer)

#exécuter le programme uniquement si on lance le main.py
if __name__=="__main__":
    main()

