import glob
import json
import matplotlib.pyplot as plt

pattern = "/scratch/iiif_inspect/japan/*.json"
pattern = "/tmp/corners/*.json"
# T, B, L, R = [], [], [], []


## The map frame their sizes for the whole series
W, H = [], []
for filename in glob.glob(pattern):

    with open(filename) as fh:
        try:
            J = json.load(fh)
            print(J.keys())
            wide = J["image_size"][0]
            s = 1024.0 / wide
            xs = [pt[0] for pt in J["corners"]["pixel_corner_points"]]
            ys = [pt[1] for pt in J["corners"]["pixel_corner_points"]]
            if xs:
                left = list(filter(lambda x: x >= 0, [xs[0], xs[3]]))
                # left = xs[0] * s, xs[3] * s
                # right = xs[1] * s, xs[2] * s

                left = xs[0] * 0.5 + xs[3] * 0.5
                right = xs[1] * 0.5 + xs[2] * 0.5

                W.append(right - left)

                # L.extend(left)
                # R.extend(right)
            if ys:

                # bottom = ys[0] * s, ys[1] * s
                # top = ys[2] * s, ys[3] * s

                bottom = ys[0] * 0.5 + ys[1] * 0.5
                top = ys[2] * s + ys[3] * 0.5

                H.append(bottom - top)
                # B.extend(bottom)
                # T.extend(top)

        except json.decoder.JSONDecodeError:
            print("JSON ERROR in: ", filename)
            pass


# def div1024(l):
#     return [el / 1024.0 for el in l]


# for side in list(map(div1024, (T, B, L, R))):
# for side in (L, R):
for side, name in zip([W, H], ["w", "h"]):
    plt.hist(side, bins=100, alpha=0.5, label=name)  # , range=[0, 1024])
plt.legend()
plt.show()
