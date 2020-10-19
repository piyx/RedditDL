# reddit_downloader
A simple script to download wallpapers from popular subreddits

## Usage
`python reddit.py <subreddit_name> [-category] [-limit]`

```
positional arguments:
  subreddit_name      Name of subreddit

optional arguments:
  -h, --help          show this help message and exit
  -category CATEGORY  Category (hot/top/new) [default=hot]
  -limit LIMIT        Number of images to download [default=10]
```

## Example
`python reddit.py wallpapers -category=top -limit=10`

## Output
```
Desktop\reddit-downloader> python reddit.py amoledbackgrounds -category=top -limit=10  
Downloading 10 of 10...
Download Completed Successffully!   
```

## Pics
![](imgs/op.png)


## Result
![](imgs/res.png)
