from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import selenium.webdriver.support.ui as ui
import time 
import pickle
from tqdm import tqdm

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

chrome_driver_path = "youtube_scraper/scrapers/chromedriver"

class Scraper:

    def __init__(self, URL):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                       chrome_options=self.options)
        self.driver.get(URL)


    def get_video_info(self):

        info_content = self.driver.find_element_by_id("info-contents")
        meta_content = self.driver.find_element_by_id("meta-contents")

        #info content
        class_name_info_content = "title.style-scope.ytd-video-primary-info-renderer"
        class_name_count_views = "view-count.style-scope.ytd-video-view-count-renderer"
        class_name_like_button = "style-scope.ytd-menu-renderer.force-icon-button.style-text"

        #meta content       
        self.title = info_content.find_element_by_class_name(class_name_info_content)
        self.count_views = info_content.find_element_by_class_name(class_name_count_views)
        self.count_likes = info_content.find_element_by_class_name(class_name_like_button).\
            find_element_by_id("text")
        self.date = info_content.find_element_by_id("info-strings")

        self.channel_name = meta_content.find_element_by_id("upload-info").find_element_by_id("channel-name")
        self.channel_subs = meta_content.find_element_by_id("upload-info").find_element_by_id("owner-sub-count")

        self.channel_url = self.channel_name.find_element_by_class_name("yt-simple-endpoint.style-scope.yt-formatted-string")
        self.video_description = meta_content.find_element_by_id("description")

    def scroll_down(self, pause=3):
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight)") 
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_video_comments(self):
        try:
            return self.driver.find_elements_by_tag_name('ytd-comment-thread-renderer')
        except Exception as e:
            return e

    def parse_comment(self, comment):
        comment_obj = dict()

        comment_obj["comment"] = (comment.find_element_by_id("comment")
        .find_element_by_id("body")
        .find_element_by_id("main")
        .find_element_by_id("expander")
        .find_element_by_id("content")
        .find_element_by_id("content-text").get_attribute('innerHTML'))

        comment_obj["author"] = (comment.find_element_by_id("comment")
        .find_element_by_id("body")
        .find_element_by_id("main")
        .find_element_by_id("header")
        .find_element_by_id("header-author")
        .find_element_by_id("author-text").text)

        comment_obj["author_url"] = (comment.find_element_by_id("comment")
        .find_element_by_id("body")
        .find_element_by_id("main")
        .find_element_by_id("header")
        .find_element_by_id("header-author")
        .find_element_by_id("author-text").get_attribute("href"))

        return comment_obj

    def parse_comments(self, comments):
        print(f"There are: {len(comments)}")
        comment_data = []
        for comment in tqdm(comments, desc="Parsing Comments"):
            try:
                comment_data.append(self.parse_comment(comment))
            except Exception as e:
                print(e)

        return comment_data

    def save_comments(self, data, path = "comments.pkl"):
        with open(path,"wb") as f:
            pickle.dump(data, f)


