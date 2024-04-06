How to know if a piece of python code is working 
```
ps aux | grep python
```

How to kill a running program 
```
sudo pkill -f v5.py
```
Sample Output 
```
vishal@raspberrypi:~ $ ps aux | grep python
root         571  0.0  0.1  12172  4480 ?        S    11:22   0:00 sudo python3 /home/vishal/v5.py
root         583  3.1  1.8 742828 73676 ?        Sl   11:23   0:08 python3 /home/vishal/v5.py
vishal       978  0.2  0.9  62492 36504 ?        S    11:23   0:00 /usr/bin/python3 /usr/share/system-config-printer/applet.py
vishal      1819  0.0  0.0   6044  1920 pts/1    S+   11:27   0:00 grep --color=auto python
vishal@raspberrypi:~ $ sudo pkill -f v5.py
vishal@raspberrypi:~ $ ps aux | grep python
vishal       978  0.1  0.9  62492 36504 ?        S    11:23   0:00 /usr/bin/python3 /usr/share/system-config-printer/applet.py
vishal      1863  0.0  0.0   6044  2048 pts/1    S+   11:28   0:00 grep --color=auto python
vishal@raspberrypi:~ $ 
```
