from boot import display, wifi
import server

if __name__ == '__main__':
    mode, ip = wifi.get_current_state()
    display.show_message(f"{mode} - Ready", ip or "No connection")
    server.start(display, wifi)
