import pymysql
import csv

mydb = pymysql.connect(host='127.0.0.1', port=3304, user='root', password='12345678', db='test_db')
cursor = mydb.cursor()

csv_data = csv.reader(open('components.csv'))
is_first = True
for row in csv_data:
    if is_first:
        is_first = False
        continue
    count = int(row[3]) if row[3].isdigit() else None
    discount = int(row[6]) if row[6].isdigit() else None
    color = row[2] if ".." not in row[2] else ""
    guarantee = int(row[7]) if row[7].isdigit() else '6'
    price = int(row[10]) if row[10].isdigit() else None
    component_type_id = int(row[12]) if row[12].isdigit() else None

    cursor.execute("INSERT INTO component(characteristics, color, count, country_of_origin, description, discount, guarantee, images, model, price, title, component_type_id)"+
        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[1], color, count, row[4], row[5], discount, guarantee, row[8], row[9], price, row[11], component_type_id))

mydb.commit()
cursor.close()
mydb.close()
print("Done")