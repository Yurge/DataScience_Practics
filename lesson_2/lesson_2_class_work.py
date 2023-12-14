import pandas as pd
from datetime import datetime

today_date = datetime.today().strftime('%d.%m.%Y')
# создаем заготовку имени файла если какой-то отчет требуют на постоянной основе
name_file = f'lesson_2/money_by_title_and_status_{today_date}.csv'

# считываем файл
df = pd.read_csv('lesson_2/lesson_1_data.csv',
                 encoding='windows-1251', sep=';', parse_dates=['Дата создания', 'Дата оплаты'])

# переименовываем колонки
df = df.rename(columns={'Номер': 'number',
                        'Дата создания': 'create_date',
                        'Дата оплаты': 'payment_date',
                        'Title': 'title',
                        'Статус': 'status',
                        'Заработано': 'money',
                        'Город': 'city',
                        'Платежная система': 'payment_sistem'})

# на всякий случай до начала форматирования данных сохраняем сумму денег как эталон
all_money = df.money.sum()

# создаем отчет: сколько денег принёс нам каждый курс с разделением по городам.
# группируем по названию курса,
# суммируем деньги по каждому курсу,
# сортируем от большего к меньшему
money_by_city = df \
    .groupby(['title', 'city'], as_index=False) \
    .aggregate({'money': 'sum'}) \
    .sort_values('money', ascending=False)

# проверяем сумму и записываем отчёт в файл
print(money_by_city.money.sum())
money_by_city.to_csv('lesson_2/money_by_city.csv', index=False)

# создаем отчет: сколько каждый курс принёс нам денег и сколько было Завершенных заказов.
money_by_title_and_status = df \
    .query("status == 'Завершен'") \
    .groupby('title', as_index=False) \
    .aggregate({'money': 'sum', 'number': 'count'}) \
    .sort_values('money', ascending=False) \
    .rename(columns={'number': 'число Завершенных заказов', 'money': 'сумма'})

# проверим не потерялись ли деньги в процессе форматирования таблицы и сохраняем таблицу в файл
if int(all_money) == int(money_by_title_and_status.сумма.sum()):
    print('OK')
    money_by_title_and_status.to_csv(name_file)
else:
    print('ERROR!!!!')