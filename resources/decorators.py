import time
import tracemalloc


def seconds_conversion(seconds: float) -> str:
    """ Takes in a value in seconds and returns a formatted string value with appropriate units for the given amount of time. """

    try:
        seconds = float(seconds)
    except ValueError:
        return f"\nInvalid input. Expecting value in seconds. \n\tValue: {seconds}\n\tType: {type(seconds)}"

    if seconds <= 1:
        seconds_si_conversion = {
            0: "seconds",
            1: "miliseconds",
            2: "microseconds",
            3: "nanoseconds",
            4: "picoseconds",
        }
        thousandths = 0
        while seconds < 1 and thousandths < max(seconds_si_conversion.keys()):
            seconds *= 1000
            thousandths += 1
        seconds = round(seconds, 3)
        return f"{seconds} {seconds_si_conversion.get(thousandths)}"

    else:
        seconds = round(seconds, 3)
        if seconds < 60:
            return f"{seconds} seconds"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%d:%02d:%02d" % (hours, minutes, seconds)


def timeit(func):
    """ Decorator function. Used to print out function name, arguments, return value, and elapsed time of a function. """

    def timeit_wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        return_value = func(*args, **kwargs)
        t_elapsed = time.perf_counter() - t_start

        print()
        print(f"Function: {func.__name__}")
        print(f"\tPositional Arguments: {args}")
        print(f"\tKey Word Arguments: {kwargs}")
        print(f"\tReturn Value: {return_value}")
        print(f"\tRuntime: {seconds_conversion(t_elapsed)}")

        return return_value

    return timeit_wrapper


def bytes_conversion(bytes):
    bytes_si_conversion = {
        0: "b",
        1: "kb",
        2: "mb",
        3: "gb",
        4: "tb",
    }
    thousands = 0
    while bytes > 1000 and thousands < max(bytes_si_conversion.keys()):
        bytes /= 1000
        thousands += 1
    bytes = round(bytes, 3)
    return f"{bytes} {bytes_si_conversion.get(thousands)}"


def memory_usage(func):
    """ Decorator function. Used to print out function name, and the peak memory usage during the function execution. """

    def memory_usage_wrapper(*args, **kwargs):
        if not memory_usage.tracemalloc_running:
            tracemalloc.start()
            memory_usage.tracemalloc_running = True

        current_memory_usage, peak_memory_usage = tracemalloc.get_traced_memory()
        memory_usage.memory_stack.append(current_memory_usage)
        return_value = func(*args, **kwargs)
        current_memory_usage, peak_memory_usage = tracemalloc.get_traced_memory()
        peak_memory_usage -= memory_usage.memory_stack.pop()

        if not memory_usage.memory_stack:
            tracemalloc.stop()
            memory_usage.tracemalloc_running = False

        print()
        print(f"Function: {func.__name__}")
        print(f"\tPeak Memory Usage: {bytes_conversion(peak_memory_usage)}")

        return return_value

    return memory_usage_wrapper


# static variables for memory_usage wrapper
memory_usage.tracemalloc_running = False
memory_usage.memory_stack = []


if __name__ == "__main__":
    pass
