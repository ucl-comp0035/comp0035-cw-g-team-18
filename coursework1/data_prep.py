import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# Load initial datasets
# https://gender-pay-gap.service.gov.uk/viewing/download
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

# Delete unnecessary columns
df_merge.drop(['Address', 'EmployerName', 'EmployerId', 'CompanyNumber', 'CompanyLinkToGPGInfo',
               'ResponsiblePerson', 'CurrentName', 'SubmittedAfterTheDeadline',
               'DueDate', 'DateSubmitted'], axis=1, inplace=True)
print(df_merge.shape, df_merge.columns)

# Check null values
print(df_merge.isnull().sum())

# Show correlations
pd.set_option('display.max_columns', None)
print(df_merge.corr())
ax = sns.heatmap(df_merge.corr(), linewidth=0.5)
plt.show()

# Deal with null values
df_merge = df_merge.dropna(subset=['MaleLowerQuartile', 'SicCodes', 'PostCode'])
print(df_merge.shape, df_merge.columns, df_merge.isnull().sum())
# Split the dataset into training and testing
df_merge_training = df_merge[df_merge['DiffMedianBonusPercent'].notnull()].dropna(subset=['DiffMeanBonusPercent'])
print(df_merge_training.shape, df_merge_training.columns, df_merge_training.isnull().sum())
df_merge_testing = df_merge[df_merge['DiffMedianBonusPercent'].isnull()]
print(df_merge_testing.shape, df_merge_testing.columns, df_merge_testing.isnull().sum())

# Train random forest regression model
# NOTE: This can quite slow, please wait
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

# Bind the two dataset together again
df_none_na = pd.concat([df_merge_training, df_merge_testing], axis=0)
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

# Deal with Postcode, SicCodes & EmployerSize
# Deal with Postcode
# Only keep outcode (before space)
df_none_na["PostCode"] = df_none_na["PostCode"].str.split().str[0]
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

# Load a dataframe explaining outcode in the UK
# https://www.doogal.co.uk/PostcodeDistricts
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

# Deal with SicCodes
df_none_na["SicCodes"] = df_none_na["SicCodes"].str.split(pat='\n').str[-1]
print(df_none_na.shape, df_none_na.columns, df_none_na.isnull().sum(), df_none_na.head(5))

# https://resources.companieshouse.gov.uk/sic/
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

# Deal with EmployerSize
print(df_none_na.EmployerSize.value_counts())
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

# Export .csv file
df_none_na.to_csv('gender_pay_gap_prepared.csv')

# Data Visualization
df_visualization = pd.read_csv('gender_pay_gap_prepared.csv')
df_visualization.drop(['Unnamed: 0', 'PostCode', 'SicCodes', 'EmployerSize'], axis=1, inplace=True)
print(df_visualization.shape, df_visualization.columns, df_visualization.isnull().sum(), df_visualization.head(5))
pd.set_option('display.max_columns', None)
print(df_visualization.describe())

# Plot graphs
# Plot1: Histogram on DiffMeanHourly Percent
fig1, ax1 = plt.subplots()
ax1.set_title('Distribution of DiffMeanHourlyPercent')
ax1.hist(df_visualization[['DiffMeanHourlyPercent']], bins=50)

# Plot2: Histogram on DiffMedianHourly Percent
fig2, ax2 = plt.subplots()
ax2.set_title('Distribution of DiffMedianHourlyPercent')
ax2.hist(df_visualization[['DiffMedianHourlyPercent']], bins=50)

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

plt.show()