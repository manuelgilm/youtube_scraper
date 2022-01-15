from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time 
import pickle

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

    def get_video_comments(self):
        pause = 2
        print("Scrolling down...") # change for logger
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            self.driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight)") 
            time.sleep(pause)

            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height

        comments = self.driver.find_elements_by_id('comment')

        return comments

    def parse_comments(self):
        comments = self.get_video_comments()

        comment_data = {
            "comment":[],
            "author":[],
            "author_url":[]
        }

        print("Saving comments")
        for comment in comments:

            try:
                comment_data["comment"].append(comment.find_element_by_id("body").find_element_by_id("expander").find_element_by_id("content-text").text)
                comment_data["author"].append(comment.find_element_by_id("body").find_element_by_id("author-text").find_element_by_class_name("style-scope.ytd-comment-renderer").text)
                comment_data["author_url"].append(comment.find_element_by_id("body").find_element_by_id("author-thumbnail").find_element_by_class_name(
                        'yt-simple-endpoint.style-scope.ytd-comment-renderer').get_attribute("href"))

            except Exception as e:
                print(e)
                

        with open("comment_data.pkl","wb") as f:
            pickle.dump(comment_data, f)

