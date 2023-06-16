import mysql.connector
import configparser as cf
from pcpartpicker import API
import itertools
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def checkString(lookup_string, parsing_string):
    if(len(parsing_string) != len(lookup_string)):
        return False

    for i in range(len(lookup_string)):
        if parsing_string[i] != lookup_string[i]:
            return False
    return True

# Set Brave-specific options
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

# Create the ChromeDriver instance for Brave
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
try:
    #relevant attributes: base_clock, boost_clock, brand, cores, integrated graphics, model, multithreading, price, tdp
    #loop through the API, put the model name into the searchbar, and find the result we are looking for 
    counter = 0
    for element in flattened_values:
        if(counter >= 6):
            

            print(element.model)
            search_bar.send_keys(element.model)
            wait = WebDriverWait(driver, 10)
            search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.processors tr")))
            
            #selects only items in the search table
            #processor_table = driver.find_elements_by_css_selector("table.processors")
            #loops through the search results
            for item in search_results:
                tr_elements = item.find_elements_by_tag_name('tr')
                #loops through everything after the first element to avoid the header row
                for result in tr_elements[1:]:
                    result_name = str(result.text)
                    result_name = result_name.split(" ", 1)
                    result_name = result_name[0].strip()
                    if(result.text.strip()):
                        print(f"looking up {element.model} showing {result.text}")

                        if(checkString(element.model.strip(), result_name) == True):
                            print("found match")
                        else:
                            print("fuck")
                    # result_name = str(result.text)
                    # result_name = result_name.split("/", 1)
                    # result_name = result_name[0].strip()
                    # if(result_name == element.model):
                    #     print("hooray!")
                    # else:
                    #     print(f"booo! result name: {result_name}, element model: {element.model}")
            search_bar.clear()
                    

            counter += 1
            sleep(1)
        counter += 1
    
except:
    # Quit the browser
    driver.quit()

    
