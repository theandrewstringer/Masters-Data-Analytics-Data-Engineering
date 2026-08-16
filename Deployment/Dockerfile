# image recommended in the class resources
FROM python:3.12.1-slim

# set the working directory
WORKDIR /Users/andrewstringer/School/d602/task_3/d602_task_3_code

# copy the requirements and then install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code
COPY . .

# expose port
EXPOSE 8000

# run the app
CMD ["uvicorn", "api_v2:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]