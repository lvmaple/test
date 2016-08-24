import asyncio
import dologin
from bilibiliClient import BilibiliClient
# import threading

dologin.dologin()

danmuji = BilibiliClient()

tasks = [
            danmuji.connectserver() ,
            danmuji.heartbeatloop()
        ]
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
    danmuji.connected = False
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.run_forever()

loop.close()
