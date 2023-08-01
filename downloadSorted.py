import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

def sort_files(path):
    if os.path.isfile(path) and os.path.exists(path):
        # previde the path for move file
        location = os.path.dirname(path) + os.sep + os.path.basename(path).split(".")[-1]

        # try to create the path if the folder not exist
        try:
            os.makedirs(location)
        except:
            pass
            
        try_time = 1
        file_name = os.path.basename(path)
        
        try:
            # move the file
            os.rename(path, os.path.join(location, file_name))
            
        except FileExistsError:
            # add (numbers) to the file name if the same file name exist
            try_name = file_name[:file_name.rfind('.')] + '(' + str(try_time) + ')' + file_name[file_name.rfind('.'):]
            while os.path.exists(os.path.join(location, try_name)):
                try_time += 1
                try_name = file_name[:file_name.rfind('.')] + '(' + str(try_time) + ')' + file_name[
                                                                                          file_name.rfind('.'):]
            file_name = try_name
            os.rename(path, os.path.join(location, file_name))

        # print the successes message, including the path and end time  
        print(f"File: {file_name} is moved to: {location}")
        finish_time = datetime.now().strftime("%B-%d, %H:%m")
        print(f"Download finished at {finish_time}")

    return

# build the handler to monitor the download folder
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # skip the downloading file
        if not event.src_path.endswith("download") and not event.src_path.endswith("tmp"):
            
            # provide some time to chrome for checking virus
            time.sleep(1)
            sort_files(event.src_path)


observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, os.path.expanduser("~\\Downloads"), False)

# start observer
observer.start()
print("running")

# start loop
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
