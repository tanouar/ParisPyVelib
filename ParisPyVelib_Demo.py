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
sommaire = ['Introduction', 'Datasets', 'Evolution Temporelle', 'Prédiction du trafic', 'Conclusion et Perspectives']
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
            df = pd.read_csv(dataset_2018_comptage_velo_donnees_compteurs , sep = ';')
        if option == 2019:
            df = pd.read_csv(dataset_2019_comptage_velo_donnees_compteurs, sep = ';')
        if option == 2020:
            df = pd.read_csv(dataset_2020_comptage_velo_donnees_compteurs, sep = ';')
        if option == '04/2020 - 05/2021':
            df = pd.read_csv(dataset_New_comptage_velo_donnees_compteurs, sep = ';')
        st.write(df.head())
        st.subheader('Source des données')

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
       'nom_jour_ferie', 'vacances_zone_c', 'nom_vacances', 'Confinement_id', 'Id','Unnamed: 0'], axis = 1) 
    # Création d'un df par année et par compteurs
    col = ['Y_Date_Count','Address', 'Address_Dir']
    df_year = df.groupby(col).mean().reset_index()
    # Création d'un df par mois et par compteurs
    col = ['Y_Date_Count','M_Date_Count']
    df_month = df.groupby(col).mean().reset_index()
    df_month['Y_M_Date_Count'] = df_month['Y_Date_Count'].astype(str) + '-' + df_month['M_Date_Count'].astype(str)

    parties = st.radio('', ['I. Evolution du comptage horaire des vélos de 2018 à 2021',
                            'II. Evolution du comptage horaire des vélos par jour',
                            'III. Classement des compteurs Parisien'])
    
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
        
        st.markdown("""L’utilisation des vélos est principalement utilisée en tant que mode de transport pour le trajet domicile-travail. En effet, on peut remarquer sur les graphiques ci-dessous une différence notable entre la semaine et les weekends. """)
        
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
    
        st.markdown("""En semaine, la fréquentation est plus intense que les weekends. Deux pics de circulation sont présents le matin et l'après-midi, correspondant aux heures de pointe du travail. Les deux pics ayant une allure quasi identique, cela pourrait montrer que ce sont les mêmes cyclistes à l’aller et au retour de leur trajet domicile-travail.   

Le weekend, la distribution est plus dispersée tout au long de la journée, avec une gaussienne plus aplatie. Nous avons remarqué également que les jours fériés se comportent comme les weekends.
""")
    
    if parties == 'III. Classement des compteurs Parisien':
        st.markdown("""""")
        
        annee = st.selectbox("""Sélectionner l'année""", [2018, 2019, 2020, 2021])
        df2 = df_year[df_year['Y_Date_Count'] == annee].sort_values(by = 'Count_by_hour', ascending = False)

        # Toutes les adresses
        fig = plt.figure(figsize = (10,20))
        plt.subplot(131)
        sns.barplot(x = df2['Count_by_hour'], y = df2['Address_Dir'], color = '#FD8D3C');
        plt.title('Adresses avec direction', fontsize = 20)
        plt.xlabel('Comptage moyen de vélos / heure / site')
        plt.ylabel('')

        # Adresse
        plt.subplot(133)
        sns.barplot(x = df2['Count_by_hour'], y = df2['Address'], color = '#3FE3BD');
        plt.title('Adresses sans direction', fontsize = 20)
        plt.xlabel('Comptage moyen de vélos / heure / site')
        plt.ylabel('')
        st.pyplot(fig) 

       
# Prédiction du trafic    
if parties == sommaire[3]:
    
    st.title(parties)

    st.header('Observation de la target')
    # st.subheader('Observation de la cible')
      
    
    st.markdown("""Selectionner le compteur qui comptabilise le plus de passage afin d'observer 
                l'évolution de la variable *Count_by_hour* pendant une journée. 
                L'objectif est de determiner si la variable *Count_by_hour* suit une distribution 
                probabilistique connue.""")
   

# Conclusion et Perspectives
if parties == sommaire[4]:
    st.title('Conclusion') 
    st.markdown("""Le projet ParisPyVelib avait pour but différents objectifs : analyse et traitement des données, visualisation et prédiction du traffic.

L’objectif de se familiariser avec les données, de les nettoyer et les traiter dans le but de pouvoir s’en servir pour de la visualisation ou de la prédiction a été accompli malgré des difficultés rencontrées afin d’harmoniser toutes les données récoltées entre 2018 et 2021.

De même, la partie visualisation a permis d’obtenir des informations et des tendances sur l’utilisation des vélos dans Paris (fréquentation majoritairement en heure de pointe en semaine pour trajet domicile-travail, augmentation au fil des années, effet du 1er confinement, quartier les plus fréquentés…). Les pistes d’améliorations concernant cette partie, seraient d’une part d’étudier l’augmentation de la part de vélo par rapport aux autres modes transports (voiture, métro…). Les datasets source ont été trouvés sur ce sujet, mais non exploités faute de temps. D’autre part, d’analyser en temps réel de la circulation des cyclistes.

Concernant la partie modélisation en vue de prédire le trafic des vélos, l’objectif a été partiellement atteint. La comparaison entre un modèle “simple” basé sur une moyenne sur l’année n-1 et un modèle Random Forest donne une précision équivalente.  
Il est envisageable d’améliorer les scores de prédictions en explorant plusieurs pistes :  
●	Simplification des features actuelles  
●	Analyse des erreurs du modèle et biais potentiel du dataset  
●	Ajouts de features (jours de grèves, événements sportifs, manifestation, etc)  
●	Test d’autre algorithme de classification  
Cependant, la précision de modèle atteint une moyenne d'environ 80% ce qui reste suffisant tout en s’accordant une incertitude raisonnable. L'optimisation du modèle demanderait beaucoup plus de temps d’étude qu'initialement envisagé en début de projet.
""")

    st.title('Perspectives') 
    st.markdown("""Les perspectives d’utilisations de ses données sont multiples :

Tout d’abord, l’analyse et la prédiction du trafic cycliste peut permettre à la mairie de Paris d’étudier de manière précise l’impact de certains facteurs (météo, accidents, etc.). Ceux-ci influent sur le comportement des vélos et ainsi la mairie peut optimiser leur circulation en les protégeant grâce à l’aménagement de pistes cyclables efficaces.	

De plus, en combinant l’analyse et le machine learning, il est envisageable de pouvoir créer à l’image d’autres applications pour voiture (Waze), une application pour améliorer les trajets des vélos au quotidien à Paris en fluidifiant le trafic, par exemple. Celui-ci pouvant être étendu aux autres grandes agglomérations comme Bordeaux. 
""")    