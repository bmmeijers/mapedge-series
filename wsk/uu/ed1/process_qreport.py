from csv import DictReader
from matplotlib import pyplot as plt
import numpy as np

D = []
U = []
with open("/tmp/report.csv") as fh:
    r = DictReader(fh)

    for item in r:
        print(item)
        dists = list([item[f"distance_{i}"] for i in range(6)])

        if "" in dists:
            continue
        else:
            dists = list(map(int, dists))
        print(dists)
        d = dists[0]
        D.append(d)
        U.append(item["uuid"])


# to_plot = list(filter(lambda x: 4500 < x < 4760, D))
# to_plot = list(filter(lambda x: 5500 < x < 5800, D))
to_plot = np.array(D)
uuid = np.array(U)

match_indices = []
for i, x in enumerate(D):
    if 4500 > x or x > 4760:
        match_indices.append(i)

print(to_plot[match_indices])
print(uuid[match_indices])

avg = np.average(to_plot)
std = np.std(to_plot)
print(avg)
print(std)

plt.hist(to_plot[match_indices], bins=100)
plt.show()
