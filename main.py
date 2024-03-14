# like remote service organizer

import sys
sys.path.append(sys.path[0])

from args.argparser import parse_args
from manager.service_manager import ServiceManager

if __name__ == "__main__":
    args = parse_args()
    manager = ServiceManager(args.config)
    manager.Run()
