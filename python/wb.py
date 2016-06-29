import threading

from Queue import Queue

white = 1
black = 0
queue = Queue()

year = int(raw_input("input:"))

for i in range(year):
    o_white = white
    o_black = black
    
    white = o_white * 3 + o_black
    black = o_black * 3 + o_white
    
    if white >= 1000000007 & black >= 1000000007 :
        white =white % 1000000007
        black =black % 1000000007
        
white =white % 1000000007
print white
