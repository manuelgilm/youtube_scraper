from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time 

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