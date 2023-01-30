"""
Scrapper for hh.ru - заданы параметры для поиска работы без опыта, либо до года. Так же поиск стажировок и онлайн курсов от IT фирм из РФ, РБ, РК.

Данная версия не очень гибкая. Ссылки забиты жестко со всеми нужными атрибутами, в будущем нужно реализовать подобие фильтра, для выбора разных критериев. Мин. приоритет

Отладка:
-В конце ссылки необходимо писать &customDomain=1 - hh.ru по дефолту определяет месторасположение, и изменяет возвращаемые ссылки hh.ru на tomsk.hh.ru
-Доработать - Возможны ошибки если hh.ru изменит теги в структуре сайтов, необходимо, через код стр, получить через теги с атрибутами номер последней стр в выборке.

Выбор стран:
РФ - area=113
Беларусь - area=16
Казахстан - area=40

ссылка с кучей фильтров без опыта, игнор вакансий где нет опыта, но внутри требуют опыта
url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text={text}&no_magic=true&L_save_area=true&items_on_page=20&page={page}&customDomain=1",
Ссылка с кучей фильтров с годом опыта, игнор вакансий где в описании требуют опыт 1,5+ лет
https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=2+%D0%BB%D0%B5%D1%82%2C+2+%D0%B3%D0%BE%D0%B4%D0%B0%2C+3+%D0%BB%D0%B5%D1%82%2C+3+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1.5+%D0%BB%D0%B5%D1%82%2C+1.5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%B3%D0%BE%D0%B4%D0%B0%2C+1%2C5+%D0%BB%D0%B5%D1%82&experience=between1And3&search_field=name&search_field=company_name&search_field=description&text={text}&from=suggest_post&no_magic=true&ored_clusters=true&items_on_page=20&page={page}&customDomain=1

Проработать фильтр внутри вакансии 2 лет, 2 года, 3 лет, 3 года, 1.5 лет, 1.5 года, 1,5 года, 1,5 лет
"""
import requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
import time
import json
import api_google_sheet as api



def get_keywords_from_config():
    parser = ConfigParser()
    parser.read("config.ini", encoding="utf-8")
    keywords = parser['keywords']['keywords']
    print(keywords)
def get_links(text):
    ua = "User-Agent"
    response = requests.get(
        url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&text={text}&no_magic=true&ored_clusters=true&items_on_page=20&experience=noExperience&enable_snippets=true&excluded_text=&customDomain=1",
        headers={"user-agent": ua}
    )
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, "lxml")
    # спарсим количество страниц, для перебора, перехода и получить с них данные в дальнейшем
    try:
        max_page = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        max_page = 0
    # выборка страниц с вакансиями по запросу, проходим по страницам, возвращаем ссылку
    for page in range(max_page+1):
        try:
            resp = requests.get(
                url=f"https://hh.ru/search/vacancy?area=16&area=113&area=40&excluded_text=&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text={text}&no_magic=true&L_save_area=true&items_on_page=20&page={page}&customDomain=1",
                headers={"user-agent": ua}
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "lxml") # Не удалять, это нужнно при переходе на новую стр, получать новое содержание, которое распарсим
                for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                    yield f'{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_content(link):
    ua = "User-Agent"
    data = requests.get(
        url=link,
        headers={"user-agent": ua}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"data-qa": "vacancy-title"}).text
    except:
        name = "Fail"
    try:
        name_firm = soup.find(attrs={"data-qa": "vacancy-company__details"}).text
    except:
        name_firm = "Fail"
    try:
        salary = soup.find(attrs={"data-qa": "vacancy-salary"}).text.replace("\u2009", "").replace(
            "\xa0", "")
    except:
        salary = "Fail"
    try:
        link_vacancy = link
    except:
        link_vacancy = "Fail"
    try:
        link_firm = "https://hh.ru" + soup.find(attrs={"class": "vacancy-company-details"}).find(attrs={"data-qa": "vacancy-company-name"}).get('href')
    except:
        link_firm = "Fail"
    try:
        description_vacancy = soup.find(attrs={"data-qa": "vacancy-description"}).get_text()
    except:
        description_vacancy = "Fail"
    print(name, salary, link_vacancy, name_firm, link_firm, description_vacancy)
    # Что то сделать с return - выдает в консоль лишний None
    # return

# def check_keywords(*args):
#     pass

if __name__ == '__main__':
    # Подключение к sheets, poluchit i zapisat dannie
    # connected_to_file = api.connect_to_file()
    i = 0
    for link in get_links("python"):
        i += 1
        print(link)
        get_content(link)
        time.sleep(1)
    print("Число спарсенных ссылок" + str(i))
    # api.get_data_from_sheets(connected_to_file) - нужно чтобы в будущем сравнить по ссылке если есть но не записываем
    # api.push_data_to_sheets(connected_to_file, name, salary, link_vacancy, name_firm, link_firm)




