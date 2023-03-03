import os
import subprocess

class scanner:
    def scan():
        path = subprocess.run(["command -v wpa_supplicant"], capture_output=True)
        print(path)