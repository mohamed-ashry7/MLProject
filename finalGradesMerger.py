import pandas as pd 
import joblib


df1 = pd.read_excel('final_grades.xlsx',sheet_name='Exam (First time)')
df2 =pd.read_excel('final_grades.xlsx',sheet_name='Exam (Second time)')
IDs = df1['student_Id']
diffRows = df2[~df2.student_Id.isin(IDs)]
df1 =pd.concat([diffRows,df1])
df1['Session_1'] = df1['Es_1_1']+df1['Es_1_2']
df1['Session_2'] = df1['Es_2_1']+df1['Es_2_2']
df1['Session_3'] = df1['Es_3_1']+df1['Es_3_2']+df1['Es_3_3']+df1['Es_3_4']+df1['Es_3_5']
df1['Session_4'] = df1['Es_4_1']+df1['Es_4_2']
df1['Session_5'] = df1['Es_5_1']+df1['Es_5_2']+df1['Es_5_3']
df1['Session_6'] = df1['Es_6_1']+df1['Es_6_2'] 

deleted_columns = df1.columns[1:18]
df1.drop(deleted_columns,axis=1,inplace =True)
print (df1)
joblib.dump(df1,'final_grades_merged.joblib')
