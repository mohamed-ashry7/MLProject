import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer, StandardScaler ,MultiLabelBinarizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from fn import  get_time_in_seconds, get_the_grade, get_the_Intermediate_grade, rename_remove
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
        self.encoder = MultiLabelBinarizer(*args, **kwargs)

    def fit(self, x, y=0):
        self.encoder.fit(x)
        return self

    def transform(self, x, y=0):
        return self.encoder.transform(x)


df = pd.read_csv("MLData.csv", skipinitialspace=True)
# I have only taken the the students who only took the exam once
final_grades = joblib.load('final_grades_merged.joblib')
students_attended_final = final_grades['student_Id']

# I deleted all the excersices that does not mention the number of it
df = df[df.exercise != 'Es']
df = df[df.student_Id.isin(students_attended_final)]

# renamed the activities without the ES_X_Y
df['activity'] = df['activity'].apply(lambda x: rename_remove(x))
df['exercise'] = df['exercise'].apply(lambda x : x[:4])
# converted the start and end time into working time
df['working_time'] = df[['start_time', 'end_time']].apply(
    lambda x: get_time_in_seconds(x.start_time.strip(), x.end_time.strip()), axis=1)
# I Have dropped the idle time because it was corrupted
# Also dropping the start_time and end_time as I have converted them into other column which is working time
df.drop(['start_time', 'end_time', 'idle_time'], axis=1, inplace=True)

# d = {'sum': df.columns[3:]}
# df = df.groupby(['student_Id', 'exercise', 'activity'], as_index=False).agg(
#     {col: f for f, cols in d.items() for col in cols})
    

d = {set : ['activity'] , 'mean' : df.columns[3:]}
df = df.groupby(['student_Id', 'exercise'], as_index=False).agg(
    {col: f for f, cols in d.items() for col in cols})


df['intermediate_grade'] = df[['student_Id','exercise']].apply(lambda x :get_the_Intermediate_grade(x.student_Id,x.exercise) , axis = 1 )
GRADE_labels = df[['student_Id','exercise']].apply(lambda x :get_the_grade(x.student_Id,x.exercise) , axis = 1 )
df['activity'] = df['activity'].apply(lambda x : str(x))
print(df)
print (GRADE_labels)
df.drop(['student_Id'], axis=1, inplace=True)

print (df)


encoder = LabelBinarizer()
activity_encoded_one_hot = encoder.fit_transform(df['activity'])

num_attribs = list(df.columns[2:])
cat_attribs = list(df.columns[0:2])

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

print(df_prepared.shape)
joblib.dump(df_prepared,'ProcessedData.joblib')
joblib.dump(GRADE_labels,'Grades_labels.joblib')
