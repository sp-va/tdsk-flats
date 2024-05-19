import pandas as pd
import re
import datetime as dt

raw_data = pd.read_csv("data.csv", sep="\t")
data = raw_data[['description', 'actualized_at']]
df = pd.DataFrame()


def address_from_description(descr):
    pat_prefix = r'\d-комнатная квартира на\s*'
    pat_postfix = r'\s*\d*\s*подъезд'
    address = re.sub(pat_prefix, '', descr)
    address = re.sub(pat_postfix, '', address)
    return address


def timestamp_to_date(actualized_at):
    to_datetime = dt.datetime.fromisoformat(actualized_at)
    formated = to_datetime.strftime("%d.%m.%Y")
    return formated


df["Корпус"] = data["description"].apply(address_from_description) # Получаем чистый адрес
df["Дата"] = data["actualized_at"].apply(timestamp_to_date) # Получаем дату из дата-время
df = df.groupby(['Дата', 'Корпус']).size().reset_index(name='Кол-во активных квартир') # Группируем данные и получаем суммы значений по парам дата-адрес
df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y') # До этого момента дата была str, из-за чего сортировка работала бы соответствующе
df = df.sort_values(by="Дата") # Сортируем по возрастанию даты
df['Дата'] = df['Дата'].dt.strftime('%d.%m.%Y') # Форматируем обратно
df.to_excel("result.xlsx", index=False) # Пишем dataframe в таблицу excel

