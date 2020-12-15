from urllib.error import HTTPError
from urllib.request import urlopen
import praw
import enum
import os


class Category(enum.Enum):
    HOT = "hot"
    TOP = "top"
    NEW = "new"


class RedditClientManager:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")

    @property
    def reddit_client(self):
        '''
        Return reddit client
        '''
        return praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent
        )


def download_post(post_url: str, img_name: str) -> None:
    '''
    Downloads the image from the given url
    '''
    extension = os.path.splitext(post_url)[-1]

    if not extension:
        return False

    try:
        img_data = urlopen(post_url).read()
        with open(f'{img_name}{extension}', 'wb') as img:
            img.write(img_data)
            return True

    except (HTTPError, WindowsError):
        return False
