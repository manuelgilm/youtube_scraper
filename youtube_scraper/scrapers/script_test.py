from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time 
import pickle

driver_path = "youtube_scraper/scrapers/chromedriver"
driver_path = "geckodriver"
URL = "https://www.youtube.com/watch?v=9mtlSiKm3kg"
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument('start-maximized')
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Firefox(executable_path=driver_path, options=options)
driver.get(url=URL)
print("Scrolling down...")

for n in range(10):
    driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight)")
    time.sleep(3)

comments = driver.find_elements_by_tag_name('ytd-comment-thread-renderer')

comment_data = {
    "comment":[],
    "author":[],
    "author_url":[]
}

print("Printing comments")
for comment in comments:

    comment_data["comment"].append(comment.find_element_by_id("comment")
    .find_element_by_id("body")
    .find_element_by_id("main")
    .find_element_by_id("expander")
    .find_element_by_id("content")
    .find_element_by_id("content-text").get_attribute('innerHTML'))

    comment_data["author"].append(comment.find_element_by_id("comment")
    .find_element_by_id("body")
    .find_element_by_id("main")
    .find_element_by_id("header")
    .find_element_by_id("header-author")
    .find_element_by_id("author-text").text)

    comment_data["author_url"].append(comment.find_element_by_id("comment")
    .find_element_by_id("body")
    .find_element_by_id("main")
    .find_element_by_id("header")
    .find_element_by_id("header-author")
    .find_element_by_id("author-text").get_attribute("href"))


print(len(comment_data["comment"]))
with open("comments_with_new_method.pkl","wb") as f:
    pickle.dump(comment_data, f)

for comment, author, url in zip(comment_data["comment"],comment_data["author"],comment_data["author_url"]):
    print(author)
    print("\n")
    print(comment)
    print("\n")
    print(url)
    print("\n")
    print("\n")
    print("\n")