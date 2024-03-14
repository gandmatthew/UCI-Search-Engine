import time

dev_path = "./DEV/"
partitions_path = "./partitions/"
indexes_path = "./indexes/"
word_threshold = 10000
threads = 10

# def message(*argv):
#     result = ""
#     for arg in argv:
#         t = str(arg)
#         result += f"{t} "
#     print(f'\033[\033[31m{result}\u001b[0m')

def log(*argv):
    result = ""
    current_time = time.ctime(time.time())

    for arg in argv:
        t = str(arg)
        result += f"{t} "
    with open("log.json", "a") as file:
        file.write(f"{current_time}: {result}\n")