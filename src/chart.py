import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


raw_data = pd.read_csv("data.csv", sep="\t")
data = raw_data[['actualized_at', 'room_count']]
df = pd.DataFrame()


def month_year(actualized_at):
    to_datetime = dt.datetime.fromisoformat(actualized_at)
    formated = to_datetime.strftime("%m.%Y")
    return formated


df["Месяц"] = data["actualized_at"].apply(month_year)
df["Комнатность"] = data["room_count"]
df = df.groupby(['Месяц', 'Комнатность']).size().reset_index(name='Кол-во активных квартир')

df['Месяц'] = pd.to_datetime(df['Месяц'], format='%m.%Y')
df = df.sort_values(by="Месяц")

room_count_unique = sorted(df["Комнатность"].unique())
for i in room_count_unique:
    room_count_filtered = df[df["Комнатность"] == i]
    plt.plot(room_count_filtered['Месяц'], room_count_filtered['Кол-во активных квартир'], label=f'{i} комнат')

plt.xlabel('Месяц')
plt.ylabel('Количество активных квартир')
plt.title('Месячное количество активных квартир в разрезе комнатности')
plt.legend(title='Количество комнат')
plt.grid(True)
plt.show()
