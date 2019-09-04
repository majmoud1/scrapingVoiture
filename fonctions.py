import psycopg2 as psy

def annee():
    annee = []
    debut1 = 200
    debut2 = 20
    for i in range(1,10):
        annee.append(str(debut1)+str(i))
    for i in range(10,20):
        annee.append(str(debut2)+str(i))
    return annee

def connexionBD():
    serveur = "localhost"
    bdd = "scraping"
    user = "majmoud"
    password = "diop"
    try:
        connexion = psy.connect(host=serveur, database=bdd, user=user, password=password)
        return connexion
    except Exception:
        print("Erreur lors de la connexion !!!")

def createTable():
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS voiture_a_vendre_1(
            idVoiture SERIAL PRIMARY KEY NOT NULL,
            marque VARCHAR(255),
            modele VARCHAR(255),
            transmission VARCHAR(50),
            carburant VARCHAR(50),
            kilometrage INT,
            annee VARCHAR(10),
            prix VARCHAR(50),
            localisation VARCHAR(100),
            image TEXT,
            lienAnnonce TEXT
        )
    """
    cursor.execute(sql)
    connexion.commit()
    cursor.close()

def selectAllCar():
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT * FROM voiture_a_vendre_1 "
    cursor.execute(sql)
    donnees = cursor.fetchall()
    cursor.close()
    connexion.close()
    return donnees

def nbrTransmission():
    connexion = connexionBD()
    cursor = connexion.cursor()

    sql1 = " SELECT COUNT(transmission) FROM voiture_a_vendre_1 WHERE transmission='AUTOMATIQUE' "
    cursor.execute(sql1)
    automatique = cursor.fetchall()

    sql2 = " SELECT COUNT(transmission) FROM voiture_a_vendre_1 WHERE transmission='MANUEL' "
    cursor.execute(sql2)
    manuel = cursor.fetchall()

    cursor.close()
    connexion.close()
    return int(automatique[0][0]), int(manuel[0][0])

def nbrCarburant():
    connexion = connexionBD()
    cursor = connexion.cursor()

    sql1 = " SELECT COUNT(carburant) FROM voiture_a_vendre_1 WHERE carburant='ESSENCE' "
    cursor.execute(sql1)
    essence = cursor.fetchall()

    sql2 = " SELECT COUNT(carburant) FROM voiture_a_vendre_1 WHERE carburant='GASOIL' "
    cursor.execute(sql2)
    gasoil = cursor.fetchall()

    cursor.close()
    connexion.close()
    return int(essence[0][0]), int(gasoil[0][0])

def nbrVoitures(marque):
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT COUNT(marque) FROM voiture_a_vendre_1 WHERE marque='{}' ".format(marque)
    cursor.execute(sql)
    nbr = cursor.fetchone()
    cursor.close()
    connexion.close()
    return int(nbr[0])

def typesVoitures():
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT DISTINCT marque FROM voiture_a_vendre_1 "
    cursor.execute(sql)
    m = cursor.fetchall()
    cursor.close()
    connexion.close()
    marques = []
    nbr = []
    for i in m:
        marques.append(i[0])
        nbr.append(nbrVoitures(i[0]))
    return marques, nbr

def VoitureParAnnee(annee):
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT COUNT(marque) FROM voiture_a_vendre_1 WHERE annee='{}' ".format(annee)
    cursor.execute(sql)
    nbr = cursor.fetchone()
    cursor.close()
    connexion.close()
    return int(nbr[0])

def nbrVoitureParAnnee():
    annees = annee()
    nbrVoiture = []
    for i in annees:
        nbrVoiture.append(VoitureParAnnee(i))
    return annees, nbrVoiture

def nbrVoitureParModele(modele):
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT COUNT(modele) FROM voiture_a_vendre_1 WHERE modele='{}' ".format(modele)
    cursor.execute(sql)
    nbr = cursor.fetchone()
    cursor.close()
    connexion.close()
    return int(nbr[0])

def typeModeles():
    connexion = connexionBD()
    cursor = connexion.cursor()
    sql = " SELECT DISTINCT modele FROM voiture_a_vendre_1 "
    cursor.execute(sql)
    m = cursor.fetchall()
    modeles = []
    nbr = []
    for i in m:
        modeles.append(i[0])
        nbr.append(nbrVoitureParModele(i[0]))
    cursor.close()
    connexion.close()
    return modeles, nbr





