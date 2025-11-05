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
    ts = "1762248240000"
    cname = 'liveshow2'
    spkuid = 1
    file_name = "prod_{ts}_{cname}_{uid}.dot".format(
        ts = ts, cname = cname, uid = spkuid
    )
    print("file_name:{}".format(file_name))
    pt.WriteDot(file_name)