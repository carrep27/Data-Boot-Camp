
Part 1: District Summaries


```python
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


```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Avg Math Score</th>
      <th>Avg Reading Score</th>
      <th>Budget</th>
      <th>Overall Pass Rate</th>
      <th>School Count</th>
      <th>Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.72</td>
      <td>0.83</td>
      <td>78.99</td>
      <td>81.88</td>
      <td>24649428</td>
      <td>0.78</td>
      <td>15</td>
      <td>39170</td>
    </tr>
  </tbody>
</table>
</div>



Part 2: School Summary


```python
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


```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>Total Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>71.066164</td>
      <td>63.318478</td>
      <td>78.813850</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>2917</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>71.091896</td>
      <td>63.750424</td>
      <td>78.433367</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>2949</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>91.254969</td>
      <td>89.892107</td>
      <td>92.617831</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>1761</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>71.467098</td>
      <td>64.746494</td>
      <td>78.187702</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>4635</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>917500</td>
      <td>625.0</td>
      <td>91.553134</td>
      <td>89.713896</td>
      <td>93.392371</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>1468</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>92.093736</td>
      <td>90.932983</td>
      <td>93.254490</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>2283</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>91.711518</td>
      <td>89.558665</td>
      <td>93.864370</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>1858</td>
    </tr>
    <tr>
      <th>Bailey High School</th>
      <td>District</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>71.965434</td>
      <td>64.630225</td>
      <td>79.300643</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>4976</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>248087</td>
      <td>581.0</td>
      <td>91.686183</td>
      <td>90.632319</td>
      <td>92.740047</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>427</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>585858</td>
      <td>609.0</td>
      <td>91.943867</td>
      <td>91.683992</td>
      <td>92.203742</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>962</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>91.861111</td>
      <td>90.277778</td>
      <td>93.444444</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>1800</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>70.905226</td>
      <td>64.066017</td>
      <td>77.744436</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>3999</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>71.067003</td>
      <td>63.852132</td>
      <td>78.281874</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>4761</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>71.631982</td>
      <td>65.753925</td>
      <td>77.510040</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>2739</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>91.559633</td>
      <td>90.214067</td>
      <td>92.905199</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>1635</td>
    </tr>
  </tbody>
</table>
</div>



Top Performing Schools


```python
# use sort_values to dataframe just made, sort descending so top performers are first
TopSchools = SummaryMerge.sort_values('% Overall Passing Rate', ascending=False)
TopSchools

# only display first 5 rows
Top5 = TopSchools[:5]
Top5



```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>Total Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>92.093736</td>
      <td>90.932983</td>
      <td>93.254490</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>2283</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>585858</td>
      <td>609.0</td>
      <td>91.943867</td>
      <td>91.683992</td>
      <td>92.203742</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>962</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>91.861111</td>
      <td>90.277778</td>
      <td>93.444444</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>1800</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>91.711518</td>
      <td>89.558665</td>
      <td>93.864370</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>1858</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>248087</td>
      <td>581.0</td>
      <td>91.686183</td>
      <td>90.632319</td>
      <td>92.740047</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>427</td>
    </tr>
  </tbody>
</table>
</div>



Bottom Performing Schools


```python
# use sort_values
BottomSchools = SummaryMerge.sort_values('% Overall Passing Rate')

# only display first 5 rows
Bottom5 = BottomSchools[:5]
Bottom5
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>Total Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>70.905226</td>
      <td>64.066017</td>
      <td>77.744436</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>3999</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>71.066164</td>
      <td>63.318478</td>
      <td>78.813850</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>2917</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>71.067003</td>
      <td>63.852132</td>
      <td>78.281874</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>4761</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>71.091896</td>
      <td>63.750424</td>
      <td>78.433367</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>2949</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>71.467098</td>
      <td>64.746494</td>
      <td>78.187702</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>4635</td>
    </tr>
  </tbody>
</table>
</div>



Math Scores by Grade


```python
# group by school and grade
groupgrade = students.groupby(['school','grade'])

# get average math dataframe
xmathgrade = pd.DataFrame(groupgrade['math_score'].mean())
xmathgrade

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>math_score</th>
    </tr>
    <tr>
      <th>school</th>
      <th>grade</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Bailey High School</th>
      <th>10th</th>
      <td>76.996772</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>77.515588</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>76.492218</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.083676</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Cabrera High School</th>
      <th>10th</th>
      <td>83.154506</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>82.765560</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.277487</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.094697</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Figueroa High School</th>
      <th>10th</th>
      <td>76.539974</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>76.884344</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>77.151369</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>76.403037</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Ford High School</th>
      <th>10th</th>
      <td>77.672316</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>76.918058</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>76.179963</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.361345</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Griffin High School</th>
      <th>10th</th>
      <td>84.229064</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.842105</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.356164</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>82.044010</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Hernandez High School</th>
      <th>10th</th>
      <td>77.337408</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>77.136029</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>77.186567</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.438495</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Holden High School</th>
      <th>10th</th>
      <td>83.429825</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>85.000000</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>82.855422</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.787402</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Huang High School</th>
      <th>10th</th>
      <td>75.908735</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>76.446602</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>77.225641</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.027251</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Johnson High School</th>
      <th>10th</th>
      <td>76.691117</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>77.491653</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>76.863248</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.187857</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Pena High School</th>
      <th>10th</th>
      <td>83.372000</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>84.328125</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.121547</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.625455</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Rodriguez High School</th>
      <th>10th</th>
      <td>76.612500</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>76.395626</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>77.690748</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>76.859966</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Shelton High School</th>
      <th>10th</th>
      <td>82.917411</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.383495</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.778976</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.420755</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Thomas High School</th>
      <th>10th</th>
      <td>83.087886</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.498795</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.497041</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.590022</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Wilson High School</th>
      <th>10th</th>
      <td>83.724422</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.195326</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.035794</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.085578</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Wright High School</th>
      <th>10th</th>
      <td>84.010288</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.836782</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.644986</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.264706</td>
    </tr>
  </tbody>
</table>
</div>



Reading Scores by Grade


```python
# get average reading score data frame
xreadinggrade = pd.DataFrame(groupgrade['reading_score'].mean())
xreadinggrade

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>reading_score</th>
    </tr>
    <tr>
      <th>school</th>
      <th>grade</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Bailey High School</th>
      <th>10th</th>
      <td>80.907183</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.945643</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.912451</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>81.303155</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Cabrera High School</th>
      <th>10th</th>
      <td>84.253219</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.788382</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.287958</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.676136</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Figueroa High School</th>
      <th>10th</th>
      <td>81.408912</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.640339</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>81.384863</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>81.198598</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Ford High School</th>
      <th>10th</th>
      <td>81.262712</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.403642</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.662338</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>80.632653</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Griffin High School</th>
      <th>10th</th>
      <td>83.706897</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>84.288089</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.013699</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.369193</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Hernandez High School</th>
      <th>10th</th>
      <td>80.660147</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>81.396140</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.857143</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>80.866860</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Holden High School</th>
      <th>10th</th>
      <td>83.324561</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.815534</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.698795</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.677165</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Huang High School</th>
      <th>10th</th>
      <td>81.512386</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>81.417476</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.305983</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>81.290284</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Johnson High School</th>
      <th>10th</th>
      <td>80.773431</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.616027</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>81.227564</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>81.260714</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Pena High School</th>
      <th>10th</th>
      <td>83.612000</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>84.335938</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.591160</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.807273</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Rodriguez High School</th>
      <th>10th</th>
      <td>80.629808</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.864811</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.376426</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>80.993127</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Shelton High School</th>
      <th>10th</th>
      <td>83.441964</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>84.373786</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>82.781671</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>84.122642</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Thomas High School</th>
      <th>10th</th>
      <td>84.254157</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.585542</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>83.831361</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.728850</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Wilson High School</th>
      <th>10th</th>
      <td>84.021452</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>83.764608</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.317673</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.939778</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Wright High School</th>
      <th>10th</th>
      <td>83.812757</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>84.156322</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>84.073171</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>83.833333</td>
    </tr>
  </tbody>
</table>
</div>



Scores by School Spending


```python
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

```

    c:\Users\Carrep27\Anaconda3\envs\PythonData\lib\site-packages\ipykernel\__main__.py:10: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Spending Ranges (Per Student)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;$600</th>
      <td>83.803279</td>
      <td>83.989488</td>
      <td>90.932983</td>
      <td>93.864370</td>
      <td>92.093736</td>
    </tr>
    <tr>
      <th>$601-$615</th>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>91.683992</td>
      <td>92.203742</td>
      <td>91.943867</td>
    </tr>
    <tr>
      <th>$616-$630</th>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>89.713896</td>
      <td>93.392371</td>
      <td>91.553134</td>
    </tr>
    <tr>
      <th>&gt;$631</th>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>90.214067</td>
      <td>92.905199</td>
      <td>91.559633</td>
    </tr>
  </tbody>
</table>
</div>



Scores by School Size


```python
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
```

    c:\Users\Carrep27\Anaconda3\envs\PythonData\lib\site-packages\ipykernel\__main__.py:9: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;1500)</th>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>91.683992</td>
      <td>93.392371</td>
      <td>91.943867</td>
    </tr>
    <tr>
      <th>1501-3000</th>
      <td>83.682222</td>
      <td>83.989488</td>
      <td>90.932983</td>
      <td>93.864370</td>
      <td>92.093736</td>
    </tr>
    <tr>
      <th>&gt;3001</th>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>64.066017</td>
      <td>77.744436</td>
      <td>70.905226</td>
    </tr>
  </tbody>
</table>
</div>



Scores by School Type


```python
# specify specific desired columns, group by schook type

Columns4 = [0,6,7,4,5,3]
TypeSchool = SummaryMerge.iloc[:,Columns4]

#group by School Type
TypeGroup = TypeSchool.groupby('School Type')
TypeGroup.mean()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>90.363226</td>
      <td>93.052812</td>
      <td>91.708019</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>64.302528</td>
      <td>78.324559</td>
      <td>71.313543</td>
    </tr>
  </tbody>
</table>
</div>


