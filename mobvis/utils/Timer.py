import time

def timed(func):
    """ Function that determines how long a method has been running.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        exec = func(*args, **kwargs)
        end = time.time()

        totalTime = end - start
        print(f'\nElapsed time: {totalTime} seconds.\n')
        
        return exec
    return wrapper
