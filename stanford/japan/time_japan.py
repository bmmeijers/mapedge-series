filename = "/home/martijn/Documents/work/2023-08_synthesis/mapedge/series/stanford/japan/time_all.txt"

with open(filename) as fh:
    times = fh.readlines()
import datetime

all_times = [
    datetime.datetime.fromisoformat(dt.strip().replace("+0200", "+02:00"))
    for dt in times
]

pairs = zip(all_times, all_times[1:])
# for start, end in pairs:
#     print((end - start).total_seconds())
durations = [(end - start).total_seconds() for start, end in pairs]

import matplotlib.pyplot as plt

# (we stopped the process once for 20mins, let's throw this out)
# keep only those runs under 120 seconds
plt.hist(list(filter(lambda x: x < 120, durations)), bins=20)
plt.show()
