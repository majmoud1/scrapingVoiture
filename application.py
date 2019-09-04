from flask import Flask, render_template, url_for
from fonctions import selectAllCar, connexionBD, typesVoitures, nbrCarburant, nbrTransmission,nbrVoitureParAnnee, typeModeles

app = Flask('__name__')

@app.route('/')
def index():
    voitures = selectAllCar()
    return render_template("index.html", voitures=voitures)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", typesVoitures = typesVoitures(), nbrCarburant=nbrCarburant(),
    nbrTransmission=nbrTransmission(), nbrVoitureParAnnee=nbrVoitureParAnnee(), typeModeles=typeModeles())


if __name__ == '__main__':
	app.run(debug=True)