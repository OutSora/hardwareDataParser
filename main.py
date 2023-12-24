import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request

# headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

current_dir = os.getcwd()
folder_name = "chromedriver"
folder_path = os.path.join(current_dir, folder_name) + "\\chromedriver.exe"

service = Service(executable_path=folder_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
component_number = 0
item_number = 1
driver.get('https://www.regard.ru/catalog/1013/videokarty?search=видеокарта')
components_file = open("components.txt", "w", encoding="utf-8")
component_data = ""

hardwares = {
    5: 'Видеокарта',
    1: 'Материнская плата',
    2: 'Процессор',
    3: 'Охлаждение',
    4: 'Память',
    6: 'Корпус',
    7: 'Блок питания'
}

for key in hardwares.keys():
    if hardwares[key] != "Видеокарта":
        driver.implicitly_wait(5)
        search = driver.find_element(By.XPATH, "//div[1]/div/div[2]/div/div/div/input[2][@id='searchInput']")
        search.send_keys(hardwares[key])
        driver.implicitly_wait(20)
        element = WebDriverWait(driver, 5).until(
            # /div[1{номер элемента списка}]/div/a/div/div/div[1]/div[1]/img[@class='CardImageSlider_image__W65ZP']
            # Icons_search_Eydlv Search_searchIcon__ipNH0 Search_activeSearchIcon__HxnXX - активная
            # Icons_search__Eydlv Search_searchIcon__ipNH0 - не активная
            EC.presence_of_element_located((By.XPATH,
                                            f"//div[1]/div/div[2]/div/*[name()='svg' and @class='Icons_search__Eydlv Search_searchIcon__ipNH0 Search_activeSearchIcon__HxnXX']"))
        )
        element.click()
        driver.implicitly_wait(20)
        driver.execute_script("window.scrollBy(0,140)", "")
        driver.execute_script("window.scrollBy(0,140)", "")
        driver.implicitly_wait(20)
    item_number = 1
    component_number = 0
    while item_number != 6:
        driver.implicitly_wait(20)
        while True:
            try:
                element = WebDriverWait(driver, 5).until(
                    # /div[1{номер элемента списка}]/div/a/div/div/div[1]/div[1]/img[@class='CardImageSlider_image__W65ZP']
                    EC.presence_of_element_located((By.XPATH,
                                                    f"//div[{item_number}]/div/a/div/div/div[1]/div[1]/img[@class='CardImageSlider_image__W65ZP']"))
                )
                element.click()
                break
            except:
                driver.execute_script("window.scrollBy(0,110)", "")
                print("Элемент не найден")
        driver.implicitly_wait(15)
        title = driver.find_element(By.XPATH,
                                    "//div/div[1]/main/div/div[1]/div[1]/span/h1[@class='Product_title__42hYI']").text
        driver.implicitly_wait(5)
        price = driver.find_element(By.XPATH,
                                    "//div[2]/div[1]/div/div/span/span[@class='Price_price__m2aSe notranslate']").text
        driver.implicitly_wait(5)
        characteristics = driver.find_element(By.XPATH,
                                              "//main/div/div[2]/div[1]/div[2]/div/div/div[1][@class='Grid_col__4bXWJ Grid_col-12__JMZP1']").text
        driver.implicitly_wait(15)
        images = driver.find_elements(By.TAG_NAME, "img")

        component_number += 1
        component_images = []
        component_data += f"\nНомер товара: {component_number}\n"

        for image in images:
            number = image.get_attribute('src').split("/")
            if "https://www.regard.ru/api/site/cacheimg/goods" in image.get_attribute('src') and int(number[-1]) == 62:
                component_images.append(image.get_attribute('src'))
            print(image.get_attribute('src'))

        print("#" * 100)
        print(component_images)

        filename = hardwares[key]
        count = 0
        filenames_list = []
        for i in range(len(component_images)):
            urllib.request.urlretrieve(component_images[i], f"components_image/{filename}_{component_number}-{i}.png")
            filenames_list.append(f"{filename}_{component_number}-{i}.png")
            count += 1

        component_data += f"Тип комплектующего: {key}\n"
        component_data += f"Название: {title}\n"
        component_data += f"Цена: {price}\n"
        component_data += "Изображения:\n"
        for filename in filenames_list:
            component_data += f"{filename}\n"

        print(f"Название: {title}")
        print(f"Цена: {price}")
        data = characteristics.split("\n")
        count = 0
        print(data)
        header = data[0]
        component_data += "Характеристики:\n"
        component_data += f"---{header}---\n"
        body_data = ""
        characteristic_list = []
        index_list = []

        for i in range(len(data)):
            if count == 3:
                index_list.append(i - 1)
            if ".." not in data[i]:
                count += 1
            else:
                count = 0

        print(index_list)
        count = 0
        for i in range(1, len(data)):
            for j in range(len(index_list)):
                if index_list[j] == i:
                    component_data += f"---{data[i]}---\n"
                    count = 0
                    break
            if count == 2:
                body_data += f" - {data[i].strip()}"
                characteristic_list.append(body_data)
                component_data += f"{body_data}\n"
                body_data = ""
                count = 0
                continue
            if ".." not in data[i]:
                body_data = f"{data[i].strip()}"
            count += 1

        driver.implicitly_wait(10)
        driver.execute_script("window.history.go(-1)")
        driver.implicitly_wait(10)
        driver.execute_script("window.scrollBy(0,110)", "")
        item_number += 1

components_file.write(component_data)
components_file.close()
print(characteristic_list)