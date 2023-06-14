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




# # Set Brave-specific options
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

# # Create the ChromeDriver instance for Brave
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)

# Open a website
driver.get('https://www.techpowerup.com/cpu-specs/')
# find the search bar
search_bar = driver.find_element_by_id("quicksearch")


#open the pcpartpicker API
api = API()
cpu_data = api.retrieve("cpu")
values = cpu_data.values()
#put the pcpart object into a more readable format
flattened_values = itertools.chain(*values)

#relevant attributes: base_clock, boost_clock, brand, cores, integrated graphics, model, multithreading, price, tdp
#for 10 times, loop through the API, put the model name into the searchbar, and find the result we are looking for 
counter = 0
for element in flattened_values:
    if(counter > 10):
        break

    print(element.model)
    search_bar.send_keys(element.model)
    sleep(5)
    table = driver.find_element_by_css_selector("table.processors")
    
    tr_elements = driver.find_elements_by_tag_name('tr')
    for result in tr_elements:
        print(result.text)
        # result_name = str(result)
        # result_name = result_name.split("/", 1)
        # result_name = result_name[0].strip()
        # if(result_name == element.model):
        #     print("hooray!")
        # else:
        #     print(f"booo! result name: {result_name}, element model: {element.model}")
            

    counter += 1
    sleep(1)
   

# Quit the browser
driver.quit()

    
