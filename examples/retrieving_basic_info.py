from tqdm import tqdm
from youtube_scraper import Scraper
from bs4 import BeautifulSoup
import argparse
import time
import pickle
import ray 
parser = argparse.ArgumentParser(description="")
parser.add_argument("--url", help= "Video url")


def main(url):
    if url is None:
        url = "https://www.youtube.com/watch?v=9mtlSiKm3kg"
    
    my_scraper = Scraper(url)
    my_scraper.get_video_info()
    
    print(f"Video Title: {my_scraper.title.text}")
    print(f"Total Views: {my_scraper.count_views.text}")
    print(f"Total Likes: {my_scraper.count_likes.text}")
    print(f"Video Date: {my_scraper.date.text}")

    print(f"Channel Name: {my_scraper.channel_name.text}")
    print(f"Subscribers: {my_scraper.channel_subs.text}")

    with open("morning_glory_info.pkl","wb") as f:
        pickle.dump({
            "title":my_scraper.title.text,
            "total_views":my_scraper.count_views.text,
            "total_likes":my_scraper.count_likes.text,
            "date":my_scraper.date.text,
            "channel_name":my_scraper.channel_name.text,
            "subscribers":my_scraper.channel_subs.text
        },f)

    my_scraper.scroll_down(2)
    comments = my_scraper.get_video_comments()
    parsed_comments = my_scraper.parse_comments(comments)
    text_comments = my_scraper.get_comment_text(parsed_comments)

    for comment in tqdm(text_comments):
        print("Author: ")
        print(comment["author"])
        print("\n")
        print("Author URL: ")
        print(comment["author_url"])
        print("\n")
        print("Comment: ")
        print(comment["comment"])

    #saving data 
    my_scraper.save_comments(text_comments,"morning_glory_comments.pkl")
    
    my_scraper.close_driver()
    


if __name__ =="__main__":
    args = parser.parse_args()
    main(args.url)