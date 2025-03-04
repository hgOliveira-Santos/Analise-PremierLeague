# Importando pacotes necessários
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregando o conjunto de dados
dados = pd.read_csv('English Premier League.csv')
dados.head(10)

# Análise Exploratória 
dados.columns
dados.shape
dados.describe()

# Filtrando o intervalo desejado -> 2021-2023
# Observações:
    # Início das temporadas europeias: segundo semestre do ano X 
    # Fim das temporadas europeias: primeiro semestre do ano X + 1
# Com isso, se faz necessário considerar os dados do segundo sementre de 2020
dados['Date'] = pd.to_datetime(dados['Date'], format='%d/%m/%Y', errors='coerce')

# Filtrando os dados a partir de agosto de 2020
dados_filtrados = dados[dados['Date'] >= '2020/08/01']
dados_filtrados.head(10)

dados_filtrados.shape # 1140 registros no período de agosto de 2020 até maio de 2023

# Removendo a coluna 'League'
del dados_filtrados['League']

dados_filtrados.head(10)
dados_filtrados.tail(10)

# Desempenho dos times dentro e fora de casa
# Desempenho dentro de casa
performance_casa = dados_filtrados.groupby('HomeTeam').agg({
    'HomeGoals': 'sum',
    'AwayGoals': 'sum',
    'Result': lambda x: (x == 'H').sum(),
    'HomeTeam': 'count'
}).rename(columns={'HomeGoals': 'GoalsScored', 
                   'AwayGoals': 'GoalsConceded',
                   'Result': 'Wins',
                   'HomeTeam': 'Games'})

performance_casa['% Victory'] = (performance_casa['Wins'] / performance_casa['Games']) * 100
print(f"Desempenho em casa (primeiras 25 linhas): \n{performance_casa.head(25)}")

# Desempenho fora de casa
performance_fora = dados_filtrados.groupby('AwayTeam').agg({
    'AwayGoals': 'sum',
    'HomeGoals': 'sum', 
    'Result': lambda x: (x == 'H').sum(),
    'AwayTeam': 'count'
}).rename(columns={'AwayGoals': 'GoalsScored', 
                   'HomeGoals': 'GoalsConceded',
                   'Result': 'Wins',
                   'AwayTeam': 'Games'})

performance_fora['% Victory'] = (performance_fora['Wins'] / performance_fora['Games']) * 100
print(f"Desempenho fora de casa (primeiras 25 linhas): \n{performance_fora.head(25)}")

# ---------------------------------------------------------
# Relação entre gols marcados e % de vitórias em casa
times_casa = performance_casa.index.tolist()
gols_casa = performance_casa['GoalsScored'].tolist()
perc_vitoria_casa = performance_casa['% Victory'].tolist()

plt.figure(figsize=(8, 5))
plt.scatter(gols_casa, perc_vitoria_casa, color='blue', s=100, edgecolors='black')

texts_casa = []
for i, time in enumerate(times_casa):
    texts_casa.append(plt.text(gols_casa[i], perc_vitoria_casa[i], time, fontsize=12))

adjust_text(texts_casa, arrowprops=dict(arrowstyle="->", color='black', lw=0.8))

plt.xlabel("Gols Marcados")
plt.ylabel("Porcentagem de Vitórias (%)")
plt.title("Relação entre Gols Marcados e % de Vitórias em Casa")
plt.grid(True)
plt.show()

# ---------------------------------------------------------
# Relação entre gols marcados e % de vitórias fora de casa
times_fora = performance_fora.index.tolist()
gols_fora = performance_fora['GoalsScored'].tolist()
perc_vitoria_fora = performance_fora['% Victory'].tolist()

plt.figure(figsize=(8, 5))
plt.scatter(gols_fora, perc_vitoria_fora, color='red', s=100, edgecolors='black')

texts_fora = []
for i, time in enumerate(times_fora):
    texts_fora.append(plt.text(gols_fora[i], perc_vitoria_fora[i], time, fontsize=12))

adjust_text(texts_fora, arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

plt.xlabel("Gols Marcados")
plt.ylabel("Porcentagem de Vitórias (%)")
plt.title("Relação entre Gols Marcados e % de Vitórias Fora de Casa")
plt.grid(True)
plt.show()

# ---------------------------------------------------------



