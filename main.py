from components.display import show_message
from components.wifi import get_current_state
import server

if __name__ == '__main__':
    mode, ip = get_current_state()
    show_message(f"{mode} - Ready", ip or "No connection")
    server.start()