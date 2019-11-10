# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import browser

from selenium import webdriver

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_mission ={}

# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

# Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find("div", class_="content_title").find('a').text
    news_p = soup.find("div", class_="rollover_description_inner").text

# Visit the url for JPL Featured Space Image
    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

# Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find_all('img')[5]["src"]
    featured_img_url = "https://jpl.nasa.gov" + image
    print(featured_img_url)

#  scrape the latest Mars weather tweet from the page
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)


# Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
# getting mars weather
    mars_weathers=[]                                            

    for weather_info in soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'):
        mars_weathers.append(weather_info.text.strip())  
    mars_weather = mars_weathers[0]
    mars_weather

# Visit the Mars Facts webpage
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

# Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

# getting mars facts table
    mars_facts = pd.read_html(url4)[0]
    mars_facts.columns = ["Description","Value"]
    mars_facts_html = mars_facts.to_html()
    mars_facts_html.replace('\n', '')

    mars_facts.to_html('mars_table.html')

# Mars hemisphere name and images 
    url5 = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    
    hemisphere_img_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text  

    # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(url5 + hemisphere_link)        
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')        
        img_link = img_soup.find('div', class_='downloads')
        img_url = img_link.find('li').a['href']

    # Create Dictionary to store title and url info
        img_dict = {}
        img_dict['title'] = title
        img_dict['img_url'] = img_url        
        hemisphere_img_urls.append(img_dict)

    mars_mission = {"news_title": news_title,
                   "news_p": news_p,
                   "featured_image_url":featured_img_url,
                   "mars_weather": mars_weather,
                   "mars_facts_table": str(mars_facts_html),
                   "hemisphere_img": hemisphere_img_urls
                    }
    return mars_mission