"""AwwPaper: Pull the daily top post from reddit.com/r/aww and set as wallpaper

Program will:
-Access reddit.com/r/aww/top
-Access link for top post
-Get image from imgur
-Set image as background wallpaper

Steps:
1. Download page for reddit.com/r/aww/top (requests)
2. Find element that holds link for top post (bs4)
3. Download that link (requests)
4. Find element with image URL (bs4)
5. Download image, write to file (iter_content)
6. Set as wallpaper background
7. Check every 24 hours for new update
8. Repeat steps

To run in the background:
In the terminal enter:
chmod +x dailyWallpaper.py
nohup /path/to/file.py &

To get PID for script:
In the terminal enter:
ps -A | grep -m1 dailyWallpaper.py | awk '{print $1}'
"""


import os
import sys
import bs4
import time
import ctypes
import requests
import datetime
import subprocess


def create_dir(directory):
    """Check to see if a directory exists. If not, create it.

    Args:
        directory: Name of the directory we want to check/create
    """

    dPath = os.getcwd() + '/' + directory + '/'
    os.makedirs(dPath, exist_ok=True)
    return dPath


def get_picture(redditURL):
    """Uses redditURL to find top post and download image from imgur

    Args:
        redditURL: link to reddit/r/aww/top
    """

    # Create unique user-agent for header to get into Reddit, download page
    headers = {'user-agent': 'Mac OSX:https://github.com/jmorales2012/AwwPaper\
    :v1 (by /u/IAmAmbitious)'}
    redditPage = requests.get(redditURL, headers=headers)
    redditPage.raise_for_status()

    # Parse reddit page, find top post, class='title may-blank'
    redditParsed = bs4.BeautifulSoup(redditPage.text, "html.parser")
    topPosts = redditParsed.select('a.title.may-blank')

    # Get the imgur URL inside top reddit post
    imgurURL = topPosts[0].get('href')

    # Download the imgur page from the URL above
    imgurPage = requests.get(imgurURL, headers=headers)
    imgurPage.raise_for_status()

    # Parse imgur page, find the image selector, and get the URL
    imgurParsed = bs4.BeautifulSoup(imgurPage.text, "html.parser")
    picElem = imgurParsed.select('a.zoom')
    picURL = 'http:' + picElem[0].get('href')

    # Download image from imgur
    print('Downloading pic from ' + picURL)
    topPic = requests.get(picURL)
    topPic.raise_for_status

    # Create folder & file and write in picture data
    filename = create_dir('wallpapers') + str(datetime.date.today())
    with open(filename, 'wb') as imageFile:
        for chunk in topPic.iter_content(100000):
            imageFile.write(chunk)

    return filename


def set_background(filename):
    """Set the top /r/aww image to background wallpaper

    Args:
        imageFile: Is the full path of the image downloaded in get_picture()
    """
    # Used for Mac OS X
    if sys.platform == 'darwin':

        SCRIPT = """/usr/bin/osascript<<END
        tell application "Finder"
        set desktop picture to POSIX file "%s"
        end tell
        """

        subprocess.Popen(SCRIPT % filename, shell=True)

    # Used for Windows
    elif sys.platform == 'win32':
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0,
                                                   filename)


if __name__ == '__main__':
        print('Downloading...')

        redditURL = 'https://www.reddit.com/r/aww/top/'

        filename = get_picture(redditURL)
        set_background(filename)

        # Read instructions at top to have file run as background process
        # Uncomment to have code run every 24 hours, and add 'while true' just
        # before line # 120
        # time.sleep(86400)
