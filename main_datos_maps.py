# -*- coding: utf-8 -*-


from exportarDatos import ExportarDatosMaps
from maps_data_scraper import GoogleMapsDataScraper
from threading import Thread
import sys
import os

def split_list(a, n):
    k, m = divmod(len(a), n)
    return list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))

def scrapearMaps(idioma, lista, outputFolder, resultados, hilo):
    scraper = GoogleMapsDataScraper(idioma, outputFolder)
    scraper.initDriver()
    listaLugares = []

    cont=1
    for l in lista:
        lugar = scraper.scrapearDatos(l)
        
        if(lugar != None):
            print('Hilo nº '+str(hilo)+' ' +str(cont) + '/' + str(len(lista)) + ' - OK - ' + l)
            listaLugares.append(lugar)
        else:
            print('Hilo nº '+str(hilo)+' ' +str(cont) + '/' + str(len(lista)) + ' - ERROR - ' + l)
        cont +=1
    
    resultados[hilo] = listaLugares
def mainGoogleMaps(idioma, ficheroKw, outputFolder):
    archivo = open(ficheroKw,'r', encoding='utf-8')
    listaF = archivo.read().splitlines()
    archivo.close()

    hilos = 5
    listaHilos = [None] * hilos
    listaResultados = [None] * hilos
    divididos = split_list(listaF, hilos)

    for i in range(len(listaHilos)):
        listaHilos[i] = Thread(target = scrapearMaps, args=(idioma, divididos[i], outputFolder, listaResultados, i,))
        listaHilos[i].start()

    for i in range(len(listaHilos)):
        listaHilos[i].join()

    listaFinal = []

    for i in range(len(listaResultados)):
        listaFinal = listaFinal + listaResultados[i]

    exportar = ExportarDatosMaps(outputFolder+'00_output.xls','', listaFinal)
    exportar.exportarExcel()

if __name__ == "__main__":
    while True:
        idioma = input('----------\n[1] Introduce the language, (ES o EN): ')
        if(idioma != 'ES' and idioma != 'EN'):
            print("----------\n** Error ** That is not a valid language. Enter a valid language\n")
            continue
        else:
            break
    
    while True:
        fichero = input('----------\n[2] Introduce the path to save the images: ')
        if(os.path.isdir(fichero) == False):
            print("----------\n** Error ** That is not a valid folder. Enter a valid folder\n")
            continue
        else:
            caracter = fichero[len(fichero)-1]
            if(caracter != '/' or caracter != '\\'):
                fichero = fichero.replace('/','\\')+'\\'
            break
    
    while True:
        kwLugares = input('----------\n[3] Introduce the path of the keywords txt file: ')
        if(os.path.isfile(kwLugares) == False):
            print("----------\n** Error ** That is not a valid txt file. Enter a valid file\n")
            continue
        else:
            break
    
    mainGoogleMaps(idioma,kwLugares, fichero)