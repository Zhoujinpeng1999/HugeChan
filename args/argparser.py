import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="qaq")
    parser.add_argument('--config', type=str, help='path to config file', default="")
    return parser.parse_args()
