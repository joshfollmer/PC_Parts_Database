import mysql.connector
from mysql.connector import connect, Error
import configparser as cf
from pcpartpicker import API
import itertools
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

from time import sleep



#function to check if an entry has already been inserted into the table
def checkIfExists(cursor, table_name, column_name, value):
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    count = result[0]
    return count > 0

def insertIntoDB(cursor, api_cpu, db_cpu):
    delimiter = "Socket" if "Socket" in db_cpu else "BGA"
    before, _, after = db_cpu.partition(delimiter)
    db_cpu = delimiter + " " + after.strip() if after else db_cpu
    
    words = db_cpu.split()
    socket_type = ' '.join(words[:2])
    process = ' '.join(words[2:4])
    l3_cache = words[4]
    date_released = ' '.join(words[7:])
    
    words = str(api_cpu.base_clock)
    words = words.rpartition('cycles=')[-1][:-1]
    base_clock = int(words)

    base_clock = round(base_clock / 10**8) / 10
    
    if(api_cpu.boost_clock == None):
        boost_clock = "None"
    else:
        words = str(api_cpu.boost_clock)
        words = words.rpartition('cycles=')[-1][:-1]
        boost_clock = int(words)
        boost_clock = round(boost_clock / 10**8) / 10  
    
    try:
        query = "INSERT INTO cpu (brand, model, tdp, socket_type, base_clock, boost_clock, cores, integrated_graphics, process, l3_cache, date_released, multithreading) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (api_cpu.brand, api_cpu.model, api_cpu.tdp, socket_type, base_clock, boost_clock, api_cpu.cores, api_cpu.integrated_graphics, process, l3_cache, date_released,  api_cpu.multithreading)
        cursor.execute(query, values)
        conn.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
    print(f"{api_cpu.model} inserted")


#function that will take two strings and compare them. the first arg is what is being looked up, the second is what it is being compared to
def checkString(lookup_string, parsing_string):

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
    
    table_name = "cpu"
    column_name = "model"
    value = "temp"
    #relevant attributes: base_clock, boost_clock, brand, cores, integrated graphics, model, multithreading, price, tdp
    #loop through the API, put the model name into the searchbar, and find the result we are looking for 
    counter = 0
    for element in flattened_values:
        if(counter >= 215):
            print(element.model)
            print(f"attributes: {element.base_clock}, {element.boost_clock}, {element.cores}, {element.integrated_graphics}, {element.multithreading}, {element.tdp}")
            if(checkIfExists(cursor, table_name, column_name, element.model) == False):
                search_bar.send_keys(element.model)
                #sleep so the page loads all of the content
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

                            #we want to make sure the element we are looking at in the database actaully matches the one we are searching from the API. the following code makes sure of this
                            if(checkString(element.model.replace(' ', ''), result_name) == True):
                                print("found match")
                                db_cpu = item.find_elements_by_tag_name('tr')
                                db_cpu = str(db_cpu[1].text)
                                insertIntoDB(cursor, element, db_cpu)
                                break
                                
                            else:  #some results include the brand name in the core name, so we will try comparing again but with the brand name included
                                #the APi stores all ryzen cpus under the "AMD", but the database has it stored as "Ryzen". this takes care of thaat discrepancy before we compare them
                                if(element.brand == "AMD"):
                                    brand = "Ryzen"
                                else:
                                    brand = element.brand
                                if(checkString((brand + element.model).replace(' ', ''), result_name) == True):
                                    print("passed second try")
                                    db_cpu = item.find_elements_by_tag_name('tr')
                                    db_cpu = str(db_cpu[1].text)
                                    insertIntoDB(cursor, element, db_cpu)
                                    break
                                else:
                                    print(f"not found. arg 1: {(element.brand + element.model).replace(' ', '')}, arg 2: {result_name}")
    
                search_bar.clear()
                counter += 1
                print(f"count = {counter}")
                sleep(1)
            else:
                counter += 1
                print(f"already in database. count = {counter}")
        else:
            counter += 1
            print(f"count = {counter}")
    
finally:
    # Quit the browser
    driver.quit()

    
