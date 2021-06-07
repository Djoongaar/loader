import os
import random
import re
import time
import datetime
import joblib
from psycopg2 import errors
from xvfbwrapper import Xvfb
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from seleniumwire import webdriver
from isso_bot import bot
from utils import tokenize_lemmatize, num_to_cat, num_to_type
import sql_requests
import requests
import config
from bs4 import BeautifulSoup

svm_type_classifier = joblib.load('/home/eugene/Projects/loader/ml_classifiers/svm_type_classifier.joblib')
svm_category_classifier = joblib.load('/home/eugene/Projects/loader/ml_classifiers/svm_category_classifier.joblib')


# ================================== ЗАГРУЗКА ТЕНДЕРОВ ==================================


def update_tenders(customer_inn):
    """
    Качает новые тендеры по ИНН контрагента, классифицирует по типу объекта,
    категориям работ и записывает в базу данных
    :param customer_inn:
    :return:
    """
    # vdisplay = Xvfb()
    # vdisplay.start()
    latest_date = sql_requests.get_latest_date_by_customer(customer_inn) - datetime.timedelta(days=2)
    print(type(latest_date), latest_date)
    chrome_options = Options()
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1580,920")
    driver = webdriver.Chrome('/home/eugene/Projects/loader/chromedriver', chrome_options=chrome_options)
    driver.get("https://zakupki.gov.ru/")
    input_search = driver.find_element_by_id("quickSearchForm_header_searchString")
    driver.execute_script("arguments[0].click();", input_search)
    input_search.send_keys(customer_inn)
    time.sleep(0.5)
    input_search.submit()
    time.sleep(random.randint(1, 3))
    tenders = []
    # Запускаем цикл сбора информации и складываем в tenders
    while True:
        time.sleep(0.5)

        # Загрузка данных по тендеру
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        numbers = soup.find_all("div", class_="search-registry-entry-block box-shadow-search-input")
        new_tenders = []
        for i in numbers:
            try:
                number = i.find("div", class_="registry-entry__header-mid__number").text.strip()[2:]
                start_prices = sum([int(''.join(re.findall(r'\d', price.text))) / 100 for price in i
                                   .find_all("div", class_="price-block__value")])
                dates = i.find_all("div", class_="data-block mt-auto")
                created = "-".join(
                    re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[0].text)[::-1])
                updated_year, updated_month, updated_date = \
                    re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[1].text)[::-1]
                statuses = i.find("div", class_="registry-entry__header-mid__title").text.strip()
                names = i.find("div", class_="registry-entry__body-value").text.strip()
                updated = datetime.date(int(updated_year), int(updated_month), int(updated_date))
                if updated > latest_date:
                    new_tenders.append({
                        "model": "tendersapp.tender",
                        "pk": number,
                        "fields": {
                            "start_price": start_prices,
                            "final_price": 0,
                            "created": created,
                            "updated": updated,
                            "status": statuses,
                            "name": names,
                            "customer_inn": str(customer_inn)
                        }
                    })
            except:
                print(f'Exception erased with number {i}')
        time.sleep(0.5)
        if new_tenders:
            tenders.extend(new_tenders)
            button_next = driver.find_element_by_class_name("paginator-button-next")
            driver.execute_script("arguments[0].click();", button_next)
            time.sleep(random.randint(1, 3))
        else:
            print(f'Обновлено {len(tenders)}!')
            break
    driver.close()
    # vdisplay.stop()
    for t in tenders:
        # Идем циклом по тендерам и вставляем в СУБД
        tender = classify_tender(t)
        print(tender['fields']['name'])
        print(tender['fields']['type'], tender['fields']['category'])
        try:
            sql_requests.insert_into_tendersapp_tender(tender)
        except errors.lookup('42601') as e:
            # psycopg2.errors.SyntaxError
            print(f"WARNING!!! in tender {tender} raised an exception {e}")
            pass
    return len(tenders)


def download_tenders(customer_inn):
    """
        Качает все имеющиеся тендеры по ИНН контрагента, классифицирует по типу объекта,
        категориям работ и записывает в базу данных
        :param customer_inn:
        """

    vdisplay = Xvfb()
    vdisplay.start()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    driver.get("https://zakupki.gov.ru/")
    input_search = driver.find_element_by_id("quickSearchForm_header_searchString")
    input_search.click()
    input_search.send_keys(customer_inn)
    time.sleep(0.5)
    input_search.submit()
    time.sleep(random.randint(1, 3))
    tenders = []
    # Запускаем цикл сбора информации и складываем в tenders
    while True:
        time.sleep(0.5)

        # Загрузка данных по тендеру
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        numbers = soup.find_all("div", class_="search-registry-entry-block box-shadow-search-input")
        new_tenders = []
        for i in numbers:
            try:
                number = i.find("div", class_="registry-entry__header-mid__number").text.strip()[2:]
                start_prices = sum([int(''.join(re.findall(r'\d', price.text))) / 100 for price in i
                                   .find_all("div", class_="price-block__value")])
                dates = i.find_all("div", class_="data-block mt-auto")
                created = "-".join(
                    re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[0].text)[::-1])
                updated_year, updated_month, updated_date = \
                    re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[1].text)[::-1]
                statuses = i.find("div", class_="registry-entry__header-mid__title").text.strip()
                names = i.find("div", class_="registry-entry__body-value").text.strip()
                updated = datetime.date(int(updated_year), int(updated_month), int(updated_date))
                new_tenders.append({
                    "model": "tendersapp.tender",
                    "pk": number,
                    "fields": {
                        "start_price": start_prices,
                        "final_price": 0,
                        "created": created,
                        "updated": updated,
                        "status": statuses,
                        "name": names,
                        "customer_inn": str(customer_inn)
                    }
                })
            except:
                print(f'Exception erased with number {i}')
        time.sleep(0.5)
        tenders.extend(new_tenders)
        try:
            button_next = driver.find_element_by_class_name("paginator-button-next")
            driver.execute_script("arguments[0].click();", button_next)
            time.sleep(random.randint(1, 3))
        except NoSuchElementException:
            print(f'Обновлено {len(tenders)}!')
            break
    driver.close()
    vdisplay.stop()
    for t in tenders:
        # Идем циклом по тендерам и вставляем в СУБД
        tender = classify_tender(t)
        print(tender['fields']['name'])
        print(tender['fields']['type'], tender['fields']['category'])
        try:
            sql_requests.insert_into_tendersapp_tender(tender)
        except errors.lookup('42601') as e:
            # psycopg2.errors.SyntaxError
            print(f"WARNING!!! in tender {tender} raised an exception {e}")
            pass


# ================================== ЗАГРУЗКА ПЛАН-ГРАФИКОВ ==================================


def download_plans(customer_inn):
    vdisplay = Xvfb()
    vdisplay.start()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    driver.get("https://zakupki.gov.ru/epz/orderplan/search/results.html?morphology=on&search-filter="
               "%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F"
               "&structured=true&fz44=on&customerPlaceWithNested=on&actualPeriodRangeYearFrom=2020"
               "&sortBy=BY_MODIFY_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&searchType=false")
    input_search = driver.find_element_by_id("searchString")
    input_search.click()
    input_search.send_keys(customer_inn)
    time.sleep(0.5)
    input_search.submit()
    time.sleep(1)
    number = int(''.join(re.findall(r'\d+', driver.find_element_by_class_name("search-results__total").text)))
    plans = []
    try:
        link_div = driver.find_element_by_class_name("registry-entry__body-caption")
        button = link_div.find_element_by_tag_name('a')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        page = driver.page_source
        plans_list = parsing_plans(page, customer_inn)
        plans.extend(plans_list)
        # Запускаем цикл сбора информации, которую затем преобразовавыем в формат json и складываем в переменную tenders
        try:
            while True:
                time.sleep(random.randint(1, 2))
                button_next = driver.find_element_by_class_name("paginator-button-next")
                driver.execute_script("arguments[0].click();", button_next)
                time.sleep(random.randint(1, 2))
                page = driver.page_source
                plans_list = parsing_plans(page, customer_inn)
                plans.extend(plans_list)
        # Если в блоке пагинации нет элемента "next page" значит мы дошли до конца списка
        except NoSuchElementException:
            driver.close()
            vdisplay.stop()
            if len(plans) == number == 0:
                print(f"У клиента с ИНН {customer_inn} нет план-гафика.")
                return False
            elif len(plans) >= number * 0.99 or len(plans) == 1000:
                # Если у контрагента есть закупки и мы почти все получили, то возвращаем True и записываем в СУБД
                print(f"Загрузка торгов по ИНН {customer_inn} завершена успешно.")
                for plan in plans:
                    # Идем циклом по планам и вставляем в СУБД
                    sql_requests.insert_into_tendersapp_plan(plan)
                return True
            elif len(plans) < number * 0.99:
                # Если у контрагента есть закупки но по какой-то причине нам не удалось их загрузить - вызываем рекурсию
                print(f"Во время загрузки торгов по ИНН {customer_inn} часть данных была потеряна.\n"
                      f"Объявлено планов: {number}, загружено планов: {len(plans)}\n")
                download_plans(customer_inn)
                return True
            else:
                # Если хз какой результат - возвращаем False и выходим из программы
                print(f"Что-то пошло не так во время загрузки планов клиента с ИНН {customer_inn}")
                return False
        # Вызвать сообщение если возникнет какая-то другая ошибка
        except:
            print(f"{customer_inn} raised exception")
            driver.close()
            vdisplay.stop()
            return False
    except:
        driver.close()
        vdisplay.stop()
        print(f"{customer_inn} raised exception")
        return False


def parsing_plans(page, customer_inn):
    plans = []
    soup = BeautifulSoup(page, 'html.parser')
    numbers = soup.find_all("div", class_="search-registry-entry-block box-shadow-search-input")
    for i in numbers:
        try:
            number = i.find("div", class_="registry-entry__header-mid__number").text.strip()
            dates = i.find_all("div", class_="data-block mt-auto")
            start_prices = "".join(
                re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[0].text))
            created = "-".join(
                re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[1].text)[::-1])
            updated = "-".join(
                re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[2].text)[::-1])
            names = i.find("div", class_="registry-entry__body-value").text.strip()
            year = i.find("div", class_="d-flex lots-wrap-content__body__val").text.strip()
            plans.append({
                "model": "tendersapp.plan",
                "pk": number,
                "fields": {
                    "start_price": int(start_prices) / 100,
                    "created": created,
                    "updated": updated,
                    "name": names,
                    "year": year,
                    "customer_inn": str(customer_inn)
                }
            })
        except IndexError as e:
            number = i.find("div", class_="registry-entry__header-mid__number").text.strip()
            dates = i.find_all("div", class_="data-block mt-auto")
            start_prices = 0
            created = "-".join(
                re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[0].text)[::-1])
            updated = "-".join(
                re.findall(r'\d+', dates[0].find_all("div", class_="data-block__value")[1].text)[::-1])
            names = i.find("div", class_="registry-entry__body-value").text.strip()
            year = i.find("div", class_="d-flex lots-wrap-content__body__val").text.strip()
            plans.append({
                "model": "tendersapp.plan",
                "pk": number,
                "fields": {
                    "start_price": start_prices,
                    "created": created,
                    "updated": updated,
                    "name": names,
                    "year": year,
                    "customer_inn": str(customer_inn)
                }
            })
            print(f'{customer_inn} {number}')
            print(f'{e}')
    print(type(plans))
    return plans


# ================================== ЗАГРУЗКА ЮРЛИЦ ИЗ DADATA API ==================================


def find_customer(company_inn):
    post = f"https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Token {config.API_KEY}"
    }
    data = {
        'query': f"{company_inn}"
    }
    res = requests.post(post, headers=headers, json=data)
    response = res.json()["suggestions"][0]
    district = response["data"]["address"]["data"]["federal_district"]
    if district == 'Центральный':
        district_id = 91
    elif district == 'Южный':
        district_id = 92
    elif district == 'Северо-Западный':
        district_id = 93
    elif district == 'Дальневосточный':
        district_id = 94
    elif district == 'Сибирский':
        district_id = 95
    elif district == 'Уральский':
        district_id = 96
    elif district == 'Приволжский':
        district_id = 97
    elif district == 'Северо-Кавказский':
        district_id = 98
    else:
        district_id = 91
    valid_data = {
        "model": "projectsapp.customer",
        "pk": str(response["data"]["ogrn"]),
        "fields": {
            "title": response["value"],
            "fullname": response["data"]["name"]["full_with_opf"],
            "management": response["data"]["management"]["post"] if response["data"]["management"] else None,
            "name": response["data"]["management"]["name"] if response["data"]["management"] else None,
            "inn": response["data"]["inn"],
            "kpp": response["data"]["kpp"],
            "okved": response["data"]["okved"],
            "form_code": response["data"]["opf"]["code"] if response["data"]["opf"] else None,
            "form_title": response["data"]["opf"]["full"] if response["data"]["opf"] else None,
            "address": response["data"]["address"]["unrestricted_value"],
            "district_id": district_id
        }
    }
    print(valid_data)
    sql_requests.insert_into_projectsapp_customer(valid_data)
    return valid_data


# ================================== КЛАССИФИКАЦИЯ ТЕНДЕРОВ ==================================


def classify_tender(tender):
    """ Классифицирует тендеры по типам и категориям (Ставит метки классов) """
    token = [tokenize_lemmatize(tender['fields']['name'])]
    tender['fields']['type'] = num_to_type(svm_type_classifier.predict(token)[0])
    tender['fields']['category'] = num_to_cat(svm_category_classifier.predict(token)[0])

    return tender


# ================================== ЗАГРУЗЧИК ДОКУМЕНТОВ ==================================


def is_downloaded(path_, chat_id):
    while any([filename.endswith(".crdownload") for filename in os.listdir(path_)]):
        time.sleep(5)
        bot.send_message(chat_id, f"Почти всё загружено, пагади-ну!)")
        print(".", end="")
    return True


def download_documents(chat_id: int, customer_inn: str):
    """
    Загружаем документацию по проектам с госзакупок
    :param chat_id:
    :param customer_inn:
    :return:
    """
    # Шаг 1. Загружаем айдишники проектов по заказчику из БД
    projects = sql_requests.get_projects_list(customer_inn)
    projects_count = len(projects)
    company_title = sql_requests.get_company_title(customer_inn)
    bot.send_message(chat_id, f"Начинаем загрузку проектов {company_title['title']}")
    bot.send_message(chat_id, f"Будет загружено {projects_count} объекта(-ов)")
    print(f"Начинаем загрузку проектов контрагента {company_title['title']}")
    print(f"Будет загружено {projects_count} объекта(-ов)")
    print(projects)
    time.sleep(5)
    # Шаг 2. Проверяем есть ли уже эта документация в БД или проверяем на этапе загрузки... Пока хз

    # Шаг 3. Если такой документации в БД нет, то грузим
    for project in projects:
        try:
            download_dir = f"/home/jeka/Projects/loader/documents/{customer_inn}/{project}"

            # Запускаю хром драйвер с настроками
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1580,920")
            driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior',
                      'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            driver.execute("send_command", params)
            driver.get("https://zakupki.gov.ru/")

            # В окно страницы вводится номер тендера (проекта)
            bot.send_message(chat_id, f"Начинаем загрузку проекта {project}")
            print(f"Начинаем загрузку проекта {project}")
            input_search = driver.find_element_by_class_name("search__input")
            driver.execute_script("arguments[0].click();", input_search)

            # Открывается новое окно с карточкой проекта
            input_search.clear()
            input_search.send_keys(f"{project}")
            input_search.submit()
            time.sleep(2)
            number = driver.find_element_by_class_name("registry-entry__header-mid__number")
            result = number.find_element_by_tag_name("a")
            driver.execute_script("arguments[0].click();", result)
            time.sleep(5)

            driver.switch_to.window(driver.window_handles[1])
            files = driver.find_elements_by_class_name("tabsNav__item")
            driver.execute_script("arguments[0].click();", files[1])
            time.sleep(5)

            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": "true",
                # "download.extensions_to_open": ""
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            driver_2 = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)

            # Ищу вложенные документы и скачиваю
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            pattern = re.compile(r'row no-gutters notice-documents blockInfo__section first-row-active-documents *')
            divs = soup.find_all("div", class_=pattern)
            attachments = []

            # Создаю папку для загрузки документов и указываю для хром драйвера
            try:
                os.makedirs(f"/home/jeka/Projects/loader/documents/{customer_inn}/{project}")
            except OSError:
                bot.send_message(chat_id, f"Папка проекта {project} уже существует")
                print(f"Папка проекта {project} уже существует")
            else:
                print(f"Создана папка проекта {project}")
                time.sleep(random.randint(2, 5))

            for div in divs:
                pattern = re.compile(r'attachment row *')
                attachments.extend(div.find_all("div", class_=pattern))
            for attachment in attachments:
                try:
                    link = attachment.find("span", class_="section__value")
                    if link.find("a", href=True)["title"].endswith(('.pdf', '.rar', '.zip', '.7z', '.dwg', '.dxf')):
                        a = link.find("a", href=True)["href"]
                        driver_2.get(a)
                        time.sleep(5)
                except WebDriverException as e:
                    print(e)
                    pass
            if is_downloaded(f"/home/jeka/Projects/loader/documents/{customer_inn}/{project}", chat_id):
                projects_count -= 1
                bot.send_message(chat_id, f"Осталось загрузить {projects_count} проекта(-ов)")
                print(f"Осталось загрузить {projects_count} проекта(-ов)")
                time.sleep(5)
            # Закрываем окно
            driver_2.close()
            driver.quit()
        except (NoSuchElementException, IndexError, requests.exceptions.ConnectionError):
            print(f"500 SERVER ERROR on project {project}")
            bot.send_message(chat_id, f"500 SERVER ERROR on project {project}")
            driver.quit()
            time.sleep(5)

    bot.send_message(chat_id, f"Загрузка проектов {company_title['title']} завершена")
    print(f"Загрузка проектов {company_title} завершена")
    return projects


def unrar_docs():
    """
    using subprocess and unrar utility takes a docs from archives
        for filename in *.rar;
        do destination="${filename%.rar}";
        mkdir "$destination"; unrar x -r "$filename" "$destination";
        done
    :return: None
    """
    pass
# ================================== КАНДИДАТЫ НА УДАЛЕНИЕ ==================================
