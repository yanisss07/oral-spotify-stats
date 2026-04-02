# %% imports
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os.makedirs("out", exist_ok=True)

print("done!")

# %% import data
df = pd.read_csv("dataset.csv")
df["explicit"] = df["explicit"].astype(bool)


# %% dataset infos
print(df.shape)
print(df.dtypes)
# print(df.describe())

# %% 1/ corrélation heatmap galere
cols = [
    "popularity",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]
other: list[str] = [c for c in cols if c != "popularity"] + ["explicit"]
popularity = np.array(df["popularity"])
pop_corr = pd.Series({c: float(np.corrcoef(df[c], popularity)[0, 1]) for c in other})

fig, ax = plt.subplots()
ax.imshow(np.array([pop_corr.to_numpy()]), cmap="RdYlGn", vmin=-1, vmax=1)
ax.set_yticks([0])
ax.set_xticks(range(len(other)))
ax.set_title(
    "coefficient de corrélation de la popularité et toutes les autres colonnes"
)
ax.set_yticklabels(["popularity"])
ax.set_xticklabels(other, rotation=45, ha="right")
for i, col in enumerate(other):
    ax.text(i, 0, f"{pop_corr[col]:.2f}", ha="center", va="center")
plt.savefig("out/1.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 2/ popularity vs explicit nul
fig, ax = plt.subplots()
ax.bar(["non explicit", "explicit"], df.groupby("explicit")["popularity"].mean())
ax.set_ylabel("popularité moyenne")
corr = float(np.corrcoef(df["explicit"], df["popularity"])[0, 1])
ax.set_title("popularité groupée par explicite ou non")
ax.text(
    0.02,
    0.98,
    f"coefficient de corrélation = {corr:.2f}",
    transform=ax.transAxes,
    ha="left",
    va="top",
)
plt.savefig("out/2.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 3/ count track_genre
df["track_genre"].value_counts()
# %% 4/ compute corr by genre
all_corr = (
    df.groupby("track_genre")
    .apply(
        lambda g: (
            float(np.corrcoef(g["explicit"], g["popularity"])[0, 1])
            if g["explicit"].nunique() > 1
            else float("nan")
        )
    )
    .dropna()
    .sort_values()
)
# SELECT track_genre, CORRCOEF(explicit, popularity)
# FROM df
# GROUP BY track_genre
# print(all_corr)

# %% 5/ tout 114 genres_truc
fig, ax = plt.subplots(figsize=(18, 5))
ax.bar(all_corr.index.astype(str), all_corr.values)
ax.set_title("explicit vs popularité")
ax.set_ylabel("coefficient de corrélation")
ax.set_xticks(range(len(all_corr)))
ax.set_xticklabels(all_corr.index, rotation=90)
plt.tight_layout()
plt.savefig("out/5.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 6/ top 10 farthest from 0
top10 = all_corr.reindex(
    all_corr.abs().sort_values(ascending=False).head(10).index
).sort_values()
# SELECT * FROM all_corr
# ORDER BY ABS(valeur) DESC
# LIMIT 10

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(top10.index.astype(str), top10.values)
ax.set_ylabel("coefficient de corrélation")
ax.set_title("explicit vs popularité le top 10")
ax.set_xticks(range(len(top10)))
ax.set_xticklabels(top10.index, rotation=45, ha="right")
plt.tight_layout()
plt.savefig("out/6.png", dpi=150, bbox_inches="tight")
plt.show()

