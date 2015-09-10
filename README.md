Daily Wallpaper

Pulls the top post from reddit.com/r/aww every 24 hours and sets the picture as your desktop background.

Program will pull top post from reddit.com/r/aww/top and set as background
image anytime it is run.

**To make the program run in the background every 24 hours, follow steps below:

1. Make script an executable. Type the following in the terminal:
chmod +x dailyWallpaper.py

2. Make the program run in the background even when terminal is closed. Type:
nohup /path/to/dailyWallpaper.py &

3. Uncomment line # 130


**To kill the program:

1. Get the PID for the program. Type the following in the terminal:
ps -A | grep -m1 dailyWallpaper.py | awk '{print $1}'

2. Kill the process. Type into terminal:
kill -9 <PID>
