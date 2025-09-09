# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 10:15:42 2025

@author: FPC

Tomar canciones de la página de radios.com de la radio radioacktiva.
"""

# input("Presiona Enter para continuar...")

# import os
# import glob # built-in
import time

time.sleep(10)

# import sys
# import pyautogui
# import shutil
import pandas as pd

# from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys

# from urllib.parse import quote # codificar usuario y contraseña

# import pyautogui


df_his = pd.read_excel(r'radioactiva_songs.xlsx')



chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("window-size=1200x600")
chromeOptions.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chromeOptions)

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


