# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 10:15:42 2025

@author: FPC

Tomar canciones de la página de radios.com de la radio radioacktiva.
"""

import time

time.sleep(1)

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import sys
import types

# 🔧 Parche para reemplazar distutils en Python 3.13
distutils = types.ModuleType("distutils")
version = types.ModuleType("version")

class DummyVersion:
    def __init__(self, v="0.0"):
        self.vstring = v
        self.version = v

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return f"<DummyVersion {self.vstring}>"

    # Métodos de comparación para que no truene al comparar versiones
    def __lt__(self, other): return str(self) < str(other)
    def __le__(self, other): return str(self) <= str(other)
    def __eq__(self, other): return str(self) == str(other)
    def __ne__(self, other): return str(self) != str(other)
    def __gt__(self, other): return str(self) > str(other)
    def __ge__(self, other): return str(self) >= str(other)

version.LooseVersion = DummyVersion
version.StrictVersion = DummyVersion
distutils.version = version

sys.modules["distutils"] = distutils
sys.modules["distutils.version"] = version

# Ahora ya puedes importar undetected_chromedriver sin errores
import undetected_chromedriver as uc


df_his = pd.read_excel(r'radioactiva_songs.xlsx')



import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)
driver.get('https://radios.com.co/radioactiva/')

time.sleep(5)

# Esperar hasta que la lista de canciones esté presente
items = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.playlist__item'))
)

canciones = []
for item in items:
    try:
        nombre = item.find_element(By.CSS_SELECTOR, '.playlist__song-name').text
        artista = item.find_element(By.CSS_SELECTOR, '.playlist__artist-name').text
        # tiempo = item.find_element(By.CSS_SELECTOR, '.playlist__time').text
        # portada = item.find_element(By.CSS_SELECTOR, '.playlist__img').get_attribute('src')

        canciones.append({
            'Canción': nombre,
            'Artista': artista
        })
    except:
        continue

time.sleep(5)

# input("Presiona Enter para cerrar...")
driver.quit()

# Pasar a DataFrame
df = pd.DataFrame(canciones)
del (canciones)

df = pd.concat([df_his, df])

df = df.drop_duplicates()

df.to_excel(r'radioactiva_songs.xlsx', index = False)


