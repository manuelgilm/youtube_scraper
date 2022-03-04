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
    # Use explicity wait to wait for [id="info-contents"]
    my_scraper.get_video_info()
    
    print(f"Video Title: {my_scraper.title.text}")
    print(f"Total Views: {my_scraper.count_views.text}")
    print(f"Total Likes: {my_scraper.count_likes.text}")
    print(f"Video Date: {my_scraper.date.text}")

    print(f"Channel Name: {my_scraper.channel_name.text}")
    print(f"Subscribers: {my_scraper.channel_subs.text}")

    my_scraper.scroll_down(3)
    comments = my_scraper.get_video_comments()
    parsed_comments = my_scraper.parse_comments(comments)

    for comment in parsed_comments:
        
        print(comment["author"])
        soup = BeautifulSoup(comment["comment"])
        print(soup.get_text())
        print("-"*100)
    


if __name__ =="__main__":
    args = parser.parse_args()
    main(args.url)