import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def get_links(text):
    ua = "User-Agent"
    response = requests.get(
        url=f"https://hh.ru/search/vacancy?area=54&area=2&search_field=name&search_field=company_name&search_field=description&text={text}&page=1",
        headers={"user-agent": ua}
    )
    if response.status_code != 200:
        return
    print(response.text)
    soup = BeautifulSoup(response.text, "lxml")
    try:
        page_count = int(soup.find("div", attrs={"class_":"pager"}).find_all("span", recursive= False)[-1].find("a").find("span").text)
    except:
        return
    # for page in range(page_count):
    #     data = requests.get(
    #         url=f"https://hh.ru/search/vacancy?area=54&area=2&search_field=name&search_field=company_name&search_field=description&text={text}&page={page}",
    #         headers={"user-agent": ua}
    #     )


def get_resume(link):
    pass


if __name__ == '__main__':
    get_links("python")