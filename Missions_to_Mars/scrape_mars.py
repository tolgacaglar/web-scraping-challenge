# Dependencies
import pandas as pd

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML


def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create db object

    # Scrape and write
    nasa_mars_news(browser, db)
    jpl_image_urls(browser, db)
    mars_facts(browser, db)
    mars_hemispheres(browser, db)

def nasa_mars_news(browser, db):
    # NASA Mars News
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)

    nasa_html = browser.html
    soup = BeautifulSoup(nasa_html, "html.parser")

    news = soup.find("div", {"class": "image_and_description_container"})   # Container that keeps the first news

    news_title = news.find("div", {"class": "content_title"}).text
    news_date = news.find("div", {"class": "list_date"}).text
    news_p = news.find("div", {"class": "article_teaser_body"}).text

    # Write to database

def jpl_image_urls(browser, db):
    # JPL Mars Space Images
    jpl_folder = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    browser.visit(jpl_folder + "index.html")

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")

    img_path = jpl_soup.find("div", {"class": "floating_text_area"}).find("a")["href"]
    full_img_url = jpl_folder + img_path

    # Write to the database

def mars_facts(browser, db):
    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    facts_html = browser.html
    facts_df = pd.read_html(facts_html)[0]

    # Write to the database

def mars_hemispheres(browser, db):
    # Mars Hemispheres
    hemispheres_base = "https://astrogeology.usgs.gov"
    browser.visit(hemispheres_base + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, "html.parser")

    ## Collect the links for full-sized images
    hemispheres_results = hemispheres_soup.find_all("div", {"class": "item"})
    ## Visit each link to collect the full-sized image url
    hemispheres_links = []
    for result in hemispheres_results:
        title = "Title" # Link was not working, so I couldn't check how to retrieve the title
        visit_url = hemispheres_base + result.find("a")["href"]
        
        browser.visit(visit_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        image_url = "#" # Link was not working, so I couldn't check how to retrieve the title
        hemispheres_links.append({"title": title, 
                                "img_url": image_url })
    # Write to database