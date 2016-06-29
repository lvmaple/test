import threading
import time
class mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global x
        lock.acquire()
        for i in range(123):
            x=x+1
        time.sleep(0.0005)
        print x
        lock.release()
lock=threading.RLock()

x = 0
if __name__ == "__main__":
    for i in range(10):
        t = mythread()
        t.start()
    
