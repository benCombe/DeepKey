import time
import itertools
import threading

class ProgressBar:
    def __init__(self, total, size=50, title=None):
        self.total = total
        self.size = size
        self.title = title
        
        self.current = 0
    
    def update(self, n):
        self.current = n
        self.print_progress()


    def print_progress(self):
        # Calculate the number of hashes and spaces
        num_hash = int((self.current / self.total) * self.size)
        num_dash = self.size - num_hash

        # Calculate percentage
        percentage = (self.current / self.total) * 100

        # Print progress bar
        print(
            f"\r{self.title if self.title else ''} "
            f"[{'#' * num_hash}{'-' * num_dash}] {percentage:.2f}%",
            end="",  # Stay on the same line
            flush=True,
        )


class Spinner:
    def __init__(self, msg):
        self.msg = msg
        self.done = False
        self.thread = None

    def start(self):
        """Start the spinner in a separate thread."""
        self.done = False
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def stop(self):
        """Stop the spinner and wait for the thread to finish."""
        self.done = True
        if self.thread:
            self.thread.join()
        print(f"\r{self.msg}... Done!", flush=True)  # Replace spinner with a completion message

    def _spin(self):
        """Spinner animation logic."""
        for char in itertools.cycle('|/-\\'):
            if self.done:
                break
            print(f"\r{self.msg}... {char}", end="", flush=True)
            time.sleep(0.1)
