# import package
import pandas as pd
import mlflow
import datetime

nowdate = datetime.date.today()
# creates an experiment name that changes every day
experiment_name = "Airport Departure Delays, experiment run on " + str(nowdate)
# creates new experiment if there is not one yet today, otherwise sets the experiment to the existing one for today
experiment = mlflow.set_experiment(experiment_name)
run_name = "Run started at " + datetime.datetime.now().strftime("%H:%M")

with mlflow.start_run(run_name = 'import_and_format', nested = True):
    # file path
    path = 'T_ONTIME_REPORTING.csv'
    
    # original columns to use
    columns_original = ['YEAR', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'ORIGIN',
             'DEST', 'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY', 'CRS_ARR_TIME',
             'ARR_TIME', 'ARR_DELAY']

    # dictionary to map names
    columns_map = {
        'DAY_OF_MONTH': 'DAY',
        'ORIGIN': 'ORG_AIRPORT',
        'DEST': 'DEST_AIRPORT',
        'CRS_DEP_TIME': 'SCHEDULED_DEPARTURE',
        'DEP_TIME': 'DEPARTURE_TIME',
        'DEP_DELAY': 'DEPARTURE_DELAY',
        'CRS_ARR_TIME': 'SCHEDULED_ARRIVAL',
        'ARR_TIME': 'ARRIVAL_TIME',
        'ARR_DELAY': 'ARRIVAL_DELAY'
    }

    # import data and only use needed columns
    df = pd.read_csv(path, usecols = columns_original)

    # log the raw file as an artifact
    mlflow.log_artifact('T_ONTIME_REPORTING.csv')

    # log row and column count as parameters
    mlflow.log_param('original_rows', df.shape[0])
    mlflow.log_param('original_cols', df.shape[1])

    # filter for only atl flights
    df = df[df['ORIGIN'] == 'ATL']

    # log row count after filtering for atl as parameter
    mlflow.log_param('filtered_rows', df.shape[0])

    # read the csv and then rename columns
    df = df.rename(columns = columns_map)

    # save the df for cleaning
    df.to_pickle('filtered_data.pkl')

    # export the filtered csv
    df.to_csv('filtered_data.csv', index = False)

print('Data imported and filtered succesfully.')