from Product import Product
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url='https://best.aliexpress.com/'
products = []


def driverController():
    global url
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    scroll_heigh = 150
    scroll_inc = 5
    for _ in range(scroll_inc):
        driver.execute_script(f"window.scrollBy(0, {scroll_heigh});")
        time.sleep(0.2)
        try:
            more_to_love_button = WebDriverWait(driver, 0.1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'more-to-love--action--2gSTocC'))
            )
            more_to_love_button.click()
            time.sleep(2)
        except Exception as e:
            pass
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'pop-close-btn'))
        )
        close_button.click()
    except Exception as e:
        print(f"Error: {e}")
    page = driver.page_source
    driver.quit()
    return page


def scraper(soup):
    global products
    allProducts = soup.find_all('div', class_='recommend-card--card-wrap--2jjBf6S')
    i = 0
    for product in allProducts:
        productTitle = product.find('div', style="font-size: 14px; color: rgb(25, 25, 25); height: 18px; display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-box-orient: vertical; -webkit-line-clamp: 1;")
        productRevRate = product.find('div', class_="rc-modules--stars--o9mzAea")
        productSolde = product.find('div', style="font-size: 12px; color: rgb(117, 117, 117);")
        try : 
            productShipping = product.find('span', class_="rc-modules--text--3kpyr_j", style="height: 16px; color: rgb(25, 25, 25);").text
        except:
            productShipping = ""
        try :
            productOldPrice = product.find('span', class_="rc-modules--price--1NNLjth", style="display: inline-block; text-decoration: line-through; color: rgb(117, 117, 117); font-size: 12px; margin: 0px 4px;")
        except:
            productOldPrice = ""
        productPrice = product.find('span', class_="rc-modules--price--1NNLjth")

        myproductTitle = productTitle.get('title') if productTitle else ""
        myproductRevRate = productRevRate.get('title') if productRevRate else ""
        myproductSolde = productSolde.text if productSolde else ""
        myproductShipping = productShipping
        myproductPrice = productPrice.text if productPrice else ""
        myproductOldPrice = productOldPrice.text if productOldPrice else ""
    
        product_object = Product(myproductTitle, myproductRevRate, myproductSolde, myproductShipping, myproductPrice, myproductOldPrice)
        product_object.clean()
        product_object.printProduct()
        products.append(product_object)

def toCsv():
    global products
    data = [{'Title': product.productTitle, 'rating': product.productRevRate, 'solde': product.productSolde, 'shipping': product.productShipping, 'price': product.productPrice, 'old price': product.productOldPrice} for product in products]
    df = pd.DataFrame(data)
    df.to_csv('products.csv', index=False)

def main():
    page = driverController()
    soup = BeautifulSoup(page, 'html.parser')
    scraper(soup)
    toCsv()

if __name__ == "__main__":
    main()
