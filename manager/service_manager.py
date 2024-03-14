from utils.log import logger
from parse.config_parser import ParseFromFile
from node.node_manager import NodeManager
from forward.edge_service import EdgeServiceInfo, EdgeServiceRole

import sys
import os

class ServiceManager():
    def __init__(self, config_path: str):
        realpath = os.path.dirname(os.path.realpath(__file__))
        if config_path != "":
            self.config_path = realpath + "/../config/" + config_path
        else:
            self.config_path = realpath + "/../config/input.json"
        self.node_manager = NodeManager()

    def Run(self):
        config = ParseFromFile(self.config_path)
        for item in config["services"]:
            self.node_manager.AddService(EdgeServiceInfo(
                item["continent"],
                item["idc"],
                item["machine"],
                item["sid"]
            ))
        self.node_manager.AddChannel(
            config["speaker"]["cid"],
            config["speaker"]["cname"]
        )
        self.node_manager.CreateSpeaker(
            config["speaker"]["sid"],
            config["speaker"]["cid"],
            config["speaker"]["uid"]
        )