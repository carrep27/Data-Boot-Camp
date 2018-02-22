
# coding: utf-8

# Part 1: District Summaries

# In[51]:


#Dependencies
import pandas as pd

#get files
file = "schools_complete.csv"
file2 = "students_complete.csv"
school = pd.read_csv(file)
students = pd.read_csv(file2)
#rename "name" to "school" so we can merge on school
school = school.rename(columns={'name':'school'})
merge = pd.merge(school, students, on="school")

total_schools = len(merge["school"].unique())

total_students = school["size"].sum()

total_budget = school["budget"].sum()

avg_math = merge["math_score"].mean()
avg_reading = merge["reading_score"].mean()

#use loc to filter for passing math score. passing assumed to be over 70
passing_math = merge.loc[(merge["math_score"]>70)]

npm = passing_math["math_score"].count()

passmath = npm/total_students

passing_reading = merge.loc[(merge["reading_score"]>70)]

npr = passing_reading["reading_score"].count()

passreading = npr/total_students

#overall passsing rate is an average of passing math and passing reading
overall_passing_rate = (passmath+passreading)/2

#summary
summary = pd.DataFrame({'School Count':[total_schools],
                           'Students':[total_students],
                           'Budget':[total_budget],
                           'Avg Math Score':[avg_math],
                           'Avg Reading Score':[avg_reading],
                           '% Passing Math':[passmath],
                           '% Passing Reading':[passreading],
                           'Overall Pass Rate':[overall_passing_rate]
                          })
summary.round(2)



# Part 2: School Summary

# In[52]:


# rename columns
newschool = school[['school','type','budget']]
newschool2 = newschool.rename(columns={'type':'School Type','budget':'Total School Budget'})

# get budget per student;merge and set index to shool name
budget = school['budget']/school['size']
budget2 = pd.DataFrame({'Per Student Budget': budget})
school2 = pd.merge(newschool2, budget2, left_index=True, right_index=True)
school3 = school2.set_index('school')

# get student count
studentcount = students['school'].value_counts()
studentcount

#group by school and get average math/reading score
schoolgroup = students.groupby('school')
xmath = schoolgroup['math_score'].mean()
xread = schoolgroup['reading_score'].mean()

#get count of all math score, retrieve passing math count, get average
mathcount = schoolgroup['math_score'].count()
passingmath2 = passing_math[['school','math_score']] #using passing_math from Disctrict Summaries
passingmathgroup = passingmath2.groupby('school')
passmathcount =passingmathgroup['math_score'].count()
percentmath = passmathcount / mathcount * 100
percentmath

# Calculate % passing reading - using same process as math
readcount = schoolgroup['reading_score'].count()
passingreading2 = passing_reading[['school','reading_score']]
passingreadinggroup = passingreading2.groupby('school')
passreadcount =passingreadinggroup['reading_score'].count()
percentreading = passreadcount / readcount * 100
percentreading

# get overall pass rate
opr = (percentmath+percentreading)/2

# create second summary dataframe and merge with the dataframe created earlier
Summary2 = pd.DataFrame({'Total Students': studentcount,
                               'Average Math Score': xmath,
                               'Average Reading Score': xread,
                               '% Passing Math': percentmath,
                               '% Passing Reading': percentreading,
                               '% Overall Passing Rate': opr})
SummaryMerge = pd.merge(school3, Summary2, left_index=True, right_index=True)
SummaryMerge



# Top Performing Schools

# In[53]:


# use sort_values to dataframe just made, sort descending so top performers are first
TopSchools = SummaryMerge.sort_values('% Overall Passing Rate', ascending=False)
TopSchools

# only display first 5 rows
Top5 = TopSchools[:5]
Top5




# Bottom Performing Schools

# In[54]:


# use sort_values
BottomSchools = SummaryMerge.sort_values('% Overall Passing Rate')

# only display first 5 rows
Bottom5 = BottomSchools[:5]
Bottom5


# Math Scores by Grade

# In[55]:


# group by school and grade
groupgrade = students.groupby(['school','grade'])

# get average math dataframe
xmathgrade = pd.DataFrame(groupgrade['math_score'].mean())
xmathgrade


# Reading Scores by Grade

# In[56]:


# get average reading score data frame
xreadinggrade = pd.DataFrame(groupgrade['reading_score'].mean())
xreadinggrade


# Scores by School Spending

# In[57]:


# specify specific desired columns from summarymerge dataframe, create new dataframe for spending
columns = [2,6,7,4,5,3]
spending = SummaryMerge.iloc[:,columns]
spending

# create bins for spending
spendingbins = [0, 600, 615, 630, 645]
spendinglabels = ["<$600","$601-$615","$616-$630",">$631"]
pd.cut(spending['Per Student Budget'], spendingbins, labels=spendinglabels)
spending['Spending Ranges (Per Student)'] = pd.cut(spending['Per Student Budget'], spendingbins, labels=spendinglabels)
spending

# create new dataframe from bins
SpendingGroup = spending.groupby('Spending Ranges (Per Student)')
SpendingGroupM = SpendingGroup.max()
Columns2= [1,2,3,4,5]
GroupSummary =  SpendingGroupM.iloc[:,Columns2]
GroupSummary


# Scores by School Size

# In[58]:


# specify specific desired columns from summarymerge dataframe, create new dataframe for size
columns3 = [8,6,7,4,5,3]
sizesummary = SummaryMerge.iloc[:,columns3]

# create bins for size
sizebins = [0, 1500, 3000, 4500]
sizelabels = ["<1500)", "1501-3000", ">3001"]
pd.cut(sizesummary["Total Students"], sizebins, labels=sizelabels)
sizesummary['School Size'] = pd.cut(sizesummary['Total Students'], sizebins, labels=sizelabels)

sizegroup = sizesummary.groupby('School Size')
sizesummary2 = sizegroup.max()
columns4 = [1,2,3,4,5]
sizesummary2 =  sizesummary2.iloc[:,columns4]
sizesummary2


# Scores by School Type

# In[68]:


# specify specific desired columns, group by schook type

Columns4 = [0,6,7,4,5,3]
TypeSchool = SummaryMerge.iloc[:,Columns4]

#group by School Type
TypeGroup = TypeSchool.groupby('School Type')
TypeGroup.mean()

