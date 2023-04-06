from concurrent.futures import ThreadPoolExecutor
 
def thread_pool(worker,worker_args:list)->list:
    # create a thread pool
    with ThreadPoolExecutor() as executor:
        # submit tasks and process results
        results=list(executor.map(worker, worker_args))
    return sum(results,[])