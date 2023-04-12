from dotenv import load_dotenv
load_dotenv()

from utils.logger import Logger

import time
from datetime import datetime

def main():
    try:
        Logger.instance(["gmail"]).info(f'Start running at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Code for running bot

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()