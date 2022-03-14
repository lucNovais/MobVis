import time

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        exec = func(*args, **kwargs)
        end = time.time()
        totalTime = end - start
        print(f'\nElapsed time: {totalTime} seconds.\n')
        return exec
    return wrapper