import psutil
import os
import logging

# Function to identify and kill or pause a process
def mitigate_process(process_name="python", suspicious_extension=".enc"):
    """Look for the malicious process and kill or pause it."""
    logging.info(f"Searching for suspicious process: {process_name}")

    # Iterate over all running processes
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            # Check if the process matches the criteria
            if process_name in proc.info['name'] and suspicious_extension in ''.join(proc.info['cmdline']):
                logging.warning(f"Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")

                # Pause the process first
                proc.suspend()
                logging.info(f"Process {proc.info['name']} with PID {proc.info['pid']} has been paused.")

                # Optionally, prompt or take further action (e.g., user confirmation)
                user_action = input("Process paused. Enter 'kill' to terminate, or 'resume' to continue: ")
                if user_action.lower() == "kill":
                    proc.kill()
                    logging.info(f"Process {proc.info['name']} with PID {proc.info['pid']} has been terminated.")
                elif user_action.lower() == "resume":
                    proc.resume()
                    logging.info(f"Process {proc.info['name']} with PID {proc.info['pid']} has been resumed.")
                break
        except psutil.NoSuchProcess:
            continue  # Process might have already ended
