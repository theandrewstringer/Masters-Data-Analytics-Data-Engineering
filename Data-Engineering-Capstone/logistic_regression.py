import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# load the cleaned data into a dataframe
df = pd.read_csv('clean_data.csv')

# create list of columns to drop, leaving only encoded values
cols_range = df.loc[:, 'encounter_id':'readmitted'].columns.tolist()
cols_to_drop = cols_range + ['A1C_None']

# drop all of the columns in the list
df_encoded = df.drop(columns = cols_to_drop)

# type cast columns to int
df_encoded = df_encoded.astype(int)

# drop NaN and inf columns
X = df_encoded.drop(columns = ['readmitted_under_30'])
y = df_encoded['readmitted_under_30']
nan_cols = ['acetohexamide_encoded', 'troglitazone_encoded', 'examide_encoded', 'citoglipton_encoded']
inf_cols = ['A1C_test_performed']
X = X.drop(columns = nan_cols + inf_cols)

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

# calculate vif
vif = pd.DataFrame()
vif['feature'] = X_train.columns
vif['vif'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
print(vif.sort_values(by = 'vif', ascending = False))

# fit and predict
log_reg = LogisticRegression(solver = 'liblinear', class_weight = 'balanced', random_state = 42)
log_reg.fit(X_train, y_train)

# create a summary for readability and sort by impact
results = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': log_reg.coef_[0],
    'Odds Ratio': np.exp(log_reg.coef_[0])
})
print(results.sort_values(by = 'Odds Ratio', ascending = False))