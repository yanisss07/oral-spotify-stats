# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math as m
import simpy as sp
import sys
import requests

"""
Titre : Comment rendre un morceau popullaire sur spotify ?
Plan d'attaque :
    Plan d'attaque (structure présentation)

    1. HOOK (30s)
       "On vous a recruté pour répondre à une question simple :
        comment rendre un morceau populaire sur Spotify ?"

    2. LE DATASET (1min)
       - 114 000 morceaux, 114 genres, 20 variables audio
       - Source : Spotify API via Kaggle
       - Variables clés : popularity, energy, danceability, valence...

    3. ANALYSE 1 — Niveau micro (chanson) (2min)
       - Scatter plot energy vs popularity + droite de régression
       - Corrélation + R²
       - Conclusion : "Les chansons énergiques sont plus populaires"

    4. ANALYSE 2 — Niveau macro (genre) (2min)
       - Scatter plot par genre (énergie moyenne vs popularité moyenne)
       - Les genres metal/hardcore en bas à droite, pop/r&b en haut au milieu
       - Conclusion : "Les genres les plus populaires sont d'énergie modérée"

    5. CONFRONTATION — Le paradoxe (1min)
       - Même dataset → deux conclusions opposées
       - Explication : le genre est une variable confondante
       - "Vous ne pouvez pas recommander 'plus d'énergie' sans savoir dans quel genre"

    6. RECOMMANDATION BUSINESS (30s)
       - Si vous composez dans un genre donné → plus d'énergie aide
       - Si vous cherchez à toucher le plus grand public → restez dans l'énergie modérée
       - L'échelle d'analyse change la décision

    ---
    Graphiques à faire (dans l'ordre)

    1. Scatter plot energy vs popularity (tous les points, couleur par genre ou transparence) + régression
    2. Scatter plot agrégé par genre (114 points, taille = nb tracks, labels des genres extrêmes)
    3. Bar chart top 10 / bottom 10 genres par popularité, avec leur énergie moyenne en couleur
    4. Heatmap de corrélation des variables numériques (pour montrer qu'on a exploré)
"""

# %% import data
df = pd.read_csv("dataset.csv")
df.head()
print("done")
# %%
plt.plot(x, y)
plt.title("test")
plt.show()
