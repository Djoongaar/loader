import re
import time

import joblib

import loader
from config import hello, menu, token
import telebot
import sql_requests
from db_worker import States
import nltk
nltk.download('stopwords')
nltk.download('punkt')
svm_type_classifier = joblib.load('/home/eugene/Projects/loader/ml_classifiers/svm_type_classifier.joblib')
svm_category_classifier = joblib.load('/home/eugene/Projects/loader/ml_classifiers/svm_category_classifier.joblib')

# ============================== BOT API CONNECTION ==============================

bot = telebot.TeleBot(token)


# ============================== PROCESS MESSAGE ==============================


@bot.message_handler(commands=["start"])
def say_hello(message):
    bot.send_message(message.chat.id, hello(message.from_user.first_name))
    time.sleep(1)
    bot.send_message(message.chat.id, menu, parse_mode='HTML')
    States.add_state(message.chat.id, message.text)


@bot.message_handler(commands=["back"])
def callbacks(message):
    """
    Эта штука пока не работает но в будущем улучшит навигацию позволив командой /back
    возвращаться к предыдущему пункту меню. Будет реализована с помощью стэка по типу
    команды /nextRegions или /nextCustomers (они ниже)
    """
    back = States.get_state(message.chat.id)
    if back == "/start":
        say_hello(message)
    elif back == "/customers":
        customer_list(message)
    elif back == "None":
        print("None")
    else:
        print("Ошибка в callbacks")


# ==================================================== CURRENT MENU ===================================================
@bot.message_handler(commands=["menu"])
def menu_message(message):
    bot.send_message(message.chat.id, menu, parse_mode='HTML')


@bot.message_handler(commands=["nextRegions"])
def next_regions(message):
    """
    Чтобы не заспамливать клиента кучей сообщений я сохраняю их в стэке и вывожу по 5 штук за раз
    если юзер выдаст команду /nextRegions из стэка вырезутся и вернутся 5 сообщений
    """
    try:
        for i in range(5):
            report, length = States.get_regions(message.chat.id)
            bot.send_message(message.chat.id, report, parse_mode='HTML')
        if length > 0:
            bot.send_message(message.chat.id, '... следующие 5: <i>/nextRegions</i>\n'
                                              'Главное меню: <i>/menu</i>', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, '[...] Конец списка\n'
                                              'Главное меню: <i>/menu</i>', parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, '[...] Конец списка\n'
                                          'Главное меню: <i>/menu</i>', parse_mode='HTML')


@bot.message_handler(commands=["regions"])
def regions_list(message):
    """ Функция выводит список регионов прямо из стэка ведис а туда кладёт из СУБД """
    regions = sql_requests.regions_list()
    States.add_regions(message.chat.id, regions)
    next_regions(message)


@bot.message_handler(regexp="region\d{2}")
def region_details(message):
    reg_id = ''.join(re.findall(r'\d', message.text))
    print(reg_id)
    reg_rep = sql_requests.regions_details(reg_id)
    if reg_rep:
        bot.send_message(message.chat.id, reg_rep, parse_mode='HTML')


@bot.message_handler(commands=["nextCustomers"])
def next_customers(message):
    try:
        for i in range(5):
            report, length = States.get_customers(message.chat.id)
            bot.send_message(message.chat.id, report, parse_mode='HTML')
        if length > 0:
            bot.send_message(message.chat.id, '1) Cледующие 5: <i>/nextCustomers</i>\n'
                                              '2) Вернуться в главное меню: <i>/menu</i>', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Конец списка ...\n'
                                              'Вернуться в главное меню: <i>/menu</i>', parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 'Конец списка ...\n'
                                          'Вернуться в главное меню: <i>/menu</i>', parse_mode='HTML')


@bot.message_handler(commands=["customers"])
def customer_list(message):
    """ Функция записывает в ведис стэк клиентов """
    customers = sql_requests.customers_list()
    States.add_customers(message.chat.id, customers)
    next_customers(message)


@bot.message_handler(regexp="/\d{10}")  # customer_inn, customer details
def customer_details(message):
    """
    Функция формирует полный отчет из трёх частей по контрагенту:
    Часть 1: Общие данные по контрагенту. Идет запрос в СУБД если нет то на API https://dadata.ru/api/suggest/party/
    Часть 2: Все проекты.
    Часть 3: План закупок контрагента.
    :param message: объект message (а оттуда чат id и ИНН контрагента)
    :return: None
    """
    # Сохраняю введенный ИНН в Vedis для дальнейшего использования
    States.set_inn(message.chat.id, message.text[1:])

    # ---------------------   ОБЩИЕ ДАННЫЕ ПО КОНТРАГЕНТУ   ---------------------
    # Пытаюсь получить отчет из СУБД и записать в переменную "mes"
    mes = sql_requests.customer_details(message.text[1:])
    if mes:
        # Если в отчет из СУБД вернулся то отправляю его
        bot.send_message(message.chat.id, mes, parse_mode="HTML")
    else:
        # а иначе шлю запрос в DADATA API и делаю INSERT в СУБД
        try:
            loader.find_customer(message.text[1:])
            mes = sql_requests.customer_details(message.text[1:])
            bot.send_message(message.chat.id, mes, parse_mode="HTML")
        except IndexError as e:
            # Если IndexError то значит такого контрагента нет ни в одной СУБД
            print(e)
            mes = 'Такой организации нет ни в одной базе данных. Пожалуйста проверьте правильность набора ИНН.'
            bot.send_message(message.chat.id, mes, parse_mode="HTML")
        except:
            # Если другой исключение то что-то пошло не так
            print("Что-то пошло не так")
            mes = "Что-то пошло не так"
            bot.send_message(message.chat.id, mes, parse_mode="HTML")

    # ---------------------   ВСЕ ПРОЕКТЫ КОНТРАГЕНТА   ---------------------

    bot.send_message(message.chat.id, "<b>Загрузить проекты: </b>\n /download_documents\n", parse_mode="HTML")

    # ---------------------   ОБНОВИТЬ ТЕНДЕРЫ КОНТРАГЕНТА   ---------------------

    bot.send_message(message.chat.id, "<b>Обновить тендеры: </b>\n /update_tenders\n", parse_mode="HTML")

    # ---------------------   ПЛАН ЗАКУПОК КОНТРАГЕНТА   ---------------------
    plans_report = sql_requests.plans_report(message.text[1:])
    if plans_report:
        bot.send_message(message.chat.id, plans_report, parse_mode="HTML")


@bot.message_handler(commands=["download_documents"])
def download_documents(message):
    projects = loader.download_documents(message.chat.id, States.get_inn(message.chat.id))
    if projects:
        print(projects)
    else:
        print('No projects')


@bot.message_handler(commands=["future_projects"])
def download_plans(message):
    future_projects = sql_requests.future_projects(States.get_inn(message.chat.id))
    for project in future_projects:
        bot.send_message(message.chat.id, project)


@bot.message_handler(commands=["update_tenders"])
def update_tenders(message):
    customer = sql_requests.get_company_title(States.get_inn(message.chat.id))
    mes = f"Начинаю загрузку клиента: {customer['title']}"
    bot.send_message(message.chat.id, mes, parse_mode="HTML")
    result = loader.update_tenders(States.get_inn(message.chat.id))
    if result:
        mes = f"Успешно загружено {result} тендера(-ов)"
        bot.send_message(message.chat.id, mes, parse_mode="HTML")
    else:
        mes = f"Что-то пошло не так: {States.get_inn(message.chat.id)}"
        bot.send_message(message.chat.id, mes, parse_mode="HTML")


# =================================== EXCEPTIONS CATCHER ====================================


@bot.message_handler(func=lambda message: message.text)
def echo(message):
    bot.send_message(message.chat.id, message.text, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
    # tenders = sql_requests.select_from_database('7826062821')
    # print(tenders)
    # for item in tenders:
    #     t = loader.classify_tender(item)
    #     sql_requests.insert_into_tendersapp_tender(t)
    # print('Success')
