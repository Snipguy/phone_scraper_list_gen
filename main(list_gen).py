from calendar import month
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from persian_tools import digits
from docx import Document
from docx.shared import Pt
from docx2pdf import convert
from persiantools.jdatetime import JalaliDate
import os
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from datetime import datetime


chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-images")
# chrome_options.add_argument("user-data-dir=./cache")
driver = webdriver.Chrome(options=chrome_options)


logger = logging.getLogger('selenium')
t_prices = []
d_prices = []


digi_urls = {
    "A06-64-4" : r'https://www.digikala.com/product/dkp-16552148/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "A06-128-4" : r'https://www.digikala.com/product/dkp-16552147/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "A06-128-6" : r'https://www.digikala.com/product/dkp-16552106/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "A16-128-4" : r'https://www.digikala.com/product/dkp-17464125/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A16-128-6" : r'https://www.digikala.com/product/dkp-17464490/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A16-256-8" : r'https://www.digikala.com/product/dkp-17464492/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A25-128-6" : r'https://www.digikala.com/product/dkp-13980975/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a25-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A25-128-8" : r'https://www.digikala.com/product/dkp-13969539/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a15-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A25-256-8" : r'https://www.digikala.com/product/dkp-13981188/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a25-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85/',
    "A35-128-6" : r'https://www.digikala.com/product/dkp-14851168/گوشی-موبایل-سامسونگ-مدل-galaxy-a35-دو-سیم-کارت-ظرفیت-128-گیگابایت-رم-6-گیگابایت-clone-1-of-14521031/',
    "A35-128-8" : r'https://www.digikala.com/product/dkp-14851189/گوشی-موبایل-سامسونگ-مدل-galaxy-a35-دو-سیم-کارت-ظرفیت-128-گیگابایت-رم-6-گیگابایت-clone-1-of-14521031/',
    "A35-256-8" : r'https://www.digikala.com/product/dkp-14851182/گوشی-موبایل-سامسونگ-مدل-galaxy-a35-دو-سیم-کارت-ظرفیت-256-گیگابایت-رم-8-گیگابایت-ویتنام/',
    "A55-128-8" : r'https://www.digikala.com/product/dkp-14851820/گوشی-موبایل-سامسونگ-مدل-galaxy-a55-دو-سیم-کارت-ظرفیت-128-گیگابایت-و-رم-8-گیگابایت-clone-1-of-14717197/',
    "A55-256-8" : r'https://www.digikala.com/product/dkp-14851833/گوشی-موبایل-سامسونگ-مدل-galaxy-a55-دو-سیم-کارت-ظرفیت-256-گیگابایت-و-رم-8-گیگابایت-ویتنام/',
    "S23FE-256-8" : r'https://www.digikala.com/product/dkp-12924184/گوشی-موبایل-سامسونگ-مدل-galaxy-s23-fe-دو-سیم-کارت-ظرفیت-256-گیگابایت-و-رم-8-گیگابایت-ویتنام/',
    "Nokia-105" : r'https://www.digikala.com/product/dkp-2087200/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D9%88%DA%A9%DB%8C%D8%A7-%D9%85%D8%AF%D9%84-105-2019-ta-1174-ds-fa-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Nokia-106" : r'https://www.digikala.com/product/dkp-2261669/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D9%88%DA%A9%DB%8C%D8%A7-%D9%85%D8%AF%D9%84-2018-106-fa-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Nokia-106-2023" : r'https://www.digikala.com/product/dkp-15595047/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D9%88%DA%A9%DB%8C%D8%A7-%D9%85%D8%AF%D9%84-106-2023-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-clone-1-of-12376940/',
    "Nokia-210" : r'https://www.digikala.com/product/dkp-1705521/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D9%88%DA%A9%DB%8C%D8%A7-%D9%85%D8%AF%D9%84-210-fa-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA/',
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    "Note-13-4g-256-8": r'https://www.digikala.com/product/dkp-14272357/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Note-13-pro-4g-256-8": r'https://www.digikala.com/product/dkp-14271352/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Note-13-pro-4g-512-12": r'https://www.digikala.com/product/dkp-14271321/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-4g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Note-13-pro-5g-512-12": r'https://www.digikala.com/product/dkp-14176170/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-5g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Note-13-pro-plus-5g-256-8": r'https://www.digikala.com/product/dkp-14614745/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-plus-5g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Note-13-pro-plus-5g-512-12": r'https://www.digikala.com/product/dkp-14214205/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-plus-5g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Poco-X6-256-12": r'https://www.digikala.com/product/dkp-14192208/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-poco-x6-5g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Poco-X6-512-12": r'https://www.digikala.com/product/dkp-14411355/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-poco-x6-5g-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-clone-1-of-14192208/',
    "Poco-X6-pro-256-8": r'https://www.digikala.com/product/dkp-14116027/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-poco-x6-pro-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/',
    "Poco-X6-pro-512-12": r'https://www.digikala.com/product/dkp-14214794/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-poco-x6-pro-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/'
    # "": r'',
    # "": r''
}


techno_urls = {
    "A06-64-4" : r"https://www.technolife.ir/product-57991/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=1",
    "A06-128-4" : r"https://www.technolife.ir/product-57996/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=3",
    "A06-128-6" : r"https://www.technolife.ir/product-58573/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=2",
    "A06-64-4" : r"https://www.technolife.ir/product-57991/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-64-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=1",
    "A06-128-4" : r"https://www.technolife.ir/product-57996/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=3",
    "A06-128-6" : r"https://www.technolife.ir/product-58573/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a06-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA?query_id=3A10AB5F39519AC8&position=2",
    "A16-128-4" : r'https://www.technolife.ir/product-69646/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85?query_id=6D0F02CA7B8539E9&position=5',
    "A16-128-6" : r'https://www.technolife.ir/product-69647/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85?query_id=6D0F02CA7B8539E9&position=3',
    "A16-256-8" : r'https://www.technolife.ir/product-69649/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a16-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85?query_id=6D0F02CA7B8539E9&position=2',
    "A25-128-6" : r'https://www.technolife.ir/product-32539/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a25-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A25-128-8" : r'https://www.technolife.ir/product-32035/گوشی-موبايل-سامسونگ-مدل-galaxy-a25-5g-ظرفیت-128-گیگابایت-رم-8-گیگابایت---ویتنام',
    "A25-256-8" : r'https://www.technolife.ir/product-32034/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a25-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A35-128-6" : r'https://www.technolife.ir/product-49133/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a35-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-6-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A35-128-8" : r'https://www.technolife.ir/product-35828/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a35-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A35-256-8" : r'https://www.technolife.ir/product-31018/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-a35-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A55-128-8" : r'https://www.technolife.ir/product-35830/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%DA%AF%D9%84%DA%A9%D8%B3%DB%8C-a55-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "A55-256-8" : r'https://www.technolife.ir/product-31023/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%DA%AF%D9%84%DA%A9%D8%B3%DB%8C-a55-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "S23FE-256-8" : r'https://www.technolife.ir/product-29290/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%D9%85%D8%AF%D9%84-galaxy-s23-fe-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%88%DB%8C%D8%AA%D9%86%D8%A7%D9%85',
    "Nokia-105" : r'https://www.technolife.ir/product-52059/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D9%88%DA%A9%DB%8C%D8%A7-%D9%85%D8%AF%D9%84-2022-nokia-105-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA---ae',
    "Nokia-106" : r'https://www.technolife.ir/product-24143/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D9%86%D9%88%DA%A9%D9%8A%D8%A7-%D9%85%D8%AF%D9%84-106-(2018)-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D9%85%D9%88%D9%86%D8%AA%D8%A7%DA%98-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86',
    "Nokia-106-2023" : r'Not_Found',
    "Nokia-210" : r'https://www.technolife.ir/product-1032/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D9%86%D9%88%DA%A9%D9%8A%D8%A7-%D9%85%D8%AF%D9%84-210-(2019)-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-16-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA---%D8%B1%D9%85-16-%D9%85%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-',
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    "Note-13-4g-256-8": r'https://www.technolife.ir/product-33689/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Note-13-pro-4g-256-8": r'https://www.technolife.ir/product-33679/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Note-13-pro-4g-512-12": r'https://www.technolife.ir/product-33508/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Note-13-pro-5g-512-12": r'https://www.technolife.ir/product-29522/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Note-13-pro-plus-5g-256-8": r"Not_Found",
    "Note-13-pro-plus-5g-512-12": r'https://www.technolife.ir/product-34602/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%85%D8%AF%D9%84-redmi-note-13-pro-plus-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%A8%D9%87-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%B4%D8%A7%D8%B1%DA%98%D8%B1',
    "Poco-X6-256-12": r'https://www.technolife.ir/product-33517/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%BE%D9%88%DA%A9%D9%88-%D9%85%D8%AF%D9%84-x6-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Poco-X6-512-12": r'https://www.technolife.ir/product-32888/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%BE%D9%88%DA%A9%D9%88-%D9%85%D8%AF%D9%84-x6-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Poco-X6-pro-256-8": r'https://www.technolife.ir/product-38531/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D9%BE%D9%88%DA%A9%D9%88-%D9%85%D8%AF%D9%84-x6-pro-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA',
    "Poco-X6-pro-512-12": r'https://www.technolife.ir/product-32884/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D9%BE%D9%88%DA%A9%D9%88-%D9%85%D8%AF%D9%84-x6-pro-5g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-512-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA'
    # "": r'',
    # "": r''
}



xpath_for_black_techno = [
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[1]/div/p[contains(text() , "مشکی")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/p[contains(text() , "مشکی")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[3]/div/p[contains(text() , "مشکی")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[4]/div/p[contains(text() , "مشکی")]'
]
xpath_for_darkblue = [
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[1]/div/p[contains(text() , "سرمه‌ای")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/p[contains(text() , "سرمه‌ای")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[3]/div/p[contains(text() , "سرمه‌ای")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[4]/div/p[contains(text() , "سرمه‌ای")]'
]

xpath_for_white = [
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[1]/div/p[contains(text() , "سفید")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/p[contains(text() , "سفید")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[3]/div/p[contains(text() , "سفید")]',
    '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[1]/div/div[3]/div/div[2]/div/div/div/div/div[4]/div/p[contains(text() , "سفید")]'
]


xpath_for_price_techno = {
    '1': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[3]/div[2]/div/div/p',
    '2': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[5]/div/div/div/p',
    '3': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div[2]/div[3]/div[3]/div/div/div/p[2]',
    '4': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[3]/div/div/div/p',
    '5': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[4]/div/div/div/p',
    '6': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[2]/div/div/p[2]',
    '7': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[2]/div[2]/div/div/p',
    '8': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div/p',
    '9': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div[2]/div[3]/div[2]/div/div/div/p[2]',
    '10': '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[1]/div/div[2]/div[3]/div[4]/div/div/div/p[2]'
}

def check_internet_connection():
    # testing the connection by pinging google
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=5)
        return True
    except:
        return False

def wait_for_connection(max_retries=10, retry_delay=10):
    # waiting for user to reconnect the connection
    retries = 0
    while retries < max_retries:
        if check_internet_connection():
            if retries > 0:
                print("Internet is connected....")
            return True
        else:
            retries += 1
            print(f"No internet connection. Retrying in {retry_delay} seconds... ({retries}/{max_retries})")
            time.sleep(retry_delay)

    print("Failed to reconnect after multiple attempts.")
    return False


if len(digi_urls) != len(techno_urls):
    raise Exception("The number of urls for technolife and digikala are different")
else:
    urls_len = len(digi_urls)
    phone_models = []
    for key in digi_urls.keys():
        phone_models.append(key)
    # d_pbar = tqdm(total=urls_len)
    # t_pbar = tqdm(total=urls_len)
    # c_pbar = tqdm(total=100)
    # m_pbar = tqdm(total=3)

def deny(btn):
    try:
        # Wait for the 'deny' button to appear
        deny__btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "webpush-onsite"))
        )
        iframe = driver.find_element(By.ID, 'webpush-onsite')
        driver.switch_to.frame(iframe)
        
        # Try clicking the deny button
        try:
            # click(driver, (By.ID, "webpush-onsite"))
            deny__btn.click()
        except Exception as e:
            if isinstance(e, ElementClickInterceptedException):
                logger.debug("Debug : ElementClickInterceptedException")
            else:
                logger.debug(f"Debug : Exception occurred - {type(e).__name__}")
            
            try:
                # Try clicking with XPATH as fallback
                driver.find_element(By.XPATH, '//*[@id="deny"]').click()
            except Exception as inner_e:
                logger.debug(f"Debug : Failed to click deny button - {type(inner_e).__name__}")
                t_prices.append('//')
                print('*/')
                driver.implicitly_wait(500)
                return 1
        else:
            # Default action if deny button is clicked successfully
            btn.click()
    except TimeoutException:
        logger.debug("Debug : DenyButtonNotFound [In_Time]")
        t_prices.append('//')
        print('/*')
        return 1
    finally:
        # Switch back to the main content in all cases
        driver.switch_to.default_content()


def digi_scrape():
    for model , url in digi_urls.items():
        out_off_stock = True
        rang = False

        if url == r"Not_Found": 
            out_off_stock = True
            d_prices.append("**")
            print('**')
            continue


        if not wait_for_connection(max_retries=10, retry_delay=10):
            print("Could not establish connection. Exiting program.")
            return 
        else:
            driver.get(url)

        try:
            product_title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='pdp-title']"))
                )

            try:
                # driver.find_element(By.XPATH , '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[4]/div/div/div/button/div[2]/div')
                driver.find_element(By.XPATH , '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/div/h1/span')
            except NoSuchElementException:
                out_off_stock = False
            else:
                print(f"{model} **")
                d_prices.append('**')
                continue
            # checking for the colors available
            try:
                driver.find_element(By.CSS_SELECTOR, "[style='background: rgb(33, 33, 33);']").click()
            except NoSuchElementException:
                try:
                    driver.find_element(By.CSS_SELECTOR, "[style='background: rgb(0, 33, 113);']").click()
                except NoSuchElementException:
                    pass
                else:
                    rang = "Dark Blue"
            else:
                rang = "Black"

            if rang:
                print(model , rang, end=" ")
            else:
                print(model , end=" ")
            
            try:
                price_no_discount = driver.find_element(By.CSS_SELECTOR , '[data-testid="price-no-discount"]')
            except NoSuchElementException:
                try:
                    final_price_list = driver.find_elements(By.CSS_SELECTOR , '[data-testid="price-final"]')
                    price = final_price_list[1]
                except NoSuchElementException:
                    d_prices.append("//")
                    print('//')
            else:
                if "line-trough" in price_no_discount.get_attribute('class'):
                    final_price_list = driver.find_elements(By.CSS_SELECTOR , '[data-testid="price-final"]')
                    price = final_price_list[1]
                else:
                    price = price_no_discount
            

            if out_off_stock == False:
                if isinstance(price , str):
                    d_prices.append(price)
                    print(price)
                else:
                    final = digits.convert_to_en(price.text)
                    d_prices.append(final)
                    print(final)

        except TimeoutException:
            print(f"Failed to find the title for {model} within the given time.")
            d_prices.append('//')

        continue
        # d_pbar.update(1)
    driver.quit

percent = 100 / len(techno_urls)

# loading the page 
def techno_scrape():
    for model , url in techno_urls.items():
        print(model , end="---")

        if url == r"Not_Found": 
            out_off_stock = True
            t_prices.append("**")
            print('**')
            continue
    
        if not wait_for_connection(max_retries=10, retry_delay=10):
            print("Could not establish connection. Exiting program.")
            return 
        else:
            driver.get(url)

        try:
            product_title = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "pdp_name"))
                )
            

            try:
                out_off_stock = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/main/div/div/article[1]/section[2]/div/div[2]/div/div/div/div/div/p[contains (text() , "ناموجود")]')
            except NoSuchElementException:
                pass
            else:
                t_prices.append("**")
                print('**')
                continue

            rang = 'N/A'
            out_off_stock = False
            price = "//"



            # checking for the colors available
            try:
                black_btn = driver.find_element(By.CSS_SELECTOR, "[style='background-color:#1a1a1a'")
            except NoSuchElementException:
                try:
                    dark_blue_btn = driver.find_element(By.CSS_SELECTOR, "[style='background-color:#00009c']")
                except NoSuchElementException:
                    pass
                else:
                    try:
                        dark_blue_btn.click()                    
                    except ElementClickInterceptedException:
                        if deny(dark_blue_btn) == 1:
                            continue
                    finally:
                        rang = "DarkBlue"
            else:
                try:
                    black_btn.click()
                except ElementClickInterceptedException:
                    if deny(black_btn) == 1:
                        continue
                finally:
                    rang = "Black"


            # finding the price and scraping it
            for x in xpath_for_price_techno:
                try:
                    price = driver.find_element(By.XPATH , xpath_for_price_techno[x])
                except NoSuchElementException:
                    pass
                else:
                    break
        


            if out_off_stock == False:
                if isinstance(price, str):
                    t_prices.append(price)
                    print(price)
                else:
                    t_prices.append(price.text)
                    print(price.text)
            
        except TimeoutException:
                print(f"Failed to find the title for {model} within the given time.")
                t_prices.append('//')


        continue
        # t_pbar.update(1)
    driver.quit



def create_document():
    # creating the document and the row
    document = Document()
    table = document.add_table(rows=1, cols=3)

    # giving the style values

    style = document.styles['Normal']
    table.style = 'Table Grid'
    style.font.name = "Calibri" # type: ignore
    style.font.size = Pt(20) # type: ignore

    # The array of Phone model names , digikala prices , technolife prices


    hdr_cells = table.rows[0].cells
    hdr_cells[0].paragraphs[0].add_run('phone').bold = True
    hdr_cells[1].text = 'Digikala'
    hdr_cells[2].text = 'Technolife'

    for i in range(urls_len):
        row_cells = table.add_row().cells
        row_cells[0].paragraphs[0].add_run(phone_models[i]).bold = True
        row_cells[1].text = d_prices[i]
        row_cells[2].text = t_prices[i]

    today_date = str(JalaliDate.today())
    now_time = datetime.now().strftime("%H_%M")
    file_name = f"{today_date[5:]} {now_time}"
    path = today_date[:-3]


    if not os.path.exists(path):
        os.makedirs(path)

    doc_file = os.path.join(path, f"{file_name}.docx")
    document.save(doc_file)

    # Convert the document to PDF
    pdf_file = os.path.join(path, f'{file_name}.pdf')
    convert(doc_file, pdf_file)


    os.remove(doc_file)


def main():
    digi_start = time.time()
    digi_scrape()
    digi_end = time.time()
    print((digi_end - digi_start) / 60)
    # m_pbar.update(1)

    techno_start = time.time()
    techno_scrape()
    techno_end = time.time()
    print((techno_end - techno_start) / 60)


    # m_pbar.update(1)

    create_document()
    # m_pbar.update(1)



main()

