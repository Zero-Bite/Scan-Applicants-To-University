import time
from typing import Any
import random
import pandas as pd
import requests
import config
import wget
import math
import os
from bs4 import BeautifulSoup

all_text = {
    'main': '',
    'kenhi': 'Программа двух дипломов НИУ ВШЭ и Университета Кёнхи "Экономика и политика Азии" (Зарубежное регионоведение)',
    'vostok': 'Востоковедение',
    'meshd': 'Международная программа «Международные отношения и глобальные исследования» (Международные отношения)',
    'polit': 'Политология'
}

LIST_OF_TEXT = ['main', 'kenhi', 'vostok', 'meshd', 'polit']

NAME_OF_FILE_MAIN = 'file_main.xlsx'
NAME_OF_FILE_KENHI = 'file_kenhi.xlsx'
NAME_OF_FILE_MESHD = 'file_meshd.xlsx'
NAME_OF_FILE_VOSTOK = 'file_vostok.xlsx'
NAME_OF_FILE_POLIT = 'file_polit.xlsx'

'''
Рандомизация User-Agent
'''
USER_AGENTS = [
    # Chrome (Windows/Mac/Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",

    # Firefox (Windows/Mac/Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/118.0",

    # Safari (Mac/iOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",

    # Edge (Windows/Mac)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",

    # Android Devices
    "Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",

    # iOS Devices
    "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone11,8; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone10,3; U; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",

    # Tablets
    "Mozilla/5.0 (Linux; Android 13; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-T860) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-T830) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-T720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-T510) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",

    # Legacy Browsers
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",

    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/80.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/80.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/80.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/80.0.0.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/80.0.0.0",

    # Mobile Browsers
    "Mozilla/5.0 (Linux; Android 13; SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A415F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A305F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-A205F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",

    # Smart TVs
    "Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 Chrome/92.0.4515.166 Safari/537.36",
    "Mozilla/5.0 (Linux; Tizen 5.5; SmartHub; SMART-TV; SMART-TV) AppleWebKit/538.1 (KHTML, like Gecko) Version/5.5 TV Safari/538.1",
    "Mozilla/5.0 (Linux; Android 11; Mi TV Stick) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Mi Box) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

'''
Запрос get
'''
def get_data(link: str) -> str:
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    data = requests.get(link, headers=headers)
    return data.text

'''
Cкачиваем файл
'''
def download_file(type_of_file: str, result_link: str) -> tuple[str, int] | None:
    # скачиваем файл
    print(f'SYSTEM INFO: FILE_TYPE: {type_of_file} ---> {result_link}')

    if type_of_file in LIST_OF_TEXT:
        if type_of_file == 'main':
            tmp_name = 'tmp_file_main.xlsx'

            wget.download(result_link, tmp_name)
            
            if os.path.exists(NAME_OF_FILE_MAIN):
                os.remove(NAME_OF_FILE_MAIN)

            os.rename(tmp_name, NAME_OF_FILE_MAIN)

            print(f'SYSTEM INFO: downloaded {type_of_file}')
        elif type_of_file == 'kenhi':
            tmp_name = 'tmp_file_kenhi.xlsx'

            wget.download(result_link, tmp_name)

            if os.path.exists(NAME_OF_FILE_KENHI):
                os.remove(NAME_OF_FILE_KENHI)

            os.rename(tmp_name, NAME_OF_FILE_KENHI)

            print(f'SYSTEM INFO: downloaded {type_of_file}')
        elif type_of_file == 'vostok':
            tmp_name = 'tmp_file_vostok.xlsx'

            wget.download(result_link, tmp_name)

            if os.path.exists(NAME_OF_FILE_VOSTOK):
                os.remove(NAME_OF_FILE_VOSTOK)

            os.rename(tmp_name, NAME_OF_FILE_VOSTOK)

            print(f'SYSTEM INFO: downloaded {type_of_file}')
        elif type_of_file == 'meshd':
            tmp_name = 'tmp_file_meshd.xlsx'

            wget.download(result_link, tmp_name)

            if os.path.exists(NAME_OF_FILE_MESHD):
                os.remove(NAME_OF_FILE_MESHD)

            os.rename(tmp_name, NAME_OF_FILE_MESHD)

            print(f'SYSTEM INFO: downloaded {type_of_file}')
        elif type_of_file == 'polit':
            tmp_name = 'tmp_file_polit.xlsx'

            wget.download(result_link, tmp_name)

            if os.path.exists(NAME_OF_FILE_POLIT):
                os.remove(NAME_OF_FILE_POLIT)

            os.rename(tmp_name, NAME_OF_FILE_POLIT)

            print(f'SYSTEM INFO: downloaded {type_of_file}')
        return None
    else:
        print('SYSTEM INFO: ошибочный ввод')
        return None

'''
Запрос ссылка по запросу
'''
def get_link(variator: str, response: str) -> None | str | list[str] | Any:
    global result_link
    if variator in LIST_OF_TEXT:
        soup = BeautifulSoup(response, 'lxml')

        if variator == 'main':
            main_link = soup.find('div', class_='with-indent')
            link_tag = main_link.find('a', href=True)
            result_link = link_tag["href"]

        elif variator == 'kenhi':
            all_tags = soup.find('tbody')
            all_tr = all_tags.find_all('td')
            index = -1

            for element in range(len(all_tr)):
                if all_tr[element].text == all_text['kenhi']:
                    index = element + 1

            result_link = all_tr[index].find('a', href=True)['href']

        elif variator == 'vostok':
            all_tags = soup.find('tbody')
            all_tr = all_tags.find_all('td')
            index = -1

            for element in range(len(all_tr)):
                if all_tr[element].text == all_text['vostok']:
                    index = element + 1

            result_link = all_tr[index].find('a', href=True)['href']

        elif variator == 'meshd':
            all_tags = soup.find('tbody')
            all_tr = all_tags.find_all('td')
            index = -1

            for element in range(len(all_tr)):
                if all_tr[element].text == all_text['meshd']:
                    index = element + 1

            result_link = all_tr[index].find('a', href=True)['href']

        elif variator == 'polit':
            all_tags = soup.find('tbody')
            all_tr = all_tags.find_all('td')
            index = -1

            for element in range(len(all_tr)):
                if all_tr[element].text == all_text['polit']:
                    index = element + 1

            result_link = all_tr[index].find('a', href=True)['href']

        return result_link
    else:
        print('SYSTEM INFO: ошибочный ввод')

def calculate_probability(statistica: dict) -> float:
    base_weights = {
        'Позиция в списках: ': 0.25,  # Меньший вес позиции
        'Всего поданных заявление: ': 0.08,
        'Выделено мест на платную обучение: ': 0.08,
        'Приоритет данной ОП: ': 0.12,  # Меньший разрыв между приоритетами
        'Максимальный балл ЕГЭ: ': 0.07,
        'Минимальный балл ЕГЭ :': 0.03,
    }

    # Мягкие коэффициенты штрафов
    penalty_weights = {
        # БВИ
        'Кол-во абитуриентов с правом поступления БВИ с таким же приоритетом или больше: ': -0.05,  # Меньший штраф
        'Кол-во абитуриентов с правом поступления БВИ с договором или согласием о зачислении и таким же приоритетом или больше: ': -0.08,

        # Преимущественное право
        'Кол-во абитуриентов с преимущественным правом 9/10 до тебя с таким же приоритетом или больше: ': -0.03,

        # Квоты
        'Кол-во абитуриентов в рамках отдельной квоты и особого до тебя с таким же приоритетом или больше: ': -0.04,

        # Согласия
        'Всего человек с согласием*, которые выше тебя в списке: ': -0.1,  # Меньшее влияние
        'Всего человек с согласием*, которые выше тебя в списке и таким же приоритетом или больше, и заключенным договором: ': -0.15,
    }

    # 1. Мягкий расчёт базового рейтинга
    base_score = 0.0

    # Позиция с плавным уменьшением важности
    if statistica['Всего поданных заявление: '] > 0:
        position_ratio = statistica['Позиция в списках: '] / statistica['Всего поданных заявление: ']
        base_score += (1 - position_ratio ** 0.7) * base_weights['Позиция в списках: ']  # Смягчаем зависимость

    # Приоритет с меньшим разрывом
    priority = min(10, max(1, statistica['Приоритет данной ОП: ']))  # Ограничиваем 1-10
    normalized_priority = 1.1 - priority / 10  # 1→1.0, 2→0.9, ..., 10→0.1
    base_score += normalized_priority * base_weights['Приоритет данной ОП: ']

    # Конкурс с логарифмическим смягчением
    if statistica['Выделено мест на платную обучение: '] > 0:
        competition = statistica['Всего поданных заявление: '] / statistica['Выделено мест на платную обучение: ']
        base_score += (1 / math.log(competition + 1, 2)) * base_weights['Выделено мест на платную обучение: ']

    # 2. Мягкие штрафы
    penalty_score = 0.0
    for key, weight in penalty_weights.items():
        penalty_score += math.tanh(statistica[key] / 5) * weight  # Используем tanh для смягчения

    # 3. Итоговая вероятность с плавным переходом
    total_score = base_score + penalty_score
    probability = 1 / (1 + math.exp(-10 * (total_score - 0.5)))  # Сигмоида для плавного перехода

    print(round(probability * 100, 2))

    return round(probability * 100, 2)

def get_statista_from_main(name_of_program='Программа двух дипломов НИУ ВШЭ и Университета Кёнхи "Экономика и политика Азии"',
                           name_of_way_of_study='41.03.01 Зарубежное регионоведение') -> tuple:
    file_path = NAME_OF_FILE_MAIN
    data_global = pd.read_excel(file_path)

    mask_name_of_program = data_global['Unnamed: 1'] == name_of_program
    mask_name_of_way_of_study = data_global['Unnamed: 5'] == name_of_way_of_study

    data_to_program_region = data_global[mask_name_of_program & mask_name_of_way_of_study]

    all_places = data_to_program_region['Unnamed: 15']
    amount_of_cv = data_to_program_region['Unnamed: 16']

    return int(amount_of_cv.to_list()[-1]), int(all_places.to_list()[-1])




def statistic_from_way_of_study(name_of_file,
                                name_of_program='Программа двух дипломов НИУ ВШЭ и Университета Кёнхи "Экономика и политика Азии"',
                                name_of_way_of_study='41.03.01 Зарубежное регионоведение') -> dict:

    statistica = {

        'Название ОП: ': 0,
        
        'Всего поданных заявление: ': 0,
        'Выделено мест на платную обучение: ': 0,
        'Уникальный идентификатор студента: ': 0,
        'Позиция в списках: ': 0,
        'Приоритет данной ОП: ': 0,
        'Максимальный балл ЕГЭ: ': 0,
        'Минимальный балл ЕГЭ :': 0,
        'Кол-во абитуриентов выше тебя с таким же приоритетом или больше: ': 0,

        'Всего человек с согласием*: ': 0,
        'Всего человек с согласием*, которые выше тебя в списке: ': 0,
        'Всего человек с согласием*, которые выше тебя в списке и таким же приоритетом или больше, и заключенным договором: ': 0,

        'Кол-во абитуриентов с правом поступления БВИ: ': 0,
        'Кол-во абитуриентов с правом поступления БВИ с таким же приоритетом или больше: ': 0,
        'Кол-во абитуриентов с правом поступления БВИ с договором или согласием о зачислении: ': 0,
        'Кол-во абитуриентов с правом поступления БВИ с договором или согласием о зачислении и таким же приоритетом или больше: ': 0,

        'Кол-во абитуриентов с преимущественным правом 9/10: ': 0,
        'Кол-во абитуриентов с преимущественным правом 9/10 до тебя: ': 0,
        'Кол-во абитуриентов с преимущественным правом 9/10 до тебя с таким же приоритетом или больше: ': 0,
        'Кол-во абитуриентов с преимущественным правом 9/10 до тебя с договором или согласием: ': 0,
        'Кол-во абитуриентов с преимущественным правом 9/10 до тебя с договором или согласием и с таким же приоритетом или больше: ': 0,


        'Кол-во абитуриентов в рамках отдельной квоты и особого права: ': 0,
        'Кол-во абитуриентов в рамках отдельной квоты и особого права до тебя: ': 0,
        'Кол-во абитуриентов в рамках отдельной квоты и особого до тебя с таким же приоритетом или больше: ': 0,
        'Кол-во абитуриентов в рамках отдельной квоты и особого до тебя с таким же приоритетом или больше и договором: ': 0,

        'Вероятность зачисления: ': 0
    }


    df = pd.read_excel(name_of_file)
    df.columns = df.iloc[13]
    df = df[14:]

    """
    Извлечение номера абитуриента
    """
    number_of_monitoring_student = 'УНИКАЛЬНЫЙ НОМЕР СТУДЕНТА ДЛЯ ВЫДАЧИ СТАТИСТИКИ' #  номер абитуриента
    object_of_info = df[df['Уникальный идентификатор'] == number_of_monitoring_student]
    prioritet_X = object_of_info['Приоритет платных мест'].to_list()[-1] #  приоритет абитуриента
    position = (object_of_info['№ п/п'].to_list())[-1] #  позиция абитуриента в списках


    """
    Заполнение первого блока с информацией 
    """
    if name_of_program in ['vostok', 'polit']:
        all_cv = posibillity_position = 'Нет информации'

        if name_of_program == 'vostok':
            all_cv = df['Уникальный идентификатор'].count()
            posibillity_position = 115
            statistica['Название ОП: '] = 'Востоковедение'
        elif name_of_program == 'polit':
            all_cv = df['Уникальный идентификатор'].count()
            posibillity_position = 50
            statistica['Название ОП: '] = 'Политология'
    else:
        all_cv, posibillity_position = get_statista_from_main(name_of_program, name_of_way_of_study) # информация про общее число мест и кол-во поданных заявлений
        statistica['Название ОП: '] = name_of_program
    max_score, min_score = max(df['Сумма конкурсных баллов']), min(df['Сумма конкурсных баллов'])


    statistica['Всего поданных заявление: '] = all_cv
    statistica['Выделено мест на платную обучение: '] = posibillity_position
    statistica['Уникальный идентификатор студента: '] = number_of_monitoring_student
    statistica['Позиция в списках: '] = position
    statistica['Приоритет данной ОП: '] = prioritet_X
    statistica['Максимальный балл ЕГЭ: '] = max_score
    statistica['Минимальный балл ЕГЭ :'] = min_score


    """
    Заполнение второго блока с информацией 
    """
    mask_of_dogovor_status = df['Заключен договор об образовании'] == 'Да'  # маска проверка на наличие договора
    mask_of_position = df['№ п/п'] < position
    mask_of_priority = df['Приоритет платных мест'] <= prioritet_X
    mask_of_agreement = df['Наличие согласия на зачисление'] == 'Да'     # маска проверка на наличие согласия

    total_with_dogovor = len(df[mask_of_dogovor_status])
    total_with_dogovor_and_earlier = len(df[mask_of_dogovor_status & mask_of_position])
    total_with_dogovor_and_earlier_and_prioritet = len(df[mask_of_dogovor_status &
                                                          mask_of_position &
                                                          mask_of_priority])

    total_with_agreement = len(df[mask_of_agreement])
    total_with_agreement_and_earlier = len(df[mask_of_agreement & mask_of_position])
    total_with_agreement_and_earlier_and_prioritet = len(df[mask_of_agreement &
                                                         mask_of_position &
                                                         mask_of_priority])


    total_with_agreement_and = len(df[(mask_of_agreement & mask_of_dogovor_status)])
    total_with_agreement_and_earlier_and = len(df[mask_of_agreement &
                                                  mask_of_dogovor_status &
                                                  mask_of_position])
    total_with_agreement_and_earlier_and_prioritet_and = len(df[mask_of_agreement &
                                                                mask_of_dogovor_status &
                                                                mask_of_position &
                                                                mask_of_priority])

    all_people_with_dogovor_or_agreeemnt = total_with_dogovor + total_with_agreement - total_with_agreement_and
    all_people_with_dogovor_or_agreeemnt_earlier = total_with_dogovor_and_earlier + total_with_agreement_and_earlier - total_with_agreement_and_earlier_and
    all_people_with_dogovor_or_agreeemnt_earlier_and_prioritet = total_with_dogovor_and_earlier_and_prioritet + total_with_agreement_and_earlier_and_prioritet - total_with_agreement_and_earlier_and_prioritet_and

    amount_higher_and_priotiry = len(df[mask_of_priority & mask_of_position])

    statistica['Кол-во абитуриентов выше тебя с таким же приоритетом или больше: '] = amount_higher_and_priotiry
    statistica['Всего человек с согласием*: '] = all_people_with_dogovor_or_agreeemnt
    statistica['Всего человек с согласием*, которые выше тебя в списке: '] = all_people_with_dogovor_or_agreeemnt_earlier
    statistica['Всего человек с согласием*, которые выше тебя в списке и таким же приоритетом или больше, и заключенным договором: '] = all_people_with_dogovor_or_agreeemnt_earlier_and_prioritet


    """
    Заполнение третий части
    """
    mask_of_bvi = df['Право поступления\nбез вступительных испытаний'] == 'Да'

    bvi_memebers = len(df[mask_of_bvi])  # всего человек БВИ
    bvi_members_priority = len(df[mask_of_bvi & mask_of_priority])  # всего человек БВИ до X
    bvi_with_agreement = len(df[mask_of_bvi & (mask_of_agreement | mask_of_dogovor_status)])  # всего человек БВИ до X c согласием
    bvi_with_agreement_with_payment_or_agreement = len(df[mask_of_bvi & mask_of_priority & (mask_of_agreement | mask_of_dogovor_status)])# всего человек БВИ до X c договором


    statistica['Кол-во абитуриентов с правом поступления БВИ: '] = bvi_memebers
    statistica['Кол-во абитуриентов с правом поступления БВИ с таким же приоритетом или больше: '] = bvi_members_priority
    statistica['Кол-во абитуриентов с правом поступления БВИ с договором или согласием о зачислении: '] = bvi_with_agreement
    statistica['Кол-во абитуриентов с правом поступления БВИ с договором или согласием о зачислении и таким же приоритетом или больше: '] = bvi_with_agreement_with_payment_or_agreement



    """
    Заполнение четвертой части части
    """
    mask_of_priority_way_9 = df['Преимущественное право п.9'] == 'Да'
    mask_of_priority_way_10 = df['Преимущественное право п.10'] == 'Да'

    members_with_compliment = len(df[mask_of_priority_way_9| mask_of_priority_way_10])
    members_with_compliment_earlier = len(df[(mask_of_priority_way_9 | mask_of_priority_way_10) &
                                             mask_of_position])
    members_with_compliment_earlier_with_prioritet = len(df[(mask_of_priority_way_9 | mask_of_priority_way_10) &
                                                            mask_of_position &
                                                            mask_of_priority])
    members_with_compliment_dogovor = len(df[(mask_of_priority_way_9 | mask_of_priority_way_10) & (mask_of_agreement | mask_of_dogovor_status) & mask_of_position])
    members_with_compliment_earlier_with_prioritet_and_dogovor = len(df[(mask_of_priority_way_9 | mask_of_priority_way_10) &
                                                                        mask_of_position &
                                                                        mask_of_priority &
                                                                        (mask_of_agreement | mask_of_dogovor_status)])

    statistica['Кол-во абитуриентов с преимущественным правом 9/10: '] = members_with_compliment
    statistica['Кол-во абитуриентов с преимущественным правом 9/10 до тебя: '] = members_with_compliment_earlier
    statistica['Кол-во абитуриентов с преимущественным правом 9/10 до тебя с таким же приоритетом или больше: '] = members_with_compliment_earlier_with_prioritet
    statistica['Кол-во абитуриентов с преимущественным правом 9/10 до тебя с договором или согласием: '] = members_with_compliment_dogovor
    statistica['Кол-во абитуриентов с преимущественным правом 9/10 до тебя с договором или согласием и с таким же приоритетом или больше: '] = members_with_compliment_earlier_with_prioritet_and_dogovor

    """
    Заполнение пятой части части
    """
    mask_of_osobay_kvota = df['Поступление на места в рамках квоты \nдля лиц, имеющих особое право'] == 'Да'
    mask_of_otdelnay_kvota = df['Поступление на места\nв рамках отдельной квоты'] == 'Да'

    members_otdel_with_compliment = len(df[mask_of_osobay_kvota | mask_of_otdelnay_kvota])
    members_otdel_with_compliment_earlier = len(df[(mask_of_osobay_kvota | mask_of_otdelnay_kvota) &
                                                mask_of_position])
    members_otdel_with_compliment_earlier_with_prioritet = len(df[(mask_of_osobay_kvota | mask_of_otdelnay_kvota) &
                                                                  mask_of_position &
                                                                  mask_of_priority])
    members_otdel_with_compliment_earlier_with_prioritet_and_dogovor = len(df[(mask_of_osobay_kvota | mask_of_otdelnay_kvota) &
                                                                                          mask_of_position &
                                                                                          mask_of_priority &
                                                                                          (mask_of_agreement | mask_of_dogovor_status)])

    statistica['Кол-во абитуриентов в рамках отдельной квоты и особого права: '] = members_otdel_with_compliment
    statistica['Кол-во абитуриентов в рамках отдельной квоты и особого права до тебя: '] = members_otdel_with_compliment_earlier
    statistica['Кол-во абитуриентов в рамках отдельной квоты и особого до тебя с таким же приоритетом или больше: '] = members_otdel_with_compliment_earlier_with_prioritet
    statistica['Кол-во абитуриентов в рамках отдельной квоты и особого до тебя с таким же приоритетом или больше и договором: '] = members_otdel_with_compliment_earlier_with_prioritet_and_dogovor


    statistica['Вероятность зачисления: '] = calculate_probability(statistica)

    return statistica


def send_info_to_bot(data: str) -> dict:

    global to_send
    print('start_programm')

    response = get_data(config.main_link_to_page) #HTML-каркас

    link_to_download = get_link(data, response)

    download_file(data, link_to_download)
    time.sleep(2)

    link_to_download = get_link('main', response)
    download_file('main', link_to_download)
    time.sleep(2)

    if data == 'kenhi':
        print('ok')

        name_of_program = 'Программа двух дипломов НИУ ВШЭ и Университета Кёнхи "Экономика и политика Азии"'
        name_of_way_of_study = '41.03.01 Зарубежное регионоведение'
        to_send = statistic_from_way_of_study(name_of_file=NAME_OF_FILE_KENHI,
                                          name_of_program=name_of_program,
                                          name_of_way_of_study=name_of_way_of_study)

    elif data == 'vostok':
        name_of_program = 'vostok'
        name_of_way_of_study = '-'
        to_send = statistic_from_way_of_study(name_of_file=NAME_OF_FILE_VOSTOK,
                                          name_of_program=name_of_program,
                                          name_of_way_of_study=name_of_way_of_study)
    elif data == 'meshd':
        name_of_program = 'Международная программа «Международные отношения и глобальные исследования»'
        name_of_way_of_study = '41.03.05 Международные отношения'
        to_send = statistic_from_way_of_study(name_of_file=NAME_OF_FILE_MESHD,
                                          name_of_program=name_of_program,
                                          name_of_way_of_study=name_of_way_of_study)
    elif data == 'polit':
        name_of_program = 'polit'
        name_of_way_of_study = '-'
        to_send = statistic_from_way_of_study(name_of_file=NAME_OF_FILE_POLIT,
                                          name_of_program=name_of_program,
                                          name_of_way_of_study=name_of_way_of_study)

    return to_send



