#!/usr/bin/env python
# coding: utf-8


from pandas import read_csv, DataFrame, Series
data = read_csv('train.csv')
#import matplotlib.pyplot as plt
#%matplotlib qt
#%matplotlib inline
data['Fare'] = data['Fare'].fillna(data['Fare'].median())
data.pivot_table('Fare', ['PassengerId'], 'Pclass', 'mean').plot(title='Price')
data.pivot_table('PassengerId', ['SibSp'], 'Survived', 'count').plot(title='SibSp')
data.pivot_table('PassengerId', ['Parch'], 'Survived', 'count').plot(title='Parch')

print ("Заполненных значений о каютах:",data.PassengerId[data.Cabin.notnull()].count())
print("Кол-во записей о возрасте: ",data.PassengerId[data.Age.notnull()].count())
data['Age'] = data['Age'].fillna(data['Age'].median())
print("Без указанного порта:",len(data[data.Embarked.isnull()]))
MaxPassEmbarked = data.groupby('Embarked').count()['PassengerId']
data.Embarked[data.Embarked.isnull()] = MaxPassEmbarked[MaxPassEmbarked == MaxPassEmbarked.max()].index[0] 
print("Полей без цены билета:",len(data.PassengerId[data.Fare.isnull()]))
data = data.drop(['PassengerId','Name','Ticket','Cabin'],axis=1)
data

first_task = len(data[(data.Pclass == 1) & (data.Sex == 'male')])
print ("First class males count: ", first_task)

# Согласно определению, ребенком называется человек до окончания пубертатного периода. Средний возраст окончания пубертата - 19 лет
second_task = len(data[(data.Pclass == 1) & (data.Age <= 19)]) 
print ("Second class kids count: ", second_task) 

third_task = len(data[(data.SibSp == 0) & (data.Parch == 0)]) 
print ("Lonely people count: ", third_task) 

# Допустим, что "дорогой билет", это билет первого класса, цена которого не ниже цен билетов других классов (выше 73.5)
cheap_price = (data[data['Pclass'] != 1]['Fare'].max())
fourth_task = len(data[(data.Embarked == 'Q') & (data.Fare < cheap_price)])
print ('Rich people from Queenstown count: ',fourth_task)

fifth_task = data[data['Sex'] == "female"]['Age'].mean()
print ('Average women age: ', round(fifth_task, 2))

six_task = len(data[(data.SibSp == 0) & (data.Parch == 0) & (data.Age >= 50)])
print ('Lonely elderly count: ',six_task)

kids = data[data['Age'] < 18]
print ('Kids total: ', len(kids))
print ('First class kids: ', len(kids.loc[kids['Pclass'] == 1]))
print ('Second class kids: ', len(kids.loc[kids['Pclass'] == 2]))
print ('Third class kids: ', len(kids.loc[kids['Pclass'] == 3]))
print ('First class kids survived: ', len(kids[(kids.Survived == 1) & (kids.Pclass == 1)]))
print ('Second class kids survived: ', len(kids[(kids.Survived == 1) & (kids.Pclass == 2)]))
print ('Third class kids survived: ', len(kids[(kids.Survived == 1) & (kids.Pclass == 3)]))
print ('Kids with parents survived: ', len(kids[(kids.Survived == 1) & (kids.Parch >= 1)]))
print ('Kids with parents died: ', len(kids[(kids.Survived == 0) & (kids.Parch >= 1)]))
print ('Kids without parents survived: ', len(kids[(kids.Survived == 1) & (kids.Parch == 0)]))
print ('Kids without parents died: ', len(kids[(kids.Survived == 0) & (kids.Parch == 0)]))
print ('Swedish family kids: ', len(kids.loc[kids['Parch'] >= 3]), ' :D')

print ('Average Cherbourg ticket price: ', round(data[data['Embarked'] == 'C']['Fare'].mean(), 2))
print ('Average Queenstown ticket price: ', round(data[data['Embarked'] == 'Q']['Fare'].mean(), 2))
print ('Average Southampton ticket price: ', round(data[data['Embarked'] == 'S']['Fare'].mean(), 2))

print ('Average first class ticket price: ', round(data[data['Pclass'] == 1]['Fare'].mean(), 2))
print ('Average second class ticket price: ', round(data[data['Pclass'] == 2]['Fare'].mean(), 2))
print ('Average third class ticket price: ', round(data[data['Pclass'] == 3]['Fare'].mean(), 2))
