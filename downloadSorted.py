import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

def sort_files(path):
    if os.path.isfile(path) and os.path.exists(path):
        location = os.path.dirname(path) + os.sep + os.path.basename(path).split(".")[-1]
        try:
            os.makedirs(location)

        except:
            pass
        try_time = 1
        file_name = os.path.basename(path)
        try:
            os.rename(path, os.path.join(location, file_name))
        except FileExistsError:
            try_name = file_name[:file_name.rfind('.')] + '(' + str(try_time) + ')' + file_name[file_name.rfind('.'):]
            while os.path.exists(os.path.join(location, try_name)):
                try_time += 1
                try_name = file_name[:file_name.rfind('.')] + '(' + str(try_time) + ')' + file_name[
                                                                                          file_name.rfind('.'):]
            file_name = try_name
            os.rename(path, os.path.join(location, file_name))

        print(f"File: {file_name} is moved to: {location}")
        finish_time = datetime.now().strftime("%B-%d, %H:%m")
        print(f"Download finished at {finish_time}")

    return


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.src_path.endswith("download") and not event.src_path.endswith("tmp"):
            time.sleep(1)
            sort_files(event.src_path)


observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, os.path.expanduser("~\\Downloads"), False)
observer.start()
print("running")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
