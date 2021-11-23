from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Scraper:

    def __init__(self, URL):
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument("--headless")

        self.driver = webdriver.Firefox(options = self.option)
        self.driver.get(URL)

    def get_video_info(self):

        info_content = self.driver.find_element_by_id("info-contents")

        class_name_info_content = "title.style-scope.ytd-video-primary-info-renderer"
        class_name_count_views = "view-count.style-scope.ytd-video-view-count-renderer"
        class_name_like_button = "style-scope.ytd-menu-renderer.force-icon-button.style-text"

        self.title = info_content.find_element_by_class_name(class_name_info_content)
        self.count_views = info_content.find_element_by_class_name(class_name_count_views)
        self.count_likes = info_content.find_element_by_class_name(class_name_like_button).\
            find_element_by_id("text")


my_scraper = Scraper("https://www.youtube.com/watch?v=1rk3JiMFcmc")
my_scraper.get_video_info()
print(my_scraper.title.text)
print(my_scraper.count_views.text)
print(my_scraper.count_likes.text)



