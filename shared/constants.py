import math

# topology constants
SIZEX, SIZEY = 4, 4
CORE_NUMBER = SIZEX * SIZEY
GRID_SIZE = [SIZEX, SIZEY]
GRID = []

# communication constants
#CLOCK_SPEED = 100000000 # this is seconds
CLOCK_SPEED = 100000 # milliseconds
LINK_LATENCY = 1.0 / CLOCK_SPEED
ROUTER_LATENCY = 1.0 / CLOCK_SPEED
FLIT_SIZE = 32

# task gen constants
NO_BENCHMARKS = 10
FOLDER_LOCATION = "benchmarks/"
FILE_NAME = "taskset"
EXTENSION = ".txt"
TASK_GEN_NUMBER = 32
MIN_PERIOD = 100
MAX_PERIOD = 200
MIN_COMP_TIME = 10
MAX_COMP_TIME = 40
MIN_MESSAGE_SIZE = 8  # this is 2 ** MIN_MESSAGE_SIZE so 2 ** 8 = 256
MAX_MESSAGE_SIZE = 12

BENCHMARK_FOLDER = "B1"
if "P" in BENCHMARK_FOLDER:
    BENCHMARK = "benchmarks/parameters/" + BENCHMARK_FOLDER + ".txt"
else:
    BENCHMARK = "benchmarks/experiment/" + BENCHMARK_FOLDER + ".txt"


