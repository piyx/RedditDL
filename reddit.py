import os
import sys
import praw
import argparse
from urllib.error import HTTPError
from urllib.request import urlopen

ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
AGENT = os.getenv("REDDIT_USER_AGENT")


class Reddit:
    def __init__(self, client, subreddit, category):
        self.client = client
        self.subreddit = subreddit
        self.category = category
        self.path = "C:/Users/ctrla/Downloads/imgs/"
        self.posts = []

    def get_posts(self, amount=10):
        try:
            subreddit = self.client.subreddit(self.subreddit)
            if self.category == "top":
                submissions = subreddit.top(limit=amount)
            elif self.category == 'new':
                submissions = subreddit.new(limit=amount)
            else:
                submissions = subreddit.hot(limit=amount)

            for submission in submissions:
                self.posts.append(submission.url)
        except:
            print(f"{subreddit} subreddit could not be found!")
            sys.exit()

    def download_posts(self):
        n = len(self.posts)
        os.chdir(self.path)
        for i, url in enumerate(self.posts):
            print(f"\rDownloading {i+1} of {n}...", end="")
            try:
                data = urlopen(url).read()
                ext = os.path.splitext(url)[-1]
                if not ext:
                    continue
                with open(f"image{i+1}{ext}", 'wb') as f:
                    f.write(data)
            except HTTPError:
                print("\rHTTP Error 500!", end="")

        print("\rDownload Completed Successfully!", end="")


def main():
    # reddit instance
    reddit = praw.Reddit(client_id=ID,
                         client_secret=SECRET,
                         user_agent=AGENT)

    parser = argparse.ArgumentParser()
    parser.add_argument('subreddit_name', type=str, help="Name of subreddit")
    parser.add_argument('-category', type=str, default='hot',
                        help="Category (hot/top/new) [default=hot]")
    parser.add_argument('-limit', type=int, default=10,
                        help="Number of images to download [default=10]")

    args = parser.parse_args()
    subreddit = args.subreddit_name
    category = args.category
    limit = args.limit

    reddit = Reddit(reddit, subreddit, category)
    reddit.get_posts(amount=limit)
    reddit.download_posts()


if __name__ == "__main__":
    main()
