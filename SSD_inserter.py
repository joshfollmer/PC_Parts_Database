
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from time import sleep


#function to check if an entry has already been inserted into the table
def checkIfExists(cursor, table_name, column_name, value):
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    count = result[0]
    return count > 0


def parseSsdPage(url, cursor):
    table_name = "ssd"
    column_name = "model"
    value = "temp"
    driver.get(url)
    sleep(5)
    sections = driver.find_elements_by_css_selector("section.details")
    model = driver.find_element_by_class_name("drivename").text
    if(checkIfExists(cursor, table_name, column_name, value) == True):
        print(f"{model} already in table")
        return


    for section in sections:
        h1_element = section.find_element_by_css_selector("h1")
        
        if(h1_element.text == "Solid-State-Drive"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th")
                if(header.text == "Capacity:"):
                    overall_capacity = row.find_element_by_css_selector("td").text
        
        elif(h1_element.text == "NAND Flash"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th")
                if(header.text == "Type:"):
                    nand_type = row.find_element_by_css_selector("td").text
                elif(header.text == "Technology"):
                    nand_technology = row.find_element_by_css_selector("td").text
                elif(header.text == "Capacity:"):
                    nand_capacity = row.find_element_by_css_selector("td").text
        
        elif(h1_element.text == "Physical"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th")
                if(header.text == "Form Factor:"):
                    form_factor = row.find_element_by_css_selector("td").text
                elif(header.text == "Interface:"):
                    interface = row.find_element_by_css_selector("td").text
                elif(header.text == "Protocol:"):
                    protocol = row.find_element_by_css_selector("td").text

        elif(h1_element.text == "Controller"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th") 
                if(header.text == "Architecture:"):
                    controller = row.find_element_by_css_selector("td").text

        elif(h1_element.text == "DRAM Cache"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th")   
                if(header.text == "Capacity:"):
                    dram = row.find_element_by_css_selector("td").text

        elif(h1_element.text == "Performance"):
            rows = section.find_elements_by_css_selector("tr")

            for row in rows:
                header = row.find_element_by_css_selector("th")   
                if(header.text == "Sequential Read:"):
                    read_speed = row.find_element_by_css_selector("td").text
                elif(header.text == "Sequential Write:"):
                    write_speed = row.find_element_by_css_selector("td").text
                elif(header.text == "Random Read:"):
                    random_read = row.find_element_by_css_selector("td").text
                elif(header.text == "Random write:"):
                    random_write = row.find_element_by_css_selector("td").text
                elif(header.text == "Endurance:"):
                    endurance = row.find_element_by_css_selector("td").text

    


#target attributes: /capacity, /interface, /random_read, /random_write /read_speed(sequential read), /write_speed, 
# endurance, /dram, model, /protocol, /form_factor, /controller(architecture)
#/nand_type, /nand_capacity, /nand_technology,


options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

# Create the ChromeDriver instance for Brave
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)

# Open a website
driver.get('https://www.techpowerup.com/ssd-specs/')
# find the search bar
search_bar = driver.find_element_by_css_selector(".js-search-input.search-input")
#!new approach: type two letters into search bar (aa, ab, ac, etc) and then visit each entry and insert based on info from page
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


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

    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            #we need to reload the page and relocate the search bar each time because we will be loading new pages
            driver.get('https://www.techpowerup.com/ssd-specs/')
            search_bar = driver.find_element_by_css_selector(".js-search-input.search-input")
            search_bar.send_keys(f"{alphabet[i]}{alphabet[j]}")
            sleep(5)
            ssd_table = driver.find_elements_by_css_selector(".drive-title")
            link_attributes = []
            for item in ssd_table:
                a_elements = item.find_elements_by_tag_name('a')
                for result in a_elements:
                    if result.text.strip():
                        href = result.get_attribute("href")
                        text = result.text
                        link_attributes.append({"href": href, "text": text})


            for item in link_attributes:
                
                parseSsdPage(item["href"], cursor)
                        
                     
            
           

 
            
finally:
    driver.quit()