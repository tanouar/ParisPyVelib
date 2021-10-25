# Import library:
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Récupération du répertoire courant
currentPath = os.getcwd()
print('Current path : ', currentPath)

# Définition du répertoire contenant les données
datasPath = currentPath + '\\' + 'Datas'
print('Set path with datas : ', datasPath)


# Définition du chemin d'accès des datasets sources
dataset_2018_comptage_velo_donnees_compteurs = datasPath + '\\' + '2018_comptage-velo-donnees-compteurs.csv'
dataset_2019_comptage_velo_donnees_compteurs = datasPath + '\\' + '2019_comptage-velo-donnees-compteurs.csv'
dataset_2020_comptage_velo_donnees_compteurs = datasPath + '\\' + '2020_comptage-velo-donnees-compteurs.csv'
dataset_New_comptage_velo_donnees_compteurs = datasPath + '\\' + 'New_comptage-velo-donnees-compteurs.csv'

# Définition du chemin d'accès du dataset final
dataset_2018_2021_donnees_velib_meteo_hour = datasPath + '\\' + '2018-2021_donnees-velib-meteo_hour.csv'




# Streamlit
# streamlit run ParisPyVelib_Demo.py

st.sidebar.title('Projet ParisPyVelib')
st.sidebar.image('Velib.png')
sommaire = ['Introduction', 'Datasets', 'Evolution Temporelle', 'Cartographie', 'Prédiction du trafic', 'Conclusion et Perspectives']
parties = st.sidebar.radio('', sommaire)


# Introduction
lien_compteur_2021 = """"""
lien_autres_compteurs = """"""

if parties == sommaire[0]:
    st.title('ParisPyVelib')
    st.image('Velib.png')
    st.header('Analyse et prédiction du trafic des vélos de 2018 à 2021 dans la ville de Paris')
    st.markdown('''Projet réalisé par... en tant que projet fil-rouge de la formation de Data Analyst de DataScientest...
                ''')
    st.markdown('''<p style='text-align: justify'>
                Un peu partout dans Paris, des totems bleus sont placés le long des grandes artères. Ces bornes, servent à comptabiliser 
                chaque jour le nombre de cyclistes, par heure à divers endroits de la ville, le plus souvent dans les deux sens de circulation.
                </p>''',  unsafe_allow_html=True)
    st.markdown('''<p style='text-align: justify'>
                Les données générées, sont disponibles sur le site opendata de la mairie de Paris  
                sous forme de plusieurs datasets entre 2018 et aujourd'hui.</p>''',  unsafe_allow_html=True)
    st.markdown('''<p style='text-align: justify'>Ainsi, notre projet est d'utiliser ces données, dans un premier temps, pour analyser la circulation des vélos dans Paris 
                et l'impact de plusieurs facteurs comme la météo, les vacances ou bien les jours fériés. Dans second temps, l'objectif est d'utiliser les algorithme de 
                Machine Learning pour prédir le comportement des utilisateurs.</p>''',  unsafe_allow_html=True)
    st.markdown('''<p style='text-align: justify'>
               La problématique exploitée dans ce rapport a déjà fait l’objet d’un
               <a href="https://studio.datascientest.com/project/pycycle/">
               projet</a>
               mené par d'autres apprenants dans le cadre d’un bootcamp Data Analyst sur une plus petite période et avec une 
               orientation d'avantage centrée sur l'influence des accidents sur les vélos.
               Un autre
               <a href="https://www.apur.org/fr/nos-travaux/evolution-mobilites-grand-paris-tendances-historiques-evolutions-cours-emergentes">
               rapport</a>
               beaucoup plus complet qui étudie l’évolution de la mobilité de tous les modes de transport de 1976 à 2020 dans le Grand Paris 
               (vélo, pieds, voiture, transport en commun…) a permis d’avoir une vision plus globale du projet et de toutes les études pouvant
               être réalisées dans cette même thématique.
               </p>''',  unsafe_allow_html=True)

   
# Datasets
if parties == sommaire[1]:
    st.title(parties)
    st.header('Description')
    st.markdown('''<p style='text-align: justify'>
                Plusieurs jeux de données ont été utilisés au cours du projet. Tout d’abord, comme expliqué en introduction,  
                nous avons récupéré du site opendata Paris les données des compteurs de vélos de 2018 à 2021. Un autre jeu de données majeur de notre projet concerne
                les données météos. Enfin, différents jeux de données sur les dates de vacances scolaires, les jours fériés, les dates du confinement
                aussi en open data ont permis de compléter nos analyses.
                L'agrégation de toutes les données donne lieux à un dataset final qui servira par la suite à l'analyse de notre variable cible et à sa prédiction.
                </p>''',  unsafe_allow_html=True)
                
    data = st.radio('', ['Compteurs vélo', 'Données météo', 'Dataset final'])

    if data == 'Compteurs vélo':
        st.header('Description')
        st.markdown('''<p style='text-align: justify'>
                    Dans le but d'avoir des données sur le trafic des vélos sur une période de 2018 à 2021 (voir
                    <a href="https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name">
                    ici en 2021</a>
                    et <a href="https://opendata.paris.fr/explore/dataset/comptage-velo-historique-donnees-compteurs/information/">
                    ici les autres années</a>). 
                    Au total quatre datasets ont été utilisés pour le comptage horaire. Lorsque nous le concaténons, le dataframe résultant compte 
                    un peu moins de 2 millions de lignes avec 9 colonnes au total sur une période du 1er janvier 2018 au 1er mai 2021.
                    </p>''',  unsafe_allow_html=True)
        option = st.selectbox('Sélectionner le dataset', [2018, 2019, 2020, 2021])
        st.text('Affichage des 5 premières lignes du dataset')
        if option == 2018:
            df = pd.read_csv(dataset_2018_comptage_velo_donnees_compteurs , sep = ';')
        if option == 2019:
            df = pd.read_csv(dataset_2019_comptage_velo_donnees_compteurs, sep = ';')
        if option == 2020:
            df = pd.read_csv(dataset_2020_comptage_velo_donnees_compteurs, sep = ';')
        if option == 2021:
            df = pd.read_csv(dataset_New_comptage_velo_donnees_compteurs, sep = ';')
        st.write(df.head())
        st.header('Preprocessing')
        st.markdown('''<p style='text-align: justify'>
                    Tout d'abord,  il a été nécessaire de
bien homogénéiser les données'
                    </p>''',  unsafe_allow_html=True)
        
    
    if data == 'Données météo':
        st.header('Description')
        st.markdown('''<p style='text-align: justify'>
                    Nous avons opté pour un site permettant un accès libre sur toutes les données météos provenant de la ville d'Athis-Mons (91),
                    seul compteur disponible en île-de-France. Cela correspond, après sélection de 2018 à 2021,(même période que pour les compteurs vélib) 
                    à un dataframe de 9944 rows × 82 columns. Celui-ci a ensuite été réduit, par la suite, pour ne sélectionner que les données intéressantes.
                  </p>''',  unsafe_allow_html=True) 

    if data == 'Dataset final':
        st.header('Description')
        st.markdown('''<p style='text-align: justify'>
                    
                    </p>''',  unsafe_allow_html=True)

# Evolution Temporelle
if parties == sommaire[2]:
    st.title(parties)
        
    # Import du df_hour
    df_hour = pd.read_csv(dataset_2018_2021_donnees_velib_meteo_hour)
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
        st.write("""De façon général, on peut remarquer que l'utilisation des vélos augmente au fil des années comme le montre le graphique ci-dessous. 
                En effet, malgré le confinement strict qu'il y a eu en 2020, la fréquentation a presque doublé de 2018 à 2020. 
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

    st.header('Observation de la target')
    # st.subheader('Observation de la cible')
      
    
    st.markdown("""Selectionner le compteur qui comptabilise le plus de passage afin d'observer 
                l'évolution de la variable *Count_by_hour* pendant une journée. 
                L'objectif est de determiner si la variable *Count_by_hour* suit une distribution 
                probabilistique connue.""")
    
   

# Conclusion et Perspectives
if parties == sommaire[5]:
    st.title(parties) 