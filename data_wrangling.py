########################################################DATA WRANGLING############################################
import numpy as np
import pandas as pd


###Reading dataframe
df = pd.read_csv('/home/biplab/Desktop/Mypractice/practice_data/Crime_2015.csv')

###to check the dimension
df.shape

###to check the datatypes of column and 
df.dtypes
df.info() #along with datatype of columns it will give the count of nonmissing values

###to see the descriptive statistics of numeric columns
df.describe

###to see 1000 rows when use print 
pd.set_option('display.max.rows',1000)

#to see all the columns
pd.set_option('display.max.columns',len(df.columns))

###########################################ADDING NEW COLUMN ##################################################

###creating a new catagorical column based on condtion.  if robbery less than 65 then it is robberylow otherwise robberylow
##method1
df['RobberyArea'] = np.where(df['Robbery'] < 65, 'low_robbery','high_robbery')

##method2(by sing apply function)
def robbery(num):
	if num < 65:
		return 'low_robbery'
	else:
		return 'high_robbery'

df['RobberyArea1'] = df['Robbery'].apply(robbery)

#Method3
#more than two condition
conditions = [
    (df['Robbery'] < 30),
    (df['Robbery'] >= 30) & (df['Robbery'] < 60),
    (df['Robbery'] >= 60) & (df['Robbery'] < 90),
    (df['Robbery'] >= 90)]
values = ['a', 'b', 'c', 'd']
df['RobberyArea'] = np.select(conditions, values) 

#Creating a new which iss 2 times of Robbery

df['newcolumn'] = df['Robbery'] * 2

##Dropping column
#method1
df = df.drop('RobberyArea',axis= 1)	

#method2
df.drop('RobberyArea',axis = 1, inplace = True)

#dropping multiple columns
df = df.drop(['RobberyArea','newcolumn'],axis= 1)


###############################################Filtering in pandas#######################################
##method1
new_df = df[df['State'] == 'TX'] #selecting records where state is TX
new_df = df[(df['State'] == 'TX') & (df['City'] == 'Austin')] #selecting records where state is TX and city is Austin

##method2
new_df = df.loc[df['State'] == 'TX','MSA'] #selecting MSA column where State is TX
new_df = df.loc[df['State'] == 'TX',['MSA','Robbery']] #selecting two columns with filtering condition

#method3
new_df = df.query('State == "TX"')
new_df = df.query('State == "TX" & City == "Austin"')

new_df = df.iloc[:5,] #First 5 rows
new_df = df.iloc[1:5,] #Second to Fifth row
new_df = df.iloc[5,0] #Sixth row and 1st column
new_df = df.iloc[1:5,0] #Second to Fifth row, first column
new_df = df.iloc[1:5,:5] #Second to Fifth row, first 5 columns
df.iloc[2:7,1:3] #Third to Seventh row, 2nd and 3rd column

################################################sorting in pandas###########################################
new_df = df.sort_values('State',ascending = False)
df.sort_values(by = 'State',ascending = False,inplace = True) #to apply on the same dataframe
df.sort_values(by = ['State','City'],ascending = [False,False],inplace = True)

##################################################Aggragration##############################################
df['Murder'].mean() #to get the mean of murder column
df['Murder'].mediam() #to get the median of mureder column

#select the records where city is Austin
group_city = df.groupby('City')
new_df = group_city.get_group('Austin')

##group by and converting group by into proper format
df['RobberyArea'] = np.where(df['Robbery'] < 65, 'low_robbery','high_robbery')
new_df = df.groupby('RobberyArea').agg({'Murder' : ['mean','median','min','max']})
new_df.columns = new_df.columns.droplevel() #droppoing multilevel columns
new_df.columns = [('Murder_' + i) for i in new_df.columns] #concatenating columns to aggregrate variable
new_df = new_df.reset_index() #reseting index

##for two analysis varible and two grouping variables
new_df = df.groupby('RobberyArea').agg({'Murder' : ['mean','median','min','max'], 'Robbery' : ['mean','median','min','max']})
new_df = df.groupby(['RobberyArea','State']).agg({'Murder' : ['mean','median','min','max'], 'Robbery' : ['mean','median','min','max']})
