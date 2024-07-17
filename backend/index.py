import os
import threading
from time import time


import webview
import serial


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def manual(i):
        ser = serial.Serial("/dev/tty.wchusbserial51850168071", 115200)
        serialCommand = "manual,3"
        ser.write(serialCommand.encode())
        print(serialCommand)
        ser.close()

    def ls(self):
        return os.listdir(".")


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists("../gui/index.html"):  # unfrozen development
        return "../gui/index.html"

    if exists("../Resources/gui/index.html"):  # frozen py2app
        return "../Resources/gui/index.html"

    if exists("./gui/index.html"):
        return "./gui/index.html"

    raise Exception("No index.html found")


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator


entry = get_entrypoint()


@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js(
            'window.pywebview.state.setTicker("%d")' % time()
        )


if __name__ == "__main__":
    window = webview.create_window("pywebview-react boilerplate", entry, js_api=Api(),width=1200, height=800)
    webview.start(update_ticker, debug=True)
