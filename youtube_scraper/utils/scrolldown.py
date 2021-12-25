from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time
import pickle 

class ScrollDown:
    def __init__(self, driver):
        self.driver = driver
        self.pause = 2
        self.comments = None

    def scrolldown(self):
        self.last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script(f"window.scrollTo(0,{4*self.last_height})")
            time.sleep(self.pause)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            
            if new_height==self.last_height:
                break

            self.last_height = new_height

    def getting_comments(self):
        self.comments = self.driver.find_elements_by_id('comment')
        return self.comments