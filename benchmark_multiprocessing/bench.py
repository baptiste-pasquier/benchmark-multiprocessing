import logging
import platform
import time
from datetime import datetime
from multiprocessing import Pool

import matplotlib.pyplot as plt
import pandas as pd
from p_tqdm import p_map, p_umap
from tqdm.auto import tqdm


def bench_function(function, function_name, cpus_list, *args):
    """Benchmark of a function with different multiprocessing methods.

    Args:
        function (func): function to test
        function_name (str) : name of the function
        cpus_list (list[int]): numbers of cpus to test in multiprocessing
        *args (list): list of arguments to pass to the function
    """

    logging.info(f"Start benchmarking {function_name}")

    t0 = datetime.now()

    t1 = time.time()
    true_result = list(map(function, *args))
    t2 = time.time()

    d_time_map = t2 - t1
    speed_map = len(true_result) / d_time_map

    df = []

    for method in tqdm(
        [
            "Pool",
            "p_map",
            "p_umap",
        ]
    ):
        for num_cpus in tqdm(cpus_list):
            t3 = time.time()
            result = None
            if method == "Pool":
                with Pool(num_cpus) as p:
                    result = p.starmap(function, zip(*args))
            elif method == "p_map":
                result = p_map(function, *args, num_cpus=num_cpus, leave=False)
            elif method == "p_umap":
                result = p_umap(function, *args, num_cpus=num_cpus, leave=False)
            t4 = time.time()

            if method in ["Pool", "p_map"]:
                assert result == true_result

            d_time = t4 - t3
            speed = len(true_result) / d_time

            data = {}
            data["method"] = method
            data["num_cpus"] = num_cpus
            data["time"] = d_time
            data["speed"] = speed
            df.append(data)

    logging.info(f"Total duration : {datetime.now() - t0}")

    df = pd.DataFrame(df)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    for method in df["method"].unique():
        ax[0].plot(
            df[df["method"] == method]["num_cpus"],
            df[df["method"] == method]["time"],
            marker="o",
            label=method,
        )
        ax[1].plot(
            df[df["method"] == method]["num_cpus"],
            df[df["method"] == method]["speed"],
            marker="o",
            label=method,
        )

    ax[0].axhline(d_time_map, color="red", label="map")
    ax[1].axhline(speed_map, color="red", label="map")
    ax[0].set_ylabel("time (s)")
    ax[1].set_ylabel("speed (it/s)")
    for i in [0, 1]:
        ax[i].set_xlabel("num_cpus")
        ax[i].grid()
        ax[i].legend()

    fig.suptitle(f"Benchmark of {function_name} on {platform.system()}")
    fig.tight_layout()

    plt.savefig(
        f"data/{function_name} - {platform.system()} - {datetime.now().strftime('%Y.%m.%d %H-%M-%S')}.png"
    )
    plt.show()
