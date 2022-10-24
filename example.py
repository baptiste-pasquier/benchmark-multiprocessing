import logging
import random

from benchmark_multiprocessing.bench import bench_function

logging.getLogger().setLevel(logging.INFO)


def function_A(arg1, arg2):
    return arg1**arg2


def function_B(arg1, arg2):
    result = None
    for _ in range(100):
        result = arg1**arg2
    return result


if __name__ == "__main__":

    CPUS_LIST = [
        1,
        2,
        3,
        4,
        6,
        8,
        10,
        12,
        14,
        16,
        20,
        24,
        28,
        32,
    ]

    N = 10000
    arg1_list = [random.randint(int(1e5), int(1e6)) for _ in range(N)]
    arg2_list = [random.randint(int(1e3), int(1e4)) for _ in range(N)]

    bench_function(function_A, "function_A", CPUS_LIST, arg1_list, arg2_list)

    N = 160
    arg1_list = [random.randint(int(1e5), int(1e6)) for _ in range(N)]
    arg2_list = [random.randint(int(1e3), int(1e4)) for _ in range(N)]

    bench_function(function_B, "function_B", CPUS_LIST, arg1_list, arg2_list)
