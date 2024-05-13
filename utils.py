from time import time

def timer(func):
    #Decorator to measure execution time of a function
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s', flush=True)
        return result
    return wrap_func

def print_status(message, status="in progress"):
    border = "=" * 20
    if status == "in progress":
        print(f"\n{border}\n{message}...\n{border}\n", flush=True)
    elif status == "completed":
        print(f"\n{border}\n{message} without error!\n{border}", flush=True)

def handle_errors(e):
    print(f'Encountered Error: {e}', flush=True)
