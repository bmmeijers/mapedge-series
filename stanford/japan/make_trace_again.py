import glob
import os

# from the fitting of the annotation, these will not work for sure
# lines = """WARNING: bk474pr1090_00_0001 *not* enough GCPs
# WARNING: bm243ms1445_00_0001 *not* enough GCPs
# WARNING: bs659ff3817_00_0001 *not* enough GCPs
# WARNING: cf455dg4393_00_0001 *not* enough GCPs
# WARNING: cg028df0608_00_0001 *not* enough GCPs
# WARNING: cg144rh3894_00_0001 *not* enough GCPs
# WARNING: ch247vx7501_00_0001 *not* enough GCPs
# WARNING: cj422fk7676_00_0001 *not* enough GCPs
# WARNING: cn662mb2746_00_0001 *not* enough GCPs
# WARNING: cs054qt7813_00_0001 *not* enough GCPs
# WARNING: ct580jc6541_00_0001 *not* enough GCPs
# WARNING: cv223yw9621_00_0001 *not* enough GCPs
# WARNING: cx143gy5368_00_0001 *not* enough GCPs
# WARNING: cx337vv9099_00_0001 *not* enough GCPs
# WARNING: cz899gh9732_00_0001 *not* enough GCPs
# WARNING: dh828tc1188_00_0001 *not* enough GCPs
# WARNING: dk314vm7779_00_0001 *not* enough GCPs
# WARNING: dk361jr7644_00_0001 *not* enough GCPs
# WARNING: dp987tm2672_00_0001 *not* enough GCPs
# WARNING: dr618gr2072_00_0001 *not* enough GCPs
# WARNING: dv138fz3472_00_0001 *not* enough GCPs
# WARNING: dv359zk3610_00_0001 *not* enough GCPs
# WARNING: fc037kd5747_00_0001 *not* enough GCPs
# WARNING: fg106xz0738_00_0001 *not* enough GCPs
# WARNING: fg600ph4255_00_0001 *not* enough GCPs
# WARNING: fm352vv6659_00_0001 *not* enough GCPs
# WARNING: fp214tk0767_00_0001 *not* enough GCPs
# WARNING: fs409zn9131_00_0001 *not* enough GCPs
# WARNING: fs463gs0397_00_0001 *not* enough GCPs
# WARNING: ft438ns7558_00_0001 *not* enough GCPs
# WARNING: fx828qq3836_00_0001 *not* enough GCPs
# WARNING: gc656yb9866_00_0001 *not* enough GCPs
# WARNING: gh175dc4875_00_0001 *not* enough GCPs
# WARNING: gr186rh7096_00_0001 *not* enough GCPs
# WARNING: gx447nv1382_00_0001 *not* enough GCPs
# WARNING: gy024nh9204_00_0001 *not* enough GCPs
# WARNING: gz075hk1539_00_0001 *not* enough GCPs
# WARNING: hh507xx6546_00_0001 *not* enough GCPs
# WARNING: hk968xp6833_00_0001 *not* enough GCPs
# WARNING: hn424kr6627_00_0001 *not* enough GCPs
# WARNING: hp697dv0694_00_0001 *not* enough GCPs
# WARNING: hr248zq2387_00_0001 *not* enough GCPs
# WARNING: hx768vg9934_00_0001 *not* enough GCPs
# WARNING: jc904jt1675_00_0001 *not* enough GCPs
# WARNING: jc924rf0932_00_0001 *not* enough GCPs
# WARNING: jx424pb5108_00_0001 *not* enough GCPs
# WARNING: jz913np7995_00_0001 *not* enough GCPs
# WARNING: kc798mf1081_00_0001 *not* enough GCPs
# WARNING: my682qf7398_00_0001 *not* enough GCPs
# WARNING: nd924vn8802_00_0001 *not* enough GCPs
# WARNING: nz897nd6779_00_0001 *not* enough GCPs
# WARNING: pb426mk7540_00_0001 *not* enough GCPs
# WARNING: ph299bg5284_00_0001 *not* enough GCPs
# WARNING: pp034hs6992_00_0001 *not* enough GCPs
# WARNING: ps291sf2151_00_0001 *not* enough GCPs
# WARNING: ps894tm2957_00_0001 *not* enough GCPs
# WARNING: pw419ks3920_00_0001 *not* enough GCPs
# WARNING: qh269yy5828_00_0001 *not* enough GCPs
# WARNING: qj416gs4700_00_0001 *not* enough GCPs
# WARNING: qy602yr2850_00_0001 *not* enough GCPs
# WARNING: rf724qt0024_00_0001 *not* enough GCPs
# WARNING: ry529fz2101_00_0001 *not* enough GCPs
# WARNING: sc758qq3548_00_0001 *not* enough GCPs
# WARNING: sf718sg6263_00_0001 *not* enough GCPs
# WARNING: sk001gh2258_00_0001 *not* enough GCPs
# WARNING: sq842dx6340_00_0001 *not* enough GCPs
# WARNING: sr082bp9988_00_0001 *not* enough GCPs
# WARNING: ss686hg9899_00_0001 *not* enough GCPs
# WARNING: sy953kp6030_00_0001 *not* enough GCPs
# WARNING: td541nx4976_00_0001 *not* enough GCPs
# WARNING: tq652gg2776_00_0001 *not* enough GCPs
# WARNING: tq896wh6400_00_0001 *not* enough GCPs
# WARNING: ts752nm3363_00_0001 *not* enough GCPs
# WARNING: vb038hr7092_00_0001 *not* enough GCPs
# WARNING: vc316sh0555_00_0001 *not* enough GCPs
# WARNING: vc391bq0493_00_0001 *not* enough GCPs
# WARNING: vd420js0307_00_0001 *not* enough GCPs
# WARNING: vk991tc1398_00_0001 *not* enough GCPs
# WARNING: vs136sz1185_00_0001 *not* enough GCPs
# WARNING: vt079fg8765_00_0001 *not* enough GCPs
# WARNING: vv105qp3962_00_0001 *not* enough GCPs
# WARNING: wb331cc0063_00_0001 *not* enough GCPs
# WARNING: wc926bq3228_00_0001 *not* enough GCPs
# WARNING: wg393yn4261_00_0001 *not* enough GCPs
# WARNING: wh744gc9157_00_0001 *not* enough GCPs
# WARNING: wj252dn6880_00_0001 *not* enough GCPs
# WARNING: wn422jc0584_00_0001 *not* enough GCPs
# WARNING: wr512rp0028_00_0001 *not* enough GCPs
# WARNING: wv378vq3043_00_0001 *not* enough GCPs
# WARNING: ww637df6344_00_0001 *not* enough GCPs
# WARNING: wx843rc4982_00_0001 *not* enough GCPs
# WARNING: wz728bt5394_00_0001 *not* enough GCPs
# WARNING: xm969vd7626_00_0001 *not* enough GCPs
# WARNING: xs148yj3465_00_0001 *not* enough GCPs
# WARNING: xt994dv1395_00_0001 *not* enough GCPs
# WARNING: xv324bq8642_00_0001 *not* enough GCPs
# WARNING: yd639hn9787_00_0001 *not* enough GCPs
# WARNING: zp862kw2830_00_0001 *not* enough GCPs
# WARNING: zr108wb8770_00_0001 *not* enough GCPs
# WARNING: zw720zq8756_00_0001 *not* enough GCPs
# WARNING: zx949pq9528_00_0001 *not* enough GCPs
# """

# lines = """WARNING: bs659ff3817_00_0001 *not* enough GCPs
# WARNING: cg028df0608_00_0001 *not* enough GCPs
# WARNING: cs054qt7813_00_0001 *not* enough GCPs
# WARNING: dv359zk3610_00_0001 *not* enough GCPs
# WARNING: fc037kd5747_00_0001 *not* enough GCPs
# WARNING: fg106xz0738_00_0001 *not* enough GCPs
# WARNING: fg600ph4255_00_0001 *not* enough GCPs
# WARNING: fs409zn9131_00_0001 *not* enough GCPs
# WARNING: ft438ns7558_00_0001 *not* enough GCPs
# WARNING: fx828qq3836_00_0001 *not* enough GCPs
# WARNING: gh175dc4875_00_0001 *not* enough GCPs
# WARNING: gr186rh7096_00_0001 *not* enough GCPs
# WARNING: hn424kr6627_00_0001 *not* enough GCPs
# WARNING: jc904jt1675_00_0001 *not* enough GCPs
# WARNING: nd924vn8802_00_0001 *not* enough GCPs
# WARNING: ph299bg5284_00_0001 *not* enough GCPs
# WARNING: qj416gs4700_00_0001 *not* enough GCPs
# WARNING: sc758qq3548_00_0001 *not* enough GCPs
# WARNING: sr082bp9988_00_0001 *not* enough GCPs
# WARNING: sy953kp6030_00_0001 *not* enough GCPs
# WARNING: td541nx4976_00_0001 *not* enough GCPs
# WARNING: tq652gg2776_00_0001 *not* enough GCPs
# WARNING: vc391bq0493_00_0001 *not* enough GCPs
# WARNING: vd420js0307_00_0001 *not* enough GCPs
# WARNING: wb331cc0063_00_0001 *not* enough GCPs
# WARNING: wj252dn6880_00_0001 *not* enough GCPs
# WARNING: wr512rp0028_00_0001 *not* enough GCPs
# WARNING: wv378vq3043_00_0001 *not* enough GCPs
# WARNING: ww637df6344_00_0001 *not* enough GCPs
# WARNING: wz728bt5394_00_0001 *not* enough GCPs
# WARNING: xv324bq8642_00_0001 *not* enough GCPs
# """

lines = """WARNING: dv359zk3610_00_0001 *not* enough GCPs
WARNING: fg106xz0738_00_0001 *not* enough GCPs
WARNING: fg600ph4255_00_0001 *not* enough GCPs
WARNING: fx828qq3836_00_0001 *not* enough GCPs
WARNING: gh175dc4875_00_0001 *not* enough GCPs
WARNING: gr186rh7096_00_0001 *not* enough GCPs
WARNING: ph299bg5284_00_0001 *not* enough GCPs
WARNING: sc758qq3548_00_0001 *not* enough GCPs
WARNING: sr082bp9988_00_0001 *not* enough GCPs
WARNING: td541nx4976_00_0001 *not* enough GCPs
WARNING: vc391bq0493_00_0001 *not* enough GCPs
WARNING: vd420js0307_00_0001 *not* enough GCPs
WARNING: wb331cc0063_00_0001 *not* enough GCPs
WARNING: wj252dn6880_00_0001 *not* enough GCPs
WARNING: wr512rp0028_00_0001 *not* enough GCPs
WARNING: ww637df6344_00_0001 *not* enough GCPs
WARNING: wz728bt5394_00_0001 *not* enough GCPs
WARNING: xv324bq8642_00_0001 *not* enough GCPs
"""

oids = set(
    [line.strip().split(" ")[1].split("_")[0] for line in lines.split("\n") if line]
)

lines = """
bb610rn9916
bc475fy6710
bd534br4474
bf035mm2865
bf521rj9095
bg266px5594
bm287tf8360
bn687pt1869
bn722qm7677
bp230ng0408
bv215mm7252
bx561dj9658
bz237rq0572
cb173fj2995
cd377rd2504
ch508vw8100
ck394yd1365
cn155wy0239
cq918mr2233
cx422vn9780
cz998dn0802
dc268zt2002
dd611tc7884
dq152bx3663
dv138fz3472
dx090qz9203
dx890wh1783
dy180pj3311
dy941bm7042
dz131vn4639
ff922xr7550
fg106xz0738
fj251ph3384
fk351yv1204
fk820kw2643
fm352vv6659
fn681yy4919
ft261yx3353
fx428bn1290
gc571kz4633
gf777px5568
gg326xf0393
gg525kb3689
gk727by9852
gm548nc1887
gn173yc7489
gn683ty3190
gq081mq0241
gq325rd4323
gt791qw9320
gx840fj5065
hb301fq3933
hc989qx1047
hh236wr1686
hk399qf4067
hn424kr6627
hn829vx5167
hp111gs7027
hv049td1033
hw356hv7926
hx474kc9906
hy867pm7115
hz197pz8951
jc924rf0932
jd063zp3322
jg107yb2606
jg430nr1311
jh185cm6565
jk153sr9922
jk746vc9948
jm091qy9409
jm604pp0444
jp783cy0419
jr431yq4417
jv264cr9624
jv873fx6370
jw276cc9711
jx424pb5108
kg387mv8230
km955cm6597
kp217wb3102
ks156vs1610
ks453fg5171
kv323jy3525
kw217kb0117
ky299cf5346
mf036js1377
mj419xx5288
mp513gv8304
mp609jy8941
mq476jd7459
mq905sd7415
ms114ff9645
ng613ms8905
nh074mg3020
np019gh4673
nq509ns3097
ns269cv9086
ns533sh2523
ns602nx0395
nt411jx2072
nt584cc6369
nx724rb4831
nz493ys3646
nz723dc3368
nz897nd6779
pb787th5462
pb814kz7539
pc233kq4590
pg771fj4778
pj696jc4434
pk908wr5559
pt232ny4527
pw419ks3920
py079hb0288
py134jm7413
py949bw6898
pz862py0420
qb940md1743
qd009ct5259
qd876zd6739
qh771mm1777
qt180bt6568
qx197rw0921
rf724qt0024
rm830hx3210
rp293sn5184
rp834zx4717
rq552hd6282
rt246cm2336
rt334gs5040
rv108zz9254
rx020vy8442
rx428cc0233
rx893jp3821
ry093tf6718
sb883sp1598
sd381zq7692
sf163ph2995
sh039dd3025
sk712hb2764
sn317zs6633
sn519fw2715
sn565wj3739
sp940mt8807
sr082bp9988
ss018bw2455
sv729jg9962
tb318ym3123
tb462cc5639
tc192qz6527
tc967wq6930
tq565mh3570
tr780kv5299
ts241qt7878
tt234py1601
tv495qj7973
tv980hm6236
ty095jb8760
ty772gg4081
tz372zz8872
vc230qc0458
vd614sb6922
vk864nf9624
vm541xg9382
vp260rp3728
vq340zj2486
vs715qv6056
vt525bq0826
vw260hn9554
vy926bz4283
wd606ws0671
wd753ff4686
wh561md4470
wk412nf2957
wn604jm6763
wq547bq0140
wq772gb1819
ws202nh2045
ws630wb3843
ws785xg5624
wx690rr4410
wx843rc4982
wz108jn6283
xh534yt6111
xj296tg8907
xm591xf2630
xp912ry0126
xs148yj3465
xs555hq7820
xt994dv1395
xv324bq8642
xv948np1580
xw039np9324
xy660hf1402
xz446tr5065
yg404zy4688
yh267qw3290
yr360vn7341
yr749rh9869
yw196gn1627
yw499gp9137
zc089kv5918
zg682bq6104
zm115yt2020
zn547kg3314
zp462mf5577
zp862kw2830
zt926mp2020
zy137xp9883
zz189fv4341
"""


oids = set([line.strip() for line in lines.split("\n") if line])

with open("1trace_again_lt5.sh", "w") as fh:
    # print('date +"%Y-%m-%dT%H:%M:%S%z" > time.txt', file=fh)
    for id, filename in enumerate(
        sorted(glob.glob("/scratch/iiif_cache/japan/*.json"))
    ):
        # if id >= 55:
        base = os.path.basename(filename).replace(".json", "")
        if base in oids:
            print(
                f"mapedge trace -s ./series/stanford/japan/default.json -s ./series/stanford/japan/smaller_layout.json {filename} {id} -i -d",
                file=fh,
            )
            # print('date +"%Y-%m-%dT%H:%M:%S%z" >> time.txt', file=fh)
