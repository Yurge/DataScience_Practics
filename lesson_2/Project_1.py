import pandas as pd

bookings = pd.read_csv('lesson_2/bookings.csv', sep=';')

# Приводим названия колонок к нижнему регистру и заменяем пробелы на знак нижнего подчеркивания
bookings = bookings.rename(str.lower, axis='columns')
bookings.columns = bookings.columns.str.replace(' ','_')


# Пользователи из каких стран совершили наибольшее число успешных бронирований? Укажем топ-5.
bookings_no_canceled = bookings \
    .query('is_canceled == 0') \
    .groupby(['country'], as_index=False) \
    .aggregate({'hotel': 'count'}) \
    .sort_values('hotel', ascending=False) \
    .rename(columns={'hotel': 'count_bookings'}) \
    [:5]


# На сколько ночей в среднем бронируют отели разных типов?
booking_count_nights = bookings \
    .groupby('hotel', as_index=False) \
    .aggregate({'stays_total_nights': 'mean'}) \
    .round(2)


# сколько раз тип номера, полученного клиентом, отличается от изначально забронированного?
overbooking = bookings.query('reserved_room_type != assigned_room_type').shape[0]


# В каком месяце 2017 года было максимальное число бронирований?
bookings_by_month = bookings \
    .query('arrival_date_year == 2017') \
    .value_counts('arrival_date_month') \
    .idxmax()


# Проверим, на какой месяц бронирования отеля типа City Hotel отменялись чаще всего в 2015, 2016, 2017?
city_hotel_is_canceled = bookings \
    .query('hotel == "City Hotel" and is_canceled == 1') \
    .groupby('arrival_date_year')['arrival_date_month'] \
    .value_counts()


# Три колонки: adults, children и babies. Какая из них имеет наибольшее среднее значение?
old = bookings.agg({'adults': 'mean',
                    'children': 'mean',
                    'babies': 'mean'}).idxmax()


# Создаём колонку total_kids, объединив столбцы children и babies
bookings['total_kids'] = bookings.children + bookings.babies


# Для отелей какого типа среднее значение переменной оказалось наибольшим?
mean_kids_by_hotel = bookings \
    .groupby('hotel') \
    .aggregate({'total_kids': 'mean'}) \
    .max().round(2)


# Проверим может ли отток клиентов быть связан с наличием детей?
# По итогу увидим, что процент отказов больше там, где нет детей.
churn_rate_with_kids = round(
    bookings.query('is_canceled == 1 and total_kids > 0').shape[0]
    / bookings.query('total_kids > 0').shape[0] * 100
    , 2)

churn_rate_without_kids = round(
    bookings.query('is_canceled == 1 and total_kids == 0').shape[0]
    / bookings.query('total_kids == 0').shape[0] * 100
    , 2)