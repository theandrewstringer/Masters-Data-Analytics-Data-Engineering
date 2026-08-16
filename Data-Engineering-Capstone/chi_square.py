import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association

# load the cleaned data into a dataframe
df = pd.read_csv('clean_data.csv')

# use a loop to make a significance table
target = 'readmitted'
predictors = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
              'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide',
              'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone',
              'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin',
              'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone',
              'metformin-pioglitazone', 'change', 'diabetesMed']
results = []

for col in predictors:
    contingency_table = pd.crosstab(df[col], df[target])
    chi2, p, dof, ex = chi2_contingency(contingency_table)
    v = association(contingency_table, method = 'cramer')
    results.append({
        'Variable': col,
        'P-Value': p,
        'Cramer V': v,
        'Significance': p < (0.05 / 25)
    })

# convert to a dataframe and sort by cramer's v
df_results = pd.DataFrame(results).sort_values(by = 'Cramer V', ascending = False)

# view the dataframe
print(df_results)

# set visual style
sn.set_theme(style = 'whitegrid')
plt.figure(figsize = (10, 8))

# create a barplot
plot = sn.barplot(
    x = 'Cramer V',
    y = 'Variable',
    data = df_results,
    palette = 'viridis'
)

# labels and title
plt.title('Feature Importance (Cramer\'s V)', fontsize = 16)
plt.xlabel('Cramer\'s V', fontsize = 12)
plt.ylabel('Predictor Variables', fontsize = 12)
plt.tight_layout()
plt.show()