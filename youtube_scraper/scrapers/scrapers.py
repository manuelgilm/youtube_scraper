from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time 

class Scraper:

    def __init__(self, URL):
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument("--headless")
        self.driver = webdriver.Firefox(options = self.option)
        self.driver.get(URL)
        time.sleep(10)
        self.get_video_info()

    def get_video_info(self):

        info_content = self.driver.find_element_by_id("info-contents")
        meta_content = self.driver.find_element_by_id("meta-contents")

        #info content
        class_name_info_content = "title.style-scope.ytd-video-primary-info-renderer"
        class_name_count_views = "view-count.style-scope.ytd-video-view-count-renderer"
        class_name_like_button = "style-scope.ytd-menu-renderer.force-icon-button.style-text"

        #meta content       
        self.title = info_content.find_element_by_class_name(class_name_info_content).text
        self.count_views = info_content.find_element_by_class_name(class_name_count_views).text
        self.count_likes = info_content.find_element_by_class_name(class_name_like_button).\
            find_element_by_id("text").text
        self.date = info_content.find_element_by_id("info-strings").text
        self.channel_name = meta_content.find_element_by_id("upload-info").find_element_by_id("channel-name").text
        self.channel_subs = meta_content.find_element_by_id("upload-info").find_element_by_id("owner-sub-count").text
        