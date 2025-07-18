#!/usr/bin/env python3
"""Genera mapa de calor de coincidencia de mayorías entre Diputados y Senado por provincia."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).parent.parent
dep_df = pd.read_csv(BASE / 'data' / 'diputados.csv')
sen_df = pd.read_csv(BASE / 'data' / 'senadores.csv')

def norm_vote(v):
    v = str(v).strip().upper()
    if v.startswith('AFIRM'):
        return 'AFIRMATIVO'
    if v.startswith('NEGAT'):
        return 'NEGATIVO'
    if v.startswith('ABST'):
        return 'ABSTENCION'
    return 'OTRO'

dep_df['vote_norm'] = dep_df['voto'].apply(norm_vote)
sen_df['vote_norm'] = sen_df['voto'].apply(norm_vote)

dep_maj = dep_df.groupby('provincia')['vote_norm'].agg(lambda x: x.value_counts().idxmax())
sen_maj = sen_df.groupby('provincia')['vote_norm'].agg(lambda x: x.value_counts().idxmax())

compare = pd.DataFrame({
    'Diputados': dep_maj,
    'Senadores': sen_maj
})
compare['Coinciden'] = compare['Diputados'] == compare['Senadores']
compare.to_csv(BASE / 'outputs' / 'coincidencia_provincia.csv')

# Heatmap
vals = compare['Coinciden'].astype(int).values.reshape(-1, 1)
plt.figure(figsize=(4, len(compare)/3))
plt.imshow(vals, aspect='auto', cmap='viridis', vmin=0, vmax=1)
plt.yticks(range(len(compare.index)), compare.index)
plt.xticks([0], ['Coinciden'])
plt.colorbar(label='1 = coinciden, 0 = no coinciden')
plt.tight_layout()
plt.savefig(BASE / 'outputs' / 'heatmap.png', dpi=300)
print('Generado outputs/coincidencia_provincia.csv y outputs/heatmap.png')
