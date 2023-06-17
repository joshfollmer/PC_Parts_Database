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

#function that will take two strings and compare them. the first arg is what is being looked up, the second is what it is being compared to
def checkString(lookup_string, parsing_string):
    if(len(lookup_string) != len(parsing_string)):
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
        if(counter >= 700):
            print(element.model)
            search_bar.send_keys(element.model)
            sleep(5)


            #selects only items in the search table
            processor_table = driver.find_elements_by_css_selector("table.processors")
            #loops through the search results
            for item in processor_table:
                a_elements = item.find_elements_by_tag_name('a')
                
                #loops through everything after the first element to avoid the header row
                for result in a_elements:
                    result_name = str(result.text)
                    result_name = result_name.replace(' ', '')
                    
                    
                    if(result.text.strip()):   #DONT REMOVE. not sure why, but it produces a lot of blank results, so this line makes sure the thing we are looking at is not blank
                        print(f"looking up {element.model} showing {result.text}")

                        #we want to make sure the element we are looking at in the database actaully matches the one we are searching from the API. the following code makes sure of this
                        if(checkString(element.model.replace(' ', ''), result_name) == True):
                            print("found match")
                            break
                            #!where we will insert into sql
                            #remember to ensure we are not inserting duplicates
                        else:  #some results include the brand name in the core name, so we will try comparing again but with the brand name included
                            #the APi stores all ryzen cpus under the "AMD", but the database has it stored as "Ryzen". this takes care of thaat discrepancy before we compare them
                            if(element.brand == "AMD"):
                                brand = "Ryzen"
                            else:
                                brand = element.brand
                            if(checkString((brand + element.model).replace(' ', ''), result_name) == True):
                                print("passed second try")
                            else:
                                print(f"fuck. arg 1: {(element.brand + element.model).replace(' ', '')}, arg 2: {result_name}")
   
            search_bar.clear()
                    

            counter += 1
            sleep(1)
        counter += 1
    
finally:
    # Quit the browser
    driver.quit()

    
