import time


def seconds_conversion(seconds: float) -> str:
    """ Takes in a value in seconds and returns a formatted string value with appropriate units for the given amount of time. """

    try:
        seconds = float(seconds)
    except ValueError:
        return f"\nInvalid input. Expecting value in seconds. \n\tValue: {seconds}\n\tType: {type(seconds)}"

    if seconds <= 1:
        seconds_si_conversion = {
            0: "",
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


def func_info(func):
    """ Decorator function. Used to print out function name, arguments, return value, and elapsed time of a function. """

    def wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        return_value = func(*args, **kwargs)
        t_elapsed = time.perf_counter() - t_start

        print()
        print(f"Function: {func}")
        print(f"\tPositional Arguments: {args}")
        print(f"\tKey Word Arguments: {kwargs}")
        print(f"\tReturn value: {return_value}")
        print(f"\tRuntime: {seconds_conversion(t_elapsed)}")

        return return_value

    return wrapper


if __name__ == "__main__":
    pass
