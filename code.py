import pandas as pd 
import numpy as np
import re

  #CSV file. Fetching only the required Columns
csv_file = 'cps.csv'
df = pd.read_csv(csv_file, sep =',', usecols = ['School_ID','Short_Name','Is_High_School',
                                                'Zip','Student_Count_Total','College_Enrollment_Rate_School',
                                                'Grades_Offered_All','School_Hours']
                                                )
  #To Expand all the columns for the output.                                    
pd.options.display.width = 0

def generateRequiredData():
    i = 0 
    while i < len(df.index) :
          #Generate Low-High Grade Offered
        gradesofferedall = str(df['Grades_Offered_All'].values[i])
        df.at[i,'Lowest_Grade_Offered'] = gradesofferedall[ 0 : gradesofferedall.find(',') ]
        df.at[i,'Highest_Grade_Offered'] = gradesofferedall[ gradesofferedall.rfind(',') + 1 : len(gradesofferedall) ]
          #Generate Starting School Hours
        schoolhours = str(df['School_Hours'].values[i])
        match = re.search('[1-9]+', schoolhours)
        if match is not None:
            df.at[i,'Starting_Hour'] = str(match.group()) + 'am'
        i += 1
    df.drop('Grades_Offered_All', axis=1, inplace=True)
    df.drop('School_Hours', axis=1, inplace=True)
    return

generateRequiredData()
  #Replacing the empty cells from column College_Enrollment_Rate_School with the mean.
df["College_Enrollment_Rate_School"] = df["College_Enrollment_Rate_School"].replace(r'\s+',np.nan,regex=True)
df["College_Enrollment_Rate_School"] = df["College_Enrollment_Rate_School"].fillna(df.loc[:,"College_Enrollment_Rate_School"].mean())
  #Print First 10 rows from the dataframe
print(df.head(10))
  #Find Mean And SD of College_Enrollment_Rate_School for High schools
print("\nCollege Enrollment Rate for High Schools = {:.2f} (sd = {:.2f})".format(df.query("Is_High_School == True")['College_Enrollment_Rate_School'].mean(), df.query("Is_High_School == True")['College_Enrollment_Rate_School'].std()))
  #Find Mean And SD of Total Student Count for Non-High schools
print("\nTotal Student Count for Non-High Schools = {:.2f} (sd = {:.2f})".format(df.query("Is_High_School == False")['Student_Count_Total'].mean(), df.query("Is_High_School == False")['Student_Count_Total'].std()))
print("\nDistribution Of Starting Hours")
  #Find Distribution of Starting Hours
print(df['Starting_Hour'].value_counts().to_string())
  #Find Number Of Schools Outside the Loop
print("\nNumber of schools outside the Loop: ", df.query("Zip > 60616 or Zip <60601 or Zip>60607 and Zip<60616")['Zip'].count())
