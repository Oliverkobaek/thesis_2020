#This module holds the functions needed in the project of geodata. 
#The first function is used to calculate distances based on Langtitude and Longtitude. 
import numpy as np
import matplotlib.pyplot as plt           #We use it for construction of graphs, both 3D and 2D
import math
import matplotlib as mpl
import pandas as pd

import json
import os
import requests

# spatial stuff
#sksksk
import fiona
import folium
import shapely
from descartes import PolygonPatch
from tqdm import tqdm
#!conda install -U scikit -learn
from sklearn.neighbors import KNeighborsRegressor

from math import radians, cos, sin, asin, sqrt

def haversine(cords1,cords2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1 = cords1.x
    lat1 = cords1.y
    lon2 = cords2.x
    lat2 = cords2.y   
    
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

dk_crs = {'ellps': 'GRS80', 'no_defs': True, 'proj': 'utm', 'units': 'm', 'zone': 32}

import geopandas as geopandas
def cell_coords_to_polygons(square_df, x='longtitude', y='latitude', dist=1000, crs=dk_crs):
    '''
    Convert coordinates to squares in a GeoDataFrame.
       
    Parameters
    ----------
    x : str
        Name of the horizontal coordinate (~longitude)            
    y : str
        Name of the vertical coordinate (~latitude)                        
    dist : int or float
        Size of polygons
    crs : dict
        Coordinate Reference System


    Returns
    ----------
    squares_gdf: geopandas.GeoDataFrame
        This table contains squares as geometry
        and the original data.
    '''
    
    def _to_square_polygon(row):
        '''
        This auxiliary function convert a square's lower,left 
        coordinates to a polygon. 
        
        Parameters
        ----------
        row : pandas.Series
            This is a DataFrame row.            
        
        Returns
        ----------
        poly: shapely.Polygon        
        
        '''
        
        square_coords = ((row[x], row[y]), 
                         (row[x]+dist, row[y]), 
                         (row[x]+dist, row[y]+dist), 
                         (row[x], row[y]+dist))
        
        poly = shapely.geometry.Polygon(square_coords)
        
        return poly
    
    # convert to polygons
    square_geoms = geopandas.GeoSeries(square_df.apply(_to_square_polygon, axis=1), crs=crs)
    
    # make GeoDataFrame
    square_gdf = geopandas.GeoDataFrame(data=square_df, geometry=square_geoms)
    
    return square_gdf