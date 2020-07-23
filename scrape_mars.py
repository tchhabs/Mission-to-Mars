import os
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup_nasa = bs(html, 'html.parser')
    article = soup_nasa.select_one('ul.item_list li.slide')
    
    newstitle = article.find('div', class_='content_title').get_text()

    newsbody = article.find('div', class_='article_teaser_body').get_text()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup_img = bs(html, 'html.parser')
    sub_url = soup_img.find_all(class_='carousel_item')[0].get('style').strip('background-image: url ();').replace("'","")

    base_url="https://www.jpl.nasa.gov"
    featured_image_url= base_url + sub_url

    url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup_twitter = bs(html, 'html.parser')
    twitter_list= [tag.text for tag in soup_twitter.find_all('div',{'dir':"auto"})]
    new_twitter_list= [text for text in twitter_list if 'InSight sol' in text]
    new_twitter_list[0]

    url= "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    mars_facts = pd.read_html(url, header=None)

    mars_df = mars_facts[0]

    mars_table_html = mars_df.to_html(header=False, index=False)
    mars_df.to_html('mars_table.html', header=False, index=False)

    url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup_hemisphere = bs(html, 'html.parser')

    hemispheres = []

    links= browser.find_by_css("a.product-item h3")

    for index in range(len(links)):
        hemi= {}
        browser.find_by_css("a.product-item h3")[index].click()
        image= browser.find_link_by_text("Sample").first
        hemi["img_url"]= image["href"]
        hemi["title"]= browser.find_by_css("h2.title").text
        hemispheres.append(hemi)
        browser.back()
        time.sleep(5)

     mars_data = {
        "news_title": newstitle,
        "news_p": newsbody,
        "featured_image_url": featured_image_url,
        "mars_weather": new_twitter_list[0],
        "mars_table_html": mars_table_html,
        "hemisphere_data": hemispheres
    }

    browser.quit()

    return mars_data