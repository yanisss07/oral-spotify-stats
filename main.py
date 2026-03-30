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

# %% import data
df = pd.read_csv("dataset.csv")
df.head()
print("done")
# %%
plt.plot(x, y)
plt.title("test")
plt.show()
