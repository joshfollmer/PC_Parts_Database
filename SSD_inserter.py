
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from time import sleep



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
            search_bar.send_keys(f"{alphabet[i]}{alphabet[j]}")
            sleep(5)


            
finally:
    driver.quit()