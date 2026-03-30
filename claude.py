import pandas as pd
import numpy as np

df = pd.read_csv('dataset.csv', index_col=0)

# ── 0. Comparaisons de moyennes (effet plus frappant que Pearson r) ────────────
print('=== GROUPES INSTRUMENTALNESS vs POPULARITE ===')
high_instr = df[df['instrumentalness'] > 0.5]['popularity'].mean()
low_instr  = df[df['instrumentalness'] < 0.1]['popularity'].mean()
print(f'Songs instrumentalness > 0.5  → popularité moyenne : {high_instr:.1f}')
print(f'Songs instrumentalness < 0.1  → popularité moyenne : {low_instr:.1f}')
print(f'Différence : {low_instr - high_instr:.1f} points')

print()
print('=== GROUPES ACOUSTICNESS vs POPULARITE ===')
high_ac = df[df['acousticness'] > 0.8]['popularity'].mean()
low_ac  = df[df['acousticness'] < 0.1]['popularity'].mean()
print(f'Songs très acoustiques (>0.8)  → pop moy : {high_ac:.1f}')
print(f'Songs peu acoustiques (<0.1)   → pop moy : {low_ac:.1f}')

print()
print('=== EXPLICIT - différence de moyennes ===')
exp_mean  = df[df['explicit']==True]['popularity'].mean()
nexp_mean = df[df['explicit']==False]['popularity'].mean()
print(f'Explicit=True  → pop moy : {exp_mean:.1f}')
print(f'Explicit=False → pop moy : {nexp_mean:.1f}')
print(f'Différence : {exp_mean - nexp_mean:.1f} points')

# Par genre, corrélation explicit vs popularity
print()
print('=== CORRELATIONS EXPLICIT vs POPULARITY par genre (top 20 abs) ===')
expl_corrs = []
for genre, gdf in df.groupby('track_genre'):
    if gdf['explicit'].nunique() > 1:
        r = gdf['explicit'].astype(int).corr(gdf['popularity'])
        expl_corrs.append((genre, r, len(gdf)))
expl_corrs.sort(key=lambda x: abs(x[1]), reverse=True)
for genre, r, n in expl_corrs[:20]:
    print(f'{genre:22s}  r = {r:+.4f}')

print()
print('=== CORRELATION EXPLICIT vs POPULARITY : genres familiaux vs rap ===')
rap_genres = ['hip-hop','rap','trap','r-n-b']
family_genres = ['kids','classical','acoustic','classical','romance']
for g in rap_genres + family_genres:
    gdf = df[df['track_genre']==g]
    if len(gdf) > 0 and gdf['explicit'].nunique() > 1:
        r = gdf['explicit'].astype(int).corr(gdf['popularity'])
        exp_pop = gdf[gdf['explicit']==True]['popularity'].mean()
        nexp_pop = gdf[gdf['explicit']==False]['popularity'].mean()
        print(f'{g:22s}  r={r:+.4f}  explicit_pop={exp_pop:.1f}  non_explicit_pop={nexp_pop:.1f}')

print()


numeric_cols = ['popularity','danceability','energy','loudness','speechiness',
                'acousticness','instrumentalness','liveness','valence','tempo','duration_ms']
features = [c for c in numeric_cols if c != 'popularity']

genre_agg = df.groupby('track_genre')[numeric_cols].mean()

# ── 1. Corrélations globales vs popularity ─────────────────────────────────────
print('=== CORRELATIONS vs POPULARITY — niveau CHANSON (global) ===')
corr_song = df[numeric_cols].corr()['popularity'].drop('popularity').sort_values(key=abs, ascending=False)
for col, val in corr_song.items():
    print(f'{col:22s}  r = {val:+.4f}')

print()
print('=== CORRELATIONS vs POPULARITY — niveau GENRE (114 points) ===')
corr_genre = genre_agg.corr()['popularity'].drop('popularity').sort_values(key=abs, ascending=False)
for col, val in corr_genre.items():
    print(f'{col:22s}  r = {val:+.4f}')

# ── 2. Corrélations WITHIN chaque genre (moyenne des r par feature) ────────────
print()
print('=== CORRELATIONS vs POPULARITY — moyenne INTRA-GENRE ===')
within_corrs = {}
for feat in features:
    rs = []
    for genre, gdf in df.groupby('track_genre'):
        if len(gdf) > 10:
            r = gdf[feat].corr(gdf['popularity'])
            if not np.isnan(r):
                rs.append(r)
    within_corrs[feat] = np.mean(rs)

within_sorted = sorted(within_corrs.items(), key=lambda x: abs(x[1]), reverse=True)
for feat, val in within_sorted:
    print(f'{feat:22s}  r_moyen = {val:+.4f}')

# ── 3. Cherche les paradoxes : features où le signe change entre niveaux ───────
print()
print('=== PARADOXES POTENTIELS (signe inversé entre niveaux) ===')
print(f'{"Feature":22s}  {"Song-level":>12}  {"Genre-level":>12}  {"Intra-genre":>12}  PARADOXE?')
print('-' * 75)
for feat in features:
    r_song  = corr_song[feat]
    r_genre = corr_genre[feat]
    r_intra = within_corrs[feat]
    paradox = ''
    if (r_song > 0) != (r_genre > 0): paradox += 'song↔genre '
    if (r_song > 0) != (r_intra > 0): paradox += 'song↔intra '
    if (r_genre > 0) != (r_intra > 0): paradox += 'genre↔intra'
    print(f'{feat:22s}  {r_song:+.4f}      {r_genre:+.4f}      {r_intra:+.4f}      {paradox}')

# ── 4. Explicit content ────────────────────────────────────────────────────────
print()
print('=== EXPLICIT vs POPULARITY ===')
print(df.groupby('explicit')['popularity'].agg(['mean','median','count']).round(2).to_string())

# explicit par genre top/bottom
print()
print('=== TOP 10 genres (popularité) avec % explicit ===')
top10 = genre_agg.sort_values('popularity', ascending=False).head(10)[['popularity','energy','danceability','valence','instrumentalness']]
expl_rate = df.groupby('track_genre')['explicit'].apply(lambda x: (x=='True').mean() if x.dtype==object else x.mean())
top10['explicit_%'] = expl_rate
print(top10.round(3).to_string())

print()
print('=== BOTTOM 10 genres (popularité) ===')
bot10 = genre_agg.sort_values('popularity').head(10)[['popularity','energy','danceability','valence','instrumentalness']]
bot10['explicit_%'] = expl_rate
print(bot10.round(3).to_string())
