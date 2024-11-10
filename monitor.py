from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mitigation import mitigate_process
import time
import logging
from collections import defaultdict
import psutil

# Set up logging to track activity
logging.basicConfig(filename="file_monitor.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Define acess treshold, max allowed file to be acessed
ACCESS_TRESHOLD = 10

# Time window in seconds to check for excessive file access
TIME_WINDOW = 1

# Dictionary to track access counts and time of last check
access_counts = defaultdict(int)
last_checked_time = time.time()


# Define the event handler
class MonitorHandler(FileSystemEventHandler):
    def __init__(self, directory, suspicious_extensions=(".enc",)):
        # Track specific file extensions typically used for encrypted files
        self.suspicious_extensions = suspicious_extensions
        # store the directory or the path in the class
        self.directory = directory 

    def on_modified(self, event):
        """Log and alert if any file modification happens"""
        if not event.is_directory:
            logging.info(f"Modified file detected: {event.src_path}")
            self.check_suspicious_file(event.src_path)
            self.check_excessive_access(self.directory)

    def on_created(self, event):
        """Log and alert if any new file is created"""
        if not event.is_directory:
            logging.info(f"Created file detected: {event.src_path}")
            self.check_suspicious_file(event.src_path)
            self.check_excessive_access(self.directory)

    def on_deleted(self, event):
        """Log if any file is deleted"""
        if not event.is_directory:
            logging.info(f"Deleted file detected: {event.src_path}")

    def check_suspicious_file(self, file_path):
        """Check for suspicious files or modifications based on the file extension"""
        if file_path.endswith(self.suspicious_extensions):
            logging.warning(f"Suspicious file activity detected: {file_path}")
            # Here you could add additional actions, like sending alerts
            print(f"Alert: Suspicious file activity detected on {file_path}")

    # Dunction to check excessive file acess
    def check_excessive_access(self, directory):
        """Moinitor file access rate for each prcoess"""

        # Define the time now
        global last_checked_time 
        current_time = time.time()

        # iterate through all the processess
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.open_files():
                    # for all opened files
                    for open_file in proc.open_files():
                        if directory in open_file.path:
                            access_counts[proc.pid] += 1

                            if current_time - last_checked_time >= TIME_WINDOW:
                                if access_counts[proc.pid] > ACCESS_TRESHOLD:
                                    logging.warning(f"Excessive file access detected for process {proc.name()} (PID: {proc.pid}).")
                                    print(f"Alert: Excessive file access detected for process {proc.name()} (PID: {proc.pid}).")
                                    mitigate_process(proc.pid)

                                # Reset for next time window
                                access_counts[proc.pid] = 0
                                last_checked_time = current_time


            except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue


# Function to start the observer
def start_monitoring(directory):
    event_handler = MonitorHandler(directory=directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"Monitoring started on directory: {directory}")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # a directory that is being monitored
    directory_to_monitor = "C:\\Users\\Public\\Downloads\\test"
    start_monitoring(directory_to_monitor)
