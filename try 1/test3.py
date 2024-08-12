import os
import multiprocessing

# Method 1: Using os
cpu_count_os = os.cpu_count()
print(f"Number of CPUs using os module: {cpu_count_os}")

# Method 2: Using multiprocessing
cpu_count_mp = multiprocessing.cpu_count()
print(f"Number of CPUs using multiprocessing module: {cpu_count_mp}")
