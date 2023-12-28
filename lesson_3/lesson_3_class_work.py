import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sale = pd.read_csv('lesson_3/data/lesson_3_data__1_.csv',
                       encoding='windows-1251')

#  1. Из общего датасета требуется найти пользователей лояльных к определеному бренду

# Для выполнеия задачи нам требуется всего 2 колонки. Создадим новый датасет и переименуем колонки
users = sale[ ['tc', 'art_sp'] ]
users = users.rename(columns={'tc':'user_id', 'art_sp': 'brand_info'})

# Создадим новую колонку. Из названия товара оставляем только наим-е бренда
users['brand_name'] = users.brand_info.apply(lambda x: x.split(' ')[-1])

users_purchases = users \
    .groupby('user_id', as_index=False) \
    .agg({'brand_name': 'count'}) \
    .rename(columns={'brand_name': 'total_purchases'})

# Проведём первичный разведывательный анализ
users_purchases.describe()
# Мы видим, что 25% покупателей покупают 5 и более товаров. Чем меньше покупок совершил покупатель,
# тем больше вероятность ошибиться, назвав такого покупателя лояльным к бренду.
# Поэтому оставим только тех покупателей, которые вошли в 25% и покрутим на них нашу гепотезу о лояльности
users_purchases = users_purchases.query('total_purchases >= 5')
users_purchases.describe()

# посчитаем для каждого покупателя количество уникальных брендов, ведь если было много покупок и
# уникальный бренд = 1, то можно сказать, что покупатель лояльный к этому бренду
users_unique_brands = users \
    .groupby('user_id', as_index=False) \
    .agg({'brand_name': pd.Series.nunique}) \
    .rename(columns={'brand_name': 'unique_brands'})

#print(users_unique_brands)

# Теперь по каждому юзеру разобъем количество покупок по брендам
# и у каждого юзера отберем только строчку с максимальным числом покупок
lovely_brand_purchases_df = users \
    .groupby(['user_id', 'brand_name'], as_index=False) \
    .agg({'brand_info': 'count'}) \
    .sort_values(['user_id', 'brand_info'], ascending=[True, False]) \
    .groupby('user_id').head(1) \
    .rename(columns={'brand_name': 'lovely_brand', 'brand_info': 'lovely_brand_purchases'})

#print(lovely_brand_purchases_df[:15])

# Создадим финальную таблицу, объединив три предыдущих
loyalty_df = users_purchases \
    .merge(users_unique_brands, on='user_id') \
    .merge(lovely_brand_purchases_df, on='user_id')

# Отберем абсолютно лояльных покупателей
loyal_users = loyalty_df.query('unique_brands == 1')

# Нужно придумать метрику лояльности для отбора покупателей
# Давайте сначала добавим колонку коэфф-та лояльности каждого покупателя
loyalty_df['loyalty_score'] = loyalty_df.lovely_brand_purchases / loyalty_df.total_purchases

#ax1 = sns.displot(loyalty_df.loyalty_score)
#plt.show()

# На графике хорошо видно, что данные смещены в право. Вычислим медианное значение
loyalty_df.loyalty_score.median  # Медиана получилась 0.83

# Посмотрим медиану для каждого бренда
median_loyalty = loyalty_df \
    .groupby('lovely_brand') \
    .agg({'loyalty_score': 'median', 'user_id': 'count'})

# Визуализируем
#ax2 = sns.barplot(data=median_loyalty, x='lovely_brand', y='loyalty_score')
#plt.show()


### Можно сказать, что первые данные мы получили и заказчику уже можно предоставить информацию по лояльным клиентам,
# также можно обратить внимание заказчика на самый популярный бренд. В зависимости от поставленной задачи нужно дальше
# продолжать наш анализ данных.