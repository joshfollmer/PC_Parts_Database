import mysql.connector
from mysql.connector import connect, Error
import configparser as cf
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint


#function to check if an entry has already been inserted into the table
def checkIfExists(cursor, table_name, column_name, value):
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    count = result[0]
    return count > 0


def parseGpuPage(url, cursor):
   url = url


options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

# Create the ChromeDriver instance for Brave
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)

# Open a website
driver.get('https://www.techpowerup.com/gpu-specs/')
# find the search bar
search_bar = driver.find_element_by_css_selector(".js-search-input.search-input")
#the approach: type two letters into search bar (aa, ab, ac, etc) and then visit each entry and insert based on info from page
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']

counter = 0
while(True):
    try:
        config = cf.ConfigParser()
        config.read('config.ini')
        db_host = config.get('Database', 'HOST') 
        db_user = config.get('Database', 'USER')
        db_password = config.get('Database', 'PASSWORD')
        db_name = config.get('Database', 'DATABASE')
        conn = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_password,
            database = db_name
        )
        cursor = conn.cursor()
        table_name = "ssd"
        column_name = "model"
        value = "temp"
        for i in range(len(alphabet)):
            for j in range(len(alphabet)):
                if(counter > 0):
                    #we need to reload the page and relocate the search bar each time because we will be loading new pages
                    driver.get('https://www.techpowerup.com/ssd-specs/')
                    search_bar = driver.find_element_by_css_selector(".js-search-input.search-input")
                    search_bar.send_keys(f"{alphabet[i]}{alphabet[j]}")
                    sleep(5)
                    amd_cards = driver.find_elements_by_css_selector(".vender-AMD")
                    nvi_cards = driver.find_elements_by_css_selector(".vender-NVIDIA")
                    intel_cards = driver.find_elements_by_css_selector(".vender-INTEL")
                    cards = amd_cards + nvi_cards + intel_cards
                    link_attributes = []
                    for item in cards:
                        a_elements = item.find_elements_by_tag_name('a')
                        for result in a_elements:
                            if result.text.strip():
                                # href = result.get_attribute("href")
                                # text = result.text
                                # link_attributes.append({"href": href, "text": text})
                                print(item.text)

                    # for item in link_attributes:
                    #     parseGpuPage(item["href"], cursor)
                counter += 1
                print(f"counter is {counter}")
    except:
        sleep(300)          
        
    finally:
        driver.quit()