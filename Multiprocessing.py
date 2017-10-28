import multiprocessing  
from time import sleep 


def calculate(process_name, tasks, results):  
    print('[%s] evaluation routine starts' % process_name)

    while True:
        new_value = tasks.get()
        if new_value < 0:
            print('[%s] evaluation routine quits' % process_name)

            # Indicate finished
            results.put(-1)
            break
        else:
            # Compute result and mimic a long-running task
            compute = new_value * new_value
            sleep(60)

            # Output which process received the value
            # and the calculation result
            print('[%s] received value: %i' % (process_name, new_value))
            print('[%s] calculated value: %i' % (process_name, compute))

            # Add result to the queue
            results.put(compute)

    return 


if __name__ == "__main__":  
    # Define IPC manager
    manager = multiprocessing.Manager()

    # Define a list (queue) for tasks and computation results
    tasks = manager.Queue()
    results = manager.Queue()

    # Create process pool with four processes
    num_processes = 4  
    #pool = multiprocessing.Pool(processes=num_processes)  
   # processes = []
    

    for i in range(num_processes):

      # Set process name
      process_name = 'P%i' % i

      # Create the process, and connect it to the worker function
      new_process = multiprocessing.Process(target=calculate, args=(process_name,tasks,results))

      # Add new process to the list of processes
     # processes.append(new_process)

      # Start the process
      new_process.start()


# Fill task queue
task_list = [43, 1, 780, 256, 142, 68, 183, 334, 325, 3]  
for single_task in task_list:  
    tasks.put(single_task)
    print('single task {}'.format(single_task))

# Wait while the workers process
sleep(5)

# Quit the worker processes by sending them -1
#for i in range(num_processes):  
#    tasks.put(-1)

# Read calculation results
num_finished_processes = 0  
while True:  
    # Read result
    new_result = results.get()

    # Have a look at the results
    if new_result == -1:
        # Process has finished
        num_finished_processes += 1

        if num_finished_processes == num_processes:
            break
    else:
        # Output result
        print('Result:' + str(new_result))       