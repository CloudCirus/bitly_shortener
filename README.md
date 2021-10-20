# Bitly shortener

## About <a name = "about"></a>

Script use [bitly.com](https://bitly.com/) API. Input url to convert it to short bitlink, or input bitlink to see all clicks.

## Getting Started <a name = "getting_started"></a>

### Installing

Python3 should be already installed.

Use pip to install requirements.

```
pip install -r requirements.txt
```

Your need your bitly [access token](https://gist.github.com/dvmn-tasks/58f5fdf7b8eb61ea4ed1b528b74d1ab5#Authentication). 

Create in **.env** file in project directory. Declare **BITLY_TOKEN** variable with acces token, like: *9aaAA9a9999a9a999a99a9999a9a9AA99aa99aa99*

Use for linux:
```
echo BITLY_TOKEN=input your token inside this command > .env
```

### Running

```
python3 links.py someurl.com
```
Where someurl.com can be url like: google.com or https://google.com for get short bitlink.

Or it can be bitlink like: bit.ly/AAAaaA or https://bit.ly/AAAaaA for count all clicks. 

## Project goals <a name = "project_goals"></a>

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
