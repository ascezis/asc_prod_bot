import os
import shutil

for root, dirs, files in os.walk(os.path.abspath(".")):
    for file in files:
        if file.endswith(".pyc"):
            path = os.path.join(root, file)
            print(f"Deleting {path}")
            os.remove(path)
    for dir_name in dirs:
        if dir_name == "__pycache__":
            path = os.path.join(root, dir_name)
            print(f"Deleting directory {path}")
            shutil.rmtree(path)
