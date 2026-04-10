import time
from components.display import show_message
import server

if __name__ == '__main__':
    show_message("System OK!", "Load. WebPage")
    time.sleep(1)

    server.start()