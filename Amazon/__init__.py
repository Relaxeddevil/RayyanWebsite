from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt
import undetected_chromedriver as uc
import os


# terms = input("What would you like to search Amazon.ca for? ")


def clean_input(unclean):
    tmp = unclean.split(",")
    clean = []
    for i in tmp:
        clean.append(i.strip())

    return clean


def get_soup(search_term):
    # comment out "heroku" lines and uncomment "Personal" line when running locally

    options = webdriver.ChromeOptions()
    # options = Options()

    # options.headless = True
    # options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')  # heroku
    # executable_path = os.environ.get('CHROMEDRIVER_PATH')  # heroku

    options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    # driver = webdriver.Chrome(executable_path=executable_path, options=options)  # heroku
    driver = webdriver.Chrome(options=options)  # Personal
    url = 'https://www.amazon.ca/'
    driver.get(url)
    # driver.maximize_window()
    # time.sleep(15)

    # search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    wait = WebDriverWait(driver, 20)
    search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))

    search_box.send_keys(search_term)
    search_box.submit()
    time.sleep(5)

    # driver.save_screenshot('local_ss.png')

    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, 'lxml')

    return soup


def get_data(keywords):
    names_list = []
    prices_list = []
    search_list = []

    for keyword in keywords:
        temp_names = []
        temp_prices = []
        temp_search = []

        print('getting data for ' + keyword)
        soup = get_soup(keyword)

        names = soup.find_all("span", {'class': 'a-size-base-plus a-color-base a-text-normal'})
        for name in names:
            temp_names.append(name.text)

        prices = soup.find_all("span", {'class': 'a-price-whole'})
        for price in prices:
            price_clean = price.text[:-1].replace(',', '')
            temp_prices.append(int(price_clean))

        length = min(len(temp_names), len(temp_prices))

        for i in range(length):
            temp_search.append(keyword)

        names_list.extend(temp_names[:length])
        prices_list.extend(temp_prices[:length])
        search_list.extend(temp_search)
        print(len(names_list), len(prices_list), len(search_list))

    return names_list, prices_list, search_list


def create_dataframe(search):
    names, prices, search_terms = get_data(clean_input(search))

    dictionary = {'Name': names, 'Price ($)': prices, 'Search Term': search_terms}

    df = pd.DataFrame(dictionary)

    return df


def create_bp(dataframe, location='Website/static/amazon/boxplot.jpg'):
    bp = dataframe.boxplot(by=['Search Term'], column=['Price ($)'], grid=False, showmeans=True)
    bp.set_title("")
    # bp.set_xlabel("")
    bp.set_ylabel("Price ($)")

    # plt.suptitle('')
    plt.savefig(location)


def save_to_excel(dataframe, location='Website/static/amazon/Amazon Web-Scraper.xlsx'):
    writer = pd.ExcelWriter(location)
    dataframe.to_excel(writer, sheet_name='Data', index=False)
    writer.save()
    print('saved files')


if __name__ == '__main__':
    search = input('What would you like to search? ')
    df = create_dataframe(search)
    create_bp(df, 'boxplot.jpg')
    save_to_excel(df, 'Amazon Web-Scraper.xlsx')
