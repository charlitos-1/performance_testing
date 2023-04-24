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


def function_performance(func):
    """ Decorator function. Used to print out function runtime and peak memory usage during execution. """

    def memory_usage_wrapper(*args, **kwargs):
        if not function_performance.tracemalloc_running:
            tracemalloc.start()
            function_performance.tracemalloc_running = True

        current_memory_usage, peak_memory_usage = tracemalloc.get_traced_memory()
        function_performance.memory_stack.append(current_memory_usage)
        
        t_start = time.perf_counter()

        return_value = func(*args, **kwargs)

        t_elapsed = time.perf_counter() - t_start
        
        current_memory_usage, peak_memory_usage = tracemalloc.get_traced_memory()
        peak_memory_usage -= function_performance.memory_stack.pop()

        if not function_performance.memory_stack:
            tracemalloc.stop()
            function_performance.tracemalloc_running = False

        print()
        print(f"Function: {func.__name__}")
        print(f"\tPositional Arguments: {args}")
        print(f"\tKey Word Arguments: {kwargs}")
        print()
        print(f"\tReturn Value: {return_value}")
        print()
        print(f"\tPeak Memory Usage: {bytes_conversion(peak_memory_usage)}")
        print(f"\tRuntime: {seconds_conversion(t_elapsed)}")

        return return_value

    return memory_usage_wrapper


# static variables for memory_usage wrapper
function_performance.tracemalloc_running = False
function_performance.memory_stack = []

if __name__ == "__main__":
    pass
