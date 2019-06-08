# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:15:38 2019

@author: Estera
"""

import gpxpy
import gpxpy.gpx
import datetime
from datetime import timedelta
import numpy as np




def wczytaj_plik(filename):
    lat = []
    lon = []
    el = []
    dates = []
        
    with open(filename,'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        
        for track in gpx.tracks:
            for seg in track.segments:
                for point in seg.points:
                    lon.append(point.longitude)
                    lat.append(point.latitude)  # jezeli informacja o elewacji dostepna

                    if point.elevation is not None:               
                        el.append(point.elevation)  # jezeli informacja o czasie dostepna  
                        elstop=np.array(el[1:])
                        elstart=np.array(el[0:-1])
                    else:
                        el=0
                        elstop=0
                        elstart=0
                
                    if point.time is not None:                
                        point.time = point.time.replace(tzinfo=None)  # usuniecie informacji o strefie czasowej
                        dates.append(point.time) 
                        datesstop=dates[1:]
                        datesstart=dates[0:-1]
               
                        for i in range(len(dates)):
                            start=i-1
                            stop=i
                            delta=dates[stop]-dates[start]
                            sekundy=delta.total_seconds()
                            sumdates=dates[-1]-dates[0]
                    else:
                        dates=0
                        datesstop=0
                        datesstart=0
                        delta=0
                        sekundy=0
                        sumdates=0
                
    lat2=np.array(lat[1:])
    lat1=np.array(lat[0:-1])
    lon2=np.array(lon[1:])
    lon1=np.array(lon[0:-1])
    lat1wyk=np.array(lat[0])
    lon1wyk=np.array(lon[0])
            
                
    return lat,lon,lat1,lat2,lon1,lon2,el,dates,elstart,elstop,datesstop,datesstart,delta,sekundy,sumdates,lat1wyk,lon1wyk
                       