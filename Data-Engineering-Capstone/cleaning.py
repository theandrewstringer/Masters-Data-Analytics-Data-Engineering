import pandas as pd

# load the dataset, and keep none from being read as null
df = pd.read_csv('diabetic_data.csv', keep_default_na = False)

# drop columns that will not be needed
drop_col = ['race', 'gender', 'age', 'weight', 'admission_type_id', 'discharge_disposition_id',
            'admission_source_id', 'time_in_hospital', 'payer_code', 'medical_specialty', 'num_lab_procedures',
            'num_procedures', 'num_medications', 'number_outpatient', 'number_emergency', 'number_inpatient',
            'diag_1', 'diag_2', 'diag_3', 'number_diagnoses', 'max_glu_serum']
df_reduced = df.drop(columns = drop_col)

# create list of medications for encoding
medications = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide',
            'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol',
            'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin',
            'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone']

# create a loop to encode any medications being taken into 1 and create new columns for them
for col in medications:
    new_col_name = f'{col}_encoded'
    df_reduced[new_col_name] = df_reduced[col].apply(lambda x: 0 if x == 'No' else 1)

# check if an a1c test was performed and if so, make it a 1
df_reduced['A1C_test_performed'] = df_reduced['A1Cresult'].apply(lambda x: 0 if x == 'None' else 1)

# create dummy variables for a1c result
df_reduced = pd.get_dummies(df_reduced, columns = ['A1Cresult'], prefix = 'A1C')

# create readmitted_under_30 column for analysis
df_reduced['readmitted_under_30'] = (df_reduced['readmitted'] == '<30').astype(int)

# create change_enc for analysis
df_reduced['change_enc'] = (df_reduced['change'] == 'Ch').astype(int)

# verify columns
df_reduced.info()

# export cleaned data set for deliverables
df_reduced.to_csv('clean_data.csv', index = False)