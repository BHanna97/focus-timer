import win32gui
import time


def get_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


active_time = 0
start_time = 0

try:
    while True:
        active_window = get_active_window()
        if 'Visual Studio Code' in active_window:
            if start_time == 0:
                start_time = time.time()
        else:
            if start_time != 0:    
                active_time += time.time() - start_time
                start_time = 0
        
        time.sleep(1)




except KeyboardInterrupt:
    if start_time:
        active_time += time.time() - start_time #account for an ongoing session
    
    print(f"Time elapsed: {active_time / 60:.2f} minutes")