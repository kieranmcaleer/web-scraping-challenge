#all of the imports

from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    mars_final_dict={
        "news_title": scrape_news()[0],
        "news_description": scrape_news()[1],
        "image_url":image_finder(),
        "fact_table":table_finder(),
        "hemisphere_dict":hemisphere_finder()

    }

    return mars_final_dict


def scrape_news():
    url = "https://mars.nasa.gov/news/"
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    title = soup.find('div', class_='features').\
        find('div', class_='slide')\
            .find('div', class_='content_title').a.text
    description= soup.find('div', class_='features').find('div', class_='rollover_description_inner').text
    return title, description

def image_finder():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    # open the url
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = soup.find('img', class_='headerimage fade-in')['src']
    # found how to take off the last part from https://stackoverflow.com/questions/54961679/python-removing-the-last-part-of-an-url
    new_url = url[:url.rfind('/')]
    image_url= new_url + '/' + image_url

    return image_url

def table_finder():
    pandas_url = "https://space-facts.com/mars/"
    # make a pandas table by pulling the table off the page
    tables = pd.read_html(pandas_url)
    mars_df = tables[0]
    mars_df = mars_df.rename(columns={0: "Categories", 1: "Data"})
    mars_html = mars_df.to_html()
    return mars_html

def hemisphere_finder():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    base_url="https://astrogeology.usgs.gov"
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # find all of the divs with a class of description
    div = soup.find_all('div', attrs={'class' : 'description'})
    # empty url list
    url_list=[]
    # go through the div tags, grab the end of the html that we need and add it onto our base url
    for i in div:
        url_list.append(base_url +i.a['href'])

    image_urls=[]
    title_list=[]
    # go through each of those sites and grab the image url 
    for i in url_list:
        browser.visit(i)
        html = browser.html
        soup = bs(html, 'html.parser')
        image = soup.find('div', attrs={'class' : 'container'})\
        .find('div', attrs={'class' : 'wide-image-wrapper'}).ul.li.a['href']
        image_urls.append(image)
        title = soup.find('div', class_='content').h2.text
        #     found how to take last word off string https://stackoverflow.com/questions/6266727/python-cut-off-the-last-word-of-a-sentence
        title = title.rsplit(' ',1)[0]
        title_list.append(title)

    title_imag = list(zip(title_list, image_urls))

    dict_list=[]
    for i in title_imag:
        new_dict={"title":i[0], "image_url":i[1]}
        dict_list.append(new_dict)


    return dict_list



if __name__ == "__main__":
    print(scrape())
