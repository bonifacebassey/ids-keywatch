import os
import sounddevice as sd
import threading
from cfg import cfg_output_folder, cfg_add2files, RECORDING_TIME
from datetime import datetime
from scipy.io.wavfile import write


class AudioRecorder:
    def __init__(self, sample_rate=22050, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording_thread = None
        self.is_recording = False

    @staticmethod
    def _generate_filename():
        """Generate a unique filename for the recorder based on the current timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cfg_output_folder(), f"record_{timestamp}.wav")

    def _record_audio(self):
        """Internal method to handle audio recording."""
        while self.is_recording:
            try:
                recording = sd.rec(int(RECORDING_TIME * self.sample_rate), samplerate=self.sample_rate, channels=self.channels)
                sd.wait()  # Wait until the recording is finished

                output_file = self._generate_filename()  # Create a unique filename
                write(output_file, self.sample_rate, recording)  # Save to WAV file
                cfg_add2files(output_file)
            except Exception as e:
                print(f"An error occurred during recording: {e}")

    def start_recording(self):
        """Starts the recording in a separate thread to avoid blocking."""
        if self.is_recording:
            return

        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        """Stops the recording."""
        self.is_recording = False
        if self.recording_thread is not None:
            self.recording_thread.join()  # Ensure the recording thread finishes cleanly
        print("Recording stopped.")
