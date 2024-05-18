import datetime
import json
import re
from datetime import datetime, timedelta  # type: ignore
from urllib.parse import urlparse

import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6233614807:AAGPQw8Wb3e132S5G3eDNa0ZO8aMF4g6HHw")
check = False
datalist = []


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    if divider not in date:
        return False
    date_parts = date.split(divider)
    if len(date_parts) < 3:
        return False
    d, m, y = list(map(int, date_parts))
    today = list(map(int, datetime.today().date().strftime("20%y/%m/%d").split(sep="/")))  # type: ignore
    today = datetime(today[0], today[1], today[2])  # type: ignore
    try:
        date = datetime(2000 + y, m, d)  # type: ignore
    except ValueError:
        return False
    difference = date - today  # type: ignore
    if difference.days < 365 and date >= today:  # type: ignore
        return True
    else:
        return False


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        pass
    return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    return datetime.strptime(date, "%d.%m.%Y")  # type: ignore


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = "1omIyev8AiblOVOZpQGdV3rWC2zuKAy3OXdjLeSj4ams"  # Нужно извлечь id страницы из ссылки на Google-таблицу
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    global check
    check = True


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    client = gspread.service_account(filename="credentials.json")
    sh = client.open_by_key(sheet_id)
    list_object = sh.sheet1
    dataframe = pd.DataFrame(list_object.get_values(""), columns=list_object.row_values(1))  # преобразуем
    # Google-таблицу в таблицу pandas
    dataframe = dataframe.drop(0)
    dataframe.index -= 1
    return list_object, tables[max(tables)]["url"], dataframe


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        connect_table(message)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить")
        start_markup.row("Редактировать")
        start_markup.row("Удалить одно")
        start_markup.row("Удалить всё")
        information = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(information, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить дату")
        start_markup.row("Изменить дату")
        information = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(information, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        today = datetime.today()
        week = today + timedelta(days=7)
        list_object, list_url, dataframe = access_current_sheet()
        message_1 = f""
        for i in range(2, len(list_object.col_values(1)) + 1):
            for deadline in list_object.row_values(i)[2:]:
                if week >= convert_date(deadline) >= today:
                    message_1 += f"{list_object.cell(i, 1).value}: {deadline}\n"
        bot.send_message(message.chat.id, message_1)
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе 'Редактировать предметы'"""
    if message.text == "Добавить":
        message = bot.send_message(message.chat.id, "Напишите название и ссылку на предмет через пробел")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Редактировать":
        list_object, list_url, dataframe = access_current_sheet()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in dataframe.subject:
            markup.row(f"{element}")
        information = bot.send_message(message.chat.id, "Какой предмет редактируем?", reply_markup=markup)
        bot.register_next_step_handler(information, update_subject)
    elif message.text == "Удалить одно":
        list_object, list_url, dataframe = access_current_sheet()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in dataframe.subject:
            markup.row(f"{element}")
        information = bot.send_message(message.chat.id, "Какой предмет удаляем?", reply_markup=markup)
        bot.register_next_step_handler(information, delete_subject)
    elif message.text == "Удалить всё":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        start_markup.row("Не знаю")
        information = bot.send_message(message.chat.id, "Вы точно хотите удалить ВСЕ?", reply_markup=start_markup)
        bot.register_next_step_handler(information, choose_removal_option)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    global datalist
    datalist = []
    datalist.append(message.text)
    information = bot.send_message(message.chat.id, "Введите дату дедлайна")
    bot.register_next_step_handler(information, add_subject_deadline)


def add_subject_deadline(message):
    """Запрос даты дедлайна"""
    global datalist
    datalist.append(message.text)
    information = bot.send_message(message.chat.id, "Введите дедлайн: дата и разделитель (точка или слэш) через пробел")
    bot.register_next_step_handler(information, add_subject_deadline_2)


def add_subject_deadline_2(message):
    """Добавляем дедлайн в таблицу"""
    global datalist
    data, divider = message.text.split()
    if not is_valid_date(data, divider):
        information = bot.send_message(message.chat.id, "Неправильный формат даты или дедлайн уже прошел")
        bot.register_next_step_handler(information, add_subject_deadline_2)
    else:
        list_object, list_url, dataframe = access_current_sheet()
        row = list_object.find(f"{datalist[0]}").row
        length = len(list_object.row_values(row))
        list_object.update_cell(row, length + 1, message.text)
        if not list_object.cell(1, length + 1).value:
            number = int(list_object.cell(1, length).value)
            list_object.update_cell(1, length + 1, number + 1)
        bot.send_message(message.chat.id, "Изменено!")
        start(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе 'Редактировать дедлайн'"""
    if message.text == "Добавить дату":
        list_object, list_url, dataframe = access_current_sheet()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in dataframe.subject:
            markup.row(f"{element}")
        information = bot.send_message(message.chat.id, "Какому предмету добавляем?", reply_markup=markup)
        bot.register_next_step_handler(information, add_subject_deadline)
    elif message.text == "Изменить дату":
        list_object, list_url, dataframe = access_current_sheet()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in dataframe.subject:
            markup.row(f"{element}")
        information = bot.send_message(message.chat.id, "Для какого предмета изменяем?", reply_markup=markup)
        bot.register_next_step_handler(information, update_subject_deadline)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        start(message)
    elif message.text == "Не знаю":
        start(message)
        bot.send_message(message.chat.id, "Давайте примем решение")


def update_subject_deadline(message):
    """Обновляем дедлайн"""
    global datalist
    datalist = []
    datalist.append(message.text)
    list_object, list_url, dataframe = access_current_sheet()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for element in dataframe.columns[2:]:
        markup.row(f"{element}")
    information = bot.send_message(
        message.chat.id, "Для какой лабораторной работы Вы хотите изменить дедлайн?", reply_markup=markup
    )
    bot.register_next_step_handler(information, update_subject_deadline_2)


def update_subject_deadline_2(message):
    """Добавляем дедлайн для выбранной лабы"""
    global datalist
    datalist.append(message.text)
    information = bot.send_message(message.chat.id, "Введите дедлайн: дата и разделитель (точка или слэш) через пробел")
    bot.register_next_step_handler(information, update_subject_deadline_3)


def update_subject_deadline_3(message):
    """Изменяем или добавляем ранее введенный дедлайн"""
    global datalist
    data, divider = message.text.split()
    if not is_valid_date(data, divider):
        information = bot.send_message(message.chat.id, "Неправильный формат или дедлайн уже прошел")
        bot.register_next_step_handler(information, add_subject_deadline)
    else:
        list_object, list_url, dataframe = access_current_sheet()
        row = list_object.find(f"{datalist[0]}").row
        col = list_object.find(f"{datalist[1]}").col
        list_object.update_cell(row, col, message.text)
        bot.send_message(message.chat.id, "Изменено!")
        start(message)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        list_object, list_url, dataframe = access_current_sheet()
        list_object.append_row([name, url])
        bot.send_message(message.chat.id, "Добавлено")
        start(message)
    except IndexError:
        information = bot.send_message(
            message.chat.id, "Название предмета и ссылка должны быть в одном сообщении и разделены пробелом"
        )
        bot.register_next_step_handler(information, add_new_subject)


def update_subject(message):
    """Запрос пользователю на обновление информации о предмете в Google-таблице"""
    global datalist
    datalist = [message.text]
    information = bot.send_message(
        message.chat.id,
        "Введите новую информацию в формате '{название} {ссылка}'. Если что-то из этого не "
        "должно "
        "поменяться, то напишите его без изменений",
    )
    bot.register_next_step_handler(information, update_subject_2)


def update_subject_2(message):
    """Обновляем информацию о предмете"""
    global datalist
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        list_object, list_url, dataframe = access_current_sheet()
        index = dataframe.loc[dataframe.isin(datalist).any(axis=1)].index[0] + 2
        worksheet = list_object.range(f"A{index}:B{index}")
        worksheet[0].value = name
        worksheet[1].value = url
        list_object.update_cells(worksheet)
        bot.send_message(message.chat.id, "Изменено!")
    except IndexError:
        information = bot.send_message(
            message.chat.id, "Название и ссылка должны быть в одном сообщении и разделены пробелом"
        )
        bot.register_next_step_handler(information, update_subject_2)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    list_object, list_url, dataframe = access_current_sheet()
    index = dataframe.loc[dataframe.isin([message.text]).any(axis=1)].index[0] + 2
    list_object.delete_rows(int(index), int(index))
    bot.send_message(message.chat.id, "Удалено")
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    client = gspread.service_account(filename="credentials.json")
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    sheet.del_worksheet(worksheet)
    start(message)


def check_table():
    global check
    try:
        file = open("tables.json")
        check = True
    except FileNotFoundError:
        check = False


@bot.message_handler(commands=["start"])  # чтобы бот понимал к чему относится какая функция
def start(message):
    global check
    check_table()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not check:
        start_markup.row("Подключить Google-таблицу")
    else:
        list_object, list_url, dataframe = access_current_sheet()
        message_1 = f""
        for i in dataframe.index:
            message_1 += f"[{dataframe.loc[i, 'subject']}]({dataframe.loc[i, 'link']})\n"
        if message_1:
            bot.send_message(message.chat.id, message_1, parse_mode="MarkdownV2")
        else:
            bot.send_message(message.chat.id, "Таблица сейчас пустая", parse_mode="MarkdownV2")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайн")
    start_markup.row("Редактировать предметы")
    information = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(information, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
