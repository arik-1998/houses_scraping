import time
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from app.routers.houses.crud import HousesCRUD
from app.routers.houses.models import HousingTypes
from app.helpers.utils import extract_dates
from loguru import logger



async def get_house_info(session, url, headers, db):

    async with session.get(url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")

        if soup.find(class_="attr g"):
            short_house_info = soup.find(class_="attr g").find_all(class_=("c"))
        else:
            return None

        try: 
            about_house = {}
            for i in short_house_info:
                key = i.find(class_="t").text.replace(" ","_").lower()
                value = i.find(class_="i").text
                about_house[key] = value
        except: about_house = {}
        
        about_house_json = json.dumps(about_house, ensure_ascii=False)

        try:
            adress = soup.find(class_="loc").text
        except: adress = None

        try:
            price = soup.find(class_="price x").text
        except: price = None


        try:
            land_info = soup.find_all(class_="attr g")[1].find(class_="i").text
        except: land_info=None

        date_info = extract_dates(soup.find(class_="footer").text)

        data = {
            "housing_type": HousingTypes.house.value,
            "url": url,
            "adress": adress,
            "price": price,
            "short_info": about_house_json,
            "land_info": land_info,
            "created_statement": date_info["creating"],
            "updated_statement": date_info["updating"],
        }

        await HousesCRUD.add_house(data, db)
        

async def get_page_info(db):

    ua = UserAgent()

    page_number = 1

    url = f"https://www.list.am/en/category/62/{page_number}?type=1&n=0&sid=0" #english page with filter by "search" (not want)

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
        logger.error(e)

                

async def async_scraper(db):
    start_time = time.time()

    await get_page_info(db)

    end_time = time.time()
    print("============", end_time - start_time, "===========")

