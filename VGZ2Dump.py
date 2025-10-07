import os
import sys
import gzip
import shutil
import subprocess
import platform

# windos check
is_windows = os.name == "nt" or platform.system() == "Windows"

print("VGZ2Dump v1.0.2")
print("Powered by multidumper by maxim-zhao")
print("This script converts a .vgz or .vgm.gz file into a folder with dumps of the PSG/YM2612.")

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    print(f"File received: {file_path}")
    if not os.path.exists(file_path):
        print("File doesn't exist.")
        sys.exit(1)
else:
    file_path = input("Please put in the path of the file you would like to convert: ").strip()
    if not os.path.exists(file_path):
        print("File doesn't exist.")
        sys.exit(1)

file_path = os.path.abspath(file_path)

# Determine folder name
folder_name = os.path.splitext(os.path.basename(file_path))[0]
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
else:
    print(f"Folder '{folder_name}' already exists! All extracted data in the folder will be overridden. Your fault.")

# file the stuff
local_copy = os.path.join(folder_name, os.path.basename(file_path))
shutil.copy(file_path, local_copy)

if local_copy.endswith(".vgz"):
    print("Detected .vgz")
    new_name = os.path.splitext(local_copy)[0] + ".vgm.gz"
    os.rename(local_copy, new_name)
    local_copy = new_name
elif local_copy.endswith(".vgm.gz"):
    print("Detected .vgm.gz")
else:
    print("Invalid file extension. Must be .vgz or .vgm.gz")
    shutil.rmtree(folder_name)
    sys.exit(1)

# vgm.gz -> vgm
vgm_path = os.path.splitext(local_copy)[0]

print(f"Extracting {local_copy} to {vgm_path}...")
with gzip.open(local_copy, "rb") as f_in:
    with open(vgm_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(local_copy)

# heres the multi of the dumper
print(f"Dumping channels into {folder_name}")
script_dir = os.path.dirname(os.path.abspath(__file__))
multidumper_path = os.path.join(script_dir, "dumputil", "multidumper.exe")
target_file = os.path.abspath(vgm_path)

try:
    if is_windows:
        subprocess.run([multidumper_path, target_file], check=True)
    else:
        subprocess.run(["wine", multidumper_path, target_file], check=True)
except subprocess.CalledProcessError as e:
    if e.returncode == 3221226505:
        print("bae you extracted vgm used up by application close da app you dumbfuck")
    else:
        print(f"nah me personally i could never get err {e.returncode}")
    sys.exit(1)

# lean up
os.remove(target_file)
print("Dump successful!")
