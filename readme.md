
This data was collected by UCI [Data and Full Description ](https://archive.ics.uci.edu/ml/datasets/Educational+Process+Mining+(EPM)%3A+A+Learning+Analytics+Data+Set).
# Aim
### Prediction of the grade of the students in the final exam per session



# Steps and procedures

## 1)Cleaning the data :
* Dropped the session column as it is already mentioned in the exercise `Es_1_1`
* Remove all the exercises that only mention `Es`
* Remove all the records of the students that did not take the final exam 
* Dropping the `idle_time` column as there is a lot of data corrupted 

## 2) Processing the data : 
* Renamed the values of the `activity` column i.e. `Deeds_Es_1_1` to `Deeds` to ease reading and manipulating the data 
* Converting the `start_time` and `end_time` into `working_time` column and dropping the former two columns 
* Renaming the `exercise` column values to remove any indication to which exercise it is i.e. `Es_1_1` to `Es_1`
* Grouping the data by the `student_Id` and `exercise` and collecting the `activities` into a `set` and taking the `mean`of the other values i.e.
```
student_Id , exercise , activity   , mouse_clicks .......
1          , Es_1   ,  {Deeds,Blank} , 5
.
.
.
```
* Summing the grades in the `final_grades.xlsx` file to indicate the the grade it took in that particular Session to be in that way 
```
student_Id , Session_1 , Session_2 ......
1          ,  5        , 1.5
```
* Mapping each grade of the intermediate grades to each student and the session 

# Model : 
Predition of the session grades of the students in the final exam based on the Features 
```
Grade = f(session , activities , click_of_mouse .....)
```
and that by using linear regression algorithm . 
# Results : 
By running the model many times the rmse values was ranging from 6 to 8 . 
