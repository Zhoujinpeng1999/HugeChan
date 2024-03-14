'''
独立运行, 生成配置文件
'''
import argparse
import sys
import os
import json
import random
sys.path.append(sys.path[0] + "/../")
from utils.log import logger

g_machine_id = 200001
g_service_id = 100001

def GetScriptPath():
    return sys.path[0]

def AppendService(a: json, continent, idc, count):
    global g_machine_id, g_service_id
    for i in range(count):
        a["services"].append({
            "continent": continent,
            "idc": idc,
            "machine": g_machine_id,
            "sid": g_service_id
        })
        g_service_id += 1
    g_machine_id += 1


def GeneratePushModeConfig(path):
    a = {}
    a["mode"] = 0
    a["services"] = []
    AppendService(a, "asia", "shanghai", 10)
    AppendService(a, "asia", "shanghai", 10)
    AppendService(a, "asia", "shanghai", 1)
    AppendService(a, "asia", "wuxi", 10)
    AppendService(a, "asia", "beijing", 1)
    AppendService(a, "europe", "frankfurt", 5)
    AppendService(a, "europe", "frankfurt", 5)
    AppendService(a, "america", "newyork", 5)
    AppendService(a, "america", "newyork", 5)
    a["speaker"] = {
        "uid":1234567,
        "cname":"qaq",
        "cid":random.randint(100000, 999999),
        "sid":100001
    }
    with open(path, "w") as f:
        f.write(json.dumps(a, indent=4))
        logger.info("Write json successfully")

def GeneratePullModeConfig(path):
    pass

def GenerateConfig(mode, path):
    pathhhh = ""
    if path == "":
        pathhhh = GetScriptPath() + "/../config/input.json"
    else:
        pathhhh = GetScriptPath() + "/../config/" + path
    if mode == 0:
        GeneratePushModeConfig(pathhhh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成配置参数")
    parser.add_argument('--mode', type=int, help=' 0 - pushmode, 1 - pullmode', default = 0)
    parser.add_argument('--path', type=str, default="")
    args = parser.parse_args()
    GenerateConfig(args.mode, args.path)
