# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 14:19:38 2021

@author: h.berthon
"""

import numpy as np
import pandas as pd

# Importation des fonctions dont l'on se servira pour toutes les figures
from bokeh.plotting import figure, output_notebook, show

# Précision de l'affichage des graphiques dans des cellules jupyter
output_notebook()

df = pd.read_csv('2018-2021_comptage-velo-donnees-compteurs.csv')

df.head()

#Nouveau df avec moins de colonnes
df_lat_lon= df.drop(['Unnamed: 0','Id_old','Address_old','Date_count', 
                     'Date_instal', 'Photo_old', 'Coord_old', 'Source', 'Coord'
                     ], axis =1)
df_lat_lon.head()

#Visualisation de la carte
from  bokeh.tile_providers import get_provider
tuile = get_provider('CARTODBPOSITRON')
p = figure(x_range = (480000, 490000), y_range = (20000, 30000), x_axis_type = 'mercator', y_axis_type = 'mercator' )
p.add_tile(tuile)
show(p)