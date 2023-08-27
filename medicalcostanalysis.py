# -*- coding: utf-8 -*-
"""MedicalCostAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xnZD-5GpmB7tPeJbyHaXU9tYDRB81vVb

**MEDICAL COST ANALYSIS**
"""

#Gerekli olabilecek tüm kütüphaneleri import ettim.

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

# CSV dosyasını pd ile yükledim ve orijinal datayı bozmamak için copy'sini aldım.

data= pd.read_csv('insurance.csv')
df = data.copy()
df

df.isna().sum()

#Tüm dataların non-null olduğunu kontrol ettim.
df.info()

#Analiz edeceğim "charges" verisinin tipini float'tan categorical'a dönüştürdüm.
df['charges'] = df['charges'].astype("category")

df.info()

# "charges" data tipi categorical olduğu için mean value alınamıyor.
df["charges"].mean()

#BMI dağılımı

df.value_counts("bmi")

#Enhanced box plot grafiğiyle BMI dağılımını ve outlierları görünür kıldım.
sns.boxenplot(x = "bmi", data= df)

sns.displot(df, x= "bmi")

#Smoker-Charges ilişkisi

plt.plot(df.smoker, df.charges,'o',markersize=3, color='green')
plt.xlabel('Smoker')
plt.ylabel('Charges')

#Age-BMI İlişkisi

plt.figure(figsize=(10,7))
plt.title('Age vs BMI')
sns.barplot(x='age',y='bmi',data=df,palette='husl')
plt.savefig('/content/sample_data/AgevsBMI')

#BMI - Sex İlişkisi
sns.catplot(data=df.sort_values("sex"),
    x="sex", y="bmi", kind="boxen",)

#Region-Smoker İlişkisi
sns.catplot(x="smoker", kind="count",hue = 'region', palette="RdPu", data=data)

#Children-BMI İlişkisi
sns.catplot(data=df.sort_values("children"),
    x="children", y="bmi", kind="boxen",)

#BMI-Charges İlişkisi
plt.scatter(df['bmi'], df['charges'])
plt.show()

#Region-Smoker-BMI İlişkisi
sns.catplot(data=df, x="bmi", y="smoker", hue="region", kind="bar")

#sum() ile her region'daki çocuk sayısı toplamını bularak en çok çocuk sayısı olan region'u (southeast) buldum.

df.groupby("region")["children"].sum()

sns.catplot(x="region", kind="count",hue = 'children', palette="pink", data=df)

#BMI'daki outlierlar
sns.boxplot(x = "bmi", data= df)

# Sex kategorisindeki değerler
unique_values = df['sex'].unique()

print(unique_values)

#Region kategorisindeki değerler
unique_values = df['region'].unique()

print(unique_values)

#One-Hot Encoding tekniği ile Region'ları ayırarak sayısal veriye dönüştürdüm.

df = pd.get_dummies(df, columns=['region'])

df.head()

#Label Encoding tekniğiyle kadın-erkek sayısal olarak temsil edildi.

clean_data = {'sex': {'male' : 0 , 'female' : 1} ,
                 'smoker': {'no': 0 , 'yes' : 1},

               }
df_copy = df.copy()
df_copy.replace(clean_data, inplace=True)
df_copy

df_copy.isna().sum()

#Charges verisini ayırıp y'ye atadım.
y = df_copy.charges
X = df_copy.drop(["charges"] , axis =1)
X

y

#Dataseti train_test_split ile ayırdım.

from sklearn.model_selection import train_test_split

X_train, X_test, y_train , y_test = train_test_split(X,y , test_size= 0.2, random_state= 0)

# Sklearn ile veri Normalizasyonu - Min Max Scaling

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# tek adımda fit ve transform
normalized = scaler.fit_transform(df_copy)

inverse = scaler.inverse_transform(normalized)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.metrics import mean_squared_error ,r2_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import absolute
from numpy import sqrt

"""# **Random Forest Regression**"""

#Preprocessed datayı eğitmek için RandomForestRegressor import ettim.

from sklearn.ensemble import RandomForestRegressor

random_forest = RandomForestRegressor()
random_forest.fit(X_train, y_train)

random_forest = RandomForestRegressor(n_estimators=100, random_state=42)

random_forest.fit(X_train, y_train)

y_pred = random_forest.predict(X_test)

#Random Forest tahmin değerlendirmesi için Mean Squared Error hesapladım.
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# R2 skorunu hesapladım.
r2 = r2_score(y_test, y_pred)
print("R2 Score:", r2)

# Scatterplot ile gerçek ve RF tahmini değerlerini grafikle karşılaştırdım.

sns.scatterplot(y = y_test, x = range(len(y_test)), color  ='green', label = "Actual")
sns.scatterplot(y = y_pred, x = range(len(y_pred)), color = 'blue', label = "Predicted")
plt.title("Actual VS Predict - Random Forest Regression")
plt.show()

"""# **Linear Regression**"""

from sklearn.linear_model import LinearRegression
linreg_model = LinearRegression()
linreg_model.fit(X_train, y_train)

linreg_model.intercept_

# Kategorilerin katsayıları
linreg_model.coef_

X_test[:5]

y_pred_test = linreg_model.predict(X_test)

y_pred_test[:5]

#Cross Validation ile modelin performansını değerlendirdim.

cv_linear_reg = cross_val_score(estimator = linreg_model, X = X, y = y, cv = 10)

scores = cross_val_score(estimator= linreg_model, X = X_train , y= y_train , cv=5 )
print("Cross-validation scores:" , cv_linear_reg)
print("Mean score:" , cv_linear_reg.mean())
print("Std score:" , cv_linear_reg.std())

#Training data için R2 Skoru
y_pred_train = linreg_model.predict(X_train)
r2_score_train_linear = r2_score(y_train, y_pred_train)

#Testing data için R2 Skoru
y_pred_test = linreg_model.predict(X_test)
r2_score_test_linear = r2_score(y_test, y_pred_test)

#Root mean squared error (RMSE)
rmse_linear = (np.sqrt(mean_squared_error(y_test, y_pred_test)))

print('R2_score (Train Accuracy) : {0:.3f}'.format(r2_score_train_linear))
print('R2_score (Test Accuracy) : {0:.3f}'.format(r2_score_test_linear))
print('RMSE : {0:.3f}'.format(rmse_linear))

from sklearn.model_selection import cross_val_predict
from sklearn import metrics
cv_pred = cross_val_predict(estimator= linreg_model , X= X_train , y=y_train , cv=5 )
print ("R2 score :" , metrics.r2_score( y_true= y_train, y_pred = cv_pred))

#For döngüsüyle tüm sütünlar için test ve training data karşılaştırmalı grafiği

for i in X_train.columns:
    plt.scatter(X_train[i], y_train, color="pink")
    plt.scatter(X_test[i], y_pred_test, color="green")
    plt.title("Train VS Predict - Linear Regression")
    plt.xlabel(f"{i}")
    plt.ylabel(f"charges")
    plt.show()

"""# **Ridge Regression**"""

ridge_model = Ridge(alpha=1)

ridge_model.fit(X_train,y_train)

y_pred_test = ridge_model.predict(X_test)


#Training data için R2 Skoru hesaplama
y_pred_train = ridge_model.predict(X_train)
r2_score_train_ridge = r2_score(y_train, y_pred_train)

#Testing data için R2 Skoru hesaplama
y_pred_test = ridge_model.predict(X_test)
r2_score_test_ridge = r2_score(y_test, y_pred_test)

#Root mean squared error (RMSE)
rmse_ridge = (np.sqrt(mean_squared_error(y_test, y_pred_test)))

print('R2_score (Train Accuracy) : {0:.3f}'.format(r2_score_train_ridge))
print('R2_score (Test Accuracy) : {0:.3f}'.format(r2_score_test_ridge))
print('RMSE : {0:.3f}'.format(rmse_ridge))

steps = [
    ('scalar', StandardScaler()),
    ('poly', PolynomialFeatures(degree=2)),
    ('model', Ridge())
]

ridge_pipe = Pipeline(steps)

# GridSearchCV ile hiperparametreleri optimize ediyorum.

parameters =  {  'model__alpha' : [43],
                 'model__fit_intercept' : [True],
                 'model__tol' : [0.0001],
                 'model__solver' : ['auto'],
                'model__random_state': [42]
}
regressor_ridge = GridSearchCV(ridge_pipe, parameters, cv=10)
regressor_ridge = regressor_ridge.fit(X, y.ravel())

print(regressor_ridge.best_score_)
print(regressor_ridge.best_params_)

# Cross Validation test seti tahmin etme
cv_ridge = regressor_ridge.best_score_

# R2 Score Training data tahmin sonucu
y_pred_ridge_train = regressor_ridge.predict(X_train)
r2_score_ridge_train = r2_score(y_train, y_pred_ridge_train)

# R2 Score Testing data tahmin sonucu
y_pred_ridge_test = regressor_ridge.predict(X_test)
r2_score_ridge_test = r2_score(y_test, y_pred_ridge_test)

# RMSE sonucu
rmse_ridge = (np.sqrt(mean_squared_error(y_test, y_pred_ridge_test)))

#Optimize edilen Ridge Regresyon metrikleri
print('CV: ', cv_ridge.mean())
print('R2_score (train): {0:.3f}'.format(r2_score_ridge_train))
print('R2_score (test): {0:.2f} '.format( r2_score_ridge_test))
print("RMSE: ", rmse_ridge)

"""# Ridge Regression final optimize R2 test skoru (Accuracy) : 0.89"""