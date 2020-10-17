# Inspired by Destaq --> https://github.com/Destaq

import praw
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import os

# Store your client secrets in a new file and import it
from secret import CLIENT_ID, CLIENT_SECRET, USER_AGENT

# clear screen (use 'clear' for linux)
os.system('cls')

# image limit
NUM_IMAGES = int(input("Enter number of images to download: "))


# getting submission links
def get_post_link(subreddit):
    post_links = []
    parent = "https://www.reddit.com"

    for submission in subreddit.top(limit=NUM_IMAGES):
        post_links.append(parent + submission.permalink)

    return post_links


# get relevant image name
def get_image_names(post_links, image_links):
    names = [link.split('/')[-2] for link in post_links]
    extensions = [link.split('.')[-1] for link in image_links]
    return [name + '.' + ext for name, ext in zip(names, extensions)]


# retrieve image links from post links
def get_image_link(post_links):
    image_links = []
    img_link_pattern = "https://i.redd.it/"

    for i, link in enumerate(post_links, 1):
        print(f"\rProcessing image {i} of {NUM_IMAGES}...", end="")
        try:
            req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')
            for hyplink in soup.findAll('a'):
                if img_link_pattern in hyplink.get("href"):
                    image_links.append(hyplink.get("href"))
        except Exception as e:
            print(e)

    return image_links


os.system('cls')


# download images if not downloaded before
def download_images(images_links, image_names):

    # path where images will be downloaded
    path = "C:/Users/razor/Downloads/imgs/"
    downloaded_images = os.listdir(path)
    i = 1
    for link, name in zip(images_links, image_names):
        print(f"\rDownloading image {i} of {NUM_IMAGES}...", end="")
        if name in downloaded_images:
            continue
        else:
            try:
                urllib.request.urlretrieve(link, path+name)
            except Exception as e:
                print(e)
        i += 1

    print("\nAll files downloaded sucessfully!")


def main():

    # reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)

    # subreddit
    subreddit = reddit.subreddit("Amoledbackgrounds")

    post_links = get_post_link(subreddit)
    image_links = get_image_link(post_links)
    image_names = get_image_names(post_links, image_links)
    download_images(image_links, image_names)


if __name__ == "__main__":
    main()
