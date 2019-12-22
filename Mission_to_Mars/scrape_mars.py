# ### Scraping NASA Mars News

# Import necessary libraries and dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#--------------------------------------------------------------------------

def scrape():
    browser = init_browser()

# Visit url to scrape for NASA News
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)


# Scrape the first article title and paragraph text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find_all("div", class_='list_text')[0]
    mars_news_title = article.find("div", class_="content_title").text
    mars_news_para = article.find("div", class_ ="article_teaser_body").text

    print(mars_news_title)
    print(mars_news_para)

#--------------------------------------------------------------------------

# ### JPL Mars Space Images - Featured Image

# Connect to the site and Scrape JPL Mars Space images for the featured image
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)

# Scrape for the jpl featured image

# Need the full image, must navigate to it by the button link
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

# Need to naviagte to more info button to get complete image url
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

# Need to parse new site with soup
    feature_image_html = browser.html
    feature_image_soup = BeautifulSoup(feature_image_html, 'html.parser')

# Scrape the image url
    jpl_feature_image_url = feature_image_soup.find('figure', class_='lede').a['href']
    jpl_feature_image_url = f'https://www.jpl.nasa.gov{jpl_feature_image_url}'
    print(jpl_feature_image_url)

#--------------------------------------------------------------------------

# ### Mars Weather twitter


# scrape for the latest mars weather tweet and assign to mars_weather
    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)
    mars_twitter_html = browser.html

# Parse HTML with Beautiful Soup
    mars_twitter_soup = BeautifulSoup(mars_twitter_html, 'html.parser')

# Get the latest tweet from mars twitter by doing a find all for tweets and then looping through them for weather
    mars_tweet = mars_twitter_soup.find_all('div', class_="js-tweet-text-container")

# Loop through latest tweets and find the tweet that has the weather
    for tweet in mars_tweet: 
        weather = tweet.find('p').text
        if 'sol' and 'low' and 'high' in weather:
            mars_weather = weather
            print(mars_weather)
# The break stops the loop once it finds the intended tweet, if not it moves to the next tweet
            break
        else: 
            pass

#--------------------------------------------------------------------------

# ## Mars Facts
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. 
# * Use Pandas to convert the data to a HTML table string.


# Use splinter to visit to the mars facts page to scrape info from the page table
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    mars_facts_html = browser.html


# Use pandas to read the html on the visited page
    mars_facts = pd.read_html(mars_facts_html)
# The first table picked up is the correct table for the output desired
    mars_facts_table = mars_facts[0]
    mars_facts_table

# Rename columns to match the intended output once rendered using flask
    mars_facts_table.columns = ['Description','Value']

# Reset Index to be description
    mars_facts_table.set_index('Description', inplace=True)
    mars_facts_table



# Convert table to html string
    mars_facts_table = mars_facts_table.to_html(classes="table table-striped")

#--------------------------------------------------------------------------

# ## Mars Hemispheres
# 
# 
# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.



# Use splinter to visit the USGS page for mats hemisphere images
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    mars_hemispheres_html = browser.html



# Use beautiful soup to parse the html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, "html.parser")



# Create a dictionary to assign the image key and value and loop through all the images with soup
    mars_hemisphere_dict = []

# Use soup to find all the tags that contain the image links to the full images
    result = mars_hemispheres_soup.find("div", class_ = "result-list" )
    mars_hemispheres = result.find_all("div", class_="item")

# Loop through each hempishere for the title and visit the image link to find the full image url
    for hemisphere in mars_hemispheres:
        hemisphere_title = hemisphere.find("h3").text
        next_image_link = hemisphere.find("a")["href"]
    # Use the href to create a url to visit the full image site
        hemisphere_image_page = "https://astrogeology.usgs.gov/" + next_image_link    
        browser.visit(hemisphere_image_page)
    # Parse the html with soup and find the final image url
        hemisphere_html = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html, "html.parser")
        downloads_class = hemisphere_soup.find("div", class_="downloads")
        hemisphere_image_url = downloads_class.find("a")["href"]
    #A Append the image url to the dict created 
        mars_hemisphere_dict.append({"title": hemisphere_title, "image_url": hemisphere_image_url})

# Print image title and url
    print(mars_hemisphere_dict)

#--------------------------------------------------------------------------

 # Store data in a dictionary
    mars_dict = {
        "news_title": mars_news_title,
        "news_paragraph": mars_news_para,
        "mars_image_url": jpl_feature_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_table,
        "hemisphere_images_urls": mars_hemisphere_dict
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict

if __name__ == '__main__':
    scrape()



