import subprocess
import time
import pyautogui
import sys

# Safety: moving mouse to a screen corner aborts the script immediately
pyautogui.FAILSAFE = True


def automate():
    print("Launching dummy app...")
    proc = subprocess.Popen([sys.executable, "scripts/dummy_app.py"])
    time.sleep(1.5)  # wait for window to open

    try:
        # Click "Select File" button (approximate position, app opens at
        # default location — adjust if your screen/window position differs)
        print("Clicking Select File...")
        pyautogui.click(x=200, y=60)  # adjust to actual button position
        time.sleep(1)

        # A native file dialog opens — type a filename and press Enter
        # (using a file guaranteed to exist, like this script itself)
        pyautogui.write("dummy_app.py", interval=0.02)
        pyautogui.press("enter")
        time.sleep(1)

        # Click "Run" button
        print("Clicking Run...")
        pyautogui.click(x=200, y=120)

        # Wait for the simulated 2-second processing delay, plus margin
        print("Waiting for completion...")
        time.sleep(3)

        print("Automation sequence complete.")

    finally:
        proc.terminate()


if __name__ == "__main__":
    automate()