# -*- coding: utf-8 -*-

import random
import time
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lugar_maps import LugarMaps

class GoogleMapsDataScraper:

    def __init__(self, idioma, imgOutput):
        self.driver = None
        self.errorCont = 0
        self.imgOutput = imgOutput
        self.configuracion = self.setConfiguracion(idioma)
    
    def setConfiguracion(self, idioma):
        conf = {
            'idioma': '--lang=es-ES',
            'textoEstrellas': 'estrellas',
            'textoReviews': 'reseñas',
            'textoDireccion': 'Dirección: ',
            'textoWeb': 'Sitio web: ',
            'textoTelefono': 'Teléfono: ',
            'textoPlusCode': 'Plus Code: ',
            'textoHorario': 'Ocultar el horario de la semana',
            'remplazarHorario': [' Ocultar el horario de la semana', 'El horario podría cambiar', '; ']
        }
        if(idioma == 'EN'):
            conf['idioma'] = '--lang=en-GB'
            conf['textoEstrellas'] = 'stars'
            conf['textoReviews'] = 'reviews'
            conf['textoDireccion'] = 'Address: '
            conf['textoWeb'] = 'Website: '
            conf['textoTelefono'] = 'Phone: '
            conf['textoPlusCode'] = 'Plus code: '
            conf['textoHorario'] = 'Hide open hours for the week'
            conf['remplazarHorario'] = ['. Hide open hours for the week', 'Hours might differ', '; ']
        
        return conf
    
    def initDriver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument(self.configuracion['idioma'])
            s=Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=s, options=chrome_options)
            self.driver.get('https://www.google.com/maps/')
            try:
                boton_aceptar = self.wait_element('//*[@aria-label="Aceptar todo"]', 7)
                boton_aceptar.click()
            except:
                pass
            time.sleep(2)
            return True
        except Exception as e:
            print(e)
            print('Error with the Chrome Driver')
            return False
    
    def quitarTildes(self, s):
        replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),)
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    
    def scrapearDatos(self, kw):
        try:
            lugar = LugarMaps()
            lugar.keyword = kw
            if(self.errorCont == 5):
                self.errorCont = 0
                time.sleep(1)
                self.driver.get('https://www.google.com/maps/')
                time.sleep(2)
            time.sleep(random.randint(1,3))
            inputBox = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]')))
            inputBox.click()
            inputBox.clear()
            inputBox.click()
            time.sleep(1)
            inputBox.send_keys(kw)
            time.sleep(1)
            inputBox.send_keys(Keys.ENTER)
            time.sleep(4)
                        
            if(self.isLoaded(kw) == False):
                return None
            
            divImg = self.driver.find_element(By.XPATH, '//*[@id="pane"]/following-sibling::div')
            titulo = divImg.find_element(By.TAG_NAME, 'h1').text
            lugar.nombre = titulo
            time.sleep(1)
            try:
                val = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "'+
                                                                                          self.configuracion['textoEstrellas']+'") and @role="img"]')))
                if '(' in val.text and ')' in val.text:
                    dividido = val.text.replace(')','').split('(')
                    estrellas = dividido[0]
                    numResenas = dividido[1]
                else:
                    valoraciones = val.get_attribute("aria-label")
                    estrellas = valoraciones.replace(self.configuracion['textoEstrellas'],'').replace(' ','')
                
                    val = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "'+self.configuracion['textoReviews']+'")]')
                    valoraciones = val.get_attribute("aria-label")            
                    numResenas = valoraciones.replace(self.configuracion['textoReviews'],'').replace(' ','')
                
                lugar.estrellas = self.checkValoraciones(estrellas)
                lugar.resenas = self.checkValoraciones(numResenas)
            except Exception as e:
                print(e)
                pass
            
            try:
                imgSrc = divImg.find_element(By.XPATH, '//img[@decoding="async"]').get_attribute("src")
                #imgSrc = divImg.find_element(By.TAG_NAME, 'img').get_attribute("src")
                if not 'gstatic' in imgSrc or not 'streetviewpixels' in imgSrc :
                    filename = kw.lower()
                    filename = self.quitarTildes(filename)
                    filename = re.sub(r'[^\w\s-]', '', filename)
                    filename = filename.replace(' ', '-')
                    filename = re.sub(r'-+', '-', filename)

                    full_path = f"{self.imgOutput}{filename}.jpg"
                    urllib.request.urlretrieve(imgSrc, full_path)
            except Exception as e:
                print(e)
                print('Unable to obtain the image')
                pass
            
            try:
                lugar.categoria = self.buscar_xpath('//button[contains(@jsaction, "pane.") and contains(@jsaction, ".category")]')
            except:
                lugar.categoria = ''

            try:
                direccion_label = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "' + self.configuracion['textoDireccion'] + '")]').get_attribute('aria-label')
                lugar.direccion = direccion_label.replace(self.configuracion['textoDireccion'], "").strip()
            except:
                lugar.direccion = ''

            try:
                web_label = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "' + self.configuracion['textoWeb'] + '")]').get_attribute('aria-label')
                lugar.web = web_label.replace(self.configuracion['textoWeb'], "").strip()
            except:
                lugar.web = ''

            try:
                telefono_label = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "' + self.configuracion['textoTelefono'] + '")]').get_attribute('aria-label')
                lugar.telefono = telefono_label.replace(self.configuracion['textoTelefono'], "").strip()
            except:
                lugar.telefono = ''

            try:
                pluscode_label = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "' + self.configuracion['textoPlusCode'] + '")]').get_attribute('aria-label')
                lugar.pluscode = pluscode_label.replace(self.configuracion['textoPlusCode'], "").strip()
            except:
                lugar.pluscode = ''
            
            lugar.horario = self.getHorario()
            
            return lugar
        except Exception as e:
            print(e)
            self.errorCont += 1
            return None
    
    def buscar_xpath(self, xpath):
        try:
            resultado = self.driver.find_element(By.XPATH, xpath).text
            return resultado
        except:
            return ''
    
    def wait_element(self, xpath, time):
        try:
            return WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print(f"Error waiting for element: {xpath} - {e}")
            return None
    
    def getHorario(self):
        try:
            horario = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "'+self.configuracion['textoHorario']+'")]').get_attribute('aria-label')
            horario = horario.replace(self.configuracion['remplazarHorario'][0], '')
            horario = horario.replace(self.configuracion['remplazarHorario'][1], '')
            horario = horario.replace(self.configuracion['remplazarHorario'][2], '\n')
            return horario
        except:
            return ''
    
    def isLoaded(self, kw):
        #divImg = self.driver.find_element_by_id('pane')
        divImg = self.driver.find_element(By.XPATH, '//*[@id="pane"]/following-sibling::div')
        titulo = divImg.find_elements(By.TAG_NAME, 'h1')
        vacio = True
        for a in titulo:
            if(a.text != ''):
                return True
        if(vacio):
            try:
                resultados = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "'+kw+'")]')
                enlace = resultados.find_element(By.TAG_NAME, 'a')
                enlace.click()
                time.sleep(3)
                return True
            except:
                pass
        return False
    
    def checkValoraciones(self, val):
        if(self.configuracion['textoEstrellas'] in val or self.configuracion['textoReviews'] in val):
            return ''
        else:
            return val
        
    
    def endDriver(self):
        self.driver.quit()
