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



# Streamlit
# streamlit run ParisPyVelib_Demo.py

st.sidebar.title('Projet ParisPyVelib')
st.sidebar.image('Velib.png')
sommaire = ['Introduction', 'Datasets', 'Evolution Temporelle', 'Cartographie', 'Prédiction du trafic', 'Conclusion et Perspectives']
parties = st.sidebar.radio('', sommaire)


# Introduction
if parties == sommaire[0]:
    st.title('ParisPyVelib')
    st.image('Velib.png')
    st.header('Analyse et prédiction du trafic des vélos de 2018 à 2021 dans la ville de Paris')

# Datasets
if parties == sommaire[1]:
    st.title(parties)
    data = st.radio('', ['Compteurs vélo', 'Données météo', 'Dataset final'])
    if data == 'Compteurs vélo':
        st.header('Description')
        st.markdown('''Dans le but d'avoir des données sur le trafic des vélos sur une période de 2018 à 2021, 
                    au total quatre différents datasets ont été utilisés pour le 
                    comptage horaire qui sont tous disponibles en accès libre par la mairie de Paris.''')
        option = st.selectbox('Sélectionner le dataset', [2018, 2019, 2020, '04/2020 - 05/2021'])
        st.text('Affichage des 5 premières lignes du dataset')
        if option == 2018:
            df = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\2018_comptage-velo-donnees-compteurs.csv', sep = ';')
        if option == 2019:
            df = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\2019_comptage-velo-donnees-compteurs.csv', sep = ';')
        if option == 2020:
            df = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\2020_comptage-velo-donnees-compteurs.csv', sep = ';')
        if option == '04/2020 - 05/2021':
            df = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\New_comptage-velo-donnees-compteurs.csv', sep = ';')
        st.write(df.head())
        st.subheader('Source des données')

# Evolution Temporelle
if parties == sommaire[2]:
    st.title(parties)
        
    # Import du df_hour
    df_hour = pd.read_csv(r'C:\Users\Celine\Desktop\GitHub\ParisPyVelib_Datas\2018-2021_donnees-velib-meteo_hour.csv')
    # Suppression des col inutiles
    df = df_hour.drop(['Date', 'Date_instal', 'Source', 'Direction',
       'Latitude', 'Longitude', 'Coord', 'Y_Date_Instal',
       'M_Date_Instal', 'D_Date_Instal', 'T°C', 'Precip_last3h', 'HR%',
       'High_ice', 'Wind_speed_mean10mn', 'City_meteo', 'Datetime',
       'nom_jour_ferie', 'vacances_zone_c', 'nom_vacances', 'Confinement_id', 'Id'], axis = 1) 
    # Création d'un df par année et par compteurs
    col = ['Y_Date_Count','Address_Dir']
    df_year = df.groupby(col).mean().reset_index()
    # Création d'un df par mois et par compteurs
    col = ['Y_Date_Count','M_Date_Count']
    df_month = df.groupby(col).mean().reset_index()
    df_month['Y_M_Date_Count'] = df_month['Y_Date_Count'].astype(str) + '-' + df_month['M_Date_Count'].astype(str)

    parties = st.radio('', ['I. Evolution du comptage horaire des vélos de 2018 à 2021',
                            'II. Evolution du comptage horaire des vélos par jour',
                            'III. Evolution des top10 et Less10 des compteurs Parisien'])
    
    if parties == 'I. Evolution du comptage horaire des vélos de 2018 à 2021': 
        st.markdown("""De façon général, on peut remarquer que l'utilisation des vélos augmentent au fil des années comme le montre le graphique ci-dessous. 
                En effet, malgré le confinnement strict qu'il y a eu en 2020, la fréquentation a presque doublé de 2018 à 2020. 
                La légère baisse pour 2021 peut s'expliquer par le fait que les données ne sont pas complètes et ne tiennent compte que de la période janvier-mai.""")
        #Affichage de l'évolution des comptages horaires moyen /année
        fig = plt.figure(figsize = (10,4))
        sns.barplot(x = df_year['Y_Date_Count'], y = df_year['Count_by_hour'], color = '#3FE3BD');
        plt.title('Moyenne des comptages horaires par année', fontsize = 15)
        plt.ylabel('Comptages horaires moyen /année')
        plt.xticks(rotation = 90)
        plt.xlabel('')
        st.pyplot(fig)
        
        st.markdown("""Lorsque nous analysons la variable plus en détail, selon les mois de l’année, il
    semble y avoir une différence entre les mois que l’on pourrait qualifier “d'hiver", de novembre à avril,
    et “d'été", de mai à octobre. Dans les premiers, la température est plus fraîche avec de gros
    écarts de température entre la matinée et l’après-midi et les seconds ont une
    température plus douce et homogène. Nous pouvons noter que le mois d’août
    enregistre particulièrement peu de vélos. Cela est synonyme que les parisiens partent
    souvent en vacances durant ce mois, avec une recrudescence à la rentrée. De 2018 à
    2021, nous voyons une tendance en augmentation, du nombre de vélos, avec une coupure lors
    du confinement stricte et une grosse augmentation juste après à la fin de celui-ci.""")
    
        # Affichage linéaire
        fig = plt.figure(figsize = (15,4))
        sns.lineplot(x = df_month['Y_M_Date_Count'], y = df_month['Count_by_hour'], ci=None, marker = True);
        plt.title('Evolution de la fréquentation des vélos par mois', fontsize = 20)
        plt.ylabel('Comptage horaire moyen')
        plt.xticks(rotation = 90)
        plt.xlabel('')
        st.pyplot(fig)
        
        # Affichage barplot
        fig = plt.figure(figsize = (15,4))
        sns.barplot(x = df_month['M_Date_Count'], y = df_month['Count_by_hour'], color = '#3FE3BD');
        plt.title('Evolution de la fréquentation des vélos par mois', fontsize = 20)
        plt.ylabel('Comptages horaires moyen /mois')
        plt.xticks(rotation = 90)
        plt.xlabel('')
        st.pyplot(fig)
    
    if parties == 'II. Evolution du comptage horaire des vélos par jour':
        # Création d'un df par jour de semaine et par compteurs
        col = ['Y_Date_Count','M_Date_Count','Dweek_Date_Count']
        df_day = df.groupby(col).mean().reset_index()
        
        # Affichage barplot du lundi au dimanche
        fig = plt.figure(figsize = (20,4))
        sns.barplot(x = df_day['Dweek_Date_Count'], y = df_day['Count_by_hour'], color = '#3FE3BD');
        plt.title('Evolution de la fréquentation des vélib par jour de semaine', fontsize = 20)
        plt.ylabel('Comptages horaires moyen /jour de semaine')
        plt.xticks(rotation = 90, ticks = [0,1,2,3,4,5,6], labels = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'])
        plt.xlabel('')
        st.pyplot(fig)
        
        # Création d'un df par heures et par compteurs
        col = ['Y_Date_Count','M_Date_Count','Dweek_Date_Count','H_Date_Count']
        df_day = df.groupby(col).mean().reset_index()
        
        # Affichage linéaire par heure et par jour de semaine
        fig = plt.figure(figsize = (20,4))
        sns.lineplot(x = df_day['H_Date_Count'], y = df_day['Count_by_hour'], ci=None, marker = True, hue = df_day['Dweek_Date_Count']);
        plt.title('Evolution de la fréquentation des vélib par heure', fontsize = 20)
        plt.ylabel('Comptage horaire mean')
        plt.xticks(rotation = 90)
        plt.xlabel('')
        plt.legend(['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'])
        st.pyplot(fig)      
    
    if parties == 'III. Evolution des top10 et Less10 des compteurs Parisien':
        st.write('A compléter')
       
# Cartographie
if parties == sommaire[3]:
    st.title(parties)

# Prédiction du trafic    
if parties == sommaire[4]:
    st.title(parties)    

# Conclusion et Perspectives
if parties == sommaire[5]:
    st.title(parties) 