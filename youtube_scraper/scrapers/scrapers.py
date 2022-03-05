from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from youtube_scraper.utils import times
import time 
import pickle
from tqdm import tqdm
from typing import List, Dict
from selenium.common.exceptions import TimeoutException

chrome_driver_path = "youtube_scraper/scrapers/chromedriver"

class Scraper:

    def __init__(self, URL:str)->None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                       chrome_options=self.options)
        self.driver.get(URL)

        try:
            element = WebDriverWait(self.driver, times.SHORT_TIME_10).until(EC.presence_of_element_located((By.ID,"info-contents")))
        except TimeoutException as e:
            print(e)


    def get_video_info(self)->None:

        info_content = self.driver.find_element_by_id("info-contents")
        meta_content = self.driver.find_element_by_id("meta-contents")

        #info content
        class_name_info_content = "title.style-scope.ytd-video-primary-info-renderer"
        class_name_count_views = "view-count.style-scope.ytd-video-view-count-renderer"
        class_name_like_button = "style-scope.ytd-menu-renderer.force-icon-button.style-text"

        #meta content       
        self.title = info_content.find_element(By.CLASS_NAME, class_name_info_content)
        self.count_views = info_content.find_element(By.CLASS_NAME,class_name_count_views)
        self.count_likes = info_content.find_element(By.CLASS_NAME,class_name_like_button).find_element(By.ID,"text")
        self.date = info_content.find_element(By.ID,"info-strings")

        self.channel_name = meta_content.find_element(By.ID,"upload-info").find_element(By.ID,"channel-name")
        self.channel_subs = meta_content.find_element(By.ID,"upload-info").find_element(By.ID,"owner-sub-count")

        self.channel_url = self.channel_name.find_element(By.CLASS_NAME,"yt-simple-endpoint.style-scope.yt-formatted-string")
        self.video_description = meta_content.find_element(By.ID,"description")

    def scroll_down(self, pause:int=2)->None:

        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight)") 
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def get_video_comments(self)->None:
        try:
            return self.driver.find_elements_by_tag_name('ytd-comment-thread-renderer')
        except Exception as e:
            return e

    def parse_comment(self, comment)->Dict:
        comment_obj = dict()
        comment_obj["comment"] = comment.find_element(By.ID, "content-text").get_attribute("innerHTML")
        comment_obj["author"] = comment.find_element(By.ID, "author-text").text
        comment_obj["author_url"] = comment.find_element(By.ID, "author-text").get_attribute("href")
        comment_obj["published"] = comment.find_element(By.ID, "header-author").find_element(By.CLASS_NAME,
                                     "published-time-text.above-comment.style-scope.ytd-comment-renderer").text
        comment_obj["likes"] = comment.find_element(By.ID, "vote-count-middle").text

        try:
            if comment.find_element(By.ID, "creator-heart-button"):
                comment_obj["author-heart"] = 1
        except:
            comment_obj["author-heart"] = 0

        return comment_obj

    def parse_comments(self, comments:List)->List[Dict]:
        if comments:
            comment_data = [
                self.parse_comment(comment) for comment in tqdm(comments, desc="Parsing comments")
            ]
            return comment_data
        raise Exception("No comments to parsed were found")

    def get_comment_text(self, comments:List[Dict])->List[Dict]:
        parsed_comments = comments.copy()
        for n,comment in tqdm(enumerate(parsed_comments), desc="Parsing HTML"):
            comment_soup = BeautifulSoup(comment["comment"],features="html.parser")
            parsed_comments[n]["comment"] = comment_soup.get_text()
        return parsed_comments

    def save_comments(self, data:List[Dict], path:str = "comments.pkl")->None:
        with open(path,"wb") as f:
            pickle.dump(data, f)