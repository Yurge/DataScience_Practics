import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

users = pd.read_csv('lesson_3/data/user_data.csv')
logs = pd.read_csv('lesson_3/data/logs.csv')

#print(users.shape)
#print(logs.platform.nunique())
#print(users)
#print(users.dtypes)
#print(users.isna().sum())
#print(users.describe())


# Найдем клиентов с наибольшим количеством успешных операций
client_success = logs \
    .groupby('client', as_index=False) \
    .agg({'success': 'sum'}) \
    .query('success == success.max()') \
    .client \
    .tolist()

answer_client_success = ', '.join(str(client) for client in client_success)

# С какой платформы было совершено наибольшее количество успешных операций?
platform_success = logs \
    .groupby('platform') \
    .agg({'success': 'sum'}) \
    .idxmax()


# Какую платформу предпочитают премиальные клиенты?
total_df = pd.merge(users, logs, how='inner', on='client')

platform_premium_users = total_df[total_df.premium == True].platform.value_counts().idxmax()

#print(total_df.head(11))
# График распределение возраста клиентов в зависимости от типа клиента (премиум или нет)
#sns.distplot(total_df[total_df.premium == False].age)
#sns.distplot(total_df[total_df.premium == True].age)
#plt.show()


# График распределения числа успешных операций к числу клиентов, совершивших такое количество успешных операций
success = logs \
    .groupby('client', as_index=False) \
    .agg({'success': 'sum'}) \
    .value_counts('success') \
    .reset_index() \
    .sort_values('success')

#sns.barplot(success, x='success', y='count')
#plt.show()


# Число успешных операций, сделанных на платформе computer, в зависимости от возраст. + График
count_success_by_age = total_df \
    .query('platform == "computer" and success') \
    .sort_values('age')

#plt.figure(figsize=(13, 5))
#sns.countplot(data=count_success_by_age, x='age')
#plt.show()