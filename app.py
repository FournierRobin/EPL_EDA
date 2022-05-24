from turtle import color
from git import head
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns

# Déclaration des dataframes :
# Classement de l'EPL
classement_pl = pd.read_csv('csv_xl/classement_pl.csv')
classement_pl = classement_pl.drop(columns=['Unnamed: 0'])
classement_pl = classement_pl.set_index('Clt')

# Rapport de scouting des joueurs plus gros joueur de l'EPL
players_stats = pd.read_csv('csv_xl/PL_players_stats_team.csv')
players_stats = players_stats.drop(columns=['Unnamed: 0'])

# WIDE LAYOUT
st.set_page_config(layout="wide")

# CONTAINERS
header = st.container()
dataset = st.container()
graph = st.container()
pair_plot = st.container()
features = st.container()
affichage_test = st.container()

with header:
    st.title("EPL Football EDA : La meilleure équipe est-t-elle toujours celle qui possède les meilleurs joueurs ?")
    st.markdown("Bienvenue dans cette EDA. Nous allons essayer de voir ici si la présence des meilleurs joueurs implique toujours des performances collectives supérieurs")


with dataset:
    st.header("Classement de la Premier League, la ligue Anglaise de Football")
    st.dataframe(classement_pl)

    st.header("Statistiques des joueurs d'EPL / 90min")
    st.dataframe(players_stats)


with graph:
    g_col, r_col = st.columns(2)

    # COLONNE GAUCHE
    # BAR CHART : Répartition des postes
    g_col.subheader("Répartition des postes dans notre dataset")
    val_counts_pos = alt.Chart(players_stats).mark_bar().encode(
        x='Pos',
        y='count()',
        color='Pos',
    )
    text = val_counts_pos.mark_text(
        align='center',
        baseline='bottom',
        dy=-2,
        fontSize=20
    ).encode(
        text='count()'
    )

    val_counts_pos = (val_counts_pos + text).properties(height=400)
    g_col.altair_chart(val_counts_pos, use_container_width=True)
    g_col.markdown(
        "Le plus grand nombre de joueurs présent dans notre dataset sont les defenseurs, avec 159 rapport sur leurs performances, mais étant donné que les performances sont ramenées sur 90min, cela n'aura pas d'impact sur nos statistiques")

    # SCATTER CHART : Goal par poste
    g_col.subheader("Nombre de buts en fonction des positions")
    goals_by_pos = alt.Chart(players_stats).mark_circle(size=100).encode(
        x='Buts (sans les pénaltys)',
        y='Pos',
        color='Pos',
        tooltip=['Buts (sans les pénaltys)',
                 'Joueur', 'Equipe']
    ).properties(
        height=400,
    )
    g_col.altair_chart(goals_by_pos, use_container_width=True)
    g_col.markdown(
        "Comme nous pouvions nous y attendre, on voit ici une large domination des attaquants/milieu dans la répartitions des buts marqués")

    # COLONNE DROITE

    # BAR CHART : Joueurs par équipes
    r_col.subheader("Répartition des joueurs par équipes")
    val_counts_joueurs = alt.Chart(players_stats).mark_bar().encode(
        x='Equipe',
        y='count()',
        color='Equipe',
    )
    text = val_counts_joueurs.mark_text(
        align='center',
        baseline='bottom',
        fontSize=14
    ).encode(
        text='count()'
    )
    val_counts_joueurs = (val_counts_joueurs + text).properties(height=400)
    r_col.altair_chart(val_counts_joueurs, use_container_width=True)
    r_col.markdown("Le nombre de joueurs dont les rapports sont disponibles parmis les 20 équipes varient mais reste aux alentours d'une vingtaine de données disponibles par équipe")

    # SCATTER CHART : Duels aérien par poste
    r_col.subheader("Nombre de duels aérien gagnés en fonction des positions")
    aerien_duels_by_pos = alt.Chart(players_stats).mark_circle(size=100).encode(
        x='Duels aérien gagnés',
        y='Pos',
        color='Pos',
        tooltip=['Duels aérien gagnés',
                 'Joueur', 'Equipe']
    ).properties(
        height=400,
    )
    r_col.altair_chart(aerien_duels_by_pos, use_container_width=True)
    r_col.markdown(
        "Ici, on remarque grace que les Defenseurs ont des statistiques mieux condensés que les autres postes, ainsi malgré les exceptions en attaque, ce sont eux qui dominent ce secteur")


with pair_plot:

    st.subheader("Pair Plot de statistiques des joueurs")

    # PAIR PLOT
    pair_plot = alt.Chart(players_stats).mark_circle().encode(
        alt.X(alt.repeat("column"), type='quantitative'),
        alt.Y(alt.repeat("row"), type='quantitative'),
        color='Pos'
    ).properties(
        width=150,
        height=150
    ).repeat(
        row=['Buts (sans les pénaltys)',
             'Actions menant à un tir', 'npxG+xA', 'Passes décisives'],
        column=['Passes décisives', 'npxG+xA', 'Actions menant à un tir',
                'Buts (sans les pénaltys)']
    )
    st.altair_chart(pair_plot, use_container_width=True)

with features:
    st.header("Features")

    st.markdown("* **1st feature:** First feature I created")
    st.markdown("* **2nd feature:** Second feature I created")

with affichage_test:
    st.header("Graph")

    sel_col, disp_col = st.columns(2)

    max_depth = sel_col.slider('What should be the max_depth of the model ?',
                               min_value=10, max_value=100, value=20, step=10)

    n_estimators = sel_col.selectbox('How manu trees should there be ?', options=[
        100, 200, 300, 'No limit'], index=0)

    input_feature = sel_col.text_input(
        'Which feature should be used as input feature?', 'Équipe')
