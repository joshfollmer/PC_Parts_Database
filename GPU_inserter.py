import mysql.connector
import configparser as cf
from selenium import webdriver
from time import sleep
from random import randint
from selenium.webdriver.common.by import By
from datetime import datetime


#function to check if an entry has already been inserted into the table
def checkIfExists(cursor, table_name, column_name, value):
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    count = result[0]
    return count > 0

#target specs: brand, model, clock_speed, vram, bus_width, bandwidth, pcie, tdp, length, width, height,
#shading_units, memory_type, th_pixel_rate, th_texture_rate, th_FP16, th_FP32, th_FP64, architecture, 
#process size, release_date, transistors
def parseGpuPage(url, cursor):
    driver.get(url)
    sleep(10)

    brand = "unknown"
    model = "unknown"
    clock_speed = "unknown"
    vram = "unknown"
    bus_width = "unknown"
    bandwidth = "unknown"
    pcie = "unknown"
    tdp = "unknown"
    length = "unknown"
    width = "unknown"
    height = "unknown"
    shading_units = "unknown"
    memory_type = "unknown"
    th_pixel_rate = "unknown"
    th_texture_rate = "unknown"
    th_FP16 = "unknown"
    th_FP32 = "unknown"
    th_FP64 = "unknown"
    architecture = "unknown"
    process_size = "unknown"
    release_date = "unknown"
    transistors = "unknown"

    sections = driver.find_elements(By.CSS_SELECTOR, "section.details")
    name = driver.find_element(By.CLASS_NAME, "gpudb-name").text
    name = name.split(" ", 1)
    brand = name[0]
    model = name[1]
    
    for section in sections:
        h2_element = section.find_element(By.CSS_SELECTOR, "h2")

        if(h2_element.text == "Graphics Processor"):
            rows = section.find_elements(By.CLASS_NAME, "clearfix")
            for row in rows:
                header = row.find_element(By.CSS_SELECTOR, "dt")
                if(header.text == "Architecture"):
                    architecture = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "Process Size"):
                    process_size = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "Transistors"):
                    transistors = row.find_element(By.CSS_SELECTOR, "dd").text

        elif(h2_element.text == "Graphics Card"):
            rows = section.find_elements(By.CLASS_NAME, "clearfix")
            for row in rows:
                header = row.find_element(By.CSS_SELECTOR, "dt")
                if(header.text == "Release Date"):
                    release_date = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "Bus Interface"):
                    pcie = row.find_element(By.CSS_SELECTOR, "dd").text

        elif(h2_element.text == "Render Config"):
            rows = section.find_elements(By.CLASS_NAME, "clearfix")
            for row in rows:
                header = row.find_element(By.CSS_SELECTOR, "dt")
                if(header.text == "Shading Units"):
                    shading_units = row.find_element(By.CSS_SELECTOR, "dd").text  

        elif(h2_element.text == "Theoretical Performance"):
            rows = section.find_elements(By.CLASS_NAME, "clearfix")
            for row in rows:
                header = row.find_element(By.CSS_SELECTOR, "dt")
                if(header.text == "Pixel Rate"):
                    th_pixel_rate = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "Texture Rate"):
                    th_texture_rate = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "FP16(half)"):
                    th_FP16 = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "FP32(float)"):
                    th_FP32 = row.find_element(By.CSS_SELECTOR, "dd").text
                elif(header.text == "Fp64(double)"):
                    th_FP64 = row.find_element(By.CSS_SELECTOR, "dd").text

        elif(h2_element.text == "Board Design"):
            rows = section.find_elements(By.CLASS_NAME, "clearfix")
            for row in rows:
                header = row.find_element(By.CSS_SELECTOR, "dt")
                if(header.text == "Length"):
                    length = row.find_element(By.CSS_SELECTOR, "dd").text
    
    list = [brand, model, architecture, process_size, transistors, release_date, pcie, shading_units,
            th_pixel_rate, th_texture_rate, th_FP16, th_FP32, th_FP64]

    print(length)



driver = webdriver.Chrome()
# Open a website
driver.get('https://www.techpowerup.com/gpu-specs/')
sleep(1)
# find the search bar
search_bar = driver.find_element(By.NAME, "q")
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
                if(counter > 3):
                    #we need to reload the page and relocate the search bar each time because we will be loading new pages
                    driver.get('https://www.techpowerup.com/gpu-specs/')
                    search_bar = driver.find_element(By.NAME, "q")
                    search_bar.send_keys(f"{alphabet[i]}{alphabet[j]}")
                    sleep(5)
                    amd_cards = driver.find_elements(By.CSS_SELECTOR, ".vendor-AMD")
                    nvi_cards = driver.find_elements(By.CSS_SELECTOR, ".vendor-NVIDIA")
                    intel_cards = driver.find_elements(By.CSS_SELECTOR, ".vendor-INTEL")
                    cards = amd_cards + nvi_cards + intel_cards
                    link_attributes = []
                    for item in cards:
                        a_elements = item.find_elements(By.TAG_NAME, 'a')
                        for result in a_elements:
                            if result.text.strip():
                                href = result.get_attribute("href")
                                text = result.text
                                link_attributes.append({"href": href, "text": text})
                                

                    for item in link_attributes:
                        parseGpuPage(item["href"], cursor)
                counter += 1
                print(f"counter is {counter}")

    #except:
        # now = datetime.now()
        # print(f"Error at {now.strftime('%H:%M:%S')}. Waiting for 20 minutes")
        # sleep(1200) 
               
    finally:
        driver.quit()    