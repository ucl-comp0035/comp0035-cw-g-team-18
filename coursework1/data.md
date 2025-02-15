# Data Preparation and Understanding

***This markdown file is used to describe the process of data preparation including how missing values are dealt with 
and how region, industry and size of the company are determined. It will also provide some data visualizations to help 
understand the dataset.***

## 1. Description of Initial Data from GOV.UK
The dataset shows the gender pay gap situations reported from different companies in various sizes and 
from different industries and regions. It consists of six separate csv spreadsheets, which show situations from reporting
year 2017-18 to 2022-23 respectively. It can be downloaded from [website of Gender Pay Gap Service of UK Government.](https://gender-pay-gap.service.gov.uk)
Each spreadsheet has the same 27 columns which can ba grouped into
three categories:

| Company Basic Info                                                                                                                       | Gender Pay Gap Figures                                                                                                                                                                                                                                                                                                 | Submission Time                                   |
|------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|
| EmployerName, EmployerID, Address, PostCode, CompanyNumber, SicCodes, CompanyLinkToGPGInfo, ResponsiblePerson, EmployerSize, CurrentName | DiffMeanHourlyPercent, DiffMedianHourlyPercent, DiffMeanBonusPercent, DiffMedianBonusPercent, MaleBonusPercent, FemaleBonusPercent, MaleLowerQuartile, FemaleLowerQuartile, MaleLowerMiddleQuartile, FemaleLowerMiddleQuartile, MaleUpperMiddleQuartile, FemaleUpperMiddleQuartile, MaleTopQuartile, FemaleTopQuartile | SubmittedAfterTheDeadline, DueDate, DateSubmitted |
                                                                                                                                                                                                                                                                                                                                                                                                            
In case of data types, the 27 columns can also be grouped into three:

| Text                                                                                                                         | Numerical                                                                                                                                                                                                                                                                                                                          | Boolean                   |
|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| EmployerName, Address, PostCode, CompanyNumber, SicCodes, CompanyLinkToGPGInfo, ResponsiblePerson, EmployerSize, CurrentName | EmployerId, DiffMeanHourlyPercent, DiffMedianHourlyPercent, DiffMeanBonusPercent, DiffMedianBonusPercent, MaleBonusPercent, FemaleBonusPercent, MaleLowerQuartile, FemaleLowerQuartile, MaleLowerMiddleQuartile, FemaleLowerMiddleQuartile, MaleUpperMiddleQuartile, FemaleUpperMiddleQuartile, MaleTopQuartile, FemaleTopQuartile | SubmittedAfterTheDeadline |

The number of rows of each table is shown below:

| Reporting Year | Rows      |
|----------------|-----------|
| 2017-18        | 10225     |
| 2018-19        | 10466     |
| 2019-20        | 6921      |
| 2020-21        | 10532     |
| 2021-22        | 10491     |
| 2022-23        | 353       |
|                |           |
| **Total**      | **48988** |

The exact meaning of each column can be checked from the original website. 
In case readers of this file do not have time to check on their own and some names are not quite intuitive, 
it is necessary to explain some vague meanings:

1. **SicCodes** represents Standard Industrial Classification code of the company at the time of submission, showing its nature of business;
2. All **Diff** values show the % difference between male and female, where the negative figures indicate female has higher pay;
3. The remaining **Gender Pay Gap Figures** represent the percentage of certain gender employee paid a bonus or in certain quarter of payment levels within their company.

## 2. Data Preparation
After loading the six spreadsheets into the data_prep python file and looking at their basic information mentioned in 
the previous section, we decided to merge all the tables into one single dataframe they all contain the same columns. 
The merger is inconsequential as we do not expect the situation would vary a lot within these years, and we do not plan 
to analyze in time series. Instead, we wish to have a look at the gender pay gap situation across different industries, 
regions and company sizes. The merged dataset then became the initial dataset for preparation.

<details><summary> CLICK TO SEE CODES TO LOAD & MERGE DATASET </summary>
<p>

```ruby
# Load initial datasets
df_1 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2017 to 2018.csv')
df_2 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2018 to 2019.csv')
df_3 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2019 to 2020.csv')
df_4 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2020 to 2021.csv')
df_5 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2021 to 2022-2.csv')
df_6 = pd.read_csv('Gender_Pay_Gap/UK Gender Pay Gap Data - 2022 to 2023-3.csv')
dfs = [df_1, df_2, df_3, df_4, df_5, df_6]
for df in dfs:
    print(df.shape, df.columns, df.dtypes)
# Merge datasets into a single large one and save
df_merge = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6], axis=0)
print(df_merge.shape, df_merge.columns)
df_merge.to_csv('gender_pay_gap_initial.csv')
```
   
</p>
</details>

### 2.1. Delete Unnecessary Columns
Since the time series are no loger considered, columns including 
**SubmittedAfterTheDeadline, DueDate & DateSubmitted** can be removed. Meanwhile, in order to protect privacy and 
prevent direct focus on a particular company, information including **Address, EmployerName, EmployerId, 
CompanyNumber, CompanyLinkToGPGInfo,ResponsiblePerson & CurrentName** that can locate a specific company or person 
are removed as well. Although **PostCode** can also indicate the address of that single company, it is kept at this stage 
and will be processed later as the project needs to analyze on regional patterns. 

<details><summary> CLICK TO SEE CODES TO DELETE UNNECESSARY COLUMNS </summary>
<p>

```ruby
df_merge.drop(['Address', 'EmployerName', 'EmployerId', 'CompanyNumber', 'CompanyLinkToGPGInfo',
               'ResponsiblePerson', 'CurrentName', 'SubmittedAfterTheDeadline',
               'DueDate', 'DateSubmitted'], axis=1, inplace=True)
print(df_merge.shape, df_merge.columns)
```

</p>
</details>

### 2.2. Deal with Null Values
By using the code

```print(df_merge.isnull().sum())```

The numbers of null values for each column are shown as below:

```
PostCode                      170
SicCodes                     2919
DiffMeanHourlyPercent           0
DiffMedianHourlyPercent         0
DiffMeanBonusPercent         9015
DiffMedianBonusPercent       9017
MaleBonusPercent                0
FemaleBonusPercent              0
MaleLowerQuartile             397
FemaleLowerQuartile           397
MaleLowerMiddleQuartile       397
FemaleLowerMiddleQuartile     397
MaleUpperMiddleQuartile       397
FemaleUpperMiddleQuartile     397
MaleTopQuartile               397
FemaleTopQuartile             397
EmployerSize                    0
dtype: int64

```

#### Delete Directly

It can be inferred that missing values on **MaleLowerQuartile, FemaleLowerQuartile, 
MaleLowerMiddleQuartile, FemaleLowerMiddleQuartile, MaleUpperMiddleQuartile, FemaleUpperMiddleQuartile, 
MaleTopQuartile and FemaleTopQuartile** are in the **same rows**. Meanwhile, compared with 48988 total rows, 
these 397 rows as well as 2919 rows containing missing values on SicCodes and 
only 170 of that on PostCode seem to be irrelevant. 
Therefore, these columns are simply removed from the dataset with the code

```df_merge = df_merge.dropna(subset=['MaleLowerQuartile', 'SicCodes', 'PostCode'])```

#### Perform Random Forest Model to Predict Missing Values

However, even after deleting these rows, there are still 8181 missing values on DiffMeanBonusPercent and 
8183 on DiffMedianBonusPercent, which are relatively a large proportion (approximately 18%) 
of the total rows. This proportion makes it unsuitable to be removed as above as it may affect the
 total trend. Furthermore, by looking at the correlation heatmap below, there is no obvious correlations between those two 
variables and others. Therefore, it is not possible to infer those missing values directly from existing values.

![](cw1_data_visulization/correlogram.png)

<details><summary> CLICK TO SEE CODES TO DRAW CORRELATION HEATMAP </summary>
<p>

```ruby

pd.set_option('display.max_columns', None)
print(df_merge.corr())
ax = sns.heatmap(df_merge.corr(), linewidth=0.5)
plt.show()

```
   
</p>
</details>

In this case, a tree-based machine learning model -- Random Forest is utilized to predict those missing 
values. To perform the model, the dataframe was first split into a training dataframe with no missing values and a 
testing dataframe with rows containing those missing values. Each dataframe was also separated to two dependent 
variable dataframe containing columns of DiffMeanBonusPercent & DiffMedianBonusPercent respectively, which the model is about to 
make predictions on, and an independent variable dataframe containing other numerical values. Then, the training 
data was fitted into the Random Forest model to train the model. After training the model, the testing dataset was 
used to make predictions on those missing values and those missing values were filled with predictions.

***Very Important Message to Readers: The Random Forest Model can be quite slow to 
execute :smiling_face_with_tear:, please be patient.***

***Also, there might be an error message showing***
```
DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples,), for example using ravel().
  model_1.fit(X_train, y_1_train)
```
***This can be ignored as it will not impact the result.***

<details><summary> CLICK TO SEE CODES TO PERFORM RANDOM FOREST & FILL IN MISSING VALUES </summary>
<p>

```ruby

# Split Dataset
X_train = df_merge_training[['DiffMeanHourlyPercent',
                             'DiffMedianHourlyPercent', 'MaleBonusPercent', 'FemaleBonusPercent',
                             'MaleLowerQuartile', 'FemaleLowerQuartile', 'MaleLowerMiddleQuartile',
                             'FemaleLowerMiddleQuartile', 'MaleUpperMiddleQuartile',
                             'FemaleUpperMiddleQuartile', 'MaleTopQuartile', 'FemaleTopQuartile']]

y_1_train = df_merge_training[['DiffMeanBonusPercent']]

y_2_train = df_merge_training[['DiffMedianBonusPercent']]

X_test = df_merge_testing[['DiffMeanHourlyPercent',
                           'DiffMedianHourlyPercent', 'MaleBonusPercent', 'FemaleBonusPercent',
                           'MaleLowerQuartile', 'FemaleLowerQuartile', 'MaleLowerMiddleQuartile',
                           'FemaleLowerMiddleQuartile', 'MaleUpperMiddleQuartile',
                           'FemaleUpperMiddleQuartile', 'MaleTopQuartile', 'FemaleTopQuartile']]

# Define Model

model_1 = RandomForestRegressor(n_estimators=100, random_state=0)

model_2 = RandomForestRegressor(n_estimators=100, random_state=0)

# Fit Model

model_1.fit(X_train, y_1_train)

model_2.fit(X_train, y_2_train)

# Predict the value with the testing data and substitute values to null values
y_1_pred = model_1.predict(X_test)
y_2_pred = model_2.predict(X_test)
print(y_1_pred, y_2_pred)
df_merge_testing = df_merge_testing.assign(DiffMeanBonusPercent=y_1_pred)
df_merge_testing = df_merge_testing.assign(DiffMedianBonusPercent=y_2_pred)
print(df_merge_testing.shape, df_merge_testing.columns, df_merge_testing.isnull().sum())

```
   
</p>
</details>

#### Bind Separated Dataframes

Finally, the testing dataframe filled with predicted values was integrated with the training dataframe, which 
generated a dataframe with 45650 rows and no missing values. 

```

(45650, 17) 

Index(['PostCode', 'SicCodes', 'DiffMeanHourlyPercent',
       'DiffMedianHourlyPercent', 'DiffMeanBonusPercent',
       'DiffMedianBonusPercent', 'MaleBonusPercent', 'FemaleBonusPercent',
       'MaleLowerQuartile', 'FemaleLowerQuartile', 'MaleLowerMiddleQuartile',
       'FemaleLowerMiddleQuartile', 'MaleUpperMiddleQuartile',
       'FemaleUpperMiddleQuartile', 'MaleTopQuartile', 'FemaleTopQuartile',
       'EmployerSize'],
      dtype='object') 

PostCode                     0
SicCodes                     0
DiffMeanHourlyPercent        0
DiffMedianHourlyPercent      0
DiffMeanBonusPercent         0
DiffMedianBonusPercent       0
MaleBonusPercent             0
FemaleBonusPercent           0
MaleLowerQuartile            0
FemaleLowerQuartile          0
MaleLowerMiddleQuartile      0
FemaleLowerMiddleQuartile    0
MaleUpperMiddleQuartile      0
FemaleUpperMiddleQuartile    0
MaleTopQuartile              0
FemaleTopQuartile            0
EmployerSize                 0

```

<details><summary> CLICK TO SEE CODES TO INTEGRATE TWO DATAFRAMES </summary>
<p>

```ruby

df_none_na = pd.concat([df_merge_training, df_merge_testing], axis=0)
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

```

</p>
</details>

### 2.3. Deal with PostCode, SicCodes & EmployerSize
The current dataset has no clear indication on the region and industry of those companies. Therefore, we need to 
infer these information from PostCode and SicCodes. Meanwhile, in case future analysis may need relations between 
those index with company sizes, it is better to convert the EmployerSize into a numerical variable.

#### Deal with PostCode
As mentioned above, it is not appropriate to include information that can target on a particular company. Since the 
postcode in UK can easily locate an address, which then can locate the company, it is necessary to substitute these 
postcodes with a wider geographical area. By looking at the [explanation on UK postcode format 
published by UK Government, ](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/283357/ILRSpecification2013_14Appendix_C_Dec2012_v1.pdf)
it can be concluded that a postcode in UK consists of two parts -- an Outcode (before space) and an Incode (after space). 
Having only the Outcode can locate the region of the company in. Therefore, strings after the space in the column 
PostCode were dropped and only the Outcode part was kept with code below.

```ruby

df_none_na["PostCode"] = df_none_na["PostCode"].str.split().str[0]

```
Then, [a dataset published by doogal.co.uk](https://www.doogal.co.uk/PostcodeDistricts) with a complete list of UK 
postcode districts was used to match the Outcode to the Region and UK Region it represents with inner merge function of pandas.

```ruby

df_out_code = pd.read_csv('Postcode districts.csv')
df_out_code.drop(['Latitude', 'Longitude', 'Easting', 'Northing', 'Grid Reference', 'Town/Area',
                  'Postcodes', 'Active postcodes', 'Population', 'Households',
                  'Nearby districts'], axis=1, inplace=True)
print(df_out_code.dtypes)

# Inner merge two df
df_none_na = df_none_na.merge(df_out_code, left_on='PostCode', right_on='Postcode', how='inner')
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))
df_none_na.drop(['Postcode'], axis=1, inplace=True)
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

```

#### Deal with SicCodes
The Standard Industrial Classification code represents the nature of a business. In this dataframe, some companies have 
multiple SIC codes, which is understandable as the company can do various business activities. However, to make it convenient 
for us to do analysis, we choose only to keep the last term of the list for those companies having multiple codes.
```ruby

df_none_na["SicCodes"] = df_none_na["SicCodes"].str.split(pat='\n').str[-1]
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

```

The [UK government has classified SIC codes into 21 sections from A to U.](https://resources.companieshouse.gov.uk/sic/) 
Though there is no ready-to-use dataframe for matching, since codes of each section is progressive 
from small to big numbers, it is easy to manually create a mapping with the number range shown as below.

```ruby

mappings = [
    (1110, 3220, 'Agriculture， Forestry & Fishing'),
    (5101, 9900, 'Mining & Quarrying'),
    (10110, 33200, 'Manufacturing'),
    (35110, 35300, 'Electricity, gas, steam and air conditioning supply'),
    (36000, 39000, 'Water supply, sewerage, waste management and remediation activities'),
    (41100, 43999, 'Construction'),
    (45111, 47990, 'Wholesale and retail trade; repair of motor vehicles and motorcycles'),
    (49100, 53202, 'Transportation and storage'),
    (55100, 56302, 'Accommodation and food service activities'),
    (58110, 63990, 'Information and communication'),
    (64110, 66300, 'Financial and insurance activities'),
    (68100, 68320, 'Real estate activities'),
    (69101, 75000, 'Professional, scientific and technical activities'),
    (77110, 82990, 'Administrative and support service activities'),
    (84110, 84300, 'Public administration and defence; compulsory social security'),
    (85100, 85600, 'Education'),
    (86101, 88990, 'Human health and social work activities'),
    (90010, 93290, 'Arts, entertainment and recreation'),
    (94110, 96090, 'Other service activities'),
    (97000, 98200, 'Activities of households as employers; undifferentiated goods- and services-producing activities '
                   'of households for own use'),
    (99000, 99999, 'Activities of extraterritorial organisations and bodies'),
]
errors = set()

```

After that, the remaining SicCodes of the gender pay gap dataframe was converted to integers and was compared with the 
range set in mappings. By doing this, the SicCodes are matched with the business activities that companies do (Industry).

<details><summary> CLICK TO SEE HOW SIC CODES ARE MATCHED WITH INDUSTRY IN CODE </summary>
<p>

```ruby

def to_code_range(i):
    if type(i) != str:
        return np.nan
    if i == "None Supplied":
        return np.nan
    siccode = int(i[0:5])
    for code_from, code_to, name in mappings:
        if code_from <= siccode <= code_to:
            return name
    errors.add(siccode)
    return np.nan


df_none_na['Industry'] = df_none_na['SicCodes'].map(to_code_range)
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

```

</p>
</details>

#### Deal with EmployerSize
In case the future analysis may require looking at correlations between gender pay gap situations and the size 
of companies, it can be helpful to convert the EmployerSize from strings to numerical values. By checking the unique 
categories of EmployerSize with code
```print(df_none_na.EmployerSize.value_counts())```
It can be concluded that there are 7 types of EmployerSize shown as below.
```ruby

250 to 499        19769
500 to 999        11093
1000 to 4999       9781
5000 to 19,999     2108
Less than 250      1722
Not Provided        688
20,000 or more      283

```
Therefore, we simply choose to use the median number of the range given by original dataset, 
use 35000 to represent sizes of those companies having more than 20000 employees, and substitute those 
'Not Provided' with np.nan.

<details><summary> CLICK TO SEE HOW EmployerSize WERE PROCESSED IN CODE </summary>
<p>

```ruby

mapping = {
    'Less than 250': 125,
    '250 to 499': 350,
    '500 to 999': 750,
    '1000 to 4999': 3000,
    '5000 to 19,999': 12500,
    '20,000 or more': 35000,
    'Not Provided': np.nan
}

df_none_na['EmployerSizeMedian'] = df_none_na['EmployerSize'].map(mapping.get)
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

```

</p>
</details>


By then, the data is ready to be used for future analysis. While new missing values (shown as below) appear due to 
adding null values to 'Not Provided' and 'None Supplied' strings, they can be ignorable as they only take up a very 
small proportion of total rows (45444 rows after processing).
```
UK region                      7
Industry                     711
EmployerSizeMedian           688
```

The processed dataframe was then exported as gender_pay_gap_prepared.csv for future use.

## 3. Data Visualization
To help better understand the data, we have generated several data visualizations.
### Histograms of DiffMeanHourlyPercent & DiffMedianHourlyPercent
![](cw1_data_visulization/Figure_1.png) 

![](cw1_data_visulization/Figure_2.png)

The two histograms show distributions of DiffMeanHourlyPercent and DiffMedianHourlyPercent in general, 
which can be used to determine the overall trend on gender pay gap as these figures directly show the 
salary situation. Since both of these histograms are negatively skewed, it can be inferred that most 
companies pay more to male than to female.

<details><summary> CLICK TO SEE HOW HISTOGRAMS WERE DRAWN IN CODE </summary>
<p>

```ruby

# Plot1: Histogram on DiffMeanHourly Percent
fig1, ax1 = plt.subplots()
ax1.set_title('Distribution of DiffMeanHourlyPercent')
ax1.hist(df_visualization[['DiffMeanHourlyPercent']], bins=50)

# Plot2: Histogram on DiffMedianHourly Percent
fig2, ax2 = plt.subplots()
ax2.set_title('Distribution of DiffMedianHourlyPercent')
ax2.hist(df_visualization[['DiffMedianHourlyPercent']], bins=50)

```

</p>
</details>

### Boxplot against Company Size
Then, three boxplot showing DiffMeanHourlyPercent, DiffMeanBonusPercent and FemaleTopQuartile against company 
size were plotted to indicate the impact of company size on wage payment, bonus payment, and female revenue 
ceiling respectively.

![](cw1_data_visulization/Figure_3.png) 

It can be seen that larger companies tend to have narrower gap in base wage payment between men and 
women. 

![](cw1_data_visulization/Figure_4.png)

However, there is a proportional relationship between DiffMeanBonusPercent and company size, 
which indicates that larger organizations tend to pay more bonus to men in average. 

![](cw1_data_visulization/Figure_5.png)

Meanwhile, as the largest companies have fewest FemaleTopQuartile, it can be inferred that it is difficult for females to 
get paid highly in large groups. In addition, all average lines are below 50, which means the total number of highly-paid 
females is smaller than that of males.

<details><summary> CLICK TO SEE HOW BOXPLOT AGAINST COMPANY SIZE WERE DRAWN IN CODE </summary>
<p>

```ruby

# Plot3: BoxPlot of DiffMeanHourlyPercent against EmployerSizeMedian
fig3 = plt.subplots()
ax3 = sns.boxplot(data=df_visualization, y="DiffMeanHourlyPercent", x="EmployerSizeMedian")
ax3.set(ylim=(-200, 200))
ax3.set_title('BoxPlot of DiffMeanHourlyPercent against EmployerSizeMedian')

# Plot4: BoxPlot of DiffMeanBonusPercent against EmployerSizeMedian
fig4 = plt.subplots()
ax4 = sns.boxplot(data=df_visualization, y="DiffMeanBonusPercent", x="EmployerSizeMedian")
ax4.set(ylim=(-200, 200))
ax4.set_title('BoxPlot of DiffMeanBonusPercent against EmployerSizeMedian')

# Plot5: BoxPlot of FemaleTopQuartile against EmployerSizeMedian
fig5 = plt.subplots()
ax5 = sns.boxplot(data=df_visualization, y="FemaleTopQuartile", x="EmployerSizeMedian")
ax5.set(ylim=(-200, 200))
ax5.set_title('BoxPlot of FemaleTopQuartile against EmployerSizeMedian')

```

</p>
</details>

### Boxplot against Company Size & Industry
In order to see whether trends found above are in general across all types of industries, the three plots 
were re-drawn by categorizing with industries.

![](cw1_data_visulization/Figure_6.png) 

It can be seen that not all industries have narrower payment gap in larger organizations. For example, the 
largest size of financial and insurance companies tend to have the highest difference in hourly payment between 
male and female. Meanwhile, the graph makes sense in case that conventionally men-favored industries such as 
**Manufacturing, Construction, Real Estate, Mining and Finance** have overall higher mean gender pay gap against women.

![](cw1_data_visulization/Figure_7.png)

The overall trend on bonus gap keeps working on different industries except **transportation & storage**, where larger 
companies have smaller bonus gap in average.

![](cw1_data_visulization/Figure_8.png)

In case of highly paid female numbers across different industries, it can be seen that 
females in industries like **Education and Human health and social work activities**, take more proportions in highly-paid 
workers. However, it is quite difficult for them to be paid highly in men-favored industries.

<details><summary> CLICK TO SEE HOW BOXPLOT AGAINST COMPANY SIZE & INDUSTRIES WERE DRAWN IN CODE </summary>
<p>

```ruby

# Plot6: BoxPlot of DiffMeanHourlyPercent against EmployerSizeMedian & Industry
fig6 = plt.subplots()
ax6 = sns.boxplot(data=df_visualization, y="DiffMeanHourlyPercent", x="Industry", hue='EmployerSizeMedian')
ax6.set(ylim=(-200, 200))
ax6.tick_params(axis='x', labelrotation=90)
ax6.set_title('BoxPlot of DiffMeanHourlyPercent against EmployerSizeMedian & Industry')

# Plot7: BoxPlot of DiffMeanBonusPercent against EmployerSizeMedian & Industry
fig7 = plt.subplots()
ax7 = sns.boxplot(data=df_visualization, y="DiffMeanBonusPercent", x="Industry", hue='EmployerSizeMedian')
ax7.set(ylim=(-200, 200))
ax7.tick_params(axis='x', labelrotation=90)
ax7.set_title('BoxPlot of DiffMeanBonusPercent against EmployerSizeMedian & Industry')

# Plot8: BoxPlot of FemaleTopQuartile against EmployerSizeMedian & Industry
fig8 = plt.subplots()
ax8 = sns.boxplot(data=df_visualization, y="FemaleTopQuartile", x="Industry", hue='EmployerSizeMedian')
ax8.set(ylim=(-50, 150))
ax8.tick_params(axis='x', labelrotation=90)
ax8.set_title('BoxPlot of FemaleTopQuartile against EmployerSizeMedian & Industry')

```

</p>
</details>

### Boxplot against Regions
Finally, these three index were plotted against regions to show whether geographical reasons impact the gender pay gap. 

![](cw1_data_visulization/Figure_9.png) 

It can be shown that the average differences between male and female wage across different regions in the UK are similar 
to each other. However, Wales and Northern Ireland tend to have smaller variance.

![](cw1_data_visulization/Figure_10.png) 

London has the highest difference in gender bonus payment in average while North East has the lowest (nearly to 0).

![](cw1_data_visulization/Figure_11.png) 

Northern Ireland and Scotland has the smaller proportion of highly-paid women in general while other areas 
look to have similar levels.

<details><summary> CLICK TO SEE HOW BOXPLOT AGAINST REGION WERE DRAWN IN CODE </summary>
<p>

```ruby

# Plot9: BoxPlot of DiffMeanHourlyPercent against Region
fig9 = plt.subplots()
ax9 = sns.boxplot(data=df_visualization, y="DiffMeanHourlyPercent", x="UK region")
ax9.set(ylim=(-200, 200))
ax9.tick_params(axis='x', labelrotation=90)
ax9.set_title('BoxPlot of DiffMeanHourlyPercent against Region')

# Plot10: BoxPlot of DiffMeanBonusPercent against Region
fig10 = plt.subplots()
ax10 = sns.boxplot(data=df_visualization, y="DiffMeanBonusPercent", x="UK region")
ax10.set(ylim=(-200, 200))
ax10.tick_params(axis='x', labelrotation=90)
ax10.set_title('BoxPlot of DiffMeanBonusPercent against Region')

# Plot11: BoxPlot of FemaleTopQuartile against Region
fig11 = plt.subplots()
ax11 = sns.boxplot(data=df_visualization, y="FemaleTopQuartile", x="UK region")
ax11.set(ylim=(-200, 200))
ax11.tick_params(axis='x', labelrotation=90)
ax11.set_title('BoxPlot of FemaleTopQuartile against Region')

```

</p>
</details>
