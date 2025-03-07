# Importando pacotes necessários
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Carregando o conjunto de dados
dados = pd.read_csv('English Premier League.csv')
dados.head(10)

# Explorando os dados
dados.columns
dados.shape
dados.describe()

# Convertendo a coluna de data para formato datetime
dados['Date'] = pd.to_datetime(dados['Date'], format='%d/%m/%Y', errors='coerce')

# Filtrando os dados a partir de agosto de 2020 (Considerando as temporadas 2021-2023)
dados_filtrados = dados[dados['Date'] >= '2020-08-01'].copy()

# Removendo coluna desnecessária
if 'League' in dados_filtrados.columns:
    del dados_filtrados['League']

# Desempenho dos times dentro e fora de casa 
df_casa = dados_filtrados.groupby('HomeTeam').agg(
    Games=('HomeTeam', 'count'),
    GoalsScored=('HomeGoals', 'sum'),
    GoalsConceded=('AwayGoals', 'sum'),
    Wins=('Result', lambda x: (x == 'H').sum()),
    Draws=('Result', lambda x: (x == 'D').sum())
) 
df_casa['Losses'] = df_casa['Games'] - df_casa['Wins'] - df_casa['Draws']

df_fora = dados_filtrados.groupby('AwayTeam').agg(
    Games=('AwayTeam', 'count'),
    GoalsScored=('AwayGoals', 'sum'),
    GoalsConceded=('HomeGoals', 'sum'),
    Wins=('Result', lambda x: (x == 'A').sum()),
    Draws=('Result', lambda x: (x == 'D').sum())
) 
df_fora['Losses'] = df_fora['Games'] - df_fora['Wins'] - df_fora['Draws']

# Unindo os DataFrames
df_performance = pd.merge(df_casa, df_fora, left_index=True, right_index=True,
                          suffixes=('_Casa', '_Fora'), how='outer').fillna(0)

# Cálculos dos totais de jogos e gols marcados dentro de casa e fora de casa. 
df_performance['TotalGames'] = df_performance['Games_Casa'] + df_performance['Games_Fora']
df_performance['TotalGoalsScored'] = df_performance['GoalsScored_Casa'] + df_performance['GoalsScored_Fora']
df_performance['TotalGoalsConceded'] = df_performance['GoalsConceded_Casa'] + df_performance['GoalsConceded_Fora']

# Cálculo dos totais de vitórias, empates e derrotas
df_performance['TotalWins'] = df_performance['Wins_Casa'] + df_performance['Wins_Fora']
df_performance['TotalDraws'] = df_performance['Draws_Casa'] + df_performance['Draws_Fora']
df_performance['TotalLosses'] = df_performance['Losses_Casa'] + df_performance['Losses_Fora']

# Cálculo das porcentagens de vitórias, derrotas e empates em casa
df_performance['% Victory_Casa'] = (df_performance['Wins_Casa'] / df_performance['Games_Casa']) * 100
df_performance['% Losses_Casa'] = (df_performance['Losses_Casa'] / df_performance['Games_Casa']) * 100
df_performance['% Draws_Casa'] = (df_performance['Draws_Casa'] / df_performance['Games_Casa']) * 100

# Cálculo das porcentagens de vitórias, derrotas e empates fora de casa
df_performance['% Victory_Fora'] = (df_performance['Wins_Fora'] / df_performance['Games_Fora']) * 100
df_performance['% Losses_Fora'] = (df_performance['Losses_Fora'] / df_performance['Games_Fora']) * 100
df_performance['% Draws_Fora'] = (df_performance['Draws_Fora'] / df_performance['Games_Fora']) * 100

# Cálculos das porcentagens de vitórias, empates e derrotas no geral
df_performance['% Victory_Total'] = (df_performance['TotalWins'] / df_performance['TotalGames']) * 100
df_performance['% Losses_Total'] = (df_performance['TotalLosses'] / df_performance['TotalGames']) * 100
df_performance['% Draws_Total'] = (df_performance['TotalDraws'] / df_performance['TotalGames']) * 100

# Colunas do novo DataFrame
df_performance.columns
df_performance.shape

# Verificação de valores nulos após cálculos
df_performance.isnull().sum()

# Exibindo as primeiras 25 linhas do DataFrame
print(f"Desempenho total dos times (2021-2023): \n{df_performance.head(25)}")

# ----------------------------------------------------------------------------
# Relação entre gols marcados e % de vitórias em jogos dentro de casa
times = df_performance.index.tolist()
gols_casa = df_performance['GoalsScored_Casa'].tolist()
perc_vitorias_casa = df_performance['% Victory_Casa'].tolist()

plt.figure(figsize=(8, 5))
plt.scatter(gols_casa, perc_vitorias_casa, color='blue', s=100, edgecolors='black')

texts_casa = []
for i, time in enumerate(times):
    texts_casa.append(plt.text(gols_casa[i], perc_vitorias_casa[i], time, fontsize=12))

adjust_text(texts_casa, arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

plt.xlabel("Gols Marcados")
plt.ylabel("Porcentagem de Vitórias (%)")
plt.title("Relação entre Gols Marcados e % de Vitórias em Casa")
plt.grid(True)
plt.show()

# ----------------------------------------------------------------------------
# Relação entre gols marcados e % de vitórias em jogos fora de casa
times = df_performance.index.tolist()
gols_fora = df_performance['GoalsScored_Fora'].tolist()
perc_vitorias_fora = df_performance['% Victory_Fora'].tolist()

plt.figure(figsize=(8, 5))
plt.scatter(gols_fora, perc_vitorias_fora, color='red', s=100, edgecolors='black')

texts_fora = []
for i, time in enumerate(times):
    texts_fora.append(plt.text(gols_fora[i], perc_vitorias_fora[i], time, fontsize=12))

adjust_text(texts_fora, arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

plt.xlabel("Gols Marcados")
plt.ylabel("Porcentagem de Vitórias (%)")
plt.title("Relação entre Gols Marcados e % de Vitórias Fora de Casa")
plt.grid(True)
plt.show()

# ----------------------------------------------------------------------------
# Ranking dos times que mais marcaram gols no período
df_gols_marcados = df_performance[['TotalGoalsScored']].copy()
df_gols_marcados = df_gols_marcados.sort_values(by='TotalGoalsScored', ascending=False)

times = df_gols_marcados.index

plt.figure(figsize=(12, 6))
plt.bar(times, df_gols_marcados['TotalGoalsScored'], color='royalblue', edgecolor='black')
plt.xlabel('Times')
plt.ylabel('Quantidade de Gols')
plt.title('Total de Gols Marcados por Cada Time na Premier League (2021-2023)')
plt.xticks(rotation=60)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
