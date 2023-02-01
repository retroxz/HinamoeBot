from httpx import AsyncClient
from utils.config import Config
from bs4 import BeautifulSoup
import platform

# if platform.system() == "Windows":
#     import asyncio
#
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = "http://www.eclzz.love"


async def get_bt_info(keyword: str, page: int):
    """
    获取资源信息
    :param keyword: 关键词
    :param page: 页数
    """
    async with AsyncClient(proxies=None) as client:
        text = (await client.get(F"{url}/s/{keyword}_rel_{page}.html")).text
        if "大约0条结果" in text:
            return
        soup = BeautifulSoup(text, "lxml")
        item_lst = soup.find_all("div", {"class": "search-item"})
        bt_max_num = Config.get('max_number', 5)
        bt_max_num = bt_max_num if bt_max_num < len(item_lst) else len(item_lst)
        for item in item_lst[:bt_max_num]:
            divs = item.find_all("div")
            title = (
                str(divs[0].find("a").text)
                .replace("<em>", "")
                .replace("</em>", "")
                .strip()
            )
            spans = divs[2].find_all("span")
            type_ = spans[0].text
            create_time = spans[1].find("b").text
            file_size = spans[2].find("b").text
            print(divs[0].find("a")["href"])
            link = await get_download_link(divs[0].find("a")["href"])
            print(link)
            yield title, type_, create_time, file_size, link


async def get_download_link(_url: str) -> str:
    """
    获取资源下载地址
    :param _url: 链接
    """
    async with AsyncClient(proxies=None) as client:
        text = (await client.get(f"{url}{_url}")).text
        soup = BeautifulSoup(text, "lxml")
        return soup.find("a", {"id": "down-url"})["href"]
