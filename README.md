# TinderBot
Tinder swipe bot

A bot which swipes Tinder for you!

## Requirements
 - Python 3
 - install chromedriver, and set the path to chromedriver in `tinderbot.py`:
    - chromedriver_loc =`C:\path\to\chromedriver.exe`
    - Download: (chromedriver)[https://chromedriver.chromium.org/downloads]
 - `pip install -r requirements.txt`

create a secrets.py file with variables:
```
 username = 'your_username'
 password = 'your_password'
```

## How to use
```
from tinderbot import TinderBot
tb = TinderBot()
tb.login()
tb.auto_swipe()
```
