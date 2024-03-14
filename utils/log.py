import os
import time
import sys
from loguru import logger

def InitLog(label=""):
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    logger.info("Init logger success!")