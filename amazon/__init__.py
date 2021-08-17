from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt

# terms = input("What would you like to search Amazon.ca for? ")


def clean_input(unclean):
    clean = unclean.replace(' ', '').split(",")
    return clean


def get_soup(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                     "Chrome/92.0.4515.131 ""Safari/537.36")

    driver = webdriver.Chrome(options=options)
    url = 'https://www.amazon.ca/'
    driver.get(url)
    driver.maximize_window()

    search_box = driver.find_element_by_id("twotabsearchtextbox")
    search_box.send_keys(search_term)
    search_box.submit()

    '''sort = driver.find_element_by_id('a-autoid-0-announce')
    sort.click()

    av_reviews = driver.find_element_by_id('s-result-sort-select_3')
    av_reviews.click()'''

    time.sleep(1)
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

        soup = get_soup(keyword)

        names = soup.find_all("span", {'class': 'a-size-base-plus a-color-base a-text-normal'})
        for name in names:
            temp_names.append(name.text)

        prices = soup.find_all("span", {'class': 'a-price-whole'})
        for price in prices:
            price_clean = price.text[:-1].replace(',', '')
            temp_prices.append(int(price_clean))

        for i in range(len(temp_prices)):
            temp_search.append(keyword)

        names_list.extend(temp_names[:len(temp_prices)])
        prices_list.extend(temp_prices)
        search_list.extend(temp_search)

    return names_list, prices_list, search_list


def create_dataframe(search):
    names, prices, search_terms = get_data(clean_input(search))

    dictionary = {'Name': names, 'Price ($)': prices, 'Search Term': search_terms}

    df = pd.DataFrame(dictionary)

    return df


def create_bp(dataframe):
    bp = dataframe.boxplot(by=['Search Term'], column=['Price ($)'], grid=False, showmeans=True)
    bp.set_title("")
    # bp.set_xlabel("")
    bp.set_ylabel("Price ($)")

    # plt.suptitle('')
    plt.savefig('Website/static/amazon/boxplot.png')


def save_to_excel(dataframe):
    writer = pd.ExcelWriter('Website/static/amazon/Amazon Web-Scraper.xlsx')
    dataframe.to_excel(writer, sheet_name='Data', index=False)

    bpsheet = writer.sheets['Data']
    bpsheet.insert_image('E2', 'Website/static/amazon/boxplot.png')

    writer.save()
    print('saved files')


if __name__ == '__main__':
    search = input('What would you like to search? ')
    df = create_dataframe(search)
    create_bp(df)
    save_to_excel(df)
