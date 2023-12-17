import pandas as pd

taxi = pd.read_csv('lesson_2/2_taxi_nyc.csv')

new_columns = {'pcp 01': 'pcp_01', 'pcp 06': 'pcp_06', 'pcp 24': 'pcp_24'}
taxi = taxi.rename(columns = new_columns)

print(taxi.borough.unique())
print(taxi.columns)
print(taxi.shape)
#print(taxi.dtypes)
print(taxi.query("borough == 'Brooklyn'").shape[0])
print(taxi.borough.value_counts())

# находим сумму всех заказов, чтобы иметь эталон для сравнения
all_pickups = taxi.pickups.sum()

# переводим температуру из Фаренгейта в Цельсии
taxi.temp = (taxi.temp - 32) * 5 / 9

# сумма заказов по каждому району за всё время
sum_pickups_in_borough = taxi \
    .groupby('borough', dropna=False) \
    .aggregate({'pickups': 'sum'}) \
    .sort_values('pickups', ascending=False)

# найдем район с минимальным количеством заказов с помощью функции idxmin()
min_pickups = sum_pickups_in_borough.idxmin()

# среднее значение заказов по каждому району в рабочие и выходные дни
pickups_in_hday = taxi \
    .groupby(['borough', 'hday'], as_index=False, dropna=False) \
    .aggregate({'pickups': 'mean'}) \
    .sort_values('borough')

# для каждого района считаем число поездок по месяцам, сортируем по убыванию
pickups_by_mon_bor = taxi \
    .groupby(['pickup_month', 'borough'], as_index=False) \
    .aggregate({'pickups': 'sum'}) \
    .sort_values('pickups', ascending=False)