import webbrowser
import time

def Time():
    return time.strftime("%H:%M:%S")

def Header():
    while True:
        webbrowser.open("one-ng:?text="+Time())
        time.sleep(1)

if __name__ == '__main__':
    Header()