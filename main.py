"""
Scrapper for hh.ru
-В конце ссылки необходимо писать &customDomain=1 - это позволит получать все ссылки в виде
hh.ru, а не (наше месторасположение) omsk.hh.ru

Выбор стран:
РФ - area=113
Белорусь - area=16
Казахстан - area=40
https://hh.ru/search/vacancy?area=40&area=113&area=16&search_field=name&search_field=company_name&search_field=description&text=jupiter&no_magic=true&ored_clusters=true&items_on_page=20&enable_snippets=true

ссылка с кучей фильтров без опыта
url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=2+%D0%BB%D0%B5%D1%82%2C+2+%D0%B3%D0%BE%D0%B4%D0%B0%2C+3+%D0%BB%D0%B5%D1%82%2C+3+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1.5+%D0%BB%D0%B5%D1%82%2C+1.5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%BB%D0%B5%D1%82&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text={text}&no_magic=true&L_save_area=true&items_on_page=20&page={page}&customDomain=1",
Ссылка с годом опыта
https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=2+%D0%BB%D0%B5%D1%82%2C+2+%D0%B3%D0%BE%D0%B4%D0%B0%2C+3+%D0%BB%D0%B5%D1%82%2C+3+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1.5+%D0%BB%D0%B5%D1%82%2C+1.5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%BB%D0%B5%D1%82&experience=between1And3&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&no_magic=true&ored_clusters=true&items_on_page=20&page=0
"""
import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def get_links(text):
    ua = "User-Agent"
    response = requests.get(
        url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=2+%D0%BB%D0%B5%D1%82%2C+2+%D0%B3%D0%BE%D0%B4%D0%B0%2C+3+%D0%BB%D0%B5%D1%82%2C+3+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1.5+%D0%BB%D0%B5%D1%82%2C+1.5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%BB%D0%B5%D1%82&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&no_magic=true&ored_clusters=true&items_on_page=20&page=0&customDomain=1",
        headers={"user-agent": ua}
    )
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, "lxml")
    # спарсим количество страниц, для перебора, перехода и получить с них данные в дальнейшем
    try:
        max_page = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return
    # выборка страниц с вакансиями по запросу, проходим по страницам, возвращаем ссылку
    for page in range(max_page+1):
        try:
            resp = requests.get(
                url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=2+%D0%BB%D0%B5%D1%82%2C+2+%D0%B3%D0%BE%D0%B4%D0%B0%2C+3+%D0%BB%D0%B5%D1%82%2C+3+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1.5+%D0%BB%D0%B5%D1%82%2C+1.5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%BB%D0%B5%D1%82&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text={text}&no_magic=true&L_save_area=true&items_on_page=20&page={page}&customDomain=1",
                headers={"user-agent": ua}
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "lxml") # Не удалять, это нужнно при переходе на новую стр, получать новое содержание, которое распарсим
                for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                    yield f'{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_resume(link):
    pass


if __name__ == '__main__':
    i = 0
    for link in get_links("python"):
        i += 1
        print(link)
    print(i)






