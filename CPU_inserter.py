import mysql.connector
import configparser as cf
from pcpartpicker import API
import itertools
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from time import sleep

def connectToDB():
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

    return conn.cursor()


# api = API()
# cpu_data = api.retrieve("cpu")
# values = cpu_data.values()

# Set Brave-specific options
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

# Create the ChromeDriver instance for Brave
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)

# Open a website
driver.get('https://www.techpowerup.com/cpu-specs/')
#wait = driver.WebDriverWait(driver, 10)


search_bar = driver.find_element_by_id("quicksearch")
search_bar.send_keys("Core i7-13700TE")
sleep(5)

# Find all <tr> elements
td_elements = driver.find_elements_by_tag_name('tr')

# Print the text of each <tr> element
print('All <td> tags:')
for element in td_elements:
    print(element.text)
    
# Quit the browser
driver.quit()

# flattened_values = itertools.chain(*values)
# #relevant attributes: base_clock, boost_clock, brand, cores, integrated graphics, model, multithreading, price, tdp
# for element in flattened_values:
#     print(element)
   


    

    
