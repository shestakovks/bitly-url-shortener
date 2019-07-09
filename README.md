# Bitly url shortener

Python3 script that does two things:
1. Shortens the long URLs using [bit.ly](https://bitly.com/) service
2. Shows click statistics for your short links

## How to install

1. Register on [bit.ly](https://bitly.com/)
2. Get Generic Access Token (<b>Your Account - Edit Profile - Generic Access Token</b>). Token looks like this: ```0w2d1g29w43q936218ed0q1dq4y7hg8fd23563rn```
3. Create file ```.env``` in the directory with this script and put there your Generic Access Token. ```.env``` file should look like this
```
TOKEN=0w2d1g29w43q936218ed0q1dq4y7hg8fd23563rn
```
but with your token instead of presented above.

4. Python3 should be already installed. The script was made using `Python 3.7.3`. This version or higher should be fine.

5. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## How to use

Depending of what you will give to script as an argument you can get following results:
```
$ python3 main.py https://dvmn.org
Short link: http://bit.ly/2xF8G6k
```
```
$ python3 main.py http://bit.ly/2xF8G6k
Number of clicks: 2
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
