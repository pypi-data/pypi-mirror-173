from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
from quickcsv import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

class Bot:
    def __init__(self,chromedriver_path='browsers/chromedriver.exe'):
        self.chromedriver_path=chromedriver_path

    def start(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.headless = False
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path,
                                  chrome_options=options
                                  )

        self.driver.implicitly_wait(1)

    def click_by_class(self,class_name):
        ele = self.driver.find_element(by=By.CLASS_NAME, value=class_name)
        ActionChains(self.driver).click(ele).perform()

    def open(self,url):
        self.driver.get(url)

    def wait(self,seconds=10):
        time.sleep(seconds)

    def get_html_obj(self):
        html = self.driver.find_element(by=By.TAG_NAME, value='html')
        html_str = html.get_attribute("outerHTML")
        html_obj = BeautifulSoup(html_str, features='lxml')
        return html_obj

    def get_html_str(self):
        html = self.driver.find_element(by=By.TAG_NAME, value='html')
        html_str = html.get_attribute("outerHTML")
        return html_str

    def close(self):
        self.driver.close()


