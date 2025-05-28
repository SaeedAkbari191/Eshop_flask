import psutil
import time


def find_flask_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'app.py' in ' '.join(proc.info['cmdline']):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


proc = find_flask_process()
if not proc:
    print("Flask process not found.")
    exit()

print(f"Monitoring process PID={proc.pid}")
while True:
    cpu = proc.cpu_percent(interval=1)
    mem = proc.memory_info().rss / (1024 * 1024)
    print(f"CPU Usage: {cpu}% | RAM Usage: {mem:.2f} MB")
