import pandas as pd
from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
dataA = read_csv('loan.csv')

listo = ['revol_bal', 'revol_util', 'inq_last_6mths', 'delinq_2yrs', 'pub_rec',
         'purpose', 'int_rate', 'installment', 'dti', 'last_fico_range_high']
data = dataA[listo]
temp_list = ['mode', 'var', 'median']
indx_list = list(data.describe().index)
for i in temp_list:
    indx_list.append(i)

#task1
ind = data.isnull().sum()
print(ind)

#task2
def uniq(my_data):
    print('\nUnique data\n')
    print(my_data.unique())


#Построена функция для вывода индексов данных которые не приемлимы

def search_emmis(my_data):
    
    Q1 = my_data.quantile(0.25) 
    Q3 = my_data.quantile(0.75) 
    IQR = (Q3 - Q1)*1.5
    ind1 = np.where(my_data < Q1 - IQR)
    ind2 = np.where(my_data > Q3 + IQR)
    ind3 = np.where(my_data == 0)
    ind4 = np.where(my_data == None)
    index = np.concatenate((ind1, ind2, ind3, ind4), axis = 1)
    
    print('\nIndex where data need corrected\n')
    print(index)
    
# Данные которые неприемлимые: 1. которые больше или меньше квартильных эвристик, 2. данные равны нулю, 3. пустиы данные
    
# В первую очередь смотрю на уникальные значения и "формат" значений (нужно ли удол дополнительные символы и конверт в числовой тип)  

uniq(data['int_rate'])

# Данные имеют знак процента и явно не в числовот типе. Далее убираю знак процента и конверт в формат float

data['int_rate'] = data['int_rate'].replace('[\%]', '', regex = True)
data['int_rate']= data.int_rate.astype(float)

# Вызываю функцию, которая показывает индексы данных, которые требуют предобработки в таблице int_rate

search_emmis(data['int_rate'])    
  
# Функция, которая показывает индексы данных, которые требуют предобработки в таблице installment
  
uniq(data['installment'])    
search_emmis(data['installment']) 

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице ilast_fico_range_high

uniq(data['last_fico_range_high'])
search_emmis(data['last_fico_range_high'])

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице dti

uniq(data['dti'])
search_emmis(data['dti'])

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице revol_bal

uniq(data['revol_bal'])
search_emmis(data['revol_bal'])


uniq(data['revol_util'])
data['revol_util'] = data['revol_util'].replace('[\%]', '', regex = True)
data['revol_util']= data.revol_util.astype(float)

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице revol_util

search_emmis(data['revol_util'])

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице inq_last_6mths

uniq(data['inq_last_6mths'])
search_emmis(data['inq_last_6mths'])

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице delinq_2yrs

uniq(data['delinq_2yrs'])
search_emmis(data['delinq_2yrs'])

# Функция, которая показывает индексы данных, которые требуют предобработки в таблице pub_rec

uniq(data['pub_rec'])
search_emmis(data['pub_rec'])

#task3
# блок составления дата-фрейма с числовой статистикой
new_main = pd.DataFrame(index=indx_list)
for i in listo:
    if i == 'purpose':
        continue
    if i == 'revol_util' or i == 'int_rate':
        data[i] = data[i].replace('[\%]', '', regex=True) #обработка процентных данных
        data[i] = data[i].astype(float)
    fut = data[i]
    stat = fut.describe()
    extStat = {}
    extStat['mode'] = fut.mode()  #мода
    extStat['var'] = fut.var()   #дисперсия
    extStat['median'] = (fut.max() + fut.min())/2  #медиана
    stat = stat.append(pd.Series(extStat))         #объединённая статистика переводится в Фрейм и добавляется в общую таблицу
    stat = stat.to_frame().rename(columns={0: i})
    new_main = pd.concat([new_main, stat], axis=1)

# составление единого списка фич и обработка категориальных данных
data_purpose = data['purpose']
id_quantity = len(data)
purpose_list = np.delete(data.purpose.unique(), 14)
for i in purpose_list:    # составляется общий список индексов для категориальных и числовых признаков
    indx_list.append(i)
ind = pd.Series(indx_list)

new_data = pd.DataFrame(new_main, index=ind)

purpose_list_count = data['purpose'].value_counts()
columns = ['Quantity', 'Percent']
Stat = pd.DataFrame(index=ind, columns=columns)

for element in purpose_list:
    Stat.at[element, 'Quantity'] = purpose_list_count[element]
    Stat.at[element, 'Percent'] = (purpose_list_count[element]/id_quantity)*100

main_data = pd.concat([new_data, Stat], axis=1) # объединение числовой и категориальной статистики

#task4-5
main_data['Percent'].dropna().plot.pie(autopct='%i%%')
# Распределение данных категорий не является нормальным


installment_print = 0           # if val == 1 => enable print
int_rate_print = 0              # if val == 1 => enable print
dti_print = 0
last_fico_range_high_print = 0
revol_bal_print = 0
revol_util_print = 0
inq_last_6mths_print = 0
delinq_2yrs_print = 0
pub_rec_print = 0



data=pd.read_csv('loan.csv')

new_data = data[['purpose', 'int_rate', 'installment', 'dti', 'last_fico_range_high', 'revol_bal', 'revol_util', 'inq_last_6mths', 'delinq_2yrs', 'pub_rec']]
new_data.to_csv('new_data_loan.csv')

################################# Параметр № 1 : Цель кредита

# График к этому заданию "пришит" к файлу ovs.py

################################# Параметр № 2 : Ежемесячные взносы ($), причитающиеся заемщику, если кредит финансируется.
if installment_print == 1:
    #new_data.installment.plot.hist()
    new_data.installment.plot.kde()

################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному.
    #  Применимость этого вида распределения должна быть согласована с заказчиком!
    

################################# Параметр № 3 : Процентная ставка по кредиту 
if int_rate_print == 1:
    new_data['int_rate'] = new_data['int_rate'].replace('[\%]', '', regex = True)
    new_data['int_rate']= new_data.int_rate.astype(float)
    #new_data.int_rate.plot.hist()
    new_data.installment.plot.kde()


################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному.
    #  Применимость этого вида распределения должна быть согласована с заказчиком!


################################# Параметр № 4 : Отношение долга к доходу заемщика.
if dti_print == 1:
    #new_data.dti.plot.hist()
    new_data.dti.plot.kde()

################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения близкий к нормальному
    # Данные репрезентативны и готовы к анализу

################################# Параметр № 5 : Кредитная оценка FICO заемщика.
if last_fico_range_high_print == 1:
    #new_data.last_fico_range_high.plot.hist()
    new_data.last_fico_range_high.plot.kde()

################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения близкий к нормальному
    # 2) Можно ожидать, что на выборках большего размера распределение значений будет подобно нормальному (с небольшой ассимметрией)


################################# Параметр № 6 : Револьверный баланс заемщика.
if revol_bal_print == 1:
    #new_data.revol_bal.plot.hist()
    new_data.revol_bal.plot.kde()
    D = new_data.groupby(['revol_bal']).size()
    print (D)

################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному
    # 3) Экспоненциальный вид распределения является приемлемым, и корректно описывает нашу задачу


################################# Параметр № 7 : Показатель использования возобновляемой линии заемщика.

if revol_util_print == 1:
    new_data['revol_util'] = new_data['revol_util'].replace('[\%]', '', regex = True)
    new_data['revol_util']= new_data.int_rate.astype(float)
    #new_data.revol_util.plot.hist()
    new_data.revol_util.plot.kde()

################## Выводы по результатам анализа этого параметра:
    # Затрудняюсь сделать вывод о том, является ли распределение нормальным.
    # Либо распределение нормально, но выборка нерепрезентативная, либо распределение мультимодально


################################# Параметр № 8 : Количество запросов заемщика кредиторами за последние 6 месяцев.
if inq_last_6mths_print == 1:
    #new_data.inq_last_6mths.plot.hist()
    #new_data.inq_last_6mths.plot.kde()
    C = new_data.groupby(['inq_last_6mths']).size()
    print (C)
    plt.subplot(aspect=True)
    plt.pie(C, labels=C.index.values, autopct='%i%%')
    plt.title("The borrower’s number of inquiries by creditors in the last 6 months.")


################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному
    # 3) Для наглядности, кроме столбчатой диаграммы, приведена круговая
    # 4) Экспоненциальный вид распределения является приемлемым, и корректно описывает нашу задачу

    
################################# Параметр №9 : Количество случаев, когда заемщик просрочил 30+ дней после оплаты ( в течении последних 2 лет).
if delinq_2yrs_print == 1:
    #new_data.delinq_2yrs.plot.hist()
    #new_data.delinq_2yrs.plot.kde()
    B = new_data.groupby(['delinq_2yrs']).size()
    print (B)
    plt.subplot(aspect=True)
    plt.pie(B, labels=B.index.values, autopct='%i%%')
    plt.title("The number of times the borrower had been 30+ days past due on a payment in the past 2 years.")


################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному
    # 3) Для наглядности, кроме столбчатой диаграммы, приведена круговая
    # 4) Экспоненциальный вид распределения является приемлемым, и корректно описывает нашу задачу


################################# Параметр №10 : Количество негативных кредитных историй у заёмщиков
if pub_rec_print == 1:
    #new_data.pub_rec.plot.hist()
    #new_data.pub_rec.plot.kde()
    A = new_data.groupby(['pub_rec']).size()
    print (A)
    plt.subplot(aspect=True)
    plt.pie(A, labels=A.index.values, autopct='%i%%')
    plt.title("The borrower’s number of derogatory public records")


################## Выводы по результатам анализа этого параметра:
    # 1) Показатель имеет вид разпределения, отличный от нормального
    # 2) Вид распределения приближён к экспоненциальному
    # 3) Для наглядности, кроме столбчатой диаграммы, приведена круговая
    # 4) Экспоненциальный вид распределения является приемлемым, и корректно описывает нашу задачу
