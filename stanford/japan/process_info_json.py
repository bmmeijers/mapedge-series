import glob
import json
import matplotlib.pyplot as plt

W, H = [], []
pattern = "/scratch/iiif_cache/japan/*.json"
for filename in glob.glob(pattern):

    with open(filename) as fh:
        try:
            J = json.load(fh)
            w, h = J["width"], J["height"]
            # s = w / 1024.0
            W.append(w * (1 / (w / 1024.0)))
            H.append(h * (1 / (w / 1024.0)))
            # W.append(w)
            # H.append(h)
        except json.decoder.JSONDecodeError:
            print("JSON ERROR in: ", filename)
            pass

print(W)
plt.boxplot([W, H])
# plt.hist(H, bins=100)
plt.show()
