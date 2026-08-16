# import packages
import subprocess

# call each script in order
subprocess.run(['python', 'import_and_format_complete.py'], check = True)
subprocess.run(['python', 'cleaning_data_complete.py'], check = True)
subprocess.run(['python', 'poly_regressor_Python_1.0.0.py'], check = True)