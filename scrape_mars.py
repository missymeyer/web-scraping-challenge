#!/usr/bin/env python
# coding: utf-8

# ## Mission To Mars

# In[ ]:


# Declare Dependencies 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[ ]:


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)


# In[ ]:


# Visit url for NASA Mars News
browser.visit(url)
html = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html, "html.parser")

# Extract article title and paragraph text
article = soup.find("div", class_='list_text')
news_title = article.find("div", class_="content_title").text
news_p = article.find("div", class_ ="article_teaser_body").text

print(news_title)
print(news_p)


# ## JPL Mars Space Images

# In[ ]:


jpl_nasa_url = 'https://www.jpl.nasa.gov'
images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

browser.visit(images_url)

html = browser.html

images_soup = BeautifulSoup(html, 'html.parser')


# In[ ]:


# Retrieve featured image link
relative_image_path = images_soup.find_all('img')[3]["src"]
featured_image_url = relative_image_path
print(featured_image_url)


# ## Mars Facts

# In[ ]:


facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(facts_url)
tables


# In[ ]:


mars_facts_df = tables[2]
mars_facts_df.columns = ["Description", "Value"]
mars_facts_df


# In[ ]:


mars_html_table = mars_facts_df.to_html()
mars_html_table


# In[ ]:


mars_html_table.replace('\n', '')


# In[ ]:


print(mars_html_table)


# ## Mars Hemispheres

# In[ ]:


usgs_url = 'https://astrogeology.usgs.gov'
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(hemispheres_url)

hemispheres_html = browser.html

hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')


# In[ ]:


# Mars hemispheres products data
all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

hemisphere_image_urls = []

# Iterate through each hemisphere data
for i in mars_hemispheres:
    # Collect Title
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text
    
    # Collect image link by browsing to hemisphere page
    hemisphere_link = hemisphere.a["href"]    
    browser.visit(usgs_url + hemisphere_link)
    
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    
    image_link = image_soup.find('div', class_='downloads')
    image_url = image_link.find('li').a['href']

    # Create Dictionary to store title and url info
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url
    
    hemisphere_image_urls.append(image_dict)

print(hemisphere_image_urls)


# In[ ]:


mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }


# In[ ]:


mars_dict

