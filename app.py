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
classement_pl = classement_pl.rename(columns={"Équipe": "Equipe"})

# Rapport de scouting des joueurs plus gros joueur de l'EPL
players_stats = pd.read_csv('csv_xl/PL_players_stats_team.csv')
players_stats = players_stats.drop(columns=['Unnamed: 0'])

# Statistiques des gardiens par équipe
keepers_stats = pd.read_csv('csv_xl/keepers_stats.csv')
keepers_stats = keepers_stats.drop(columns=['Unnamed: 0'])
keepers_stats = keepers_stats.rename(
    columns={"Équipe": "Equipe", "BE": "Keepers_BE"})
# Dataframe merge classement x players
players_stats_classement = classement_pl[["Clt", "Equipe",	"MJ", "V", "N",	"D", "BM", "BE", "DB", "Pts"]].merge(
    players_stats, how='left', on='Equipe')

# Dataframe merge classement x keepers
keepers_stats_classement = classement_pl[["Clt", "Equipe",	"MJ", "BM", "BE", "DB", "Pts"]].merge(
    keepers_stats, how='left', on='Equipe')


# WIDE LAYOUT
st.set_page_config(layout="wide")

# CONTAINERS
header = st.container()
dataset_classement = st.container()
dataset_players_keepers = st.container()
distribution = st.container()
perf_players = st.container()
pair_plot = st.container()
list_plot = st.container()
keepers_plot = st.container()

with header:
    st.title("EPL Football EDA : La meilleure équipe est-t-elle toujours celle qui possède les meilleurs joueurs ?")
    st.markdown("Bienvenue dans cette EDA. Nous allons essayer de voir ici si la présence des meilleurs joueurs implique toujours des performances collectives supérieurs")


with dataset_classement:
    st.header("Presentation des datasets")
    st.subheader(
        "Classement de la Premier League, la ligue Anglaise de Football")
    st.dataframe(
        classement_pl[["Equipe", "MJ", "Pts", "V", "N", "D", "BM", "BE"]])
    st.title("")

with dataset_players_keepers:
    players_col, keepers_col = st.columns(2)

    players_col.subheader("Statistiques des joueurs d'EPL (90min)")
    players_col.dataframe(players_stats)
    players_col.title("")

    keepers_col.subheader("Statistiques des gardiens d'EPL")
    keepers_col.dataframe(keepers_stats)
    keepers_col.title("")


with distribution:
    st.header("Distribution")
    g_col, r_col = st.columns(2)
    # COLONNE GAUCHE

    # BAR CHART : Répartition des postes
    g_col.subheader("Répartition des postes dans notre dataset")
    g_col.title("")
    val_counts_pos = alt.Chart(players_stats).mark_bar().encode(
        x='Pos',
        y='count()',
        color=alt.Color('Pos', legend=None),

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
        "Le plus grand nombre de joueurs présent dans notre dataset sont les defenseurs, avec 159 rapport sur leurs performances, mais étant donné que les performances sont ramenées sur 90min, aucun impact sur nos statistiques")
    g_col.title("")

    # COLONNE DROITE

    # BAR CHART : Joueurs par équipes
    r_col.subheader("Répartition des joueurs par équipes")
    r_col.title("")

    val_counts_joueurs = alt.Chart(players_stats).mark_bar().encode(
        x='Equipe',
        y='count()',
        color=alt.Color('Equipe', legend=None),
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
    r_col.title("")

with perf_players:
    st.header("Performances des joueurs de champs")

    g_col, r_col = st.columns(2)

    # COLONNE GAUCHE

    # SCATTER CHART : Goal par poste
    g_col.subheader("Nombre de buts en fonction des positions")
    g_col.title("")

    goals_by_pos = alt.Chart(players_stats).mark_circle(size=100).encode(
        x='Buts (sans les pénaltys)',
        y='Pos',
        color=alt.Color('Pos', legend=None),
        tooltip=['Buts (sans les pénaltys)',
                 'Joueur', 'Equipe']
    ).properties(
        height=400,
    )
    g_col.altair_chart(goals_by_pos, use_container_width=True)
    g_col.markdown(
        "Comme nous pouvions nous y attendre, on voit ici une large domination des attaquants/milieu dans la répartitions des buts marqués")
    g_col.title("")

    # COLONNE DROITE

    # SCATTER CHART : Duels aérien par poste
    r_col.subheader("Nombre de duels aérien gagnés en fonction des positions")
    r_col.title("")
    aerien_duels_by_pos = alt.Chart(players_stats).mark_circle(size=100).encode(
        x='Duels aérien gagnés',
        y='Pos',
        color=alt.Color('Pos', legend=None),
        tooltip=['Duels aérien gagnés',
                 'Joueur', 'Equipe']
    ).properties(
        height=400,
    )
    r_col.altair_chart(aerien_duels_by_pos, use_container_width=True)
    r_col.markdown(
        "Ici, on remarque grace que les Defenseurs ont des statistiques mieux condensés que les autres postes, ainsi malgré les exceptions en attaque, ce sont eux qui dominent ce secteur")
    r_col.title("")


with pair_plot:

    c1, c2 = st.columns((3, 2))
    m1, m2, m3 = st.columns((3, 1, 1))

    c1.subheader("En fonction des postes")
    c1.markdown(
        "Pair plot des statistiques de joueurs en fonction de leur poste")

    # PAIR PLOT
    pair_plot = alt.Chart(players_stats).mark_circle().encode(
        alt.X(alt.repeat("column"), type='quantitative'),
        alt.Y(alt.repeat("row"), type='quantitative'),
        color='Pos'
    ).properties(
        width=200,
        height=200
    ).repeat(
        row=['Buts (sans les pénaltys)'],
        column=['Passes décisives', 'npxG+xA', 'Actions menant à un tir']
    )
    m1.altair_chart(pair_plot, use_container_width=True)
    m1.caption(
        "On peut remarque ici que pour un nombre équivalent de passes décisives, les AT et AT/MT sont bien plus efficaces devant le but")

    c2.subheader("Quelques chiffres importants")
    # Première ligne
    m2.metric(label='Maximum de Points',
              value=classement_pl['Pts'][1])
    m3.metric(label='Maximum de Buts marqués par une équipe',
              value=classement_pl['BM'][1])

    # Seconde ligne
    m2.metric(label='Joueur avec le plus de buts marqués',
              value=players_stats['Joueur'][players_stats['Buts (sans les pénaltys)'].idxmax()])
    m3.metric(label='Equipe du joueur avec le plus de buts marqués',
              value=players_stats['Equipe'][players_stats['Buts (sans les pénaltys)'].idxmax()])

with list_plot:

    st.subheader("En fonction des points")
    st.markdown(
        "Statistiques des joueurs en fonction de leur équipe, trié par nombre de points")

    B_PD_xG_pts = alt.Chart(players_stats_classement).mark_circle().encode(
        alt.X(alt.repeat("column"), type='quantitative'),
        alt.Y(alt.repeat("row"), type='quantitative'),
        color='Equipe'
    ).properties(
        width=300,
        height=300
    ).repeat(
        row=['Pts'],
        column=['Passes décisives', 'npxG+xA', 'Buts (sans les pénaltys)']
    )
    st.altair_chart(B_PD_xG_pts, use_container_width=True)

with keepers_plot:
    st.header("Performance & Impact des gardiens")

    keep_g, keep_r = st.columns(2)

    # COLONNE GAUCHE
    keep_g.subheader("Nombre d'arrêts par équipe")

    bars = alt.Chart(keepers_stats_classement).mark_bar().encode(
        x=alt.X('Equipe', sort='y'),
        y='Arrêts',
        color=alt.Color('Equipe', legend=None),
        tooltip=['BE', 'TCC', 'Arrêts%']
    ).properties(
        height=400,
    )

    text = bars.mark_text(
        align='center',
        baseline='middle',
        dy=-10
    ).encode(
        text='Clt'
    )

    keep_save_nb = (bars + text).properties(height=600)
    keep_g.altair_chart(keep_save_nb, use_container_width=True)

    # COLONNE DROITE
    keep_r.subheader("Pourcentage d'arrêts par équipe")

    bars = alt.Chart(keepers_stats_classement).mark_bar().encode(
        x=alt.X('Equipe', sort='-y'),
        y='Arrêts%',
        color=alt.Color('Equipe', legend=None),
        tooltip=['BE', 'TCC', 'Arrêts']
    ).properties(
        height=400,
    )

    text = bars.mark_text(
        align='center',
        baseline='middle',
        dy=-10
    ).encode(
        text='Clt'
    )

    keep_save_pourcent = (bars + text).properties(height=600)
    keep_r.altair_chart(keep_save_pourcent, use_container_width=True)
