import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from app.routers.houses.crud import HousesCRUD
from app.routers.houses.models import HousingTypes

# one time for searching html

ua = UserAgent()

url = "https://www.list.am/category/62"

def headers():
    return  {
            "Accept":"*/*",
            "User-Agent":ua.random
            }           

req = requests.get(url, headers=headers())

src = req.text

soup = BeautifulSoup(src, "lxml")

def get_house_info(url, headers, db):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    short_house_info = soup.find(class_="attr g").find_all(class_=("c")) if soup.find(class_="attr g") != None else None
    if short_house_info == None:
        print(url)
        return None
    adress = soup.find(class_="loc").text if soup.find(class_="loc") != None else None
    price = soup.find(class_="price x").text if soup.find(class_="price x") != None else None
    condition = short_house_info[1].find(class_="i").text
    building_type = short_house_info[2].find(class_="i").text 
    area = short_house_info[3].find(class_="i").text 
    rooms_count = short_house_info[5].find(class_="i").text 

    data = {
        "housing_type": HousingTypes.house.value,
        "url": url,
        "adress": adress,
        "price": price,
        "condition": condition,
        "building_type": building_type,
        "area": area,
        "rooms_count": rooms_count,
    }

    HousesCRUD.add_house(data, db)

def get_page_info(db):
    all_houses = soup.find_all(class_="dl")[1].find(class_="gl")
    for element in all_houses:
        house_href = "https://www.list.am" + element.get("href")
        get_house_info(house_href, headers(), db)

        