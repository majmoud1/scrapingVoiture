import requests
from bs4 import BeautifulSoup
from fonctions import annee, connexionBD

#-----------------------Année posible------------------------------------------------------------------------
annee = annee()

#----------------------------------------------------------------------------------------------------------
#       Scrapping des données du site sn.coinafrique.com dans la catégorie voitures
#----------------------------------------------------------------------------------------------------------

for i in range(1,11):
    site = requests.get("https://sn.coinafrique.com/categorie/voitures/45?page='{}'".format(i))
    
    if(site.status_code == 200):
        contenu = site.text

        contenuSoup = BeautifulSoup(contenu, "lxml")
        
        div = contenuSoup.find_all("div", class_ = "card round")

        """                 Récupération des informations pour chaque voiture            """
        try:
        #--------------------------Parcours des données scrappées-----------------------------------------------
            for v in div:
                voiture = BeautifulSoup(str(v), "lxml")
            #-----------------------Prix------------------------------------------------------------------------
                prix = voiture.find("p", class_ = "card-title activator orange-text")
                prix = BeautifulSoup(str(prix), "lxml").getText().strip()
                prix = prix[0:len(prix)-4]
                #prix = int(prix[0:len(prix)-4].replace(' ',''))
            #-----------------------Marque, Modele et année de la voiture----------------------------------------
                m = voiture.find("p", class_ = "card-desc")
                m = BeautifulSoup(str(m), "lxml").getText().strip()
                liste = m.split()
                #--------------------Année de la voiture---------------------------------------------------------
                anneeVoiture = ""
                for i in annee:
                    if(liste.__contains__(i)):
                        anneeVoiture = i
                    else:
                        continue
                
            #-----------------------Localisation-----------------------------------------------------------------
                localisation = voiture.find("p", class_ = "card-location")
                localisation = BeautifulSoup(str(localisation), "lxml").getText()[12:].strip()
            #-----------------------Image------------------------------------------------------------------------
                image = voiture.find("img", class_ = "imgAnnonce")["src"]
            #-----------------------Lien vers annonce------------------------------------------------------------
                site = "https://sn.coinafrique.com"
                lienAnnonce = site + voiture.find("a")["href"]

                #-----------------------Accès à l'annonce pour avoir plus d'informations-----------------------
                acces_annonce = requests.get(lienAnnonce)
                if(acces_annonce.status_code == 200):
                    #----------Récupérons le modele, le constructeur, le kilometrage, la transmission et le carburant
                    c = acces_annonce.text
                    caracteristiques = BeautifulSoup(str(c), "lxml").find("div", class_="details-characteristics")
                    details = caracteristiques.find_all("span", class_="qt")
                    
                    tab = []
                    for i in details:
                        tab.append(BeautifulSoup(str(i), "lxml").find("span", class_="qt").getText().upper().strip())
                    
                    if(tab.__contains__('N/A') or (tab[4] != "GASOIL" and tab[4] != "ESSENCE")):
                        tab.clear()
                    else:
                        km = tab[2].split()
                        tab[2] = int(km[0])
                        #---------------------------------------------------------------------------------------------------
                        #       Connexion à la base de données PostgreSQL pour insérer les données
                        #---------------------------------------------------------------------------------------------------
                        connexion = connexionBD()
                        cursor = connexion.cursor()
                        sql = """
                            INSERT INTO voiture_a_vendre_1 (marque, modele, kilometrage, transmission,
                            carburant, annee, prix, localisation, image, lienAnnonce)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        cursor.execute(sql,(tab[0],tab[1],tab[2],tab[3],tab[4],anneeVoiture,prix,localisation,image,lienAnnonce))
                        connexion.commit()
                        cursor.close()
                        connexion.close()
                else:
                    break
        except Exception:
            print("Erreur lors de la recherche des informations")
    else:
        break