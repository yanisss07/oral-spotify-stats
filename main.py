# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math as m
import simpy as sp
import sys
import requests

"""
Titre : "Comment rendre un morceau populaire sur Spotify ?"
Plan d'attaque :
  1. HOOK (30s)
  - "On vous a recruté pour répondre à une question simple : faut-il mettre du contenu explicite pour cartonner sur Spotify ?"
  - Spoiler : la réponse change complètement selon comment on regarde les données.

  2. LE DATASET (1min)
  - 114 000 morceaux, 114 genres, 20 variables audio
  - Source : Spotify API via Kaggle
  - Variable cible : popularity (score 0-100 calculé par Spotify)
  - Variable analysée : explicit (contenu censuré ou non)

  3. ANALYSE 1 — Vision globale (2min)
  - Bar chart : popularité moyenne explicit vs non-explicit sur tout le dataset
  - Résultat : 36.5 vs 32.9 → explicit = +3.5 points
  - Conclusion : "Les chansons explicites sont plus populaires, il faut oser"

  4. ANALYSE 2 — Vision par genre (2min)
  - Bar chart ou scatter : même comparaison explicit/non-explicit mais par genre
  - Hip-hop : 23.3 vs 44.5 → explicit = -21 points (r = -0.30)
  - K-pop : r = -0.49 → explicit pénalise massivement
  - R-n-b : explicit = +11 points → aide au contraire
  - Conclusion : "Dans les genres qui utilisent le plus l'explicit, c'est justement là que ça nuit le plus"

  5. CONFRONTATION — Le paradoxe de Simpson (1min)
  - Même dataset, même variable, deux conclusions opposées
  - Explication : les genres très explicit (hip-hop) ont une popularité moyenne plus basse globalement → ils tirent la
  moyenne vers le bas, ce qui fausse la vision globale
  - "La moyenne globale vous ment si vous ignorez les sous-groupes"

  6. RECOMMANDATION BUSINESS (30s)
  - Si tu fais du r-n-b → explicit aide (+11 pts)
  - Si tu fais du hip-hop → explicit nuit (-21 pts), les tracks propres crossover mieux
  - Si tu regardes juste la moyenne globale → tu prends la mauvaise décision
  - Morale : toujours segmenter avant de conclure

  Graphiques à faire (dans l'ordre)
  1. Bar chart simple : explicit vs non-explicit, popularité moyenne globale (Analyse 1)
  2. Bar chart groupé par genre : les 5-6 genres les plus parlants (hip-hop, k-pop, emo, r-n-b, funk) avec les deux barres
  explicit/non-explicit côte à côte (Analyse 2)
  3. Scatter plot : % explicit par genre vs popularité moyenne du genre (114 points, labels des extrêmes)
  4. Heatmap corrélation globale (pour montrer qu'on a exploré toutes les features)

Diapo :
  ┌─────┬────────────────────────────────────┐
  │  #  │               Slide                │
  ├─────┼────────────────────────────────────┤
  │ 1   │ Titre + hook                       │
  ├─────┼────────────────────────────────────┤
  │ 2   │ Présentation dataset               │
  ├─────┼────────────────────────────────────┤
  │ 3   │ Analyse 1 + graphique global       │
  ├─────┼────────────────────────────────────┤
  │ 4   │ Analyse 2 + graphique par genre    │
  ├─────┼────────────────────────────────────┤
  │ 5   │ Confrontation des deux conclusions │
  ├─────┼────────────────────────────────────┤
  │ 6   │ Explication paradoxe de Simpson    │
  ├─────┼────────────────────────────────────┤
  │ 7   │ Recommandation + conclusion        │
  └─────┴────────────────────────────────────┘



Le Paradoxe de Simpson :

  Imagine que tu regardes si les pompiers causent des incendies. Tu constates que dans les villes où y'a beaucoup de
  pompiers, y'a plus d'incendies → "les pompiers causent des incendies !"

  Mais si tu regardes par taille de ville : dans chaque catégorie de ville, plus de pompiers = moins d'incendies. La tendance
   globale était inversée à cause d'une variable cachée (la taille de la ville).

  Ici c'est pareil :
  - Globalement → explicit semble aider
  - Mais c'est parce que les genres qui font beaucoup d'explicit (hip-hop, trap) sont des genres qui ont naturellement un
  certain niveau de popularité
  - Quand tu regardes au sein de chaque genre → dans le hip-hop, les tracks explicit performent bien moins bien que les
  propres

  La variable cachée = le genre musical. Si tu l'ignores, tu tires la mauvaise conclusion.
"""
print("imported!")

# %% import data
df = pd.read_csv("dataset.csv")
df.head()
print("done")
# %%
plt.plot(x, y)
plt.title("test")
plt.show()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np





#%% Exercice 1

data = [(25.44, 9.64, 'Algeria'), (3367.85, 203.43, 'Argentina'), (80.87, 3.58, 'Australia'), (290.67, 21.07, 'Austria'), (413.51, 24.52, 'Belgium'), (437.04, 64.16, 'Bulgaria'), (678.71, 40.88, 'Canada'), (24.08, 1.42, 'Cyprus'), (594.11, 67.71, 'Czechia'), (41.75, 5.37, 'Denmark'), (31.67, 4.67, 'Estonia'), (29.51, 2.72, 'Finland'), (2689.36, 163.74, 'France'), (2764.98, 218.38, 'Germany'), (77.77, 10.1, 'Ireland'), (154.28, 13.66, 'Israel'), (1349.21, 176.33, 'Italy'), (14.35, 1.19, 'Luxembourg'), (722.32, 84.77, 'Malaysia'), (7.58, 0.72, 'Malta'), (433.79, 26.64, 'Netherlands'), (214.26, 33.48, 'Portugal'), (896.28, 118.56, 'Romania'), (147.79, 26.22, 'Serbia'), (149.09, 39.98, 'Slovakia'), (115.18, 8.12, 'Slovenia'), (1692.84, 106.85, 'Spain'), (153.63, 18.84, 'Sweden'), (185.64, 12.4, 'Switzerland'), (1086.72, 210.26, 'United Kingdom'), (14074.58, 1312.24, 'United States')]

# Création des séries marginales
X = []
Y = []

for z in data:
    X.append(z[0])
    Y.append(z[1])
    
# 1. Indicateurs statistiques
print("1.")

print("Nombre moyen d'admissions en soins critiques")

print("Médiane : ", np.median(X))
print("Moyenne : ", np.mean(X))
print("Variance : ", np.var(X))
print("Ecart-type : ", np.std(X))

print("Nombre moyen de décès")

print("Médiane : ", np.median(Y))
print("Moyenne : ", np.mean(Y))
print("Variance : ", np.var(Y))
print("Ecart-type : ", np.std(Y))


# 2. Diagramme de dispersion
print("2. Tracé du diagramme de dispersion")
plt.close('all')        

plt.scatter(X,Y)
plt.title("Diagramme de dispersion")
plt.xlabel("Nombre moyen d'admissions en soins critiques")
plt.ylabel("Nombre moyen de décès")
plt.show()


# 3. Covariance et corrélation
print("3.")

print("Covariance : ", np.cov(X,Y,bias=True)[0][1])
print("Coefficient de corrélation : ", np.corrcoef(X,Y)[0][1])


# 4. Régression linéaire à la main 
print("4.")
a = np.cov(X,Y,bias=True)[0][1]/np.var(X)
b = np.mean(Y) - a*np.mean(X)
print("La droite de régression linéaire a pour équation y=",round(a,3),"x+",round(b,3))


# 5. Régression linéaire avec polyfit
print("5.")
aa, bb = np.polyfit(X,Y,1)
print("Avec polyfit, la droite de régression linéaire a pour équation y=",round(aa,3),"x+",round(bb,3))

# Tracé de la droite de régression linéaire
print("5. Tracé de la droite de régression linéaire")
x_trace = np.array([0,max(X)])
plt.figure()
plt.plot(x_trace, a*x_trace+b , 'red')
plt.scatter(X,Y)
plt.title("Diagramme de dispersion")
plt.xlabel("Nombre moyen d'admissions en soins critiques")
plt.ylabel("Nombre moyen de décès")
plt.show()


import pandas
import matplotlib.pyplot as plt

# Exercice 1. Les données de la France. 

# 1. Chargement de la table
# Attention au dossier où l'on travaille pour charger les données.




print("1.")
COVID = pandas.read_csv(r"C:\Users\Timothée\OneDrive\Bureau\Teaching_IUT_Toulouse2024-2025\StatsS2_2024-2025\Stats24-25\TP3\Data2TP3.csv")

#%% 
#2.
print("2.")

COVID_NC=COVID["new_cases"]

print(COVID_NC.head(8))


# 3. Affichage d'une donnée
print("3.")
COVID2102 = COVID.loc[COVID['date'] == '2021-02-01']
affichage = COVID2102["new_cases"]
print("Nombre de patients hospitalisés le 1 Février 2021 : ", affichage)
# Ici affichage est au format Series ce qui donne le numéro de ligne 374 
# Pour éviter cela, on peut remplacer affichage par affichage.iloc[0] 
# ou par affichage.to_string(index=False)


# 4. Indicateurs statistiques
print("4.")
print("Nombre moyen de patients hospitalisés ", COVID["hosp_patients"].mean())

print("Indicateurs statistiques du nombre de patients hospitalisés")
print(COVID["hosp_patients"].describe())


# 5. Indicateurs statistiques partiels
print("5.")
COVID_2021 = COVID.loc[(COVID['date']>='2021-01-01') & (COVID['date']<='2021-12-31')]
print("Indicateurs statistiques du nombre de patients hospitalisés sur l'année 2021")
print(COVID_2021["hosp_patients"].describe())


# 6. Diagramme en boite
print("6. Diagramme en boite")
plt.close('all')
COVID_2021["hosp_patients"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des hospitalisations COVID en 2021")
plt.show()


# 7. Tracé de courbe
print("7. Tracé d'une courbe")
COVID.plot(x='date', y='new_cases_smoothed')
plt.show()
#COVID['new_cases_smoothed'] = COVID['new_cases'].rolling(window=7).mean()

# 8. Tracé de plusieurs courbes avec plusieurs échelles
print("8. Tracé de plusieurs courbes")
COVID.loc[COVID['date']<='2021-11-30'].plot(x='date', y=['new_cases_smoothed', 'hosp_patients', 'icu_patients'], secondary_y = 'icu_patients')
plt.show()


# 9. Tracé de diagramme en bandes
print("9. Tracé de diagrammes en bandes")
COVID.loc[(COVID['date']>='2021-11-01') & (COVID['date']<='2021-12-15')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients'])
plt.show()


# 10. Subplots 
print("10. Tracé de plusieurs graphiques avec subplot")
COVID.loc[(COVID['date']>='2021-11-01') & (COVID['date']<='2021-12-15')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients', 'icu_patients'], subplots=True, layout=(3,1))
plt.show()



# 11. Subplots avec matplotlib. 
print("11. Gestion fine de subplots avec matplotlib")
fig, (ax1, ax2, ax3) = plt.subplots(3,1)

COVID.loc[(COVID['date']>='2021-11-01') & (COVID['date']<='2021-12-15')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients'], ax=ax1)
COVID.loc[(COVID['date']>='2020-09-15') & (COVID['date']<='2020-10-31')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients'], ax=ax2)
COVID.plot(x='date', y='people_fully_vaccinated', ax=ax3)
plt.show()

# 11bis. Autre correction
print("11. Gestion fine de subplots avec matplotlib v2")

plt.figure()
ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,3)
ax3 = plt.subplot(1,2,2)

COVID.loc[(COVID['date']>='2021-11-01') & (COVID['date']<='2021-12-15')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients'], ax=ax1)
COVID.loc[(COVID['date']>='2020-09-15') & (COVID['date']<='2020-10-31')].plot.bar(x='date', y=['new_cases_smoothed', 'hosp_patients'], ax=ax2)
COVID.plot(x='date', y='people_fully_vaccinated', ax=ax3)
plt.show()


