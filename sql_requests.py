import os
from contextlib import closing
from datetime import datetime

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from psycopg2.extras import DictCursor
from config import DATABASE, USER, PASSWORD, HOST


def get_rate(money):
    try:
        money = float(money)
        if money >= 1000000000:
            value = f"{round(money / 1000000000, 2)} млрд."
        else:
            value = f"{round(money / 1000000, 2)} млн."
    except ValueError as e:
        print(e)
        value = "Данные отсутствуют"
    return value


# =============================== MAIN CUSTOMERS INNS ===============================

MAIN_CUSTOMERS_INNS = (
        # ========== МОСКВА ===============
        # "7722765428",  # ГБУ ГОРМОСТ - 426
        # "7728381587",  # ГКУ УДМС - 93
        # "7714125897",  # "ФКУ 'ЦЕНТРАВТОМАГИСТРАЛЬ'" - 128
        # "7704515009",  # ДЕПАРТАМЕНТ КОНКУРЕНТНОЙ ПОЛИТИКИ - 12
        # "5000001525",  # ГБУ МОСАВТОДОР - 84
        # "5031035549",  # "ФКУ УПРДОР МОСКВА - НИЖНИЙ НОВГОРОД" - 79
        "7717151380",  # ГК Автодор - 165
        "7701885820",  # АО "МОСИНЖПРОЕКТ" - 113
        "5024063954",  # ГУП МО "МОДЦ" - 43
        # 1143 projects

        # # ========== САНКТ-ПЕТЕРБУРГ и СЕВЕРО-ЗАПАД ===============
        # "7806215195",  # ГБУ МОСТОТРЕСТ - 49
        # "7830001853",  # КОМИТЕТ ПО РАЗВИТИЮ ТРАНСПОРТНОЙ ИНФРАСТРУКТУРЫ САНКТ-ПЕТЕРБУРГА - 2
        # "7826062821",  # "ФКУ УПРДОР 'СЕВЕРО-ЗАПАД'" - 40
        # "1001117010",  # "ФКУ УПРДОР 'КОЛА'" - 60
        # 151 projects
        #
        # # =============== ЦЕНТРАЛЬНАЯ РОССИЯ ===============
        # "6905005038",  # "ФКУ УПРДОР 'РОССИЯ'" - 100
        # "6725000810",  # "ФКУ УПРДОР МОСКВА-БОБРУЙСК" - 74
        # "5752000133",  # "ФКУ УПРДОР МОСКВА-ХАРЬКОВ" - 77
        # "3525065660",  # "ФКУ УПРДОР ""ХОЛМОГОРЫ""" - 113
        # "6832018699",  # "ФКУ УПРДОР МОСКВА - ВОЛГОГРАД" - 64
        # 428 projects
        #
        # # ============== ТАТАРСТАН и УРАЛ ===================
        # "1660049283",  # Главтатдолртранс - 112
        # "1660061210",  # "ФКУ 'ВОЛГО-ВЯТСКУПРАВТОДОР'" - 189
        # "2126000323",  # "ФКУ УПРДОР 'ПРИКАМЬЕ'" - 32
        # "7451189048",  # "ФКУ УПРДОР 'ЮЖНЫЙ УРАЛ'" - 121
        # "0278007048",  # "ФКУ УПРДОР 'ПРИУРАЛЬЕ'" - 61
        # "7223007316",  # "ФКУ 'УРАЛУПРАВТОДОР'" - 130
        # 645 projects
        #
        # # ============== ЮГ РОССИИ ===================
        # "5836010699",  # "ФКУ ""ПОВОЛЖУПРАВТОДОР""" - 177
        # "6450108421",  # "ФКУ УПРДОР ""НИЖНЕ-ВОЛЖСКОЕ""" - 0
        # "6147014910",  # "ФКУ УПРДОР 'АЗОВ'" - 23
        # "2309033598",  # "ФКУ УПРДОР 'КАСПИЙ'" - 97
        # "4909083435",  # "ФКУ УПРДОР 'ТАМАНЬ'" - 8
        # "2320100329",  # "ФКУ УПРДОР 'ЧЕРНОМОРЬЕ'" - 79
        # "2632041647",  # "ФКУ УПРДОР 'КАВКАЗ'" - 107
        # 491 projects
        #
        # # ============== СИБИРЬ И ДАЛЬНИЙ ВОСТОК ===================
        # "1435193127",  # "ФКУ УПРДОР 'ВИЛЮЙ'" - 100
        # "0326012322",  # "ФКУ УПРДОР 'ЮЖНЫЙ БАЙКАЛ'" - 50
        # "2721144517",  # "ФКУ 'ДАЛЬУПРАВТОДОР'" - 34
        # "2460028834",  # "ФКУ УПРДОР 'ЕНИСЕЙ'" - 96
        # "5405201071",  # "ФКУ 'СИБУПРАВТОДОР'" - 56
        # "1402008636",  # "ФКУ УПРДОР 'ЛЕНА'" - 61
        # "3800000140",  # "ФКУ УПРДОР 'ПРИБАЙКАЛЬЕ'" - 77
        # "7536053744",  # "ФКУ УПРДОР 'ЗАБАЙКАЛЬЕ'" - 93
        # "2725022365",  # "ФКУ ДСД ""ДАЛЬНИЙ ВОСТОК""" - 93
        # "2225061905",  # "ФКУ УПРДОР ""АЛТАЙ""" - 76
        # 736 projects
        # 3594 projects totally
)

# =============================== INSERT INTO DATABASE ===============================


def insert_into_tendersapp_tender(data):
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                insert into tendersapp_tender 
                (id,
                name,
                start_price,
                final_price,
                created,
                updated,
                status,
                customer_inn,
                category,
                type)
                values ('{
                data['pk']}', 
                '{data['fields']['name']}', 
                '{data['fields']['start_price']}',
                '{data['fields']['final_price']}',
                '{data['fields']['created']}',
                '{data['fields']['updated']}',
                '{data['fields']['status']}',
                '{data['fields']['customer_inn']}',
                '{data['fields']['category']}',
                '{data['fields']['type']}')
                on conflict (id) do update set 
                    updated = excluded.updated, 
                    status = excluded.status, 
                    name = excluded.name;
                """
            )
        conn.commit()


def insert_into_tendersapp_plan(data):
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                insert into tendersapp_plan 
                (id,
                name,
                start_price,
                created,
                updated,
                customer_inn,
                year)
                values ('{
                data['pk']}', 
                '{data['fields']['name']}', 
                '{data['fields']['start_price']}',
                '{data['fields']['created']}',
                '{data['fields']['updated']}',
                '{data['fields']['customer_inn']}',
                '{data['fields']['year']}') 
                on conflict(id) do update set 
                start_price = EXCLUDED.start_price,
                name = EXCLUDED.name,
                updated = EXCLUDED.updated,
                year = EXCLUDED.year;
                """
            )
        conn.commit()


def insert_into_projectsapp_customer(data):
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                insert into projectsapp_customer 
                (id,
                title,
                fullname,
                management,
                name,
                inn,
                kpp,
                okved,
                form_code,
                form_title,
                address,
                district_id)
                values ('{
                data['pk']}', 
                '{data['fields']['title']}', 
                '{data['fields']['fullname']}',
                '{data['fields']['management']}',
                '{data['fields']['name']}',
                '{data['fields']['inn']}',
                '{data['fields']['kpp']}',
                '{data['fields']['okved']}',
                '{data['fields']['form_code']}',
                '{data['fields']['form_title']}',
                '{data['fields']['address']}',
                '{data['fields']['district_id']}') 
                on conflict(id) do nothing;
                """
            )
        conn.commit()


def insert_into_projectsapp_project(data):
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                insert into projectsapp_project 
                (id,
                name,
                image,
                status,
                creation_date,
                is_active,
                category,
                customer_id,
                region_id)
                values (
                '{data['pk']}', 
                '{data['name']}',
                'projects_images/avatars/default_bridge.png',
                'завершен',
                '{data['creation_date']}',
                'false',
                '{data['category']}',
                '{data['customer_id']}',
                '{data['region_id']}') 
                on conflict(id) do nothing;
                """
            )
        conn.commit()


# =============================== UPDATE DATABASE ===============================


def customer_tenders_updated(customer_inn):
    dtt = str(datetime.now())
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                update projectsapp_customer set tenders_updated = '{dtt}'
                where inn = '{customer_inn}'
                """
            )
            conn.commit()


def customer_plans_updated(customer_inn):
    dtt = str(datetime.now())
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                update projectsapp_customer set plans_updated = '{dtt}'
                where inn = '{customer_inn}'
                """
            )
            conn.commit()


# =============================== SELECT FROM DATABASE ===============================

def get_company_title(customer_inn):
    report = {}
    try:
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    select title
                    from projectsapp_customer
                    where inn = '{customer_inn}'
                    """
                )
                for i in cursor:
                    report['title'] = i['title']
        return report
    except KeyError as e:
        print(e)
        return False


def report_2019(customer_inn):
    report = []
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                select sum(start_price),
                    'ВСЕГО'::text as types
                    from tendersapp_tender
                    where customer_inn = '{customer_inn}'
                    and created between '2019-01-01' and '2020-01-01'
                union
                select sum(start_price),
                    'НА ИССО'::text as types
                    from tendersapp_tender
                    where to_tsvector('russian', name)
                    @@ to_tsquery('russian', '(мост | путепровод | эстакада | тоннель)')
                    and customer_inn = '{customer_inn}'
                    and (created between '2019-01-01' and '2020-01-01')
                """
            )
            for i in cursor:
                report.append({
                    "types": i["types"],
                    "count": i["sum"]
                })
    types = [i['types'] for i in report if i['types'] is not None]
    count = [int(i['count']) for i in report if i['count'] is not None]
    if len(count):
        pd.DataFrame(count, types, columns=['Сумма, руб.']).plot(kind='bar', color='red', rot=0)
        plt.title('Объявленные торги в 2019г. \n'
                  'Общие расходы и расходы на содержание\n'
                  'искусственных сооружений')
        report_2019_path = os.path.join('media', f'report_2019_{customer_inn}.png')
        plt.savefig(report_2019_path)
        plt.close()
        return report_2019_path
    else:
        return False


def plans_report(customer_inn):
    report = {}
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                select sum(start_price)
                from tendersapp_plan
                where customer_inn = '{customer_inn}'
                """
            )
            for i in cursor:
                report['plans_2020'] = f'{i["sum"]}'
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                select sum(start_price)
                from tendersapp_plan
                where to_tsvector('russian', name) @@ to_tsquery('russian', '(мост | путепровод | эстакада | тоннель)') 
                and customer_inn = '{customer_inn}'
                """
            )
            for i in cursor:
                report['plans_isso_2020'] = f'{i["sum"]}'
    print(report)
    if report['plans_2020'] != 'None':
        plans_2020 = get_rate(report['plans_2020'])
        plans_isso_2020 = get_rate(report['plans_isso_2020'])
        return f"<b>План - график 2020 - 2022 гг:</b>\n" \
               f"Планируются закупки на сумму: {plans_2020}\n" \
               f"... в том числе на ИССО: {plans_isso_2020}\n" \
               f"\n" \
               f"<b>Планируемые проекты: </b>\n" \
               f"/future_projects\n"
    else:
        return False


def future_projects(customer_inn):
    projects = []
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                select *
                from tendersapp_plan
                where customer_inn = '{customer_inn}' 
                    and to_tsvector('russian', name) @@ 
                    to_tsquery('russian', '(мост | путепровод | эстакада | тоннель)')
                """
            )
            for i in cursor:
                projects.append(i['name'])
    return projects


def regions_details(region_id):
    report = {}
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                select 
                count(p.id) as count,
                r.id,
                r.name,
                r.population,
                r.area,
                count(p.id) / area * 1000 as per_area,
                count(p.id) * 1000000 / population as per_popul
                    from projectsapp_project as p
                    join projectsapp_region as r
                on p.region_id = r.id
                where r.id = '{region_id}'
                group by r.id
                limit 1;
                """
            )
            for i in cursor:
                report['Название'] = i['name'],
                report['Количество сооружений'] = i['count'],
                report['Население'] = i['population'],
                report['Площадь региона'] = i['area'],
                report['Плотность сооружений на 1000 кв.км.'] = i['per_area'],
                report['Количество мостов на 1 млн жителей'] = i['per_popul']
    print(report)
    return '\n'.join(f"<b>{i}:</b> <i>{j[0] if isinstance(j, tuple) else j}</i>" for i, j in report.items())


def regions_list():
    regions = []
    with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                select count(p.id) as count, r.id, r.name
                from projectsapp_project as p
                join projectsapp_region as r
                on p.region_id = r.id
                group by r.id
                order by count desc
                limit 30
                """
            )
            for i in cursor:
                region_id = i['id'] if i['id'] >= 10 else f"0{i['id']}"
                regions.append(
                    f"{i['name']}\n"
                    f"Подробная информация: <i>/region{region_id}</i>"
                )
    return regions


# =============================== CUSTOMERS INFO ===============================

class Customers:
    """ Класс работы со списком Заказчиков """

    def __init__(self, inns: tuple = None):
        if inns:
            self.inns = inns
        else:
            self.inns = MAIN_CUSTOMERS_INNS

    def __str__(self):
        return list(self.inns)

    def render_to_message(self):
        """ Возвращает строку html со списокм заказчиков для вывода в сообщении бота """
        customers = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                         SELECT 
                            title,
                            inn
                         FROM projectsapp_customer
                         WHERE inn = ANY(ARRAY[{list(self.inns)}]);
                        """
                )
                for i in cursor:
                    customers.append(

                        f"{i['title']}\n"
                        f"ИНН: <i>/{i['inn']}</i>\n"
                    )
        return " ".join(customers)

    def not_updated_customers(self):
        """ Возвращает список заказчиков готовых к обновлению """
        customers = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                        SELECT count(*) AS count,
                        c.fullname,
                        c.inn,
                        c.tenders_updated,
                        plans_updated
    
                        FROM projectsapp_project p
                        FULL OUTER JOIN projectsapp_customer c ON p.customer_id = c.id 
                        where c.tenders_updated < current_timestamp - interval '24 hour' 
                        and c.inn = ANY(ARRAY[{list(self.inns)}])
                        GROUP BY c.id
                        ORDER BY (count(*)) DESC;
                    """
                )
                for i in cursor:
                    customers.append(i['inn'])
        return customers

    @staticmethod
    def get_latest_date_by_customer(customer_inn):
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    select updated
                    from tendersapp_tender
                    where customer_inn = '{customer_inn}'
                    order by updated desc
                    limit 1
                    """
                )
                return cursor.fetchone()[0]

    @staticmethod
    def get_projects_list(customer_inn):
        """ Возвращает список id тендеров по строительству и ремонту ИССО """
        projects = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    select *
                    from tendersapp_tender
                    where customer_inn = '{customer_inn}' 
                        and type = 'Искусственное сооружение' 
                        and (category = 'Строительство' or category = 'Капитальный ремонт')
                    """
                )
                for i in cursor:
                    projects.append(i['id'])
        return projects

    @staticmethod
    def get_all_tenders(customer_inn):
        """ Возвращает список всех тендеров """
        tenders = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    select * from tendersapp_tender
                    where customer_inn = '{customer_inn}'
                    """
                )
                data = cursor.fetchall()
                for d in data:
                    tenders.append(
                        {
                            'pk': d[0],
                            'fields': {
                                'name': d[1],
                                'start_price': d[2],
                                'final_price': d[3],
                                'created': d[4],
                                'updated': d[5],
                                'status': d[6],
                                'customer_inn': d[7],
                                'category': d[8],
                                'type': d[9],
                                'last_checked': d[10]
                            }
                        }
                    )
            return tenders

    @staticmethod
    def customer_details(customer_inn):
        report = {}
        try:
            with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(
                        f"""
                        select title, name, fullname, form_title, address, inn, kpp, management
                        from projectsapp_customer
                        where inn = '{customer_inn}'
                        """
                    )
                    for i in cursor:
                        report['title'] = i['title']
                        report['name'] = i['name']
                        report['form_title'] = i['form_title']
                        report['fullname'] = i['fullname']
                        report['address'] = i['address']
                        report['inn'] = i['inn']
                        report['kpp'] = i['kpp']
                        report['management'] = i['management']
            return f"<b>Название организации: </b>\n" \
                   f"{report['fullname']}\n" \
                   f"\n" \
                   f"<b>ИНН / КПП:</b>\n" \
                   f"{report['inn']} / {report['kpp']}\n" \
                   f"\n" \
                   f"<b>Адрес: </b>\n" \
                   f"{report['address']}\n" \
                   f" \n" \
                   f"<b>Форма организации:</b>\n" \
                   f"{report['form_title']}\n" \
                   f"\n" \
                   f"<b>{report['management'].title()}:</b>\n" \
                   f"{report['name']}"
        except KeyError as e:
            print(e)
            return False

    @staticmethod
    def type_report(customer_inn):
        types = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    SELECT count(p.id),
                        'МОСТЫ'::text as types
                       FROM projectsapp_project as p
                       JOIN projectsapp_customer as c
                        ON p.customer_id = c.id
                      WHERE c.inn::text = '{customer_inn}' and
                      (to_tsvector('russian', p.name) @@ to_tsquery('russian', 'мост'))

                    UNION

                    SELECT count(p.id),
                        'ПУТЕПРОВОДЫ'::text as types
                       FROM projectsapp_project as p
                       JOIN projectsapp_customer as c
                        ON p.customer_id = c.id
                      WHERE c.inn::text = '{customer_inn}' and
                      (to_tsvector('russian', p.name) @@ to_tsquery('russian', 'путепровод'))

                    UNION

                    SELECT count(p.id),
                        'ЭСТАКАДЫ'::text as types
                       FROM projectsapp_project as p
                       JOIN projectsapp_customer as c
                        ON p.customer_id = c.id
                      WHERE c.inn::text = '{customer_inn}' and
                      (to_tsvector('russian', p.name) @@ to_tsquery('russian', 'эстакада'))

                    UNION

                    SELECT count(p.id),
                        'ТОННЕЛИ'::text as types
                       FROM projectsapp_project as p
                       JOIN projectsapp_customer as c
                        ON p.customer_id = c.id
                      WHERE c.inn::text = '{customer_inn}' and
                      (to_tsvector('russian', p.name) @@ to_tsquery('russian', 'тоннель'));
                    """
                )
                for i in cursor:
                    types.append({
                        "types": i["types"],
                        "count": i["count"]
                    })
        types = pd.DataFrame(types)
        plt.bar(types['types'], types['count'], width=0.8)
        plt.title('Количество сооружений по типам, шт.')
        types_hist_path = os.path.join('media', f'types_{customer_inn}.png')
        plt.savefig(types_hist_path)
        plt.close()
        return types_hist_path

    @staticmethod
    def category_report(customer_inn):
        bridges = {
            'КАТЕГОРИЯ 1': 0,
            'КАТЕГОРИЯ 2': 0,
            'КАТЕГОРИЯ 3': 0,
            'КАТЕГОРИЯ 4': 0
        }
        customers = []
        with closing(psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                    select count(p.id) as count, p.category
                    from projectsapp_project as p
                    join projectsapp_customer as c
                    on p.customer_id = c.id
                    where c.inn = '{customer_inn}'
                    group by p.category
                    """
                )
                for i in cursor:
                    bridges[f'КАТЕГОРИЯ {i["category"]}'] = f'{i["count"]}'
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"""
                     SELECT count(*) AS count,
                        c.title,
                        c.fullname,
                        c.inn
                       FROM projectsapp_project p
                         JOIN projectsapp_customer c ON p.customer_id = c.id
                      GROUP BY c.id
                      ORDER BY (count(*)) DESC
                     LIMIT 5;
                    """
                )
                for i in cursor:
                    customers.append({
                        "name": i['title'],
                        "fullname": i['fullname'],
                        "inn": i['inn'],
                        "count": int(i["count"])
                    })
        categories = [i for i in bridges.keys()]
        values = [int(i) for i in bridges.values()]
        if sum(values):
            pd.DataFrame(values, categories, columns=['Количество']).plot(kind='bar', color='magenta', rot=0, width=0.8)
            plt.title('Количество сооружений по категориям, шт.')
            category_hist_path = os.path.join('media', f'category_{customer_inn}.png')
            plt.savefig(category_hist_path)
            plt.close()
            return category_hist_path
        else:
            return False
