from multiprocessing import Pool
import multiprocessing
import pandas as pd
my_bucket = 'ws20-input'
import requests
import boto3

def save_asset_to_s3(process_name,tasts, results):
    data = tasks.get()
    download_url = data[0]
    file_name = data[1]
    file_download = requests.get(url = download_url)
    client = boto3.client('s3')
    client.put_object(Body=file_download.content, Bucket=my_bucket, Key=file_name)
    print( file_name + 'is finished')





manager = multiprocessing.Manager()

    # Define a list (queue) for tasks and computation results
tasks = manager.Queue()
results = manager.Queue()

num_processes = 10
pool = multiprocessing.Pool(processes=num_processes)
processes = []

for i in range(num_processes):

    # Set process name
    process_name = 'P%i' % i

    # Create the process, and connect it to the worker function
    new_process = multiprocessing.Process(target=save_asset_to_s3, args=(process_name, tasks, results))

    # Add new process to the list of processes
    processes.append(new_process)

    # Start the process
    new_process.start()

data = pd.read_csv('./final_list_friday.csv')
data = data[['download_link','file_name']].values.tolist()
task_list = data

for single_task in task_list:
    tasks.put(single_task)