from reddit import RedditClientManager
from reddit import download_post
from PyInquirer import prompt
from reddit import Category
import concurrent.futures
from pathlib import Path
import time
import sys
import os


def ask_subreddit():
    question = {
        'type': 'input',
        'name': 'subreddit',
        'message': 'Enter the name of the subreddit:'
    }

    return prompt(question)['subreddit']


def select_category():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'Select a category',
        'choices': [
            Category.HOT.value,
            Category.TOP.value,
            Category.NEW.value
        ]
    }
    return prompt(options)['choice']


def ask_limit():
    question = {
        'type': 'input',
        'name': 'limit',
        'message': 'How many images do you want to download?',
        'validate': lambda val: val.isdigit() or 'Please Enter a number!'
    }

    return prompt(question)['limit']


def ask_download_path():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'Where do you want to download the song?',
        'choices': [
            '1.Current folder',
            '2.Create a new folder here and download',
            '3.Enter a custom download path',
            '4.Exit'
        ]
    }

    choice = prompt(options)['choice']
    if '1' in choice:
        return os.getcwd()

    elif '2' in choice:
        ques = {
            'type': 'input',
            'name': 'folder',
            'message': 'Enter a folder name:'
        }
        folder = prompt(ques)['folder']
        if not os.path.exists(folder):
            os.mkdir(folder)

        return folder

    elif '3' in choice:
        ques = {
            'type': 'input',
            'name': 'path',
            'message': 'Enter path where images should be downloaded:'
        }

        return prompt(ques)['path']

    else:
        sys.exit()


def main():
    subreddit = ask_subreddit()
    category = select_category()
    limit = int(ask_limit())
    path = ask_download_path()

    if not os.path.exists(path):
        print('Invalid path')
        return

    os.chdir(Path(path))

    client_manager = RedditClientManager()
    reddit = client_manager.reddit_client

    getposts = getattr(reddit.subreddit(subreddit), category)

    imgs_downloaded = 0
    start = time.perf_counter()

    processes = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, post in enumerate(getposts(limit=limit), 1):
            processes.append(executor.submit(download_post, post.url, i))

    end = time.perf_counter()

    for p in concurrent.futures.as_completed(processes):
        imgs_downloaded += int(p.result())

    print(f"Complete! Downloaded {imgs_downloaded} of {limit} imgs.", end="")
    print(f"It took {end-start} seconds.")


if __name__ == "__main__":
    main()
