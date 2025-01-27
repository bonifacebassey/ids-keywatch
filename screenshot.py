import time
import os
from PIL import ImageGrab
from datetime import datetime
from cfg import cfg_output_folder, cfg_add2files


class Screenshot:
    def __init__(self):
        pass

    @staticmethod
    def _generate_filename():
        """Generate a unique filename for the screenshot based on the current timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cfg_output_folder(), f"screenshot_{timestamp}.png")

    def capture(self):
        """Capture a screenshot and save it to a file."""
        output_file = self._generate_filename()  # Create a unique filename
        try:
            # Capture the screenshot
            im = ImageGrab.grab()
            time.sleep(1)  # Optional delay

            # Save the screenshot to a file
            im.save(output_file, format='PNG')
            cfg_add2files(output_file)
        except Exception as e:
            print(f"An error occurred during screenshot capture: {e}")
