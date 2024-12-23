# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb

# import Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR

from sklearn.metrics import r2_score , mean_squared_error

import warnings
warnings.filterwarnings('ignore')

"""# Read Data"""

data = pd.read_csv("/content/car_price_prediction.csv")

"""# Explore data"""

data.head(3)

data.shape

data.info()

data.describe()

data.duplicated()

data.duplicated().sum()

data.drop_duplicates(inplace=True)

data.duplicated().sum()

data.shape

data.isnull()

data.isnull().sum()

data['Manufacturer'].unique()

for i in data.columns:
  print(i," : ",data[i].nunique())

pd.DataFrame(data.nunique())

data.hist(bins=15,figsize=(15,10))
plt.show()

top_10_cars = data['Manufacturer'].value_counts().sort_values(ascending=False)[:10]
top_10_cars

top_10_cars.plot(figsize=(10,5))
plt.show()

top10_mean_prices = [data[data['Manufacturer']==i]['Price'].mean() for i in list(top_10_cars.index)]
top10_mean_prices

plt.plot(top_10_cars.index,top10_mean_prices)
plt.show()

object_data = data.select_dtypes(include='object')

object_data.info()

for i in object_data.columns:
  plt.figure(figsize=(10,5))
  top10 = data[i].value_counts()[:3]
  top10.plot(kind='bar')
  plt.title(i)
  plt.show()

"""#  Data Processing"
"""

data = data.drop(['ID','Doors'],axis=1)

data.shape

"""# Date Column"""

import datetime

dtime = datetime.datetime.now()

data['Car_age'] = dtime.year - data['Prod. year']

data = data.drop('Prod. year',axis=1)

"""# Levy Column

"""

data.Levy.replace('-',0,inplace=True)

# data['Levy'] = data['Levy'].astype(int)

data.Levy.value_counts()

"""# Mileage column"""

data['Mileage'] = data['Mileage'].str.replace('km','')

"""# Engine volume Column"""

data['Engine volume'] = data['Engine volume'].str.replace('Turbo','')
data['Engine volume'] = data['Engine volume'].astype(float)

data.info()

"""# Detect Outliers"
"""

data_numeric = data.select_dtypes(exclude='object')

for col in data_numeric :
  q1 = data[col].quantile(0.25)
  q3 = data[col].quantile(0.75)
  iqr = q3 - q1
  lower_bound = q1 - (1.5 * iqr)
  upper_bound = q3 + (1.5 * iqr)
  outliers = ((data_numeric[col] < lower_bound) | (data_numeric[col] > upper_bound)).sum()
  total = data_numeric[col].shape[0]
  print(f"Total Outliers in {col} are : {outliers}-{round(100*(outliers)/total,2)} %")

  if outliers > 0:
    data = data.loc[(data[col] <= upper_bound) & (data[col] >= lower_bound)]

"""# Transform Data"""

dobject = data.select_dtypes(include='object')
dnumeric = data.select_dtypes(exclude='object')

le = LabelEncoder()

for i in dobject.columns:
  dobject[i] = le.fit_transform(dobject[i].astype(str))

data = pd.concat([dobject,dnumeric],axis=1)

data.info()

cor = data.corr()

sns.heatmap(cor)
plt.show()

"""# Model"""

X = data.drop('Price',axis=1)
y = data['Price']

x_train , x_test , y_train , y_test = train_test_split(X,y,test_size=0.2 , random_state=42)

algorithms = ['LinearRegression', 'DecisionTreeRegressor' , 'RandomForestRegressor' ,
              'GradientBoostingRegressor', 'XGBRegressor' , 'SVR']
Accuracy1 = []
Accuracy2 = []

def models(model):
  model.fit(x_train,y_train)
  y_pred = model.predict(x_test)
  accuracy1 = r2_score(y_test,y_pred)
  accuracy2 = np.sqrt(mean_squared_error(y_test, y_pred))
  Accuracy1.append(accuracy1)
  Accuracy2.append(accuracy2)
  score = model.score(x_test,y_test)
  print(f"The Score Model is : {score}")

model1 = LinearRegression()
model2 = DecisionTreeRegressor()
model3 = RandomForestRegressor()
model4 = GradientBoostingRegressor()
model5 = XGBRegressor()
model6 = SVR()

models(model1)
models(model2)
models(model3)
models(model4)
models(model5)
models(model6)

df = pd.DataFrame({'Algorithms':algorithms,"Accuracy1":Accuracy1,"Accuracy2":Accuracy2})
df

fig , ax  = plt.subplots(figsize=(20,5))
plt.plot(df.Algorithms,df.Accuracy1,c='red',marker='o')
plt.title('R2_Score')
plt.show()

fig , ax  = plt.subplots(figsize=(20,5))
plt.plot(df.Algorithms,df.Accuracy2,c='blue',marker='*')
plt.title('RMSE_SCore')
plt.show()

"""# Using My Model To Predict New Data"""

import pickle

file_name = "model.pkl"

pickle.dump(model2,open(file_name,'wb'))

file_name1 = "model1.sav"

pickle.dump(model2,open(file_name1,'wb'))

