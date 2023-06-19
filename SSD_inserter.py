from pcpartpicker import API
import itertools
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

api = API()
#relevant attributes: brand, cache_amount, capacity, form_factor, interface, model, storage_type
cpu_data = api.retrieve("internal-hard-drive")
values = cpu_data.values()
#put the pcpart object into a more readable format
flattened_values = itertools.chain(*values)

try:
    counter = 0
    for element in flattened_values:
        if(counter <= 10 and element.storage_type == "SSD"):
            search_bar.send_keys(element.model)
            sleep(5)

            ssd_table = driver.find_elements_by_css_selector("table.drives-desktop-table")

            for item in ssd_table:
                a_elements = item.find_elements_by_tag_name('a')

                for result in a_elements:
                    if(result.text.strip()):
                        link = result.get_attribute("href")
                        driver.get(link)
                        sleep(5)

        search_bar.clear()
        counter += 1
finally:
    driver.quit()