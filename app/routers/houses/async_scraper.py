import time
import json
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
            print(url)
            global flag_for_log
            if flag_for_log:
                with open("logs/log_async_"+url.split("/")[4] + "_" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ".txt", "w") as file:
                    file.write(response_text)
                flag_for_log = False
            return None
        adress = soup.find(class_="loc").text if soup.find(class_="loc") != None else None
        price = soup.find(class_="price x").text if soup.find(class_="price x") != None else None

        about_house = {}
        for i in short_house_info:
            key = i.find(class_="t").text
            value = i.find(class_="i").text
            about_house[key] = value

        about_house_json = json.dumps(about_house, ensure_ascii=False)

        land_info = soup.find_all(class_="attr g")[1].find(class_="i").text if soup.find_all(class_="attr g")[1] != None else None

        date_info = soup.find(class_="footer").text.split("Տեղադրված է ")[1].split("Թարմացվել է ")
        if len(date_info) == 1:
            date_info.append(None)

        data = {
            "housing_type": HousingTypes.house.value,
            "url": url,
            "adress": adress,
            "price": price,
            "short_info": about_house_json,
            "land_info": land_info,
            "created_statement": date_info[0],
            "updated_statement": date_info[1],
        }

        await HousesCRUD.add_house(data, db)
        

async def get_page_info(db):

    ua = UserAgent()

    url = "https://www.list.am/category/62"

    def get_headers():
        return  {
                "Accept":"*/*",
                "User-Agent":ua.random
                }      
      
    try:
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
    except Exception as e:
        print(e)

                

async def async_scraper(db):
    start_time = time.time()

    await get_page_info(db)

    end_time = time.time()
    print("============", end_time - start_time, "===========")

