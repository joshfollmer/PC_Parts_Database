
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from time import sleep

#target attributes: capacities, interface, random_iops, read_speed(sequential read), write_speed, endurance, dram, model, protocol, form_factor, controller(name)
#nand_type, nand_capacity, nand_technology,
def parseSsdPage(url, text):
    driver.get(url)
    sleep(3)
    print(text)





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
                print(item["text"])
                #parseSsdPage(item["href"], item["text"])
                        
                     
            
           

 
            
finally:
    driver.quit()