from youtube_scraper import Scraper
import argparse
import time
import pickle

parser = argparse.ArgumentParser(description="")
parser.add_argument("--url", help= "Video url")


def main(url):
    if url is None:
        url = "https://www.youtube.com/watch?v=9mtlSiKm3kg"
    
    my_scraper = Scraper(url)
    time.sleep(15)
    my_scraper.get_video_info()

    print(f"Video Title: {my_scraper.title.text}")
    print(f"Total Views: {my_scraper.count_views.text}")
    print(f"Total Likes: {my_scraper.count_likes.text}")
    print(f"Video Date: {my_scraper.date.text}")

    print(f"Channel Name: {my_scraper.channel_name.text}")
    print(f"Subscribers: {my_scraper.channel_subs.text}")

    my_scraper.parse_comments()
    

if __name__ =="__main__":
    args = parser.parse_args()
    main(args.url)