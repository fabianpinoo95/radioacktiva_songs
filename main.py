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

# parche para que librerías viejas que buscan distutils no fallen en Python 3.13
sys.modules["distutils"] = types.ModuleType("distutils")
sys.modules["distutils.version"] = types.ModuleType("version")
sys.modules["distutils.version"].LooseVersion = lambda x: x
sys.modules["distutils.version"].StrictVersion = lambda x: x

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


