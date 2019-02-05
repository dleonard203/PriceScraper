# PriceScraper
Python 3 code that scrapes Amazon (and eventually more) for prices


## Setup
1.) Download [Google Chrome](https://www.google.com/chrome/)

2.) Download [Chome web driver](http://chromedriver.chromium.org/downloads)
  - Note where this is downloaded to. You will need this for configuration. A good place is C:/Program Files/

3.) Download [Python3](https://www.python.org/downloads/)

4.) requirements.txt includes all required python libraries and versions. I would recomend creating a new [virtualenv](https://virtualenv.pypa.io/en/latest/installation/), activating it, and calling the following in the terminal of the requirements.txt directory: 
```
pip install -r requirements.txt
``` 
5.) Prevent websites from detecting the fact that you are using selenium with [this helpful article](http://danlec.com/st4k#questions/33225947) by updating your ket in the chrome driver binary (editable with Notepad++)

## config.json

This configuration file has 3 paraemters the user must set before use.
1.) *items* is a list of strings. Each string is an item to be monitored.
2.) *sleep_minutes* is an integer, the amount of time to sleep before taking each value
3.) *chromedriver_path* is the file path to your Chrome Webdriver from step 2 (ex; "C:/Program Files/GoogleWebDriver")

## Using the PriceScraper

Once all setup steps have been performed and the config.json file has your local parameters, it is time to the the PriceScraper. Bring up a new terminal. If you are using virtualenv, activate it. Change directories to where you dowload PriceScraper to. In the terminal, run :
```
python server.py
```

## Graphing the results

Once you have one or more data points, you can generate plotly offline html charts to show the price at every known time point. With your virtualenv active (if applicable), change to the directory of PriceScraper in your terminal. Run:
```python make_graphs.py``` One graph per item in the config file will be in the PriceScraper directory.


## Clearing your databases

PriceScraper uses TinyDB, a JSON based data storage library to hang on to results between sessions. If you want to clear your database, run ```python empty_dbs.py``` in the directory of your PriceScraper.

## How it works

Popular websites often block html parsers (for example, Amazon blocks Python's requests library's 'get' function). This makes it hard to scrape certain websites. This is where Selenium comes in. Selenium acts as a layer between Python and Chrome's Web Driver to programatically navigate web pages. After *sleep_minutes* number of minutes from config.json, a new Chrome window is opened with Selenium. The window navigates to Amazon, searches for your item in the window, and scrapes the current price from the first result. This result is then stored in a [TinyDB](https://tinydb.readthedocs.io/en/latest/). The program sleeps, then does it again. This tool is meant to help find the best time to buy your favorite products!

## Future improvements

A Chrome window physically pops up when the PriceScraper reaches amazon. This can be disruptive to everyday computer use. Its recomended that this program is run while no one is using the machine. Doing this prevents the browser from being run in headless_mode, which is another way for websites to detect that a non-human is navigating their website. I want to look into making this appear as a pop-under so that it is barely noticeable.

Amazon is currently the only website being monitored. I want to eventually have a list of acceptable websites depending on what you want to monitor (ex; BestBuy, eBay, NewEgg).

Amazon's top result for your items can be influenced by advertisements and sponsorships. This means that you are not guaranteed to get the price for the same item every time. If Amazon supports your item's SKU, that is the best way to search items.
