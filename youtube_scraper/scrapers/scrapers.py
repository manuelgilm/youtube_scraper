from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time 

class Scraper:

    def __init__(self, URL):
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument("--headless")

        self.driver = webdriver.Firefox(options = self.option)

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
        self.date = info_content.find_element_by_id("text")

        self.channel_name = meta_content.find_element_by_id("upload-info").find_element_by_id("channel-name")
        self.channel_subs = meta_content.find_element_by_id("upload-info").find_element_by_id("owner-sub-count")

        self.channel_url = self.channel_name.find_element_by_class_name("yt-simple-endpoint.style-scope.yt-formatted-string")
        self.video_description = meta_content.find_element_by_id("description")



my_scraper = Scraper("https://www.youtube.com/watch?v=9mtlSiKm3kg")
time.sleep(15)
my_scraper.get_video_info()

print(my_scraper.title.text)
print(my_scraper.count_views.text)
print(my_scraper.count_likes.text)
print(my_scraper.date.text)

print(my_scraper.channel_name.text)
print(my_scraper.channel_url.get_attribute("href"))
print(my_scraper.channel_subs.text)
print(my_scraper.video_description.text)



