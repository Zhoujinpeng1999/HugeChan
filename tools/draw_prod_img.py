from draw.painter import Painter
import os

def Run():
    pt = Painter()
    real_path = os.path.dirname(os.path.realpath(__file__))
    with open("{}/source.txt".format(real_path), "r") as f:
        mode = 0
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "----------":
                mode = 1
                continue
            if mode == 0:
                # point mode
                line = line.split(",")
                pt.AddNode(line[0], int(line[1]))
            else:
                # edge mode
                line = line.split(",")
                pt.AddEdge(line[0], line[1])
    # env, ts, cname, spkuid, spksid
    pt.WriteDot("prod_1714540140000_1123307_22343256_1410479477.dot")