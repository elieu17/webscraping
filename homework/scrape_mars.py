#!/usr/bin/env python
# coding: utf-8

# In[15]:


from splinter import Browser 
from bs4 import BeautifulSoup as bs
import time
import numpy as np
import pandas as pd
import collections


# In[2]:


# Visit URL
browser = Browser('chrome')

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path)


# In[3]:


def scrape_nasa_title():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #get the news title
    news_title = str(soup.find('div',class_="content_title").text)
    
       # Close the browser after scraping
    browser.quit()

    # Return results
    return news_title

def scrape_nasa_teaser():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #get the corrsponding paragraph text
    news_p = str(soup.find('div',class_="article_teaser_body").text)
    
       # Close the browser after scraping
    browser.quit()

    # Return results
    return news_p


# In[4]:


def scrape_JPL():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    anchor = soup.find('a', class_="button fancybox")
    image_url = str(anchor.get('data-fancybox-href'))
    featured_image_url = ("https://www.jpl.nasa.gov/" + image_url)
    browser.quit()
    
    return featured_image_url


# In[5]:


def scrape_twitter():
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather = mars_weather.strip('/n')
    browser.quit()
    return mars_weather


# In[24]:


def scrape_table():
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table),skiprows=1)[0]
    df = df.rename(index=str, columns={0: "Description", 1: "Data"})
    html_table = df.to_html(header=True,index=False,index_names=False,justify="center")
    html_table = html_table.replace('\n', " ").encode('utf-8')
    html_table = str(html_table)
    browser.quit()
    return html_table


# In[27]:


def image_urls():
    link_names = ['Cerberus Hemisphere Enhanced','Schiaparelli Hemisphere Enhanced','Syrtis Major Hemisphere Enhanced','Valles Marineris Hemisphere Enhanced']
    url_list = []
    title_list = []
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"
    browser.visit(url)
    for name in link_names:
        browser.click_link_by_partial_text(name)
        time.sleep(1)
        # Scrape page into Soup for img url
        html = browser.html
        soup = bs(html, "html.parser")
        img = soup.find('img',class_="wide-image")
        src = str(img.get('src'))
        img_url = ("https://astrogeology.usgs.gov/" + src)
        url_list.append(img_url)
        
        title = soup.find('h2',class_="title").text
        title_list.append(str(title))
        
        browser.back()
    browser.quit()
    hemisphere_image_urls = [
    {"title": title_list[0], "img_url": url_list[0]},
    {"title": title_list[1], "img_url": url_list[1]},
    {"title": title_list[2], "img_url": url_list[2]},
    {"title": title_list[3], "img_url": url_list[3]},
    ]
    
    return hemisphere_image_urls

def scrape():
    scraped = {"title":scrape_nasa_title(),
               "teaser":scrape_nasa_teaser(),
               "table":scrape_table(),
               "featured_image_url":scrape_JPL(),
               "mars_weather":scrape_twitter(),
               "image_urls":image_urls()
               }
    
    return scraped
# In[ ]:




