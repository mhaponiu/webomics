import random

FRAMES_ = 5000

def getExampleIntervals():
    testing_intervals = []
    for i in range(FRAMES_):
        start = random.randint(0, (i + 1) * 10000)
        stop = start + 1000000
        testing_intervals.append((start, stop))
    return testing_intervals

intervals = getExampleIntervals()
int_file = open("example_intervals_chr_3.csv", "w")
for inter in intervals:
    int_file.write(str(inter[0]) + "\t" + str(inter[1]) + "\n")
int_file.close()
