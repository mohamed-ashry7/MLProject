
from datetime import datetime
import joblib 
import pandas as pd 

intermediate_grade = pd.read_csv('intermediate_grades.csv',skipinitialspace=True)
final_grades = joblib.load('final_grades_merged.joblib')


def convert_to_numeric (activities) :
    maper = {}
    x = 0
    def put_the_values(val):
        return maper[val]

    unique_elements = set(activities)
    for activity in unique_elements : 
        if activity not in maper :
            maper[activity] = x 
            x+=1
    return list(map(put_the_values,activities))
    
       
        
def rename_remove(activity):
    value = activity
    if 'Es' in  activity :
        value = activity[0:activity.index("Es")-1]
    if 'Fsm' in value :
        value = 'FSM'+value[3:]
    return value 
    
def get_time_in_seconds(start,end):
    dateformat = "%d.%m.%Y %H:%M:%S"
    a=datetime.strptime(start, dateformat)
    b = datetime.strptime(end, dateformat)
    delta = b-a
    return delta.seconds



def get_the_grade (student_Id , exercise ):
    session = 'Session_'+exercise[3:4]
    arr = final_grades.loc[(final_grades['student_Id'] == student_Id)][session].values
        
    return float(arr[0]) 


def get_the_Intermediate_grade (student_Id , exercise ):
    value = 'nil'
    session = int (exercise[3:4])
    if session >=2 and session <= 6 and student_Id in intermediate_grade['student_Id'] :
        session = 'Session '+str(session)
        arr = intermediate_grade.loc[(intermediate_grade['student_Id'] == student_Id)][session].values
        if len(arr) !=0 : 
            value = arr[0]
    elif session == 1 :
        value = 0 

    return value 