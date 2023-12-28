import csv
from random import *

file_info = open("components.txt", encoding="utf-8")

all_info = file_info.read().split("Номер товара: ")

column_names = [
    "id",
    "characteristics",
    "color",
    "count",
    "country_of_origin",
    "description",
    "discount",
    "guarantee",
    "images",
    "model",
    "price",
    "title",
    "component_type_id"
]

all_data = [
    column_names
]

for i in range(1, len(all_info)):
    print(all_info[i])
    line = all_info[i].split("\n")
    title = ""
    price = ""
    color = ""
    country_of_origin = ""
    description = ""
    count = str(randint(1, 100))
    discount = [0, 5, 10, 15]
    index = randint(0, 3)
    guarantee = ""
    model = ""
    characteristics = ""
    is_exist = False
    ex = False
    images = ""
    component_type_id = ""
    for j in range(len(line)):
        if "Название:" in line[j]:
            title = line[j].split(":")[1].strip()
        if "Цена:" in line[j]:
            price = line[j].split(":")[1].strip()
            price = price.replace("₽", "").replace(" ", "")
        if "Цвета, использованные в оформлении -" in line[j]:
            color = line[j].split("-")[1].strip()
        if "Производитель -" in line[j]:
            country_of_origin = line[j].split("-")[1].strip()
        if "Описание" in line[j]:
            description = line[j].split("-")[1].strip()
        if "Гарантия -" in line[j]:
            guarantee = line[j].split("-")[1].strip()
            guarantee = guarantee.replace("мес.", "").replace(" ", "")
        if "Модель -" in line[j]:
            model = line[j].split("-")[1].strip()
        if line[j] == "Характеристики:":
            is_exist = True
            continue
        if is_exist:
            characteristics += line[j] + "<br>"
        if ".png" in line[j]:
            images += line[j] + "<br>"
        if "Тип комплектующего:" in line[j]:
            component_type_id = line[j].split(":")[1].strip()
    all_data.append(["",characteristics,color,count,country_of_origin,description,str(discount[index]),guarantee,images,model,price,title,component_type_id])

with open('components.csv', 'w', newline='', encoding='cp1251') as file:
    writer = csv.writer(file)
    writer.writerows(all_data)