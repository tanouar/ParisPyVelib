# Import library:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import datetime
from rfModel import rfMmodel, preLoadH5
# data = pd.DataFrame()

# data = preLoadDataset("Datas/2018-2021_donnees-velib-meteo_hour.csv")
data = preLoadH5("Datas/machineLearningDataset.h5", 'dst')

# Récupération du répertoire courant
currentPath = os.getcwd()
# print('Current path : ', currentPath)

# Définition du répertoire contenant les données
datasPath = currentPath + '\\' + 'Datas'
# print('Set path with datas : ', datasPath)


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
st.sidebar.image('Pictures/Velib.png')
sommaire = ['Introduction', 'Datasets', 'Evolution Temporelle', 'Prédiction du trafic', 'Conclusion et Perspectives']
parties = st.sidebar.radio('', sommaire)


# Introduction


if parties == sommaire[0]:
    st.title('ParisPyVelib')
    st.image('Pictures/Velib.png')
    st.header('Analyse et prédiction du trafic des vélos de 2018 à 2021 dans la ville de Paris')
    st.markdown('''<p style='text-align: justify'>Projet réalisé par Tarik Anouar, Céline Doussot et Hermine Berthon en tant que projet fil-rouge de la formation de Data Analyst de DataScientest.
                 </p>''',  unsafe_allow_html=True)
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
                    L'observation de ces jeux de données a montré quelques problèmes d'homogénéité. Certains compteurs ont été remplacés
                    par des nouveaux, ce qui a pu changer l’identifiant ou les coordonnées géographiques. De même, le format de certaines
                    variables, en particulier les adresses, n’était pas identique entre les différents dataframe
                    (2018, 2019 différent de 2020, 2021).
                    </p>''',  unsafe_allow_html=True)
        st.markdown('''<p style='text-align: justify'>
                    Pour cela, nous avons dans un premier temps identifié les problèmes tels que la gestion des doublons.
                    Ensuite, nous avons harmonisé tous les fichiers afin d’attribuer chacune des coordonnées à une adresse
                    puis créé un nouvel identifiant unique pour chacun des compteurs.
                    </p>''',  unsafe_allow_html=True)
        st.markdown('''<p style='text-align: justify'>
                    Dans un second temps, nous avons transformé, supprimé et ajouté certaines colonnes qui nous semblaient
                    pertinentes pour la suite tel que l’ajout de colonnes séparant l’heure, le jour, le mois et l’année de comptage.
                    </p>''',  unsafe_allow_html=True)
        st.markdown('''<p style='text-align: justify'>
                    Enfin, nous avons renommé certaines colonnes pour faciliter la compréhension. Sur le dataframe final, la colonne
                    cible est le comptage horaire mais les autres colonnes importantes pour son étude et prédiction, sont les colonnes
                    temporelles ainsi que les coordonnées géographiques.
                    </p>''',  unsafe_allow_html=True)
        
    if data == 'Données météo':
        st.header('Description')
        st.markdown('''<p style='text-align: justify'>
                    Nous avons opté pour un 
                    <a href= "https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/table/?flg=fr&sort=date">
                    site</a>
                    permettant un accès libre sur toutes les données météos provenant de la ville d'Athis-Mons (91),
                    seul compteur disponible en île-de-France. Cela correspond, après sélection de 2018 à 2021,(même période que pour les compteurs vélib) 
                    à un dataframe de 9944 rows × 82 columns. Celui-ci a ensuite été réduit, par la suite, pour ne sélectionner que les données intéressantes.
                    </p>''',  unsafe_allow_html=True)
        df_meteo =pd.read_csv("Datas/donnees-synop-essentielles-omm.csv")
        st.write(df_meteo.head())


    if data == 'Dataset final':
        st.header('Description')
        st.markdown('''<p style='text-align: justify'>
                    Au dataset rassemblant toute les données précédentes, nous avons ajouté des données sur les
                    <a href= "https://www.data.gouv.fr/fr/datasets/vacances-scolaires-par-zones/">
                     vacances scolaires</a>
                     , sur les
                     <a href= "https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/">
                     jours fériés</a> et les confinements.
                    </p>''',  unsafe_allow_html=True)
                    
        # Import du df_hour
        df_hour = pd.read_csv(dataset_2018_2021_donnees_velib_meteo_hour)
        df_final = df_hour.drop(['Unnamed: 0'], axis = 1)
        st.text('Affichage des 5 premières lignes du dataset')
        st.write(df_final.head())
        
        st.header('Preprocessing')
        st.markdown('''<p style='text-align: justify'>
                    Lorsque nous avons voulu introduire les données météos à notre dataset initial, nous
                    nous sommes aperçus que de nombreuses colonnes étaient inutiles ou comportaient beaucoup
                    de NANs. De plus, les données météo n’étaient mises à jour que toutes les 3h et non toutes les
                    heures comme notre dataset standard. Pour pallier ce problème, nous avons sélectionné
                    certaines colonnes pertinentes pour l’étude de la fréquentation vélo comme la pluie, le vent ou
                    encore la neige, puis nous avons utilisé un backfill pour compléter les données manquantes sur
                    certaines heures.
                    </p>''',  unsafe_allow_html=True)
                    
        st.header('Distribution')
        Liste_col = ['Count_by_hour', 'Latitude', 'Longitude',
             'M_Date_Count', 'D_Date_Count', 'Dweek_Date_Count', 'H_Date_Count',
             'Y_Date_Instal', 'M_Date_Instal', 'D_Date_Instal',
             'T°C', 'Precip_last3h', 'HR%', 'High_ice','Wind_speed_mean10mn']
        

        df_final['Latitude'] = df_final['Latitude'].astype('float64')
        df_final['Longitude'] = df_final['Longitude'].astype('float64')
        option2 = st.selectbox('Sélectionner la variable', Liste_col) 
        for col in Liste_col:
            if option2 == col:
                fig = plt.figure(figsize = (10,4))
                st.write(sns.boxplot(data=df_final, y=col, x = 'Y_Date_Count'))
                st.pyplot(fig)
        

        
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
        st.markdown("""<p style='text-align: justify'>
                    De façon général, on peut remarquer que l'utilisation des vélos augmentent au fil des années comme le montre le graphique ci-dessous. 
                    En effet, malgré le confinnement strict qu'il y a eu en 2020, la fréquentation a presque doublé de 2018 à 2020. 
                    La légère baisse pour 2021 peut s'expliquer par le fait que les données ne sont pas complètes et ne tiennent compte
                    que de la période janvier-mai.
                    </p>""",  unsafe_allow_html=True)
        #Affichage de l'évolution des comptages horaires moyen /année
        fig = plt.figure(figsize = (10,4))
        sns.barplot(x = df_year['Y_Date_Count'], y = df_year['Count_by_hour'], color = '#3FE3BD');
        plt.title('Moyenne des comptages horaires par année', fontsize = 15)
        plt.ylabel('Comptages horaires moyen /année')
        plt.xticks(rotation = 90)
        plt.xlabel('')
        st.pyplot(fig)
        
        st.markdown("""<p style='text-align: justify'>Lorsque nous analysons la variable plus en détail, selon les mois de l’année, il
                    semble y avoir une différence entre les mois que l’on pourrait qualifier “d'hiver", de novembre à avril,
                    et “d'été", de mai à octobre. Dans les premiers, la température est plus fraîche avec de gros
                    écarts de température entre la matinée et l’après-midi et les seconds ont une
                    température plus douce et homogène. Nous pouvons noter que le mois d’août
                    enregistre particulièrement peu de vélos. Cela est synonyme que les parisiens partent
                    souvent en vacances durant ce mois, avec une recrudescence à la rentrée. De 2018 à
                    2021, nous voyons une tendance en augmentation, du nombre de vélos, avec une coupure lors
                    du confinement stricte et une grosse augmentation juste après à la fin de celui-ci.</p>""",  unsafe_allow_html=True)
    
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
        
        st.markdown("""<p style='text-align: justify'>L’utilisation des vélos est principalement utilisée en tant que mode 
                    de transport pour le trajet domicile-travail. En effet, on peut remarquer sur les graphiques ci-dessous
                    une différence notable entre la semaine et les weekends.</p>""",  unsafe_allow_html=True)
        
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
    
        st.markdown("""<p style='text-align: justify'>En semaine, la fréquentation est plus intense que les weekends.
                    Deux pics de circulation sont présents le matin et l'après-midi, correspondant aux heures de pointe du travail.
                    Les deux pics ayant une allure quasi identique, cela pourrait montrer que ce sont les mêmes cyclistes à l’aller
                    et au retour de leur trajet domicile-travail. Le weekend, la distribution est plus dispersée tout au long de 
                    la journée, avec une gaussienne plus aplatie. Nous avons remarqué également que les jours fériés se comportent
                    comme les weekends.</p>""",  unsafe_allow_html=True)
    
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

    st.header('Prédiction de la target *Count_by_hour*')    
    
    st.markdown("""<p style='text-align: justify'>Selectionner un compteur ainsi qu'une date. Observer la variable cible
                *Count_by_hour* ainsi que les prédiction realisées par le modèle Random Forest pendant une journée.
                </p>""",  unsafe_allow_html=True)
                
    # Selection du compteur via selectbox            
    selectAddress = st.selectbox('select address', data.Address_Dir.unique())
    st.write('Addresse selectionnée :', selectAddress)
    
    # Selection du jour, mois et années par l'utilisateur
    d = st.date_input('Selection de la date', datetime.date(2020, 7, 6))
    st.write('Date selectionnée:', d)

    
    # Calcul des prédictions en fonction du compteurs, et de la date
    resultats = rfMmodel(selectAddress, d.year, d.month, d.day, data=data)

    figure = plt.figure(figsize = (18,9))
    hh = np.arange(0, 24, 1)    
    
    # Affichage de la variable target
    plt.plot(hh, resultats[0], color="black")
    plt.scatter(hh, resultats[0], color="black")
    
    # Affichage des prédictions    
    plt.plot(hh, resultats[1], color="red")
    plt.scatter(hh, resultats[1], color="red")
    
    # Ajout de la valeur max et min de chaque classes prédites comme contours
    plt.fill_between(hh, resultats[2], resultats[3], alpha=0.1, color="blue")
           
    plt.xlabel('Heure')
    plt.ylabel('Nombre de velo')
    plt.legend(['target : Count_by_hour', 'Prediction : Mean Count_by_hour'])
    plt.title("Prédiction et Target en fonction de l'heure de la journée, compteur")
    plt.grid('--')
    plt.xticks(np.arange(0, 24, 1));

    st.pyplot(figure)
    
    st.write('Score :', resultats[4], '%')


# Conclusion et Perspectives
if parties == sommaire[4]:
    st.title('Conclusion') 
    st.markdown("""<p style='text-align: justify'>Le projet ParisPyVelib avait pour but différents objectifs : analyse et traitement des données, visualisation et prédiction du traffic.

L’objectif de se familiariser avec les données, de les nettoyer et les traiter dans le but de pouvoir s’en servir pour de la visualisation ou de la prédiction a été accompli malgré des difficultés rencontrées afin d’harmoniser toutes les données récoltées entre 2018 et 2021.

De même, la partie visualisation a permis d’obtenir des informations et des tendances sur l’utilisation des vélos dans Paris (fréquentation majoritairement en heure de pointe en semaine pour trajet domicile-travail, augmentation au fil des années, effet du 1er confinement, quartier les plus fréquentés…). Les pistes d’améliorations concernant cette partie, seraient d’une part d’étudier l’augmentation de la part de vélo par rapport aux autres modes transports (voiture, métro…). Les datasets source ont été trouvés sur ce sujet, mais non exploités faute de temps. D’autre part, d’analyser en temps réel de la circulation des cyclistes.

Concernant la partie modélisation en vue de prédire le trafic des vélos, l’objectif a été partiellement atteint. La comparaison entre un modèle “simple” basé sur une moyenne sur l’année n-1 et un modèle Random Forest donne une précision équivalente.  
Il est envisageable d’améliorer les scores de prédictions en explorant plusieurs pistes :  
●	Simplification des features actuelles  
●	Analyse des erreurs du modèle et biais potentiel du dataset  
●	Ajouts de features (jours de grèves, événements sportifs, manifestation, etc)  
●	Test d’autre algorithme de classification  
Cependant, la précision de modèle atteint une moyenne d'environ 80% ce qui reste suffisant tout en s’accordant une incertitude raisonnable. L'optimisation du modèle demanderait beaucoup plus de temps d’étude qu'initialement envisagé en début de projet.
</p>""",  unsafe_allow_html=True)


    st.title('Perspectives') 
    st.markdown("""<p style='text-align: justify'>Les perspectives d’utilisations de ses données sont multiples :

Tout d’abord, l’analyse et la prédiction du trafic cycliste peut permettre à la mairie de Paris d’étudier de manière précise l’impact de certains facteurs (météo, accidents, etc.). Ceux-ci influent sur le comportement des vélos et ainsi la mairie peut optimiser leur circulation en les protégeant grâce à l’aménagement de pistes cyclables efficaces.	

De plus, en combinant l’analyse et le machine learning, il est envisageable de pouvoir créer à l’image d’autres applications pour voiture (Waze), une application pour améliorer les trajets des vélos au quotidien à Paris en fluidifiant le trafic, par exemple. Celui-ci pouvant être étendu aux autres grandes agglomérations comme Bordeaux. 
</p>""",  unsafe_allow_html=True)