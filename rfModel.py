# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 13:27:37 2021

@author: TAR
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, ensemble
import time


def rfMmodel(Address_Dir,  
             Y_Date_Count, 
             M_Date_Count, 
             D_Date_Count, data):
    """
    Parameters
    ----------
    data : DataFrame
    Address : address du compteur 
    Direction : direction du compteur
    Y_Date_Count : année de 2018 à 2019 (int)
    M_Date_Count : mois de l'année de 1 à 12 (int) 
    D_Date_Count : jour de 1 à 31 (int)
    
    
    Returns
    ---------
    target_to_predict : comptage horaire de la date selectionné
    pred : prédiction moyen par le modèle random forest
    pred_min : prédiction min par le modèle random forest 
    pred_max : prédiction max par le modèle random forest
    score : score des prédictions
    
    """
    
    start = time.time()
  
    # affectaction du dataset data au dataframe df
    df = data
    
    # Selection d'un seul compteur et uniquement pour l'année 2021
    df = data[data.Address_Dir == Address_Dir]
    df = df[df.Y_Date_Count == Y_Date_Count ]
    
    # Supression des colonnes non utile pour le modele
    # df = df.drop(['Unnamed: 0', 'Coord', 'City_meteo', 'vacances_zone_c', 'Address', 'Date', 'Address_Dir',
    #               'Source', 'Id', 'Y_Date_Instal', 'M_Date_Instal', 'D_Date_Instal', 'Date_instal', 'Datetime'], axis = 1)
    
    
    # Ajout de la variable AP et PM
    df['AM_PM'] = ['AM' if x < 12 else 'PM' for x in df['H_Date_Count']]
       
    # Ajout de la variable weekend et week
    df['week_day_type'] = ['week' if x < 5 else 'weekend' for x in df['Dweek_Date_Count']]
    
    # Reset de l'index
    df = df.reset_index(drop=True)
    
    # List des variable catégorielle
    cat_df = df.select_dtypes(include='object')
    cat_df = cat_df.columns.tolist()
    
    # Transformation des variable catégorielle en variable indicatrices
    df = pd.get_dummies(df, columns=cat_df)
    
    # Selection de la target et des feats
    target = df['Count_by_hour']
    feats = df.drop(['Count_by_hour'], axis=1)
    
    # On récupère les valeurs des classes
    classVal, inter = pd.qcut(target, 4, retbins=True)
    
    # Classification de la varibale Target
    target = pd.qcut(target, 4, labels = [0, 1, 2, 3])
    
    # Séparation du jeux de donnée pour entrainement
    X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.2, random_state=101)
    
    # Preprocessing
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = X_train
    X_test_scaled = X_test
    
    # Prédiction des features
    clf = ensemble.RandomForestClassifier(min_samples_split=4)
    clf.fit(X_train_scaled, y_train)
    
    # Selection de la date
    df_Select = df[df.M_Date_Count == M_Date_Count]
    df_Select = df_Select[df_Select.D_Date_Count == D_Date_Count]
    
    # Selection de la target et des feats
    target_to_predict = df_Select['Count_by_hour']
    feats_to_predict = df_Select.drop(['Count_by_hour'], axis=1)
    
    # Calul des prédiction
    prediction = clf.predict(feats_to_predict)
    
    
    # Création d'une liste avec les moyennes des classes et remplacement des moyennes dans le resultat des prédictions
    lmin = [inter[0], inter[1], inter[2], inter[3]]
    lmax = [inter[1], inter[2], inter[3], inter[4]]
    lmc=[]
    
    # Calcul de la valeur moyenne des min-max pour chaque classe
    for i, j, in zip (lmin, lmax): 
        x = (i + j) / 2
        lmc.append(x)
        
    pred = []
    pred_min = []
    pred_max = []
    
    for classes in prediction:
        if classes == 0:
            pred.append(lmc[0])
            pred_min.append(lmin[0])
            pred_max.append(lmax[0])
        if classes == 1:
            pred.append(lmc[1])
            pred_min.append(lmin[1])
            pred_max.append(lmax[1])
        if classes == 2:
            pred.append(lmc[2])
            pred_min.append(lmin[2])
            pred_max.append(lmax[2])
        if classes == 3:
            pred.append(lmc[3]) 
            pred_min.append(lmin[3])
            pred_max.append(lmax[3])
            
    target_to_predict = list(target_to_predict)
    score = (clf.score(X_test_scaled, y_test)*100).round(2)
    
    end = time.time()
    t = end - start    
        
    # print(target_to_predict)
    # print(pred)
    # print(pred_min)
    # print(pred_max)
    # print(score)
    print("processing time : ", "%.2f" %t, "s")
    
    
    return target_to_predict, pred, pred_min, pred_max, score



def preLoadDataset(filePath):
    
    start = time.time()
    
    cols = ['Count_by_hour',
             # 'Direction',
             # 'Latitude',
             # 'Longitude',
             'Y_Date_Count',
             'M_Date_Count',
             'D_Date_Count',
             'Dweek_Date_Count',
             'H_Date_Count',
             'T°C',
             'Precip_last3h',
             'HR%',
             # 'High_ice',
             'Wind_speed_mean10mn',
             # 'nom_jour_ferie',
             'nom_vacances',
             'Confinement_id', 'Address_Dir']
    
    df = pd.read_csv(filePath, usecols=(cols))
    df = df.fillna(method="ffill")
    df = df.fillna(method="bfill")
    
    end = time.time()
    t = end - start 
    
    print("loading time : ", "%.2f" %t, "s")
    
    return df


def preLoadH5(filePath, key):
    
    start = time.time()
    
    df = pd.read_hdf(filePath, key)
    
    end = time.time()
    t = end - start 
    
    print("loading time : ", "%.2f" %t, "s")
    
    return df



if __name__ == '__main__':
    
    # Chargement des données
    print('loading Dataset')
    data = preLoadDataset("Datas/2018-2021_donnees-velib-meteo_hour.csv")       
    
    # Enregistrement des données au format h5
    print("saving dataset in new format")
    data.to_hdf("Datas/machineLearningDataset.h5", 'dst')        