"""

Auteur : Vincent calzas
mail : vincent.calzas@gmail.com

"""
#Importation bibliothèque
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

#ouverture du fichier csv sur internet grace à panda
data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7', sep = ';')
#Convertis les données des tableau sous forme de liste
df=pd.DataFrame(data)
dep = (df["dep"].values).tolist()#str
sexe = (df["sexe"].values).tolist()#int
sexe= [str(i) for i in sexe]
jour = (df["jour"].values).tolist()#str
hosp = (df["hosp"].values).tolist()#int
hosp= [str(i) for i in hosp]
rea = (df["rea"].values).tolist()#int
rea=[str(i) for i in rea]
rad = (df["rad"].values).tolist()#int
rad=[str(i) for i in rad]
dc = (df["dc"].values).tolist()#int
dc=[str(i) for i in dc]

#déclaration variable
i=0
i2=0
JourHosp, nbHospFranceHomme, nbHospFranceFemme = [], [], []
totalHomme=0
totalFemme=0
ih=0
iFemme=0

def convertisseurJourEnMois(jour,nbHospFranceHomme,nbHospFranceFemme):#on traite les cas hospitalisés par mois pour ne pas surcharger le graphe
	
	#variables
	accVide = ' '
	moisActuel = jour[0][5:7]
	mois = []
	accHomme = 0
	accFemme = 0
	i = 0
	nbHospFranceHommeMois= []
	nbHospFranceFemmeMois= []

	for j in jour:#parcours jour
		if (j[5:7] != moisActuel):#Lorsque l'on change de mois : on met le mois et le nombre d'hospitalisés associé dans des tableaux

			if ((moisActuel == '01') or (mois == [])):
				mois.append(moisActuel + '/' + j[0:4])	
				accVide+=' ' #permet de discerner 03/2020 de 03/2021 ainsi ils apparaissent respectivemnt dans la liste : '03' et ' 03 '
			else: 
				mois.append(accVide + moisActuel + accVide)
			
			nbHospFranceHommeMois.append(accHomme)
			nbHospFranceFemmeMois.append(accFemme)
			moisActuel = j[5:7] #on change de mois
			accHomme = 0
			accFemme = 0

		#sinon on ajoute les hospitalisé de chaque journée
		accHomme += nbHospFranceHomme[i]
		accFemme += nbHospFranceFemme[i]
		i+=1

	mois.append(accVide + moisActuel + accVide)
	nbHospFranceHommeMois.append(accHomme)
	nbHospFranceFemmeMois.append(accFemme)
	
	return mois,nbHospFranceHommeMois,nbHospFranceFemmeMois


for x in dep:#date utilisé pour l'axe des abscisses
    if (x=="29" and sexe[i]=="0"):
            JourHosp.append(jour[i]) #jours utilisés dans le graphique
    i=i+1


for x in jour: #on parcours les jours
    if (sexe[i2] == "1"): #si c'est un homme
        if (x==jour[ih]): #si le jour passée en paramêtre est bien le jour dans les données fournit
            totalHomme+=int(hosp[i2])  #on fait la somme de tous les hospitalisés hommes de la journée
        else: # lorque le jour passée en paramêtre n'est plus le jour dans les données fournit
            nbHospFranceHomme.append(totalHomme) #on classe les hospitalisés de cette journée particulière dans un tableau
            totalHomme = int(hosp[i2]) #on récupère la dernière valeur du nombre d'hospitalisés pour ne pas la perdre et la transmettre au jour suivant
            ih = i2 #on change le paramêtre jour

    if (sexe[i2] == "2"): #si c'est une femme
        if (x == jour[iFemme]): #si le jour passée en paramêtre est bien le jour dans les données fournit
            totalFemme+=int(hosp[i2]) #on fait la somme de tous les hospitalisés hommes de la journée
        else: # lorque le jour passée en paramêtre n'est plus le jour dans les données fournit
            nbHospFranceFemme.append(totalFemme) #on classe les hospitalisés de cette journée particulière dans un tableau
            totalFemme = int(hosp[i2]) #on récupère la dernière valeur du nombre d'hospitalisés pour ne pas la perdre et la transmettre au jour suivant
            iFemme = i2 #on change le paramêtre jour

    i2=i2+1

#on récupère le nombre d'hospitalisés pour l'ajouter à la liste car elle n'a pas été récupérer dans la boucle
nbHospFranceHomme.append(totalHomme)
nbHospFranceFemme.append(totalFemme)

#on regarde le nombre d'hospitalisé par mois
mois, nbHospFranceHommeDef, nbHospFranceFemmeDef = convertisseurJourEnMois(JourHosp,nbHospFranceHomme,nbHospFranceFemme)

#total
nbHospFranceTot = []
for i in range (len(mois)):
	nbHospFranceTot.append(nbHospFranceHommeDef[i] + nbHospFranceFemmeDef[i])

#Graphique de l'évolution du nombre d'hospitalisations pour les femmes et les hommes chaque jour.
tmin = 0 #valeur minimale pour l'axe des abscisses
tmax = len(mois) #valeur maximale pour l'axe des abscisses
ordmin = 0 #valeur minimale pour l'axe des ordonnées
ordmax= max(nbHospFranceTot) #valeur maximale pour l'axe des ordonnées (nombre maximale d'hospitalisées pendant la durée)

#Courbes et axes avec leur nom, légende et titre
plt.grid(color='b', linestyle='-', linewidth=0.5)
plt.axis([tmin, tmax, ordmin, ordmax])
plt.plot(mois, nbHospFranceHommeDef, 'r.', label='Hommes hospitalisés', linestyle='dotted')
plt.plot(mois, nbHospFranceFemmeDef, 'g*', label='Femmes hospitalisées', linestyle='dotted')
plt.plot(mois, nbHospFranceTot, '+', label='Total', linestyle='dotted', c='black')
plt.title("Evolution du nombre d'hospitalisations pour les femmes et les hommes chaque jour.")
plt.axes().set(xlabel='Mois', ylabel="Nombre d'hospitalisations pour les femmes et les hommes")
plt.legend(loc = 'best')
plt.show()

