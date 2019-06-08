# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:44:15 2019

@author: Estera
"""
from kivy.garden.mapview import MapView
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker, MarkerMapLayer
import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg # lub FigureCanvas
import matplotlib.pyplot as plt     # pyplot importujemy PO matplotlib.use(...)
import matplotlib.dates as mdates
import biblio
import numpy as np

   
#--------------------KIVY------------------------------------------------------

class AddLocationForm(BoxLayout): #stworzenie klasy
    
    txt1=ObjectProperty()
    txt2=ObjectProperty()
    my_map=ObjectProperty()
    plot=ObjectProperty()


            
    def __init__(self, **kwargs):           # inicjalizacja dla klasy niedziedziczacej po App
        super(AddLocationForm, self).__init__(**kwargs)        
        self.fig = plt.figure()# stworzenie pustego wykresu        
        self.cnv = FigureCanvasKivyAgg(self.fig)# utworzenie wykresu w aplikacji na podstawie pustego wykresu        
        self.plot.add_widget(self.cnv) # dodanie wykresu do aplikacji do widgeta plots           
            
        
        
        
#----------------wykres - profil wysokosci-------------------------------------     
            
    def rysuj_wykres1(self):
        filename = self.txt1.text #wczytanie pliku
                
        lat,lon,lat1,lat2,lon1,lon2,el,dates,elstart,elstop,datesstop,datesstart,delta,sekundy,sumdates,lat1wyk,lon1wyk=biblio.wczytaj_plik(filename)#import danych
        
        def haversine1(orig, dest): #funkcja licząca odlegosć poziomą między punktem początkowym trasy a kolejnymi punktami trasy
            lat1wyk, lon1wyk = orig
            lat2, lon2 = dest
            radius = 6371000 # m
    

            dlat1 = np.radians(lat2-lat1wyk)

            dlon1 = np.radians(lon2-lon1wyk)
    
            a1 = np.sin(dlat1/2) * np.sin(dlat1/2) + np.cos(np.radians(lat1wyk)) \
            * np.cos(np.radians(lat2)) * np.sin(dlon1/2) * np.sin(dlon1/2)
            c1 = 2 * np.arctan2(np.sqrt(a1), np.sqrt(1-a1))
            d1 = radius * c1

            return d1
        
        
        dist_part1 = haversine1((lat1wyk, lon1wyk), (lat2, lon2))
        D=list(dist_part1)#utworzenie listy z odległosciami
        D.insert(0, 0)#wprowadzenie odleglosci równej 0 w pierwszym punkcie trasy (aby móc zaznaczyć na wykresie wysokosć dla punktu początkowego) 
        
       
        
        if el is not None:  #rysowanie wykresu, jesli wysokosc istnieje         
            self.ax1 = self.fig.add_subplot(111)    
            self.ax1.plot(D,el) 
            plt.xlabel('Odległość pozioma [m]')
            plt.ylabel('Wysokość [m]')
            plt.title('Profil wysokościowy')        
            self.cnv.draw()
            plt.savefig("wykres_profil.png")#zapis do pliku
        else: 
            pass


#----------------wykres - predkosc od odleglosci-------------------------------

    def rysuj_wykres2(self):
        filename = self.txt1.text #wczytanie pliku
                
        lat,lon,lat1,lat2,lon1,lon2,el,dates,elstart,elstop,datesstop,datesstart,delta,sekundy,sumdates,lat1wyk,lon1wyk=biblio.wczytaj_plik(filename)#import danych
        
        def haversine1(orig, dest):#funkcja licząca odlegosć poziomą między punktem początkowym trasy a kolejnymi punktami trasy
            lat1wyk, lon1wyk = orig
            lat2, lon2 = dest
            radius = 6371000 # m
    

            dlat1 = np.radians(lat2-lat1wyk)

            dlon1 = np.radians(lon2-lon1wyk)
    
            a1 = np.sin(dlat1/2) * np.sin(dlat1/2) + np.cos(np.radians(lat1wyk)) \
            * np.cos(np.radians(lat2)) * np.sin(dlon1/2) * np.sin(dlon1/2)
            c1 = 2 * np.arctan2(np.sqrt(a1), np.sqrt(1-a1))
            d1 = radius * c1

            return d1
        
        
        dist_part1 = haversine1((lat1wyk, lon1wyk), (lat2, lon2))
        D=list(dist_part1)
        D.insert(0, 0) 
        

#------------------predkosci---------------------------------------------------  
    
        def haversine(origin, destination):#funkcja licząca odleglosci na pomiedzy punktami trasy
            lat1, lon1 = origin
            lat2, lon2 = destination
            radius = 6371000 # m

            dlat = np.radians(lat2-lat1)
            dlon = np.radians(lon2-lon1)
    
            a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) \
            * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
            d = radius * c

            return d        
        
        
        dist_part = haversine((lat1, lon1), (lat2, lon2))# m  
        #obliczenie prędkosci na odcinkach 
        if sekundy>0:
            v=dist_part/sekundy #m/s  
            V=list(v)
            V.insert(0, 0)    
            self.ax1 = self.fig.add_subplot(111)    
            self.ax1.plot(D,V) 
            plt.xlabel('Odległość pozioma [m]')
            plt.ylabel('Prędkość [m/s]')
            plt.title('Wykres zależności prędkości od odległości poziomej')        
            self.cnv.draw()
            plt.savefig("wykres_v_od_s).png")#zapis do pliku
        else:
            pass                        
             

    def czyszczenie(self):#funkcja czyszcząca 
        self.txt2.text =''#nazwę pliku
        self.txt1.text =''#statystyki
        self.ax1.remove()#wykres
        self.my_map.remove_layer(self.data_lay)#znacznik na mapie
        
        
        
#------------------analiza trasy-----------------------------------------------        

    def analyse_file(self): 
        filename = self.txt1.text #wczytanie pliku                
        lat,lon,lat1,lat2,lon1,lon2,el,dates,elstart,elstop,datesstop,datesstart,delta,sekundy,sumdates,lat1wyk,lon1wyk=biblio.wczytaj_plik(filename)

   
#---------------------HAVERSINE------------------------------------------------
    
        def haversine(origin, destination):
            lat1, lon1 = origin
            lat2, lon2 = destination
            radius = 6371000 # m

            dlat = np.radians(lat2-lat1)
            dlon = np.radians(lon2-lon1)
    
            a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) \
            * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
            d = radius * c

            return d



#------------------rysowanie poczatku trasy------------------------------------  

        self.data_lay = MarkerMapLayer()
        self.my_map.add_layer(self.data_lay)         
        marker = MapMarker(lat=lat[0], lon=lon[0], source="dot.png")
        self.my_map.add_marker(marker, layer=self.data_lay)

#-----------------------obliczenia---------------------------------------------
        
        dist_part = haversine((lat1, lon1), (lat2, lon2))# m        
        sumdist=sum(dist_part)#długosć całkowita trasy - pozioma
        alt_part = (elstop-elstart) #przwyższenia na odcinkach trasy
        
        
        def przewyzszenie_dodatnie(alt_part):#całkowite przewyższenie w górę           
            dodatnie=[]           
            for przewyzszenie in alt_part:
                if przewyzszenie>=0:
                    dodatnie.append(przewyzszenie)                
            return dodatnie

        def przewyzszenie_ujemne(alt_part): #całkowite przewyższenie w dół              
            ujemne=[]           
            for przewyzszenie in alt_part:
                if przewyzszenie<0:
                    ujemne.append(przewyzszenie)                   
            return ujemne    
                    
            
        altsum=sum(alt_part)#całkowite przewyższenie na trasie
        odl3D=np.sqrt((dist_part**2+alt_part**2)) #odległosć skosna
        sum3D=sum(odl3D) #całkowita odleglosc skosna trasy
      
#------------------predkosci---------------------------------------------------            
        if sekundy>0:
            v=dist_part/sekundy #m/s
            vavg = sum(v) / len(v)
            p7=str(round(vavg,3))        
        else:
            v=0
            vavg=0
            p7=str('Brak')



#-------------wyswietlanie statystyk-------------------------------------------

        p1=str(round(sumdist,3))
        p2=str(round(sum3D,3))
        p3=str(round(altsum,3))
        p4=str(round(sum(np.array(przewyzszenie_dodatnie(alt_part))),3))
        p5=str(round(sum(np.array(przewyzszenie_ujemne(alt_part))),3))
        p6=str(sumdates)
        p8=str(round(max(el),3))
        p9=str(round(min(el),3))

        
        self.txt2.text ='Statystyki:'       
        self.txt2.text +='\nCałkowita odległość (długość) pozioma [m]    '
        self.txt2.text +=p1
        self.txt2.text +='\nCałkowita odległość skośna [m]    '
        self.txt2.text +=p2
        self.txt2.text +='\nCałkowite przewyższenie [m]    '  
        self.txt2.text +=p3
        self.txt2.text +='\nw tym: w górę / w dół    '
        self.txt2.text +=p4
        self.txt2.text +='  /  '
        self.txt2.text +=p5
        self.txt2.text +='\nCzas [h:m:s]    '
        self.txt2.text +=p6
        self.txt2.text +='\nSrednia predkość [m/s]    '
        self.txt2.text +=p7
        self.txt2.text +='\nMaksymalna wysokość [m]    '
        self.txt2.text +=p8
        self.txt2.text +='\nMinimalna wysokość [m]    '
        self.txt2.text +=p9



       
class MapViewApp(App):
    def build(self):
        return AddLocationForm()
       
if __name__ == '__main__':
    MapViewApp().run()