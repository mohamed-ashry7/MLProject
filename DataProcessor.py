import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer ,StandardScaler
from sklearn.pipeline import FeatureUnion ,Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from fn import convert_to_numeric , get_time_in_seconds , get_the_grade ,get_the_Intermediate_grade,rename_remove
import joblib 
import numpy as np

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values


class MyLabelBinarizer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.encoder = LabelBinarizer(*args, **kwargs)
    def fit(self, x, y=0):
        self.encoder.fit(x)
        return self
    def transform(self, x, y=0):
        return self.encoder.transform(x)


df = pd.read_csv("MLData.csv",skipinitialspace=True)
# I have only taken the the students who only took the exam once 
final_grades = joblib.load('final_grades_merged.joblib')
students_attended_final = final_grades['student_Id']

#I deleted all the excersices that does not mention the number of it 
df = df[df.exercise !='Es']
df = df[df.student_Id.isin(students_attended_final)]

# renamed the activities without the ES_X_Y
df['activity'] = df['activity'].apply(lambda x :rename_remove(x) )

# converted the start and end time into working time 
df['working_time'] = df[['start_time','end_time']].apply(lambda x :get_time_in_seconds(x.start_time.strip(),x.end_time.strip()),axis=1)
#I Have dropped the idle time because it was corrupted 
#Also dropping the start_time and end_time as I have converted them into other column which is working time 
df.drop(['start_time','end_time','idle_time'],axis=1,inplace =True)
             
encoder = LabelBinarizer()
activity_encoded_one_hot = encoder.fit_transform(df['activity'])
print (df)




# #we have converted the non-numeric data of activities to numeric ones 
num_attribs = list(df.columns[3:])
cat_attribs = list(df.columns[2:3])

num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('std_scaler', StandardScaler()),
])

cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),  
    ('label_binarizer', MyLabelBinarizer()),
])

full_pipeline = FeatureUnion(transformer_list=[
    ("num_pipeline", num_pipeline),
    ("cat_pipeline", cat_pipeline),
])


df_prepared = full_pipeline.fit_transform(df)
print(df_prepared)
# df['activity'] = convert_to_numeric(df['activity'].apply(lambda x : str(x)))

# df['intermediate_grade'] = df[['student_Id','exercise']].apply(lambda x :get_the_Intermediate_grade(x.student_Id,x.exercise) , axis = 1 )
# df['grade'] = df[['student_Id','exercise']].apply(lambda x :get_the_grade(x.student_Id,x.exercise) , axis = 1 )


# df.drop(['student_Id'],axis=1,inplace =True)
# df['exercise'] = convert_to_numeric(df['exercise'])
# df = df[df.grade != 0.001]
# df.plot(kind='scatter',x='activity',y='grade')
# # df.hist(bins=50, figsize=(20,15))
# plt.show()
# # joblib.dump(df,'ProcessedData.joblib')
