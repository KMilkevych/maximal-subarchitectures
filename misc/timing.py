# Helper function for timing actions
def time_it(fun):
    import time
    start_time = time.time()
    result = fun()
    return (result, time.time() - start_time)
