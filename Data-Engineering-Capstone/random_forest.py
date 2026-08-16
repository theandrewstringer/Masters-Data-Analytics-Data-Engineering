import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

# load the cleaned data into a dataframe
df = pd.read_csv('clean_data.csv')

# create list of columns to drop
cols_range = df.loc[:, 'readmitted':'A1C_test_performed'].columns.tolist()
identifier_cols = ['encounter_id', 'patient_nbr']

# drop all of the columns in the list
df_encoded = df.drop(columns = cols_range + identifier_cols)

# define target and predictors
X = df_encoded.drop(columns = ['readmitted_under_30'])
y = df_encoded['readmitted_under_30']

# one-hot encode categorical features
X = pd.get_dummies(X, drop_first = True)

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

# fit random forest
rf = RandomForestClassifier(
    n_estimators = 500,
    max_depth = None,
    class_weight = 'balanced',
    random_state = 42
)
rf.fit(X_train, y_train)

# permutation feature importance
perm_importance = permutation_importance(
    rf,
    X_test,
    y_test,
    n_repeats = 20,
    random_state = 42,
    n_jobs = -1
)
importances = pd.Series(perm_importance.importances_mean, index = X.columns)
importances = importances.sort_values(ascending = False)
print('Top 20 Permutation Importances:')
print(importances.head(20))

# plot the top 20
plt.figure(figsize = (10, 6))
sn.barplot(x = importances.head(20), y = importances.head(20).index)
plt.title('Top 20 Permutation Feature Importances')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

# pick top 3 features for pdp
top_features = importances.head(3).index.tolist()
PartialDependenceDisplay.from_estimator(
    rf,
    X_test,
    features = top_features,
    kind = 'average',
    grid_resolution = 50
)
plt.suptitle('Partial Dependence Plots (Top Features)', y = 1.02)
plt.show()

# initialize shap explainer for tree-based model
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# plot summary
shap.summary_plot(shap_values[1], X_test, plot_type = 'bar')
shap.summary_plot(shap_values[1], X_test)