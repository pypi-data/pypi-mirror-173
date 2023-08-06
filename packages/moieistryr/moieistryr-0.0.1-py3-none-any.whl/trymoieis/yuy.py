import random
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random as r
import numpy as n



def t():


		a = webdriver.Chrome(ChromeDriverManager().install())
		a.get('https://www.instagram.com/')
