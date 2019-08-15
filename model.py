import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
import numpy as np




X = joblib.load('ProcessedData.joblib')
y = joblib.load('Grades_labels.joblib')
X_train,X_test , y_train , y_test =train_test_split(X,y,test_size=0.2)
model= LinearRegression()
model.fit(X_train,y_train)
predictions = model.predict(X_test)
lin_mse = mean_squared_error(y_test,predictions)
lin_rmse = np.sqrt(lin_mse)
print (lin_rmse)

