from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time
import pickle 

option = webdriver.FirefoxOptions()
option.add_argument("--headless")

driver = webdriver.Firefox(options= option)
URL = "https://www.youtube.com/watch?v=oSulEWeZlPA"
driver.get(URL)

pause = 2
print("Scrolling down...")
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:

    driver.execute_script(f"window.scrollTo(0, {4*last_height})") 

    time.sleep(pause)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    if new_height == last_height:
        break

    last_height = new_height

comments = driver.find_elements_by_id('comment')

comment_data = {
    "comment":[],
    "author":[],
    "author_url":[]
}

print("Printing comments")
for comment in comments:

    try:
        comment_data["comment"].append(comment.find_element_by_id("body").find_element_by_id("expander").find_element_by_id("content-text").text)
        comment_data["author"].append(comment.find_element_by_id("body").find_element_by_id("author-text").find_element_by_class_name("style-scope.ytd-comment-renderer").text)
        comment_data["author_url"].append(comment.find_element_by_id("body").find_element_by_id("author-thumbnail").find_element_by_class_name(
                'yt-simple-endpoint.style-scope.ytd-comment-renderer').get_attribute("href"))

        print("\n")
        print(comment_data["author_url"][-1])
        print(comment_data["author"][-1])
        print(comment_data["comment"][-1])

    except:
        print(comment)

with open("comment_data.pkl","wb") as f:
    pickle.dump(comment_data, f)