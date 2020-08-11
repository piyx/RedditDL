import os
import praw
from collections import namedtuple
import urllib.request
from secret import CLIENT_ID, CLIENT_SECRET, USER_AGENT

Post = namedtuple('Post', ['name', 'url'])


class Reddit:
    def __init__(self, client, subreddit):
        self.reddit_client = client
        self.subreddit = subreddit
        self.posts = []

    def get_posts(self, amount=10):
        subreddit = self.reddit_client.subreddit(self.subreddit)
        for submission in subreddit.top(limit=amount):
            post = Post(submission.title, submission.url)
            self.posts.append(post)

    def download_posts(self):
        # path where images will be downloaded
        path = "C:/Users/razor/Downloads/imgs/"
        NUM_IMAGES = len(self.posts)
        for i, post in enumerate(self.posts, 1):
            ext = os.path.splitext(post.url)[-1]
            if not ext:
                print(f"Post {i} is not an image!")
            else:
                print(f"\rDownloading image {i} of {NUM_IMAGES}...", end="")
                urllib.request.urlretrieve(post.url, path+post.name+ext)


def main():
    # reddit instance
    reddit_client = praw.Reddit(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                user_agent=USER_AGENT)

    subreddit = input("Enter subreddit: ")
    amount = int(input("Enter num images: "))
    reddit = Reddit(reddit_client, subreddit)
    reddit.get_posts(amount=amount)
    reddit.download_posts()


if __name__ == "__main__":
    main()
