import os
import winsound
import time

import config

def jobs_done(window, entireRuntimeStart):
    os.system('cmd /c "MSG %USERNAME% Tasks Completed! && EXIT"')
    winsound.PlaySound("notification", winsound.SND_ALIAS)
    print("Notfication - End of processes")
    print("Notification - Total time:", (time.time() - entireRuntimeStart))
    try:
        window.bring_to_front()
    except Exception:
        print("Alert - Window was not brought to foreground.")
    return

def queue_runner(queueList: list[list], gui_queue):
    r: int = -1
    for queue in queueList:
        individualTaskStartTime = time.time()
        r += 1
        gui_queue.put("0")
        processing.process(queueList[r][0], queueList[r][1], queueList[r][2], gui_queue)
        gui_queue.put("100")  # Multithreading
        print("Notification - Individual task total time:", time.time() - individualTaskStartTime)
    return