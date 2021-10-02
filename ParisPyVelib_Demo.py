# Import library:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Définition du chemin d'accès:
### Data Scientest:
#%cd Datas
### Céline:
#%C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas
### Hermine:
#%cd C:\Users\h.berthon\Documents\GitHub\ParisPyVelibHB\ParisPyVelib_Datas
### Tarik:
#%cd C:\Users\Home\Documents\Git\ParisPyVelib\Data

# Import df_hour
df = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\New_comptage-velo-donnees-compteurs.csv', sep = ';')
df.head()

# Streamlit

st.sidebar.title('Projet ParisPyVelib')
sommaire = ['Introduction', 'Datasets', 'Evolution Temporelle', 'Cartographie', 'Prédiction du trafic', 'Conclusion et Perspectives']
parties = st.sidebar.radio('', sommaire)


# Introduction
if parties == sommaire[0]:
    st.title('ParisPyVelib')
    st.header('Analyse et prédiction du trafic des vélos de 2018 à 2021 dans la ville de Paris')

# Datasets
if parties == sommaire[1]:
    st.title(parties)
    data = st.radio('', ['Compteurs vélo', 'Données météo', 'Dataset final'])
    if data == 'Compteurs vélo':
        st.header('Description')
        st.text('''Dans le but d'avoir des données sur le trafic des vélos sur une période 
                de 2018 à 2021, au total quatre différents datasets ont été utilisés pour le 
                comptage horaire qui sont tous disponibles en accès libre par la mairie de Paris''')
        option = st.selectbox('Sélectionner le dataset', [2018, 2019, 2020, 2021])
        st.text('Affichage des 5 premières lignes du dataset')
        st.write(df.head())

# Evolution Temporelle
if parties == sommaire[2]:
    st.title(parties)

    
# Cartographie
if parties == sommaire[3]:
    st.title(parties)

# Prédiction du trafic    
if parties == sommaire[4]:
    st.title(parties)    

# Conclusion et Perspectives
if parties == sommaire[5]:
    st.title(parties) 