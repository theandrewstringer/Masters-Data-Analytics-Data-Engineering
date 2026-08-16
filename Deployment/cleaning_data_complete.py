# import packages
import pandas as pd
import mlflow
import datetime

nowdate = datetime.date.today()
# creates an experiment name that changes every day
experiment_name = "Airport Departure Delays, experiment run on " + str(nowdate)
# creates new experiment if there is not one yet today, otherwise sets the experiment to the existing one for today
experiment = mlflow.set_experiment(experiment_name)
run_name = "Run started at " + datetime.datetime.now().strftime("%H:%M")

with mlflow.start_run(run_name = 'data_cleaning', nested = True):
    # read df from import_and_format_complete
    df = pd.read_pickle('filtered_data.pkl')

    # data type conversion dictionary
    conversion_map = {
        'YEAR': 'int',
        'MONTH': 'int',
        'DAY': 'int',
        'DAY_OF_WEEK': 'int',
        'ORG_AIRPORT': 'str',
        'DEST_AIRPORT': 'str',
        'SCHEDULED_DEPARTURE': 'int',
        'DEPARTURE_TIME': 'int',
        'DEPARTURE_DELAY': 'int',
        'SCHEDULED_ARRIVAL': 'int',
        'ARRIVAL_TIME': 'int',
        'ARRIVAL_DELAY': 'int'
    }

    # fill null values in departure_time, departure_delay, arrival_time, and arrival_delay
    # if departure_time or arrival_time is null, the flight left and arrived on time
    # when the flight leaves or arrives on time, the delay will be 0
    df['DEPARTURE_TIME'] = df['DEPARTURE_TIME'].fillna(df['SCHEDULED_DEPARTURE'])
    df['DEPARTURE_DELAY'] = df['DEPARTURE_DELAY'].fillna(0)
    df['ARRIVAL_TIME'] = df['ARRIVAL_TIME'].fillna(df['SCHEDULED_ARRIVAL'])
    df['ARRIVAL_DELAY'] = df['ARRIVAL_DELAY'].fillna(0)

    # convert the data types
    df_cleaned = df.astype(conversion_map)

    # log cleaned data as artifact
    mlflow.log_artifact('cleaned_data.csv')

    # export cleaned data to csv
    df_cleaned.to_csv('cleaned_data.csv', index = False)

print('Data cleaned and exported successfully.')