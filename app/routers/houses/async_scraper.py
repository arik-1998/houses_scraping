import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from app.routers.houses.crud import HousesCRUD
from app.routers.houses.models import HousingTypes

flag_for_log = True

async def get_house_info(session, url, headers, db):

    async with session.get(url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")
        short_house_info = soup.find(class_="attr g").find_all(class_=("c")) if soup.find(class_="attr g") != None else None
        if short_house_info == None:
            global flag_for_log
            if flag_for_log:
                with open("logs/log_async_"+url.split("/")[4] + "_" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ".txt", "w") as file:
                    file.write(response_text)
                flag_for_log = False
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
        

async def get_page_info(db):

    ua = UserAgent()

    url = "https://www.list.am/category/62"

    def get_headers():
        return  {
                "Accept":"*/*",
                "User-Agent":ua.random
                }      
      

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=get_headers())
        soup = BeautifulSoup(await response.text(), "lxml")
        all_houses = soup.find_all(class_="dl")[1].find(class_="gl")

        tasks = []

        for element in all_houses:
            house_href = "https://www.list.am" + element.get("href")
            task = asyncio.create_task(get_house_info(session, house_href, get_headers(), db))
            tasks.append(task)

        await asyncio.gather(*tasks)

                

async def async_scraper(db):
    start_time = time.time()

    await get_page_info(db)

    end_time = time.time()
    print("============", end_time - start_time, "===========")

